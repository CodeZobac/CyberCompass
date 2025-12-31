"""Repository for AI conversations."""

from typing import List, Optional
from uuid import UUID

from src.database import SupabaseClient
from src.models.database import (
    AIConversation,
    AIConversationCreate,
    AIConversationUpdate,
)
from src.repositories.base_repository import BaseRepository


class ConversationRepository(BaseRepository[AIConversation, AIConversationCreate, AIConversationUpdate]):
    """Repository for managing AI conversations."""

    def __init__(self, supabase_client: SupabaseClient):
        """Initialize conversation repository.
        
        Args:
            supabase_client: Supabase client instance
        """
        super().__init__(
            supabase_client=supabase_client,
            table_name="ai_conversations",
            model_class=AIConversation,
        )

    async def get_by_session_id(
        self,
        session_id: str,
        use_service_role: bool = False,
    ) -> List[AIConversation]:
        """Get all conversations for a session.
        
        Args:
            session_id: Session ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of conversations for the session
        """
        try:
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("session_id", session_id)
                .order("created_at", desc=False)
                .execute()
            )
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error fetching conversations by session_id: {str(e)}")

    async def get_user_conversations(
        self,
        user_id: UUID,
        scenario_type: Optional[str] = None,
        limit: Optional[int] = None,
        use_service_role: bool = False,
    ) -> List[AIConversation]:
        """Get all conversations for a user.
        
        Args:
            user_id: User ID
            scenario_type: Optional filter by scenario type
            limit: Maximum number of conversations to return
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of user conversations
        """
        try:
            query = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("user_id", str(user_id))
                .order("created_at", desc=True)
            )
            
            if scenario_type:
                query = query.eq("scenario_type", scenario_type)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error fetching user conversations: {str(e)}")

    async def append_message(
        self,
        conversation_id: UUID,
        message: dict,
        use_service_role: bool = False,
    ) -> Optional[AIConversation]:
        """Append a message to a conversation.
        
        Args:
            conversation_id: Conversation ID
            message: Message to append
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Updated conversation if found, None otherwise
        """
        try:
            # First, get the current conversation
            conversation = await self.get_by_id(conversation_id, use_service_role)
            if not conversation:
                return None
            
            # Append the new message
            updated_messages = conversation.messages + [message]
            
            # Update the conversation
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .update({"messages": updated_messages})
                .eq("id", str(conversation_id))
                .execute()
            )
            
            if not response.data:
                return None
            
            return self.model_class(**response.data[0])
        except Exception as e:
            raise Exception(f"Error appending message to conversation: {str(e)}")
