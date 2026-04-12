# API Gateway with Rate Limiting & Analytics Dashboard

## Features
- Token Bucket Rate Limiter (Redis + Lua)
- API Key Management
- Async Logging (Redis Queue + Worker)
- Analytics Dashboard (React + Chart.js)

## Tech Stack
- FastAPI
- PostgreSQL
- Redis
- React

## Run Locally

### Backend
uvicorn app.main:app --reload

### Frontend
cd dashboard
npm start