"""
BETSOKA — FastAPI Application
==============================
Entry point for the REST API server.
Mounts routes and configures CORS for the React frontend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="BETSOKA API",
    description="AI-Based Football Match Outcome Prediction — Demo System",
    version="1.0.0",
)

# Allow React dev server (localhost:5173) and any origin for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "BETSOKA API is running", "docs": "/docs"}
