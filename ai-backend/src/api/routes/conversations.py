"""
WebSocket routes for real-time conversations.

Handles WebSocket connections for various conversation types including
catfish chat, social media simulation, and ethics discussions.
"""

from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status

from src.api.middleware import AuthenticationError
from src.api.websocket import authenticate_websocket
from src.services.conversation_engine import conversation_engine

router = APIRouter(tags=["conversations"])


@router.websocket("/ws/conversation")
async def websocket_conversation_endpoint(
    websocket: WebSocket,
    conversation_type: str = Query(..., description="Type of conversation"),
    session_id: Optional[str] = Query(None, description="Optional session ID"),
    locale: str = Query("en", description="User locale (en or pt)"),
    token: Optional[str] = Query(None, description="Authentication token"),
):
    """
    WebSocket endpoint for real-time conversations.
    
    Supports multiple conversation types:
    - catfish_chat: Catfishing detection simulation
    - social_media_sim: Social media disinformation simulation
    - ethics_feedback: Ethics discussion and feedback
    - deepfake_detection: Deepfake detection training
    
    Args:
        websocket: WebSocket connection
        conversation_type: Type of conversation
        session_id: Optional session ID (generated if not provided)
        locale: User locale (en or pt)
        token: JWT authentication token
    """
    # Authenticate user
    user_data = await authenticate_websocket(websocket, token)
    
    if not user_data:
        # Authentication failed, connection already closed
        return
    
    user_id = user_data["user_id"]
    
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid4())
    
    # Validate conversation type
    valid_types = ["catfish_chat", "social_media_sim", "ethics_feedback", "deepfake_detection"]
    if conversation_type not in valid_types:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason=f"Invalid conversation type. Must be one of: {', '.join(valid_types)}",
        )
        return
    
    # Validate locale
    if locale not in ["en", "pt"]:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION,
            reason="Invalid locale. Must be 'en' or 'pt'",
        )
        return
    
    print(f"🔗 New WebSocket connection: user={user_id}, type={conversation_type}, session={session_id}")
    
    # Handle conversation
    try:
        await conversation_engine.handle_websocket_connection(
            websocket=websocket,
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type,
            locale=locale,
        )
    except WebSocketDisconnect:
        print(f"🔌 WebSocket disconnected: session={session_id}")
    except Exception as e:
        print(f"❌ Error in WebSocket connection: {e}")
        if websocket.client_state.name == "CONNECTED":
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="Internal server error")


@router.websocket("/ws/catfish-chat")
async def websocket_catfish_chat(
    websocket: WebSocket,
    session_id: Optional[str] = Query(None, description="Optional session ID"),
    difficulty: int = Query(1, ge=1, le=5, description="Difficulty level (1-5)"),
    locale: str = Query("en", description="User locale (en or pt)"),
    token: Optional[str] = Query(None, description="Authentication token"),
):
    """
    Dedicated WebSocket endpoint for catfish chat simulation.
    
    Args:
        websocket: WebSocket connection
        session_id: Optional session ID
        difficulty: Difficulty level (1-5)
        locale: User locale
        token: JWT authentication token
    """
    # Authenticate user
    user_data = await authenticate_websocket(websocket, token)
    
    if not user_data:
        return
    
    user_id = user_data["user_id"]
    
    if not session_id:
        session_id = str(uuid4())
    
    print(f"🎭 Catfish chat started: user={user_id}, difficulty={difficulty}, session={session_id}")
    
    try:
        await conversation_engine.handle_websocket_connection(
            websocket=websocket,
            session_id=session_id,
            user_id=user_id,
            conversation_type="catfish_chat",
            locale=locale,
        )
    except WebSocketDisconnect:
        print(f"🔌 Catfish chat disconnected: session={session_id}")
    except Exception as e:
        print(f"❌ Error in catfish chat: {e}")


@router.websocket("/ws/social-media")
async def websocket_social_media(
    websocket: WebSocket,
    session_id: Optional[str] = Query(None, description="Optional session ID"),
    locale: str = Query("en", description="User locale (en or pt)"),
    token: Optional[str] = Query(None, description="Authentication token"),
):
    """
    Dedicated WebSocket endpoint for social media simulation.
    
    Args:
        websocket: WebSocket connection
        session_id: Optional session ID
        locale: User locale
        token: JWT authentication token
    """
    # Authenticate user
    user_data = await authenticate_websocket(websocket, token)
    
    if not user_data:
        return
    
    user_id = user_data["user_id"]
    
    if not session_id:
        session_id = str(uuid4())
    
    print(f"📱 Social media simulation started: user={user_id}, session={session_id}")
    
    try:
        await conversation_engine.handle_websocket_connection(
            websocket=websocket,
            session_id=session_id,
            user_id=user_id,
            conversation_type="social_media_sim",
            locale=locale,
        )
    except WebSocketDisconnect:
        print(f"🔌 Social media simulation disconnected: session={session_id}")
    except Exception as e:
        print(f"❌ Error in social media simulation: {e}")


@router.get("/conversations/active")
async def get_active_conversations():
    """
    Get count of active conversations.
    
    Returns:
        Active conversation statistics
    """
    return {
        "active_sessions": conversation_engine.get_active_sessions_count(),
        "timestamp": "2024-01-15T10:30:00Z",  # Will use actual timestamp
    }


@router.get("/conversations/user/{user_id}")
async def get_user_conversations(user_id: str):
    """
    Get active conversations for a specific user.
    
    Args:
        user_id: User identifier
        
    Returns:
        List of user's active conversations
    """
    sessions = conversation_engine.get_user_sessions(user_id)
    
    return {
        "user_id": user_id,
        "active_sessions": len(sessions),
        "sessions": [
            {
                "session_id": session.session_id,
                "conversation_type": session.conversation_type.value,
                "started_at": session.started_at.isoformat(),
                "message_count": session.message_count,
                "duration_seconds": session.get_session_duration(),
            }
            for session in sessions
        ],
    }
