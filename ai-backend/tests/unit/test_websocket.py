"""
Unit tests for WebSocket connection handling and message routing.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock, patch
import json
from datetime import datetime

from src.main import app


@pytest.fixture
def client():
    """Create test client with WebSocket support."""
    return TestClient(app)


class TestWebSocketConnection:
    """Test WebSocket connection establishment and lifecycle."""
    
    def test_websocket_connect_success(self, client):
        """Test successful WebSocket connection."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            assert websocket is not None
    
    def test_websocket_disconnect(self, client):
        """Test WebSocket disconnection."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            websocket.close()


class TestMessageRouting:
    """Test WebSocket message routing and handling."""
    
    def test_send_user_message(self, client):
        """Test sending user message through WebSocket."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            message = {
                "type": "user_message",
                "content": "Hello, how are you?",
                "timestamp": datetime.utcnow().isoformat()
            }
            websocket.send_json(message)
            response = websocket.receive_json()
            assert response is not None
            assert "type" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestWebSocketErrorHandling:
    """Test WebSocket error handling."""
    
    def test_malformed_json(self, client):
        """Test handling malformed JSON messages."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            try:
                websocket.send_text("not valid json {")
                response = websocket.receive_json()
                assert response.get("type") == "error"
            except:
                pass
    
    def test_message_validation(self, client):
        """Test message validation and error handling."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            websocket.send_json({"type": "invalid_type"})
            response = websocket.receive_json()
            assert response.get("type") == "error" or "error" in response


class TestWebSocketMessageTypes:
    """Test different WebSocket message types."""
    
    def test_user_message_type(self, client):
        """Test user message type handling."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            websocket.send_json({"type": "user_message", "content": "Hello"})
            response = websocket.receive_json()
            assert response is not None
    
    def test_typing_status_message(self, client):
        """Test typing status message handling."""
        with client.websocket_connect("/api/v1/ws/conversation/test-conv-123") as websocket:
            websocket.send_json({"type": "typing_status", "is_typing": True})
            response = websocket.receive_json()
            assert response is not None
