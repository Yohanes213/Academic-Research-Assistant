import requests
from state import State
import json

def retrieve_node(state: State) -> dict:
    docs = requests.get(
        "http://vector-db:5000/query",
        params={"query": state.query, "top_k": state.top_k},
    ).json()
    
    # Convert documents to a formatted string
    context = ""
    if docs:
        context = "\n\n".join([
            f"Document {i+1}:\n" +
            f"Title: {doc.get('title', 'N/A')}\n" +
            f"Abstract: {doc.get('abstract', 'N/A')}\n" +
            f"URL: {doc.get('article_url', 'N/A')}"
            for i, doc in enumerate(docs)
        ])

    return {
        "context": context,
        "messages": state.messages
    }
