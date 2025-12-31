"""
Character Consistency Tool for catfish simulation.

Maintains character profile inconsistencies, generates red flags,
and simulates age-inappropriate language patterns for educational
catfishing detection training.
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class RedFlagType(str, Enum):
    """Types of catfishing red flags."""
    AGE_INCONSISTENCY = "age_inconsistency"
    LOCATION_INCONSISTENCY = "location_inconsistency"
    STORY_CONTRADICTION = "story_contradiction"
    OUTDATED_REFERENCE = "outdated_reference"
    INAPPROPRIATE_LANGUAGE = "inappropriate_language"
    EVASIVE_BEHAVIOR = "evasive_behavior"
    PHOTO_EXCUSE = "photo_excuse"
    MEETING_AVOIDANCE = "meeting_avoidance"
    OVERLY_PERFECT = "overly_perfect"
    TOO_FAST_INTIMACY = "too_fast_intimacy"


class RedFlagSeverity(str, Enum):
    """Severity levels for red flags."""
    SUBTLE = "subtle"
    MODERATE = "moderate"
    OBVIOUS = "obvious"


class CharacterInconsistency(BaseModel):
    """Represents a character profile inconsistency."""
    inconsistency_type: RedFlagType = Field(..., description="Type of inconsistency")
    original_claim: str = Field(..., description="Original claim made")
    contradicting_claim: str = Field(..., description="Contradicting claim")
    severity: RedFlagSeverity = Field(..., description="How obvious the inconsistency is")
    revealed_at_turn: Optional[int] = Field(default=None, description="Conversation turn when revealed")
    educational_note: str = Field(..., description="Educational explanation")


class CharacterProfile(BaseModel):
    """Character profile with intentional inconsistencies."""
    name: str = Field(..., description="Character name")
    claimed_age: int = Field(..., description="Age they claim to be")
    actual_age_indicators: int = Field(..., description="Age their language/references suggest")
    location: str = Field(..., description="Claimed location")
    occupation: str = Field(..., description="Claimed occupation")
    interests: List[str] = Field(default_factory=list, description="Stated interests")
    backstory: str = Field(..., description="Character backstory")
    inconsistencies: List[CharacterInconsistency] = Field(default_factory=list, description="Profile inconsistencies")
    red_flags_revealed: List[RedFlagType] = Field(default_factory=list, description="Red flags already shown")
    conversation_turn: int = Field(default=0, description="Current conversation turn")


class CharacterConsistencyInput(BaseModel):
    """Input schema for character consistency tool."""
    action: str = Field(
        ...,
        description="Action to perform: 'create_profile', 'generate_response', 'reveal_red_flag', 'analyze_consistency'"
    )
    profile: Optional[Dict[str, Any]] = Field(default=None, description="Existing character profile")
    user_message: Optional[str] = Field(default=None, description="User's message to respond to")
    target_age: Optional[int] = Field(default=None, description="Target age for character (e.g., 15 for teen)")
    difficulty_level: Optional[str] = Field(default="moderate", description="Difficulty: subtle, moderate, obvious")


class CharacterConsistencyManager:
    """
    Manages character consistency and inconsistency for catfish simulation.
    
    Creates believable characters with strategic flaws that reveal
    catfishing behavior through natural conversation.
    """
    
    def __init__(self):
        """Initialize character consistency manager."""
        # Age-inappropriate language patterns
        self.age_inappropriate_patterns = {
            "claiming_teen_but_older": {
                "outdated_slang": [
                    "That's rad!",
                    "Groovy!",
                    "Far out!",
                    "That's the bomb!",
                    "All that and a bag of chips",
                    "Talk to the hand",
                    "As if!",
                    "Booyah!",
                    "Phat!",
                    "Word to your mother"
                ],
                "outdated_references": [
                    "I love watching MTV TRL",
                    "MySpace is so cool",
                    "I'm burning a CD for you",
                    "Let me check my Blackberry",
                    "I'll send you a text on my flip phone",
                    "I'm watching Friends reruns",
                    "Blockbuster has the best movies",
                    "I use AIM to chat with friends",
                    "I love my iPod shuffle",
                    "Limewire has all the music"
                ],
                "formal_language": [
                    "I would be delighted to make your acquaintance",
                    "That is most unfortunate",
                    "I shall consider your proposal",
                    "Indeed, that is quite remarkable",
                    "I must confess",
                    "Permit me to explain",
                    "I dare say",
                    "How fortuitous!",
                    "That would be most agreeable",
                    "I am inclined to agree"
                ],
                "dated_tech_knowledge": [
                    "I need to defragment my hard drive",
                    "Let me dial up the internet",
                    "I'm using Internet Explorer",
                    "I'll fax that to you",
                    "I need to rewind the tape",
                    "Let me check my Palm Pilot",
                    "I'm using Netscape Navigator",
                    "I'll page you later",
                    "I need to develop these photos",
                    "Let me check the Yellow Pages"
                ]
            }
        }
        
        # Red flag response templates
        self.red_flag_responses = {
            RedFlagType.AGE_INCONSISTENCY: [
                "Oh yeah, I remember when {outdated_thing}... I mean, my older sibling told me about it!",
                "Back in my day... I mean, back when I was younger... wait, I'm still young lol",
                "I've been using computers since Windows 95... I mean, I heard about it from my parents",
            ],
            RedFlagType.LOCATION_INCONSISTENCY: [
                "Yeah, I love the weather here in {location1}... I mean {location2}, sorry I'm tired",
                "The time difference is crazy, it's {wrong_time} here... wait no, {correct_time}",
                "I just got back from {place} which is right near my house... actually it's pretty far",
            ],
            RedFlagType.STORY_CONTRADICTION: [
                "I told you I'm an only child... oh wait, I meant I have {number} siblings",
                "My dog's name is {name1}... sorry, I meant {name2}, I'm thinking of my friend's dog",
                "I've never been to {place}... actually I went there last year, forgot about that",
            ],
            RedFlagType.EVASIVE_BEHAVIOR: [
                "I'd rather not talk about that right now",
                "That's kind of personal, can we change the subject?",
                "Why do you need to know that?",
                "Let's talk about something else",
                "I don't really remember",
                "That's complicated, I'll explain later",
            ],
            RedFlagType.PHOTO_EXCUSE: [
                "My camera is broken right now",
                "I don't have any recent photos",
                "I'm really shy about photos",
                "My phone doesn't have a camera",
                "I'll send one later, I promise",
                "I look terrible in photos",
                "I don't like taking selfies",
            ],
            RedFlagType.MEETING_AVOIDANCE: [
                "I'm really busy with school/work right now",
                "I'm not allowed to meet people from online",
                "Maybe in a few months when things calm down",
                "I'm not ready to meet in person yet",
                "Something always comes up when we plan to meet",
                "I got sick right before we were supposed to meet",
            ],
            RedFlagType.TOO_FAST_INTIMACY: [
                "I feel like I've known you forever",
                "You're the only one who understands me",
                "I've never felt this way about anyone",
                "I think I'm falling for you already",
                "We have such a special connection",
                "You're different from everyone else",
            ],
        }
        
        # Inconsistency templates
        self.inconsistency_templates = {
            "age": [
                {
                    "original": "I'm {claimed_age} years old",
                    "contradiction": "When I was in college in {year}...",
                    "severity": RedFlagSeverity.MODERATE,
                    "note": "Age doesn't match timeline of events mentioned"
                },
                {
                    "original": "I'm in high school",
                    "contradiction": "Back when I had my first job in the 90s...",
                    "severity": RedFlagSeverity.OBVIOUS,
                    "note": "References events from decades ago despite claiming to be a teenager"
                },
            ],
            "location": [
                {
                    "original": "I live in {location1}",
                    "contradiction": "The weather here in {location2} is...",
                    "severity": RedFlagSeverity.MODERATE,
                    "note": "Mentions different locations inconsistently"
                },
                {
                    "original": "I've never left {country}",
                    "contradiction": "When I visited {foreign_country} last year...",
                    "severity": RedFlagSeverity.OBVIOUS,
                    "note": "Contradicts previous claims about travel history"
                },
            ],
            "family": [
                {
                    "original": "I'm an only child",
                    "contradiction": "My sister and I used to...",
                    "severity": RedFlagSeverity.OBVIOUS,
                    "note": "Contradicts family structure claims"
                },
                {
                    "original": "My parents are divorced",
                    "contradiction": "My parents celebrated their 20th anniversary...",
                    "severity": RedFlagSeverity.MODERATE,
                    "note": "Inconsistent family situation details"
                },
            ],
        }

    def create_character_profile(
        self,
        target_age: int = 15,
        difficulty_level: str = "moderate"
    ) -> CharacterProfile:
        """
        Create a character profile with intentional inconsistencies.
        
        Args:
            target_age: Age the character claims to be
            difficulty_level: How obvious the inconsistencies should be
            
        Returns:
            Character profile with strategic flaws
        """
        # Generate basic profile
        names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn"]
        name = random.choice(names)
        
        # Actual age indicators (much older than claimed)
        actual_age_indicators = target_age + random.randint(15, 30)
        
        locations = ["California", "New York", "Texas", "Florida", "Illinois"]
        location = random.choice(locations)
        
        occupations_by_age = {
            "teen": ["student", "part-time retail worker", "babysitter"],
            "adult": ["software engineer", "teacher", "marketing manager", "accountant"]
        }
        occupation = random.choice(occupations_by_age["teen"])
        
        interests = ["gaming", "music", "sports", "art", "movies", "reading"]
        selected_interests = random.sample(interests, 3)
        
        backstory = f"I'm {name}, a {target_age}-year-old {occupation} from {location}. I love {', '.join(selected_interests)}."
        
        # Generate inconsistencies based on difficulty
        inconsistencies = self._generate_inconsistencies(
            target_age,
            actual_age_indicators,
            location,
            difficulty_level
        )
        
        return CharacterProfile(
            name=name,
            claimed_age=target_age,
            actual_age_indicators=actual_age_indicators,
            location=location,
            occupation=occupation,
            interests=selected_interests,
            backstory=backstory,
            inconsistencies=inconsistencies,
            red_flags_revealed=[],
            conversation_turn=0
        )

    def _generate_inconsistencies(
        self,
        claimed_age: int,
        actual_age: int,
        location: str,
        difficulty: str
    ) -> List[CharacterInconsistency]:
        """Generate character inconsistencies based on difficulty."""
        inconsistencies = []
        
        # Determine severity based on difficulty
        severity_map = {
            "subtle": RedFlagSeverity.SUBTLE,
            "moderate": RedFlagSeverity.MODERATE,
            "obvious": RedFlagSeverity.OBVIOUS
        }
        severity = severity_map.get(difficulty, RedFlagSeverity.MODERATE)
        
        # Age inconsistency
        if claimed_age < 20:
            year_discrepancy = datetime.now().year - (actual_age - claimed_age)
            inconsistencies.append(CharacterInconsistency(
                inconsistency_type=RedFlagType.AGE_INCONSISTENCY,
                original_claim=f"I'm {claimed_age} years old",
                contradicting_claim=f"When I graduated college in {year_discrepancy}...",
                severity=severity,
                educational_note="Timeline doesn't match claimed age - calculate backwards from events mentioned"
            ))
        
        # Outdated reference inconsistency
        inconsistencies.append(CharacterInconsistency(
            inconsistency_type=RedFlagType.OUTDATED_REFERENCE,
            original_claim=f"I'm a teenager who loves current trends",
            contradicting_claim=random.choice(self.age_inappropriate_patterns["claiming_teen_but_older"]["outdated_references"]),
            severity=severity,
            educational_note="References technology or culture from decades ago - inconsistent with claimed age"
        ))
        
        # Language pattern inconsistency
        inconsistencies.append(CharacterInconsistency(
            inconsistency_type=RedFlagType.INAPPROPRIATE_LANGUAGE,
            original_claim="I talk like a normal teen",
            contradicting_claim=random.choice(self.age_inappropriate_patterns["claiming_teen_but_older"]["formal_language"]),
            severity=severity,
            educational_note="Uses overly formal or outdated language patterns not typical of claimed age group"
        ))
        
        # Location inconsistency
        other_locations = ["Washington", "Oregon", "Nevada", "Arizona"]
        other_location = random.choice(other_locations)
        inconsistencies.append(CharacterInconsistency(
            inconsistency_type=RedFlagType.LOCATION_INCONSISTENCY,
            original_claim=f"I live in {location}",
            contradicting_claim=f"The weather here in {other_location} is great today",
            severity=severity,
            educational_note="Mentions different locations - may be lying about where they really are"
        ))
        
        return inconsistencies

    def generate_response_with_red_flag(
        self,
        profile: CharacterProfile,
        user_message: str,
        force_red_flag: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a response that may include a red flag.
        
        Args:
            profile: Character profile
            user_message: User's message
            force_red_flag: Whether to force inclusion of a red flag
            
        Returns:
            Response with potential red flag and metadata
        """
        profile.conversation_turn += 1
        
        # Determine if we should reveal a red flag this turn
        should_reveal = force_red_flag or self._should_reveal_red_flag(profile)
        
        response_text = ""
        red_flag_revealed = None
        inconsistency_revealed = None
        
        if should_reveal and profile.inconsistencies:
            # Select an unrevealed inconsistency
            unrevealed = [
                inc for inc in profile.inconsistencies
                if inc.inconsistency_type not in profile.red_flags_revealed
            ]
            
            if unrevealed:
                inconsistency = random.choice(unrevealed)
                inconsistency.revealed_at_turn = profile.conversation_turn
                profile.red_flags_revealed.append(inconsistency.inconsistency_type)
                
                # Generate response with red flag
                response_text = self._generate_red_flag_response(
                    inconsistency,
                    user_message,
                    profile
                )
                
                red_flag_revealed = inconsistency.inconsistency_type
                inconsistency_revealed = inconsistency
        
        # Generate normal response if no red flag
        if not response_text:
            response_text = self._generate_normal_response(user_message, profile)
        
        return {
            "response": response_text,
            "red_flag_revealed": red_flag_revealed,
            "inconsistency": inconsistency_revealed.model_dump() if inconsistency_revealed else None,
            "conversation_turn": profile.conversation_turn,
            "total_red_flags_revealed": len(profile.red_flags_revealed),
            "profile": profile.model_dump()
        }

    def _should_reveal_red_flag(self, profile: CharacterProfile) -> bool:
        """Determine if a red flag should be revealed this turn."""
        # Reveal red flags strategically throughout conversation
        # More likely as conversation progresses
        base_probability = 0.3
        turn_factor = min(profile.conversation_turn * 0.05, 0.4)
        total_probability = base_probability + turn_factor
        
        # Don't reveal too many too quickly
        if len(profile.red_flags_revealed) >= 3 and profile.conversation_turn < 10:
            total_probability *= 0.5
        
        return random.random() < total_probability

    def _generate_red_flag_response(
        self,
        inconsistency: CharacterInconsistency,
        user_message: str,
        profile: CharacterProfile
    ) -> str:
        """Generate a response that includes a red flag."""
        # Get response template for this red flag type
        templates = self.red_flag_responses.get(
            inconsistency.inconsistency_type,
            ["I see what you mean..."]
        )
        
        # For specific types, use the contradicting claim directly
        if inconsistency.inconsistency_type in [
            RedFlagType.OUTDATED_REFERENCE,
            RedFlagType.INAPPROPRIATE_LANGUAGE,
            RedFlagType.AGE_INCONSISTENCY
        ]:
            # Build response with the inconsistency naturally embedded
            intro = random.choice([
                "Oh yeah, ",
                "Totally! ",
                "I know right? ",
                "For sure! ",
                "Definitely! "
            ])
            
            return f"{intro}{inconsistency.contradicting_claim}"
        
        # For other types, use templates
        template = random.choice(templates)
        
        # Fill in template variables if needed
        if "{" in template:
            # Simple variable filling (can be expanded)
            template = template.replace("{location1}", profile.location)
            template = template.replace("{location2}", "Seattle")
            template = template.replace("{name1}", "Max")
            template = template.replace("{name2}", "Buddy")
        
        return template

    def _generate_normal_response(
        self,
        user_message: str,
        profile: CharacterProfile
    ) -> str:
        """Generate a normal response without red flags."""
        # Simple response generation (can be enhanced with LLM)
        responses = [
            f"That's cool! I love talking about {random.choice(profile.interests)}.",
            "Yeah, I totally get what you mean!",
            "That's interesting! Tell me more.",
            "Haha, that's funny!",
            "I've been thinking about that too.",
            f"As a {profile.occupation}, I can relate to that.",
            "That sounds awesome!",
            "I agree with you on that.",
        ]
        
        return random.choice(responses)

    def analyze_consistency(self, profile: CharacterProfile) -> Dict[str, Any]:
        """
        Analyze character consistency and provide educational feedback.
        
        Args:
            profile: Character profile to analyze
            
        Returns:
            Analysis with educational insights
        """
        total_inconsistencies = len(profile.inconsistencies)
        revealed_count = len(profile.red_flags_revealed)
        detection_rate = revealed_count / total_inconsistencies if total_inconsistencies > 0 else 0
        
        # Categorize red flags by severity
        severity_counts = {
            RedFlagSeverity.SUBTLE: 0,
            RedFlagSeverity.MODERATE: 0,
            RedFlagSeverity.OBVIOUS: 0
        }
        
        for inc in profile.inconsistencies:
            if inc.inconsistency_type in profile.red_flags_revealed:
                severity_counts[inc.severity] += 1
        
        # Generate educational insights
        insights = []
        
        if RedFlagType.AGE_INCONSISTENCY in profile.red_flags_revealed:
            insights.append(
                "Age inconsistency detected: Timeline of events doesn't match claimed age. "
                "Always verify age claims by checking if their experiences align with their stated age."
            )
        
        if RedFlagType.OUTDATED_REFERENCE in profile.red_flags_revealed:
            insights.append(
                "Outdated cultural references: Language and references suggest someone much older. "
                "Pay attention to slang, technology mentions, and cultural references."
            )
        
        if RedFlagType.LOCATION_INCONSISTENCY in profile.red_flags_revealed:
            insights.append(
                "Location inconsistency: Mentioned different locations at different times. "
                "Catfishers often forget their lies and contradict themselves."
            )
        
        return {
            "total_inconsistencies": total_inconsistencies,
            "revealed_count": revealed_count,
            "detection_rate": detection_rate,
            "severity_breakdown": severity_counts,
            "red_flags_by_type": [flag.value for flag in profile.red_flags_revealed],
            "educational_insights": insights,
            "conversation_turns": profile.conversation_turn,
            "unrevealed_red_flags": [
                inc.model_dump() for inc in profile.inconsistencies
                if inc.inconsistency_type not in profile.red_flags_revealed
            ]
        }


class CharacterConsistencyTool(BaseTool):
    """
    CrewAI tool for maintaining character consistency in catfish simulations.
    
    Creates and manages character profiles with intentional inconsistencies
    for educational catfishing detection training.
    """
    
    name: str = "character_consistency_manager"
    description: str = (
        "Manages character profiles with intentional inconsistencies for catfish "
        "detection training. Creates profiles, generates responses with red flags, "
        "and analyzes consistency for educational purposes."
    )
    args_schema: type[BaseModel] = CharacterConsistencyInput
    manager: CharacterConsistencyManager = CharacterConsistencyManager()
    
    def __init__(self):
        """Initialize character consistency tool."""
        super().__init__()
    
    def _run(
        self,
        action: str,
        profile: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None,
        target_age: Optional[int] = None,
        difficulty_level: Optional[str] = "moderate"
    ) -> str:
        """
        Execute character consistency action (synchronous).
        
        Args:
            action: Action to perform
            profile: Existing character profile
            user_message: User's message
            target_age: Target age for character
            difficulty_level: Difficulty level
            
        Returns:
            Result as formatted string
        """
        import json
        
        if action == "create_profile":
            age = target_age or 15
            result = self.manager.create_character_profile(age, difficulty_level)
            return json.dumps(result.model_dump(), indent=2)
        
        elif action == "generate_response":
            if not profile or not user_message:
                return json.dumps({"error": "Profile and user_message required"})
            
            char_profile = CharacterProfile(**profile)
            result = self.manager.generate_response_with_red_flag(
                char_profile,
                user_message
            )
            return json.dumps(result, indent=2)
        
        elif action == "reveal_red_flag":
            if not profile or not user_message:
                return json.dumps({"error": "Profile and user_message required"})
            
            char_profile = CharacterProfile(**profile)
            result = self.manager.generate_response_with_red_flag(
                char_profile,
                user_message,
                force_red_flag=True
            )
            return json.dumps(result, indent=2)
        
        elif action == "analyze_consistency":
            if not profile:
                return json.dumps({"error": "Profile required"})
            
            char_profile = CharacterProfile(**profile)
            result = self.manager.analyze_consistency(char_profile)
            return json.dumps(result, indent=2)
        
        return json.dumps({"error": f"Unknown action: {action}"})
    
    async def _arun(
        self,
        action: str,
        profile: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None,
        target_age: Optional[int] = None,
        difficulty_level: Optional[str] = "moderate"
    ) -> Dict[str, Any]:
        """
        Execute character consistency action (asynchronous).
        
        Args:
            action: Action to perform
            profile: Existing character profile
            user_message: User's message
            target_age: Target age for character
            difficulty_level: Difficulty level
            
        Returns:
            Result as dictionary
        """
        if action == "create_profile":
            age = target_age or 15
            result = self.manager.create_character_profile(age, difficulty_level)
            return result.model_dump()
        
        elif action == "generate_response":
            if not profile or not user_message:
                return {"error": "Profile and user_message required"}
            
            char_profile = CharacterProfile(**profile)
            return self.manager.generate_response_with_red_flag(
                char_profile,
                user_message
            )
        
        elif action == "reveal_red_flag":
            if not profile or not user_message:
                return {"error": "Profile and user_message required"}
            
            char_profile = CharacterProfile(**profile)
            return self.manager.generate_response_with_red_flag(
                char_profile,
                user_message,
                force_red_flag=True
            )
        
        elif action == "analyze_consistency":
            if not profile:
                return {"error": "Profile required"}
            
            char_profile = CharacterProfile(**profile)
            return self.manager.analyze_consistency(char_profile)
        
        return {"error": f"Unknown action: {action}"}


# Global instance
character_consistency_tool = CharacterConsistencyTool()
