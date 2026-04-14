import redis
import json
import time

from app.db.database import SessionLocal
from app.db.models import RequestLog

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

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