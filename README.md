Milestone 2: Tool-Enabled AI Agent using LangChain & Gemini
--> Project Overview
This project demonstrates Milestone 2 of an Agent-Orchestration Framework using LangChain.
The objective of this milestone is to extend a basic conversational agent by integrating multiple tools and enabling the agent to take actions, not just generate text.
The agent is powered by Google Gemini and uses LangChain’s tool abstraction to perform real-world tasks such as calculations, weather queries, file searching, and text summarization.

-->Objectives
Integrate custom tools into a LangChain agent
Enable the agent to select and invoke tools autonomously
Demonstrate tool-based reasoning and action execution
Handle errors gracefully during tool execution

-->Tools Implemented
The agent has access to four tools:
1) Calculator Tool
Performs mathematical calculations
Used automatically for arithmetic expressions

2) Simulated Weather API
Returns mock weather information for any city
Demonstrates API-style tool integration

3)File Search Tool
Searches for keywords inside a local text file (sample.txt)
Returns only sentences containing the keyword

4)Text Summarizer Tool
Summarizes long paragraphs of text
Extracts key sentences for concise output

-->Environment Setup
1) Clone the Repository
git clone <repository-url>
cd Agent-Orchestration-Framework

2) Create and Activate Virtual Environment
python -m venv agentenv
agentenv\Scripts\activate

3) Install Dependencies
pip install -r requirements.txt

4)  Set Environment Variables
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key_here

--> How to Run the Program
python mileStone2.py







Milestone 1: Environment Setup & Basic Agent Creation

--> Project Overview
This project represents Milestone 1 of the Agent-Orchestration Framework using LangChain.
The goal of this milestone is to set up the development environment and build a foundational conversational AI agent powered by Google Gemini.
The agent supports memory, tool usage, and interactive console-based conversations, forming the base for future enhancements in later milestones.

-->Objectives
Configure Python and LangChain development environment
Connect to Google Gemini LLM
Understand LangChain core concepts: LLMs, Prompts, Chains, Agents, Memory
Build a basic zero-shot agent with tool access
Enable interactive CLI-based conversations

-->Core Features
Gemini-powered conversational agent
Conversation memory using ConversationBufferMemory
Tool-based reasoning
Zero-Shot ReAct agent
Interactive command-line interface



--> Environment Setup
1) Clone the Repository
git clone <repository-url>
cd Agent-Orchestration-Framework

2) Create and Activate Virtual Environment
python -m venv agentenv
agentenv\Scripts\activate

3) Install Dependencies
pip install -r requirements.txt

4) Configure Environment Variables
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key_here

---> How to Run the Program
python milestone1.py

--> Sample Interactions
You: 24 * (5 + 4)
Agent: Result: 216

You: Weather in Delhi
Agent: Temperature in Delhi: 31°C 

You: Explain zero-shot agents
Agent: A zero-shot agent is an AI system that...

