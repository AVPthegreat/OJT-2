"""
AI Viva Interview Platform - Main FastAPI Application
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routers import interview
from services.stt_service import STTService
from services.tts_service import TTSService
from services.llm_service import LLMService


# Global service instances
stt_service = None
tts_service = None
llm_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup, cleanup on shutdown"""
    global stt_service, tts_service, llm_service
    
    print("🚀 Initializing AI services...")
    
    # Initialize services (will be implemented)
    # stt_service = STTService()
    # tts_service = TTSService()
    # llm_service = LLMService()
    
    print("✅ Services ready!")
    
    yield
    
    print("👋 Shutting down services...")


app = FastAPI(
    title="AI Viva Interview Platform",
    description="Practice DSA interviews with AI-powered voice conversations",
    version="0.1.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "AI Viva Interview Platform",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "stt": stt_service is not None,
            "tts": tts_service is not None,
            "llm": llm_service is not None
        }
    }


# Include routers
app.include_router(interview.router, prefix="/api/interview", tags=["interview"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
