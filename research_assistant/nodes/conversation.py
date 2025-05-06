from config import llm
from state import State
from langchain_core.messages import AIMessage

def conversation_node(state: State) -> dict:
    # Check if query is conversational or needs research
    prompt = f"""
    You are an AI assistant. Determine if the following query requires research/document retrieval or is just a conversational exchange.
    Respond with EXACTLY:
    - CONVERSATIONAL: for greetings, personal questions, or general chat
    - RESEARCH: for questions that need information from documents or research

    Query: {state.query}

    Decision:
    """
    
    decision = llm.invoke([prompt])
    needs_retrieval = decision.content.strip() == "RESEARCH"
    
    if not needs_retrieval:
        # Handle conversational exchange directly
        chat_prompt = f"""
        You are a helpful and friendly AI assistant. Respond naturally to the user's message.
        Previous messages: {state.messages}
        Current message: {state.query}
        """
        response = llm.invoke([chat_prompt])

        return {
            "messages": [AIMessage(content=response.content)],
            "response": response.content,
        }
    
    return {"response": ""}