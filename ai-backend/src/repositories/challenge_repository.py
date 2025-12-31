"""Repository for AI challenge results."""

from typing import List, Optional
from uuid import UUID

from src.database import SupabaseClient
from src.models.database import (
    AIChallengeResult,
    AIChallengeResultCreate,
)
from src.repositories.base_repository import BaseRepository


class ChallengeResultRepository(BaseRepository[AIChallengeResult, AIChallengeResultCreate, None]):
    """Repository for managing AI challenge results."""

    def __init__(self, supabase_client: SupabaseClient):
        """Initialize challenge result repository.
        
        Args:
            supabase_client: Supabase client instance
        """
        super().__init__(
            supabase_client=supabase_client,
            table_name="ai_challenge_results",
            model_class=AIChallengeResult,
        )

    async def get_by_session_id(
        self,
        session_id: str,
        use_service_role: bool = False,
    ) -> List[AIChallengeResult]:
        """Get all challenge results for a session.
        
        Args:
            session_id: Session ID
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of challenge results for the session
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
            raise Exception(f"Error fetching challenge results by session_id: {str(e)}")

    async def get_user_results(
        self,
        user_id: UUID,
        challenge_type: Optional[str] = None,
        limit: Optional[int] = None,
        use_service_role: bool = False,
    ) -> List[AIChallengeResult]:
        """Get all challenge results for a user.
        
        Args:
            user_id: User ID
            challenge_type: Optional filter by challenge type
            limit: Maximum number of results to return
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of user challenge results
        """
        try:
            query = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("user_id", str(user_id))
                .order("created_at", desc=True)
            )
            
            if challenge_type:
                query = query.eq("challenge_type", challenge_type)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error fetching user challenge results: {str(e)}")

    async def get_user_statistics(
        self,
        user_id: UUID,
        challenge_type: Optional[str] = None,
        use_service_role: bool = False,
    ) -> dict:
        """Get statistics for a user's challenge results.
        
        Args:
            user_id: User ID
            challenge_type: Optional filter by challenge type
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Dictionary with statistics (total, average_score, etc.)
        """
        try:
            results = await self.get_user_results(
                user_id=user_id,
                challenge_type=challenge_type,
                use_service_role=use_service_role,
            )
            
            if not results:
                return {
                    "total_challenges": 0,
                    "average_score": 0.0,
                    "total_time_seconds": 0,
                }
            
            total_challenges = len(results)
            scores = [r.score for r in results if r.score is not None]
            times = [r.time_taken_seconds for r in results if r.time_taken_seconds is not None]
            
            return {
                "total_challenges": total_challenges,
                "average_score": sum(scores) / len(scores) if scores else 0.0,
                "total_time_seconds": sum(times) if times else 0,
                "average_time_seconds": sum(times) / len(times) if times else 0,
            }
        except Exception as e:
            raise Exception(f"Error calculating user statistics: {str(e)}")
