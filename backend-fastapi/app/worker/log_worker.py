import redis
import json
import time
import os
from app.db.database import SessionLocal
from app.db.models import RequestLog

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url, decode_responses=True)

QUEUE_NAME = "request_logs_queue"

def process_logs():
    print("Worker started...")

    while True:
        _, log_data = r.blpop(QUEUE_NAME) #blocking pop
        
        data = json.loads(log_data)

        db = SessionLocal()
        try:
            log = RequestLog(**data)
            db.add(log)
            db.commit()
        except Exception as e:
            print("Error: ", e)
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    process_logs()