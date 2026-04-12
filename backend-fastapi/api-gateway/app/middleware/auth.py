from fastapi import HTTPException
from app.db.database import SessionLocal
from app.crud.api_key import get_api_key

VALID_API_KEYS = {
    "test-key-123",
    "internal-service-key"
}

def verify_api_key(api_key: str):
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API Key")
    
    db = SessionLocal()
    db_key = get_api_key(db, api_key)
    db.close()

    if not db_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return db_key #return full object
        