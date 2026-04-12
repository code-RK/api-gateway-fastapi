import time
import redis
from fastapi import HTTPException

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

LUA_SCRIPT = """
local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- Get current state
local data = redis.call("HMGET", key, "tokens", "last_refill")

local tokens = tonumber(data[1])
local last_refill = tonumber(data[2])

if tokens == nil then
    tokens = capacity
    last_refill = now
end

-- Refill tokens
local delta = math.max(0, now - last_refill)
local refill = delta * refill_rate
tokens = math.min(capacity, tokens + refill)

-- Check if request allowed
if tokens < requested then
    local retry_after = (requested - tokens) / refill_rate
    return {0, tokens, retry_after}
end

-- Consume tokens
tokens = tokens - requested

-- Save state
redis.call("HMSET", key,
    "tokens", tokens,
    "last_refill", now
)

redis.call("EXPIRE", key, 60)

return {1, tokens, 0}
"""

# Load script into Redis
rate_limiter_script = r.register_script(LUA_SCRIPT)

def is_allowed(api_key: str, capacity=10, refill_rate=5):
    key = f"rate_limit:{api_key}"
    now = time.time()

    allowed, tokens_left, retry_after = rate_limiter_script(
        keys = [key],
        args = [capacity, refill_rate, now, 1]
    )


    return {
        "allowed": bool(allowed),
        "tokens_left": tokens_left,
        "retry_after": retry_after
    }