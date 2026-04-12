import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

QUEUE_NAME = "request_logs_queue"

def push_log(data: dict):
    r.rpush(QUEUE_NAME, json.dumps(data))

