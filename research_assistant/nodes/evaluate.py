from config import llm
from state import Query

def evaluate_context_node(state: Query) -> dict:
    if state.needs_search:
        return {"needs_search": True}

    prompt = f"""
        You are an assistant. Given the context and the user question, decide whether we need live web information to answer.
        Respond with EXACTLY NEED_MORE_INFO or SUFFICIENT.

        Context:
        {state.context}

        Question:
        {state.query}

        Decision:
        """
    resp = llm.invoke([prompt])
    decision = resp.content.strip()
    return {"needs_search": decision == "NEED_MORE_INFO"}
