import requests
from bs4 import BeautifulSoup
import re
import csv
import json
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
#         logging.StreamHandler()  # Keeps printing logs to the console as well
#     ]
# )

# logger = logging.getLogger(__name__)

# Pattern for publication date (e.g. "2025 Mar 29")
date_pattern = r"\b\d{4} [A-Z][a-z]{2} \d{1,2}\b"

def extract_articles(base_url):
    """Fetch and parse articles from the PubMed trending page."""
    try:
        # logger.info("Requesting URL: %s", base_url)
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_="full-docsum")
        # logger.info("Found %d articles", len(articles))
        return articles
    except Exception as e:
        # logger.error("Error extracting articles from %s: %s", base_url, e)
        return []

def parse_article_info(article):
    """Extract metadata (title, authors, journal info, PMID, etc.) from an article snippet.
    
    Any missing field is set to None.
    """
    try:
        # Extract journal citation or assign None
        journal_citation_elem = article.find('span', class_="full-journal-citation")
        journal_citation = journal_citation_elem.text.strip() if journal_citation_elem and journal_citation_elem.text.strip() else None

        # Extract publication date safely
        publication_date = None
        if journal_citation:
            date_match = re.search(date_pattern, journal_citation)
            publication_date = date_match.group(0) if date_match else None

        # Extract authors
        authors_elem = article.find('span', class_="full-authors")
        authors = authors_elem.text.strip() if authors_elem and authors_elem.text.strip() else None

        # Extract title and URL
        title_elem = article.find('a', class_="docsum-title")
        title = title_elem.text.strip() if title_elem and title_elem.text.strip() else None
        article_url = ("https://pubmed.ncbi.nlm.nih.gov" + title_elem['href']) if title_elem and title_elem.has_attr('href') else None

        # Extract PMID
        pmid_elem = article.find('span', class_="docsum-pmid")
        pmid = pmid_elem.text.strip() if pmid_elem and pmid_elem.text.strip() else None

        article_info = {
            "title": title,
            "authors": authors,
            "journal_citation": journal_citation,
            "publication_date": publication_date,
            "pmid": pmid,
            "article_url": article_url
        }
        # logger.info("Parsed article: %s", title)
        return article_info
    except Exception as e:
        # logger.error("Error parsing article info: %s", e)
        return {}

def fetch_article_details(article_url, headers=None):
    """Fetch additional details like abstract, keywords, references, and mesh terms from the full article page.

    Missing fields are set to an empty string or empty list, as appropriate.
    """
    details = {
        "abstract": "",
        "keywords": "",
        "conflict_of_interest": "",
        "references": [],
        "mesh_terms": []
    }
    try:
        # logger.info("Fetching details for article URL: %s", article_url)
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Abstract extraction
        abstract_elem = soup.find('div', class_="abstract-content selected")
        if abstract_elem:
            details["abstract"] = abstract_elem.get_text(strip=True)

        # Keywords extraction (if available)
        keywords_elem = abstract_elem.find_next_sibling('p') if abstract_elem else None
        if keywords_elem:
            details["keywords"] = keywords_elem.get_text(strip=True)

        # Conflict of Interest extraction
        conflict_elem = soup.find('div', class_="conflict-of-interest")
        if conflict_elem:
            statement = conflict_elem.find('p')
            details["conflict_of_interest"] = statement.get_text(strip=True) if statement else ""

        # References extraction
        references_elem = soup.find('div', class_="references")
        if references_elem:
            refs_url = article_url + 'references/'
            ref_response = requests.get(refs_url, headers=headers)
            ref_soup = BeautifulSoup(ref_response.text, "html.parser")
            references = ref_soup.find_all('li', class_='skip-numbering')
            details["references"] = [ref.get_text(strip=True) for ref in references]

        # Mesh terms extraction
        mesh_terms_elem = soup.find('div', class_="mesh-terms")
        if mesh_terms_elem:
            terms = mesh_terms_elem.find_all('li')
            details["mesh_terms"] = [term.get_text(strip=True) for term in terms]

        # logger.info("Fetched details for article URL: %s", article_url)
    except Exception as e:
        # logger.error("Error fetching article details for %s: %s", article_url, e)
        print()

    return details

def save_articles_to_json(articles, filename="pubmed_articles.json"):
    """Save extracted articles data into a JSON file in a readable format."""
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Write data to the file
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(articles, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving articles to JSON: {e}")
