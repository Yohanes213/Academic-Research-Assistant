from config import llm
from state import Query, Output

def response_node(state: Query) -> Output:
    answer_prompt = f"""
    You are a helpful assistant. Answer the question using ALL the information provided in the context below.
    You must consider and synthesize information from BOTH retrieved documents and web search results when available.

    Retrived_context:
    {state.context}

    Web_search_results:
    {state.search_results}

    Question:
    {state.query}

    Instructions:
    1. Analyze ALL provided information from both retrieved documents and web search results
    2. Synthesize a comprehensive answer that combines relevant information from all sources
    3. If there are source URLs in the context, include relevant ones in your response
    4. Clearly indicate when you're drawing information from retrieved documents vs web search results
    
    Answer:
    """
    gen = llm.invoke([answer_prompt])
    msg = gen[0] if isinstance(gen, list) else gen

    return Output(results=msg.content)
