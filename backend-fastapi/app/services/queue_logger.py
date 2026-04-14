import redis
import json
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url, decode_responses=True)

QUEUE_NAME = "request_logs_queue"

def push_log(data: dict):
    r.rpush(QUEUE_NAME, json.dumps(data))

