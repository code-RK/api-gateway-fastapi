from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.db.database import Base
from datetime import datetime

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)

    #Rate limiting config
    capacity = Column(Integer, default=10)
    refill_rate = Column(Integer, default=5)

    is_active = Column(Boolean, default=True)

class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String)
    path = Column(String)
    method = Column(String)
    status_code = Column(Integer)
    latency = Column(Float)
    timestamp = Column(DateTime, default=datetime.now())