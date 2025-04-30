# Academic Research Assistant

An AI-powered system that helps researchers explore and analyze academic papers. The system automatically scrapes papers from PubMed, processes them, and provides intelligent responses to research queries.

## System Overview

1. **Paper Ingestion Service** (Port 8000)
   - Automatically scrapes trending papers from PubMed
   - Extracts metadata and content
   - Processes papers for vector storage

2. **Vector Database Service** (Port 5000)
   - Uses Pinecone for efficient vector storage
   - Enables semantic search across papers
   - Handles document deduplication

3. **Research Assistant** (Port 5001)
   - Powered by Google's Gemini
   - Provides intelligent research insights
   - Uses Tavily for enhanced web search

4. **Airflow** (Port 8080)
   - Schedules weekly paper ingestion
   - Manages the data pipeline
   - Provides task monitoring

## Setup Guide

1. API Keys Setup:
   ```bash
   # In vector_db/.env
   PINECONE_API_KEY=your_pinecone_key

   # In research_assistant/.env
   GOOGLE_API_KEY=your_gemini_key
   TAVILY_API_KEY=your_tavily_key
   LANGSMITH_API_KEY=your_langsmith_key  # Optional
   ```

2. Start Services:
   ```bash
   docker-compose up -d
   ```

3. Access Points:
   - Airflow Dashboard: http://localhost:8080 
     - Username: admin
     - Password: admin
   - Research Assistant: http://localhost:5001
   - Paper Ingestion: http://localhost:8000
   - Vector DB: http://localhost:5000

## Key Features

- **Automated Paper Collection**: Weekly scraping of trending PubMed papers
- **Intelligent Research Assistance**: AI-powered research insights using Google's Gemini
- **Semantic Search**: Find relevant papers using natural language queries
- **Scalable Architecture**: Microservices design with Docker containerization

## API Endpoints

### Research Assistant
- `POST /response`
  ```json
  {
    "query": "What are the latest findings in COVID-19 treatment?",
    "top_k": 5,
    "needs_search": true
  }
  ```

### Paper Ingestion
- `GET /scrape`: Trigger manual paper collection
- `GET /health`: Service health check

### Vector DB
- `POST /upsert`: Add new papers
- `GET /query`: Search papers
- `POST /check_id`: Check paper existence

## Requirements

- Docker and Docker Compose
- API Keys:
  - [Pinecone](https://www.pinecone.io/) for vector storage
  - [Google AI Studio](https://aistudio.google.com/app/apikey) for Gemini
  - [Tavily](https://app.tavily.com/home) for web search
  - [LangSmith](https://smith.langchain.com/) (optional) for LLM monitoring

## Development

For local development of individual services:

```bash
# Paper Ingestion Service
cd paper_ingestion
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Vector DB Service
cd vector_db
pip install -r requirements.txt
uvicorn main:app --reload --port 5000

# Research Assistant
cd research_assistant
pip install -r requirements.txt
uvicorn main:app --reload --port 5001
```

## Monitoring

- View service logs: `docker logs <container-name>`
- Check Airflow tasks: http://localhost:8080/admin/
- Service health endpoints: `/health`

## Project Structure

```
.
├── airflow/              # Airflow DAGs and configurations
├── paper_ingestion/      # Paper processing service
├── vector_db/           # Vector database service
└── research_assistant/  # Research query processing service
```

## Future Development

- Research Agent implementation
- Enhanced search capabilities
- User interface development
- Integration with additional academic databases

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to:
- Update the README.md with details of changes if applicable
- Update any relevant documentation
- Add tests for new features if applicable

## License

This project is licensed under the MIT License - see below for details:
