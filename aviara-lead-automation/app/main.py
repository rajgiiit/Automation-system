from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import classify, enrich

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "AI Powered Lead Automation System"),
    version="1.0.0",
    description="Backend APIs for an n8n-powered lead automation workflow.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(enrich.router, prefix="/api", tags=["Enrichment"])
app.include_router(classify.router, prefix="/api", tags=["Classification"])
app.include_router(enrich.router, tags=["Assignment Compatible Endpoints"])
app.include_router(classify.router, tags=["Assignment Compatible Endpoints"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "AI Powered Lead Automation System",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
