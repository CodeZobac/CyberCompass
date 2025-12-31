"""WebSocket connection management for real-time communication."""

import asyncio
import json
from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect, status
from fastapi.websockets import WebSocketState

from src.config import get_settings

settings = get_settings()


class ConnectionManager:
    """
    Manages WebSocket connections for real-time communication.

    Handles connection lifecycle, message routing, and session management.
    """

    def __init__(self):
        """Initialize connection manager."""
        # Active connections: {session_id: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}

        # Connection metadata: {session_id: metadata}
        self.connection_metadata: Dict[str, Dict] = {}

        # Typing indicators: {session_id: is_typing}
        self.typing_status: Dict[str, bool] = {}

    async def connect(
        self, websocket: WebSocket, session_id: str, user_id: str, conversation_type: str
    ) -> None:
        """
        Accept and register a new WebSocket connection.

        Args:
            websocket: WebSocket connection
            session_id: Unique session identifier
            user_id: User identifier
            conversation_type: Type of conversation (catfish_chat, social_media, etc.)
        """
        await websocket.accept()

        self.active_connections[session_id] = websocket
        self.connection_metadata[session_id] = {
            "user_id": user_id,
            "conversation_type": conversation_type,
            "connected_at": datetime.utcnow(),
            "message_count": 0,
        }
        self.typing_status[session_id] = False

        print(f"✅ WebSocket connected: session={session_id}, user={user_id}, type={conversation_type}")

        # Send connection confirmation
        await self.send_personal_message(
            session_id,
            {
                "type": "connection_established",
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    async def disconnect(self, session_id: str) -> None:
        """
        Disconnect and cleanup a WebSocket connection.

        Args:
            session_id: Session identifier to disconnect
        """
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]

            # Close connection if still open
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()

            # Cleanup
            del self.active_connections[session_id]
            del self.connection_metadata[session_id]
            del self.typing_status[session_id]

            print(f"🔌 WebSocket disconnected: session={session_id}")

    async def send_personal_message(self, session_id: str, message: dict) -> None:
        """
        Send a message to a specific WebSocket connection.

        Args:
            session_id: Target session identifier
            message: Message data to send
        """
        if session_id not in self.active_connections:
            print(f"⚠️ Cannot send message: session {session_id} not found")
            return

        websocket = self.active_connections[session_id]

        try:
            # Add timestamp if not present
            if "timestamp" not in message:
                message["timestamp"] = datetime.utcnow().isoformat()

            await websocket.send_json(message)

            # Update message count
            if session_id in self.connection_metadata:
                self.connection_metadata[session_id]["message_count"] += 1

        except Exception as e:
            print(f"❌ Error sending message to {session_id}: {e}")
            await self.disconnect(session_id)

    async def send_typing_indicator(self, session_id: str, is_typing: bool, agent_name: Optional[str] = None) -> None:
        """
        Send typing indicator to a session.

        Args:
            session_id: Target session identifier
            is_typing: Whether agent is typing
            agent_name: Optional agent name
        """
        self.typing_status[session_id] = is_typing

        await self.send_personal_message(
            session_id,
            {
                "type": "typing_indicator",
                "is_typing": is_typing,
                "agent_name": agent_name,
            },
        )

    async def broadcast_to_session(self, session_id: str, message: dict) -> None:
        """
        Broadcast a message to all connections in a session.

        Currently sends to single session, but can be extended for multi-user sessions.

        Args:
            session_id: Session identifier
            message: Message to broadcast
        """
        await self.send_personal_message(session_id, message)

    def get_connection_info(self, session_id: str) -> Optional[Dict]:
        """
        Get connection metadata.

        Args:
            session_id: Session identifier

        Returns:
            Connection metadata or None if not found
        """
        return self.connection_metadata.get(session_id)

    def is_connected(self, session_id: str) -> bool:
        """
        Check if a session is connected.

        Args:
            session_id: Session identifier

        Returns:
            True if connected, False otherwise
        """
        return session_id in self.active_connections

    async def ping_connection(self, session_id: str) -> bool:
        """
        Ping a connection to check if it's alive.

        Args:
            session_id: Session identifier

        Returns:
            True if connection is alive, False otherwise
        """
        if session_id not in self.active_connections:
            return False

        websocket = self.active_connections[session_id]

        try:
            await websocket.send_json({"type": "ping", "timestamp": datetime.utcnow().isoformat()})
            return True
        except Exception:
            await self.disconnect(session_id)
            return False

    async def cleanup_inactive_connections(self, max_idle_seconds: int = 3600) -> None:
        """
        Cleanup connections that have been idle too long.

        Args:
            max_idle_seconds: Maximum idle time before cleanup
        """
        now = datetime.utcnow()
        to_disconnect = []

        for session_id, metadata in self.connection_metadata.items():
            connected_at = metadata["connected_at"]
            idle_seconds = (now - connected_at).total_seconds()

            if idle_seconds > max_idle_seconds:
                to_disconnect.append(session_id)

        for session_id in to_disconnect:
            print(f"🧹 Cleaning up inactive connection: {session_id}")
            await self.disconnect(session_id)

    def get_active_connections_count(self) -> int:
        """
        Get count of active connections.

        Returns:
            Number of active connections
        """
        return len(self.active_connections)

    def get_connections_by_user(self, user_id: str) -> list[str]:
        """
        Get all session IDs for a specific user.

        Args:
            user_id: User identifier

        Returns:
            List of session IDs
        """
        return [
            session_id
            for session_id, metadata in self.connection_metadata.items()
            if metadata["user_id"] == user_id
        ]


# Global connection manager instance
connection_manager = ConnectionManager()


async def authenticate_websocket(websocket: WebSocket, token: Optional[str] = None) -> Optional[dict]:
    """
    Authenticate WebSocket connection using JWT token.

    Args:
        websocket: WebSocket connection
        token: Optional JWT token

    Returns:
        User data if authenticated, None otherwise
    """
    if not token:
        # Try to get token from query parameters
        token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing authentication token")
        return None

    try:
        # Import here to avoid circular dependency
        from src.api.middleware import verify_token

        payload = verify_token(token)
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("roles", []),
            "locale": payload.get("locale", settings.default_locale),
        }
    except Exception as e:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason=f"Authentication failed: {str(e)}")
        return None


async def handle_websocket_message(session_id: str, message: dict) -> dict:
    """
    Process incoming WebSocket message and route to appropriate handler.

    Args:
        session_id: Session identifier
        message: Incoming message data

    Returns:
        Response message
    """
    message_type = message.get("type")

    if message_type == "ping":
        return {"type": "pong", "timestamp": datetime.utcnow().isoformat()}

    elif message_type == "user_message":
        # This will be handled by conversation engine in later tasks
        return {
            "type": "acknowledgment",
            "message_id": message.get("message_id", str(uuid4())),
            "status": "received",
        }

    elif message_type == "typing_start":
        # User started typing
        return {"type": "acknowledgment", "status": "typing_registered"}

    elif message_type == "typing_stop":
        # User stopped typing
        return {"type": "acknowledgment", "status": "typing_stopped"}

    else:
        return {
            "type": "error",
            "error": "unknown_message_type",
            "detail": f"Unknown message type: {message_type}",
        }


async def websocket_heartbeat(session_id: str, interval: int = 30) -> None:
    """
    Send periodic heartbeat to keep connection alive.

    Args:
        session_id: Session identifier
        interval: Heartbeat interval in seconds
    """
    while connection_manager.is_connected(session_id):
        await asyncio.sleep(interval)

        if connection_manager.is_connected(session_id):
            alive = await connection_manager.ping_connection(session_id)
            if not alive:
                print(f"💔 Heartbeat failed for session {session_id}")
                break
