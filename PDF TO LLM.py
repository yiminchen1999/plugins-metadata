
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS

# Get your API keys from openai, you will need to create an account.
# Here is the link to get the keys: https://platform.openai.com/account/billing/overview
import os
os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI-API-KEY"

# connect Google Drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth=GoogleAuth()
gauth.LocalWebserverAuth()
drive=GoogleDrive(gauth)
root_dir = "https://drive.google.com/drive/folders/1im_lRhTiyB2tqj9gHyC3MzzIg4taLEPz"

# location of the pdf file/files. a example
reader = PdfReader('https://drive.google.com/file/d/1loUdhb4x-FzRjXdgnKVgEvruHaet2yAL/view?usp=drive_link')

reader

# read data from the file and put them into a variable called raw_text
raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# raw_text

raw_text[:100]

# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits.

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

len(texts)

texts[0]

texts[1]

# Download embeddings from OpenAI
embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)

docsearch

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

chain = load_qa_chain(OpenAI(), chain_type="stuff")

query = "who are the authors of the article?"
docs = docsearch.similarity_search(query)
chain.run(input_documents=docs, question=query)

query = "What was the abstract?"
docs = docsearch.similarity_search(query)
chain.run(input_documents=docs, question=query)



