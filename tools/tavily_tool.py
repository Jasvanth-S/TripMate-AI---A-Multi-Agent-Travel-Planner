from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(
    api_key = os.getenv("TAVILY_API_KEY")
)

def tavily_search(query: str):
    """this is the main function t seach te news retrive and relative information from tavily api"""
    response= client.search(
        query = query,
        max_results = 5
    )

    result = []

    for i, r in enumerate(response["results"], 1):
        title = r.get("title", "Unknown")
        url = r.get("url", "")
        snippet = r.get("content", "").strip()

        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        result.append(f"{i}. {title}\n URL:{url}\n {snippet}")

    return "\n\n".join(result)
