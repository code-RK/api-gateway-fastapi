from fastapi import FastAPI, Request, HTTPException, Depends
from app.middleware.auth import verify_api_key
from app.services.proxy import forward_request
from app.rate_limiter.token_bucket import is_allowed
import time
import logging
import uuid
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import APIKey, RequestLog
from app.services.logger import log_request
from app.services.queue_logger import push_log
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-gateway")

PUBLIC_PATHS = {"/create-key", "/analytics/summary", "/analytics/by-key", "/analytics/status-codes"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def api_gateway_middleware(request: Request, call_next):

    # ✅ Skip public endpoints
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    start_time = time.time()
    api_key = request.headers.get("x-api-key")
    try:
        api_key_obj = verify_api_key(api_key)

        rate_limit_result = is_allowed(
            api_key=api_key,
            capacity=api_key_obj.capacity,
            refill_rate=api_key_obj.refill_rate
        )
        if not rate_limit_result["allowed"]:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        response = await forward_request(request)

        return response
    
    except HTTPException as e:
        raise e
    
    finally:
        process_time = round((time.time() - start_time) * 1000, 2)

        push_log({
            "api_key": api_key,
            "path": request.url.path,
            "method": request.method,
            "status_code": getattr(locals().get("response", None), "status_code",500),
            "latency": process_time
        })

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-key")
def create_key(db: Session = Depends(get_db)):
    try:
        new_key = str(uuid.uuid4())
        print("This is called")
        api_key = APIKey(
            key=new_key,
            capacity=10,
            refill_rate=2
        )

        db.add(api_key)
        db.commit()

        return {"api_key": new_key}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.get("/analytics/summary")
def get_summary(db: Session = Depends(get_db)):
    
    total_requests = db.query(func.count(RequestLog.id)).scalar()

    return {
        "total_requests": total_requests
    }

@app.get("/analytics/by-key")
def by_key(db: Session = Depends(get_db)):
    data =  db.query(
        RequestLog.api_key,
        func.count().label("count")
    ).group_by(RequestLog.api_key).all()

    # Convert to dict
    result = [
        {"api_key": row[0], "count": row[1]}
        for row in data
    ]

    return result

@app.get("/analytics/status-codes")
def status_codes(db: Session=Depends(get_db)):
    data = db.query(
        RequestLog.status_code,
        func.count().label("count")
    ).group_by(RequestLog.status_code).all()

    # Convert to dict
    result = [
        {"status_code": row[0], "count": row[1]}
        for row in data
    ]

    return result