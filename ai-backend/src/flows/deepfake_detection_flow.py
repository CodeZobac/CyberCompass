"""
Deepfake Detection Flow - CrewAI Flow for deepfake challenge progression.

This flow manages the complete deepfake detection challenge lifecycle:
1. Initialize challenge with appropriate difficulty
2. Present media content for analysis
3. Process user submission
4. Provide detailed feedback with detection clues
5. Adapt difficulty based on performance
"""

from typing import Any, Dict, Optional
from datetime import datetime
import uuid

from crewai import Flow, Agent, Crew, Task
from crewai.flow.flow import start, listen, router

from ..agents.factory import AgentFactory
from ..models.requests import (
    DeepfakeChallengeRequest,
    DeepfakeSubmissionRequest,
    MediaType,
)
from ..models.responses import SuccessResponse


class DeepfakeDetectionFlow(Flow):
    """
    CrewAI Flow for managing deepfake detection challenges.
    
    This flow coordinates the deepfake analyst agent to:
    - Generate appropriate challenges based on user skill level
    - Analyze user submissions
    - Provide educational feedback with detection clues
    - Track progress and adapt difficulty
    """
    
    def __init__(self, agent_factory: AgentFactory, locale: str = "en"):
        """
        Initialize the Deepfake Detection Flow.
        
        Args:
            agent_factory: Factory for creating agents
            locale: Language locale ('en' or 'pt')
        """
        super().__init__()
        self.agent_factory = agent_factory
        self.locale = locale
        
        # Create specialized agents
        self.deepfake_analyst = agent_factory.create_agent("deepfake_analyst", locale)
        self.ethics_mentor = agent_factory.create_agent("ethics_mentor", locale)
        
        # Flow state
        self.current_challenge: Optional[Dict[str, Any]] = None
        self.user_performance_history: list = []
        
    @start()
    def initialize_challenge(self, request: DeepfakeChallengeRequest) -> Dict[str, Any]:
        """
        Initialize a new deepfake detection challenge.
        
        This is the entry point of the flow. It creates a challenge
        appropriate for the user's skill level.
        
        Args:
            request: Challenge request with user preferences
            
        Returns:
            Challenge data including media URL and instructions
        """
        # Create task for challenge generation
        challenge_task = Task(
            description=f"""
            Create a deepfake detection challenge with the following parameters:
            - Difficulty level: {request.difficulty_level} (1-5 scale)
            - Media type: {request.media_type or 'any'}
            - User locale: {request.locale}
            
            Generate a challenge that includes:
            1. A media file (audio, video, or image) that may or may not be a deepfake
            2. Clear instructions in {request.locale}
            3. Appropriate hints based on difficulty level
            4. Detection clues that should be identifiable at this difficulty
            
            The challenge should be educational and help users develop real-world detection skills.
            """,
            expected_output="""
            A JSON object containing:
            - challenge_id: unique identifier
            - media_url: URL to the media content
            - media_type: type of media (audio/video/image)
            - is_deepfake: boolean indicating if it's actually a deepfake
            - difficulty_level: the difficulty level
            - instructions: clear instructions in the user's language
            - hints: list of optional hints
            - detection_clues: list of clues that reveal the truth
            """,
            agent=self.deepfake_analyst,
        )
        
        # Create crew for challenge generation
        challenge_crew = Crew(
            agents=[self.deepfake_analyst],
            tasks=[challenge_task],
            verbose=True,
        )
        
        # Execute challenge generation
        result = challenge_crew.kickoff()
        
        # Parse and structure the challenge
        challenge_data = self._parse_challenge_result(result, request)
        self.current_challenge = challenge_data
        
        return {
            "status": "challenge_initialized",
            "challenge": challenge_data,
            "user_id": request.user_id,
        }
    
    @listen(initialize_challenge)
    def await_user_submission(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wait for user submission and prepare for analysis.
        
        This method transitions the flow to a state where it's ready
        to receive and process the user's detection decision.
        
        Args:
            state: Current flow state with challenge data
            
        Returns:
            State indicating readiness for submission
        """
        return {
            "status": "awaiting_submission",
            "challenge_id": state["challenge"]["challenge_id"],
            "user_id": state["user_id"],
            "ready_for_submission": True,
        }
    
    def process_submission(
        self, 
        submission: DeepfakeSubmissionRequest
    ) -> Dict[str, Any]:
        """
        Process user's deepfake detection submission.
        
        This method is called when the user submits their detection decision.
        It analyzes the submission and generates detailed feedback.
        
        Args:
            submission: User's detection submission
            
        Returns:
            Analysis results and feedback
        """
        if not self.current_challenge:
            raise ValueError("No active challenge to process submission for")
        
        # Verify submission matches current challenge
        if submission.challenge_id != self.current_challenge["challenge_id"]:
            raise ValueError("Submission does not match current challenge")
        
        # Determine if user was correct
        is_correct = submission.is_deepfake == self.current_challenge["is_deepfake"]
        
        # Create feedback task
        feedback_task = Task(
            description=f"""
            Analyze the user's deepfake detection submission and provide educational feedback.
            
            Challenge Details:
            - Media type: {self.current_challenge['media_type']}
            - Actual answer: {'IS a deepfake' if self.current_challenge['is_deepfake'] else 'NOT a deepfake'}
            - Difficulty level: {self.current_challenge['difficulty_level']}
            
            User Submission:
            - Detection decision: {'IS a deepfake' if submission.is_deepfake else 'NOT a deepfake'}
            - Confidence: {submission.confidence}
            - User's reasoning: {submission.reasoning or 'Not provided'}
            - Result: {'CORRECT' if is_correct else 'INCORRECT'}
            
            Provide comprehensive feedback that includes:
            1. Whether the detection was correct
            2. Detailed explanation of the actual answer
            3. Key detection clues the user should have noticed
            4. Technical explanation of deepfake indicators (or lack thereof)
            5. Encouragement and learning points
            6. Suggestions for what to look for in future challenges
            
            Adapt the feedback complexity to the difficulty level and user's reasoning.
            Be educational, supportive, and help build detection skills.
            """,
            expected_output="""
            A JSON object containing:
            - correct: boolean
            - actual_answer: boolean (is it actually a deepfake)
            - feedback: detailed feedback text
            - detection_clues: list of key clues
            - technical_explanation: technical details about the media
            - score: numerical score (0-100)
            - learning_points: key takeaways
            - next_steps: suggestions for improvement
            """,
            agent=self.deepfake_analyst,
        )
        
        # Create crew for feedback generation
        feedback_crew = Crew(
            agents=[self.deepfake_analyst, self.ethics_mentor],
            tasks=[feedback_task],
            verbose=True,
        )
        
        # Execute feedback generation
        result = feedback_crew.kickoff()
        
        # Parse feedback result
        feedback_data = self._parse_feedback_result(result, is_correct, submission)
        
        # Update performance history
        self._update_performance_history(submission, feedback_data)
        
        return {
            "status": "submission_processed",
            "feedback": feedback_data,
            "challenge_id": submission.challenge_id,
            "user_id": submission.user_id,
        }
    
    @router(process_submission)
    def determine_next_action(self, state: Dict[str, Any]) -> str:
        """
        Determine the next action based on user performance.
        
        This router decides whether to:
        - Increase difficulty (if user is performing well)
        - Maintain difficulty (if performance is appropriate)
        - Decrease difficulty (if user is struggling)
        - Provide additional training (if user needs more practice)
        
        Args:
            state: Current state with feedback data
            
        Returns:
            Route name for next action
        """
        feedback = state["feedback"]
        
        # Analyze recent performance
        if len(self.user_performance_history) >= 3:
            recent_scores = [p["score"] for p in self.user_performance_history[-3:]]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            if avg_score >= 80:
                return "increase_difficulty"
            elif avg_score >= 60:
                return "maintain_difficulty"
            else:
                return "provide_additional_training"
        
        # Not enough history, maintain current difficulty
        return "maintain_difficulty"
    
    @listen("increase_difficulty")
    def adapt_difficulty_up(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Increase challenge difficulty for high-performing users.
        
        Args:
            state: Current flow state
            
        Returns:
            Updated state with new difficulty level
        """
        current_difficulty = self.current_challenge.get("difficulty_level", 1)
        new_difficulty = min(current_difficulty + 1, 5)
        
        return {
            "status": "difficulty_increased",
            "new_difficulty": new_difficulty,
            "message": f"Great job! Moving to difficulty level {new_difficulty}",
        }
    
    @listen("maintain_difficulty")
    def maintain_current_difficulty(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maintain current difficulty level.
        
        Args:
            state: Current flow state
            
        Returns:
            State confirming difficulty maintenance
        """
        current_difficulty = self.current_challenge.get("difficulty_level", 1)
        
        return {
            "status": "difficulty_maintained",
            "difficulty": current_difficulty,
            "message": "Continue practicing at this level",
        }
    
    @listen("provide_additional_training")
    def offer_training_resources(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide additional training resources for struggling users.
        
        Args:
            state: Current flow state
            
        Returns:
            Training resources and guidance
        """
        # Create task for personalized training recommendations
        training_task = Task(
            description=f"""
            Based on the user's recent performance in deepfake detection challenges,
            provide personalized training recommendations and resources.
            
            Recent Performance:
            {self._format_performance_history()}
            
            Provide:
            1. Specific areas where the user needs improvement
            2. Training exercises or resources
            3. Tips for better detection
            4. Encouragement and motivation
            
            Be supportive and constructive in your recommendations.
            """,
            expected_output="""
            A JSON object with:
            - improvement_areas: list of specific areas to work on
            - training_resources: list of recommended resources
            - tips: practical tips for better detection
            - encouragement: motivational message
            """,
            agent=self.ethics_mentor,
        )
        
        training_crew = Crew(
            agents=[self.ethics_mentor, self.deepfake_analyst],
            tasks=[training_task],
            verbose=True,
        )
        
        result = training_crew.kickoff()
        
        return {
            "status": "training_provided",
            "training_data": self._parse_training_result(result),
        }
    
    def _parse_challenge_result(
        self, 
        result: Any, 
        request: DeepfakeChallengeRequest
    ) -> Dict[str, Any]:
        """Parse crew result into structured challenge data."""
        # In a real implementation, this would parse the LLM output
        # For now, create a structured response
        challenge_id = str(uuid.uuid4())
        
        return {
            "challenge_id": challenge_id,
            "media_url": f"/media/deepfake_challenge_{challenge_id}",
            "media_type": request.media_type or MediaType.VIDEO,
            "is_deepfake": True,  # This would come from the agent's decision
            "difficulty_level": request.difficulty_level,
            "instructions": self._get_instructions(request.locale),
            "hints": self._get_hints(request.difficulty_level, request.locale),
            "detection_clues": [],  # Populated by agent
        }
    
    def _parse_feedback_result(
        self,
        result: Any,
        is_correct: bool,
        submission: DeepfakeSubmissionRequest
    ) -> Dict[str, Any]:
        """Parse crew result into structured feedback data."""
        # Calculate score based on correctness and confidence
        base_score = 100 if is_correct else 0
        confidence_bonus = submission.confidence * 20 if is_correct else 0
        score = min(base_score + confidence_bonus, 100)
        
        return {
            "correct": is_correct,
            "actual_answer": self.current_challenge["is_deepfake"],
            "feedback": str(result),
            "detection_clues": self.current_challenge.get("detection_clues", []),
            "score": score,
            "technical_explanation": "Detailed technical analysis would be here",
            "learning_points": ["Key learning point 1", "Key learning point 2"],
            "next_steps": ["Practice with similar examples", "Focus on audio artifacts"],
        }
    
    def _parse_training_result(self, result: Any) -> Dict[str, Any]:
        """Parse training recommendations from crew result."""
        return {
            "improvement_areas": ["Audio analysis", "Visual artifacts detection"],
            "training_resources": ["Resource 1", "Resource 2"],
            "tips": ["Tip 1", "Tip 2"],
            "encouragement": str(result),
        }
    
    def _update_performance_history(
        self,
        submission: DeepfakeSubmissionRequest,
        feedback: Dict[str, Any]
    ):
        """Update user performance history."""
        self.user_performance_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "challenge_id": submission.challenge_id,
            "correct": feedback["correct"],
            "score": feedback["score"],
            "confidence": submission.confidence,
            "difficulty": self.current_challenge["difficulty_level"],
        })
    
    def _format_performance_history(self) -> str:
        """Format performance history for agent context."""
        if not self.user_performance_history:
            return "No performance history available"
        
        history_str = "Recent Performance:\n"
        for entry in self.user_performance_history[-5:]:
            history_str += f"- Score: {entry['score']}, Difficulty: {entry['difficulty']}\n"
        
        return history_str
    
    def _get_instructions(self, locale: str) -> str:
        """Get challenge instructions in the appropriate language."""
        instructions = {
            "en": "Analyze the media content and determine if it's a deepfake. Look for inconsistencies, artifacts, and unnatural patterns.",
            "pt": "Analise o conteúdo de mídia e determine se é um deepfake. Procure por inconsistências, artefatos e padrões não naturais.",
        }
        return instructions.get(locale, instructions["en"])
    
    def _get_hints(self, difficulty: int, locale: str) -> list:
        """Get hints based on difficulty level."""
        if difficulty <= 2:
            hints_en = [
                "Pay attention to facial movements",
                "Listen for audio inconsistencies",
                "Look at the background for artifacts",
            ]
            hints_pt = [
                "Preste atenção aos movimentos faciais",
                "Ouça inconsistências no áudio",
                "Observe o fundo em busca de artefatos",
            ]
            return hints_pt if locale == "pt" else hints_en
        
        return []  # Fewer hints for higher difficulty
