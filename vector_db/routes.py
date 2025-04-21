from fastapi import APIRouter, HTTPException
from models import DataPoint
from crud import upsert_data, check_id_exists
from config import index_name, index
import hashlib 

router = APIRouter()

@router.get("/health")
async def health_check():
    try:
        index.describe_index_stats(index_name)
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.post("/upsert")
async def upsert_data(record: DataPoint):
    try:
        payload = record.dict(exclude_none=True)

        index.upsert_records(
            namespace=index_name,
            records=[payload]
        )
        return {"message": "Data upserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check_id")
async def check_id_exists(pmid: str) -> bool:
    record_id = hashlib.md5(pmid.encode()).hexdigest()
    
    res = index.fetch(
        namespace=index_name,
        ids=[record_id]
    )
    
    return bool(res.vectors and record_id in res.vectors)