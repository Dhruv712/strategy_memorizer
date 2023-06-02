import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader, OnlinePDFLoader
import pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from typing import Optional
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

load_dotenv(find_dotenv())

def findAlgorithm(prompt):
    loader = TextLoader('algorithms.txt')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=db.as_retriever())
    query = "Find an algorithm relevant to this question: " + prompt + "... Then summarize it in bullet points."
    answer = qa.run(query)
    return answer


def summarize_algorithm(
        prompt: Optional[str] = None                  
) -> str:
    """Tool that accepts a problem, finds an algorithm or strategy to solve that problem, and summarizes the algorithm in bullets."""
    chat = ChatOpenAI(model_name="gpt-4", temperature=0.2)
    summary = findAlgorithm(prompt)
    # print("SUMMARY: " + summary)
    # prompt = "Use this algorithm: " + summary + "... to solve this problem: " + prompt
    # answer = chat([HumanMessage(content=prompt)])
    # return answer
    return summary



