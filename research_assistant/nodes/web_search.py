from config import search_tool
from state import State

def web_search_node(state: State) -> dict:
    if state.needs_search:
        search_results = search_tool.invoke(state.query)
        additional_context = "\n".join([f"Source: {result['url']}\nContent: {result['content']}\n" for result in search_results["results"]])
        return {"search_results": additional_context}
    return {"search_results": ""}
