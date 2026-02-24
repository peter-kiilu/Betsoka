"""
BETSOKA — FastAPI Application
==============================
Entry point for the REST API server.
Mounts routes and configures CORS for the React frontend.
In production, also serves the built React app as static files.
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# ─── Serve React build in production ────────────────────────
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():
    # Serve static assets (JS, CSS, images, logos)
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")

    # Serve files from public/ that end up in dist root (logos, favicon, etc.)
    @app.get("/logos/{filepath:path}")
    async def serve_logos(filepath: str):
        logo_path = FRONTEND_DIR / "logos" / filepath
        if logo_path.exists():
            return FileResponse(logo_path)
        return FileResponse(FRONTEND_DIR / "index.html")

    # SPA fallback: serve index.html for all non-API routes
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Try to serve an actual file first (e.g., favicon.ico, manifest.json)
        file_path = FRONTEND_DIR / full_path
        if full_path and file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        # Otherwise, serve index.html for client-side routing
        return FileResponse(FRONTEND_DIR / "index.html")
else:
    # Dev mode — no frontend build, just show API info
    @app.get("/")
    def root():
        return {"message": "BETSOKA API is running", "docs": "/docs"}
