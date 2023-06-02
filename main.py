import config
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader, OnlinePDFLoader
import pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.vectorstores import Chroma

### Imports for LLM + Chat Functionality ###
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.tools.base import StructuredTool
from langchain.agents import initialize_agent, AgentType, load_tools

from tooltest import summarize_algorithm
### END IMPORTS FOR LLM FUNCTIONALITY ###



openai_api_key = config.OPENAI_KEY
pinecone_api_key = config.PINECONE_KEY
pinecone_api_env = config.PINECONE_ENV

os.environ['OPENAI_API_KEY'] = openai_api_key

def getSimilarDocs(database, prompt):
    docs = database.similarity_search_with_score(prompt)
    return docs


### Loading in text file with stored learnings and splitting into docs for vector storage ###
loader = TextLoader('algorithms.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)


### DOING SAME THING WITH CHROMA ### 
# loader = TextLoader('algorithms.txt')
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)
### END CHROMA ###

### Creating embeddings and storing in vector storage ###
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

### EMBEDDINGS WITH CHROMA 
# embeddings = OpenAIEmbeddings()
# db = Chroma.from_documents(docs, embeddings)
### END CHROMA ###

### Retrieval with a prompt ### *** NOTE: SEEMS LIKE a lower similarity score means it's more similar.
# query = "Please solve the game of 24 with the following numbers: 3, 6, 3, 3"
# results = getSimilarDocs(db, query)
# pg = results[0][0].page_content
# mtdt = results[0][0].metadata
# similarity_score = results[0][1]

# print("page content: ", pg)
# print("metadata: ", mtdt)
# print("results[0][1]: ", similarity_score)

# if (similarity_score < 0.4): # Should we use this algorithm
#     print("We can use this background: ", pg)
# else:
#     print("It is unclear whether there is a strategy we should employ. The closest we could find is this: ", pg)


# prompt = input("Please input a question: ")



### Testing QA Chain ###
# qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=db.as_retriever())
# query = "Find an algorithm relevant to this question: " + prompt + "... Then summarize it in bullet points. If there is no information that will help you solve the question, respond \"None\"."
# answer = qa.run(query)
# print(answer)

summarization_tool = StructuredTool.from_function(summarize_algorithm)

# answer = summarization_tool(prompt)
chat = ChatOpenAI(model_name="gpt-4", temperature=0.2)
llm = OpenAI(temperature=0.2)
tools = load_tools(["llm-math"], llm)
tools.append(summarization_tool)

agent_chain = initialize_agent(tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# agent_chain()
agent_chain.run("The game of 24 seeks to reach the number 24 by using a combination of the four basic mathematical operations on the four numbers given. Find a solution to the game of 24 using the numbers 8, 8, 4, and 4. Look for an algorithm or strategy first. Remember, the algorithm isn't the final solution. Solve the problem being posed. Think step by step.")


# if ("None" in answer):
#     print("Wah wah wahhhhh...")
# else:
#     ### Chat time ###
#     human_template = "Using the following strategy or algorithm: {algorithm} \n... Solve this problem: {prompt}. Think step by step, and number your steps."
#     system_template = "You are a helpful assistant that solves problems using strategies and algorithms provided to you."
#     human_prompt = HumanMessagePromptTemplate.from_template(human_template)
#     system_prompt = SystemMessagePromptTemplate.from_template(system_template)

#     chat = ChatOpenAI(temperature=0)
#     chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
#     formattedPrompt = chat_prompt.format_prompt(algorithm=answer, prompt=prompt).to_messages()
#     print(formattedPrompt, "##########")
#     chatResult = chat(formattedPrompt)
#     print(chatResult)





