"""
Typing Delay Tool for realistic human-like conversation delays.

Simulates realistic typing delays based on message complexity,
agent personality, and human typing patterns.
"""

import asyncio
import random
from typing import Dict, Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class TypingDelayInput(BaseModel):
    """Input schema for typing delay calculation."""

    message: str = Field(..., description="Message content to analyze")
    personality: str = Field(
        default="normal",
        description="Agent personality type (catfish_suspicious, social_media_bot, ethics_mentor, normal)",
    )
    emotional_state: Optional[str] = Field(
        default=None,
        description="Optional emotional state (excited, hesitant, confident, nervous)",
    )


class TypingDelayCalculator:
    """
    Calculates realistic typing delays based on various factors.
    
    Simulates human typing patterns including:
    - Base typing speed variations
    - Pauses for thinking
    - Personality-based speed adjustments
    - Message complexity analysis
    """

    # Base typing speeds (characters per second)
    TYPING_SPEEDS = {
        "very_slow": 2.0,  # 2 chars/sec (~24 WPM)
        "slow": 3.5,  # 3.5 chars/sec (~42 WPM)
        "normal": 5.0,  # 5 chars/sec (~60 WPM)
        "fast": 7.0,  # 7 chars/sec (~84 WPM)
        "very_fast": 10.0,  # 10 chars/sec (~120 WPM)
    }

    # Personality typing characteristics
    PERSONALITY_PROFILES = {
        "catfish_suspicious": {
            "base_speed": "slow",
            "thinking_pause_multiplier": 2.5,
            "variation": 0.4,
            "description": "Slower, more hesitant typing with frequent pauses",
        },
        "social_media_bot": {
            "base_speed": "very_fast",
            "thinking_pause_multiplier": 0.3,
            "variation": 0.1,
            "description": "Very fast, consistent typing with minimal pauses",
        },
        "ethics_mentor": {
            "base_speed": "normal",
            "thinking_pause_multiplier": 1.2,
            "variation": 0.2,
            "description": "Steady, thoughtful typing with moderate pauses",
        },
        "deepfake_analyst": {
            "base_speed": "normal",
            "thinking_pause_multiplier": 1.5,
            "variation": 0.25,
            "description": "Analytical typing with pauses for technical explanations",
        },
        "normal": {
            "base_speed": "normal",
            "thinking_pause_multiplier": 1.0,
            "variation": 0.3,
            "description": "Average human typing pattern",
        },
    }

    # Emotional state modifiers
    EMOTIONAL_MODIFIERS = {
        "excited": {"speed_multiplier": 1.3, "variation_increase": 0.2},
        "hesitant": {"speed_multiplier": 0.7, "variation_increase": 0.3},
        "confident": {"speed_multiplier": 1.1, "variation_increase": 0.1},
        "nervous": {"speed_multiplier": 0.8, "variation_increase": 0.4},
        "angry": {"speed_multiplier": 1.2, "variation_increase": 0.3},
        "thoughtful": {"speed_multiplier": 0.9, "variation_increase": 0.15},
    }

    def __init__(self):
        """Initialize typing delay calculator."""
        self.min_delay = 0.5  # Minimum delay in seconds
        self.max_delay = 8.0  # Maximum delay in seconds

    def calculate_delay(
        self,
        message: str,
        personality: str = "normal",
        emotional_state: Optional[str] = None,
    ) -> float:
        """
        Calculate realistic typing delay for a message.
        
        Args:
            message: Message content
            personality: Agent personality type
            emotional_state: Optional emotional state
            
        Returns:
            Typing delay in seconds
        """
        # Get personality profile
        profile = self.PERSONALITY_PROFILES.get(personality, self.PERSONALITY_PROFILES["normal"])
        
        # Get base typing speed
        base_speed = self.TYPING_SPEEDS[profile["base_speed"]]
        
        # Calculate base delay from message length
        char_count = len(message)
        base_delay = char_count / base_speed
        
        # Add thinking pauses based on message complexity
        thinking_time = self._calculate_thinking_time(message)
        thinking_time *= profile["thinking_pause_multiplier"]
        
        # Apply personality variation
        variation = profile["variation"]
        variation_factor = random.uniform(1 - variation, 1 + variation)
        
        # Calculate total delay
        total_delay = (base_delay + thinking_time) * variation_factor
        
        # Apply emotional state modifier if present
        if emotional_state and emotional_state in self.EMOTIONAL_MODIFIERS:
            modifier = self.EMOTIONAL_MODIFIERS[emotional_state]
            total_delay *= modifier["speed_multiplier"]
            
            # Add additional variation for emotional states
            extra_variation = modifier["variation_increase"]
            total_delay *= random.uniform(1 - extra_variation, 1 + extra_variation)
        
        # Clamp to reasonable bounds
        total_delay = max(self.min_delay, min(total_delay, self.max_delay))
        
        return round(total_delay, 2)

    def _calculate_thinking_time(self, message: str) -> float:
        """
        Calculate thinking/pause time based on message complexity.
        
        Args:
            message: Message content
            
        Returns:
            Thinking time in seconds
        """
        thinking_time = 0.0
        
        # Sentence breaks (periods, question marks, exclamation points)
        sentence_breaks = message.count('.') + message.count('?') + message.count('!')
        thinking_time += sentence_breaks * 0.3  # 300ms pause per sentence
        
        # Commas (shorter pauses)
        comma_count = message.count(',')
        thinking_time += comma_count * 0.15  # 150ms pause per comma
        
        # Long words (7+ characters) require more thinking
        words = message.split()
        long_words = sum(1 for word in words if len(word) >= 7)
        thinking_time += long_words * 0.2  # 200ms per long word
        
        # Numbers and special characters
        digit_count = sum(1 for char in message if char.isdigit())
        thinking_time += digit_count * 0.1  # 100ms per digit
        
        # Uppercase words (emphasis, requires thought)
        uppercase_words = sum(1 for word in words if word.isupper() and len(word) > 1)
        thinking_time += uppercase_words * 0.25  # 250ms per emphasized word
        
        return thinking_time

    def calculate_chunked_delays(
        self,
        message: str,
        personality: str = "normal",
        chunk_by: str = "sentence",
    ) -> list[tuple[str, float]]:
        """
        Calculate delays for message chunks (for progressive typing simulation).
        
        Args:
            message: Message content
            personality: Agent personality type
            chunk_by: How to chunk the message ("sentence", "word", "character")
            
        Returns:
            List of (chunk, delay) tuples
        """
        if chunk_by == "sentence":
            # Split by sentence
            chunks = self._split_into_sentences(message)
        elif chunk_by == "word":
            # Split by word
            chunks = message.split()
        else:
            # Character by character
            chunks = list(message)
        
        # Calculate delay for each chunk
        result = []
        for chunk in chunks:
            delay = self.calculate_delay(chunk, personality)
            result.append((chunk, delay))
        
        return result

    def _split_into_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        import re
        
        # Simple sentence splitting
        sentences = re.split(r'([.!?]+\s*)', text)
        
        # Recombine sentences with their punctuation
        result = []
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
            if sentence.strip():
                result.append(sentence)
        
        # Add last sentence if it doesn't end with punctuation
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            result.append(sentences[-1])
        
        return result if result else [text]


class TypingDelayTool(BaseTool):
    """
    CrewAI tool for calculating realistic typing delays.
    
    Can be used by agents to simulate human-like typing patterns
    in conversations.
    """

    name: str = "typing_delay_calculator"
    description: str = (
        "Calculates realistic typing delays for messages based on content, "
        "personality, and emotional state. Returns delay in seconds."
    )
    args_schema: type[BaseModel] = TypingDelayInput
    calculator: TypingDelayCalculator = TypingDelayCalculator()

    def __init__(self):
        """Initialize typing delay tool."""
        super().__init__()

    def _run(
        self,
        message: str,
        personality: str = "normal",
        emotional_state: Optional[str] = None,
    ) -> str:
        """
        Calculate typing delay (synchronous).
        
        Args:
            message: Message content
            personality: Agent personality type
            emotional_state: Optional emotional state
            
        Returns:
            Delay information as string
        """
        delay = self.calculator.calculate_delay(message, personality, emotional_state)
        
        return (
            f"Typing delay: {delay} seconds\n"
            f"Message length: {len(message)} characters\n"
            f"Personality: {personality}\n"
            f"Emotional state: {emotional_state or 'neutral'}"
        )

    async def _arun(
        self,
        message: str,
        personality: str = "normal",
        emotional_state: Optional[str] = None,
    ) -> float:
        """
        Calculate typing delay (asynchronous).
        
        Args:
            message: Message content
            personality: Agent personality type
            emotional_state: Optional emotional state
            
        Returns:
            Delay in seconds
        """
        return self.calculator.calculate_delay(message, personality, emotional_state)


class TypingSimulator:
    """
    Simulates realistic typing with delays for WebSocket communication.
    
    Provides methods to simulate typing indicators and progressive
    message delivery.
    """

    def __init__(self, calculator: Optional[TypingDelayCalculator] = None):
        """
        Initialize typing simulator.
        
        Args:
            calculator: Optional typing delay calculator instance
        """
        self.calculator = calculator or TypingDelayCalculator()

    async def simulate_typing(
        self,
        message: str,
        personality: str = "normal",
        emotional_state: Optional[str] = None,
        send_callback: Optional[callable] = None,
    ) -> float:
        """
        Simulate typing delay with optional progress callbacks.
        
        Args:
            message: Message to type
            personality: Agent personality
            emotional_state: Optional emotional state
            send_callback: Optional callback for typing indicators
            
        Returns:
            Total delay time in seconds
        """
        delay = self.calculator.calculate_delay(message, personality, emotional_state)
        
        # Send typing start indicator
        if send_callback:
            await send_callback({"type": "typing_start", "estimated_delay": delay})
        
        # Simulate typing with occasional progress updates
        chunks = max(1, int(delay / 0.5))  # Update every 0.5 seconds
        chunk_delay = delay / chunks
        
        for i in range(chunks):
            await asyncio.sleep(chunk_delay)
            
            # Send progress update
            if send_callback and i < chunks - 1:
                progress = (i + 1) / chunks
                await send_callback({
                    "type": "typing_progress",
                    "progress": progress,
                    "remaining": delay * (1 - progress),
                })
        
        # Send typing stop indicator
        if send_callback:
            await send_callback({"type": "typing_stop"})
        
        return delay

    async def simulate_progressive_typing(
        self,
        message: str,
        personality: str = "normal",
        send_chunk_callback: Optional[callable] = None,
    ) -> float:
        """
        Simulate progressive typing (character by character or word by word).
        
        Args:
            message: Message to type
            personality: Agent personality
            send_chunk_callback: Callback for each chunk
            
        Returns:
            Total delay time in seconds
        """
        chunks = self.calculator.calculate_chunked_delays(message, personality, chunk_by="word")
        
        total_delay = 0.0
        accumulated_text = ""
        
        for chunk, delay in chunks:
            await asyncio.sleep(delay)
            accumulated_text += chunk + " "
            
            if send_chunk_callback:
                await send_chunk_callback({
                    "type": "typing_chunk",
                    "chunk": chunk,
                    "accumulated": accumulated_text.strip(),
                    "progress": len(accumulated_text) / len(message),
                })
            
            total_delay += delay
        
        return total_delay


# Global instances
typing_delay_calculator = TypingDelayCalculator()
typing_simulator = TypingSimulator(typing_delay_calculator)
typing_delay_tool = TypingDelayTool()
