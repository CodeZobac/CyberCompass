"""WebSocket route handlers for real-time communication."""

import asyncio
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional

from src.api.websocket import (
    authenticate_websocket,
    connection_manager,
    handle_websocket_message,
    websocket_heartbeat,
)

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/catfish-chat")
async def catfish_chat_websocket(
    websocket: WebSocket,
    token: Optional[str] = Query(None, description="JWT authentication token"),
    session_id: Optional[str] = Query(None, description="Optional session ID for reconnection"),
) -> None:
    """
    WebSocket endpoint for catfish detection chat simulation.

    Provides real-time chat with AI catfish character including:
    - Realistic typing delays
    - Character consistency with red flags
    - Real-time message exchange

    Args:
        websocket: WebSocket connection
        token: JWT authentication token
        session_id: Optional session ID for reconnection
    """
    # Authenticate connection
    user = await authenticate_websocket(websocket, token)
    if not user:
        return

    # Generate or use provided session ID
    if not session_id:
        session_id = f"catfish_{user['user_id']}_{uuid4().hex[:8]}"

    try:
        # Connect to manager
        await connection_manager.connect(
            websocket=websocket,
            session_id=session_id,
            user_id=user["user_id"],
            conversation_type="catfish_chat",
        )

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(websocket_heartbeat(session_id))

        # Send welcome message
        await connection_manager.send_personal_message(
            session_id,
            {
                "type": "system_message",
                "message": "Connected to catfish chat simulation. The character will respond shortly.",
                "locale": user.get("locale", "en"),
            },
        )

        # TODO: Initialize catfish character (will be implemented in task 3)
        # For now, send a placeholder message
        await asyncio.sleep(2)  # Simulate typing delay
        await connection_manager.send_personal_message(
            session_id,
            {
                "type": "agent_message",
                "agent": "catfish_character",
                "message": "Hey! How are you doing? 😊",
                "timestamp": None,  # Will be added by send_personal_message
            },
        )

        # Message loop
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Handle message
            response = await handle_websocket_message(session_id, data)

            # Send response if needed
            if response.get("type") != "acknowledgment":
                await connection_manager.send_personal_message(session_id, response)

            # TODO: Route user messages to CrewAI agents (task 5)
            # For now, just echo back
            if data.get("type") == "user_message":
                await asyncio.sleep(1.5)  # Simulate typing
                await connection_manager.send_personal_message(
                    session_id,
                    {
                        "type": "agent_message",
                        "agent": "catfish_character",
                        "message": "That's interesting! Tell me more about yourself.",
                    },
                )

    except WebSocketDisconnect:
        print(f"Client disconnected from catfish chat: {session_id}")
    except Exception as e:
        print(f"Error in catfish chat websocket: {e}")
    finally:
        # Cleanup
        heartbeat_task.cancel()
        await connection_manager.disconnect(session_id)


@router.websocket("/social-media-sim")
async def social_media_simulation_websocket(
    websocket: WebSocket,
    token: Optional[str] = Query(None, description="JWT authentication token"),
    session_id: Optional[str] = Query(None, description="Optional session ID for reconnection"),
) -> None:
    """
    WebSocket endpoint for social media disinformation simulation.

    Provides real-time social media feed with:
    - Dynamic content generation
    - Real-time engagement tracking
    - Algorithm feedback

    Args:
        websocket: WebSocket connection
        token: JWT authentication token
        session_id: Optional session ID for reconnection
    """
    # Authenticate connection
    user = await authenticate_websocket(websocket, token)
    if not user:
        return

    # Generate or use provided session ID
    if not session_id:
        session_id = f"social_media_{user['user_id']}_{uuid4().hex[:8]}"

    try:
        # Connect to manager
        await connection_manager.connect(
            websocket=websocket,
            session_id=session_id,
            user_id=user["user_id"],
            conversation_type="social_media_sim",
        )

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(websocket_heartbeat(session_id))

        # Send welcome message
        await connection_manager.send_personal_message(
            session_id,
            {
                "type": "system_message",
                "message": "Connected to social media simulation. Your feed is loading...",
                "locale": user.get("locale", "en"),
            },
        )

        # TODO: Initialize social media feed (will be implemented in task 4)
        # For now, send placeholder posts
        await asyncio.sleep(1)
        await connection_manager.send_personal_message(
            session_id,
            {
                "type": "feed_update",
                "posts": [
                    {
                        "post_id": "post_001",
                        "content": "Breaking: New study shows amazing health benefits!",
                        "author": "HealthNews247",
                        "is_disinformation": True,
                    }
                ],
            },
        )

        # Message loop
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Handle message
            response = await handle_websocket_message(session_id, data)

            # Send response
            if response.get("type") != "acknowledgment":
                await connection_manager.send_personal_message(session_id, response)

            # TODO: Handle user interactions (likes, shares, reports)
            # This will be implemented in task 4

    except WebSocketDisconnect:
        print(f"Client disconnected from social media sim: {session_id}")
    except Exception as e:
        print(f"Error in social media sim websocket: {e}")
    finally:
        # Cleanup
        heartbeat_task.cancel()
        await connection_manager.disconnect(session_id)


@router.websocket("/analytics-stream")
async def analytics_stream_websocket(
    websocket: WebSocket,
    token: Optional[str] = Query(None, description="JWT authentication token"),
) -> None:
    """
    WebSocket endpoint for streaming real-time analytics updates.

    Provides live updates on:
    - Progress metrics
    - Competency scores
    - Achievement unlocks
    - Peer comparisons

    Args:
        websocket: WebSocket connection
        token: JWT authentication token
    """
    # Authenticate connection
    user = await authenticate_websocket(websocket, token)
    if not user:
        return

    session_id = f"analytics_{user['user_id']}_{uuid4().hex[:8]}"

    try:
        # Connect to manager
        await connection_manager.connect(
            websocket=websocket,
            session_id=session_id,
            user_id=user["user_id"],
            conversation_type="analytics_stream",
        )

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(websocket_heartbeat(session_id))

        # Send initial analytics
        await connection_manager.send_personal_message(
            session_id,
            {
                "type": "analytics_update",
                "data": {
                    "competency_scores": {},
                    "total_challenges": 0,
                    "accuracy_rate": 0.0,
                },
                "message": "Analytics stream connected",
            },
        )

        # Message loop
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            # Handle message
            response = await handle_websocket_message(session_id, data)

            # Send response
            if response.get("type") != "acknowledgment":
                await connection_manager.send_personal_message(session_id, response)

            # TODO: Stream real-time analytics updates (task 6)

    except WebSocketDisconnect:
        print(f"Client disconnected from analytics stream: {session_id}")
    except Exception as e:
        print(f"Error in analytics stream websocket: {e}")
    finally:
        # Cleanup
        heartbeat_task.cancel()
        await connection_manager.disconnect(session_id)


@router.get("/connections/status")
async def get_connections_status() -> dict:
    """
    Get WebSocket connections status.

    Returns:
        Connection statistics
    """
    return {
        "active_connections": connection_manager.get_active_connections_count(),
        "max_connections": 1000,  # From settings
        "status": "operational",
    }
