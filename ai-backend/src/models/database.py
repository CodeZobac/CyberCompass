"""Pydantic models for database entities."""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class AIUserSessionBase(BaseModel):
    """Base model for AI user session."""
    
    user_id: UUID
    session_id: str
    activity_type: str = Field(..., pattern="^(deepfake_detection|social_media_sim|catfish_chat|ethics_feedback|analytics)$")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    flow_state: Dict[str, Any] = Field(default_factory=dict)


class AIUserSessionCreate(AIUserSessionBase):
    """Model for creating a new AI user session."""
    pass


class AIUserSessionUpdate(BaseModel):
    """Model for updating an AI user session."""
    
    end_time: Optional[datetime] = None
    context: Optional[Dict[str, Any]] = None
    flow_state: Optional[Dict[str, Any]] = None


class AIUserSession(AIUserSessionBase):
    """Complete AI user session model."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIConversationBase(BaseModel):
    """Base model for AI conversation."""
    
    user_id: UUID
    session_id: str
    scenario_type: str = Field(..., pattern="^(catfish_detection|social_media_sim|deepfake_analysis|ethics_discussion)$")
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    agent_memory: Dict[str, Any] = Field(default_factory=dict)
    analysis_results: Optional[Dict[str, Any]] = None
    character_profile: Optional[Dict[str, Any]] = None
    red_flags_revealed: List[Dict[str, Any]] = Field(default_factory=list)


class AIConversationCreate(AIConversationBase):
    """Model for creating a new AI conversation."""
    pass


class AIConversationUpdate(BaseModel):
    """Model for updating an AI conversation."""
    
    messages: Optional[List[Dict[str, Any]]] = None
    agent_memory: Optional[Dict[str, Any]] = None
    analysis_results: Optional[Dict[str, Any]] = None
    character_profile: Optional[Dict[str, Any]] = None
    red_flags_revealed: Optional[List[Dict[str, Any]]] = None


class AIConversation(AIConversationBase):
    """Complete AI conversation model."""
    
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIChallengeResultBase(BaseModel):
    """Base model for AI challenge result."""
    
    user_id: UUID
    session_id: str
    challenge_type: str = Field(..., pattern="^(deepfake_detection|disinformation_identification|catfish_detection|ethics_dilemma)$")
    challenge_data: Dict[str, Any]
    user_response: Dict[str, Any]
    ai_feedback: Dict[str, Any]
    score: Optional[float] = Field(None, ge=0, le=100)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    time_taken_seconds: Optional[int] = None


class AIChallengeResultCreate(AIChallengeResultBase):
    """Model for creating a new AI challenge result."""
    pass


class AIChallengeResult(AIChallengeResultBase):
    """Complete AI challenge result model."""
    
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class AIUserAnalyticsBase(BaseModel):
    """Base model for AI user analytics."""
    
    user_id: UUID
    competency_scores: Dict[str, Any] = Field(default_factory=dict)
    progress_trends: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[Dict[str, Any]] = Field(default_factory=list)
    achievements: List[Dict[str, Any]] = Field(default_factory=list)
    total_sessions: int = 0
    total_challenges_completed: int = 0
    average_score: Optional[float] = None
    last_activity: Optional[datetime] = None


class AIUserAnalyticsCreate(AIUserAnalyticsBase):
    """Model for creating new AI user analytics."""
    pass


class AIUserAnalyticsUpdate(BaseModel):
    """Model for updating AI user analytics."""
    
    competency_scores: Optional[Dict[str, Any]] = None
    progress_trends: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[Dict[str, Any]]] = None
    achievements: Optional[List[Dict[str, Any]]] = None
    total_sessions: Optional[int] = None
    total_challenges_completed: Optional[int] = None
    average_score: Optional[float] = None
    last_activity: Optional[datetime] = None


class AIUserAnalytics(AIUserAnalyticsBase):
    """Complete AI user analytics model."""
    
    id: UUID
    created_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True
