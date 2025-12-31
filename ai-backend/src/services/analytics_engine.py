"""
Analytics Engine - Core service for user progress tracking and analytics.

This module implements the analytics engine that processes user interaction data,
calculates competency scores, identifies trends, and generates personalized recommendations.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import statistics

from src.agents.analytics_agent import AnalyticsAgent
from src.agents.factory import AgentFactory


class CompetencyDomain:
    """Competency domain definitions."""
    
    PRIVACY_AWARENESS = "privacy_awareness"
    SECURITY_PRACTICES = "security_practices"
    DISINFORMATION_DETECTION = "disinformation_detection"
    SOCIAL_ENGINEERING_RESISTANCE = "social_engineering_resistance"
    DEEPFAKE_DETECTION = "deepfake_detection"
    ETHICAL_DECISION_MAKING = "ethical_decision_making"
    
    @classmethod
    def all_domains(cls) -> List[str]:
        """Get all competency domains."""
        return [
            cls.PRIVACY_AWARENESS,
            cls.SECURITY_PRACTICES,
            cls.DISINFORMATION_DETECTION,
            cls.SOCIAL_ENGINEERING_RESISTANCE,
            cls.DEEPFAKE_DETECTION,
            cls.ETHICAL_DECISION_MAKING,
        ]


class AnalyticsEngine:
    """
    Core analytics engine for processing user progress and generating insights.
    
    This engine implements sophisticated algorithms for:
    - Competency scoring with weighted recency
    - Trend analysis with statistical significance
    - Pattern recognition in learning behavior
    - Personalized recommendation generation
    """
    
    def __init__(self, agent_factory: Optional[AgentFactory] = None):
        """
        Initialize analytics engine.
        
        Args:
            agent_factory: Factory for creating analytics agents
        """
        self.agent_factory = agent_factory or AgentFactory()
        self.analytics_agent: Optional[AnalyticsAgent] = None
        
        # Scoring weights
        self.recency_weight = 0.7  # Weight for recent performance
        self.historical_weight = 0.3  # Weight for historical performance
        
        # Thresholds
        self.mastery_threshold = 0.85
        self.proficient_threshold = 0.70
        self.developing_threshold = 0.50
        
    async def initialize(self):
        """Initialize analytics agent."""
        if not self.analytics_agent:
            agent = await self.agent_factory.create_agent("analytics_agent")
            self.analytics_agent = AnalyticsAgent(agent)
    
    def calculate_competency_scores(
        self,
        interaction_history: List[Dict[str, Any]],
        use_weighted_recency: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate competency scores for all domains with advanced algorithms.
        
        Args:
            interaction_history: List of user interactions
            use_weighted_recency: Whether to weight recent performance more heavily
            
        Returns:
            Dictionary mapping domains to score details
        """
        scores = {}
        
        for domain in CompetencyDomain.all_domains():
            domain_interactions = [
                i for i in interaction_history 
                if i.get("domain") == domain
            ]
            
            if not domain_interactions:
                scores[domain] = {
                    "score": 0.0,
                    "level": "no_data",
                    "total_attempts": 0,
                    "correct_count": 0,
                    "confidence": 0.0
                }
                continue
            
            # Calculate score with optional recency weighting
            if use_weighted_recency and len(domain_interactions) >= 5:
                score = self._calculate_weighted_score(domain_interactions)
            else:
                score = self._calculate_simple_score(domain_interactions)
            
            # Calculate confidence based on sample size
            confidence = self._calculate_confidence(len(domain_interactions))
            
            # Determine level
            level = self._determine_competency_level(score)
            
            # Count correct answers
            correct_count = sum(1 for i in domain_interactions if i.get("correct", False))
            
            scores[domain] = {
                "score": round(score, 3),
                "level": level,
                "total_attempts": len(domain_interactions),
                "correct_count": correct_count,
                "confidence": round(confidence, 2),
                "last_activity": domain_interactions[-1].get("timestamp")
            }
        
        return scores
    
    def _calculate_weighted_score(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate score with recency weighting."""
        if not interactions:
            return 0.0
        
        sorted_interactions = sorted(
            interactions,
            key=lambda x: datetime.fromisoformat(x.get("timestamp", datetime.utcnow().isoformat()))
        )
        
        split_point = max(1, len(sorted_interactions) // 2)
        historical = sorted_interactions[:split_point]
        recent = sorted_interactions[split_point:]
        
        historical_score = sum(1 for i in historical if i.get("correct", False)) / len(historical)
        recent_score = sum(1 for i in recent if i.get("correct", False)) / len(recent)
        
        weighted_score = (
            historical_score * self.historical_weight +
            recent_score * self.recency_weight
        )
        
        return weighted_score
    
    def _calculate_simple_score(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate simple accuracy score."""
        if not interactions:
            return 0.0
        
        correct_count = sum(1 for i in interactions if i.get("correct", False))
        return correct_count / len(interactions)
    
    def _calculate_confidence(self, sample_size: int) -> float:
        """Calculate confidence level based on sample size."""
        if sample_size == 0:
            return 0.0
        elif sample_size < 5:
            return 0.3
        elif sample_size < 10:
            return 0.5
        elif sample_size < 20:
            return 0.7
        elif sample_size < 50:
            return 0.85
        else:
            return 0.95
    
    def _determine_competency_level(self, score: float) -> str:
        """Determine competency level from score."""
        if score >= self.mastery_threshold:
            return "mastery"
        elif score >= self.proficient_threshold:
            return "proficient"
        elif score >= self.developing_threshold:
            return "developing"
        else:
            return "beginner"
    
    def analyze_trends(
        self,
        interaction_history: List[Dict[str, Any]],
        time_window_days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze learning trends over time.
        
        Args:
            interaction_history: User interaction history
            time_window_days: Time window for trend analysis
            
        Returns:
            Comprehensive trend analysis
        """
        if len(interaction_history) < 3:
            return {
                "overall_trend": "insufficient_data",
                "trend_strength": 0.0,
                "velocity": 0.0,
                "consistency": 0.0,
                "domain_trends": {}
            }
        
        cutoff_date = datetime.utcnow() - timedelta(days=time_window_days)
        recent_interactions = [
            i for i in interaction_history
            if datetime.fromisoformat(i.get("timestamp", datetime.utcnow().isoformat())) > cutoff_date
        ]
        
        if len(recent_interactions) < 3:
            recent_interactions = interaction_history[-10:]
        
        overall_trend, trend_strength = self._calculate_trend_direction(recent_interactions)
        velocity = self._calculate_learning_velocity(recent_interactions)
        consistency = self._calculate_consistency_score(recent_interactions, time_window_days)
        domain_trends = self._analyze_domain_trends(interaction_history)
        patterns = self._identify_learning_patterns(recent_interactions)
        
        return {
            "overall_trend": overall_trend,
            "trend_strength": round(trend_strength, 2),
            "velocity": round(velocity, 3),
            "consistency": round(consistency, 2),
            "domain_trends": domain_trends,
            "patterns": patterns,
            "activity_level": self._assess_activity_level(recent_interactions, time_window_days)
        }
    
    def _calculate_trend_direction(self, interactions: List[Dict[str, Any]]) -> Tuple[str, float]:
        """Calculate trend direction with statistical significance."""
        if len(interactions) < 3:
            return "insufficient_data", 0.0
        
        sorted_interactions = sorted(
            interactions,
            key=lambda x: datetime.fromisoformat(x.get("timestamp", datetime.utcnow().isoformat()))
        )
        
        window_size = max(3, len(sorted_interactions) // 3)
        scores = [1.0 if i.get("correct", False) else 0.0 for i in sorted_interactions]
        
        if len(scores) < window_size * 2:
            mid = len(scores) // 2
            early_avg = sum(scores[:mid]) / mid
            late_avg = sum(scores[mid:]) / (len(scores) - mid)
            difference = late_avg - early_avg
        else:
            early_window = scores[:window_size]
            late_window = scores[-window_size:]
            early_avg = sum(early_window) / len(early_window)
            late_avg = sum(late_window) / len(late_window)
            difference = late_avg - early_avg
        
        strength = abs(difference)
        
        if difference > 0.15:
            return "improving", strength
        elif difference < -0.15:
            return "declining", strength
        else:
            return "stable", strength
    
    def _calculate_learning_velocity(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate rate of improvement (learning velocity)."""
        if len(interactions) < 5:
            return 0.0
        
        quartile_size = len(interactions) // 4
        if quartile_size == 0:
            return 0.0
        
        quartiles = [
            interactions[i:i+quartile_size]
            for i in range(0, len(interactions), quartile_size)
        ][:4]
        
        quartile_scores = [
            sum(1 for i in q if i.get("correct", False)) / len(q)
            for q in quartiles if q
        ]
        
        if len(quartile_scores) < 2:
            return 0.0
        
        velocity = (quartile_scores[-1] - quartile_scores[0]) / len(quartile_scores)
        return velocity
    
    def _calculate_consistency_score(
        self,
        interactions: List[Dict[str, Any]],
        time_window_days: int
    ) -> float:
        """Calculate consistency of engagement."""
        if len(interactions) < 2:
            return 0.0
        
        timestamps = [
            datetime.fromisoformat(i.get("timestamp", datetime.utcnow().isoformat()))
            for i in interactions
        ]
        timestamps.sort()
        
        gaps = [(timestamps[i+1] - timestamps[i]).days for i in range(len(timestamps)-1)]
        
        if not gaps:
            return 0.5
        
        avg_gap = statistics.mean(gaps)
        gap_variance = statistics.variance(gaps) if len(gaps) > 1 else 0
        
        consistency = 1.0 / (1.0 + avg_gap + (gap_variance * 0.1))
        return min(1.0, consistency)
    
    def _analyze_domain_trends(self, interaction_history: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Analyze trends for each competency domain."""
        domain_trends = {}
        
        for domain in CompetencyDomain.all_domains():
            domain_interactions = [
                i for i in interaction_history
                if i.get("domain") == domain
            ]
            
            if len(domain_interactions) < 3:
                domain_trends[domain] = {
                    "trend": "insufficient_data",
                    "strength": 0.0
                }
                continue
            
            trend, strength = self._calculate_trend_direction(domain_interactions)
            
            domain_trends[domain] = {
                "trend": trend,
                "strength": strength,
                "recent_accuracy": self._calculate_recent_accuracy(domain_interactions)
            }
        
        return domain_trends
    
    def _calculate_recent_accuracy(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate accuracy for most recent interactions."""
        if not interactions:
            return 0.0
        
        recent = interactions[-5:]
        correct = sum(1 for i in recent if i.get("correct", False))
        return correct / len(recent)
    
    def _identify_learning_patterns(self, interactions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Identify patterns in learning behavior."""
        patterns = []
        
        if len(interactions) < 5:
            return patterns
        
        # Check for streaks
        current_streak = 0
        max_streak = 0
        for i in interactions:
            if i.get("correct", False):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        if max_streak >= 5:
            patterns.append({
                "type": "streak",
                "description": f"Achieved a {max_streak}-challenge winning streak",
                "impact": "positive"
            })
        
        # Check for time-of-day patterns
        timestamps = [
            datetime.fromisoformat(i.get("timestamp", datetime.utcnow().isoformat()))
            for i in interactions
        ]
        hours = [t.hour for t in timestamps]
        
        if hours:
            most_common_hour = max(set(hours), key=hours.count)
            if hours.count(most_common_hour) / len(hours) > 0.5:
                patterns.append({
                    "type": "time_preference",
                    "description": f"Most active around {most_common_hour}:00",
                    "impact": "neutral"
                })
        
        # Check for difficulty progression
        difficulties = [i.get("difficulty", 1) for i in interactions if "difficulty" in i]
        if len(difficulties) >= 5:
            if difficulties[-1] > difficulties[0]:
                patterns.append({
                    "type": "progression",
                    "description": "Progressing to more challenging content",
                    "impact": "positive"
                })
        
        return patterns
    
    def _assess_activity_level(self, interactions: List[Dict[str, Any]], time_window_days: int) -> str:
        """Assess user's activity level."""
        if time_window_days == 0:
            return "unknown"
        
        interactions_per_day = len(interactions) / time_window_days
        
        if interactions_per_day >= 5:
            return "very_high"
        elif interactions_per_day >= 3:
            return "high"
        elif interactions_per_day >= 1:
            return "moderate"
        elif interactions_per_day >= 0.3:
            return "low"
        else:
            return "very_low"
    
    def generate_recommendations(
        self,
        competency_scores: Dict[str, Dict[str, Any]],
        trends: Dict[str, Any],
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized learning recommendations.
        
        Args:
            competency_scores: User's competency scores
            trends: Trend analysis results
            user_preferences: Optional user preferences
            
        Returns:
            List of prioritized recommendations
        """
        recommendations = []
        user_prefs = user_preferences or {}
        
        # Find weakest domains
        weak_domains = [
            domain for domain, data in competency_scores.items()
            if data["score"] < self.developing_threshold and data["total_attempts"] > 0
        ]
        
        # Find domains with declining trends
        declining_domains = [
            domain for domain, data in trends.get("domain_trends", {}).items()
            if data.get("trend") == "declining"
        ]
        
        # Find strong domains for advanced challenges
        strong_domains = [
            domain for domain, data in competency_scores.items()
            if data["score"] >= self.proficient_threshold
        ]
        
        # Priority 1: Address declining domains
        for domain in declining_domains:
            recommendations.append({
                "priority": "high",
                "type": "remedial",
                "domain": domain,
                "title": f"Refresh Your {self._format_domain_name(domain)} Skills",
                "description": f"Your performance in {self._format_domain_name(domain)} has declined recently. Let's review the fundamentals.",
                "action": "review_basics",
                "estimated_time_minutes": 20,
                "difficulty": "easy"
            })
        
        # Priority 2: Strengthen weak domains
        for domain in weak_domains[:2]:
            if domain not in declining_domains:
                recommendations.append({
                    "priority": "high",
                    "type": "skill_building",
                    "domain": domain,
                    "title": f"Build {self._format_domain_name(domain)} Competency",
                    "description": f"Complete focused exercises to improve your {self._format_domain_name(domain)} skills.",
                    "action": "practice_challenges",
                    "estimated_time_minutes": 30,
                    "difficulty": "medium"
                })
        
        # Priority 3: Advance strong domains
        for domain in strong_domains[:1]:
            recommendations.append({
                "priority": "medium",
                "type": "advancement",
                "domain": domain,
                "title": f"Master {self._format_domain_name(domain)}",
                "description": f"You're doing great! Try advanced challenges to reach mastery level.",
                "action": "advanced_challenges",
                "estimated_time_minutes": 25,
                "difficulty": "hard"
            })
        
        # Priority 4: Consistency recommendations
        if trends.get("consistency", 0) < 0.5:
            recommendations.append({
                "priority": "medium",
                "type": "habit_building",
                "domain": "general",
                "title": "Build a Learning Routine",
                "description": "Regular practice leads to better retention. Try to practice 3-4 times per week.",
                "action": "set_schedule",
                "estimated_time_minutes": 15,
                "difficulty": "easy"
            })
        
        # Priority 5: Explore new domains
        unexplored_domains = [
            domain for domain, data in competency_scores.items()
            if data["total_attempts"] == 0
        ]
        
        if unexplored_domains:
            domain = unexplored_domains[0]
            recommendations.append({
                "priority": "low",
                "type": "exploration",
                "domain": domain,
                "title": f"Explore {self._format_domain_name(domain)}",
                "description": f"Discover new skills in {self._format_domain_name(domain)}.",
                "action": "intro_challenges",
                "estimated_time_minutes": 20,
                "difficulty": "easy"
            })
        
        return recommendations
    
    def _format_domain_name(self, domain: str) -> str:
        """Format domain name for display."""
        return domain.replace("_", " ").title()
    
    def calculate_peer_percentiles(
        self,
        user_scores: Dict[str, Dict[str, Any]],
        peer_data: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Calculate user's percentile ranking compared to peers.
        
        Args:
            user_scores: User's competency scores
            peer_data: Anonymized peer score data
            
        Returns:
            Percentile analysis
        """
        if not peer_data:
            return {
                "available": False,
                "message": "Insufficient peer data for comparison"
            }
        
        percentiles = {}
        
        for domain in CompetencyDomain.all_domains():
            user_score = user_scores.get(domain, {}).get("score", 0.0)
            peer_scores = [p.get(domain, 0.0) for p in peer_data if domain in p]
            
            if not peer_scores:
                continue
            
            below_user = sum(1 for s in peer_scores if s < user_score)
            percentile = (below_user / len(peer_scores)) * 100
            
            percentiles[domain] = {
                "percentile": round(percentile, 1),
                "peer_average": round(statistics.mean(peer_scores), 2),
                "user_score": user_score,
                "comparison": self._get_comparison_text(percentile)
            }
        
        overall_percentile = statistics.mean([p["percentile"] for p in percentiles.values()])
        
        return {
            "available": True,
            "overall_percentile": round(overall_percentile, 1),
            "domain_percentiles": percentiles,
            "interpretation": self._interpret_percentile(overall_percentile),
            "sample_size": len(peer_data),
            "privacy_note": "All peer data is anonymized and aggregated"
        }
    
    def _get_comparison_text(self, percentile: float) -> str:
        """Get comparison text for percentile."""
        if percentile >= 90:
            return "exceptional"
        elif percentile >= 75:
            return "above_average"
        elif percentile >= 50:
            return "average"
        elif percentile >= 25:
            return "below_average"
        else:
            return "needs_improvement"
    
    def _interpret_percentile(self, percentile: float) -> str:
        """Interpret overall percentile ranking."""
        if percentile >= 90:
            return "You're performing better than most learners! Excellent work!"
        elif percentile >= 75:
            return "You're doing great compared to your peers!"
        elif percentile >= 50:
            return "You're making solid progress!"
        elif percentile >= 25:
            return "Keep practicing - you're on the right track!"
        else:
            return "Focus on consistent practice to improve!"
