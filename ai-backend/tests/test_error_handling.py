"""
Tests for error handling and graceful degradation system.
"""

import pytest
from src.utils.exceptions import (
    AIServiceError,
    AgentUnavailableError,
    ValidationError,
    InvalidLocaleError,
    RateLimitError,
)
from src.utils.error_handler import (
    logger,
    error_monitor,
    handle_exception,
)
from src.services.fallback_service import fallback_service, FallbackContentType
from src.services.health_monitor import health_monitor, ServiceStatus, CircuitBreaker
from src.services.graceful_degradation import graceful_degradation_service


class TestCustomExceptions:
    """Test custom exception classes."""
    
    def test_ai_service_error(self):
        """Test AIServiceError creation and properties."""
        error = AIServiceError(
            message="Test error",
            details={"test": "data"}
        )
        
        assert error.message == "Test error"
        assert error.status_code == 503
        assert error.details["test"] == "data"
        assert "temporarily unavailable" in error.recovery_suggestion.lower()
    
    def test_validation_error(self):
        """Test ValidationError with field errors."""
        error = ValidationError(
            message="Invalid input",
            field_errors={"locale": "Must be en or pt"}
        )
        
        assert error.status_code == 400
        assert "locale" in error.details["field_errors"]
    
    def test_invalid_locale_error(self):
        """Test InvalidLocaleError."""
        error = InvalidLocaleError("fr")
        
        assert "fr" in error.message
        assert error.status_code == 400
    
    def test_rate_limit_error(self):
        """Test RateLimitError."""
        error = RateLimitError(retry_after=60)
        
        assert error.status_code == 429
        assert error.details["retry_after"] == 60
    
    def test_exception_to_dict(self):
        """Test exception serialization."""
        error = AIServiceError("Test")
        error_dict = error.to_dict()
        
        assert error_dict["error"] is True
        assert error_dict["message"] == "Test"
        assert error_dict["status_code"] == 503
        assert "recovery_suggestion" in error_dict


class TestErrorMonitor:
    """Test error monitoring functionality."""
    
    def test_record_error(self):
        """Test error recording."""
        error = AIServiceError("Test error")
        
        initial_count = sum(error_monitor.error_counts.values())
        error_monitor.record_error(error, request_id="test-123")
        final_count = sum(error_monitor.error_counts.values())
        
        assert final_count > initial_count
    
    def test_get_error_stats(self):
        """Test error statistics retrieval."""
        stats = error_monitor.get_error_stats()
        
        assert "total_errors" in stats
        assert "error_counts" in stats
        assert "recent_errors" in stats
        assert "timestamp" in stats


class TestFallbackService:
    """Test fallback service functionality."""
    
    def test_get_fallback_feedback_english(self):
        """Test English fallback feedback."""
        feedback = fallback_service.get_fallback_feedback(locale="en")
        
        assert "feedback" in feedback
        assert "reasoning" in feedback
        assert "learning_objectives" in feedback
        assert "follow_up_questions" in feedback
        assert feedback["is_fallback"] is True
    
    def test_get_fallback_feedback_portuguese(self):
        """Test Portuguese fallback feedback."""
        feedback = fallback_service.get_fallback_feedback(locale="pt")
        
        assert "feedback" in feedback
        assert feedback["is_fallback"] is True
        # Check for Portuguese content
        assert any(char in feedback["feedback"] for char in "áéíóúãõç")
    
    def test_get_fallback_deepfake_challenge(self):
        """Test fallback deepfake challenge."""
        challenge = fallback_service.get_fallback_deepfake_challenge(locale="en")
        
        assert "challenge_id" in challenge
        assert "title" in challenge
        assert "detection_clues" in challenge
        assert challenge["is_fallback"] is True
    
    def test_get_fallback_social_media_post(self):
        """Test fallback social media post."""
        post = fallback_service.get_fallback_social_media_post(locale="en")
        
        assert "post_id" in post
        assert "content" in post
        assert "is_disinformation" in post
        assert post["is_fallback"] is True
    
    def test_get_fallback_catfish_response(self):
        """Test fallback catfish response."""
        response = fallback_service.get_fallback_catfish_response(
            user_message="Hey, how are you?",
            locale="en"
        )
        
        assert "message" in response
        assert "typing_delay" in response
        assert response["is_fallback"] is True
    
    def test_fallback_usage_statistics(self):
        """Test fallback usage tracking."""
        # Use some fallback content
        fallback_service.get_fallback_feedback(locale="en")
        fallback_service.get_fallback_feedback(locale="pt")
        
        stats = fallback_service.get_usage_statistics()
        
        assert "usage_count" in stats
        assert "total_fallbacks" in stats
        assert stats["total_fallbacks"] > 0


class TestCircuitBreaker:
    """Test circuit breaker functionality."""
    
    def test_circuit_breaker_initial_state(self):
        """Test circuit breaker starts closed."""
        cb = CircuitBreaker("test_service")
        
        assert cb.state == "closed"
        assert not cb.is_open()
    
    def test_circuit_breaker_opens_on_failures(self):
        """Test circuit breaker opens after threshold failures."""
        cb = CircuitBreaker("test_service", failure_threshold=3)
        
        # Record failures
        for _ in range(3):
            cb.record_failure()
        
        assert cb.state == "open"
        assert cb.is_open()
    
    def test_circuit_breaker_closes_on_success(self):
        """Test circuit breaker closes after successful calls."""
        cb = CircuitBreaker("test_service", failure_threshold=2, success_threshold=2)
        
        # Open the circuit
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "open"
        
        # Simulate timeout and half-open state
        cb.state = "half_open"
        
        # Record successes
        cb.record_success()
        cb.record_success()
        
        assert cb.state == "closed"


@pytest.mark.asyncio
class TestGracefulDegradation:
    """Test graceful degradation service."""
    
    async def test_feedback_with_fallback_on_error(self):
        """Test automatic fallback when AI function fails."""
        
        async def failing_ai_function():
            raise AIServiceError("Service unavailable")
        
        result = await graceful_degradation_service.get_feedback_with_fallback(
            ai_feedback_func=failing_ai_function,
            locale="en"
        )
        
        assert result["is_fallback"] is True
        assert "feedback" in result
    
    async def test_deepfake_challenge_with_fallback(self):
        """Test deepfake challenge fallback."""
        
        async def failing_challenge_function():
            raise AgentUnavailableError("deepfake_analyst")
        
        result = await graceful_degradation_service.get_deepfake_challenge_with_fallback(
            ai_challenge_func=failing_challenge_function,
            locale="en"
        )
        
        assert result["is_fallback"] is True
        assert "challenge_id" in result
    
    async def test_degradation_statistics(self):
        """Test degradation statistics tracking."""
        stats = graceful_degradation_service.get_degradation_stats()
        
        assert "fallback_usage_count" in stats
        assert "fallback_service_stats" in stats
        assert "health_report" in stats


@pytest.mark.asyncio
class TestHealthMonitor:
    """Test health monitoring functionality."""
    
    async def test_register_service(self):
        """Test service registration."""
        
        async def health_check():
            return True
        
        health_monitor.register_service(
            service_name="test_service",
            health_check=health_check
        )
        
        assert "test_service" in health_monitor.service_status
        assert health_monitor.service_status["test_service"] == ServiceStatus.HEALTHY
    
    async def test_check_service_health(self):
        """Test service health checking."""
        
        async def healthy_check():
            return True
        
        status = await health_monitor.check_service_health(
            service_name="test_healthy",
            health_check=healthy_check
        )
        
        assert status == ServiceStatus.HEALTHY
    
    async def test_service_failure_handling(self):
        """Test service failure detection."""
        
        async def unhealthy_check():
            return False
        
        # Register service
        health_monitor.register_service(
            service_name="test_unhealthy",
            health_check=unhealthy_check
        )
        
        # Check health multiple times to trigger failure
        for _ in range(3):
            await health_monitor.check_service_health(
                service_name="test_unhealthy",
                health_check=unhealthy_check
            )
        
        status = health_monitor.get_service_status("test_unhealthy")
        assert status in [ServiceStatus.DEGRADED, ServiceStatus.UNHEALTHY]
    
    def test_get_health_report(self):
        """Test health report generation."""
        report = health_monitor.get_health_report()
        
        assert "timestamp" in report
        assert "services" in report
        assert "overall_health" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
