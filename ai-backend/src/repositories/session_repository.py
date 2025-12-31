"""Repository for AI user sessions."""

from typing import List, Optional
from uuid import UUID

from src.database import SupabaseClient
from src.models.database import (
    AIUserSession,
    AIUserSessionCreate,
    AIUserSessionUpdate,
)
from src.repositories.base_repository import BaseRepository


class SessionRepository(BaseRepository[AIUserSession, AIUserSessionCreate, AIUserSessionUpdate]):
    """Repository for managing AI user sessions."""

    def __init__(self, supabase_client: SupabaseClient):
        """Initialize session repository.
        
        Args:
            supabase_client: Supabase client instance
        """
        super().__init__(
            supabase_client=supabase_client,
            table_name="ai_user_sessions",
            model_class=AIUserSession,
        )

    async def get_by_session_id(
        self,
        session_id: str,
        use_service_role: bool = False,
    ) -> Optional[AIUserSession]:
        """Get a session by session_id.
        
        Args:
            session_id: Session ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Session if found, None otherwise
        """
        try:
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("session_id", session_id)
                .execute()
            )
            
            if not response.data:
                return None
            
            return self.model_class(**response.data[0])
        except Exception as e:
            raise Exception(f"Error fetching session by session_id: {str(e)}")

    async def get_user_sessions(
        self,
        user_id: UUID,
        activity_type: Optional[str] = None,
        limit: Optional[int] = None,
        use_service_role: bool = False,
    ) -> List[AIUserSession]:
        """Get all sessions for a user.
        
        Args:
            user_id: User ID
            activity_type: Optional filter by activity type
            limit: Maximum number of sessions to return
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of user sessions
        """
        try:
            query = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("user_id", str(user_id))
                .order("start_time", desc=True)
            )
            
            if activity_type:
                query = query.eq("activity_type", activity_type)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error fetching user sessions: {str(e)}")

    async def get_active_sessions(
        self,
        user_id: UUID,
        use_service_role: bool = False,
    ) -> List[AIUserSession]:
        """Get all active (not ended) sessions for a user.
        
        Args:
            user_id: User ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of active sessions
        """
        try:
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("user_id", str(user_id))
                .is_("end_time", "null")
                .order("start_time", desc=True)
                .execute()
            )
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error fetching active sessions: {str(e)}")
