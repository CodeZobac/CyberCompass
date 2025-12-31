"""
Ethics Mentor Agent - Provides educational feedback on ethical decisions.
"""

from typing import Dict, List, Optional, Any
from crewai import Agent, Task

from .base import BaseEducationalAgent


class EthicsMentorAgent(BaseEducationalAgent):
    """
    Specialized agent for providing ethical guidance and educational feedback.
    Supports cultural adaptation for Portuguese and English learners.
    """
    
    def __init__(self, agent: Agent):
        """
        Initialize Ethics Mentor Agent.
        
        Args:
            agent: CrewAI Agent instance configured for ethics mentoring
        """
        super().__init__(agent)
        self.cultural_contexts = {
            "en": {
                "communication_style": "direct and analytical",
                "examples": "US/UK technology contexts",
                "values": ["individual privacy", "transparency", "accountability"]
            },
            "pt": {
                "communication_style": "warm and relational",
                "examples": "Brazilian technology contexts",
                "values": ["community trust", "social responsibility", "digital inclusion"]
            }
        }
    
    def generate_feedback(
        self,
        user_choice: str,
        correct_choice: str,
        scenario_context: Dict[str, Any],
        user_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate contextual feedback on an ethical decision.
        
        Args:
            user_choice: The option the user selected
            correct_choice: The ethically preferred option
            scenario_context: Context about the ethical dilemma
            user_history: User's previous interactions for adaptive feedback
            
        Returns:
            Structured feedback with reasoning and follow-up questions
        """
        # Analyze user's learning level
        learning_level = self._assess_learning_level(user_history)
        
        # Get cultural context
        cultural_context = self.cultural_contexts.get(self.locale, self.cultural_contexts["en"])
        
        # Create feedback task for the agent
        task_description = f"""
        Provide educational feedback on an ethical decision.
        
        Scenario: {scenario_context.get('description', 'Ethical dilemma')}
        User's choice: {user_choice}
        Ethically preferred choice: {correct_choice}
        Learning level: {learning_level}
        Cultural context: {cultural_context['communication_style']}
        
        Generate feedback that:
        1. Acknowledges the user's reasoning
        2. Explains why the preferred choice is more ethical
        3. Provides {learning_level}-level explanation
        4. Uses culturally appropriate examples from {cultural_context['examples']}
        5. Includes 2-3 reflective follow-up questions
        6. Responds in {'Portuguese' if self.locale == 'pt' else 'English'}
        """
        
        task = Task(
            description=task_description,
            expected_output="Structured educational feedback with reasoning and questions",
            agent=self.agent
        )
        
        # Store context in memory
        self.memory.update_user_context({
            "last_scenario": scenario_context,
            "last_choice": user_choice,
            "learning_level": learning_level
        })
        
        # Generate feedback structure
        feedback = {
            "acknowledgment": self._generate_acknowledgment(user_choice, correct_choice),
            "explanation": self._generate_explanation(scenario_context, correct_choice),
            "learning_objectives": self._identify_learning_objectives(scenario_context),
            "follow_up_questions": self._generate_follow_up_questions(scenario_context),
            "cultural_examples": self._get_cultural_examples(scenario_context),
            "complexity_level": learning_level
        }
        
        return feedback
    
    def _assess_learning_level(self, user_history: Optional[List[Dict[str, Any]]]) -> str:
        """
        Assess user's learning level based on history.
        
        Args:
            user_history: User's interaction history
            
        Returns:
            Learning level: 'beginner', 'intermediate', or 'advanced'
        """
        if not user_history or len(user_history) < 3:
            return "beginner"
        
        # Calculate accuracy from history
        correct_count = sum(1 for item in user_history if item.get("correct", False))
        accuracy = correct_count / len(user_history)
        
        if accuracy >= 0.8:
            return "advanced"
        elif accuracy >= 0.5:
            return "intermediate"
        else:
            return "beginner"
    
    def _generate_acknowledgment(self, user_choice: str, correct_choice: str) -> str:
        """Generate acknowledgment of user's choice."""
        if user_choice == correct_choice:
            return "Great thinking! Your choice demonstrates strong ethical reasoning."
        else:
            return "I appreciate your thoughtful consideration of this dilemma."
    
    def _generate_explanation(
        self,
        scenario_context: Dict[str, Any],
        correct_choice: str
    ) -> str:
        """Generate explanation of the ethical reasoning."""
        # This would use the CrewAI agent to generate detailed explanation
        return f"The ethically preferred approach considers multiple stakeholders and long-term consequences."
    
    def _identify_learning_objectives(self, scenario_context: Dict[str, Any]) -> List[str]:
        """Identify key learning objectives from the scenario."""
        objectives = []
        
        scenario_type = scenario_context.get("type", "general")
        
        if scenario_type == "privacy":
            objectives = [
                "Understanding data privacy principles",
                "Balancing convenience with security",
                "Recognizing consent requirements"
            ]
        elif scenario_type == "security":
            objectives = [
                "Identifying security vulnerabilities",
                "Understanding responsible disclosure",
                "Balancing security with usability"
            ]
        elif scenario_type == "social_media":
            objectives = [
                "Recognizing disinformation patterns",
                "Understanding algorithmic amplification",
                "Practicing digital citizenship"
            ]
        else:
            objectives = [
                "Applying ethical frameworks",
                "Considering stakeholder impacts",
                "Making principled decisions"
            ]
        
        return objectives
    
    def _generate_follow_up_questions(self, scenario_context: Dict[str, Any]) -> List[str]:
        """Generate reflective follow-up questions."""
        questions = [
            "What other stakeholders might be affected by this decision?",
            "How might this situation look different in 5 years?",
            "What ethical principles guided your thinking?"
        ]
        
        return questions
    
    def _get_cultural_examples(self, scenario_context: Dict[str, Any]) -> List[str]:
        """Get culturally appropriate examples."""
        cultural_context = self.cultural_contexts.get(self.locale, self.cultural_contexts["en"])
        
        # This would be expanded with actual cultural examples
        examples = [
            f"Example from {cultural_context['examples']}",
            f"Considering {cultural_context['values'][0]}"
        ]
        
        return examples
    
    def provide_learning_path_recommendation(
        self,
        user_progress: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Recommend personalized learning path based on user progress.
        
        Args:
            user_progress: User's progress data across different domains
            
        Returns:
            Recommended learning path with specific topics
        """
        # Analyze strengths and weaknesses
        strengths = []
        improvement_areas = []
        
        for domain, score in user_progress.get("domain_scores", {}).items():
            if score >= 0.8:
                strengths.append(domain)
            elif score < 0.6:
                improvement_areas.append(domain)
        
        # Create learning plan
        plan = self.create_learning_plan(
            objective="Improve cyber ethics competency",
            user_context=user_progress
        )
        
        recommendation = {
            "strengths": strengths,
            "improvement_areas": improvement_areas,
            "recommended_topics": self._prioritize_topics(improvement_areas),
            "learning_plan": plan,
            "estimated_time": self._estimate_learning_time(improvement_areas)
        }
        
        return recommendation
    
    def _prioritize_topics(self, improvement_areas: List[str]) -> List[Dict[str, str]]:
        """Prioritize topics for learning."""
        topic_map = {
            "privacy": {
                "title": "Data Privacy Fundamentals",
                "description": "Learn about personal data protection and privacy rights"
            },
            "security": {
                "title": "Cybersecurity Basics",
                "description": "Understand security threats and protective measures"
            },
            "disinformation": {
                "title": "Media Literacy",
                "description": "Develop skills to identify and combat disinformation"
            },
            "social_engineering": {
                "title": "Social Engineering Awareness",
                "description": "Recognize and defend against manipulation tactics"
            }
        }
        
        return [topic_map.get(area, {"title": area, "description": ""}) 
                for area in improvement_areas]
    
    def _estimate_learning_time(self, improvement_areas: List[str]) -> str:
        """Estimate time needed for learning path."""
        hours = len(improvement_areas) * 2  # 2 hours per topic
        return f"{hours} hours"
