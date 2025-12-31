"""Repository for AI user analytics."""

from typing import Optional
from uuid import UUID

from src.database import SupabaseClient
from src.models.database import (
    AIUserAnalytics,
    AIUserAnalyticsCreate,
    AIUserAnalyticsUpdate,
)
from src.repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository[AIUserAnalytics, AIUserAnalyticsCreate, AIUserAnalyticsUpdate]):
    """Repository for managing AI user analytics."""

    def __init__(self, supabase_client: SupabaseClient):
        """Initialize analytics repository.
        
        Args:
            supabase_client: Supabase client instance
        """
        super().__init__(
            supabase_client=supabase_client,
            table_name="ai_user_analytics",
            model_class=AIUserAnalytics,
        )

    async def get_by_user_id(
        self,
        user_id: UUID,
        use_service_role: bool = False,
    ) -> Optional[AIUserAnalytics]:
        """Get analytics for a user.
        
        Args:
            user_id: User ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            User analytics if found, None otherwise
        """
        try:
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("user_id", str(user_id))
                .execute()
            )
            
            if not response.data:
                return None
            
            return self.model_class(**response.data[0])
        except Exception as e:
            raise Exception(f"Error fetching analytics by user_id: {str(e)}")

    async def get_or_create(
        self,
        user_id: UUID,
        use_service_role: bool = False,
    ) -> AIUserAnalytics:
        """Get analytics for a user, creating if it doesn't exist.
        
        Args:
            user_id: User ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            User analytics
        """
        try:
            # Try to get existing analytics
            analytics = await self.get_by_user_id(user_id, use_service_role)
            
            if analytics:
                return analytics
            
            # Create new analytics if not found
            create_data = AIUserAnalyticsCreate(user_id=user_id)
            return await self.create(create_data, use_service_role)
        except Exception as e:
            raise Exception(f"Error getting or creating analytics: {str(e)}")

    async def increment_sessions(
        self,
        user_id: UUID,
        use_service_role: bool = False,
    ) -> Optional[AIUserAnalytics]:
        """Increment the total sessions count for a user.
        
        Args:
            user_id: User ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Updated analytics if found, None otherwise
        """
        try:
            analytics = await self.get_or_create(user_id, use_service_role)
            
            update_data = AIUserAnalyticsUpdate(
                total_sessions=analytics.total_sessions + 1
            )
            
            return await self.update(analytics.id, update_data, use_service_role)
        except Exception as e:
            raise Exception(f"Error incrementing sessions: {str(e)}")

    async def increment_challenges(
        self,
        user_id: UUID,
        score: Optional[float] = None,
        use_service_role: bool = False,
    ) -> Optional[AIUserAnalytics]:
        """Increment the total challenges count and update average score.
        
        Args:
            user_id: User ID
            score: Score for the challenge (if applicable)
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Updated analytics if found, None otherwise
        """
        try:
            analytics = await self.get_or_create(user_id, use_service_role)
            
            new_total = analytics.total_challenges_completed + 1
            
            # Calculate new average score if score provided
            new_avg_score = analytics.average_score
            if score is not None:
                if analytics.average_score is None:
                    new_avg_score = score
                else:
                    # Weighted average
                    total_score = analytics.average_score * analytics.total_challenges_completed
                    new_avg_score = (total_score + score) / new_total
            
            update_data = AIUserAnalyticsUpdate(
                total_challenges_completed=new_total,
                average_score=new_avg_score,
            )
            
            return await self.update(analytics.id, update_data, use_service_role)
        except Exception as e:
            raise Exception(f"Error incrementing challenges: {str(e)}")
