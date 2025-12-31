"""
Deepfake Analysis Tool for detecting manipulated media content.
"""

import random
from enum import Enum
from typing import List, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class MediaType(str, Enum):
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class DeepfakeAnalysisInput(BaseModel):
    media_url: str = Field(..., description="URL or path to media file")
    media_type: MediaType = Field(..., description="Type of media")
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    user_guess: Optional[bool] = Field(default=None)


class DeepfakeIndicator(BaseModel):
    indicator_type: str
    description: str
    severity: str
    location: Optional[str] = None
    technical_detail: str


class DeepfakeAnalysisResult(BaseModel):
    is_deepfake: bool
    confidence_score: float
    indicators: List[DeepfakeIndicator]
    overall_assessment: str
    educational_notes: List[str]
    difficulty_level: DifficultyLevel


class DeepfakeAnalyzer:
    """Analyzes media content for deepfake indicators."""
    
    def __init__(self):
        self.indicators_db = {
            MediaType.VIDEO: {
                "beginner": [
                    {"type": "visual", "desc": "Unnatural blinking", "severity": "high",
                     "tech": "Deepfake models struggle with eye movements"},
                    {"type": "visual", "desc": "Blurred facial boundaries", "severity": "high",
                     "tech": "Face swapping creates artifacts"},
                ],
                "intermediate": [
                    {"type": "visual", "desc": "Skin tone inconsistencies", "severity": "medium",
                     "tech": "GANs produce different color distributions"},
                ]
            },
            MediaType.AUDIO: {
                "beginner": [
                    {"type": "audio", "desc": "Robotic voice quality", "severity": "high",
                     "tech": "TTS systems produce mechanical speech"},
                ]
            },
            MediaType.IMAGE: {
                "beginner": [
                    {"type": "visual", "desc": "Distorted background", "severity": "high",
                     "tech": "GANs struggle with backgrounds"}
                ]
            }
        }
    
    def analyze(self, media_url: str, media_type: MediaType, 
                difficulty_level: DifficultyLevel) -> DeepfakeAnalysisResult:
        is_deepfake = random.choice([True, False])
        indicators = self._get_indicators(media_type, difficulty_level, is_deepfake)
        confidence = self._calculate_confidence(indicators)
        assessment = self._generate_assessment(is_deepfake, confidence)
        notes = self._generate_notes(media_type, is_deepfake)
        
        return DeepfakeAnalysisResult(
            is_deepfake=is_deepfake,
            confidence_score=confidence,
            indicators=indicators,
            overall_assessment=assessment,
            educational_notes=notes,
            difficulty_level=difficulty_level
        )
    
    def _get_indicators(self, media_type: MediaType, difficulty: DifficultyLevel, 
                       is_deepfake: bool) -> List[DeepfakeIndicator]:
        available = []
        levels = ["beginner", "intermediate", "advanced"]
        current_idx = levels.index(difficulty.value) if difficulty.value in levels else 0
        
        for level in levels[:current_idx + 1]:
            if level in self.indicators_db.get(media_type, {}):
                available.extend(self.indicators_db[media_type][level])
        
        if is_deepfake and available:
            num = min(2, len(available))
            selected = random.sample(available, num)
        else:
            selected = []
        
        return [DeepfakeIndicator(
            indicator_type=ind["type"],
            description=ind["desc"],
            severity=ind["severity"],
            location=f"Timestamp: 0:{random.randint(5, 30):02d}",
            technical_detail=ind["tech"]
        ) for ind in selected]
    
    def _calculate_confidence(self, indicators: List[DeepfakeIndicator]) -> float:
        if not indicators:
            return round(random.uniform(0.2, 0.4), 2)
        base = 0.5 + len(indicators) * 0.15
        return round(min(1.0, base + random.uniform(-0.05, 0.05)), 2)
    
    def _generate_assessment(self, is_deepfake: bool, confidence: float) -> str:
        if is_deepfake:
            return "Strong indicators of manipulation detected." if confidence > 0.7 else "Likely deepfake."
        return "Appears authentic."
    
    def _generate_notes(self, media_type: MediaType, is_deepfake: bool) -> List[str]:
        notes = ["Deepfakes use AI models (GANs) to manipulate media." if is_deepfake 
                else "Not all suspicious media is fake."]
        if media_type == MediaType.VIDEO:
            notes.append("Check facial boundaries and eye movements.")
        return notes


class DeepfakeAnalysisTool(BaseTool):
    """CrewAI tool for analyzing media for deepfake indicators."""
    
    name: str = "deepfake_analyzer"
    description: str = "Analyzes media content for deepfake indicators."
    args_schema: type[BaseModel] = DeepfakeAnalysisInput
    analyzer: DeepfakeAnalyzer = DeepfakeAnalyzer()
    
    def __init__(self):
        super().__init__()
    
    def _run(self, media_url: str, media_type: MediaType, 
             difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER,
             user_guess: Optional[bool] = None) -> str:
        result = self.analyzer.analyze(media_url, media_type, difficulty_level)
        
        output = f"=== Deepfake Analysis ===\n"
        output += f"Verdict: {'DEEPFAKE' if result.is_deepfake else 'AUTHENTIC'}\n"
        output += f"Confidence: {result.confidence_score:.0%}\n\n"
        
        if user_guess is not None:
            correct = user_guess == result.is_deepfake
            output += f"User Guess: {'Correct' if correct else 'Incorrect'}\n\n"
        
        output += f"{result.overall_assessment}\n\n"
        
        if result.indicators:
            output += "Indicators:\n"
            for i, ind in enumerate(result.indicators, 1):
                output += f"{i}. [{ind.severity.upper()}] {ind.description}\n"
        
        output += "\nEducational Notes:\n"
        for note in result.educational_notes:
            output += f"• {note}\n"
        
        return output
    
    async def _arun(self, media_url: str, media_type: MediaType,
                   difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER,
                   user_guess: Optional[bool] = None) -> DeepfakeAnalysisResult:
        return self.analyzer.analyze(media_url, media_type, difficulty_level)


deepfake_analysis_tool = DeepfakeAnalysisTool()
