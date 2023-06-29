import tiktoken
from datasets import load_dataset
import os
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from getpass import getpass
from langchain.embeddings.openai import OpenAIEmbeddings

#export OPENAI_API_KEY = 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
# Load the OpenAI API key from an environment variable
api_key = os.environ["OPENAI_API_KEY"]

# Set the OpenAI API key
tiktoken.set_openai_key(api_key)

tokenizer = tiktoken.get_encoding('cl100k_base')
# Load the dataset or read the Excel file
df = pd.read_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/CSCL_1995_fullcopy.xlsx', engine='openpyxl')

# Create the length function
def tiktoken_len(text):
    tokens = tokenizer.encode(text)
    return len(tokens)

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
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

embed = OpenAIEmbeddings(
    model=model_name,
    openai_api_key=api_key
)
texts = [
    'this is the first chunk of text',
    'then another second chunk of text is here'
]

res = embed.embed_documents(texts)
print(len(res), len(res[0]))
