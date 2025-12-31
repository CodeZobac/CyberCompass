"""Pydantic models for request validation."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class LocaleEnum(str, Enum):
    """Supported locales."""

    EN = "en"
    PT = "pt"


class ActivityType(str, Enum):
    """Types of educational activities."""

    DEEPFAKE_DETECTION = "deepfake_detection"
    SOCIAL_MEDIA_SIM = "social_media_sim"
    CATFISH_CHAT = "catfish_chat"
    ETHICS_FEEDBACK = "ethics_feedback"
    ANALYTICS = "analytics"


class MediaType(str, Enum):
    """Types of media content."""

    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"


class DisinformationType(str, Enum):
    """Categories of disinformation."""

    HEALTH = "health"
    POLITICS = "politics"
    CONSPIRACY = "conspiracy"
    FAKE_NEWS = "fake_news"
    MANIPULATED_MEDIA = "manipulated_media"


# Authentication Requests


class LoginRequest(BaseModel):
    """User login request."""

    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v.lower()


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")


# Feedback Requests


class FeedbackRequest(BaseModel):
    """Request for AI feedback on ethical decisions."""

    user_id: str = Field(..., description="User identifier")
    challenge_id: str = Field(..., description="Challenge identifier")
    selected_option: str = Field(..., description="User's selected option")
    correct_option: str = Field(..., description="Correct option")
    locale: LocaleEnum = Field(default=LocaleEnum.EN, description="User locale")
    user_history: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="User's learning history"
    )
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "challenge_id": "ethics_001",
                "selected_option": "option_b",
                "correct_option": "option_a",
                "locale": "en",
                "context": {"difficulty": "medium", "topic": "privacy"},
            }
        }


class FeedbackResponse(BaseModel):
    """AI-generated feedback response."""

    feedback: str = Field(..., description="Detailed feedback text")
    reasoning: str = Field(..., description="Explanation of the reasoning")
    learning_objectives: List[str] = Field(
        ..., description="Key learning objectives addressed"
    )
    follow_up_questions: List[str] = Field(
        ..., description="Questions to encourage deeper reflection"
    )
    competency_impact: Dict[str, float] = Field(
        ..., description="Impact on user competency scores"
    )


# Deepfake Challenge Requests


class DeepfakeChallengeRequest(BaseModel):
    """Request to start a deepfake detection challenge."""

    user_id: str = Field(..., description="User identifier")
    difficulty_level: int = Field(default=1, ge=1, le=5, description="Difficulty level (1-5)")
    media_type: Optional[MediaType] = Field(
        default=None, description="Preferred media type"
    )
    locale: LocaleEnum = Field(default=LocaleEnum.EN, description="User locale")


class DeepfakeChallengeResponse(BaseModel):
    """Deepfake challenge data."""

    challenge_id: str = Field(..., description="Challenge identifier")
    media_url: str = Field(..., description="URL to media content")
    media_type: MediaType = Field(..., description="Type of media")
    difficulty_level: int = Field(..., description="Challenge difficulty")
    instructions: str = Field(..., description="Challenge instructions")
    hints: Optional[List[str]] = Field(default=None, description="Optional hints")


class DeepfakeSubmissionRequest(BaseModel):
    """User's deepfake detection submission."""

    challenge_id: str = Field(..., description="Challenge identifier")
    user_id: str = Field(..., description="User identifier")
    is_deepfake: bool = Field(..., description="User's detection decision")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level (0-1)")
    reasoning: Optional[str] = Field(default=None, description="User's reasoning")


class DeepfakeSubmissionResponse(BaseModel):
    """Feedback on deepfake detection submission."""

    correct: bool = Field(..., description="Whether detection was correct")
    actual_answer: bool = Field(..., description="Actual answer (is it a deepfake)")
    feedback: str = Field(..., description="Detailed feedback")
    detection_clues: List[str] = Field(..., description="Key detection clues")
    score: float = Field(..., description="Score for this challenge")


# Social Media Simulation Requests


class SocialMediaSimulationRequest(BaseModel):
    """Request to start social media simulation."""

    user_id: str = Field(..., description="User identifier")
    session_duration_minutes: int = Field(
        default=15, ge=5, le=60, description="Session duration"
    )
    disinformation_ratio: float = Field(
        default=0.3, ge=0.0, le=1.0, description="Ratio of disinformation posts"
    )
    categories: Optional[List[DisinformationType]] = Field(
        default=None, description="Disinformation categories to include"
    )
    locale: LocaleEnum = Field(default=LocaleEnum.EN, description="User locale")


class SocialMediaPost(BaseModel):
    """Social media post data."""

    post_id: str = Field(..., description="Post identifier")
    content: str = Field(..., description="Post content")
    author_name: str = Field(..., description="Author name")
    author_avatar: Optional[str] = Field(default=None, description="Author avatar URL")
    timestamp: datetime = Field(..., description="Post timestamp")
    likes: int = Field(default=0, description="Number of likes")
    shares: int = Field(default=0, description="Number of shares")
    comments_count: int = Field(default=0, description="Number of comments")
    is_disinformation: bool = Field(..., description="Whether post is disinformation")
    category: Optional[DisinformationType] = Field(
        default=None, description="Disinformation category"
    )


# Catfish Chat Requests


class CatfishChatStartRequest(BaseModel):
    """Request to start catfish chat simulation."""

    user_id: str = Field(..., description="User identifier")
    difficulty_level: int = Field(default=1, ge=1, le=5, description="Difficulty level")
    character_age_range: Optional[str] = Field(
        default=None, description="Character age range (e.g., '13-17')"
    )
    locale: LocaleEnum = Field(default=LocaleEnum.EN, description="User locale")


class CatfishCharacterProfile(BaseModel):
    """Catfish character profile."""

    character_id: str = Field(..., description="Character identifier")
    name: str = Field(..., description="Character name")
    age: int = Field(..., description="Stated age")
    bio: str = Field(..., description="Character bio")
    interests: List[str] = Field(..., description="Character interests")
    profile_image: Optional[str] = Field(default=None, description="Profile image URL")
    red_flags_count: int = Field(..., description="Number of red flags to reveal")


class ChatMessage(BaseModel):
    """Chat message."""

    message_id: str = Field(..., description="Message identifier")
    sender: str = Field(..., description="Sender (user or character)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")
    typing_delay: Optional[float] = Field(
        default=None, description="Typing delay in seconds"
    )


# Analytics Requests


class AnalyticsRequest(BaseModel):
    """Request for user analytics."""

    user_id: str = Field(..., description="User identifier")
    time_range_days: int = Field(default=30, ge=1, le=365, description="Time range in days")
    include_peer_comparison: bool = Field(
        default=True, description="Include peer comparison"
    )
    locale: LocaleEnum = Field(default=LocaleEnum.EN, description="User locale")


class CompetencyScore(BaseModel):
    """Competency score in a specific domain."""

    domain: str = Field(..., description="Competency domain")
    score: float = Field(..., ge=0.0, le=1.0, description="Score (0-1)")
    trend: str = Field(..., description="Trend (improving, stable, declining)")
    percentile: Optional[float] = Field(
        default=None, description="Percentile compared to peers"
    )


class AnalyticsResponse(BaseModel):
    """User analytics response."""

    user_id: str = Field(..., description="User identifier")
    competency_scores: List[CompetencyScore] = Field(
        ..., description="Competency scores by domain"
    )
    total_challenges_completed: int = Field(..., description="Total challenges completed")
    accuracy_rate: float = Field(..., description="Overall accuracy rate")
    learning_path_recommendations: List[str] = Field(
        ..., description="Recommended learning paths"
    )
    achievements: List[str] = Field(..., description="Earned achievements")
    insights: List[str] = Field(..., description="Personalized insights")


# WebSocket Messages


class WebSocketMessage(BaseModel):
    """WebSocket message structure."""

    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")


class TypingIndicator(BaseModel):
    """Typing indicator message."""

    is_typing: bool = Field(..., description="Whether agent is typing")
    agent_name: Optional[str] = Field(default=None, description="Agent name")
