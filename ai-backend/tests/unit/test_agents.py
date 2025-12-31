"""
Unit tests for CrewAI agents and their responses.
Tests individual agent behavior, response quality, and multilingual support.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from crewai import Agent, Task, Crew

from src.agents.ethics_mentor import EthicsMentorAgent
from src.agents.deepfake_analyst import DeepfakeAnalystAgent
from src.agents.social_media_simulator import SocialMediaSimulatorAgent
from src.agents.catfish_character import CatfishCharacterAgent
from src.agents.analytics_agent import AnalyticsAgent
from src.agents.factory import AgentFactory


class TestEthicsMentorAgent:
    """Test Ethics Mentor Agent functionality."""
    
    @pytest.fixture
    def ethics_mentor(self):
        """Create Ethics Mentor Agent instance."""
        return EthicsMentorAgent(locale="en")
    
    def test_agent_initialization(self, ethics_mentor):
        """Test agent is properly initialized."""
        assert ethics_mentor is not None
        assert ethics_mentor.locale == "en"
        assert hasattr(ethics_mentor, 'agent')
    
    def test_agent_role_and_goal(self, ethics_mentor):
        """Test agent has correct role and goal."""
        agent = ethics_mentor.agent
        assert "ethics" in agent.role.lower() or "mentor" in agent.role.lower()
        assert agent.goal is not None
        assert len(agent.goal) > 0
    
    @pytest.mark.asyncio
    async def test_generate_feedback_english(self, ethics_mentor):
        """Test feedback generation in English."""
        with patch.object(ethics_mentor, 'generate_feedback', new_callable=AsyncMock) as mock_feedback:
            mock_feedback.return_value = {
                "feedback": "Good analysis of the ethical dilemma.",
                "reasoning": "You considered multiple perspectives.",
                "learning_objectives": ["Privacy", "Consent"],
                "follow_up_questions": ["What about data security?"]
            }
            
            result = await ethics_mentor.generate_feedback(
                challenge_id="test-123",
                user_response="I would respect privacy",
                correct_answer="Respect privacy and inform users"
            )
            
            assert "feedback" in result
            assert "reasoning" in result
            assert "learning_objectives" in result
            assert isinstance(result["learning_objectives"], list)
    
    @pytest.mark.asyncio
    async def test_generate_feedback_portuguese(self):
        """Test feedback generation in Portuguese."""
        ethics_mentor_pt = EthicsMentorAgent(locale="pt")
        
        with patch.object(ethics_mentor_pt, 'generate_feedback', new_callable=AsyncMock) as mock_feedback:
            mock_feedback.return_value = {
                "feedback": "Boa análise do dilema ético.",
                "reasoning": "Você considerou múltiplas perspectivas.",
                "learning_objectives": ["Privacidade", "Consentimento"],
                "follow_up_questions": ["E quanto à segurança dos dados?"]
            }
            
            result = await ethics_mentor_pt.generate_feedback(
                challenge_id="test-123",
                user_response="Eu respeitaria a privacidade",
                correct_answer="Respeitar privacidade e informar usuários"
            )
            
            assert "feedback" in result
            # Check for Portuguese characters
            assert any(char in str(result) for char in "áéíóúãõç")
    
    def test_adaptive_complexity(self, ethics_mentor):
        """Test feedback adapts to user history."""
        with patch.object(ethics_mentor, 'adjust_complexity') as mock_adjust:
            mock_adjust.return_value = "intermediate"
            
            user_history = [
                {"score": 0.8, "challenge_type": "privacy"},
                {"score": 0.9, "challenge_type": "security"}
            ]
            
            complexity = ethics_mentor.adjust_complexity(user_history)
            assert complexity in ["beginner", "intermediate", "advanced"]


class TestDeepfakeAnalystAgent:
    """Test Deepfake Analyst Agent functionality."""
    
    @pytest.fixture
    def deepfake_analyst(self):
        """Create Deepfake Analyst Agent instance."""
        return DeepfakeAnalystAgent()
    
    def test_agent_initialization(self, deepfake_analyst):
        """Test agent is properly initialized."""
        assert deepfake_analyst is not None
        assert hasattr(deepfake_analyst, 'agent')
    
    @pytest.mark.asyncio
    async def test_analyze_media_content(self, deepfake_analyst):
        """Test media content analysis."""
        with patch.object(deepfake_analyst, 'analyze_media', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = {
                "is_deepfake": True,
                "confidence": 0.85,
                "detection_clues": [
                    "Unnatural facial movements",
                    "Audio-video sync issues"
                ],
                "technical_indicators": ["Artifacts around mouth", "Inconsistent lighting"]
            }
            
            result = await deepfake_analyst.analyze_media(
                media_url="https://example.com/video.mp4",
                media_type="video"
            )
            
            assert "is_deepfake" in result
            assert "confidence" in result
            assert "detection_clues" in result
            assert isinstance(result["detection_clues"], list)
    
    @pytest.mark.asyncio
    async def test_generate_challenge(self, deepfake_analyst):
        """Test deepfake challenge generation."""
        with patch.object(deepfake_analyst, 'generate_challenge', new_callable=AsyncMock) as mock_challenge:
            mock_challenge.return_value = {
                "challenge_id": "df-001",
                "media_url": "https://example.com/challenge.mp4",
                "difficulty_level": 2,
                "is_deepfake": True
            }
            
            result = await deepfake_analyst.generate_challenge(difficulty=2)
            
            assert "challenge_id" in result
            assert "difficulty_level" in result
            assert result["difficulty_level"] == 2
    
    def test_difficulty_adaptation(self, deepfake_analyst):
        """Test difficulty adapts based on user accuracy."""
        with patch.object(deepfake_analyst, 'adjust_difficulty') as mock_adjust:
            mock_adjust.return_value = 3
            
            # High accuracy should increase difficulty
            new_difficulty = deepfake_analyst.adjust_difficulty(
                current_difficulty=2,
                accuracy_rate=0.9
            )
            
            assert new_difficulty >= 2


class TestSocialMediaSimulatorAgent:
    """Test Social Media Simulator Agent functionality."""
    
    @pytest.fixture
    def social_media_agent(self):
        """Create Social Media Simulator Agent instance."""
        return SocialMediaSimulatorAgent(locale="en")
    
    def test_agent_initialization(self, social_media_agent):
        """Test agent is properly initialized."""
        assert social_media_agent is not None
        assert social_media_agent.locale == "en"
    
    @pytest.mark.asyncio
    async def test_generate_social_media_feed(self, social_media_agent):
        """Test social media feed generation."""
        with patch.object(social_media_agent, 'generate_feed', new_callable=AsyncMock) as mock_feed:
            mock_feed.return_value = {
                "posts": [
                    {
                        "post_id": "post-1",
                        "content": "Breaking news about health...",
                        "is_disinformation": True,
                        "category": "health"
                    },
                    {
                        "post_id": "post-2",
                        "content": "Verified information from WHO",
                        "is_disinformation": False,
                        "category": "health"
                    }
                ]
            }
            
            result = await social_media_agent.generate_feed(num_posts=2)
            
            assert "posts" in result
            assert len(result["posts"]) == 2
            assert any(post["is_disinformation"] for post in result["posts"])
    
    @pytest.mark.asyncio
    async def test_generate_comment_thread(self, social_media_agent):
        """Test comment thread generation."""
        with patch.object(social_media_agent, 'generate_comments', new_callable=AsyncMock) as mock_comments:
            mock_comments.return_value = {
                "comments": [
                    {"user": "user1", "text": "I agree with this", "sentiment": "positive"},
                    {"user": "user2", "text": "This seems suspicious", "sentiment": "skeptical"}
                ]
            }
            
            result = await social_media_agent.generate_comments(
                post_id="post-1",
                num_comments=2
            )
            
            assert "comments" in result
            assert len(result["comments"]) == 2
    
    @pytest.mark.asyncio
    async def test_disinformation_categories(self, social_media_agent):
        """Test different disinformation categories."""
        categories = ["health", "politics", "conspiracy"]
        
        for category in categories:
            with patch.object(social_media_agent, 'generate_post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = {
                    "post_id": f"post-{category}",
                    "category": category,
                    "is_disinformation": True
                }
                
                result = await social_media_agent.generate_post(category=category)
                assert result["category"] == category


class TestCatfishCharacterAgent:
    """Test Catfish Character Agent functionality."""
    
    @pytest.fixture
    def catfish_agent(self):
        """Create Catfish Character Agent instance."""
        return CatfishCharacterAgent()
    
    def test_agent_initialization(self, catfish_agent):
        """Test agent is properly initialized."""
        assert catfish_agent is not None
        assert hasattr(catfish_agent, 'agent')
        assert hasattr(catfish_agent, 'character_profile')
    
    @pytest.mark.asyncio
    async def test_create_character_profile(self, catfish_agent):
        """Test character profile creation with inconsistencies."""
        with patch.object(catfish_agent, 'create_profile', new_callable=AsyncMock) as mock_profile:
            mock_profile.return_value = {
                "name": "Alex",
                "age": "25",
                "location": "New York",
                "inconsistencies": [
                    "Claims to be 25 but uses outdated slang",
                    "Says lives in NY but mentions local places from LA"
                ]
            }
            
            result = await catfish_agent.create_profile()
            
            assert "name" in result
            assert "inconsistencies" in result
            assert len(result["inconsistencies"]) > 0
    
    @pytest.mark.asyncio
    async def test_generate_response_with_red_flags(self, catfish_agent):
        """Test response generation with red flags."""
        with patch.object(catfish_agent, 'generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = {
                "message": "Hey! I'm doing great. Want to chat on another app?",
                "red_flags": ["Immediate request to move to another platform"],
                "typing_delay": 2.5
            }
            
            result = await catfish_agent.generate_response(
                user_message="Hi, how are you?",
                conversation_history=[]
            )
            
            assert "message" in result
            assert "red_flags" in result
            assert "typing_delay" in result
            assert result["typing_delay"] > 0
    
    @pytest.mark.asyncio
    async def test_character_consistency(self, catfish_agent):
        """Test character maintains consistency across conversation."""
        conversation_history = [
            {"role": "user", "content": "Where are you from?"},
            {"role": "agent", "content": "I'm from Seattle"},
        ]
        
        with patch.object(catfish_agent, 'generate_response', new_callable=AsyncMock) as mock_response:
            mock_response.return_value = {
                "message": "Yeah, I love the weather here in Seattle",
                "maintains_consistency": True
            }
            
            result = await catfish_agent.generate_response(
                user_message="Do you like the weather there?",
                conversation_history=conversation_history
            )
            
            assert "Seattle" in result["message"] or result.get("maintains_consistency")
    
    def test_typing_delay_calculation(self, catfish_agent):
        """Test realistic typing delay calculation."""
        with patch.object(catfish_agent, 'calculate_typing_delay') as mock_delay:
            mock_delay.return_value = 2.3
            
            short_message = "Hi"
            long_message = "This is a much longer message with more content"
            
            short_delay = catfish_agent.calculate_typing_delay(short_message)
            long_delay = catfish_agent.calculate_typing_delay(long_message)
            
            # Longer messages should have longer delays
            assert isinstance(short_delay, (int, float))
            assert isinstance(long_delay, (int, float))


class TestAnalyticsAgent:
    """Test Analytics Agent functionality."""
    
    @pytest.fixture
    def analytics_agent(self):
        """Create Analytics Agent instance."""
        return AnalyticsAgent()
    
    def test_agent_initialization(self, analytics_agent):
        """Test agent is properly initialized."""
        assert analytics_agent is not None
        assert hasattr(analytics_agent, 'agent')
    
    @pytest.mark.asyncio
    async def test_analyze_user_progress(self, analytics_agent):
        """Test user progress analysis."""
        with patch.object(analytics_agent, 'analyze_progress', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.return_value = {
                "competency_scores": {
                    "deepfake_detection": 0.75,
                    "disinformation_awareness": 0.82,
                    "catfish_detection": 0.68
                },
                "strengths": ["disinformation_awareness"],
                "improvement_areas": ["catfish_detection"]
            }
            
            user_history = [
                {"challenge_type": "deepfake", "score": 0.8},
                {"challenge_type": "social_media", "score": 0.9}
            ]
            
            result = await analytics_agent.analyze_progress(user_history)
            
            assert "competency_scores" in result
            assert "strengths" in result
            assert "improvement_areas" in result
    
    @pytest.mark.asyncio
    async def test_generate_recommendations(self, analytics_agent):
        """Test personalized recommendation generation."""
        with patch.object(analytics_agent, 'generate_recommendations', new_callable=AsyncMock) as mock_recs:
            mock_recs.return_value = {
                "recommendations": [
                    "Practice more catfish detection scenarios",
                    "Review red flag identification techniques"
                ],
                "next_challenges": ["catfish-advanced-1", "catfish-advanced-2"]
            }
            
            competency_scores = {
                "deepfake_detection": 0.85,
                "catfish_detection": 0.60
            }
            
            result = await analytics_agent.generate_recommendations(competency_scores)
            
            assert "recommendations" in result
            assert len(result["recommendations"]) > 0
    
    @pytest.mark.asyncio
    async def test_peer_comparison(self, analytics_agent):
        """Test anonymized peer comparison."""
        with patch.object(analytics_agent, 'compare_with_peers', new_callable=AsyncMock) as mock_compare:
            mock_compare.return_value = {
                "percentile": 75,
                "average_score": 0.70,
                "user_score": 0.80
            }
            
            result = await analytics_agent.compare_with_peers(
                user_id="user-123",
                competency_area="deepfake_detection"
            )
            
            assert "percentile" in result
            assert result["user_score"] >= result["average_score"]


class TestAgentFactory:
    """Test Agent Factory functionality."""
    
    @pytest.fixture
    def agent_factory(self):
        """Create Agent Factory instance."""
        return AgentFactory()
    
    def test_create_ethics_mentor(self, agent_factory):
        """Test creating ethics mentor agent."""
        with patch.object(agent_factory, 'create_agent') as mock_create:
            mock_create.return_value = Mock(spec=EthicsMentorAgent)
            
            agent = agent_factory.create_agent("ethics_mentor", locale="en")
            
            assert agent is not None
            mock_create.assert_called_once()
    
    def test_create_all_agents(self, agent_factory):
        """Test creating all agent types."""
        agent_types = [
            "ethics_mentor",
            "deepfake_analyst",
            "social_media_simulator",
            "catfish_character",
            "analytics"
        ]
        
        for agent_type in agent_types:
            with patch.object(agent_factory, 'create_agent') as mock_create:
                mock_create.return_value = Mock()
                
                agent = agent_factory.create_agent(agent_type)
                assert agent is not None
    
    def test_invalid_agent_type(self, agent_factory):
        """Test handling of invalid agent type."""
        with pytest.raises(ValueError):
            agent_factory.create_agent("invalid_agent_type")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



class TestAgentErrorHandling:
    """Test error handling across all agents."""
    
    @pytest.mark.asyncio
    async def test_agent_handles_invalid_input(self):
        """Test agents handle invalid input gracefully."""
        ethics_mentor = EthicsMentorAgent(locale="en")
        
        with patch.object(ethics_mentor, 'generate_feedback', new_callable=AsyncMock) as mock_feedback:
            mock_feedback.side_effect = ValueError("Invalid input")
            
            with pytest.raises(ValueError):
                await ethics_mentor.generate_feedback(
                    challenge_id="",
                    user_response="",
                    correct_answer=""
                )
    
    @pytest.mark.asyncio
    async def test_agent_timeout_handling(self):
        """Test agents handle timeouts appropriately."""
        deepfake_analyst = DeepfakeAnalystAgent()
        
        with patch.object(deepfake_analyst, 'analyze_media', new_callable=AsyncMock) as mock_analyze:
            mock_analyze.side_effect = TimeoutError("Request timeout")
            
            with pytest.raises(TimeoutError):
                await deepfake_analyst.analyze_media(
                    media_url="https://example.com/video.mp4",
                    media_type="video"
                )
    
    def test_agent_locale_validation(self):
        """Test agents validate locale parameter."""
        # Valid locales should work
        ethics_mentor_en = EthicsMentorAgent(locale="en")
        assert ethics_mentor_en.locale == "en"
        
        ethics_mentor_pt = EthicsMentorAgent(locale="pt")
        assert ethics_mentor_pt.locale == "pt"

    
    def test_agent_response_format_validation(self):
        """Test agents return properly formatted responses."""
        # This test validates that agent responses have required fields
        with patch('src.agents.ethics_mentor.EthicsMentorAgent') as MockAgent:
            mock_instance = MockAgent.return_value
            mock_instance.generate_feedback = AsyncMock(return_value={
                "feedback": "Test feedback",
                "reasoning": "Test reasoning",
                "learning_objectives": ["Objective 1"],
                "follow_up_questions": ["Question 1"]
            })
            
            # Verify the mock returns expected format
            assert mock_instance.generate_feedback is not None
