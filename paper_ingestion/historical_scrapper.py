from scrapper import extract_articles, parse_article_info, fetch_article_details, save_articles_to_json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

import logging

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("/opt/airflow/logs/scraper.log"),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger(__name__)

app = FastAPI()

def scrape_articles():
    # logger.info("Scraping articles")
    page_number = 1
    base_url = 'https://pubmed.ncbi.nlm.nih.gov/trending/?sort=date&page='

    # Get output directory from environment variable or use default
    output_dir = os.getenv('OUTPUT_DIR', '/app/output')
    output_file = os.path.join(output_dir, 'pubmed_articles.json')
    
    # Also set the path for Airflow container
    airflow_output_file = '/opt/airflow/paper_ingestion/output/pubmed_articles.json'
    
    for page_number in range(1, 10):
        # logger.info(f"Processing page {page_number}")
        url = base_url + str(page_number)
        soup = extract_articles(url)
        articles = [parse_article_info(article) for article in soup]

        # Fetch additional details
        for article in articles:
            if article and article["article_url"]:
                details = fetch_article_details(article["article_url"])
                article.update(details)

        # logger.info(f"Saving articles to JSON")
        # Save to JSON in both locations
        save_articles_to_json(articles, output_file)
        save_articles_to_json(articles, airflow_output_file)
        # logger.info(f"Articles saved to JSON")

@app.get("/scrape")
def main():
    scrape_articles()
    return {"status": "Scraping completed"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
