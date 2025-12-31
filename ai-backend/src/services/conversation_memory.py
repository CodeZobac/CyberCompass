"""
Conversation Memory and Context Management.

Provides persistent storage and retrieval of conversation history,
context preservation across sessions, and state recovery for reconnections.
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ConversationMessage(BaseModel):
    """Represents a single conversation message."""

    message_id: str = Field(default_factory=lambda: str(uuid4()))
    session_id: str
    sender: str  # 'user' or agent role
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConversationContext(BaseModel):
    """Represents conversation context and state."""

    session_id: str
    user_id: str
    conversation_type: str
    locale: str
    context_data: Dict[str, Any] = Field(default_factory=dict)
    agent_memory: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationSnapshot(BaseModel):
    """Complete snapshot of a conversation for recovery."""

    session_id: str
    user_id: str
    conversation_type: str
    locale: str
    messages: List[ConversationMessage]
    context: ConversationContext
    snapshot_timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationMemoryStore:
    """
    In-memory storage for conversation history and context.
    
    This is a temporary implementation that stores data in memory.
    In production, this should be replaced with persistent storage
    (PostgreSQL, Redis, etc.) as implemented in Task 9.
    """

    def __init__(self):
        """Initialize memory store."""
        # Message storage: {session_id: [messages]}
        self.messages: Dict[str, List[ConversationMessage]] = {}
        
        # Context storage: {session_id: context}
        self.contexts: Dict[str, ConversationContext] = {}
        
        # Snapshots for recovery: {session_id: snapshot}
        self.snapshots: Dict[str, ConversationSnapshot] = {}
        
        # User session mapping: {user_id: [session_ids]}
        self.user_sessions: Dict[str, List[str]] = {}

    def store_message(self, message: ConversationMessage) -> None:
        """
        Store a conversation message.
        
        Args:
            message: Message to store
        """
        session_id = message.session_id
        
        if session_id not in self.messages:
            self.messages[session_id] = []
        
        self.messages[session_id].append(message)
        
        # Update context timestamp
        if session_id in self.contexts:
            self.contexts[session_id].updated_at = datetime.utcnow()

    def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None,
        since: Optional[datetime] = None,
    ) -> List[ConversationMessage]:
        """
        Retrieve messages for a session.
        
        Args:
            session_id: Session identifier
            limit: Optional limit on number of messages
            since: Optional timestamp to filter messages after
            
        Returns:
            List of messages
        """
        messages = self.messages.get(session_id, [])
        
        # Filter by timestamp if provided
        if since:
            messages = [msg for msg in messages if msg.timestamp > since]
        
        # Apply limit if provided
        if limit:
            messages = messages[-limit:]
        
        return messages

    def store_context(self, context: ConversationContext) -> None:
        """
        Store conversation context.
        
        Args:
            context: Context to store
        """
        context.updated_at = datetime.utcnow()
        self.contexts[context.session_id] = context
        
        # Update user session mapping
        if context.user_id not in self.user_sessions:
            self.user_sessions[context.user_id] = []
        
        if context.session_id not in self.user_sessions[context.user_id]:
            self.user_sessions[context.user_id].append(context.session_id)

    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """
        Retrieve conversation context.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Context or None if not found
        """
        return self.contexts.get(session_id)

    def update_context_data(
        self,
        session_id: str,
        key: str,
        value: Any,
    ) -> bool:
        """
        Update specific context data.
        
        Args:
            session_id: Session identifier
            key: Context key
            value: Context value
            
        Returns:
            True if updated, False if session not found
        """
        context = self.contexts.get(session_id)
        
        if not context:
            return False
        
        context.context_data[key] = value
        context.updated_at = datetime.utcnow()
        
        return True

    def update_agent_memory(
        self,
        session_id: str,
        agent_name: str,
        memory_data: Dict[str, Any],
    ) -> bool:
        """
        Update agent-specific memory.
        
        Args:
            session_id: Session identifier
            agent_name: Agent name
            memory_data: Memory data to store
            
        Returns:
            True if updated, False if session not found
        """
        context = self.contexts.get(session_id)
        
        if not context:
            return False
        
        if agent_name not in context.agent_memory:
            context.agent_memory[agent_name] = {}
        
        context.agent_memory[agent_name].update(memory_data)
        context.updated_at = datetime.utcnow()
        
        return True

    def create_snapshot(self, session_id: str) -> Optional[ConversationSnapshot]:
        """
        Create a snapshot of conversation for recovery.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Snapshot or None if session not found
        """
        context = self.contexts.get(session_id)
        messages = self.messages.get(session_id, [])
        
        if not context:
            return None
        
        snapshot = ConversationSnapshot(
            session_id=session_id,
            user_id=context.user_id,
            conversation_type=context.conversation_type,
            locale=context.locale,
            messages=messages,
            context=context,
        )
        
        self.snapshots[session_id] = snapshot
        
        return snapshot

    def restore_from_snapshot(self, session_id: str) -> Optional[ConversationSnapshot]:
        """
        Restore conversation from snapshot.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Snapshot or None if not found
        """
        snapshot = self.snapshots.get(session_id)
        
        if not snapshot:
            return None
        
        # Restore messages and context
        self.messages[session_id] = snapshot.messages
        self.contexts[session_id] = snapshot.context
        
        return snapshot

    def get_user_sessions(self, user_id: str) -> List[str]:
        """
        Get all session IDs for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of session IDs
        """
        return self.user_sessions.get(user_id, [])

    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get summary of a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary or None
        """
        context = self.contexts.get(session_id)
        messages = self.messages.get(session_id, [])
        
        if not context:
            return None
        
        return {
            "session_id": session_id,
            "user_id": context.user_id,
            "conversation_type": context.conversation_type,
            "locale": context.locale,
            "message_count": len(messages),
            "created_at": context.created_at.isoformat(),
            "updated_at": context.updated_at.isoformat(),
            "duration_seconds": (context.updated_at - context.created_at).total_seconds(),
        }

    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Cleanup old sessions that haven't been updated recently.
        
        Args:
            max_age_hours: Maximum age in hours
            
        Returns:
            Number of sessions cleaned up
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        sessions_to_remove = []
        
        for session_id, context in self.contexts.items():
            if context.updated_at < cutoff_time:
                sessions_to_remove.append(session_id)
        
        # Remove old sessions
        for session_id in sessions_to_remove:
            self._remove_session(session_id)
        
        return len(sessions_to_remove)

    def _remove_session(self, session_id: str) -> None:
        """
        Remove a session from storage.
        
        Args:
            session_id: Session identifier
        """
        # Remove messages
        if session_id in self.messages:
            del self.messages[session_id]
        
        # Remove context
        context = self.contexts.get(session_id)
        if context:
            # Remove from user session mapping
            if context.user_id in self.user_sessions:
                if session_id in self.user_sessions[context.user_id]:
                    self.user_sessions[context.user_id].remove(session_id)
            
            del self.contexts[session_id]
        
        # Remove snapshot
        if session_id in self.snapshots:
            del self.snapshots[session_id]

    def export_session(self, session_id: str) -> Optional[str]:
        """
        Export session data as JSON.
        
        Args:
            session_id: Session identifier
            
        Returns:
            JSON string or None
        """
        snapshot = self.create_snapshot(session_id)
        
        if not snapshot:
            return None
        
        return snapshot.model_dump_json(indent=2)

    def import_session(self, json_data: str) -> Optional[str]:
        """
        Import session data from JSON.
        
        Args:
            json_data: JSON string
            
        Returns:
            Session ID or None if import failed
        """
        try:
            snapshot = ConversationSnapshot.model_validate_json(json_data)
            
            # Restore from snapshot
            self.messages[snapshot.session_id] = snapshot.messages
            self.contexts[snapshot.session_id] = snapshot.context
            self.snapshots[snapshot.session_id] = snapshot
            
            # Update user session mapping
            if snapshot.user_id not in self.user_sessions:
                self.user_sessions[snapshot.user_id] = []
            
            if snapshot.session_id not in self.user_sessions[snapshot.user_id]:
                self.user_sessions[snapshot.user_id].append(snapshot.session_id)
            
            return snapshot.session_id
        
        except Exception as e:
            print(f"❌ Error importing session: {e}")
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory store statistics.
        
        Returns:
            Statistics dictionary
        """
        total_messages = sum(len(msgs) for msgs in self.messages.values())
        
        return {
            "total_sessions": len(self.contexts),
            "total_messages": total_messages,
            "total_users": len(self.user_sessions),
            "total_snapshots": len(self.snapshots),
            "average_messages_per_session": (
                total_messages / len(self.contexts) if self.contexts else 0
            ),
        }


class ConversationMemoryManager:
    """
    High-level manager for conversation memory operations.
    
    Provides convenient methods for storing, retrieving, and managing
    conversation history and context.
    """

    def __init__(self, store: Optional[ConversationMemoryStore] = None):
        """
        Initialize memory manager.
        
        Args:
            store: Optional memory store instance
        """
        self.store = store or ConversationMemoryStore()

    async def save_message(
        self,
        session_id: str,
        sender: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationMessage:
        """
        Save a conversation message.
        
        Args:
            session_id: Session identifier
            sender: Message sender
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Saved message
        """
        message = ConversationMessage(
            session_id=session_id,
            sender=sender,
            content=content,
            metadata=metadata or {},
        )
        
        self.store.store_message(message)
        
        return message

    async def get_conversation_history(
        self,
        session_id: str,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history.
        
        Args:
            session_id: Session identifier
            limit: Optional message limit
            
        Returns:
            List of messages as dictionaries
        """
        messages = self.store.get_messages(session_id, limit=limit)
        
        return [
            {
                "message_id": msg.message_id,
                "sender": msg.sender,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata,
            }
            for msg in messages
        ]

    async def initialize_context(
        self,
        session_id: str,
        user_id: str,
        conversation_type: str,
        locale: str,
        initial_data: Optional[Dict[str, Any]] = None,
    ) -> ConversationContext:
        """
        Initialize conversation context.
        
        Args:
            session_id: Session identifier
            user_id: User identifier
            conversation_type: Type of conversation
            locale: User locale
            initial_data: Optional initial context data
            
        Returns:
            Created context
        """
        context = ConversationContext(
            session_id=session_id,
            user_id=user_id,
            conversation_type=conversation_type,
            locale=locale,
            context_data=initial_data or {},
        )
        
        self.store.store_context(context)
        
        return context

    async def update_context(
        self,
        session_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """
        Update conversation context.
        
        Args:
            session_id: Session identifier
            updates: Context updates
            
        Returns:
            True if successful
        """
        for key, value in updates.items():
            self.store.update_context_data(session_id, key, value)
        
        return True

    async def save_agent_state(
        self,
        session_id: str,
        agent_name: str,
        state: Dict[str, Any],
    ) -> bool:
        """
        Save agent state to memory.
        
        Args:
            session_id: Session identifier
            agent_name: Agent name
            state: Agent state data
            
        Returns:
            True if successful
        """
        return self.store.update_agent_memory(session_id, agent_name, state)

    async def get_agent_state(
        self,
        session_id: str,
        agent_name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get agent state from memory.
        
        Args:
            session_id: Session identifier
            agent_name: Agent name
            
        Returns:
            Agent state or None
        """
        context = self.store.get_context(session_id)
        
        if not context:
            return None
        
        return context.agent_memory.get(agent_name)

    async def create_recovery_point(self, session_id: str) -> bool:
        """
        Create a recovery point for the session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful
        """
        snapshot = self.store.create_snapshot(session_id)
        return snapshot is not None

    async def recover_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Recover a session from snapshot.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Recovery data or None
        """
        snapshot = self.store.restore_from_snapshot(session_id)
        
        if not snapshot:
            return None
        
        return {
            "session_id": snapshot.session_id,
            "user_id": snapshot.user_id,
            "conversation_type": snapshot.conversation_type,
            "message_count": len(snapshot.messages),
            "recovered_at": datetime.utcnow().isoformat(),
        }

    async def cleanup_expired_sessions(self, max_age_hours: int = 24) -> int:
        """
        Cleanup expired sessions.
        
        Args:
            max_age_hours: Maximum age in hours
            
        Returns:
            Number of sessions cleaned up
        """
        return self.store.cleanup_old_sessions(max_age_hours)


# Global memory manager instance
conversation_memory = ConversationMemoryManager()
