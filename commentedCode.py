########## CODE FOR GETTING SIMILAR DOCS WITH SIMILARITY SCORE ###
### Loading in text file with stored learnings and splitting into docs for vector storage ###
# loader = TextLoader('algorithms.txt')
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# texts = text_splitter.split_documents(documents)

# ### Creating embeddings and storing in vector storage ###
# embeddings = OpenAIEmbeddings()
# db = FAISS.from_documents(texts, embeddings)

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



###### OLD VERSION ######
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



### USING CONVERSATIONMEMORY ###
# prefix = """You're a helpful problem solver and you apply your past knowledge to solving problems the human gives to you."""
#     suffix = """Begin!"

#     {chat_history}
#     Question: {input}
#     {agent_scratchpad}"""

#     prompt = ZeroShotAgent.create_prompt(
#         tools, 
#         prefix=prefix, 
#         suffix=suffix, 
#         input_variables=["input", "chat_history", "agent_scratchpad"]
#     )
#     memory = ConversationBufferMemory(memory_key="chat_history")
#     llm_chain = LLMChain(llm=OpenAI(temperature=0.2), prompt=prompt)
#     agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    # agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)
    
    # agent_chain.run(input="The game of 24 seeks to reach the number 24 by using a combination of the four basic mathematical operations on the four numbers given. 1) First, find a solution to the game of 24 with the numbers 12, 4, 2, and 1. Don't just guess that something is the right answer. You don't know the final answer until you've verified it.")
    # print(agent_chain.memory)
    # agent_chain.run(input="Once you've found a solution, decide whether your approach was good. If it was, serialize it into a series of steps for a future system to follow on similar problems.")
    
    
    # agent_chain.run(input="what's its population?")

    # agent = ZeroShotAgent(llm=llm, tools=tools, verbose=True)
    # agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=ConversationBufferMemory())
    