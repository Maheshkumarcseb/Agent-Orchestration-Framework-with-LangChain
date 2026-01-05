import math
import re
import requests
from datetime import datetime

from langchain_core.tools import tool



#  Research Tool (Web Content Fetcher)

@tool
def web_research_tool(query: str) -> str:
    """
    Fetches brief information from DuckDuckGo Instant Answer API.
    Useful for research agents.
    """
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            return data["RelatedTopics"][0].get("Text", "No useful data found.")
        else:
            return "No relevant research data found."

    except Exception as e:
        return f"Research tool error: {str(e)}"



#  Safe Calculator Tool

@tool
def calculator_tool(expression: str) -> str:
    """
    Safely evaluates mathematical expressions.
    Allowed operators: + - * / ( )
    """
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expression):
        return "Invalid expression"

    try:
        result = eval(expression, {"__builtins__": None}, {"math": math})
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"



#  Current Time Tool

@tool
def current_time_tool(_: str = "") -> str:
    """
    Returns the current system time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#  Tool Registry (Used by Agents)

TOOLS = [
    web_research_tool,
    calculator_tool,
    current_time_tool
]
