# Milestone 3: Multi-Agent Orchestration & Memory
# GROQ API + llama-3.1-8b-instant
# LangChain 1.x | Single File
import os
from dotenv import load_dotenv
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.memory import VectorStoreRetrieverMemory
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS




# LOAD ENV VARIABLES
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError(" GROQ_API_KEY not found in .env")

# GROQ LLM
from langchain_groq import ChatGroq
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.3
)

print(" Groq LLM loaded (llama-3.1-8b-instant)")

research_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

summary_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

reasoning_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# SHARED VECTOR MEMORY (LOCAL)
embeddings = FakeEmbeddings(size=384)
vector_store = FAISS.from_texts(
    texts=["Shared memory initialized"],
    embedding=embeddings
)
shared_memory = VectorStoreRetrieverMemory(
    retriever=vector_store.as_retriever(search_kwargs={"k": 3})
)
# PROMPTS
from langchain_core.prompts import ChatPromptTemplate


research_prompt = ChatPromptTemplate.from_messages([
    ("human", "You are a Research Agent. Research the following topic:\n{input}")
])

summary_prompt = ChatPromptTemplate.from_messages([
    ("human", "You are a Summarizer Agent. Summarize the following:\n{input}")
])

reasoning_prompt = ChatPromptTemplate.from_messages([
    ("human", "You are a Reasoning Agent. Use shared memory and summary to conclude:\n{input}")
])

# AGENTS
from langchain_classic.chains import LLMChain
research_agent = LLMChain(
    llm=llm,
    prompt=research_prompt,
    memory=research_memory
)

summarizer_agent = LLMChain(
    llm=llm,
    prompt=summary_prompt,
    memory=summary_memory
)

reasoning_agent = LLMChain(
    llm=llm,
    prompt=reasoning_prompt,
    memory=reasoning_memory
)

# ORCHESTRATOR
def orchestrator(user_query: str):
    print("\n🔍 Research Agent Running...")
    research_output = research_agent.run(user_query)
    shared_memory.save_context({"input": user_query}, {"output": research_output})
    print("\n Summarizer Agent Running...")
    summary_output = summarizer_agent.run(research_output)
    shared_memory.save_context({"input": research_output}, {"output": summary_output})
    print("\n Reasoning Agent Running...")
    shared_context = shared_memory.load_memory_variables({"input": user_query})["history"]
    final_answer = reasoning_agent.run(
        f"Shared Memory:\n{shared_context}\n\nSummary:\n{summary_output}"
    )
    shared_context = shared_memory.load_memory_variables({"input": user_query})["history"]
    return final_answer

# MAIN
if __name__ == "__main__":
    query = "Explain how multi-agent systems use memory to improve decision making"
    result = orchestrator(query)
    print("\n FINAL OUTPUT\n")
    print(result)
