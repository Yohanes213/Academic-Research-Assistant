from graph import build_graph
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/response")
def get_response(query: str, top_k: int = 1, needs_search: bool = False):
    graph = build_graph()
    result = graph.invoke({
        "query": query,
        "top_k": top_k,
        "needs_search": needs_search,
        "search_results": "",
    })
    return result["results"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
    
