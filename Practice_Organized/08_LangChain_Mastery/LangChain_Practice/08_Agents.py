# -----------------------------------
# Imports
# -----------------------------------
from typing import Dict

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun


# -----------------------------------
# Tool 1: DuckDuckGo Web Search (REAL)
# -----------------------------------
duckduckgo_search = DuckDuckGoSearchRun()

@tool
def search_web(query: str) -> str:
    """Search the web using DuckDuckGo and return results."""
    return duckduckgo_search.run(query)


# -----------------------------------
# Tool 2: Text analysis (REAL)
# -----------------------------------
@tool
def analyze_data(text: str) -> Dict[str, int]:
    """Analyze text and return statistics."""
    words = text.split()
    return {
        "word_count": len(words),
        "unique_words": len(set(words)),
        "character_count": len(text),
    }


# -----------------------------------
# Tool 3: Save report to file 
# -----------------------------------
@tool
def save_report(content: str) -> str:
    """Save the research report to a local file."""
    with open("ai_safety_report.txt", "w", encoding="utf-8") as f:
        f.write(content)

    return "Report saved to ai_safety_report.txt"


# -----------------------------------
# Gemini Model
# -----------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))



# -----------------------------------
# Create LangChain Agent
# -----------------------------------
agent = create_agent(
    model=llm,
    tools=[search_web, analyze_data, save_report],
    system_prompt=(
        "You are a research assistant. "
        "Use web search when needed, analyze information, "
        "and save a concise final report."
    )
)


# -----------------------------------
# Invoke Agent
# -----------------------------------
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Research current AI safety trends and save a short report"
            }
        ]
    }
)

# -----------------------------------
# Output
# -----------------------------------
print(result)
