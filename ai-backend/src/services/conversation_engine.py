"""
Conversation Engine for real-time AI interactions.

Manages WebSocket-based conversations with CrewAI agents, including
realistic typing delays, message routing, and context preservation.
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect

from src.api.websocket import ConnectionManager, connection_manager
from src.models.requests import ActivityType, ChatMessage, LocaleEnum
from src.services.conversation_memory import conversation_memory
from src.tools.typing_delay import typing_simulator


class ConversationSession:
    """
    Represents an active conversation session.
    
    Manages conversation state, history, and agent interactions.
    """

    def __init__(
        self,
        session_id: str,
        user_id: str,
        conversation_type: ActivityType,
        websocket: WebSocket,
        locale: LocaleEnum = LocaleEnum.EN,
    ):
        """
        Initialize conversation session.
        
        Args:
            session_id: Unique session identifier
            user_id: User identifier
            conversation_type: Type of conversation
            websocket: WebSocket connection
            locale: User locale
        """
        self.session_id = session_id
        self.user_id = user_id
        self.conversation_type = conversation_type
        self.websocket = websocket
        self.locale = locale
        
        # Conversation state
        self.conversation_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.started_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        
        # Agent state
        self.active_agents: List[str] = []
        self.agent_memory: Dict[str, Any] = {}
        
        # Session metadata
        self.message_count = 0
        self.is_active = True

    async def add_message(self, sender: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> ChatMessage:
        """
        Add a message to conversation history.
        
        Args:
            sender: Message sender (user or agent role)
            content: Message content
            metadata: Optional message metadata
            
        Returns:
            ChatMessage object
        """
        message = ChatMessage(
            message_id=str(uuid4()),
            sender=sender,
            content=content,
            timestamp=datetime.utcnow(),
        )
        
        # Store in local history
        self.conversation_history.append({
            "message_id": message.message_id,
            "sender": sender,
            "content": content,
            "timestamp": message.timestamp.isoformat(),
            "metadata": metadata or {},
        })
        
        # Persist to memory store
        await conversation_memory.save_message(
            session_id=self.session_id,
            sender=sender,
            content=content,
            metadata=metadata,
        )
        
        self.message_count += 1
        self.last_activity = datetime.utcnow()
        
        return message

    def get_recent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversation history.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of recent messages
        """
        return self.conversation_history[-limit:]

    def update_context(self, key: str, value: Any) -> None:
        """
        Update session context.
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        self.last_activity = datetime.utcnow()

    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Get context value.
        
        Args:
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        return self.context.get(key, default)

    def get_session_duration(self) -> float:
        """
        Get session duration in seconds.
        
        Returns:
            Duration in seconds
        """
        return (datetime.utcnow() - self.started_at).total_seconds()

    def is_idle(self, max_idle_seconds: int = 300) -> bool:
        """
        Check if session is idle.
        
        Args:
            max_idle_seconds: Maximum idle time in seconds
            
        Returns:
            True if idle, False otherwise
        """
        idle_seconds = (datetime.utcnow() - self.last_activity).total_seconds()
        return idle_seconds > max_idle_seconds


class ConversationEngine:
    """
    Main conversation engine for managing real-time AI interactions.
    
    Handles WebSocket connections, message routing to CrewAI agents,
    and conversation state management.
    """

    def __init__(self, connection_manager: ConnectionManager):
        """
        Initialize conversation engine.
        
        Args:
            connection_manager: WebSocket connection manager
        """
        self.connection_manager = connection_manager
        self.active_sessions: Dict[str, ConversationSession] = {}
        
        # Agent routing configuration
        self.agent_routes = {
            ActivityType.CATFISH_CHAT: "catfish_character",
            ActivityType.SOCIAL_MEDIA_SIM: "social_media_simulator",
            ActivityType.ETHICS_FEEDBACK: "ethics_mentor",
            ActivityType.DEEPFAKE_DETECTION: "deepfake_analyst",
        }

    async def create_session(
        self,
        session_id: str,
        user_id: str,
        conversation_type: ActivityType,
        websocket: WebSocket,
        locale: LocaleEnum = LocaleEnum.EN,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> ConversationSession:
        """
        Create a new conversation session.
        
        Args:
            session_id: Unique session identifier
            user_id: User identifier
            conversation_type: Type of conversation
            websocket: WebSocket connection
            locale: User locale
            initial_context: Optional initial context
            
        Returns:
            ConversationSession object
        """
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type,
            websocket=websocket,
            locale=locale,
        )
        
        if initial_context:
            session.context.update(initial_context)
        
        # Initialize context in memory store
        await conversation_memory.initialize_context(
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type.value,
            locale=locale.value,
            initial_data=initial_context,
        )
        
        self.active_sessions[session_id] = session
        
        print(f"📝 Created conversation session: {session_id} (type: {conversation_type.value})")
        
        return session

    async def handle_websocket_connection(
        self,
        websocket: WebSocket,
        session_id: str,
        user_id: str,
        conversation_type: str,
        locale: str = "en",
    ) -> None:
        """
        Handle WebSocket connection lifecycle.
        
        Args:
            websocket: WebSocket connection
            session_id: Session identifier
            user_id: User identifier
            conversation_type: Type of conversation
            locale: User locale
        """
        # Connect WebSocket
        await self.connection_manager.connect(
            websocket=websocket,
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type,
        )
        
        # Create conversation session
        try:
            activity_type = ActivityType(conversation_type)
            locale_enum = LocaleEnum(locale)
        except ValueError as e:
            await self.connection_manager.send_personal_message(
                session_id,
                {
                    "type": "error",
                    "error": "invalid_parameters",
                    "detail": str(e),
                },
            )
            await self.connection_manager.disconnect(session_id)
            return
        
        session = await self.create_session(
            session_id=session_id,
            user_id=user_id,
            conversation_type=activity_type,
            websocket=websocket,
            locale=locale_enum,
        )
        
        # Send welcome message
        await self.send_welcome_message(session)
        
        # Start heartbeat task
        heartbeat_task = asyncio.create_task(self._heartbeat_loop(session_id))
        
        try:
            # Message handling loop
            while session.is_active:
                try:
                    # Receive message from client
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Process message
                    await self.process_message(session, message)
                    
                except WebSocketDisconnect:
                    print(f"🔌 WebSocket disconnected: {session_id}")
                    break
                except json.JSONDecodeError:
                    await self.send_error(session_id, "Invalid JSON format")
                except Exception as e:
                    print(f"❌ Error processing message: {e}")
                    await self.send_error(session_id, f"Error processing message: {str(e)}")
        
        finally:
            # Cleanup
            heartbeat_task.cancel()
            await self.cleanup_session(session_id)

    async def process_message(self, session: ConversationSession, message: Dict[str, Any]) -> None:
        """
        Process incoming message and route to appropriate handler.
        
        Args:
            session: Conversation session
            message: Incoming message data
        """
        message_type = message.get("type")
        
        if message_type == "user_message":
            await self.handle_user_message(session, message)
        
        elif message_type == "typing_start":
            # User started typing - could be used for analytics
            session.update_context("user_typing", True)
        
        elif message_type == "typing_stop":
            # User stopped typing
            session.update_context("user_typing", False)
        
        elif message_type == "ping":
            await self.connection_manager.send_personal_message(
                session.session_id,
                {"type": "pong", "timestamp": datetime.utcnow().isoformat()},
            )
        
        else:
            await self.send_error(
                session.session_id,
                f"Unknown message type: {message_type}",
            )

    async def handle_user_message(self, session: ConversationSession, message: Dict[str, Any]) -> None:
        """
        Handle user message and generate AI response.
        
        Args:
            session: Conversation session
            message: User message data
        """
        user_content = message.get("content", "")
        
        if not user_content.strip():
            await self.send_error(session.session_id, "Empty message")
            return
        
        # Add user message to history
        user_msg = await session.add_message("user", user_content)
        
        # Send acknowledgment
        await self.connection_manager.send_personal_message(
            session.session_id,
            {
                "type": "message_received",
                "message_id": user_msg.message_id,
                "timestamp": user_msg.timestamp.isoformat(),
            },
        )
        
        # Create recovery point before agent processing
        await conversation_memory.create_recovery_point(session.session_id)
        
        # Route to appropriate agent (will be implemented with CrewAI integration)
        agent_type = self.agent_routes.get(session.conversation_type, "ethics_mentor")
        
        # For now, send a placeholder response
        # This will be replaced with actual CrewAI agent calls in later integration
        await self.send_agent_response(
            session=session,
            agent_type=agent_type,
            content=f"[Placeholder] AI response to: {user_content[:50]}...",
            metadata={"note": "CrewAI integration pending"},
        )

    async def send_agent_response(
        self,
        session: ConversationSession,
        agent_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        simulate_typing: bool = True,
    ) -> None:
        """
        Send agent response to user with realistic typing delay.
        
        Args:
            session: Conversation session
            agent_type: Type of agent responding
            content: Response content
            metadata: Optional response metadata
            simulate_typing: Whether to simulate typing delay
        """
        # Simulate typing delay if enabled
        if simulate_typing:
            # Create callback for typing indicators
            async def typing_callback(indicator_data: Dict[str, Any]) -> None:
                await self.connection_manager.send_personal_message(
                    session.session_id,
                    {
                        **indicator_data,
                        "agent": agent_type,
                    },
                )
            
            # Simulate typing with personality-based delay
            await typing_simulator.simulate_typing(
                message=content,
                personality=agent_type,
                send_callback=typing_callback,
            )
        
        # Add agent message to history
        agent_msg = await session.add_message(agent_type, content, metadata)
        
        # Send to client
        await self.connection_manager.send_personal_message(
            session.session_id,
            {
                "type": "agent_message",
                "message_id": agent_msg.message_id,
                "agent": agent_type,
                "content": content,
                "timestamp": agent_msg.timestamp.isoformat(),
                "metadata": metadata or {},
            },
        )

    async def send_welcome_message(self, session: ConversationSession) -> None:
        """
        Send welcome message to user.
        
        Args:
            session: Conversation session
        """
        welcome_messages = {
            ActivityType.CATFISH_CHAT: "Hi! I'm excited to chat with you. What's up?",
            ActivityType.SOCIAL_MEDIA_SIM: "Welcome to the social media simulation. Start exploring the feed!",
            ActivityType.ETHICS_FEEDBACK: "Hello! I'm here to help you understand cyber ethics. How can I assist you?",
            ActivityType.DEEPFAKE_DETECTION: "Welcome to deepfake detection training. Let's analyze some media!",
        }
        
        welcome_content = welcome_messages.get(
            session.conversation_type,
            "Welcome! How can I help you today?",
        )
        
        agent_type = self.agent_routes.get(session.conversation_type, "ethics_mentor")
        
        await self.send_agent_response(
            session=session,
            agent_type=agent_type,
            content=welcome_content,
            metadata={"is_welcome": True},
            simulate_typing=False,  # No typing delay for welcome message
        )

    async def send_error(self, session_id: str, error_message: str) -> None:
        """
        Send error message to client.
        
        Args:
            session_id: Session identifier
            error_message: Error message
        """
        await self.connection_manager.send_personal_message(
            session_id,
            {
                "type": "error",
                "error": error_message,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    async def cleanup_session(self, session_id: str) -> None:
        """
        Cleanup conversation session.
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.is_active = False
            
            # Save conversation history (will be implemented with database integration)
            print(f"💾 Saving conversation history for session {session_id}")
            print(f"   Messages: {session.message_count}")
            print(f"   Duration: {session.get_session_duration():.1f}s")
            
            # Remove from active sessions
            del self.active_sessions[session_id]
        
        # Disconnect WebSocket
        await self.connection_manager.disconnect(session_id)

    async def _heartbeat_loop(self, session_id: str, interval: int = 30) -> None:
        """
        Periodic heartbeat to keep connection alive.
        
        Args:
            session_id: Session identifier
            interval: Heartbeat interval in seconds
        """
        while session_id in self.active_sessions:
            await asyncio.sleep(interval)
            
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                
                # Check if session is idle
                if session.is_idle(max_idle_seconds=300):
                    print(f"⏰ Session {session_id} is idle, sending reminder")
                    await self.connection_manager.send_personal_message(
                        session_id,
                        {
                            "type": "idle_reminder",
                            "message": "Are you still there?",
                        },
                    )
                
                # Ping connection
                await self.connection_manager.ping_connection(session_id)

    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """
        Get conversation session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            ConversationSession or None
        """
        return self.active_sessions.get(session_id)

    def get_active_sessions_count(self) -> int:
        """
        Get count of active sessions.
        
        Returns:
            Number of active sessions
        """
        return len(self.active_sessions)

    def get_user_sessions(self, user_id: str) -> List[ConversationSession]:
        """
        Get all active sessions for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of user's active sessions
        """
        return [
            session
            for session in self.active_sessions.values()
            if session.user_id == user_id
        ]

    async def recover_session(
        self,
        session_id: str,
        websocket: WebSocket,
    ) -> Optional[ConversationSession]:
        """
        Recover a disconnected session.
        
        Args:
            session_id: Session identifier
            websocket: New WebSocket connection
            
        Returns:
            Recovered session or None
        """
        # Try to recover from memory
        recovery_data = await conversation_memory.recover_session(session_id)
        
        if not recovery_data:
            print(f"⚠️ No recovery data found for session {session_id}")
            return None
        
        # Get conversation history
        history = await conversation_memory.get_conversation_history(session_id)
        
        # Create new session with recovered data
        try:
            activity_type = ActivityType(recovery_data["conversation_type"])
        except ValueError:
            print(f"⚠️ Invalid conversation type in recovery data")
            return None
        
        session = ConversationSession(
            session_id=session_id,
            user_id=recovery_data["user_id"],
            conversation_type=activity_type,
            websocket=websocket,
            locale=LocaleEnum.EN,  # Will be updated from context
        )
        
        # Restore conversation history
        session.conversation_history = history
        session.message_count = len(history)
        
        self.active_sessions[session_id] = session
        
        print(f"🔄 Recovered session {session_id} with {len(history)} messages")
        
        # Send recovery notification
        await self.connection_manager.send_personal_message(
            session_id,
            {
                "type": "session_recovered",
                "message_count": len(history),
                "recovered_at": datetime.utcnow().isoformat(),
            },
        )
        
        return session


# Global conversation engine instance
conversation_engine = ConversationEngine(connection_manager)
