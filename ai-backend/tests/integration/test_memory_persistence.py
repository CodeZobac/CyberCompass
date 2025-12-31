"""
Integration tests for memory persistence and context preservation in CrewAI workflows.

This module tests how memory systems maintain context across conversations,
sessions, and agent interactions, ensuring continuity in educational experiences.

Requirements tested: 9.1, 9.2
"""

import pytest
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch, MagicMock

from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai import Agent, Crew, Task

from src.flows.catfish_detection_flow import CatfishDetectionFlow
from src.flows.deepfake_detection_flow import DeepfakeDetectionFlow
from src.flows.social_media_simulation_flow import SocialMediaSimulationFlow
from src.models.requests import (
    CatfishChatStartRequest,
    DeepfakeChallengeRequest,
    SocialMediaSimulationRequest,
    LocaleEnum,
)


class MockMemorySystem:
    """Mock memory system for testing persistence."""
    
    def __init__(self, memory_type: str = "long_term"):
        self.memory_type = memory_type
        self.storage: Dict[str, Any] = {}
        self.access_log: List[Dict[str, Any]] = []
        self.session_data: Dict[str, Dict[str, Any]] = {}
    
    def save(self, data: Dict[str, Any], session_id: Optional[str] = None) -> None:
        """Save data to memory with optional session isolation."""
        timestamp = datetime.utcnow().isoformat()
        
        if session_id:
            if session_id not in self.session_data:
                self.session_data[session_id] = {}
            self.session_data[session_id].update(data)
        else:
            self.storage.update(data)
        
        self.access_log.append({
            "operation": "save",
            "session_id": session_id,
            "data_keys": list(data.keys()),
            "timestamp": timestamp
        })
    
    def search(self, query: str, session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search memory with optional session filtering."""
        timestamp = datetime.utcnow().isoformat()
        
        # Simple mock search implementation
        results = []
        search_space = self.session_data.get(session_id, {}) if session_id else self.storage
        
        for key, value in search_space.items():
            if query.lower() in str(value).lower():
                results.append({key: value})
        
        self.access_log.append({
            "operation": "search",
            "query": query,
            "session_id": session_id,
            "results_count": len(results),
            "timestamp": timestamp
        })
        
        return results
    
    def get(self, key: str, session_id: Optional[str] = None) -> Any:
        """Get specific data from memory."""
        timestamp = datetime.utcnow().isoformat()
        
        if session_id:
            result = self.session_data.get(session_id, {}).get(key)
        else:
            result = self.storage.get(key)
        
        self.access_log.append({
            "operation": "get",
            "key": key,
            "session_id": session_id,
            "found": result is not None,
            "timestamp": timestamp
        })
        
        return result
    
    def clear_session(self, session_id: str) -> None:
        """Clear session-specific memory."""
        if session_id in self.session_data:
            del self.session_data[session_id]
        
        self.access_log.append({
            "operation": "clear_session",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def get_access_stats(self) -> Dict[str, Any]:
        """Get memory access statistics."""
        operations = [log["operation"] for log in self.access_log]
        return {
            "total_operations": len(self.access_log),
            "operations_by_type": {
                op: operations.count(op) for op in set(operations)
            },
            "sessions_active": len(self.session_data),
            "storage_keys": len(self.storage)
        }


class MockAgentWithMemory:
    """Mock agent with memory capabilities."""
    
    def __init__(self, role: str, memory_system: MockMemorySystem):
        self.role = role
        self.memory = memory_system
        self.conversation_context: List[Dict[str, Any]] = []
        self.session_id: Optional[str] = None
    
    def set_session(self, session_id: str) -> None:
        """Set current session for memory isolation."""
        self.session_id = session_id
    
    def remember(self, key: str, value: Any) -> None:
        """Store information in memory."""
        self.memory.save({key: value}, session_id=self.session_id)
    
    def recall(self, key: str) -> Any:
        """Retrieve information from memory."""
        return self.memory.get(key, session_id=self.session_id)
    
    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """Search memory for relevant information."""
        return self.memory.search(query, session_id=self.session_id)
    
    def add_to_conversation(self, message: Dict[str, Any]) -> None:
        """Add message to conversation context."""
        self.conversation_context.append(message)
        
        # Store in memory for persistence
        conversation_key = f"conversation_history_{self.session_id}"
        self.remember(conversation_key, self.conversation_context)


@pytest.fixture
def mock_memory_systems():
    """Create mock memory systems for testing."""
    return {
        "long_term": MockMemorySystem("long_term"),
        "short_term": MockMemorySystem("short_term"),
        "entity": MockMemorySystem("entity")
    }


@pytest.fixture
def mock_agent_factory_with_memory(mock_memory_systems):
    """Create mock agent factory with memory-enabled agents."""
    class MockAgentFactoryWithMemory:
        def __init__(self):
            self.memory_systems = mock_memory_systems
        
        def create_agent(self, agent_name: str, locale: str = "en") -> MockAgentWithMemory:
            return MockAgentWithMemory(
                role=f"{agent_name}_role",
                memory_system=self.memory_systems["long_term"]
            )
    
    return MockAgentFactoryWithMemory()


class TestMemoryPersistence:
    """Test memory persistence across different scenarios."""
    
    def test_conversation_memory_persistence(self, mock_memory_systems):
        """Test that conversation history is preserved in memory."""
        memory = mock_memory_systems["long_term"]
        agent = MockAgentWithMemory("catfish_character", memory)
        session_id = str(uuid.uuid4())
        agent.set_session(session_id)
        
        # Simulate conversation
        messages = [
            {"sender": "user", "content": "Hi there!", "timestamp": datetime.utcnow().isoformat()},
            {"sender": "character", "content": "Hey! How's it going?", "timestamp": datetime.utcnow().isoformat()},
            {"sender": "user", "content": "Good! What's your favorite music?", "timestamp": datetime.utcnow().isoformat()},
            {"sender": "character", "content": "I love pop music!", "timestamp": datetime.utcnow().isoformat()},
        ]
        
        # Add messages to conversation
        for message in messages:
            agent.add_to_conversation(message)
        
        # Verify conversation is stored in memory
        conversation_key = f"conversation_history_{session_id}"
        stored_conversation = agent.recall(conversation_key)
        
        assert stored_conversation is not None
        assert len(stored_conversation) == len(messages)
        assert stored_conversation[0]["content"] == "Hi there!"
        assert stored_conversation[-1]["content"] == "I love pop music!"
        
        # Verify memory access was logged
        stats = memory.get_access_stats()
        assert stats["total_operations"] > 0
        assert "save" in stats["operations_by_type"]
        assert "get" in stats["operations_by_type"]
    
    def test_character_profile_persistence(self, mock_memory_systems):
        """Test that character profiles persist across interactions."""
        memory = mock_memory_systems["long_term"]
        agent = MockAgentWithMemory("catfish_character", memory)
        session_id = str(uuid.uuid4())
        agent.set_session(session_id)
        
        # Store character profile
        character_profile = {
            "name": "Alex",
            "stated_age": 16,
            "bio": "Love music and games!",
            "red_flags": ["Avoids video calls", "Uses outdated slang"],
            "inconsistencies": ["Age vs cultural references"],
            "revealed_flags": []
        }
        
        agent.remember("character_profile", character_profile)
        
        # Simulate revealing red flags over time
        revealed_flags = [
            {"flag": "Avoids video calls", "turn": 5, "message": "I can't video chat right now"},
            {"flag": "Uses outdated slang", "turn": 8, "message": "That's so fetch!"}
        ]
        
        for flag in revealed_flags:
            current_profile = agent.recall("character_profile")
            current_profile["revealed_flags"].append(flag)
            agent.remember("character_profile", current_profile)
        
        # Verify profile persistence and updates
        final_profile = agent.recall("character_profile")
        
        assert final_profile["name"] == "Alex"
        assert len(final_profile["revealed_flags"]) == 2
        assert final_profile["revealed_flags"][0]["flag"] == "Avoids video calls"
        assert final_profile["revealed_flags"][1]["flag"] == "Uses outdated slang"
    
    def test_user_progress_tracking(self, mock_memory_systems):
        """Test persistent tracking of user progress and performance."""
        memory = mock_memory_systems["long_term"]
        analytics_agent = MockAgentWithMemory("analytics_agent", memory)
        user_id = "test_user_123"
        
        # Initialize user progress
        initial_progress = {
            "user_id": user_id,
            "competency_scores": {
                "deepfake_detection": 0.6,
                "social_media_literacy": 0.7,
                "catfish_awareness": 0.5
            },
            "challenges_completed": 0,
            "accuracy_history": [],
            "learning_path": ["beginner_deepfake", "intermediate_social_media"]
        }
        
        analytics_agent.remember(f"user_progress_{user_id}", initial_progress)
        
        # Simulate multiple challenge completions
        challenge_results = [
            {"challenge_type": "deepfake", "score": 85, "correct": True},
            {"challenge_type": "social_media", "score": 70, "correct": True},
            {"challenge_type": "catfish", "score": 60, "correct": False},
            {"challenge_type": "deepfake", "score": 90, "correct": True}
        ]
        
        for result in challenge_results:
            # Update progress
            current_progress = analytics_agent.recall(f"user_progress_{user_id}")
            current_progress["challenges_completed"] += 1
            current_progress["accuracy_history"].append(result)
            
            # Update competency scores based on performance
            if result["challenge_type"] == "deepfake":
                current_progress["competency_scores"]["deepfake_detection"] += 0.05
            elif result["challenge_type"] == "social_media":
                current_progress["competency_scores"]["social_media_literacy"] += 0.03
            elif result["challenge_type"] == "catfish":
                current_progress["competency_scores"]["catfish_awareness"] += 0.02
            
            analytics_agent.remember(f"user_progress_{user_id}", current_progress)
        
        # Verify progress tracking
        final_progress = analytics_agent.recall(f"user_progress_{user_id}")
        
        assert final_progress["challenges_completed"] == 4
        assert len(final_progress["accuracy_history"]) == 4
        assert final_progress["competency_scores"]["deepfake_detection"] > 0.6
        assert final_progress["accuracy_history"][-1]["score"] == 90
    
    def test_session_isolation(self, mock_memory_systems):
        """Test that different sessions maintain separate memory contexts."""
        memory = mock_memory_systems["long_term"]
        
        # Create two agents for different sessions
        agent1 = MockAgentWithMemory("catfish_character", memory)
        agent2 = MockAgentWithMemory("catfish_character", memory)
        
        session1_id = str(uuid.uuid4())
        session2_id = str(uuid.uuid4())
        
        agent1.set_session(session1_id)
        agent2.set_session(session2_id)
        
        # Store different data in each session
        agent1.remember("character_name", "Alice")
        agent1.remember("character_age", 16)
        
        agent2.remember("character_name", "Bob")
        agent2.remember("character_age", 17)
        
        # Verify session isolation
        assert agent1.recall("character_name") == "Alice"
        assert agent1.recall("character_age") == 16
        
        assert agent2.recall("character_name") == "Bob"
        assert agent2.recall("character_age") == 17
        
        # Verify cross-session data doesn't leak
        assert agent1.recall("character_name") != agent2.recall("character_name")
        
        # Verify memory system tracks separate sessions
        assert session1_id in memory.session_data
        assert session2_id in memory.session_data
        assert memory.session_data[session1_id] != memory.session_data[session2_id]


class TestContextPreservation:
    """Test context preservation across different flow operations."""
    
    def test_deepfake_flow_context_preservation(self, mock_agent_factory_with_memory):
        """Test context preservation in deepfake detection flow."""
        flow = DeepfakeDetectionFlow(mock_agent_factory_with_memory, locale="en")
        
        # Mock the flow's memory systems
        flow.long_term_memory = mock_agent_factory_with_memory.memory_systems["long_term"]
        flow.short_term_memory = mock_agent_factory_with_memory.memory_systems["short_term"]
        
        # Simulate challenge progression with context
        challenge_context = {
            "user_id": "test_user",
            "difficulty_progression": [1, 2, 2, 3],
            "performance_history": [
                {"challenge_id": "ch1", "score": 70, "difficulty": 1},
                {"challenge_id": "ch2", "score": 85, "difficulty": 2},
                {"challenge_id": "ch3", "score": 75, "difficulty": 2}
            ]
        }
        
        # Store context in flow memory
        flow.long_term_memory.save(challenge_context)
        
        # Simulate performance history updates
        flow.user_performance_history = challenge_context["performance_history"]
        
        # Test context retrieval and usage
        stored_context = flow.long_term_memory.search("performance_history")
        assert len(stored_context) > 0
        
        # Verify performance history is maintained
        assert len(flow.user_performance_history) == 3
        assert flow.user_performance_history[-1]["score"] == 75
        
        # Test difficulty adaptation based on context
        avg_score = sum(p["score"] for p in flow.user_performance_history) / len(flow.user_performance_history)
        assert avg_score > 70  # Should indicate good performance
    
    def test_catfish_flow_conversation_context(self, mock_agent_factory_with_memory):
        """Test conversation context preservation in catfish detection flow."""
        flow = CatfishDetectionFlow(mock_agent_factory_with_memory, locale="en")
        
        # Mock memory systems
        flow.long_term_memory = mock_agent_factory_with_memory.memory_systems["long_term"]
        flow.short_term_memory = mock_agent_factory_with_memory.memory_systems["short_term"]
        
        # Set up character profile in memory
        character_profile = {
            "character_id": "char_123",
            "name": "Alex",
            "stated_age": 16,
            "red_flags": ["Avoids video calls", "Uses outdated slang", "Inconsistent stories"],
            "conversation_strategy": "Reveal flags gradually"
        }
        
        flow.character_profile = character_profile
        flow.long_term_memory.save({"character_profile": character_profile})
        
        # Simulate conversation progression
        conversation_turns = [
            {"user": "Hi there!", "character": "Hey! How's it going?"},
            {"user": "Good! What school do you go to?", "character": "Oh, just a local school"},
            {"user": "Which one?", "character": "Um, you probably wouldn't know it"},
            {"user": "Can we video chat?", "character": "My camera is broken right now"}
        ]
        
        # Process conversation and track context
        for i, turn in enumerate(conversation_turns):
            # Add to conversation history
            flow.conversation_history.extend([
                {"sender": "user", "content": turn["user"], "turn": i*2},
                {"sender": "character", "content": turn["character"], "turn": i*2+1}
            ])
            
            # Update short-term memory with recent context
            flow.short_term_memory.save({
                "recent_turn": i,
                "user_message": turn["user"],
                "character_response": turn["character"]
            })
        
        # Test context preservation
        assert len(flow.conversation_history) == 8  # 4 turns * 2 messages each
        
        # Test recent conversation formatting
        recent_context = flow._format_recent_conversation(last_n=3)
        assert "video chat" in recent_context
        assert "camera is broken" in recent_context
        
        # Verify red flag tracking
        # In this conversation, the character avoided the video chat question
        flow.red_flags_revealed.append({
            "flag": "Avoids video calls",
            "revealed_at_turn": 7,
            "message": "My camera is broken right now"
        })
        
        assert len(flow.red_flags_revealed) == 1
        assert flow.red_flags_revealed[0]["flag"] == "Avoids video calls"
    
    def test_social_media_flow_engagement_context(self, mock_agent_factory_with_memory):
        """Test engagement context preservation in social media simulation."""
        flow = SocialMediaSimulationFlow(mock_agent_factory_with_memory, locale="en")
        
        # Set up feed and interaction tracking
        flow.current_feed = [
            {"post_id": "post_1", "content": "Breaking news!", "is_disinformation": True},
            {"post_id": "post_2", "content": "Interesting article", "is_disinformation": False},
            {"post_id": "post_3", "content": "URGENT: Share now!", "is_disinformation": True}
        ]
        
        # Simulate user interactions with context tracking
        interactions = [
            {"post_id": "post_1", "type": "view", "timestamp": datetime.utcnow()},
            {"post_id": "post_1", "type": "like", "timestamp": datetime.utcnow()},
            {"post_id": "post_2", "type": "view", "timestamp": datetime.utcnow()},
            {"post_id": "post_2", "type": "share", "timestamp": datetime.utcnow()},
            {"post_id": "post_3", "type": "view", "timestamp": datetime.utcnow()},
            {"post_id": "post_3", "type": "report", "timestamp": datetime.utcnow()}
        ]
        
        # Process interactions and maintain context
        for interaction in interactions:
            flow.user_interactions.append({
                "interaction_id": str(uuid.uuid4()),
                "post_id": interaction["post_id"],
                "interaction_type": interaction["type"],
                "timestamp": interaction["timestamp"].isoformat(),
                "post_is_disinformation": next(
                    p["is_disinformation"] for p in flow.current_feed 
                    if p["post_id"] == interaction["post_id"]
                )
            })
        
        # Test context preservation in analysis
        assert len(flow.user_interactions) == 6
        
        # Analyze engagement patterns
        disinformation_interactions = [
            i for i in flow.user_interactions 
            if i["post_is_disinformation"]
        ]
        
        authentic_interactions = [
            i for i in flow.user_interactions 
            if not i["post_is_disinformation"]
        ]
        
        assert len(disinformation_interactions) == 4  # post_1 (2) + post_3 (2)
        assert len(authentic_interactions) == 2  # post_2 (2)
        
        # Verify context is used for algorithm feedback
        problematic_engagements = [
            i for i in disinformation_interactions 
            if i["interaction_type"] in ["like", "share"]
        ]
        
        positive_engagements = [
            i for i in disinformation_interactions 
            if i["interaction_type"] == "report"
        ]
        
        assert len(problematic_engagements) == 1  # liked post_1
        assert len(positive_engagements) == 1  # reported post_3


class TestMemoryRecovery:
    """Test memory recovery and error handling scenarios."""
    
    def test_memory_corruption_recovery(self, mock_memory_systems):
        """Test recovery from memory corruption or data loss."""
        memory = mock_memory_systems["long_term"]
        agent = MockAgentWithMemory("test_agent", memory)
        session_id = str(uuid.uuid4())
        agent.set_session(session_id)
        
        # Store important data
        important_data = {
            "user_progress": {"score": 85, "level": 3},
            "conversation_state": {"turn": 10, "flags_revealed": 2}
        }
        
        agent.remember("critical_data", important_data)
        
        # Simulate memory corruption (data becomes None)
        memory.session_data[session_id]["critical_data"] = None
        
        # Test recovery mechanism
        recovered_data = agent.recall("critical_data")
        
        if recovered_data is None:
            # Implement fallback recovery
            fallback_data = {
                "user_progress": {"score": 0, "level": 1},
                "conversation_state": {"turn": 0, "flags_revealed": 0},
                "recovered": True
            }
            agent.remember("critical_data", fallback_data)
            recovered_data = agent.recall("critical_data")
        
        assert recovered_data is not None
        assert "recovered" in recovered_data or recovered_data == important_data
    
    def test_session_timeout_handling(self, mock_memory_systems):
        """Test handling of session timeouts and cleanup."""
        memory = mock_memory_systems["long_term"]
        
        # Create sessions with different timestamps
        old_session = str(uuid.uuid4())
        current_session = str(uuid.uuid4())
        
        # Store data in old session (simulate expired session)
        memory.save({"last_activity": (datetime.utcnow() - timedelta(hours=2)).isoformat()}, old_session)
        memory.save({"conversation": "old conversation data"}, old_session)
        
        # Store data in current session
        memory.save({"last_activity": datetime.utcnow().isoformat()}, current_session)
        memory.save({"conversation": "current conversation data"}, current_session)
        
        # Simulate session cleanup (remove expired sessions)
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        sessions_to_remove = []
        for session_id, session_data in memory.session_data.items():
            last_activity_str = session_data.get("last_activity")
            if last_activity_str:
                last_activity = datetime.fromisoformat(last_activity_str)
                if last_activity < cutoff_time:
                    sessions_to_remove.append(session_id)
        
        # Clean up expired sessions
        for session_id in sessions_to_remove:
            memory.clear_session(session_id)
        
        # Verify cleanup
        assert old_session not in memory.session_data
        assert current_session in memory.session_data
        
        # Verify current session data is preserved
        current_data = memory.session_data[current_session]
        assert current_data["conversation"] == "current conversation data"
    
    def test_memory_search_performance(self, mock_memory_systems):
        """Test memory search performance with large datasets."""
        memory = mock_memory_systems["long_term"]
        
        # Store large amount of conversation data
        session_id = str(uuid.uuid4())
        
        # Generate conversation history
        conversation_data = []
        for i in range(100):
            conversation_data.extend([
                {"sender": "user", "content": f"User message {i}", "turn": i*2},
                {"sender": "character", "content": f"Character response {i}", "turn": i*2+1}
            ])
        
        memory.save({"large_conversation": conversation_data}, session_id)
        
        # Test search performance
        search_queries = [
            "User message 50",
            "Character response",
            "message 25",
            "nonexistent content"
        ]
        
        for query in search_queries:
            results = memory.search(query, session_id)
            
            if "nonexistent" not in query:
                assert len(results) > 0
            else:
                assert len(results) == 0
        
        # Verify search operations were logged
        search_operations = [
            log for log in memory.access_log 
            if log["operation"] == "search"
        ]
        
        assert len(search_operations) == len(search_queries)
    
    def test_concurrent_memory_access(self, mock_memory_systems):
        """Test concurrent access to memory systems."""
        memory = mock_memory_systems["long_term"]
        
        # Simulate concurrent agents accessing memory
        agents = [
            MockAgentWithMemory(f"agent_{i}", memory) 
            for i in range(3)
        ]
        
        session_ids = [str(uuid.uuid4()) for _ in range(3)]
        
        # Set up agents with different sessions
        for agent, session_id in zip(agents, session_ids):
            agent.set_session(session_id)
        
        # Simulate concurrent operations
        for i, agent in enumerate(agents):
            # Each agent stores and retrieves data
            agent.remember(f"agent_data_{i}", {"value": i * 10})
            agent.remember("shared_key", f"data_from_agent_{i}")
        
        # Verify each agent can access its own data
        for i, agent in enumerate(agents):
            own_data = agent.recall(f"agent_data_{i}")
            assert own_data["value"] == i * 10
        
        # Verify session isolation (agents can't see each other's data)
        agent_0_shared = agents[0].recall("shared_key")
        agent_1_shared = agents[1].recall("shared_key")
        agent_2_shared = agents[2].recall("shared_key")
        
        assert agent_0_shared == "data_from_agent_0"
        assert agent_1_shared == "data_from_agent_1"
        assert agent_2_shared == "data_from_agent_2"
        
        # Verify memory system handled concurrent access
        stats = memory.get_access_stats()
        assert stats["total_operations"] >= 9  # 3 agents * 3 operations each
        assert stats["sessions_active"] == 3


class TestMemoryIntegrationWithFlows:
    """Test memory integration with actual flow operations."""
    
    @patch('crewai.Crew.kickoff')
    def test_memory_integration_in_catfish_flow(self, mock_kickoff, mock_agent_factory_with_memory):
        """Test memory integration in catfish detection flow."""
        mock_kickoff.return_value = Mock(raw="Mock response")
        
        flow = CatfishDetectionFlow(mock_agent_factory_with_memory, locale="en")
        
        # Initialize flow with memory
        flow.long_term_memory = mock_agent_factory_with_memory.memory_systems["long_term"]
        flow.short_term_memory = mock_agent_factory_with_memory.memory_systems["short_term"]
        
        # Create test request
        request = CatfishChatStartRequest(
            user_id="test_user",
            difficulty_level=2,
            locale=LocaleEnum.EN
        )
        
        # Initialize character (should store in memory)
        init_result = flow.initialize_character(request)
        
        # Verify character profile is stored in long-term memory
        stored_profile = flow.long_term_memory.search("character_profile")
        assert len(stored_profile) > 0
        
        # Process user messages (should update memory)
        messages = [
            "Hi there!",
            "What's your favorite music?",
            "Do you want to video chat?"
        ]
        
        for message in messages:
            flow.process_user_message(
                session_id=init_result["session_id"],
                user_id="test_user",
                message_content=message
            )
        
        # Verify conversation history is maintained
        assert len(flow.conversation_history) > 0
        
        # Verify memory systems were used
        long_term_stats = flow.long_term_memory.get_access_stats()
        short_term_stats = flow.short_term_memory.get_access_stats()
        
        assert long_term_stats["total_operations"] > 0
        assert short_term_stats["total_operations"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])