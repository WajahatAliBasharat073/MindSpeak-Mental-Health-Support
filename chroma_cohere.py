import os
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Cohere
from langchain.chains import VectorDBQA
from langchain.document_loaders import PyMuPDFLoader


COHERE_API_KEY="Put you API key here"

def generate_prompt(query, file_path):

    print('query:', query)

    loader = PyMuPDFLoader("static/files/book.pdf")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # embeddings = CohereEmbeddings(cohere_api_key="Put you API key here")
    embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
    vectordb = Chroma.from_documents(texts, embeddings)

    qa = VectorDBQA.from_chain_type(llm=Cohere(cohere_api_key=COHERE_API_KEY), chain_type="stuff", vectorstore=vectordb)

    prompt = qa.run(query)

    if prompt == "":
        return ""
    
    print('prompt:', prompt)
    
    return prompt.strip()