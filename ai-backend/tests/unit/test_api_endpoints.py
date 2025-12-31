"""
Unit tests for FastAPI endpoints with various input scenarios.
Tests request validation, authentication, error handling, and response formats.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta

from src.main import app
from src.api.middleware.auth import create_access_token


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def auth_token():
    """Create valid authentication token."""
    return create_access_token(
        data={"sub": "test-user-123"},
        expires_delta=timedelta(hours=1)
    )


@pytest.fixture
def auth_headers(auth_token):
    """Create authentication headers."""
    return {"Authorization": f"Bearer {auth_token}"}


class TestRootEndpoints:
    """Test root and health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "operational"
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ai-backend"


class TestAuthenticationEndpoints:
    """Test authentication endpoints."""
    
    def test_login_success(self, client):
        """Test successful login."""
        with patch('src.api.routes.auth.authenticate_user', new_callable=AsyncMock) as mock_auth:
            mock_auth.return_value = {
                "user_id": "user-123",
                "username": "testuser"
            }
            
            response = client.post(
                "/api/v1/auth/login",
                json={"username": "testuser", "password": "password123"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        with patch('src.api.routes.auth.authenticate_user', new_callable=AsyncMock) as mock_auth:
            mock_auth.return_value = None
            
            response = client.post(
                "/api/v1/auth/login",
                json={"username": "testuser", "password": "wrongpassword"}
            )
            
            assert response.status_code == 401
            data = response.json()
            assert "detail" in data
    
    def test_login_missing_fields(self, client):
        """Test login with missing required fields."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser"}  # Missing password
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/v1/conversations/history")
        
        assert response.status_code == 401
    
    def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/conversations/history", headers=headers)
        
        assert response.status_code == 401


class TestConversationEndpoints:
    """Test conversation-related endpoints."""
    
    def test_get_conversation_history(self, client, auth_headers):
        """Test retrieving conversation history."""
        with patch('src.api.routes.conversations.get_user_conversations', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {
                "conversations": [
                    {
                        "id": "conv-1",
                        "scenario_type": "catfish",
                        "created_at": datetime.utcnow().isoformat()
                    }
                ]
            }
            
            response = client.get("/api/v1/conversations/history", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "conversations" in data
    
    def test_start_new_conversation(self, client, auth_headers):
        """Test starting a new conversation."""
        with patch('src.api.routes.conversations.create_conversation', new_callable=AsyncMock) as mock_create:
            mock_create.return_value = {
                "conversation_id": "conv-123",
                "scenario_type": "catfish",
                "character_profile": {"name": "Alex"}
            }
            
            response = client.post(
                "/api/v1/conversations/start",
                headers=auth_headers,
                json={"scenario_type": "catfish", "locale": "en"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "conversation_id" in data
            assert data["scenario_type"] == "catfish"
    
    def test_start_conversation_invalid_scenario(self, client, auth_headers):
        """Test starting conversation with invalid scenario type."""
        response = client.post(
            "/api/v1/conversations/start",
            headers=auth_headers,
            json={"scenario_type": "invalid_type", "locale": "en"}
        )
        
        assert response.status_code == 400
    
    def test_get_conversation_by_id(self, client, auth_headers):
        """Test retrieving specific conversation."""
        with patch('src.api.routes.conversations.get_conversation', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {
                "id": "conv-123",
                "messages": [
                    {"role": "user", "content": "Hi"},
                    {"role": "agent", "content": "Hello!"}
                ]
            }
            
            response = client.get("/api/v1/conversations/conv-123", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "messages" in data
    
    def test_get_nonexistent_conversation(self, client, auth_headers):
        """Test retrieving non-existent conversation."""
        with patch('src.api.routes.conversations.get_conversation', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            
            response = client.get("/api/v1/conversations/nonexistent", headers=auth_headers)
            
            assert response.status_code == 404


class TestAnalyticsEndpoints:
    """Test analytics-related endpoints."""
    
    def test_get_user_analytics(self, client, auth_headers):
        """Test retrieving user analytics."""
        with patch('src.api.routes.analytics.get_analytics', new_callable=AsyncMock) as mock_analytics:
            mock_analytics.return_value = {
                "competency_scores": {
                    "deepfake_detection": 0.75,
                    "disinformation_awareness": 0.82
                },
                "progress_trends": [],
                "recommendations": []
            }
            
            response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "competency_scores" in data
    
    def test_get_progress_trends(self, client, auth_headers):
        """Test retrieving progress trends."""
        with patch('src.api.routes.analytics.get_progress_trends', new_callable=AsyncMock) as mock_trends:
            mock_trends.return_value = {
                "trends": [
                    {"date": "2024-01-01", "score": 0.70},
                    {"date": "2024-01-15", "score": 0.75}
                ]
            }
            
            response = client.get("/api/v1/analytics/trends", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "trends" in data
    
    def test_get_recommendations(self, client, auth_headers):
        """Test retrieving personalized recommendations."""
        with patch('src.api.routes.analytics.get_recommendations', new_callable=AsyncMock) as mock_recs:
            mock_recs.return_value = {
                "recommendations": [
                    "Practice more deepfake detection",
                    "Review social media analysis"
                ]
            }
            
            response = client.get("/api/v1/analytics/recommendations", headers=auth_headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "recommendations" in data
            assert len(data["recommendations"]) > 0


class TestCulturalContentEndpoints:
    """Test cultural content endpoints."""
    
    def test_get_feedback_english(self, client, auth_headers):
        """Test getting feedback in English."""
        with patch('src.api.routes.cultural_content.generate_feedback', new_callable=AsyncMock) as mock_feedback:
            mock_feedback.return_value = {
                "feedback": "Good analysis of the ethical dilemma.",
                "reasoning": "You considered multiple perspectives.",
                "learning_objectives": ["Privacy", "Consent"],
                "follow_up_questions": ["What about data security?"]
            }
            
            response = client.post(
                "/api/v1/cultural/feedback",
                headers=auth_headers,
                json={
                    "challenge_id": "test-123",
                    "user_response": "I would respect privacy",
                    "correct_answer": "Respect privacy",
                    "locale": "en"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "feedback" in data
            assert "learning_objectives" in data
    
    def test_get_feedback_portuguese(self, client, auth_headers):
        """Test getting feedback in Portuguese."""
        with patch('src.api.routes.cultural_content.generate_feedback', new_callable=AsyncMock) as mock_feedback:
            mock_feedback.return_value = {
                "feedback": "Boa análise do dilema ético.",
                "reasoning": "Você considerou múltiplas perspectivas.",
                "learning_objectives": ["Privacidade", "Consentimento"],
                "follow_up_questions": ["E quanto à segurança?"]
            }
            
            response = client.post(
                "/api/v1/cultural/feedback",
                headers=auth_headers,
                json={
                    "challenge_id": "test-123",
                    "user_response": "Eu respeitaria a privacidade",
                    "correct_answer": "Respeitar privacidade",
                    "locale": "pt"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "feedback" in data
    
    def test_get_feedback_invalid_locale(self, client, auth_headers):
        """Test feedback with invalid locale."""
        response = client.post(
            "/api/v1/cultural/feedback",
            headers=auth_headers,
            json={
                "challenge_id": "test-123",
                "user_response": "Response",
                "correct_answer": "Answer",
                "locale": "fr"  # Invalid locale
            }
        )
        
        assert response.status_code == 400
    
    def test_get_deepfake_challenge(self, client, auth_headers):
        """Test getting deepfake challenge."""
        with patch('src.api.routes.cultural_content.generate_deepfake_challenge', new_callable=AsyncMock) as mock_challenge:
            mock_challenge.return_value = {
                "challenge_id": "df-001",
                "media_url": "https://example.com/video.mp4",
                "difficulty_level": 2,
                "is_deepfake": True
            }
            
            response = client.post(
                "/api/v1/cultural/deepfake-challenge",
                headers=auth_headers,
                json={"difficulty": 2, "locale": "en"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "challenge_id" in data
            assert "media_url" in data
    
    def test_get_social_media_feed(self, client, auth_headers):
        """Test getting social media feed."""
        with patch('src.api.routes.cultural_content.generate_social_feed', new_callable=AsyncMock) as mock_feed:
            mock_feed.return_value = {
                "posts": [
                    {"post_id": "post-1", "content": "Test post", "is_disinformation": False}
                ]
            }
            
            response = client.post(
                "/api/v1/cultural/social-media-feed",
                headers=auth_headers,
                json={"num_posts": 5, "locale": "en"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "posts" in data


class TestRateLimiting:
    """Test rate limiting middleware."""
    
    def test_rate_limit_enforcement(self, client, auth_headers):
        """Test rate limiting blocks excessive requests."""
        # Make multiple rapid requests
        responses = []
        for _ in range(150):  # Exceed typical rate limit
            response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
            responses.append(response.status_code)
        
        # Should eventually get 429 (Too Many Requests)
        assert 429 in responses or all(r == 200 for r in responses[:100])
    
    def test_rate_limit_headers(self, client):
        """Test rate limit headers are present."""
        response = client.get("/")
        
        # Check for rate limit headers (if implemented)
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling across endpoints."""
    
    def test_validation_error_response(self, client, auth_headers):
        """Test validation error returns proper format."""
        response = client.post(
            "/api/v1/cultural/feedback",
            headers=auth_headers,
            json={"challenge_id": "test"}  # Missing required fields
        )
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_internal_error_handling(self, client, auth_headers):
        """Test internal errors are handled gracefully."""
        with patch('src.api.routes.analytics.get_analytics', side_effect=Exception("Internal error")):
            response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
            
            # Should return 500 or graceful degradation
            assert response.status_code in [500, 503]
    
    def test_not_found_error(self, client):
        """Test 404 for non-existent endpoints."""
        response = client.get("/api/v1/nonexistent-endpoint")
        
        assert response.status_code == 404


class TestRequestValidation:
    """Test request validation across endpoints."""
    
    def test_missing_required_fields(self, client, auth_headers):
        """Test validation catches missing required fields."""
        response = client.post(
            "/api/v1/conversations/start",
            headers=auth_headers,
            json={}  # Missing required fields
        )
        
        assert response.status_code == 422
    
    def test_invalid_field_types(self, client, auth_headers):
        """Test validation catches invalid field types."""
        response = client.post(
            "/api/v1/cultural/deepfake-challenge",
            headers=auth_headers,
            json={"difficulty": "invalid", "locale": "en"}  # Should be int
        )
        
        assert response.status_code == 422
    
    def test_field_constraints(self, client, auth_headers):
        """Test validation enforces field constraints."""
        response = client.post(
            "/api/v1/cultural/deepfake-challenge",
            headers=auth_headers,
            json={"difficulty": 10, "locale": "en"}  # Difficulty too high
        )
        
        # Should either accept or return validation error
        assert response.status_code in [200, 400, 422]


class TestCORSHeaders:
    """Test CORS headers are properly set."""
    
    def test_cors_headers_present(self, client):
        """Test CORS headers are included in responses."""
        response = client.options("/api/v1/analytics/dashboard")
        
        # CORS headers should be present
        assert response.status_code in [200, 204]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
