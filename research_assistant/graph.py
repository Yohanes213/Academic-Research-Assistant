from langgraph.graph import StateGraph, START, END
from state import State
from nodes.retrieve import retrieve_node
from nodes.evaluate import evaluate_context_node
from nodes.web_search import web_search_node
from nodes.response import response_node

def build_graph():
    graph = StateGraph(State)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("evaluate", evaluate_context_node)
    graph.add_node("web_search", web_search_node)
    graph.add_node("response", response_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "evaluate")
    graph.add_edge("evaluate", "web_search")
    graph.add_edge("web_search", "response")
    graph.add_edge("response", END)

    return graph.compile()
