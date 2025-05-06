from langgraph.graph import StateGraph, START, END
from state import State
from nodes.retrieve import retrieve_node
from nodes.evaluate import evaluate_context_node
from nodes.web_search import web_search_node
from nodes.response import response_node
from nodes.conversation import conversation_node
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()


def build_graph():
    graph = StateGraph(State)

    # Add all nodes
    graph.add_node("conversation_node", conversation_node)
    graph.add_node("retrieve_node", retrieve_node)
    graph.add_node("evaluate_node", evaluate_context_node)
    graph.add_node("web_search_node", web_search_node)
    graph.add_node("response_node", response_node)

    # Add edges with conditional routing
    graph.add_edge(START, "conversation_node")
    graph.add_conditional_edges(
        "conversation_node",
        lambda state: END if state.response else "retrieve_node"
    )
    graph.add_edge("retrieve_node", "evaluate_node")
    graph.add_edge("evaluate_node", "web_search_node")
    graph.add_edge("web_search_node", "response_node")
    graph.add_edge("response_node", END)

    return graph.compile(checkpointer=memory)
