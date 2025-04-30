import requests
from state import Query

def retrieve_node(state: Query) -> dict:
    docs = requests.get(
        "http://vector-db:5000/query",
        params={"query": state.query, "top_k": state.top_k},
    ).json()
    return {"context": docs}
