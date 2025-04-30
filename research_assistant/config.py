from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    temperature=0,
    max_retries=2,
)

search_tool = TavilySearch(
    max_results=2,
)
