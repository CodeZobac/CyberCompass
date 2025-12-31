"""
Pytest configuration and fixtures for CrewAI integration tests.

This module provides shared fixtures and configuration for all
integration tests, ensuring consistent test setup and teardown.
"""

import pytest
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock, patch

# Import test utilities
from test_crewai_flows import MockAgentFactory, MockCrewResult
from test_agent_collaboration import MockAgent, MockCrew
from test_memory_persistence import MockMemorySystem, MockAgentWithMemory


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_agent_factory():
    """Provide a mock agent factory for testing."""
    return MockAgentFactory()


@pytest.fixture
def mock_memory_systems():
    """Provide mock memory systems for testing."""
    return {
        "long_term": MockMemorySystem("long_term"),
        "short_term": MockMemorySystem("short_term"),
        "entity": MockMemorySystem("entity")
    }


@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing."""
    return {
        "user_id": "test_user_123",
        "locale": "en",
        "competency_scores": {
            "deepfake_detection": 0.65,
            "social_media_literacy": 0.72,
            "catfish_awareness": 0.58
        },
        "learning_history": [
            {"challenge_type": "deepfake", "score": 75, "date": "2024-01-01"},
            {"challenge_type": "social_media", "score": 82, "date": "2024-01-02"},
            {"challenge_type": "catfish", "score": 68, "date": "2024-01-03"}
        ]
    }


@pytest.fixture
def sample_conversation_data():
    """Provide sample conversation data for testing."""
    return [
        {
            "message_id": str(uuid.uuid4()),
            "sender": "user",
            "content": "Hi there!",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "message_id": str(uuid.uuid4()),
            "sender": "character",
            "content": "Hey! How's it going?",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "message_id": str(uuid.uuid4()),
            "sender": "user", 
            "content": "Good! What's your favorite music?",
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "message_id": str(uuid.uuid4()),
            "sender": "character",
            "content": "I love pop music! What about you?",
            "timestamp": datetime.utcnow().isoformat()
        }
    ]


@pytest.fixture
def sample_social_media_posts():
    """Provide sample social media posts for testing."""
    return [
        {
            "post_id": "post_1",
            "content": "URGENT: New study reveals shocking truth about vaccines!",
            "author_name": "HealthTruth2024",
            "is_disinformation": True,
            "category": "health",
            "likes": 1250,
            "shares": 340
        },
        {
            "post_id": "post_2",
            "content": "Interesting article about digital privacy from MIT researchers.",
            "author_name": "TechReporter",
            "is_disinformation": False,
            "category": None,
            "likes": 89,
            "shares": 23
        },
        {
            "post_id": "post_3",
            "content": "Share this before they delete it! The government doesn't want you to know!",
            "author_name": "TruthSeeker",
            "is_disinformation": True,
            "category": "conspiracy",
            "likes": 2100,
            "shares": 890
        }
    ]


@pytest.fixture
def sample_deepfake_challenges():
    """Provide sample deepfake challenges for testing."""
    return [
        {
            "challenge_id": "df_001",
            "media_url": "/media/test_video_1.mp4",
            "media_type": "video",
            "is_deepfake": True,
            "difficulty_level": 2,
            "detection_clues": [
                "Unnatural eye movements",
                "Audio-visual synchronization issues",
                "Facial boundary artifacts"
            ]
        },
        {
            "challenge_id": "df_002", 
            "media_url": "/media/test_audio_1.wav",
            "media_type": "audio",
            "is_deepfake": False,
            "difficulty_level": 1,
            "detection_clues": []
        },
        {
            "challenge_id": "df_003",
            "media_url": "/media/test_image_1.jpg",
            "media_type": "image",
            "is_deepfake": True,
            "difficulty_level": 3,
            "detection_clues": [
                "Inconsistent lighting",
                "Pixel-level artifacts",
                "Unnatural skin texture"
            ]
        }
    ]


@pytest.fixture
def sample_catfish_profiles():
    """Provide sample catfish character profiles for testing."""
    return [
        {
            "character_id": "char_001",
            "name": "Alex",
            "stated_age": 16,
            "bio": "Love music, games, and meeting new people!",
            "interests": ["Music", "Gaming", "Movies"],
            "red_flags": [
                "Avoids video calls",
                "Uses outdated slang",
                "Inconsistent location stories",
                "Pushes for personal information"
            ],
            "difficulty_level": 2
        },
        {
            "character_id": "char_002",
            "name": "Jordan",
            "stated_age": 17,
            "bio": "Artist and musician, looking for creative friends",
            "interests": ["Art", "Music", "Photography"],
            "red_flags": [
                "Profile photos look professional",
                "Evasive about school details",
                "Uses adult language patterns",
                "Requests inappropriate photos"
            ],
            "difficulty_level": 4
        }
    ]


@pytest.fixture
def mock_crew_execution():
    """Provide mock crew execution context."""
    def _mock_crew_kickoff(return_value: str = "Mock crew result"):
        with patch('crewai.Crew.kickoff') as mock_kickoff:
            mock_kickoff.return_value = MockCrewResult(return_value)
            yield mock_kickoff
    
    return _mock_crew_kickoff


@pytest.fixture
def integration_test_config():
    """Provide configuration for integration tests."""
    return {
        "test_timeout": 30,  # seconds
        "max_concurrent_flows": 5,
        "memory_cleanup_interval": 3600,  # seconds
        "mock_response_delay": 0.1,  # seconds
        "supported_locales": ["en", "pt"],
        "test_data_retention": 24,  # hours
        "performance_thresholds": {
            "flow_initialization": 2.0,  # seconds
            "agent_response": 1.0,  # seconds
            "memory_operation": 0.1,  # seconds
            "concurrent_flows": 10.0  # seconds for 5 flows
        }
    }


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically cleanup test data after each test."""
    # Setup
    test_sessions = []
    test_memory_systems = []
    
    yield {
        "sessions": test_sessions,
        "memory_systems": test_memory_systems
    }
    
    # Cleanup
    for session_id in test_sessions:
        # Clean up any persistent session data
        pass
    
    for memory_system in test_memory_systems:
        if hasattr(memory_system, 'clear_all'):
            memory_system.clear_all()


@pytest.fixture
def performance_monitor():
    """Provide performance monitoring utilities."""
    class PerformanceMonitor:
        def __init__(self):
            self.metrics = {}
            self.start_times = {}
        
        def start_timer(self, operation: str):
            """Start timing an operation."""
            import time
            self.start_times[operation] = time.time()
        
        def end_timer(self, operation: str) -> float:
            """End timing and return duration."""
            import time
            if operation in self.start_times:
                duration = time.time() - self.start_times[operation]
                self.metrics[operation] = duration
                del self.start_times[operation]
                return duration
            return 0.0
        
        def get_metrics(self) -> Dict[str, float]:
            """Get all recorded metrics."""
            return self.metrics.copy()
        
        def assert_performance(self, operation: str, max_duration: float):
            """Assert that an operation completed within time limit."""
            if operation in self.metrics:
                assert self.metrics[operation] <= max_duration, \
                    f"Operation '{operation}' took {self.metrics[operation]:.2f}s, expected <= {max_duration}s"
    
    return PerformanceMonitor()


@pytest.fixture
def test_data_generator():
    """Provide utilities for generating test data."""
    class TestDataGenerator:
        @staticmethod
        def generate_conversation(length: int = 10) -> List[Dict[str, Any]]:
            """Generate a conversation with specified length."""
            conversation = []
            for i in range(length):
                sender = "user" if i % 2 == 0 else "character"
                conversation.append({
                    "message_id": str(uuid.uuid4()),
                    "sender": sender,
                    "content": f"Test message {i} from {sender}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "turn": i
                })
            return conversation
        
        @staticmethod
        def generate_user_interactions(count: int = 20) -> List[Dict[str, Any]]:
            """Generate user interactions for social media simulation."""
            import random
            
            interactions = []
            interaction_types = ["view", "like", "share", "comment", "report"]
            
            for i in range(count):
                interactions.append({
                    "interaction_id": str(uuid.uuid4()),
                    "post_id": f"post_{random.randint(1, 10)}",
                    "interaction_type": random.choice(interaction_types),
                    "timestamp": datetime.utcnow().isoformat(),
                    "post_is_disinformation": random.choice([True, False])
                })
            
            return interactions
        
        @staticmethod
        def generate_performance_history(count: int = 15) -> List[Dict[str, Any]]:
            """Generate user performance history."""
            import random
            
            history = []
            challenge_types = ["deepfake", "social_media", "catfish"]
            
            for i in range(count):
                history.append({
                    "challenge_id": f"challenge_{i}",
                    "challenge_type": random.choice(challenge_types),
                    "score": random.randint(40, 100),
                    "correct": random.choice([True, False]),
                    "difficulty": random.randint(1, 5),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            return history
    
    return TestDataGenerator()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest for integration tests."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "memory: mark test as memory-related test"
    )
    config.addinivalue_line(
        "markers", "collaboration: mark test as agent collaboration test"
    )
    config.addinivalue_line(
        "markers", "flow: mark test as flow execution test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add integration marker to all tests in integration directory
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Add specific markers based on test names
        if "memory" in item.name.lower():
            item.add_marker(pytest.mark.memory)
        
        if "collaboration" in item.name.lower():
            item.add_marker(pytest.mark.collaboration)
        
        if "flow" in item.name.lower():
            item.add_marker(pytest.mark.flow)
        
        if "performance" in item.name.lower():
            item.add_marker(pytest.mark.performance)


@pytest.fixture(scope="session", autouse=True)
def setup_integration_test_environment():
    """Set up the integration test environment."""
    print("\n" + "="*60)
    print("SETTING UP CREWAI INTEGRATION TEST ENVIRONMENT")
    print("="*60)
    
    # Mock external dependencies
    with patch.dict('os.environ', {
        'OPENAI_API_KEY': 'test_key',
        'CREWAI_LOG_LEVEL': 'ERROR',
        'TEST_MODE': 'true'
    }):
        yield
    
    print("\n" + "="*60)
    print("INTEGRATION TEST ENVIRONMENT CLEANUP COMPLETE")
    print("="*60)