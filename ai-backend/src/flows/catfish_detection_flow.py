"""
Catfish Detection Flow - CrewAI Flow for catfishing detection training.

This flow manages interactive chat simulations with suspicious personas:
1. Create character profile with intentional inconsistencies
2. Manage real-time conversation with typing delays
3. Strategically reveal red flags through natural dialogue
4. Track user's detection awareness
5. Provide comprehensive analysis and feedback
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid
import random

from crewai import Flow, Agent, Crew, Task, Process
from crewai.flow.flow import start, listen, router
from crewai.memory import LongTermMemory, ShortTermMemory

from ..agents.factory import AgentFactory
from ..models.requests import (
    CatfishChatStartRequest,
    CatfishCharacterProfile,
    ChatMessage,
)


class CatfishDetectionFlow(Flow):
    """
    CrewAI Flow for managing catfish detection chat simulations.
    
    This flow coordinates agents to:
    - Generate believable but flawed character profiles
    - Maintain conversation with strategic inconsistencies
    - Reveal red flags naturally through dialogue
    - Track user's detection progress
    - Provide educational feedback on catfishing tactics
    """
    
    def __init__(self, agent_factory: AgentFactory, locale: str = "en"):
        """
        Initialize the Catfish Detection Flow.
        
        Args:
            agent_factory: Factory for creating agents
            locale: Language locale ('en' or 'pt')
        """
        super().__init__()
        self.agent_factory = agent_factory
        self.locale = locale
        
        # Create specialized agents
        self.catfish_character = agent_factory.create_agent("catfish_character", locale)
        self.conversation_moderator = agent_factory.create_agent(
            "conversation_moderator", locale
        )
        self.analytics_agent = agent_factory.create_agent("analytics_agent", locale)
        self.ethics_mentor = agent_factory.create_agent("ethics_mentor", locale)
        
        # Flow state with memory persistence
        self.character_profile: Optional[Dict[str, Any]] = None
        self.conversation_history: List[ChatMessage] = []
        self.red_flags_revealed: List[Dict[str, Any]] = []
        self.user_suspicion_level: float = 0.0
        self.session_start_time: Optional[datetime] = None
        
        # Memory systems for context preservation
        self.long_term_memory = LongTermMemory()
        self.short_term_memory = ShortTermMemory()
        
    @start()
    def initialize_character(
        self, 
        request: CatfishChatStartRequest
    ) -> Dict[str, Any]:
        """
        Initialize a catfish character with intentional inconsistencies.
        
        This is the entry point of the flow. It creates a believable
        character profile with strategic flaws for educational purposes.
        
        Args:
            request: Chat start request with preferences
            
        Returns:
            Character profile and session information
        """
        self.session_start_time = datetime.utcnow()
        
        # Create task for character generation
        character_task = Task(
            description=f"""
            Create a catfish character profile for educational detection training.
            
            Parameters:
            - Difficulty level: {request.difficulty_level} (1-5 scale)
            - Target age range: {request.character_age_range or 'teen/young adult'}
            - User locale: {request.locale}
            
            Create a character that:
            1. Has a believable basic profile (name, age, interests, bio)
            2. Contains {3 + request.difficulty_level} intentional inconsistencies
            3. Includes red flags appropriate for the difficulty level
            4. Uses age-inappropriate language patterns or cultural references
            5. Has a backstory with exploitable gaps
            
            Red flags to incorporate (based on difficulty):
            - Level 1-2: Obvious inconsistencies (age vs. interests, location changes)
            - Level 3: Moderate flags (evasive about personal details, rushed intimacy)
            - Level 4-5: Subtle flags (sophisticated manipulation, grooming behaviors)
            
            The character should be educational and help users recognize real catfishing tactics.
            All content must be appropriate for educational purposes and in {request.locale}.
            """,
            expected_output="""
            A JSON object containing:
            - character_id: unique identifier
            - name: character name
            - stated_age: the age they claim to be
            - actual_age_indicators: clues suggesting different age
            - bio: character biography
            - interests: list of interests
            - profile_image: profile image description
            - red_flags: list of red flags to reveal
            - inconsistencies: list of profile inconsistencies
            - manipulation_tactics: tactics the character will use
            - conversation_strategy: how to reveal flags naturally
            """,
            agent=self.catfish_character,
        )
        
        # Create crew for character generation
        character_crew = Crew(
            agents=[self.catfish_character, self.conversation_moderator],
            tasks=[character_task],
            verbose=True,
            memory=True,
            process=Process.sequential,
        )
        
        # Execute character generation
        result = character_crew.kickoff()
        
        # Parse and store character profile
        character_data = self._parse_character_result(result, request)
        self.character_profile = character_data
        
        # Store in long-term memory for consistency
        self.long_term_memory.save({
            "character_profile": character_data,
            "session_id": character_data["session_id"],
            "user_id": request.user_id,
        })
        
        return {
            "status": "character_initialized",
            "session_id": character_data["session_id"],
            "character_profile": {
                "character_id": character_data["character_id"],
                "name": character_data["name"],
                "age": character_data["stated_age"],
                "bio": character_data["bio"],
                "interests": character_data["interests"],
                "profile_image": character_data.get("profile_image"),
            },
            "user_id": request.user_id,
            "red_flags_count": len(character_data["red_flags"]),
        }
    
    @listen(initialize_character)
    def start_conversation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start the conversation with an opening message from the character.
        
        Args:
            state: Current flow state with character data
            
        Returns:
            Opening message and conversation state
        """
        # Generate opening message
        opening_task = Task(
            description=f"""
            Generate an opening message for the catfish character to start the conversation.
            
            Character: {self.character_profile['name']}
            Bio: {self.character_profile['bio']}
            
            The opening message should:
            1. Be friendly and engaging
            2. Establish the character's persona
            3. Subtly include the first red flag (if difficulty > 1)
            4. Be natural and conversational
            5. Be in {self.locale}
            
            Keep it brief (2-3 sentences) and age-appropriate for the stated age.
            """,
            expected_output="A natural opening message from the character",
            agent=self.catfish_character,
        )
        
        opening_crew = Crew(
            agents=[self.catfish_character],
            tasks=[opening_task],
            verbose=True,
        )
        
        result = opening_crew.kickoff()
        
        # Create opening message
        opening_message = ChatMessage(
            message_id=str(uuid.uuid4()),
            sender=self.character_profile["name"],
            content=str(result.raw) if hasattr(result, 'raw') else str(result),
            timestamp=datetime.utcnow(),
            typing_delay=self._calculate_typing_delay(str(result)),
        )
        
        self.conversation_history.append(opening_message)
        
        return {
            "status": "conversation_started",
            "session_id": state["session_id"],
            "opening_message": opening_message.model_dump(),
            "ready_for_user_input": True,
        }
    
    @listen(start_conversation)
    def manage_conversation_flow(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manage ongoing conversation flow and state.
        
        Args:
            state: Current flow state
            
        Returns:
            Conversation management state
        """
        return {
            "status": "conversation_active",
            "session_id": state["session_id"],
            "message_count": len(self.conversation_history),
            "red_flags_revealed": len(self.red_flags_revealed),
            "awaiting_user_message": True,
        }
    
    def process_user_message(
        self,
        session_id: str,
        user_id: str,
        message_content: str,
        user_suspicion_indicators: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user's message and generate character response.
        
        This method handles the core conversation interaction, maintaining
        character consistency while strategically revealing red flags.
        
        Args:
            session_id: Current session identifier
            user_id: User identifier
            message_content: User's message text
            user_suspicion_indicators: Optional indicators of user's suspicion level
            
        Returns:
            Character's response with typing delay and red flag tracking
        """
        # Record user message
        user_message = ChatMessage(
            message_id=str(uuid.uuid4()),
            sender="user",
            content=message_content,
            timestamp=datetime.utcnow(),
        )
        
        self.conversation_history.append(user_message)
        
        # Update short-term memory with recent context
        self.short_term_memory.save({
            "recent_message": message_content,
            "conversation_turn": len(self.conversation_history),
        })
        
        # Analyze user message for probing questions
        is_probing = self._detect_probing_question(message_content)
        
        # Update user suspicion level if they're asking probing questions
        if is_probing:
            self.user_suspicion_level = min(1.0, self.user_suspicion_level + 0.1)
        
        # Determine if it's time to reveal a new red flag
        should_reveal_flag = self._should_reveal_red_flag()
        
        # Create response task
        response_task = Task(
            description=f"""
            Generate a response as the catfish character to the user's message.
            
            Character Profile:
            - Name: {self.character_profile['name']}
            - Stated Age: {self.character_profile['stated_age']}
            - Bio: {self.character_profile['bio']}
            
            Conversation Context:
            {self._format_recent_conversation()}
            
            User's Message: "{message_content}"
            
            User Suspicion Level: {self.user_suspicion_level * 100:.0f}%
            Is Probing Question: {is_probing}
            Should Reveal New Red Flag: {should_reveal_flag}
            
            Red Flags Already Revealed: {len(self.red_flags_revealed)}
            Remaining Red Flags: {self._get_remaining_red_flags()}
            
            Generate a response that:
            1. Maintains character consistency with previous messages
            2. Responds naturally to the user's message
            3. {'Reveals a new red flag subtly' if should_reveal_flag else 'Continues conversation naturally'}
            4. {'Shows evasiveness or inconsistency if asked probing questions' if is_probing else 'Engages normally'}
            5. Uses language patterns consistent with stated age (with intentional slips)
            6. Is in {self.locale}
            
            Keep the response conversational and realistic (2-4 sentences).
            """,
            expected_output="A natural response from the catfish character",
            agent=self.catfish_character,
        )
        
        # Create crew for response generation
        response_crew = Crew(
            agents=[self.catfish_character, self.conversation_moderator],
            tasks=[response_task],
            verbose=True,
            memory=True,
        )
        
        # Execute response generation
        result = response_crew.kickoff()
        
        # Calculate realistic typing delay
        response_text = str(result.raw) if hasattr(result, 'raw') else str(result)
        typing_delay = self._calculate_typing_delay(response_text, is_evasive=is_probing)
        
        # Create character response
        character_response = ChatMessage(
            message_id=str(uuid.uuid4()),
            sender=self.character_profile["name"],
            content=response_text,
            timestamp=datetime.utcnow(),
            typing_delay=typing_delay,
        )
        
        self.conversation_history.append(character_response)
        
        # Track red flag if revealed
        if should_reveal_flag:
            self._record_red_flag_reveal(response_text)
        
        return {
            "status": "response_generated",
            "response": character_response.model_dump(),
            "typing_delay": typing_delay,
            "red_flags_revealed": len(self.red_flags_revealed),
            "conversation_turn": len(self.conversation_history),
        }
    
    @router(manage_conversation_flow)
    def check_conversation_status(self, state: Dict[str, Any]) -> str:
        """
        Check conversation status and determine next action.
        
        Args:
            state: Current flow state
            
        Returns:
            Route name for next action
        """
        # Check if user has detected the catfish
        if self.user_suspicion_level >= 0.8:
            return "user_detected_catfish"
        
        # Check if all red flags have been revealed
        if len(self.red_flags_revealed) >= len(self.character_profile.get("red_flags", [])):
            return "all_flags_revealed"
        
        # Check if conversation has gone on long enough
        if len(self.conversation_history) >= 20:
            return "conversation_timeout"
        
        # Continue conversation
        return "continue_conversation"
    
    @listen("continue_conversation")
    def continue_active_conversation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continue the active conversation.
        
        Args:
            state: Current flow state
            
        Returns:
            Updated conversation state
        """
        return {
            "status": "conversation_continuing",
            "session_id": state.get("session_id"),
            "awaiting_user_message": True,
        }
    
    @listen("user_detected_catfish")
    def handle_detection(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle case where user has detected the catfish.
        
        Args:
            state: Current flow state
            
        Returns:
            Detection confirmation and analysis
        """
        return self._generate_final_analysis(
            state,
            detection_status="detected",
            reason="User demonstrated high suspicion through probing questions"
        )
    
    @listen("all_flags_revealed")
    def handle_all_flags_revealed(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle case where all red flags have been revealed.
        
        Args:
            state: Current flow state
            
        Returns:
            Complete analysis with all red flags
        """
        return self._generate_final_analysis(
            state,
            detection_status="all_flags_shown",
            reason="All red flags have been presented"
        )
    
    @listen("conversation_timeout")
    def handle_timeout(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle conversation timeout.
        
        Args:
            state: Current flow state
            
        Returns:
            Analysis with timeout notification
        """
        return self._generate_final_analysis(
            state,
            detection_status="timeout",
            reason="Conversation reached maximum length"
        )
    
    def _generate_final_analysis(
        self,
        state: Dict[str, Any],
        detection_status: str,
        reason: str
    ) -> Dict[str, Any]:
        """
        Generate comprehensive analysis of the catfish detection session.
        
        Args:
            state: Current flow state
            detection_status: How the session ended
            reason: Reason for ending
            
        Returns:
            Detailed analysis and feedback
        """
        # Create analysis task
        analysis_task = Task(
            description=f"""
            Provide comprehensive analysis of the user's catfish detection performance.
            
            Session Information:
            - Detection Status: {detection_status}
            - Reason: {reason}
            - Total Messages: {len(self.conversation_history)}
            - Red Flags Revealed: {len(self.red_flags_revealed)}
            - User Suspicion Level: {self.user_suspicion_level * 100:.0f}%
            - Session Duration: {self._get_session_duration()}
            
            Character Profile:
            - Name: {self.character_profile['name']}
            - Stated Age: {self.character_profile['stated_age']}
            - Total Red Flags: {len(self.character_profile.get('red_flags', []))}
            
            Red Flags That Were Revealed:
            {self._format_revealed_red_flags()}
            
            Conversation Summary:
            {self._format_conversation_summary()}
            
            Provide detailed analysis including:
            1. Detection performance score (0-100)
            2. List of all red flags (revealed and missed)
            3. Analysis of user's questioning strategy
            4. Specific red flags the user identified (based on their questions)
            5. Red flags the user missed
            6. Educational explanation of each catfishing tactic used
            7. Recommendations for improving detection skills
            8. Real-world safety tips
            
            Be educational, supportive, and help the user learn to protect themselves.
            Provide the analysis in {self.locale}.
            """,
            expected_output="""
            A JSON object containing:
            - detection_score: 0-100
            - detection_status: detected/partial/missed
            - all_red_flags: complete list with explanations
            - flags_user_caught: list of flags user identified
            - flags_user_missed: list of flags user missed
            - questioning_strategy_analysis: analysis of approach
            - catfishing_tactics_explained: educational explanations
            - recommendations: personalized recommendations
            - safety_tips: real-world safety advice
            - performance_summary: overall summary
            """,
            agent=self.analytics_agent,
        )
        
        # Create crew for analysis
        analysis_crew = Crew(
            agents=[self.analytics_agent, self.ethics_mentor],
            tasks=[analysis_task],
            verbose=True,
            process=Process.sequential,
        )
        
        # Execute analysis
        result = analysis_crew.kickoff()
        
        # Parse analysis result
        analysis_data = self._parse_final_analysis(result, detection_status)
        
        return {
            "status": "session_completed",
            "session_id": state.get("session_id"),
            "detection_status": detection_status,
            "analysis": analysis_data,
            "conversation_history": [msg.model_dump() for msg in self.conversation_history],
        }
    
    def _parse_character_result(
        self,
        result: Any,
        request: CatfishChatStartRequest
    ) -> Dict[str, Any]:
        """Parse crew result into structured character profile."""
        session_id = str(uuid.uuid4())
        character_id = str(uuid.uuid4())
        
        # Generate character based on difficulty
        difficulty = request.difficulty_level
        
        # Sample character (in real implementation, comes from agent)
        character = {
            "session_id": session_id,
            "character_id": character_id,
            "name": "Alex" if self.locale == "en" else "Alexandre",
            "stated_age": 16,
            "actual_age_indicators": ["Uses outdated slang", "References old technology"],
            "bio": self._generate_bio(difficulty, self.locale),
            "interests": self._generate_interests(difficulty, self.locale),
            "profile_image": "/profiles/generic_teen.png",
            "red_flags": self._generate_red_flags(difficulty, self.locale),
            "inconsistencies": [
                "Age vs. cultural references",
                "Location inconsistencies",
                "Evasive about video calls",
            ],
            "manipulation_tactics": [
                "Rushed intimacy",
                "Isolation attempts",
                "Guilt tripping",
            ],
            "conversation_strategy": "Reveal flags gradually through natural conversation",
        }
        
        return character
    
    def _parse_final_analysis(
        self,
        result: Any,
        detection_status: str
    ) -> Dict[str, Any]:
        """Parse final analysis from crew result."""
        # Calculate detection score
        flags_revealed = len(self.red_flags_revealed)
        total_flags = len(self.character_profile.get("red_flags", []))
        
        base_score = (self.user_suspicion_level * 50)  # Up to 50 points for suspicion
        flag_score = (flags_revealed / max(total_flags, 1)) * 50  # Up to 50 points for catching flags
        
        detection_score = min(100, base_score + flag_score)
        
        return {
            "detection_score": detection_score,
            "detection_status": detection_status,
            "all_red_flags": self.character_profile.get("red_flags", []),
            "flags_revealed_count": flags_revealed,
            "flags_user_caught": self.red_flags_revealed,
            "flags_user_missed": total_flags - flags_revealed,
            "questioning_strategy_analysis": str(result),
            "catfishing_tactics_explained": self.character_profile.get("manipulation_tactics", []),
            "recommendations": self._generate_recommendations(),
            "safety_tips": self._generate_safety_tips(self.locale),
            "performance_summary": f"Detected {flags_revealed} out of {total_flags} red flags",
        }
    
    def _detect_probing_question(self, message: str) -> bool:
        """Detect if user is asking probing questions."""
        probing_keywords = [
            "where", "when", "how old", "age", "school", "parents",
            "video", "call", "meet", "photo", "prove", "verify",
            "onde", "quando", "idade", "escola", "pais", "vídeo",
            "encontrar", "foto", "provar", "verificar"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in probing_keywords)
    
    def _should_reveal_red_flag(self) -> bool:
        """Determine if it's time to reveal a new red flag."""
        # Reveal flags gradually based on conversation progress
        messages_per_flag = 4
        expected_flags = len(self.conversation_history) // messages_per_flag
        
        return len(self.red_flags_revealed) < expected_flags
    
    def _record_red_flag_reveal(self, message: str):
        """Record that a red flag was revealed."""
        remaining_flags = self._get_remaining_red_flags()
        
        if remaining_flags:
            flag = remaining_flags[0]
            self.red_flags_revealed.append({
                "flag": flag,
                "revealed_at_turn": len(self.conversation_history),
                "message": message,
                "timestamp": datetime.utcnow().isoformat(),
            })
    
    def _get_remaining_red_flags(self) -> List[str]:
        """Get list of red flags not yet revealed."""
        all_flags = self.character_profile.get("red_flags", [])
        revealed_flag_texts = [f["flag"] for f in self.red_flags_revealed]
        
        return [f for f in all_flags if f not in revealed_flag_texts]
    
    def _calculate_typing_delay(
        self,
        message: str,
        is_evasive: bool = False
    ) -> float:
        """Calculate realistic typing delay based on message and context."""
        # Base delay: ~50ms per character
        base_delay = len(message) * 0.05
        
        # Add thinking time for longer messages
        word_count = len(message.split())
        thinking_time = word_count * 0.1
        
        # Evasive responses take longer (more thinking)
        if is_evasive:
            thinking_time *= 1.5
        
        # Add some randomness for realism
        randomness = random.uniform(0.8, 1.2)
        
        total_delay = (base_delay + thinking_time) * randomness
        
        # Clamp between 1-5 seconds
        return max(1.0, min(5.0, total_delay))
    
    def _format_recent_conversation(self, last_n: int = 5) -> str:
        """Format recent conversation for context."""
        if not self.conversation_history:
            return "No previous conversation"
        
        recent = self.conversation_history[-last_n:]
        formatted = "Recent Conversation:\n"
        
        for msg in recent:
            formatted += f"{msg.sender}: {msg.content}\n"
        
        return formatted
    
    def _format_revealed_red_flags(self) -> str:
        """Format revealed red flags for analysis."""
        if not self.red_flags_revealed:
            return "No red flags revealed yet"
        
        formatted = ""
        for i, flag_data in enumerate(self.red_flags_revealed, 1):
            formatted += f"{i}. {flag_data['flag']} (Turn {flag_data['revealed_at_turn']})\n"
        
        return formatted
    
    def _format_conversation_summary(self) -> str:
        """Format conversation summary."""
        return f"Total messages: {len(self.conversation_history)}, Duration: {self._get_session_duration()}"
    
    def _get_session_duration(self) -> str:
        """Get formatted session duration."""
        if not self.session_start_time:
            return "0 minutes"
        
        duration = datetime.utcnow() - self.session_start_time
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def _generate_bio(self, difficulty: int, locale: str) -> str:
        """Generate character bio based on difficulty."""
        if locale == "pt":
            return "Adoro música, jogos e conhecer pessoas novas. Procurando fazer amigos!"
        return "Love music, games, and meeting new people. Looking to make friends!"
    
    def _generate_interests(self, difficulty: int, locale: str) -> List[str]:
        """Generate character interests."""
        if locale == "pt":
            return ["Música", "Jogos", "Filmes", "Redes sociais"]
        return ["Music", "Gaming", "Movies", "Social media"]
    
    def _generate_red_flags(self, difficulty: int, locale: str) -> List[str]:
        """Generate red flags based on difficulty."""
        if locale == "pt":
            flags = [
                "Evita chamadas de vídeo",
                "Pede fotos pessoais rapidamente",
                "Usa gírias desatualizadas",
                "Inconsistente sobre localização",
                "Pressiona para encontro pessoal",
            ]
        else:
            flags = [
                "Avoids video calls",
                "Asks for personal photos quickly",
                "Uses outdated slang",
                "Inconsistent about location",
                "Pushes for in-person meeting",
            ]
        
        # Return appropriate number based on difficulty
        return flags[:3 + difficulty]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate personalized recommendations."""
        recommendations = []
        
        if self.user_suspicion_level < 0.5:
            recommendations.append("Practice asking more probing questions")
            recommendations.append("Pay attention to inconsistencies in stories")
        
        if len(self.red_flags_revealed) < 3:
            recommendations.append("Look for evasive behavior when asked direct questions")
            recommendations.append("Notice age-inappropriate language or references")
        
        recommendations.append("Always verify identity before sharing personal information")
        recommendations.append("Trust your instincts if something feels off")
        
        return recommendations
    
    def _generate_safety_tips(self, locale: str) -> List[str]:
        """Generate safety tips in appropriate language."""
        if locale == "pt":
            return [
                "Nunca compartilhe informações pessoais com estranhos online",
                "Sempre peça videochamada para verificar identidade",
                "Conte a um adulto de confiança se algo parecer suspeito",
                "Nunca concorde em encontrar alguém pessoalmente sozinho",
                "Bloqueie e denuncie comportamento suspeito",
            ]
        
        return [
            "Never share personal information with strangers online",
            "Always request video calls to verify identity",
            "Tell a trusted adult if something seems suspicious",
            "Never agree to meet someone in person alone",
            "Block and report suspicious behavior",
        ]
