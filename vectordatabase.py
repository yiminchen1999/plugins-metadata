import tiktoken
import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from getpass import getpass
from langchain.embeddings.openai import OpenAIEmbeddings
import json


#如果要使用code记得下载config.json
with open('config.json') as config_file:
    config = json.load(config_file)
    api_key = config['OPENAI_API_KEY']
    pinecone_api_key = config['PINECONE_API_KEY']


# export OPENAI_API_KEY=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
#echo "export OPENAI_API_KEY='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'" >> ~  /Users/chenyimin

# Load the OpenAI API key from an environment variable
#api_key = os.environ["OPENAI_API_KEY"]
#api_key = os.environ.get('OPENAI_API_KEY')
#OPENAI_API_KEY = getpass("OpenAI API Key: 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")

#check the key
#for key, value in os.environ.items():
    #print(f"{key}={value}")
import tiktoken
tokenizer = tiktoken.get_encoding('cl100k_base')
# Load the dataset or read the Excel file
df = pd.read_excel('/content/CSCL_1995_fullcopy.xlsx')
tiktoken.encoding_for_model('gpt-3.5-turbo')
def embed_query(texts):
    embeddings = embed.embed_documents(texts)
    return embeddings
# Create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)



from langchain.text_splitter import RecursiveCharacterTextSplitter
# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1100,
    chunk_overlap=40,
    length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_text(df[2:3]['text'])[:3]
chunks

print(tiktoken_len(chunks[0])) # 201
print(tiktoken_len(chunks[1])) # 198
print(tiktoken_len(chunks[2])) # 204

model_name = 'text-embedding-ada-002'
from sklearn.metrics.pairwise import cosine_similarity

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
print(len(res), len(res[0]))# 2 1536

#move to the pinecone vector database
import pinecone

# find API key in console at app.pinecone.io
#YOUR_API_KEY = getpass("Pinecone API Key:af46e200-9246-45a0-bc1d-3cdc544b9d2b")
# find ENV (cloud region) next to API key in console

index_name = 'langchain-retrieval-augmentation'


pinecone.init(
    api_key=config['PINECONE_API_KEY'],
    environment=config['PINECONE_ENVIRONMENT']
)

if index_name not in pinecone.list_indexes():
    # we create a new index
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=len(res[0])  # 1536 dim of text-embedding-ada-002
    )
index = pinecone.Index(index_name=index_name)

index.describe_index_stats()

#INDEXING
from tqdm.auto import tqdm
from uuid import uuid4

batch_limit = 100

#处理大小大于2MB的最大支持大小，导致了 "请求太多 "的错误。
# 要解决这个问题，你需要进一步减少批处理的大小，以确保它适合在允许的限制内。
content = []
metadatas = []

for i, record in enumerate(tqdm(df)):
    # first get metadata fields for this record
    metadata = {
        'id': str(df['id'].values[0]),
        'source': str(df['dc.identifier.uri'].values[0]),
        'title': str(df['title'].values[0])
    }
    # create chunks
    record_content = text_splitter.split_text(df['content'])
    # create individual metadata dicts for each chunk
    record_metadatas = [{
        "chunk": j, "content": content, **metadata
    } for j, content in enumerate(record_content)]
    # append these to current batches
    content.extend(record_content)
    metadatas.extend(record_metadatas)
    # if reach batch_limit then add texts
    if len(content) >= batch_limit:
        batches = [content[i:i + batch_limit] for i in range(0, len(content), batch_limit)]
        batch_metadatas = [metadatas[i:i + batch_limit] for i in range(0, len(metadatas), batch_limit)]
        for batch, metadata_batch in zip(batches, batch_metadatas):
            ids = [str(uuid4()) for _ in range(len(batch))]
            embeds = embed_query(batch)
            index.upsert(vectors=zip(ids, embeds, metadata_batch))
        content = []
        metadatas = []

# Upsert the remaining vectors
if len(content) > 0:
    ids = [str(uuid4()) for _ in range(len(content))]
    embeds = embed_query(content)
    index.upsert(vectors=zip(ids, embeds, metadatas))

index.describe_index_stats()


from langchain.vectorstores import Pinecone

text_field = "content"

# switch back to normal index for langchain
index = pinecone.Index(index_name)

vectorstore = Pinecone(
    index, embed.embed_query, text_field
)

query = "who was Benito Mussolini?"

vectorstore.similarity_search(
    query,  # our search query
    k=3  # return 3 most relevant docs
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# completion llm
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

qa.run(query)

from langchain.chains import RetrievalQAWithSourcesChain

qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

qa_with_sources(query)


