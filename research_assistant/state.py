# state.py
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field
from typing import List, Annotated
from langgraph.graph.message import add_messages

class State(BaseModel):
    messages: Annotated[List[AnyMessage], add_messages] = Field(
        default_factory=list,
        description="Chat message history with user and AI messages"
    )
    
    query: str = Field(..., description="Current user query")
    
    context: str = Field("", description="Retrieved document context")
    search_results: str = Field("", description="Web search results")
    
    needs_search: bool = Field(False, description="Flag for web search need")
    top_k: int = Field(1, description="Number of top results to consider")
    response: str = Field("", description="Generated AI response")