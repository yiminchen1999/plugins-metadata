import tiktoken
import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from getpass import getpass
from langchain.embeddings.openai import OpenAIEmbeddings
import json
from sklearn.metrics.pairwise import cosine_similarity
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from tqdm.auto import tqdm
import logging
from uuid import uuid4
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='debug.log'
)
# Load the OpenAI API key from an environment variable
with open('config.json') as config_file:
    config = json.load(config_file)
    api_key = config['OPENAI_API_KEY']
    pinecone_api_key = config['PINECONE_API_KEY']

tokenizer = tiktoken.get_encoding('cl100k_base')

# Load the dataset or read the Excel file
df = pd.read_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/CSCL_1995_fullcopy.xlsx', engine='openpyxl')

# Create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(text)
    return len(tokens)

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_text(df['content'])[:3]
print(chunks)

print(tiktoken_len(chunks[0])) # 201
print(tiktoken_len(chunks[1])) # 198
print(tiktoken_len(chunks[2])) # 204

model_name = 'text-embedding-ada-002'

def embed_query(texts):
    embeddings = embed.embed_documents(texts)
    return embeddings

embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=api_key
)

texts = [
    'this is the first chunk of text',
    'then another second chunk of text is here'
]

res = embed_query(texts)
print(len(res), len(res[0])) # 2 1536
import pinecone
# Commented out index creation
# Create a new index
index_name = 'langchain-retrieval-augmentation'

pinecone.init(
     api_key=pinecone_api_key,
    environment=config['PINECONE_ENVIRONMENT']
 )

# Get the list of all indexes
indexes = pinecone.list_indexes()

# Check if the index exists
#if indexes is not None and index_name in indexes:
    # Clear the index
    #pinecone.delete_index(index_name)
    #print(f"Index '{index_name}' has been cleared.")
#else:
    #print(f"Index '{index_name}' does not exist.")


index = pinecone.Index(index_name=index_name)
index.describe_index_stats()
# Batch upsert operation
batch_limit = 100

texts = []
metadatas = []
logging.info('Starting file processing...')
for i, record in enumerate(tqdm(df)):
    # First get metadata fields for this record
    metadata = {
        'id': str(df['id'].values[0]),
        'source': str(df['dc.identifier.uri'].values[0]),
        'title': str(df['title'].values[0])
    }
    # Create chunks
    record_texts = text_splitter.split_text(df['content'])
    # Continued from previous code snippet

    record_metadatas = [{
        "chunk": j, "content": content, **metadata
    }for j, content in enumerate(record_texts)]

    # Append these to current batches
    texts.extend(record_texts)
    metadatas.extend(record_metadatas)
    # If reach batch limit or the last record
    # if we have reached the batch_limit we can add texts
    if len(texts) >= batch_limit:
        ids = [str(uuid4()) for _ in range(len(texts))]
        embeds = embed.embed_documents(texts)
        index.upsert(vectors=zip(ids, embeds, metadatas))
        texts = []
        metadatas = []

if len(texts) > 0:
    ids = [str(uuid4()) for _ in range(len(texts))]
    embeds = embed.embed_documents(texts)
    index.upsert(vectors=zip(ids, embeds, metadatas))

# Verify the upserted items
index.describe_index_stats()

