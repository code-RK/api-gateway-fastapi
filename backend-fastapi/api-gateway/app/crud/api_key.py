from sqlalchemy.orm import Session
from app.db.models import APIKey

def get_api_key(db: Session, key: str):
    return db.query(APIKey).filter(APIKey.key==key, APIKey.is_active==True).first()
