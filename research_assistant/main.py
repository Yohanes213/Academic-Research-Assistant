from graph import build_graph
from fastapi import FastAPI
import uvicorn
import uuid
from langchain_core.messages import HumanMessage, AIMessage
import os
from dotenv import load_dotenv

import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("LANGSMITH_API_KEY")

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langchain-academy"

# Initialize thread ID and config once
thread_id = uuid.uuid4().hex
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

print(f"Thread ID: {thread_id}")
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Initialize graph once
graph = build_graph()

@app.post("/response")
def get_response(query: str, top_k: int = 1, needs_search: bool = False):
    result = graph.invoke(
        {
            "messages": [HumanMessage(content=query)],
            "query": query,
            "top_k": top_k,
            "search_results": "",
        },
        config=config
    )
    
    return result["response"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    
