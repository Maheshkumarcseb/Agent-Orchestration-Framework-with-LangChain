#######   MILESTONE 2: INTEGRATING MULTIPLE TOOLS WITH GEMINI MODEL #######
import os
import random
import re
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import SystemMessagePromptTemplate

# LOAD ENV VARIABLES
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(" GOOGLE_API_KEY missing in .env file")

# TOOL CALCULATOR
def calculator_tool(expression: str) -> str:
    """Safely evaluate mathematical expressions."""
    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Error: Invalid mathematical expression."


# TOOL : SIMULATED WEATHER API
def weather_tool(city: str) -> str:
    """Returns a simulated weather response."""
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Stormy"]
    temp = random.randint(20, 34)
    condition = random.choice(conditions)
    return f"Weather in {city}: {temp}°C, {condition} (simulated)"



# TOOL : FILE SEARCH TOOL (Sentence-based)
def file_search_tool(keyword: str) -> str:
    """
    Searches inside sample.txt for sentences containing the given keyword.
    User only provides the keyword.
    Example: LangChain
    """
    file_name = "sample.txt"
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            text = f.read()

        sentences = re.split(r'(?<=[.!?]) +', text)
        matches = [s.strip() for s in sentences if keyword.lower() in s.lower()]

        if matches:
            return "Matches found:\n" + "\n".join(matches)

        return f"No matches found for keyword '{keyword}'."

    except FileNotFoundError:
        return f"Error: Default file '{file_name}' not found."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# TOOL : TEXT SUMMARIZER
def text_summarizer_tool(text: str) -> str:
    """
    Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century, fundamentally reshaping the way industries operate and societies function. AI systems are designed to simulate human intelligence by learning from data, recognizing patterns, making decisions, and continuously improving over time. These systems rely on advanced algorithms, machine learning models, and large datasets to perform complex tasks that were traditionally handled by humans.

In the healthcare sector, AI is being used to enhance diagnostic accuracy, personalize treatment plans, and streamline administrative processes. Machine learning models can analyze medical images, detect diseases at early stages, and assist doctors in making more informed decisions. AI-powered tools also help in drug discovery by identifying potential compounds and predicting their effectiveness, significantly reducing research time and costs.

The financial industry has also embraced AI to improve efficiency, security, and customer experience. AI-driven fraud detection systems monitor transactions in real time, identifying suspicious patterns and preventing unauthorized activities. Chatbots and virtual assistants powered by natural language processing provide instant customer support, handle routine inquiries, and improve service availability. Additionally, algorithmic trading systems leverage AI to analyze market trends and execute trades with minimal human intervention.

In manufacturing and supply chain management, AI enables predictive maintenance, quality control, and demand forecasting. Sensors and AI models work together to detect equipment failures before they occur, minimizing downtime and reducing operational costs. AI-driven analytics help organizations optimize inventory levels, manage logistics, and respond quickly to market changes.

Despite its benefits, the widespread adoption of AI also raises ethical and social concerns. Issues such as data privacy, algorithmic bias, job displacement, and transparency must be carefully addressed. Ensuring responsible AI development requires strong governance frameworks, ethical guidelines, and collaboration between governments, organizations, and researchers. As AI continues to evolve, balancing innovation with ethical responsibility will be critical to maximizing its positive impact on society.
    """
    try:
        sentences = re.split(r'(?<=[.!?]) +', text)

        if len(sentences) <= 2:
            return "Summary:\n" + text

        summary = " ".join(sentences[:2])
        return "Summary:\n" + summary

    except Exception as e:
        return f"Error while summarizing text: {str(e)}"

# REGISTER TOOLS WITH LANGCHAIN
tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Perform mathematical calculations. Example: 12 + 48 / 3"
    ),
    Tool(
        name="WeatherAPI",
        func=weather_tool,
        description="Get simulated weather for any city"
    ),
    Tool(
        name="FileSearch",
        func=file_search_tool,
        description="Search inside sample.txt for a keyword. Example: LangChain"
    ),
    Tool(
        name="TextSummarizer",
        func=text_summarizer_tool,
        description="Summarize a given paragraph of text"
    )
]

# INITIALIZE GEMINI MODEL
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

# SYSTEM PROMPT
system_prompt = SystemMessagePromptTemplate.from_template(
    """
You are an intelligent LangChain Agent with access to four tools:

1. Calculator → Use for ANY math.
2. WeatherAPI → Use for ANY weather question.
3. FileSearch → Use for searching inside sample.txt.
4. TextSummarizer → Use to summarize long text.

Rules:
- ALWAYS use a tool when needed.
- NEVER guess numbers or weather.
- For file search, extract only sentences containing the keyword.
- If no tool is needed, answer normally.
- If a tool fails, return a helpful message.
"""
)

# INITIALIZE AGENT
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="chat-zero-shot-react-description",
    verbose=True,
    max_iterations=3,
    handle_parsing_errors=True
)

# DEMO USING invoke()
def run_demo():
    print("\n--- Milestone 2 Demo (Gemini + 4 Tools) ---\n")

    queries = [
        "What is 12 + 48 / 3?",
        "What is the weather in Bengaluru?",
        "Search in the file for LangChain",
        "Summarize this text: LangChain is a framework for building LLM-powered applications. It enables tool integration, memory, and agent orchestration. It is widely used in modern AI systems.",
        "Explain what tools you used above.",
        "What is 100 / (5 - 5)?"
    ]

    for q in queries:
        print(f"\nUser: {q}")
        try:
            response = agent.invoke({"input": q})
            print("Agent:", response["output"])
        except Exception as e:
            print(f"Agent: Error: {str(e)}")


if __name__ == "__main__":
    run_demo()



















#######   MILESTONE 2: INTEGRATING MULTIPLE TOOLS WITH GROK MODEL #######
###### USE GROKENV FOR RUNNING THE BELOW CODE ###############


# import os
# import random
# import re
# from dotenv import load_dotenv

# from langchain_core.tools import Tool

# from langchain_classic.agents import initialize_agent


# from langchain_groq import ChatGroq
# from langchain_core.prompts import SystemMessagePromptTemplate



# # 0. LOAD ENV VARIABLES

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY missing in .env file")


# # 1. TOOL: CALCULATOR

# def calculator_tool(expression: str) -> str:
#     try:
#         result = eval(expression)
#         return str(result)
#     except Exception:
#         return "Error: Invalid mathematical expression."



# #  TOOL: SIMULATED WEATHER API


# def weather_tool(city: str) -> str:
#     conditions = ["Sunny", "Cloudy", "Rainy", "Windy", "Stormy"]
#     temp = random.randint(20, 34)
#     condition = random.choice(conditions)
#     return f"Weather in {city}: {temp}°C, {condition} (simulated)"



# #  TOOL: FILE SEARCH TOOL (Sentence-based Search)


# def file_search_tool(keyword: str) -> str:
#     file_name = "sample.txt"

#     try:
#         with open(file_name, "r", encoding="utf-8") as f:
#             text = f.read()

#         # Split into sentences
#         sentences = re.split(r'(?<=[.!?]) +', text)

#         # Find matches
#         matches = [s.strip() for s in sentences if keyword.lower() in s.lower()]

#         if matches:
#             return "Matches found:\n" + "\n".join(matches)

#         return f"No matches found for keyword '{keyword}'."

#     except FileNotFoundError:
#         return f"Error: Default file '{file_name}' not found."
#     except Exception as e:
#         return f"Unexpected error: {str(e)}"



# #  REGISTER TOOLS WITH LANGCHAIN


# tools = [
#     Tool(
#         name="Calculator",
#         func=calculator_tool,
#         description="Perform math calculations. Example: 12 + 48 / 3"
#     ),
#     Tool(
#         name="WeatherAPI",
#         func=weather_tool,
#         description="Get simulated weather information."
#     ),
#     Tool(
#         name="FileSearch",
#         func=file_search_tool,
#         description="Search inside sample.txt for a keyword. Example: LangChain"
#     )
# ]



# #  INITIALIZE GROK LLM (via Groq API)


# llm = ChatGroq(
#     model_name="llama-3.1-8b-instant",     # GROK MODEL
#     api_key=GROQ_API_KEY,
#     temperature=0
# )


# # SYSTEM PROMPT


# system_prompt = SystemMessagePromptTemplate.from_template(
#     """
# You are an intelligent LangChain Agent with three tools:

# 1. Calculator → Math problems.
# 2. WeatherAPI → Simulated weather.
# 3. FileSearch → Find sentences containing a keyword inside sample.txt.

# Rules:
# - Always use the correct tool when needed.
# - Never guess any numbers or weather.
# - For FileSearch, extract only sentences containing the keyword.
# - If no tool is required, answer normally.
# """
# )



# #  INITIALIZE AGENT


# agent = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent_type="chat-zero-shot-react-description",
#     verbose=True,
#     max_iterations=3,
#     handle_parsing_errors=True
# )



# #  DEMO USING invoke()


# def run_demo():
#     print("\n--- Milestone 2 Demo (Grok + Tools) ---\n")

#     queries = [
#         "What is 12 + 48 / 3?",
#         "What is the weather in Bengaluru?",
#         "Search in the file for LangChain",
#         "Explain what tools you used above.",
#         "What is 100 / (5 - 5)?"
#     ]

#     for q in queries:
#         print(f"\nUser: {q}")
#         try:
#             response = agent.invoke({"input": q})
#             print("Agent:", response["output"])
#         except Exception as e:
#             print(f"Agent Error:", str(e))


# if __name__ == "__main__":
#     run_demo()
