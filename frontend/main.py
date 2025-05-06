import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Academic Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Constants
RESEARCH_ASSISTANT_URL = os.getenv("RESEARCH_ASSISTANT_URL", "http://research-assistant:5001")
PAPER_INGESTION_URL = os.getenv("PAPER_INGESTION_URL", "http://paper-ingestion:8000")
VECTOR_DB_URL = os.getenv("VECTOR_DB_URL", "http://vector-db:5000")

def check_service_health(url):
    try:
        response = requests.get(f"{url}/health")
        return response.status_code == 200
    except:
        return False

# Custom CSS for ChatGPT-like interface
st.markdown("""
    <style>
    .chat-container {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f7f7f8;
    }
    .assistant-message {
        background-color: white;
    }
    .search-toggle {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .search-toggle:hover {
        background-color: #f0f0f0;
    }
    .search-toggle.active {
        background-color: #e6f3ff;
        border-color: #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Research Assistant", "Paper Search", "System Status"])

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# System Status Section
if page == "System Status":
    st.title("System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Research Assistant",
            "Online" if check_service_health(RESEARCH_ASSISTANT_URL) else "Offline"
        )
    
    with col2:
        st.metric(
            "Paper Ingestion",
            "Online" if check_service_health(PAPER_INGESTION_URL) else "Offline"
        )
    
    with col3:
        st.metric(
            "Vector DB",
            "Online" if check_service_health(VECTOR_DB_URL) else "Offline"
        )

# Research Assistant Section
elif page == "Research Assistant":
    st.title("Research Assistant")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.container():
            st.markdown(f"""
                <div class="chat-container {'user-message' if message['role'] == 'user' else 'assistant-message'}">
                    <b>{'You' if message['role'] == 'user' else 'Assistant'}:</b><br>{message['content']}
                </div>
            """, unsafe_allow_html=True)

    # Chat input area
    with st.container():
        col1, col2 = st.columns([6, 1])
        with col1:
            query = st.text_area("", placeholder="Enter your research question...", height=100, label_visibility="collapsed")
        with col2:
            needs_search = st.toggle("🔍", value=True, help="Toggle web search")
        
        if st.button("Send", use_container_width=True):
            if query:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": query})
                
                try:
                    response = requests.post(
                        f"{RESEARCH_ASSISTANT_URL}/response",
                        params={
                            "query": query,
                            "needs_search": needs_search
                        },
                        json={"chat_history": st.session_state.messages}  # Send chat history as JSON
                    )
                    if response.status_code == 200:
                        result = response.json()
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": result})
                        st.rerun()
                    else:
                        st.error("Failed to get response from the service")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Paper Search Section
elif page == "Paper Search":
    st.title("Paper Search")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search papers:", placeholder="Enter your search query...")
    with col2:
        top_k = st.number_input("Number of results:", min_value=1, max_value=20, value=5)
    
    if search_query:
        try:
            response = requests.get(
                f"{VECTOR_DB_URL}/query",
                params={"query": search_query, "top_k": top_k}
            )
            if response.status_code == 200:
                papers = response.json()
                for paper in papers:
                    with st.expander(paper["title"]):
                        st.write(f"**Authors:** {paper['authors']}")
                        st.write(f"**Abstract:** {paper['abstract']}")
                        st.write(f"**Published:** {paper['publication_date']}")
                        st.write(f"**Article URL:**  {paper['article_url']}")
            else:
                st.error("Failed to fetch papers")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.sidebar.markdown("---")