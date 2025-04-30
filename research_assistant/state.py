from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage
from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages

class State(TypedDict):
    query: str
    top_k: int
    context: str
    results: str
    needs_search: bool
    search_results: str

class Query(BaseModel):
    query: str = Field(..., description="The query to be answered.")
    top_k: int = Field(5, description="The number of top results to return.")
    context: str = Field("", description="Retrieved context for the LLM.")
    needs_search: bool = Field(False, description="Whether additional search is needed")
    search_results: str = Field("", description="Results from web search")

class Output(BaseModel):
    results: str = Field(..., description="The generated answer from the LLM.")
