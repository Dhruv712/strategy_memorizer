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
    # Loading in Algorithms.txt
    loader = TextLoader('algorithms.txt')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    # Loading in Feedback.txt
    feedbackLoader = TextLoader('mistakes.txt')
    feedbackDocs = feedbackLoader.load()
    feedback_text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    feedbackTexts = feedback_text_splitter.split_documents(feedbackDocs)
    feedbackEmbeddings = OpenAIEmbeddings()
    feedbackDB = FAISS.from_documents(feedbackTexts, feedbackEmbeddings)

    relevant_feedback = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=feedbackDB.as_retriever())
    feedbackQuery = "Given this prompt: " + prompt + "... Find relevant mistakes to learn from. List them concisely."
    feedback = relevant_feedback.run(feedbackQuery)
    # print(feedback)

    # qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=db.as_retriever())
    # query = "From this document, find the algorithm relevant to this question: " + prompt + " \n Then summarize it as a series of steps."
    # answer = qa.run(query)
    query = prompt
    # retriever = db.as_retriever()
    results = db.similarity_search(query)
    pg = results[0].page_content
    return pg, feedback


def summarize_algorithm(
        prompt: Optional[str] = None                  
) -> str:
    """Tool that, given a problem, finds a relevant strategy for solving it."""
    summary, feedback = findAlgorithm(prompt)
    # summary += ("\nAvoid the following mistakes: " + feedback)
    return summary

def write_report(
        prompt: Optional[str] = None                  
) -> str:
    """Tool that serializes the steps taken to solve a problem into a plan for a future system to use on similar problems."""
    llm = OpenAI(temperature=0.2)
    serialization = llm(prompt)
    with open('reports.txt', 'w') as f:
        f.write(serialization)
    return serialization


