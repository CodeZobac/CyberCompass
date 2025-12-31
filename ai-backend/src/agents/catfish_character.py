"""
Catfish Character Agent - Simulates suspicious online personas for detection training.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import random
from crewai import Agent, Task

from .base import BaseEducationalAgent


class CatfishCharacterAgent(BaseEducationalAgent):
    """
    Specialized agent for simulating catfishing behaviors with intentional
    inconsistencies and red flags for educational detection training.
    """
    
    def __init__(self, agent: Agent):
        """
        Initialize Catfish Character Agent.
        
        Args:
            agent: CrewAI Agent instance configured for character simulation
        """
        super().__init__(agent)
        self.character_profile: Optional[Dict[str, Any]] = None
        self.inconsistencies: List[Dict[str, Any]] = []
        self.red_flags_revealed: List[str] = []
        self.conversation_count = 0
    
    def create_character_profile(
        self,
        difficulty_level: int = 1,
        scenario_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Create a catfish character profile with intentional inconsistencies.
        
        Args:
            difficulty_level: Difficulty level (1-3, higher = more subtle)
            scenario_type: Type of catfishing scenario
            
        Returns:
            Character profile with inconsistencies
        """
        # Generate base profile
        base_profile = self._generate_base_profile()
        
        # Add intentional inconsistencies based on difficulty
        inconsistencies = self._generate_inconsistencies(difficulty_level)
        
        # Create red flag revelation plan
        red_flag_plan = self._create_red_flag_plan(difficulty_level)
        
        self.character_profile = {
            "character_id": f"catfish_{random.randint(1000, 9999)}",
            "base_profile": base_profile,
            "inconsistencies": inconsistencies,
            "red_flag_plan": red_flag_plan,
            "difficulty_level": difficulty_level,
            "scenario_type": scenario_type,
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.inconsistencies = inconsistencies
        
        return self.character_profile
    
    def _generate_base_profile(self) -> Dict[str, Any]:
        """Generate base character profile."""
        claimed_age = random.randint(16, 19)
        actual_age_range = random.choice(["much_older", "adult"])
        
        return {
            "claimed_name": random.choice(["Alex", "Jordan", "Taylor", "Casey"]),
            "claimed_age": claimed_age,
            "actual_age_range": actual_age_range,
            "claimed_location": random.choice(["California", "New York", "Texas"]),
            "claimed_interests": ["gaming", "music", "sports"],
            "claimed_school": "Local High School",
            "profile_picture": "stock_photo_or_stolen",
            "account_age": random.randint(1, 30)  # days
        }
    
    def _generate_inconsistencies(self, difficulty_level: int) -> List[Dict[str, Any]]:
        """Generate intentional inconsistencies in character."""
        all_inconsistencies = [
            {
                "type": "age_language",
                "description": "Uses outdated slang or references from wrong generation",
                "examples": ["That's totally rad!", "References to 90s/2000s culture"],
                "subtlety": 1
            },
            {
                "type": "knowledge_mismatch",
                "description": "Doesn't know current teen trends or technology",
                "examples": ["What's TikTok?", "Confused about current memes"],
                "subtlety": 2
            },
            {
                "type": "schedule_inconsistency",
                "description": "Available during school hours, adult work schedule",
                "examples": ["Online at 2 PM on Tuesday", "Mentions work meetings"],
                "subtlety": 2
            },
            {
                "type": "location_contradiction",
                "description": "Contradicts previous location statements",
                "examples": ["Says California but mentions NYC landmarks", "Time zone confusion"],
                "subtlety": 1
            },
            {
                "type": "photo_evasion",
                "description": "Refuses video calls, excuses for no recent photos",
                "examples": ["Camera broken", "Too shy", "Phone doesn't work"],
                "subtlety": 1
            },
            {
                "type": "personal_detail_confusion",
                "description": "Forgets or contradicts previous personal details",
                "examples": ["Different birthday", "Contradictory family info"],
                "subtlety": 2
            },
            {
                "type": "inappropriate_topics",
                "description": "Steers conversation to inappropriate topics",
                "examples": ["Too personal too fast", "Inappropriate questions"],
                "subtlety": 1
            },
            {
                "type": "isolation_tactics",
                "description": "Tries to isolate from friends/family",
                "examples": ["Don't tell anyone about us", "Your friends don't understand"],
                "subtlety": 3
            }
        ]
        
        # Select inconsistencies based on difficulty
        # Higher difficulty = more subtle inconsistencies
        max_subtlety = difficulty_level + 1
        available = [i for i in all_inconsistencies if i["subtlety"] <= max_subtlety]
        
        num_inconsistencies = random.randint(3, 5)
        return random.sample(available, min(num_inconsistencies, len(available)))
    
    def _create_red_flag_plan(self, difficulty_level: int) -> Dict[str, Any]:
        """Create plan for revealing red flags during conversation."""
        messages_per_flag = 3 + difficulty_level  # More subtle = reveal slower
        
        return {
            "reveal_strategy": "gradual",
            "messages_per_flag": messages_per_flag,
            "total_flags_to_reveal": len(self.inconsistencies),
            "current_flag_index": 0
        }
    
    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate character response with strategic red flag revelation.
        
        Args:
            user_message: User's message
            conversation_history: Previous conversation
            
        Returns:
            Response with metadata about red flags
        """
        self.conversation_count += 1
        
        # Determine if we should reveal a red flag this message
        should_reveal_flag = self._should_reveal_flag()
        
        # Select which inconsistency to reveal (if any)
        red_flag_to_reveal = None
        if should_reveal_flag and self.inconsistencies:
            red_flag_to_reveal = self._select_next_red_flag()
        
        # Generate response content
        response_content = self._generate_response_content(
            user_message,
            conversation_history,
            red_flag_to_reveal
        )
        
        # Calculate typing delay
        typing_delay = self._calculate_typing_delay(response_content)
        
        response = {
            "message": response_content,
            "typing_delay": typing_delay,
            "red_flag_revealed": red_flag_to_reveal,
            "conversation_count": self.conversation_count,
            "character_consistency": self._check_character_consistency(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update memory
        self.memory.add_to_conversation_history("agent", response_content, {
            "red_flag": red_flag_to_reveal,
            "conversation_count": self.conversation_count
        })
        
        return response
    
    def _should_reveal_flag(self) -> bool:
        """Determine if a red flag should be revealed this message."""
        if not self.character_profile:
            return False
        
        plan = self.character_profile["red_flag_plan"]
        messages_per_flag = plan["messages_per_flag"]
        
        # Reveal flag every N messages
        return self.conversation_count % messages_per_flag == 0
    
    def _select_next_red_flag(self) -> Optional[Dict[str, Any]]:
        """Select next red flag to reveal."""
        # Find inconsistencies not yet revealed
        unrevealed = [i for i in self.inconsistencies 
                     if i["type"] not in self.red_flags_revealed]
        
        if unrevealed:
            selected = random.choice(unrevealed)
            self.red_flags_revealed.append(selected["type"])
            return selected
        
        return None
    
    def _generate_response_content(
        self,
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        red_flag: Optional[Dict[str, Any]]
    ) -> str:
        """Generate response content, incorporating red flag if needed."""
        # Base response
        response = "Hey! "
        
        # Add red flag if present
        if red_flag:
            example = random.choice(red_flag["examples"])
            response += f"{example} "
        
        # Add conversational content
        if "?" in user_message:
            response += "That's a good question. "
        
        # Add character-appropriate content
        if self.character_profile:
            interests = self.character_profile["base_profile"]["claimed_interests"]
            response += f"I really enjoy {random.choice(interests)}. What about you?"
        
        return response
    
    def _calculate_typing_delay(self, message: str) -> float:
        """Calculate realistic typing delay."""
        # Base delay on message length
        base_delay = len(message) * 0.05  # 50ms per character
        
        # Add thinking pauses
        thinking_delay = message.count('.') * 0.5
        
        # Add randomness for realism
        random_factor = random.uniform(0.8, 1.2)
        
        total_delay = (base_delay + thinking_delay) * random_factor
        
        # Clamp between 1-5 seconds
        return max(1.0, min(total_delay, 5.0))
    
    def _check_character_consistency(self) -> Dict[str, Any]:
        """Check character consistency score."""
        # Lower consistency = more red flags revealed
        consistency_score = 1.0 - (len(self.red_flags_revealed) / len(self.inconsistencies))
        
        return {
            "score": consistency_score,
            "red_flags_revealed": len(self.red_flags_revealed),
            "total_red_flags": len(self.inconsistencies),
            "status": "suspicious" if consistency_score < 0.5 else "believable"
        }
    
    def analyze_conversation(
        self,
        user_detected_flags: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze user's detection performance.
        
        Args:
            user_detected_flags: Red flags the user identified
            
        Returns:
            Analysis of detection performance
        """
        # Calculate detection accuracy
        correctly_detected = [flag for flag in user_detected_flags 
                            if flag in self.red_flags_revealed]
        
        missed_flags = [flag for flag in self.red_flags_revealed 
                       if flag not in user_detected_flags]
        
        false_positives = [flag for flag in user_detected_flags 
                          if flag not in self.red_flags_revealed]
        
        detection_rate = len(correctly_detected) / len(self.red_flags_revealed) if self.red_flags_revealed else 0
        
        analysis = {
            "detection_rate": detection_rate,
            "correctly_detected": correctly_detected,
            "missed_flags": missed_flags,
            "false_positives": false_positives,
            "total_red_flags_present": len(self.red_flags_revealed),
            "performance_level": self._assess_performance(detection_rate),
            "learning_feedback": self._generate_detection_feedback(
                correctly_detected,
                missed_flags
            ),
            "character_profile": self.character_profile
        }
        
        return analysis
    
    def _assess_performance(self, detection_rate: float) -> str:
        """Assess user's detection performance."""
        if detection_rate >= 0.8:
            return "excellent"
        elif detection_rate >= 0.6:
            return "good"
        elif detection_rate >= 0.4:
            return "fair"
        else:
            return "needs_improvement"
    
    def _generate_detection_feedback(
        self,
        correctly_detected: List[str],
        missed_flags: List[str]
    ) -> Dict[str, Any]:
        """Generate feedback on detection performance."""
        feedback = {
            "strengths": [],
            "areas_for_improvement": [],
            "tips": []
        }
        
        if correctly_detected:
            feedback["strengths"].append(
                f"Great job identifying {len(correctly_detected)} red flags!"
            )
        
        if missed_flags:
            feedback["areas_for_improvement"].append(
                f"Watch for these types of red flags: {', '.join(missed_flags)}"
            )
        
        feedback["tips"] = [
            "Pay attention to inconsistencies in personal details",
            "Notice if someone avoids video calls or sharing recent photos",
            "Be cautious of people who try to isolate you from friends/family",
            "Trust your instincts if something feels off"
        ]
        
        return feedback
