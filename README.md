# Academic Research Assistant

A distributed system for collecting, processing, and analyzing academic research papers. The system consists of multiple microservices orchestrated using Docker Compose and Apache Airflow.

## System Architecture

The system consists of the following main components:

### 1. Paper Ingestion Service
- Located in `/paper_ingestion`
- A FastAPI service that scrapes PubMed's trending papers
- Features:
  - Automated scraping of trending articles from PubMed
  - Article metadata extraction
  - Integration with Vector DB service for storage
  - Health check endpoints
  - Automatic deduplication of articles

### 2. Vector Database Service
- Located in `/vector_db`
- A FastAPI service that manages the vector database (using Pinecone)
- Features:
  - Document storage and retrieval
  - Vector similarity search
  - Document existence checking
  - Health monitoring

### 3. Airflow Orchestration
- Located in `/airflow`
- Manages scheduled tasks and workflow orchestration
- Features:
  - Weekly paper ingestion scheduling
  - Task retry mechanisms
  - Monitoring and logging
  - Web interface for task management

### 4. Research Agent (In Development)
- Located in `/research_agent`
- Future service for intelligent research assistance
- Currently in initial development phase

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Pinecone API Key

## Environment Variables

The following environment variables need to be set:

```env
PINECONE_API_KEY=your_pinecone_api_key
VECTOR_DB_URL=http://vector-db:5000 (default in docker-compose)
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/Yohanes213/Academic-Research-Assistant
cd Academic-Research-Assistant
```

2. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your Pinecone API key

3. Start the services:
```bash
docker-compose up -d
```

4. Access the services:
- Airflow UI: http://localhost:8080 (username: admin, password: admin)
- Paper Ingestion API: http://localhost:8000
- Vector DB API: http://localhost:5000

## Service Endpoints

### Paper Ingestion Service
- `GET /health`: Health check endpoint
- `GET /scrape`: Trigger paper scraping process

### Vector DB Service
- `GET /health`: Health check endpoint
- `POST /upsert`: Add or update documents
- `POST /check_id`: Check if a document exists
- `GET /query`: Query documents by similarity

## Development

Each service can be developed independently:

1. Paper Ingestion Service:
```bash
cd paper_ingestion
pip install -r requirements.txt
uvicorn main:app --reload
```

2. Vector DB Service:
```bash
cd vector_db
pip install -r requirements.txt
uvicorn main:app --reload
```

## Monitoring and Maintenance

- Airflow logs are available in `/airflow/logs`
- Each service includes health check endpoints
- Docker container logs can be viewed using `docker logs [container-name]`

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
