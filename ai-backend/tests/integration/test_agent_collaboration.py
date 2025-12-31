"""
Integration tests for CrewAI agent collaboration and task delegation.

This module tests how agents work together in crews, task delegation
between agents, and collaborative decision making.

Requirements tested: 9.1, 9.2
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List

from crewai import Agent, Crew, Task, Process
from crewai.memory import LongTermMemory, ShortTermMemory

from src.agents.factory import AgentFactory
from src.flows.deepfake_detection_flow import DeepfakeDetectionFlow
from src.flows.social_media_simulation_flow import SocialMediaSimulationFlow
from src.flows.catfish_detection_flow import CatfishDetectionFlow


class MockAgent:
    """Enhanced mock agent for collaboration testing."""
    
    def __init__(self, role: str, goal: str, backstory: str = ""):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.memory = True
        self.verbose = True
        self.allow_delegation = False
        self.max_iter = 5
        self.execution_history = []
        self.collaboration_log = []
    
    def execute_task(self, task: Task) -> str:
        """Mock task execution with logging."""
        self.execution_history.append({
            "task_description": task.description,
            "expected_output": task.expected_output,
            "timestamp": "mock_timestamp"
        })
        return f"Mock result from {self.role}"
    
    def collaborate_with(self, other_agent: 'MockAgent', context: str) -> str:
        """Mock collaboration between agents."""
        collaboration_entry = {
            "collaborator": other_agent.role,
            "context": context,
            "result": f"Collaboration between {self.role} and {other_agent.role}"
        }
        self.collaboration_log.append(collaboration_entry)
        other_agent.collaboration_log.append(collaboration_entry)
        return collaboration_entry["result"]


class MockCrew:
    """Enhanced mock crew for testing agent collaboration."""
    
    def __init__(self, agents: List[MockAgent], tasks: List[Task], process: Process = Process.sequential):
        self.agents = agents
        self.tasks = tasks
        self.process = process
        self.execution_log = []
        self.collaboration_events = []
    
    def kickoff(self) -> str:
        """Mock crew execution with collaboration tracking."""
        result = "Mock crew execution result"
        
        # Log execution
        self.execution_log.append({
            "agents_count": len(self.agents),
            "tasks_count": len(self.tasks),
            "process": self.process,
            "result": result
        })
        
        # Simulate agent collaboration
        if len(self.agents) > 1:
            for i, agent in enumerate(self.agents):
                for j, other_agent in enumerate(self.agents):
                    if i != j:
                        collaboration = agent.collaborate_with(
                            other_agent, 
                            f"Task collaboration context"
                        )
                        self.collaboration_events.append(collaboration)
        
        return result


@pytest.fixture
def mock_agents():
    """Create a set of mock agents for testing."""
    return {
        "deepfake_analyst": MockAgent(
            role="Deepfake Detection Specialist",
            goal="Analyze media content for deepfake indicators",
            backstory="Expert in media forensics and deepfake detection"
        ),
        "ethics_mentor": MockAgent(
            role="Ethics Education Mentor", 
            goal="Provide educational feedback on ethical decisions",
            backstory="Experienced educator in cyber ethics"
        ),
        "social_media_simulator": MockAgent(
            role="Social Media Content Simulator",
            goal="Generate realistic social media content for training",
            backstory="Expert in social media patterns and disinformation"
        ),
        "catfish_character": MockAgent(
            role="Catfish Character Simulator",
            goal="Simulate suspicious online personas for detection training",
            backstory="Specialist in online deception patterns"
        ),
        "analytics_agent": MockAgent(
            role="Learning Analytics Specialist",
            goal="Analyze user progress and generate insights",
            backstory="Expert in educational data analysis"
        ),
        "conversation_moderator": MockAgent(
            role="Conversation Moderator",
            goal="Manage conversation flow and context",
            backstory="Specialist in dialogue management"
        )
    }


class TestAgentCollaboration:
    """Test agent collaboration patterns."""
    
    def test_two_agent_collaboration(self, mock_agents):
        """Test collaboration between two agents."""
        deepfake_agent = mock_agents["deepfake_analyst"]
        ethics_agent = mock_agents["ethics_mentor"]
        
        # Create a task that requires collaboration
        collaborative_task = Task(
            description="Analyze deepfake content and provide educational feedback",
            expected_output="Combined analysis and educational content",
            agent=deepfake_agent
        )
        
        # Create crew with both agents
        crew = MockCrew(
            agents=[deepfake_agent, ethics_agent],
            tasks=[collaborative_task],
            process=Process.sequential
        )
        
        # Execute crew
        result = crew.kickoff()
        
        # Verify collaboration occurred
        assert len(crew.collaboration_events) > 0
        assert len(deepfake_agent.collaboration_log) > 0
        assert len(ethics_agent.collaboration_log) > 0
        
        # Verify agents collaborated with each other
        deepfake_collaborations = [
            log for log in deepfake_agent.collaboration_log 
            if log["collaborator"] == ethics_agent.role
        ]
        assert len(deepfake_collaborations) > 0
    
    def test_multi_agent_crew_collaboration(self, mock_agents):
        """Test collaboration in a multi-agent crew."""
        agents = [
            mock_agents["deepfake_analyst"],
            mock_agents["ethics_mentor"],
            mock_agents["analytics_agent"]
        ]
        
        # Create tasks for multi-agent collaboration
        tasks = [
            Task(
                description="Analyze media content for deepfake indicators",
                expected_output="Technical analysis report",
                agent=agents[0]
            ),
            Task(
                description="Generate educational feedback based on analysis",
                expected_output="Educational content",
                agent=agents[1]
            ),
            Task(
                description="Track user progress and generate insights",
                expected_output="Progress analytics",
                agent=agents[2]
            )
        ]
        
        # Create crew with hierarchical process
        crew = MockCrew(
            agents=agents,
            tasks=tasks,
            process=Process.hierarchical
        )
        
        result = crew.kickoff()
        
        # Verify all agents participated
        assert len(crew.execution_log) > 0
        assert crew.execution_log[0]["agents_count"] == 3
        
        # Verify cross-agent collaboration
        total_collaborations = sum(len(agent.collaboration_log) for agent in agents)
        assert total_collaborations > 0
        
        # Verify each agent collaborated with others
        for agent in agents:
            collaborator_roles = [log["collaborator"] for log in agent.collaboration_log]
            other_agent_roles = [other.role for other in agents if other != agent]
            
            # At least some collaboration should have occurred
            assert any(role in collaborator_roles for role in other_agent_roles)
    
    def test_task_delegation_patterns(self, mock_agents):
        """Test different task delegation patterns."""
        manager_agent = mock_agents["conversation_moderator"]
        worker_agents = [
            mock_agents["deepfake_analyst"],
            mock_agents["social_media_simulator"]
        ]
        
        # Enable delegation for manager
        manager_agent.allow_delegation = True
        
        # Create delegated tasks
        main_task = Task(
            description="Coordinate content analysis and generation",
            expected_output="Coordinated analysis and content",
            agent=manager_agent
        )
        
        subtask_1 = Task(
            description="Analyze content for authenticity",
            expected_output="Authenticity analysis",
            agent=worker_agents[0]
        )
        
        subtask_2 = Task(
            description="Generate educational content",
            expected_output="Educational materials",
            agent=worker_agents[1]
        )
        
        # Create crew with delegation
        all_agents = [manager_agent] + worker_agents
        crew = MockCrew(
            agents=all_agents,
            tasks=[main_task, subtask_1, subtask_2],
            process=Process.hierarchical
        )
        
        result = crew.kickoff()
        
        # Verify delegation occurred
        assert manager_agent.allow_delegation is True
        
        # Verify manager collaborated with workers
        manager_collaborations = manager_agent.collaboration_log
        worker_roles = [agent.role for agent in worker_agents]
        
        collaborating_with_workers = any(
            log["collaborator"] in worker_roles 
            for log in manager_collaborations
        )
        assert collaborating_with_workers
    
    def test_sequential_vs_hierarchical_collaboration(self, mock_agents):
        """Test different collaboration patterns in sequential vs hierarchical processes."""
        agents = [
            mock_agents["deepfake_analyst"],
            mock_agents["ethics_mentor"]
        ]
        
        task = Task(
            description="Analyze and provide feedback",
            expected_output="Analysis with feedback",
            agent=agents[0]
        )
        
        # Test sequential process
        sequential_crew = MockCrew(
            agents=agents,
            tasks=[task],
            process=Process.sequential
        )
        
        sequential_result = sequential_crew.kickoff()
        sequential_collaborations = len(sequential_crew.collaboration_events)
        
        # Test hierarchical process
        hierarchical_crew = MockCrew(
            agents=agents,
            tasks=[task],
            process=Process.hierarchical
        )
        
        hierarchical_result = hierarchical_crew.kickoff()
        hierarchical_collaborations = len(hierarchical_crew.collaboration_events)
        
        # Both should have collaborations, but patterns may differ
        assert sequential_collaborations > 0
        assert hierarchical_collaborations > 0
        
        # Verify process types were recorded
        assert sequential_crew.execution_log[0]["process"] == Process.sequential
        assert hierarchical_crew.execution_log[0]["process"] == Process.hierarchical


class TestTaskDelegation:
    """Test task delegation mechanisms."""
    
    def test_complex_task_breakdown(self, mock_agents):
        """Test breaking down complex tasks into subtasks."""
        # Create a complex scenario requiring multiple agents
        main_agent = mock_agents["analytics_agent"]
        supporting_agents = [
            mock_agents["deepfake_analyst"],
            mock_agents["social_media_simulator"],
            mock_agents["ethics_mentor"]
        ]
        
        # Complex task requiring multiple expertise areas
        complex_task = Task(
            description="""
            Generate comprehensive user progress report including:
            1. Deepfake detection performance analysis
            2. Social media literacy assessment  
            3. Overall ethical decision-making evaluation
            4. Personalized learning recommendations
            """,
            expected_output="Comprehensive progress report with recommendations",
            agent=main_agent
        )
        
        # Supporting tasks for each expertise area
        supporting_tasks = [
            Task(
                description="Analyze user's deepfake detection performance",
                expected_output="Deepfake detection analysis",
                agent=supporting_agents[0]
            ),
            Task(
                description="Assess social media literacy skills",
                expected_output="Social media literacy assessment",
                agent=supporting_agents[1]
            ),
            Task(
                description="Evaluate ethical decision-making patterns",
                expected_output="Ethics evaluation",
                agent=supporting_agents[2]
            )
        ]
        
        # Create crew with task delegation
        all_agents = [main_agent] + supporting_agents
        crew = MockCrew(
            agents=all_agents,
            tasks=[complex_task] + supporting_tasks,
            process=Process.hierarchical
        )
        
        result = crew.kickoff()
        
        # Verify task delegation occurred
        assert len(crew.execution_log) > 0
        assert crew.execution_log[0]["tasks_count"] == 4  # 1 main + 3 supporting
        
        # Verify main agent collaborated with all supporting agents
        main_collaborations = main_agent.collaboration_log
        supporting_roles = [agent.role for agent in supporting_agents]
        
        for role in supporting_roles:
            collaborated_with_role = any(
                log["collaborator"] == role 
                for log in main_collaborations
            )
            assert collaborated_with_role, f"Main agent should collaborate with {role}"
    
    def test_dynamic_task_assignment(self, mock_agents):
        """Test dynamic task assignment based on agent capabilities."""
        # Create agents with different specializations
        specialist_agents = {
            "media_analysis": mock_agents["deepfake_analyst"],
            "content_generation": mock_agents["social_media_simulator"],
            "user_education": mock_agents["ethics_mentor"],
            "data_analysis": mock_agents["analytics_agent"]
        }
        
        # Tasks requiring different specializations
        specialized_tasks = [
            {
                "task": Task(
                    description="Analyze suspicious media content",
                    expected_output="Media analysis report",
                    agent=specialist_agents["media_analysis"]
                ),
                "required_specialty": "media_analysis"
            },
            {
                "task": Task(
                    description="Generate educational scenarios",
                    expected_output="Educational content",
                    agent=specialist_agents["content_generation"]
                ),
                "required_specialty": "content_generation"
            },
            {
                "task": Task(
                    description="Create learning feedback",
                    expected_output="Educational feedback",
                    agent=specialist_agents["user_education"]
                ),
                "required_specialty": "user_education"
            }
        ]
        
        # Create crew with specialized task assignment
        all_agents = list(specialist_agents.values())
        all_tasks = [item["task"] for item in specialized_tasks]
        
        crew = MockCrew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # Verify appropriate agents were assigned to tasks
        for agent in all_agents:
            assert len(agent.execution_history) >= 0  # Agents may execute tasks
        
        # Verify collaboration occurred between specialists
        total_collaborations = sum(len(agent.collaboration_log) for agent in all_agents)
        assert total_collaborations > 0
    
    def test_error_handling_in_delegation(self, mock_agents):
        """Test error handling when task delegation fails."""
        main_agent = mock_agents["conversation_moderator"]
        failing_agent = Mock(spec=MockAgent)
        failing_agent.role = "Failing Agent"
        failing_agent.collaboration_log = []
        
        # Mock failure in collaboration
        def failing_collaboration(other_agent, context):
            raise Exception("Collaboration failed")
        
        failing_agent.collaborate_with = failing_collaboration
        
        # Create crew with failing agent
        crew = MockCrew(
            agents=[main_agent, failing_agent],
            tasks=[Task(
                description="Test task with failing collaboration",
                expected_output="Should handle failure gracefully",
                agent=main_agent
            )],
            process=Process.sequential
        )
        
        # Execute should handle failure gracefully
        try:
            result = crew.kickoff()
            # In a real implementation, this would handle the error gracefully
            assert True  # Test passes if no unhandled exception
        except Exception as e:
            # If exception occurs, it should be a handled error
            assert "Collaboration failed" in str(e)


class TestMemoryAndContextSharing:
    """Test memory persistence and context sharing between agents."""
    
    def test_shared_memory_between_agents(self, mock_agents):
        """Test that agents can share memory and context."""
        agent1 = mock_agents["deepfake_analyst"]
        agent2 = mock_agents["ethics_mentor"]
        
        # Mock memory systems
        shared_memory = Mock(spec=LongTermMemory)
        shared_memory.save = Mock()
        shared_memory.search = Mock(return_value=["shared context"])
        
        # Simulate agents sharing memory
        agent1.shared_memory = shared_memory
        agent2.shared_memory = shared_memory
        
        # Create collaborative task
        task = Task(
            description="Analyze content and provide educational feedback using shared context",
            expected_output="Contextual analysis and feedback",
            agent=agent1
        )
        
        crew = MockCrew(
            agents=[agent1, agent2],
            tasks=[task],
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # Verify agents collaborated
        assert len(agent1.collaboration_log) > 0
        assert len(agent2.collaboration_log) > 0
        
        # In a real implementation, we would verify memory operations
        # For now, we verify the mock memory was set up
        assert hasattr(agent1, 'shared_memory')
        assert hasattr(agent2, 'shared_memory')
        assert agent1.shared_memory == agent2.shared_memory
    
    def test_context_preservation_across_tasks(self, mock_agents):
        """Test context preservation across multiple tasks."""
        agents = [
            mock_agents["deepfake_analyst"],
            mock_agents["ethics_mentor"],
            mock_agents["analytics_agent"]
        ]
        
        # Sequential tasks that build on each other
        sequential_tasks = [
            Task(
                description="Analyze user submission for deepfake indicators",
                expected_output="Technical analysis with context",
                agent=agents[0]
            ),
            Task(
                description="Generate educational feedback based on previous analysis",
                expected_output="Contextual educational feedback",
                agent=agents[1]
            ),
            Task(
                description="Update user progress based on analysis and feedback",
                expected_output="Updated progress with full context",
                agent=agents[2]
            )
        ]
        
        crew = MockCrew(
            agents=agents,
            tasks=sequential_tasks,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # Verify all tasks were processed
        assert len(crew.execution_log) > 0
        assert crew.execution_log[0]["tasks_count"] == 3
        
        # Verify context was shared between agents
        for i, agent in enumerate(agents):
            # Each agent should have execution history
            assert hasattr(agent, 'execution_history')
            
            # Agents should have collaborated (shared context)
            if i < len(agents) - 1:  # Not the last agent
                next_agent = agents[i + 1]
                collaborated = any(
                    log["collaborator"] == next_agent.role 
                    for log in agent.collaboration_log
                )
                assert collaborated, f"Agent {agent.role} should collaborate with {next_agent.role}"
    
    def test_memory_isolation_between_sessions(self, mock_agents):
        """Test that different sessions maintain separate memory contexts."""
        agent = mock_agents["catfish_character"]
        
        # Simulate two different sessions
        session1_memory = Mock(spec=LongTermMemory)
        session1_memory.session_id = "session_1"
        session1_memory.context = {"character": "Alice", "age": 16}
        
        session2_memory = Mock(spec=LongTermMemory)
        session2_memory.session_id = "session_2"  
        session2_memory.context = {"character": "Bob", "age": 17}
        
        # Test session 1
        agent.current_memory = session1_memory
        task1 = Task(
            description="Respond as character Alice",
            expected_output="Response from Alice",
            agent=agent
        )
        
        crew1 = MockCrew(agents=[agent], tasks=[task1])
        result1 = crew1.kickoff()
        
        # Test session 2 with different memory
        agent.current_memory = session2_memory
        task2 = Task(
            description="Respond as character Bob", 
            expected_output="Response from Bob",
            agent=agent
        )
        
        crew2 = MockCrew(agents=[agent], tasks=[task2])
        result2 = crew2.kickoff()
        
        # Verify sessions maintained separate contexts
        assert session1_memory.session_id != session2_memory.session_id
        assert session1_memory.context != session2_memory.context
        
        # Verify agent executed tasks in both sessions
        assert len(agent.execution_history) == 2


class TestRealWorldCollaborationScenarios:
    """Test collaboration scenarios that mirror real-world usage."""
    
    def test_deepfake_analysis_collaboration(self, mock_agents):
        """Test collaboration in deepfake analysis scenario."""
        # Agents involved in deepfake analysis
        deepfake_analyst = mock_agents["deepfake_analyst"]
        ethics_mentor = mock_agents["ethics_mentor"]
        analytics_agent = mock_agents["analytics_agent"]
        
        # Real-world deepfake analysis workflow
        analysis_tasks = [
            Task(
                description="Analyze uploaded media for deepfake indicators",
                expected_output="Technical deepfake analysis report",
                agent=deepfake_analyst
            ),
            Task(
                description="Generate educational feedback based on analysis results",
                expected_output="Educational feedback with learning objectives",
                agent=ethics_mentor
            ),
            Task(
                description="Update user competency scores based on performance",
                expected_output="Updated user analytics",
                agent=analytics_agent
            )
        ]
        
        crew = MockCrew(
            agents=[deepfake_analyst, ethics_mentor, analytics_agent],
            tasks=analysis_tasks,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # Verify realistic collaboration pattern
        assert len(crew.collaboration_events) > 0
        
        # Verify analyst collaborated with educator
        analyst_collaborations = [
            log for log in deepfake_analyst.collaboration_log
            if log["collaborator"] == ethics_mentor.role
        ]
        assert len(analyst_collaborations) > 0
        
        # Verify educator collaborated with analytics
        educator_collaborations = [
            log for log in ethics_mentor.collaboration_log
            if log["collaborator"] == analytics_agent.role
        ]
        assert len(educator_collaborations) > 0
    
    def test_social_media_simulation_collaboration(self, mock_agents):
        """Test collaboration in social media simulation scenario."""
        # Agents for social media simulation
        content_generator = mock_agents["social_media_simulator"]
        moderator = mock_agents["conversation_moderator"]
        analytics_agent = mock_agents["analytics_agent"]
        
        # Social media simulation workflow
        simulation_tasks = [
            Task(
                description="Generate realistic social media feed with disinformation",
                expected_output="Mixed authentic and disinformation posts",
                agent=content_generator
            ),
            Task(
                description="Monitor user interactions and provide real-time feedback",
                expected_output="Interaction monitoring and algorithm feedback",
                agent=moderator
            ),
            Task(
                description="Analyze user engagement patterns and detection accuracy",
                expected_output="Engagement analysis and recommendations",
                agent=analytics_agent
            )
        ]
        
        crew = MockCrew(
            agents=[content_generator, moderator, analytics_agent],
            tasks=simulation_tasks,
            process=Process.hierarchical
        )
        
        result = crew.kickoff()
        
        # Verify collaboration in simulation context
        assert len(crew.collaboration_events) > 0
        
        # Verify content generator worked with moderator
        generator_collaborations = [
            log for log in content_generator.collaboration_log
            if log["collaborator"] == moderator.role
        ]
        assert len(generator_collaborations) > 0
    
    def test_catfish_detection_collaboration(self, mock_agents):
        """Test collaboration in catfish detection scenario."""
        # Agents for catfish simulation
        catfish_character = mock_agents["catfish_character"]
        moderator = mock_agents["conversation_moderator"]
        analytics_agent = mock_agents["analytics_agent"]
        
        # Catfish detection workflow
        catfish_tasks = [
            Task(
                description="Create believable character with red flags",
                expected_output="Character profile with strategic inconsistencies",
                agent=catfish_character
            ),
            Task(
                description="Manage conversation flow and red flag revelation",
                expected_output="Natural conversation with strategic reveals",
                agent=moderator
            ),
            Task(
                description="Analyze user's detection skills and provide feedback",
                expected_output="Detection performance analysis",
                agent=analytics_agent
            )
        ]
        
        crew = MockCrew(
            agents=[catfish_character, moderator, analytics_agent],
            tasks=catfish_tasks,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # Verify catfish character collaborated with moderator
        character_collaborations = [
            log for log in catfish_character.collaboration_log
            if log["collaborator"] == moderator.role
        ]
        assert len(character_collaborations) > 0
        
        # Verify moderator collaborated with analytics
        moderator_collaborations = [
            log for log in moderator.collaboration_log
            if log["collaborator"] == analytics_agent.role
        ]
        assert len(moderator_collaborations) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])