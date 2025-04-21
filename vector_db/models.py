from pydantic import BaseModel, root_validator
from typing import List, Optional
import hashlib

class DataPoint(BaseModel):
    id: Optional[str] = None
    pmid: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    journal_citation: Optional[str] = None
    publication_date: Optional[str] = None
    article_url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[str] = None
    conflict_of_interest: Optional[str] = None
    references: List[str] = []
    mesh_terms: List[str] = []

    @root_validator(pre=True)
    def ensure_id_from_pmid(cls, values):
        # If no 'id' provided but 'pmid' is present, generate MD5 hash
        if not values.get('id') and values.get('pmid'):
            pmid_val = values['pmid']
            values['id'] = hashlib.md5(pmid_val.encode()).hexdigest()
        return values