"""
Deepfake Analyst Agent - Analyzes media content and provides detection training.
"""

from typing import Dict, List, Optional, Any
from crewai import Agent, Task

from .base import BaseEducationalAgent


class DeepfakeAnalystAgent(BaseEducationalAgent):
    """
    Specialized agent for deepfake detection training and media analysis.
    Provides technical explanations and progressive difficulty adjustment.
    """
    
    def __init__(self, agent: Agent):
        """
        Initialize Deepfake Analyst Agent.
        
        Args:
            agent: CrewAI Agent instance configured for deepfake analysis
        """
        super().__init__(agent)
        self.difficulty_levels = {
            1: {"name": "beginner", "clue_visibility": "obvious"},
            2: {"name": "intermediate", "clue_visibility": "moderate"},
            3: {"name": "advanced", "clue_visibility": "subtle"}
        }
    
    def analyze_media_submission(
        self,
        media_url: str,
        media_type: str,
        user_decision: str,
        actual_authenticity: str,
        difficulty_level: int = 1
    ) -> Dict[str, Any]:
        """
        Analyze user's deepfake detection decision and provide feedback.
        
        Args:
            media_url: URL or path to the media file
            media_type: Type of media ('audio', 'video', 'image')
            user_decision: User's decision ('authentic' or 'deepfake')
            actual_authenticity: Actual status of the media
            difficulty_level: Current difficulty level (1-3)
            
        Returns:
            Detailed analysis with detection clues and feedback
        """
        is_correct = user_decision == actual_authenticity
        
        # Get detection clues based on difficulty
        detection_clues = self._get_detection_clues(
            media_type,
            actual_authenticity,
            difficulty_level
        )
        
        # Generate technical explanation
        technical_explanation = self._generate_technical_explanation(
            media_type,
            actual_authenticity,
            detection_clues
        )
        
        # Create analysis task for the agent
        task_description = f"""
        Provide educational feedback on deepfake detection.
        
        Media type: {media_type}
        User's decision: {user_decision}
        Actual status: {actual_authenticity}
        Correct: {is_correct}
        Difficulty: {self.difficulty_levels[difficulty_level]['name']}
        
        Generate feedback that:
        1. Confirms or corrects the user's decision
        2. Highlights specific detection clues
        3. Explains technical indicators
        4. Provides learning tips for future detection
        5. Responds in {'Portuguese' if self.locale == 'pt' else 'English'}
        """
        
        analysis = {
            "is_correct": is_correct,
            "detection_clues": detection_clues,
            "technical_explanation": technical_explanation,
            "learning_tips": self._generate_learning_tips(media_type, is_correct),
            "confidence_indicators": self._identify_confidence_indicators(detection_clues),
            "next_difficulty": self._calculate_next_difficulty(is_correct, difficulty_level)
        }
        
        # Update memory with performance
        self.memory.update_user_context({
            "last_detection_correct": is_correct,
            "current_difficulty": difficulty_level,
            "media_type": media_type
        })
        
        return analysis
    
    def _get_detection_clues(
        self,
        media_type: str,
        authenticity: str,
        difficulty_level: int
    ) -> List[Dict[str, str]]:
        """
        Get detection clues based on media type and difficulty.
        
        Args:
            media_type: Type of media
            authenticity: Whether media is authentic or deepfake
            difficulty_level: Current difficulty level
            
        Returns:
            List of detection clues with descriptions
        """
        clues = []
        
        if authenticity == "deepfake":
            if media_type == "video":
                clues = [
                    {
                        "type": "visual",
                        "indicator": "facial_inconsistency",
                        "description": "Unnatural facial movements or expressions",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    },
                    {
                        "type": "visual",
                        "indicator": "lighting_mismatch",
                        "description": "Inconsistent lighting on face vs. background",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    },
                    {
                        "type": "temporal",
                        "indicator": "frame_artifacts",
                        "description": "Glitches or artifacts between frames",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    }
                ]
            elif media_type == "audio":
                clues = [
                    {
                        "type": "audio",
                        "indicator": "unnatural_prosody",
                        "description": "Robotic or unnatural speech patterns",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    },
                    {
                        "type": "audio",
                        "indicator": "background_inconsistency",
                        "description": "Inconsistent background noise",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    }
                ]
            elif media_type == "image":
                clues = [
                    {
                        "type": "visual",
                        "indicator": "edge_artifacts",
                        "description": "Blurring or artifacts around edges",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    },
                    {
                        "type": "visual",
                        "indicator": "texture_inconsistency",
                        "description": "Unnatural skin texture or details",
                        "visibility": self.difficulty_levels[difficulty_level]["clue_visibility"]
                    }
                ]
        else:
            # Authentic media - explain why it's authentic
            clues = [
                {
                    "type": "authenticity",
                    "indicator": "natural_consistency",
                    "description": "Consistent natural patterns throughout",
                    "visibility": "clear"
                }
            ]
        
        return clues
    
    def _generate_technical_explanation(
        self,
        media_type: str,
        authenticity: str,
        clues: List[Dict[str, str]]
    ) -> str:
        """Generate technical explanation of detection indicators."""
        if authenticity == "deepfake":
            explanation = f"This {media_type} shows signs of AI-generated manipulation. "
            explanation += "Key technical indicators include: "
            explanation += ", ".join([clue["indicator"].replace("_", " ") for clue in clues])
        else:
            explanation = f"This {media_type} appears to be authentic. "
            explanation += "It shows natural consistency in all analyzed aspects."
        
        return explanation
    
    def _generate_learning_tips(self, media_type: str, was_correct: bool) -> List[str]:
        """Generate learning tips based on performance."""
        tips = []
        
        if was_correct:
            tips.append("Great job! Continue to look for these types of indicators.")
            tips.append(f"Try analyzing {media_type} content from different sources to build your skills.")
        else:
            tips.append("Don't worry - deepfake detection takes practice!")
            tips.append(f"Focus on these key areas when analyzing {media_type}: consistency, naturalness, and artifacts.")
            tips.append("Try pausing and examining the content frame-by-frame or section-by-section.")
        
        return tips
    
    def _identify_confidence_indicators(self, clues: List[Dict[str, str]]) -> Dict[str, Any]:
        """Identify indicators of detection confidence."""
        return {
            "number_of_clues": len(clues),
            "clue_strength": "strong" if len(clues) >= 3 else "moderate",
            "recommendation": "High confidence" if len(clues) >= 3 else "Moderate confidence"
        }
    
    def _calculate_next_difficulty(self, was_correct: bool, current_level: int) -> int:
        """Calculate next difficulty level based on performance."""
        if was_correct and current_level < 3:
            return current_level + 1
        elif not was_correct and current_level > 1:
            return current_level - 1
        return current_level
    
    def generate_challenge(
        self,
        difficulty_level: int,
        media_type: str,
        user_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a new deepfake detection challenge.
        
        Args:
            difficulty_level: Desired difficulty level (1-3)
            media_type: Type of media for the challenge
            user_history: User's previous challenge history
            
        Returns:
            Challenge configuration with media and metadata
        """
        # Analyze user's weak areas from history
        weak_areas = self._identify_weak_areas(user_history) if user_history else []
        
        challenge = {
            "challenge_id": f"deepfake_{media_type}_{difficulty_level}",
            "media_type": media_type,
            "difficulty_level": difficulty_level,
            "difficulty_name": self.difficulty_levels[difficulty_level]["name"],
            "focus_areas": weak_areas or ["general_detection"],
            "time_limit": 60 * difficulty_level,  # seconds
            "hints_available": 3 - difficulty_level,  # fewer hints at higher levels
            "educational_context": self._get_educational_context(media_type, difficulty_level)
        }
        
        return challenge
    
    def _identify_weak_areas(self, user_history: List[Dict[str, Any]]) -> List[str]:
        """Identify areas where user needs more practice."""
        weak_areas = []
        
        # Analyze performance by media type
        media_performance = {}
        for entry in user_history:
            media_type = entry.get("media_type")
            correct = entry.get("correct", False)
            
            if media_type not in media_performance:
                media_performance[media_type] = {"correct": 0, "total": 0}
            
            media_performance[media_type]["total"] += 1
            if correct:
                media_performance[media_type]["correct"] += 1
        
        # Identify weak media types
        for media_type, stats in media_performance.items():
            accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
            if accuracy < 0.6:
                weak_areas.append(f"{media_type}_detection")
        
        return weak_areas
    
    def _get_educational_context(self, media_type: str, difficulty_level: int) -> str:
        """Get educational context for the challenge."""
        contexts = {
            "video": "Focus on facial movements, lighting consistency, and temporal artifacts.",
            "audio": "Listen for unnatural speech patterns, background inconsistencies, and prosody.",
            "image": "Look for edge artifacts, texture inconsistencies, and lighting mismatches."
        }
        
        context = contexts.get(media_type, "Analyze carefully for signs of manipulation.")
        
        if difficulty_level == 3:
            context += " This is an advanced challenge - the indicators will be subtle."
        
        return context
