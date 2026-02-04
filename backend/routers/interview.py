"""
Interview Router - API endpoints for interview sessions
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()


class InterviewSession(BaseModel):
    id: str
    subject: str = "DSA"
    status: str = "pending"
    score: Optional[dict] = None


class StartInterviewRequest(BaseModel):
    subject: str = "DSA"
    difficulty: str = "medium"


# In-memory session storage (will be replaced with DB)
sessions = {}


@router.post("/start")
async def start_interview(request: StartInterviewRequest):
    """Start a new interview session"""
    session_id = str(uuid.uuid4())
    
    sessions[session_id] = InterviewSession(
        id=session_id,
        subject=request.subject,
        status="active"
    )
    
    return {
        "session_id": session_id,
        "message": "Interview session created",
        "websocket_url": f"/api/interview/ws/{session_id}"
    }


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get interview session details"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return sessions[session_id]


@router.post("/end/{session_id}")
async def end_interview(session_id: str):
    """End an interview session and get final score"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    session.status = "completed"
    
    # TODO: Calculate final score using ML model
    session.score = {
        "technical_accuracy": 0,
        "clarity": 0,
        "depth": 0,
        "confidence": 0,
        "communication": 0,
        "overall": 0
    }
    
    return session


@router.websocket("/ws/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time voice interview"""
    await websocket.accept()
    
    if session_id not in sessions:
        await websocket.close(code=4004, reason="Session not found")
        return
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "system",
            "message": "Connected to interview session",
            "session_id": session_id
        })
        
        while True:
            # Receive audio data from client
            data = await websocket.receive_bytes()
            
            # TODO: Process audio through pipeline
            # 1. STT: Convert audio to text
            # 2. LLM: Generate response with RAG
            # 3. TTS: Convert response to professor voice
            # 4. Send audio back
            
            # Placeholder response
            await websocket.send_json({
                "type": "processing",
                "message": "Audio received, processing..."
            })
            
    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
        if session_id in sessions:
            sessions[session_id].status = "disconnected"
