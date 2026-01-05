import os
from langchain_groq import ChatGroq
from memory import conversation_memory, vector_memory
from evaluator import evaluate_output
from dotenv import load_dotenv
load_dotenv()
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.4
)

def research_agent(topic):
    prompt = f"Research the topic clearly:\n{topic}"
    return llm.invoke(prompt).content

def summarize_agent(text):
    prompt = f"Summarize clearly in bullet points:\n{text}"
    return llm.invoke(prompt).content

from langchain_core.messages import HumanMessage

def email_agent(summary, purpose):
    response = llm.invoke([
        HumanMessage(
            content=f"""
Write a PROFESSIONAL EMAIL using the format below.
Follow the structure EXACTLY.
Use proper line breaks.

FORMAT:
Subject: <subject line>

Dear <Recipient>,

<Opening paragraph>

<Bullet points or body paragraphs if needed>

<Closing paragraph>

Regards,
<Sender Name>

Purpose: {purpose}

Content to use:
{summary}

IMPORTANT RULES:
- Each section MUST be on a new line
- Leave one blank line between paragraphs
- Do NOT write everything in one line
"""
        )
    ])
    return response.content.strip()


def run_workflow(topic, purpose):
    research = research_agent(topic)
    summary = summarize_agent(research)
    email = email_agent(summary, purpose)

    conversation_memory.save_context(
        {"input": topic},
        {"output": email}
    )

    evaluation = evaluate_output(email)

    return {
        "research": research,
        "summary": summary,
        "email": email,
        "evaluation": evaluation
    }
