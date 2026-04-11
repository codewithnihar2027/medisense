# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import search

app = FastAPI(title="MediSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api")
# app.include_router(analyze.router, prefix="/api")
# app.include_router(pharmacy.router, prefix="/api")

@app.get("/health")
def health(): return {"status": "ok"}