import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables from .env file
load_dotenv()

# Retrieve the Pinecone API key from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set.")

print(f"Initializing Pinecone with API key: {pinecone_api_key[:10]}...")  # Print first 10 chars for debugging

# Initialize the Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Define the index name
index_name = "pubmed"

# Initialize the index
try:
    index = pc.Index(index_name)
    print(f"Successfully connected to Pinecone index: {index_name}")
except Exception as e:
    print(f"Error connecting to Pinecone: {e}")
    raise