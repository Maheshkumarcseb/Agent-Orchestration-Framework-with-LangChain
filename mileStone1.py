import os
import re
import math
import requests
from dotenv import load_dotenv

#  Load Gemini API key 
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

# LLM (Google Gemini) 
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0.7
)
print(" Gemini Model Loaded Successfully\n")

#  MEMORY 
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# SAFE CALCULATOR TOOL 
def safe_calculator(expression: str) -> str:
    """Evaluate math expressions safely."""
    if not re.fullmatch(r"[0-9+\-*/().^ ]+", expression):
        return "Invalid calculation input."

    try:
        expression = expression.replace("^", "**")
        result = eval(expression, {"__builtins__": {}}, math.__dict__)
        return f" Result: {result}"
    except Exception as e:
        return f" Calculation error: {e}"

# WEATHER TOOL 
def weather_tool(city: str) -> str:
    """Fetch current temperature using wttr.in"""
    city = city.strip()
    if not city:
        return " Please provide a city name."
    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url, timeout=5).json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0].get("weatherDesc", [{}])[0].get("value", "")
        return f" Temperature in {city}: {temp}°C ({desc})"
    except Exception:
        return " Weather service unavailable."

#  GEMINI QUESTION TOOL 
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

template = """
You are an expert AI assistant.
Answer clearly and simply:

Question: {question}
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

def qa_tool(question: str) -> str:
    return chain.run({"question": question})

#TOOLS 
from langchain.tools import Tool

tools = [
    Tool(name="Calculator", func=safe_calculator, description="Solve math expressions like: 24*(5+4)"),
    Tool(name="Weather", func=weather_tool, description="Get current weather by city name"),
    Tool(name="QuestionAnswer", func=qa_tool, description="Answer general knowledge or explanation questions")
]

# ZERO-SHOT AGENT 
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

print(" Gemini Zero-Shot Agent is READY with Tools + Memory!\n")

# CLI LOOP 
print("Chatbot ready. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["exit", "quit"]:
        print(" Goodbye!")
        break

    try:
        response = agent.run(user_input)
        print("Agent:", response, "\n")
    except Exception as e:
        print(" Error:", str(e), "\n")
