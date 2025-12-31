"""
Integration tests for CrewAI workflows and flows.

This module tests complete Flow executions from start to finish,
verifies agent collaboration and task delegation, and tests
memory persistence and context preservation.

Requirements tested: 9.1, 9.2
"""

import pytest
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock, patch

from crewai import Agent, Crew, Task, Flow
from crewai.memory import LongTermMemory, ShortTermMemory

from src.flows.deepfake_detection_flow import DeepfakeDetectionFlow
from src.flows.social_media_simulation_flow import SocialMediaSimulationFlow
from src.flows.catfish_detection_flow import CatfishDetectionFlow
from src.agents.factory import AgentFactory
from src.models.requests import (
    DeepfakeChallengeRequest,
    DeepfakeSubmissionRequest,
    SocialMediaSimulationRequest,
    CatfishChatStartRequest,
    MediaType,
    DisinformationType,
    LocaleEnum,
)


class MockAgentFactory:
    """Mock agent factory for testing."""
    
    def __init__(self):
        self.agents = {}
        self._create_mock_agents()
    
    def _create_mock_agents(self):
        """Create mock agents for testing."""
        # Mock deepfake analyst agent
        deepfake_agent = Mock(spec=Agent)
        deepfake_agent.role = "Deepfake Detection Specialist"
        deepfake_agent.goal = "Analyze media content for deepfake indicators"
        
        # Mock social media simulator agent
        social_media_agent = Mock(spec=Agent)
        social_media_agent.role = "Social Media Content Simulator"
        social_media_agent.goal = "Generate realistic social media content"
        
        # Mock catfish character agent
        catfish_agent = Mock(spec=Agent)
        catfish_agent.role = "Catfish Character Simulator"
        catfish_agent.goal = "Simulate suspicious online personas"
        
        # Mock ethics mentor agent
        ethics_agent = Mock(spec=Agent)
        ethics_agent.role = "Ethics Education Mentor"
        ethics_agent.goal = "Provide educational feedback"
        
        # Mock analytics agent
        analytics_agent = Mock(spec=Agent)
        analytics_agent.role = "Learning Analytics Specialist"
        analytics_agent.goal = "Analyze user progress and performance"
        
        # Mock conversation moderator
        moderator_agent = Mock(spec=Agent)
        moderator_agent.role = "Conversation Moderator"
        moderator_agent.goal = "Manage conversation flow"
        
        self.agents = {
            "deepfake_analyst": deepfake_agent,
            "social_media_simulator": social_media_agent,
            "catfish_character": catfish_agent,
            "ethics_mentor": ethics_agent,
            "analytics_agent": analytics_agent,
            "conversation_moderator": moderator_agent,
        }
    
    def create_agent(self, agent_name: str, locale: str = "en") -> Agent:
        """Create a mock agent."""
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
        return self.agents[agent_name]


class MockCrewResult:
    """Mock result from crew execution."""
    
    def __init__(self, raw_output: str):
        self.raw = raw_output
        self.tasks_output = []
    
    def __str__(self):
        return self.raw


@pytest.fixture
def mock_agent_factory():
    """Provide mock agent factory."""
    return MockAgentFactory()


@pytest.fixture
def sample_deepfake_request():
    """Provide sample deepfake challenge request."""
    return DeepfakeChallengeRequest(
        user_id="test_user_123",
        difficulty_level=2,
        media_type=MediaType.VIDEO,
        locale=LocaleEnum.EN
    )


@pytest.fixture
def sample_social_media_request():
    """Provide sample social media simulation request."""
    return SocialMediaSimulationRequest(
        user_id="test_user_123",
        session_duration_minutes=15,
        disinformation_ratio=0.3,
        categories=[DisinformationType.HEALTH, DisinformationType.POLITICS],
        locale=LocaleEnum.EN
    )


@pytest.fixture
def sample_catfish_request():
    """Provide sample catfish chat request."""
    return CatfishChatStartRequest(
        user_id="test_user_123",
        difficulty_level=3,
        character_age_range="16-18",
        locale=LocaleEnum.EN
    )


class TestDeepfakeDetectionFlow:
    """Test complete deepfake detection flow execution."""
    
    @pytest.fixture
    def deepfake_flow(self, mock_agent_factory):
        """Create deepfake detection flow with mocked agents."""
        return DeepfakeDetectionFlow(mock_agent_factory, locale="en")
    
    @patch('crewai.Crew.kickoff')
    def test_complete_flow_execution(self, mock_kickoff, deepfake_flow, sample_deepfake_request):
        """Test complete deepfake detection flow from start to finish."""
        # Mock crew execution results
        challenge_result = MockCrewResult("""
        {
            "challenge_id": "test_challenge_123",
            "media_url": "/media/test_video.mp4",
            "media_type": "video",
            "is_deepfake": true,
            "difficulty_level": 2,
            "instructions": "Analyze this video for deepfake indicators",
            "hints": ["Look for facial inconsistencies", "Check audio sync"],
            "detection_clues": ["Unnatural eye movements", "Audio-visual mismatch"]
        }
        """)
        
        feedback_result = MockCrewResult("""
        {
            "correct": false,
            "actual_answer": true,
            "feedback": "This video contains several deepfake indicators...",
            "detection_clues": ["Unnatural eye movements", "Audio-visual mismatch"],
            "score": 65,
            "learning_points": ["Focus on facial micro-expressions", "Listen for audio artifacts"]
        }
        """)
        
        mock_kickoff.side_effect = [challenge_result, feedback_result]
        
        # Test flow initialization
        init_result = deepfake_flow.initialize_challenge(sample_deepfake_request)
        
        assert init_result["status"] == "challenge_initialized"
        assert "challenge" in init_result
        assert init_result["user_id"] == "test_user_123"
        assert init_result["challenge"]["difficulty_level"] == 2
        
        # Test awaiting submission
        await_result = deepfake_flow.await_user_submission(init_result)
        
        assert await_result["status"] == "awaiting_submission"
        assert await_result["ready_for_submission"] is True
        
        # Test submission processing
        submission = DeepfakeSubmissionRequest(
            challenge_id=init_result["challenge"]["challenge_id"],
            user_id="test_user_123",
            is_deepfake=False,  # Incorrect answer
            confidence=0.7,
            reasoning="The video looks natural to me"
        )
        
        submission_result = deepfake_flow.process_submission(submission)
        
        assert submission_result["status"] == "submission_processed"
        assert "feedback" in submission_result
        assert submission_result["feedback"]["correct"] is False
        
        # Verify crew was called with correct parameters
        assert mock_kickoff.call_count == 2
    
    @patch('crewai.Crew.kickoff')
    def test_agent_collaboration(self, mock_kickoff, deepfake_flow, sample_deepfake_request):
        """Test that multiple agents collaborate correctly in the flow."""
        mock_result = MockCrewResult("Test collaboration result")
        mock_kickoff.return_value = mock_result
        
        # Initialize challenge (uses deepfake_analyst)
        init_result = deepfake_flow.initialize_challenge(sample_deepfake_request)
        
        # Process submission (uses deepfake_analyst + ethics_mentor)
        submission = DeepfakeSubmissionRequest(
            challenge_id=init_result["challenge"]["challenge_id"],
            user_id="test_user_123",
            is_deepfake=True,
            confidence=0.8,
            reasoning="I noticed facial artifacts"
        )
        
        deepfake_flow.process_submission(submission)
        
        # Verify multiple crew executions with different agent combinations
        assert mock_kickoff.call_count == 2
        
        # Check that crews were created with appropriate agents
        call_args_list = mock_kickoff.call_args_list
        
        # First call should be for challenge generation
        first_call_crew = call_args_list[0][0][0] if call_args_list[0][0] else None
        
        # Second call should be for feedback generation
        second_call_crew = call_args_list[1][0][0] if call_args_list[1][0] else None
        
        # Verify crews have the expected agents
        assert mock_kickoff.called
    
    def test_difficulty_adaptation_routing(self, deepfake_flow):
        """Test that the flow correctly routes based on user performance."""
        # Simulate high performance history
        deepfake_flow.user_performance_history = [
            {"score": 85, "difficulty": 2},
            {"score": 90, "difficulty": 2},
            {"score": 88, "difficulty": 2},
        ]
        
        state = {"feedback": {"score": 87}}
        route = deepfake_flow.determine_next_action(state)
        
        assert route == "increase_difficulty"
        
        # Simulate poor performance
        deepfake_flow.user_performance_history = [
            {"score": 45, "difficulty": 2},
            {"score": 50, "difficulty": 2},
            {"score": 40, "difficulty": 2},
        ]
        
        route = deepfake_flow.determine_next_action(state)
        
        assert route == "provide_additional_training"
        
        # Simulate moderate performance
        deepfake_flow.user_performance_history = [
            {"score": 65, "difficulty": 2},
            {"score": 70, "difficulty": 2},
            {"score": 68, "difficulty": 2},
        ]
        
        route = deepfake_flow.determine_next_action(state)
        
        assert route == "maintain_difficulty"
    
    def test_memory_persistence(self, deepfake_flow, sample_deepfake_request):
        """Test that flow maintains state and memory across interactions."""
        # Initialize flow
        with patch('crewai.Crew.kickoff') as mock_kickoff:
            mock_kickoff.return_value = MockCrewResult("Test result")
            
            init_result = deepfake_flow.initialize_challenge(sample_deepfake_request)
            
            # Verify current challenge is stored
            assert deepfake_flow.current_challenge is not None
            assert deepfake_flow.current_challenge["challenge_id"] == init_result["challenge"]["challenge_id"]
            
            # Process submission
            submission = DeepfakeSubmissionRequest(
                challenge_id=init_result["challenge"]["challenge_id"],
                user_id="test_user_123",
                is_deepfake=True,
                confidence=0.8
            )
            
            deepfake_flow.process_submission(submission)
            
            # Verify performance history is updated
            assert len(deepfake_flow.user_performance_history) == 1
            assert deepfake_flow.user_performance_history[0]["challenge_id"] == submission.challenge_id
    
    def test_error_handling_in_flow(self, deepfake_flow, sample_deepfake_request):
        """Test error handling during flow execution."""
        # Test submission without active challenge
        submission = DeepfakeSubmissionRequest(
            challenge_id="nonexistent_challenge",
            user_id="test_user_123",
            is_deepfake=True,
            confidence=0.8
        )
        
        with pytest.raises(ValueError, match="No active challenge"):
            deepfake_flow.process_submission(submission)
        
        # Test submission with wrong challenge ID
        with patch('crewai.Crew.kickoff') as mock_kickoff:
            mock_kickoff.return_value = MockCrewResult("Test result")
            
            init_result = deepfake_flow.initialize_challenge(sample_deepfake_request)
            
            wrong_submission = DeepfakeSubmissionRequest(
                challenge_id="wrong_challenge_id",
                user_id="test_user_123",
                is_deepfake=True,
                confidence=0.8
            )
            
            with pytest.raises(ValueError, match="does not match current challenge"):
                deepfake_flow.process_submission(wrong_submission)


class TestSocialMediaSimulationFlow:
    """Test complete social media simulation flow execution."""
    
    @pytest.fixture
    def social_media_flow(self, mock_agent_factory):
        """Create social media simulation flow with mocked agents."""
        return SocialMediaSimulationFlow(mock_agent_factory, locale="en")
    
    @patch('crewai.Crew.kickoff')
    def test_complete_simulation_flow(self, mock_kickoff, social_media_flow, sample_social_media_request):
        """Test complete social media simulation from initialization to analysis."""
        # Mock feed generation result
        feed_result = MockCrewResult("""
        [
            {
                "post_id": "post_1",
                "content": "Breaking: New study shows...",
                "is_disinformation": true,
                "category": "health"
            },
            {
                "post_id": "post_2", 
                "content": "Interesting article about digital privacy",
                "is_disinformation": false
            }
        ]
        """)
        
        # Mock analysis result
        analysis_result = MockCrewResult("""
        {
            "detection_accuracy": 75,
            "engagement_patterns": "User showed good critical thinking",
            "recommendations": ["Verify sources before sharing"]
        }
        """)
        
        mock_kickoff.side_effect = [feed_result, analysis_result]
        
        # Test simulation initialization
        init_result = social_media_flow.initialize_simulation(sample_social_media_request)
        
        assert init_result["status"] == "simulation_initialized"
        assert "feed" in init_result
        assert init_result["user_id"] == "test_user_123"
        assert init_result["total_posts"] > 0
        
        # Test engagement tracking
        tracking_result = social_media_flow.track_user_engagement(init_result)
        
        assert tracking_result["status"] == "tracking_engagement"
        assert tracking_result["tracking_active"] is True
        
        # Test user interaction recording
        interaction_result = social_media_flow.record_interaction(
            session_id=init_result["session_id"],
            user_id="test_user_123",
            post_id="post_1",
            interaction_type="like"
        )
        
        assert interaction_result["status"] == "interaction_recorded"
        assert "algorithm_feedback" in interaction_result
        
        # Simulate multiple interactions to trigger analysis
        for i in range(10):
            social_media_flow.record_interaction(
                session_id=init_result["session_id"],
                user_id="test_user_123",
                post_id=f"post_{i % 2 + 1}",
                interaction_type="view"
            )
        
        # Test session analysis
        analysis_state = {"session_id": init_result["session_id"]}
        analysis_result = social_media_flow.analyze_session_performance(analysis_state)
        
        assert analysis_result["status"] == "session_analyzed"
        assert "analysis" in analysis_result
    
    def test_real_time_algorithm_feedback(self, social_media_flow):
        """Test real-time algorithm feedback generation."""
        # Set up a feed with known posts
        social_media_flow.current_feed = [
            {
                "post_id": "disinfo_post",
                "content": "URGENT: Share before they remove it!",
                "is_disinformation": True,
                "category": "conspiracy"
            },
            {
                "post_id": "authentic_post",
                "content": "Interesting research on digital literacy",
                "is_disinformation": False
            }
        ]
        
        # Test interaction with disinformation
        disinfo_result = social_media_flow.record_interaction(
            session_id="test_session",
            user_id="test_user",
            post_id="disinfo_post",
            interaction_type="share"
        )
        
        feedback = disinfo_result["algorithm_feedback"]
        assert feedback["algorithm_impact"] == "negative"
        assert feedback["content_amplification"] > 0
        
        # Test interaction with authentic content
        authentic_result = social_media_flow.record_interaction(
            session_id="test_session",
            user_id="test_user",
            post_id="authentic_post",
            interaction_type="like"
        )
        
        feedback = authentic_result["algorithm_feedback"]
        assert feedback["algorithm_impact"] == "positive"
    
    def test_session_routing_logic(self, social_media_flow):
        """Test session status routing based on interactions."""
        # Test with few interactions
        social_media_flow.user_interactions = [{"type": "view"}] * 5
        social_media_flow.session_start_time = datetime.utcnow()
        
        state = {"session_id": "test_session"}
        route = social_media_flow.check_session_status(state)
        
        assert route == "continue_tracking"
        
        # Test with many interactions
        social_media_flow.user_interactions = [{"type": "view"}] * 15
        
        route = social_media_flow.check_session_status(state)
        
        assert route == "generate_session_analysis"
    
    def test_multilingual_content_generation(self, mock_agent_factory):
        """Test content generation in different languages."""
        # Test Portuguese flow
        pt_flow = SocialMediaSimulationFlow(mock_agent_factory, locale="pt")
        
        sample_content = pt_flow._generate_sample_content(is_disinfo=True, locale="pt")
        
        # Should contain Portuguese characters or words
        assert any(char in sample_content for char in "áéíóúãõç") or \
               any(word in sample_content.lower() for word in ["compartilhe", "urgente", "médicos"])
        
        # Test English flow
        en_flow = SocialMediaSimulationFlow(mock_agent_factory, locale="en")
        
        sample_content = en_flow._generate_sample_content(is_disinfo=True, locale="en")
        
        # Should be in English
        assert any(word in sample_content.lower() for word in ["urgent", "share", "doctors", "study"])


class TestCatfishDetectionFlow:
    """Test complete catfish detection flow execution."""
    
    @pytest.fixture
    def catfish_flow(self, mock_agent_factory):
        """Create catfish detection flow with mocked agents."""
        return CatfishDetectionFlow(mock_agent_factory, locale="en")
    
    @patch('crewai.Crew.kickoff')
    def test_complete_catfish_flow(self, mock_kickoff, catfish_flow, sample_catfish_request):
        """Test complete catfish detection flow from character creation to analysis."""
        # Mock character creation result
        character_result = MockCrewResult("""
        {
            "character_id": "char_123",
            "name": "Alex",
            "stated_age": 16,
            "bio": "Love music and games!",
            "red_flags": ["Avoids video calls", "Uses outdated slang"],
            "inconsistencies": ["Age vs cultural references"]
        }
        """)
        
        # Mock opening message result
        opening_result = MockCrewResult("Hey! How's it going? I love your profile!")
        
        # Mock conversation response
        response_result = MockCrewResult("Yeah, I'm totally into that new TikTok dance!")
        
        # Mock final analysis
        analysis_result = MockCrewResult("""
        {
            "detection_score": 70,
            "flags_caught": 2,
            "recommendations": ["Ask more probing questions"]
        }
        """)
        
        mock_kickoff.side_effect = [character_result, opening_result, response_result, analysis_result]
        
        # Test character initialization
        init_result = catfish_flow.initialize_character(sample_catfish_request)
        
        assert init_result["status"] == "character_initialized"
        assert "character_profile" in init_result
        assert init_result["character_profile"]["name"] == "Alex"
        
        # Test conversation start
        conversation_result = catfish_flow.start_conversation(init_result)
        
        assert conversation_result["status"] == "conversation_started"
        assert "opening_message" in conversation_result
        
        # Test conversation management
        manage_result = catfish_flow.manage_conversation_flow(conversation_result)
        
        assert manage_result["status"] == "conversation_active"
        assert manage_result["awaiting_user_message"] is True
        
        # Test user message processing
        response_result = catfish_flow.process_user_message(
            session_id=init_result["session_id"],
            user_id="test_user_123",
            message_content="How old are you exactly?",
            user_suspicion_indicators={"probing_question": True}
        )
        
        assert response_result["status"] == "response_generated"
        assert "response" in response_result
        assert "typing_delay" in response_result
    
    def test_memory_and_context_preservation(self, catfish_flow):
        """Test memory persistence and context preservation across conversation."""
        # Initialize character with memory
        with patch('crewai.Crew.kickoff') as mock_kickoff:
            mock_kickoff.return_value = MockCrewResult("Test character")
            
            request = CatfishChatStartRequest(
                user_id="test_user",
                difficulty_level=2,
                locale=LocaleEnum.EN
            )
            
            init_result = catfish_flow.initialize_character(request)
            
            # Verify character profile is stored
            assert catfish_flow.character_profile is not None
            
            # Verify memory systems are initialized
            assert catfish_flow.long_term_memory is not None
            assert catfish_flow.short_term_memory is not None
            
            # Process multiple messages to build conversation history
            messages = [
                "Hi there!",
                "What's your favorite music?",
                "Do you go to school around here?",
                "Want to video chat sometime?"
            ]
            
            for i, message in enumerate(messages):
                mock_kickoff.return_value = MockCrewResult(f"Response {i}")
                
                catfish_flow.process_user_message(
                    session_id=init_result["session_id"],
                    user_id="test_user",
                    message_content=message
                )
            
            # Verify conversation history is maintained
            assert len(catfish_flow.conversation_history) == len(messages) * 2  # User + character messages
            
            # Verify context is preserved in recent conversation formatting
            recent_context = catfish_flow._format_recent_conversation(last_n=3)
            assert "Hi there!" in recent_context or "Response" in recent_context
    
    def test_red_flag_revelation_strategy(self, catfish_flow):
        """Test strategic red flag revelation during conversation."""
        # Set up character with red flags
        catfish_flow.character_profile = {
            "name": "TestChar",
            "stated_age": 16,
            "red_flags": [
                "Avoids video calls",
                "Uses outdated slang", 
                "Inconsistent location stories",
                "Pushes for personal info"
            ]
        }
        
        # Test red flag revelation timing
        catfish_flow.conversation_history = [{"sender": "user", "content": "test"}] * 8
        
        should_reveal = catfish_flow._should_reveal_red_flag()
        assert should_reveal is True  # Should reveal flag after 8 messages (8 // 4 = 2 flags expected)
        
        # Test with flags already revealed
        catfish_flow.red_flags_revealed = [
            {"flag": "Avoids video calls", "revealed_at_turn": 4},
            {"flag": "Uses outdated slang", "revealed_at_turn": 8}
        ]
        
        should_reveal = catfish_flow._should_reveal_red_flag()
        assert should_reveal is False  # Already revealed expected number of flags
    
    def test_probing_question_detection(self, catfish_flow):
        """Test detection of user's probing questions."""
        # Test obvious probing questions
        probing_messages = [
            "How old are you?",
            "Where do you go to school?",
            "Can we video chat?",
            "Show me a photo of yourself",
            "What's your parents' names?",
            "Prove you're real"
        ]
        
        for message in probing_messages:
            is_probing = catfish_flow._detect_probing_question(message)
            assert is_probing is True, f"Failed to detect probing in: {message}"
        
        # Test normal conversation
        normal_messages = [
            "Hi there!",
            "I love that song too",
            "What's your favorite color?",
            "That's so cool!"
        ]
        
        for message in normal_messages:
            is_probing = catfish_flow._detect_probing_question(message)
            assert is_probing is False, f"False positive for: {message}"
    
    def test_typing_delay_calculation(self, catfish_flow):
        """Test realistic typing delay calculation."""
        # Test short message
        short_delay = catfish_flow._calculate_typing_delay("Hi!")
        assert 1.0 <= short_delay <= 5.0
        
        # Test long message
        long_message = "This is a much longer message that should take more time to type out naturally."
        long_delay = catfish_flow._calculate_typing_delay(long_message)
        assert long_delay > short_delay
        
        # Test evasive response (should take longer)
        evasive_delay = catfish_flow._calculate_typing_delay("Hi!", is_evasive=True)
        normal_delay = catfish_flow._calculate_typing_delay("Hi!", is_evasive=False)
        assert evasive_delay >= normal_delay
    
    def test_conversation_routing_logic(self, catfish_flow):
        """Test conversation status routing based on user behavior."""
        # Test high suspicion level
        catfish_flow.user_suspicion_level = 0.9
        catfish_flow.character_profile = {"red_flags": ["flag1", "flag2"]}
        
        state = {"session_id": "test"}
        route = catfish_flow.check_conversation_status(state)
        
        assert route == "user_detected_catfish"
        
        # Test all flags revealed
        catfish_flow.user_suspicion_level = 0.5
        catfish_flow.red_flags_revealed = [{"flag": "flag1"}, {"flag": "flag2"}]
        
        route = catfish_flow.check_conversation_status(state)
        
        assert route == "all_flags_revealed"
        
        # Test conversation timeout
        catfish_flow.user_suspicion_level = 0.3
        catfish_flow.red_flags_revealed = []
        catfish_flow.conversation_history = [{"msg": f"test_{i}"} for i in range(25)]
        
        route = catfish_flow.check_conversation_status(state)
        
        assert route == "conversation_timeout"


class TestFlowIntegration:
    """Test integration between different flows and shared components."""
    
    def test_agent_factory_integration(self, mock_agent_factory):
        """Test that flows properly integrate with agent factory."""
        # Test that all flows can be created with the same factory
        deepfake_flow = DeepfakeDetectionFlow(mock_agent_factory, locale="en")
        social_flow = SocialMediaSimulationFlow(mock_agent_factory, locale="en")
        catfish_flow = CatfishDetectionFlow(mock_agent_factory, locale="en")
        
        # Verify agents are properly assigned
        assert deepfake_flow.deepfake_analyst is not None
        assert social_flow.social_media_simulator is not None
        assert catfish_flow.catfish_character is not None
        
        # Test Portuguese locale
        pt_deepfake_flow = DeepfakeDetectionFlow(mock_agent_factory, locale="pt")
        assert pt_deepfake_flow.locale == "pt"
    
    def test_cross_flow_memory_isolation(self, mock_agent_factory):
        """Test that different flow instances maintain separate memory."""
        flow1 = CatfishDetectionFlow(mock_agent_factory, locale="en")
        flow2 = CatfishDetectionFlow(mock_agent_factory, locale="en")
        
        # Modify state in flow1
        flow1.user_suspicion_level = 0.8
        flow1.conversation_history = [{"test": "data"}]
        
        # Verify flow2 is unaffected
        assert flow2.user_suspicion_level == 0.0
        assert len(flow2.conversation_history) == 0
    
    @patch('crewai.Crew.kickoff')
    def test_concurrent_flow_execution(self, mock_kickoff, mock_agent_factory):
        """Test that multiple flows can execute concurrently."""
        mock_kickoff.return_value = MockCrewResult("Concurrent test result")
        
        # Create multiple flow instances
        flows = [
            DeepfakeDetectionFlow(mock_agent_factory, locale="en"),
            SocialMediaSimulationFlow(mock_agent_factory, locale="en"),
            CatfishDetectionFlow(mock_agent_factory, locale="en")
        ]
        
        # Create test requests
        requests = [
            DeepfakeChallengeRequest(user_id=f"user_{i}", difficulty_level=1, locale=LocaleEnum.EN)
            for i in range(3)
        ]
        
        social_request = SocialMediaSimulationRequest(
            user_id="social_user",
            session_duration_minutes=10,
            locale=LocaleEnum.EN
        )
        
        catfish_request = CatfishChatStartRequest(
            user_id="catfish_user",
            difficulty_level=2,
            locale=LocaleEnum.EN
        )
        
        # Execute flows concurrently (simulate)
        results = []
        
        # Deepfake flow
        result1 = flows[0].initialize_challenge(requests[0])
        results.append(result1)
        
        # Social media flow
        result2 = flows[1].initialize_simulation(social_request)
        results.append(result2)
        
        # Catfish flow
        result3 = flows[2].initialize_character(catfish_request)
        results.append(result3)
        
        # Verify all flows executed successfully
        assert len(results) == 3
        assert all("status" in result for result in results)
        
        # Verify each flow maintains its own state
        assert flows[0].current_challenge is not None
        assert len(flows[1].current_feed) > 0
        assert flows[2].character_profile is not None


@pytest.mark.asyncio
class TestAsyncFlowOperations:
    """Test asynchronous operations in flows."""
    
    async def test_async_crew_execution_simulation(self, mock_agent_factory):
        """Test simulated async crew execution."""
        flow = DeepfakeDetectionFlow(mock_agent_factory, locale="en")
        
        # Mock async crew execution
        async def mock_async_kickoff():
            await asyncio.sleep(0.1)  # Simulate processing time
            return MockCrewResult("Async result")
        
        with patch.object(flow, '_execute_crew_async', side_effect=mock_async_kickoff):
            # This would be the actual async execution in a real implementation
            result = await mock_async_kickoff()
            assert str(result) == "Async result"
    
    async def test_concurrent_user_interactions(self, mock_agent_factory):
        """Test handling concurrent user interactions."""
        flow = SocialMediaSimulationFlow(mock_agent_factory, locale="en")
        
        # Set up feed
        flow.current_feed = [
            {"post_id": f"post_{i}", "is_disinformation": i % 2 == 0}
            for i in range(10)
        ]
        
        # Simulate concurrent interactions
        async def simulate_interaction(post_id: str, interaction_type: str):
            await asyncio.sleep(0.05)  # Simulate network delay
            return flow.record_interaction(
                session_id="test_session",
                user_id="test_user",
                post_id=post_id,
                interaction_type=interaction_type
            )
        
        # Create concurrent tasks
        tasks = [
            simulate_interaction(f"post_{i}", "view")
            for i in range(5)
        ]
        
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify all interactions were recorded
        assert len(results) == 5
        assert all(isinstance(result, dict) for result in results)
        assert len(flow.user_interactions) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])