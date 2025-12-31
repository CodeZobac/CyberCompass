"""
Social Media Simulation Flow - CrewAI Flow for social media disinformation training.

This flow manages realistic social media simulations:
1. Generate mixed authentic and disinformation content
2. Track user engagement patterns
3. Provide real-time algorithm feedback
4. Score disinformation detection accuracy
5. Analyze user behavior and provide insights
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import random

from crewai import Flow, Agent, Crew, Task, Process
from crewai.flow.flow import start, listen, router

from ..agents.factory import AgentFactory
from ..models.requests import (
    SocialMediaSimulationRequest,
    SocialMediaPost,
    DisinformationType,
)


class SocialMediaSimulationFlow(Flow):
    """
    CrewAI Flow for managing social media disinformation simulations.
    
    This flow coordinates multiple agents to:
    - Generate realistic social media feeds with mixed content
    - Create disinformation posts across various categories
    - Track user engagement and provide algorithm feedback
    - Score detection accuracy and provide insights
    """
    
    def __init__(self, agent_factory: AgentFactory, locale: str = "en"):
        """
        Initialize the Social Media Simulation Flow.
        
        Args:
            agent_factory: Factory for creating agents
            locale: Language locale ('en' or 'pt')
        """
        super().__init__()
        self.agent_factory = agent_factory
        self.locale = locale
        
        # Create specialized agents
        self.social_media_simulator = agent_factory.create_agent(
            "social_media_simulator", locale
        )
        self.ethics_mentor = agent_factory.create_agent("ethics_mentor", locale)
        self.analytics_agent = agent_factory.create_agent("analytics_agent", locale)
        
        # Flow state
        self.current_feed: List[SocialMediaPost] = []
        self.user_interactions: List[Dict[str, Any]] = []
        self.session_start_time: Optional[datetime] = None
        self.disinformation_ratio: float = 0.3
        
    @start()
    def initialize_simulation(
        self, 
        request: SocialMediaSimulationRequest
    ) -> Dict[str, Any]:
        """
        Initialize a new social media simulation session.
        
        This is the entry point of the flow. It generates an initial
        feed of mixed authentic and disinformation content.
        
        Args:
            request: Simulation request with user preferences
            
        Returns:
            Initial feed data and session information
        """
        self.session_start_time = datetime.utcnow()
        self.disinformation_ratio = request.disinformation_ratio
        
        # Determine categories to include
        categories = request.categories or [
            DisinformationType.HEALTH,
            DisinformationType.POLITICS,
            DisinformationType.FAKE_NEWS,
        ]
        
        # Create task for feed generation
        feed_generation_task = Task(
            description=f"""
            Generate a realistic social media feed for an educational simulation.
            
            Parameters:
            - Number of posts: 15-20 posts
            - Disinformation ratio: {request.disinformation_ratio * 100}%
            - Categories: {', '.join([c.value for c in categories])}
            - User locale: {request.locale}
            - Session duration: {request.session_duration_minutes} minutes
            
            Create a diverse feed that includes:
            1. Authentic, factual posts (majority)
            2. Disinformation posts with varying subtlety
            3. Mix of text, images, and video content
            4. Realistic engagement metrics (likes, shares, comments)
            5. Diverse author profiles and perspectives
            
            Disinformation posts should:
            - Range from obvious to subtle
            - Include common manipulation tactics (emotional appeals, false statistics, misleading headlines)
            - Be clearly educational (marked for later reveal)
            - Represent real-world disinformation patterns
            
            All content must be in {request.locale} and culturally appropriate.
            """,
            expected_output="""
            A JSON array of social media posts, each containing:
            - post_id: unique identifier
            - content: post text
            - author_name: author name
            - author_avatar: avatar URL
            - timestamp: post timestamp
            - likes: number of likes
            - shares: number of shares
            - comments_count: number of comments
            - is_disinformation: boolean flag
            - category: disinformation category (if applicable)
            - manipulation_tactics: list of tactics used (if disinformation)
            - fact_check_info: information for later reveal
            """,
            agent=self.social_media_simulator,
        )
        
        # Create crew for feed generation
        feed_crew = Crew(
            agents=[self.social_media_simulator],
            tasks=[feed_generation_task],
            verbose=True,
            process=Process.sequential,
        )
        
        # Execute feed generation
        result = feed_crew.kickoff()
        
        # Parse and structure the feed
        feed_data = self._parse_feed_result(result, request)
        self.current_feed = feed_data["posts"]
        
        return {
            "status": "simulation_initialized",
            "session_id": feed_data["session_id"],
            "feed": feed_data["posts"],
            "user_id": request.user_id,
            "session_duration_minutes": request.session_duration_minutes,
            "total_posts": len(feed_data["posts"]),
            "disinformation_count": sum(1 for p in feed_data["posts"] if p.get("is_disinformation")),
        }
    
    @listen(initialize_simulation)
    def track_user_engagement(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor user interactions with the social media feed.
        
        This method tracks which posts users engage with and analyzes
        their interaction patterns in real-time.
        
        Args:
            state: Current flow state with feed data
            
        Returns:
            State ready for engagement tracking
        """
        return {
            "status": "tracking_engagement",
            "session_id": state["session_id"],
            "user_id": state["user_id"],
            "tracking_active": True,
            "algorithm_feedback_enabled": True,
        }
    
    def record_interaction(
        self,
        session_id: str,
        user_id: str,
        post_id: str,
        interaction_type: str,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Record a user interaction with a post.
        
        Args:
            session_id: Current session identifier
            user_id: User identifier
            post_id: Post that was interacted with
            interaction_type: Type of interaction (view, like, share, comment, report)
            timestamp: Interaction timestamp
            
        Returns:
            Interaction record and real-time feedback
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Find the post
        post = next((p for p in self.current_feed if p.get("post_id") == post_id), None)
        if not post:
            raise ValueError(f"Post {post_id} not found in current feed")
        
        # Record interaction
        interaction = {
            "interaction_id": str(uuid.uuid4()),
            "session_id": session_id,
            "user_id": user_id,
            "post_id": post_id,
            "interaction_type": interaction_type,
            "timestamp": timestamp.isoformat(),
            "post_is_disinformation": post.get("is_disinformation", False),
            "post_category": post.get("category"),
        }
        
        self.user_interactions.append(interaction)
        
        # Generate real-time algorithm feedback
        algorithm_feedback = self._generate_algorithm_feedback(interaction, post)
        
        return {
            "status": "interaction_recorded",
            "interaction": interaction,
            "algorithm_feedback": algorithm_feedback,
            "total_interactions": len(self.user_interactions),
        }
    
    def _generate_algorithm_feedback(
        self,
        interaction: Dict[str, Any],
        post: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate real-time feedback about how the algorithm responds to user behavior.
        
        Args:
            interaction: The user interaction
            post: The post that was interacted with
            
        Returns:
            Algorithm feedback explaining content amplification
        """
        feedback = {
            "message": "",
            "algorithm_impact": "",
            "content_amplification": 0,
            "recommendations": [],
        }
        
        interaction_type = interaction["interaction_type"]
        is_disinfo = post.get("is_disinformation", False)
        
        if interaction_type in ["like", "share"]:
            if is_disinfo:
                feedback["message"] = self._get_message(
                    "disinfo_engagement",
                    self.locale
                )
                feedback["algorithm_impact"] = "negative"
                feedback["content_amplification"] = 50
                feedback["recommendations"] = [
                    self._get_message("verify_before_sharing", self.locale),
                    self._get_message("check_sources", self.locale),
                ]
            else:
                feedback["message"] = self._get_message(
                    "authentic_engagement",
                    self.locale
                )
                feedback["algorithm_impact"] = "positive"
                feedback["content_amplification"] = 10
        
        elif interaction_type == "report":
            if is_disinfo:
                feedback["message"] = self._get_message(
                    "correct_report",
                    self.locale
                )
                feedback["algorithm_impact"] = "positive"
                feedback["content_amplification"] = -30
            else:
                feedback["message"] = self._get_message(
                    "false_report",
                    self.locale
                )
                feedback["algorithm_impact"] = "neutral"
        
        return feedback
    
    @router(track_user_engagement)
    def check_session_status(self, state: Dict[str, Any]) -> str:
        """
        Check if the simulation session should continue or end.
        
        Args:
            state: Current flow state
            
        Returns:
            Route name for next action
        """
        if not self.session_start_time:
            return "end_session"
        
        # Check if session duration has been reached
        elapsed_time = datetime.utcnow() - self.session_start_time
        
        # For now, we'll let the session continue until explicitly ended
        # In a real implementation, this would check against session_duration_minutes
        
        if len(self.user_interactions) >= 10:
            return "generate_session_analysis"
        
        return "continue_tracking"
    
    @listen("continue_tracking")
    def continue_engagement_tracking(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Continue tracking user engagement.
        
        Args:
            state: Current flow state
            
        Returns:
            Updated tracking state
        """
        return {
            "status": "tracking_continued",
            "session_id": state.get("session_id"),
            "interactions_count": len(self.user_interactions),
        }
    
    @listen("generate_session_analysis")
    def analyze_session_performance(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user's performance during the simulation session.
        
        This generates comprehensive insights about:
        - Detection accuracy
        - Engagement patterns
        - Vulnerability to disinformation
        - Learning progress
        
        Args:
            state: Current flow state
            
        Returns:
            Detailed session analysis
        """
        # Create analysis task
        analysis_task = Task(
            description=f"""
            Analyze the user's performance in the social media simulation session.
            
            Session Data:
            - Total posts viewed: {len(self.current_feed)}
            - Total interactions: {len(self.user_interactions)}
            - Disinformation posts: {sum(1 for p in self.current_feed if p.get('is_disinformation'))}
            - Session duration: {self._get_session_duration()}
            
            User Interactions:
            {self._format_interactions_for_analysis()}
            
            Provide comprehensive analysis including:
            1. Detection accuracy score (0-100)
            2. Engagement pattern analysis
            3. Vulnerability assessment
            4. Specific strengths and weaknesses
            5. Personalized recommendations for improvement
            6. Comparison to typical user behavior
            
            Be constructive and educational in your analysis.
            Highlight both successes and areas for growth.
            """,
            expected_output="""
            A JSON object containing:
            - detection_accuracy: score 0-100
            - total_interactions: number
            - correct_identifications: number
            - false_positives: number
            - false_negatives: number
            - engagement_patterns: analysis of behavior
            - vulnerability_score: 0-100 (lower is better)
            - strengths: list of strengths
            - weaknesses: list of areas to improve
            - recommendations: personalized recommendations
            - peer_comparison: how they compare to others
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
        analysis_data = self._parse_analysis_result(result)
        
        return {
            "status": "session_analyzed",
            "analysis": analysis_data,
            "session_id": state.get("session_id"),
        }
    
    @listen("end_session")
    def finalize_session(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finalize the simulation session and clean up.
        
        Args:
            state: Current flow state
            
        Returns:
            Session summary
        """
        return {
            "status": "session_ended",
            "session_id": state.get("session_id"),
            "total_interactions": len(self.user_interactions),
            "session_duration": self._get_session_duration(),
        }
    
    def _parse_feed_result(
        self,
        result: Any,
        request: SocialMediaSimulationRequest
    ) -> Dict[str, Any]:
        """Parse crew result into structured feed data."""
        session_id = str(uuid.uuid4())
        
        # Generate sample posts (in real implementation, this comes from agent)
        num_posts = 18
        num_disinfo = int(num_posts * request.disinformation_ratio)
        
        posts = []
        categories = request.categories or [DisinformationType.HEALTH, DisinformationType.POLITICS]
        
        for i in range(num_posts):
            is_disinfo = i < num_disinfo
            post = {
                "post_id": str(uuid.uuid4()),
                "content": self._generate_sample_content(is_disinfo, self.locale),
                "author_name": f"User{random.randint(1000, 9999)}",
                "author_avatar": f"/avatars/avatar_{i}.png",
                "timestamp": (datetime.utcnow() - timedelta(hours=random.randint(1, 48))).isoformat(),
                "likes": random.randint(10, 1000),
                "shares": random.randint(0, 200),
                "comments_count": random.randint(0, 50),
                "is_disinformation": is_disinfo,
                "category": random.choice(categories).value if is_disinfo else None,
            }
            posts.append(post)
        
        # Shuffle to mix authentic and disinformation posts
        random.shuffle(posts)
        
        return {
            "session_id": session_id,
            "posts": posts,
        }
    
    def _parse_analysis_result(self, result: Any) -> Dict[str, Any]:
        """Parse analysis result from crew."""
        # Calculate actual metrics from interactions
        total_interactions = len(self.user_interactions)
        
        # Count correct identifications (reporting disinformation, not engaging with it)
        correct_reports = sum(
            1 for i in self.user_interactions
            if i["interaction_type"] == "report" and i["post_is_disinformation"]
        )
        
        # Count false positives (reporting authentic content)
        false_positives = sum(
            1 for i in self.user_interactions
            if i["interaction_type"] == "report" and not i["post_is_disinformation"]
        )
        
        # Count problematic engagements (liking/sharing disinformation)
        false_negatives = sum(
            1 for i in self.user_interactions
            if i["interaction_type"] in ["like", "share"] and i["post_is_disinformation"]
        )
        
        # Calculate detection accuracy
        if total_interactions > 0:
            accuracy = ((correct_reports - false_positives) / total_interactions) * 100
            accuracy = max(0, min(100, accuracy))
        else:
            accuracy = 0
        
        return {
            "detection_accuracy": accuracy,
            "total_interactions": total_interactions,
            "correct_identifications": correct_reports,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "engagement_patterns": str(result),
            "vulnerability_score": min(100, false_negatives * 10),
            "strengths": ["Critical thinking", "Careful evaluation"],
            "weaknesses": ["Speed of detection", "Recognizing subtle manipulation"],
            "recommendations": [
                "Practice identifying emotional manipulation",
                "Verify sources before sharing",
                "Look for fact-check labels",
            ],
            "peer_comparison": "Above average detection rate",
        }
    
    def _format_interactions_for_analysis(self) -> str:
        """Format user interactions for agent analysis."""
        if not self.user_interactions:
            return "No interactions recorded"
        
        summary = f"Total interactions: {len(self.user_interactions)}\n"
        
        # Group by interaction type
        by_type = {}
        for interaction in self.user_interactions:
            itype = interaction["interaction_type"]
            by_type[itype] = by_type.get(itype, 0) + 1
        
        summary += "Interaction breakdown:\n"
        for itype, count in by_type.items():
            summary += f"- {itype}: {count}\n"
        
        return summary
    
    def _get_session_duration(self) -> str:
        """Get formatted session duration."""
        if not self.session_start_time:
            return "0 minutes"
        
        duration = datetime.utcnow() - self.session_start_time
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def _generate_sample_content(self, is_disinfo: bool, locale: str) -> str:
        """Generate sample post content."""
        if locale == "pt":
            if is_disinfo:
                samples = [
                    "URGENTE: Novo estudo revela que 90% dos médicos escondem esta verdade!",
                    "Compartilhe antes que removam! A mídia não quer que você saiba disso.",
                    "Cientistas confirmam: esta técnica simples cura tudo!",
                ]
            else:
                samples = [
                    "Interessante artigo sobre segurança digital publicado hoje.",
                    "Participei de um workshop sobre privacidade online. Muito informativo!",
                    "Lembrete: sempre verifique as fontes antes de compartilhar notícias.",
                ]
        else:
            if is_disinfo:
                samples = [
                    "URGENT: New study reveals 90% of doctors hide this truth!",
                    "Share before they remove it! The media doesn't want you to know this.",
                    "Scientists confirm: this simple technique cures everything!",
                ]
            else:
                samples = [
                    "Interesting article about digital security published today.",
                    "Attended a workshop on online privacy. Very informative!",
                    "Reminder: always verify sources before sharing news.",
                ]
        
        return random.choice(samples)
    
    def _get_message(self, message_key: str, locale: str) -> str:
        """Get localized message."""
        messages = {
            "en": {
                "disinfo_engagement": "Warning: Engaging with this content may amplify disinformation.",
                "authentic_engagement": "Good! Engaging with verified content helps promote quality information.",
                "verify_before_sharing": "Always verify information before sharing",
                "check_sources": "Check the credibility of sources",
                "correct_report": "Excellent! You correctly identified disinformation.",
                "false_report": "This content appears to be authentic. Be careful with false reports.",
            },
            "pt": {
                "disinfo_engagement": "Aviso: Interagir com este conteúdo pode amplificar desinformação.",
                "authentic_engagement": "Bom! Interagir com conteúdo verificado ajuda a promover informação de qualidade.",
                "verify_before_sharing": "Sempre verifique informações antes de compartilhar",
                "check_sources": "Verifique a credibilidade das fontes",
                "correct_report": "Excelente! Você identificou corretamente a desinformação.",
                "false_report": "Este conteúdo parece ser autêntico. Cuidado com denúncias falsas.",
            },
        }
        
        return messages.get(locale, messages["en"]).get(message_key, "")
