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
from langchain.agents import initialize_agent, AgentType, load_tools, ZeroShotAgent, Tool, AgentExecutor

from customTools import summarize_algorithm, write_report
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain.memory import ConversationBufferMemory
### END IMPORTS FOR LLM FUNCTIONALITY ###



openai_api_key = config.OPENAI_KEY
pinecone_api_key = config.PINECONE_KEY
pinecone_api_env = config.PINECONE_ENV

os.environ['OPENAI_API_KEY'] = openai_api_key

def getSimilarDocs(database, prompt):
    docs = database.similarity_search_with_score(prompt)
    return docs

def gameOf24():
    summarization_tool = StructuredTool.from_function(summarize_algorithm)
    serialization_tool = StructuredTool.from_function(write_report)

    chatllm = ChatOpenAI(model_name="gpt-4", temperature=0.2)
    llm = OpenAI(temperature=0.1, model_name='text-davinci-002')
    tools = load_tools(["llm-math"], llm)
    # tools.append(summarization_tool)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True, return_intermediate_steps=True)    # output1 = agent_chain("We're going to play the game of 24. Look for an algorithm or strategy first.")
    prompt1 = "The game of 24 seeks to combine four numbers with the four basic mathematical operations to reach 24. Solve the game of 24 with the numbers 3, 9, 2, and 1."
    output1 = agent(prompt1)
    print(output1["intermediate_steps"])
    import json
    historyAsString = json.dumps(output1["intermediate_steps"], indent=2)



    prompt2 = "Your goal was this: " + prompt1 + "\n" + "Here are the steps you took to solve a problem: " + historyAsString + "\n What was your final answer? What did you do right? What did you do wrong?"
    print(prompt2)
    output2 = chatllm([HumanMessage(content=prompt2)])
    print(output2)
    
    # output1 = agent_chain.run(input="Find a strategy with which to solve the game of 24 and list the mistakes to avoid.")
    # output2 = agent_chain.run(input="Make a concrete and concise plan to avoid the above mistakes.")
    # output3 = agent_chain.run(input="Using this plan and strategy, use the four basic operations to calculate a solution with the numbers, 2, 6, 8, and 4. Don't stop until you've reached 24.")
    # "The game of 24 seeks to reach the number 24 by using a combination of the four basic mathematical operations on the numbers given. Calculate a solution to the game of 24 with the numbers 2, 4, 8, 1. Don't guess that something is the right answer. You don't know the final answer until you've verified it mathematically. Begin by looking for a good strategy."
    # print(output["intermediate_steps"])
    # import json
    # historyAsString = json.dumps(output["intermediate_steps"], indent=2)
    # output2 = llm("This is the output history from the problem you just solved: " + historyAsString + "... Based on the user's prompt and rules, did you solve the problem correctly? If so, describe your thinking. If not, explain what you did wrong.")
    # print(output2)




def findRecipe():
    summarization_tool = StructuredTool.from_function(summarize_algorithm)
    llm = OpenAI(temperature=0.1)
    tools = load_tools(["serpapi"], llm)
    # tools.append(summarization_tool)
    agent_chain = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    agent_chain.run("Find a good Christmas recipe. Break it down step by step.")

gameOf24()
# findRecipe()

##### PLAN AND EXECUTE
# model = ChatOpenAI(temperature=0)
# planner = load_chat_planner(model)
# executor = load_agent_executor(model, tools, verbose=True)
# agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
# agent.run("Solve the game of 24 with the numbers 8, 2, 4, and 4. Find one past algorithm or strategy first.")





