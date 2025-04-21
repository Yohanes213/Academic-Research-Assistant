from config import index, index_name
from models import DataPoint
import hashlib

def upsert_data(record: DataPoint):
    payload = record.dict(exclude_none=True)
    index.upsert_records(namespace=index_name, records=[payload])

def check_id_exists(pmid: str) -> bool:
    record_id = hashlib.md5(pmid.encode()).hexdigest()
    res = index.fetch(namespace=index_name, ids=[record_id])
    return bool(res.vectors and record_id in res.vectors)
