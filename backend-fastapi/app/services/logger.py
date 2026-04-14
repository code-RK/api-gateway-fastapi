from app.db.database import SessionLocal
from app.db.models import RequestLog

def log_request(data: dict):
    db = SessionLocal()

    try:
        log = RequestLog(**data)
        db.add(log)
        db.commit()
    finally:
        db.close()