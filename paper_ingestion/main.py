from scrapper import extract_articles, parse_article_info, fetch_article_details
from fastapi import FastAPI
import httpx
from pydantic import BaseModel
import uvicorn
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

VECTOR_DB_URL = os.getenv('VECTOR_DB_URL', 'http://vector-db:5000')

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

async def send_to_vector_db(article):
    """Send article data to vector DB service"""
    async with httpx.AsyncClient() as client:
        try:
            # Check vector DB health first
            try:
                health_response = await client.get(f"{VECTOR_DB_URL}/health")
                health_response.raise_for_status()
                logger.info("Vector DB health check passed")
            except Exception as e:
                logger.error(f"Vector DB health check failed: {e}")
                return False

            response = await client.post(f"{VECTOR_DB_URL}/upsert", json=article)
            response.raise_for_status()
            response.raise_for_status()
            logger.info(f"Successfully sent article {article.get('pmid')} to vector DB")
            return True

        except httpx.HTTPStatusError as e:
            # log full response so you see Pydantic’s error detail
            text = e.response.text
            status = e.response.status_code
            logger.error(f"Upsert failed [{status}]: {text}")
            return False

        except Exception as e:
            logger.error(f"Failed to send article to vector DB: {e}")
            return False

async def check_article_exists(pmid: str) -> bool:
    """Check if an article with the given PMID exists in Pinecone."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{VECTOR_DB_URL}/check_id", params={"pmid": pmid})
            response.raise_for_status()
            return response.json().get("exists", False)
    except Exception as e:
        logger.error(f"Failed to check article existence for PMID {pmid}: {e}")
        return False

async def scrape_articles():
    logger.info("Starting article scraping")
    base_url = 'https://pubmed.ncbi.nlm.nih.gov/trending/?sort=date&page='
    
    success_count = 0
    error_count = 0

    for page_number in range(1, 100):
        logger.info(f"Processing page {page_number}")
        url = base_url + str(page_number)
        soup = extract_articles(url)
        articles = [parse_article_info(article) for article in soup]

        # Fetch additional details and send to vector DB
        for article in articles:
            if article and article["article_url"]:
                details = fetch_article_details(article["article_url"])
                article.update(details)
                
                if await check_article_exists(article["pmid"]):
                    logger.info(f"Article {article['pmid']} already exists in vector DB, skipping...")
                    continue
                # Send to vector DB
                if await send_to_vector_db(article):
                    success_count += 1
                else:
                    error_count += 1

    return {    
        "success_count": success_count,
        "error_count": error_count
    }

@app.get("/scrape")
async def main():
    results = await scrape_articles()
    return {
        "status": "Scraping completed",
        "results": results
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
