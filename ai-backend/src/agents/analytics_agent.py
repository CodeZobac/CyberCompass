"""
Analytics Agent - Processes user data to generate insights and recommendations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from crewai import Agent, Task

from .base import BaseEducationalAgent


class AnalyticsAgent(BaseEducationalAgent):
    """
    Specialized agent for analyzing user progress, identifying patterns,
    and generating personalized learning recommendations.
    """
    
    def __init__(self, agent: Agent):
        """
        Initialize Analytics Agent.
        
        Args:
            agent: CrewAI Agent instance configured for analytics
        """
        super().__init__(agent)
        self.competency_domains = [
            "privacy_awareness",
            "security_practices",
            "disinformation_detection",
            "social_engineering_resistance",
            "deepfake_detection",
            "ethical_decision_making"
        ]
    
    def analyze_user_progress(
        self,
        user_id: str,
        interaction_history: List[Dict[str, Any]],
        time_period: Optional[int] = 30  # days
    ) -> Dict[str, Any]:
        """
        Analyze user's progress across all competency domains.
        
        Args:
            user_id: User identifier
            interaction_history: User's interaction history
            time_period: Time period to analyze (days)
            
        Returns:
            Comprehensive progress analysis
        """
        # Calculate competency scores
        competency_scores = self._calculate_competency_scores(interaction_history)
        
        # Identify trends
        trends = self._identify_trends(interaction_history, time_period)
        
        # Generate insights
        insights = self._generate_insights(competency_scores, trends)
        
        # Create recommendations
        recommendations = self._generate_recommendations(competency_scores, trends)
        
        # Calculate overall progress
        overall_progress = self._calculate_overall_progress(competency_scores, trends)
        
        analysis = {
            "user_id": user_id,
            "analysis_date": datetime.utcnow().isoformat(),
            "time_period_days": time_period,
            "competency_scores": competency_scores,
            "trends": trends,
            "insights": insights,
            "recommendations": recommendations,
            "overall_progress": overall_progress,
            "achievements": self._identify_achievements(competency_scores, interaction_history)
        }
        
        return analysis
    
    def _calculate_competency_scores(
        self,
        interaction_history: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate scores for each competency domain."""
        scores = {}
        
        for domain in self.competency_domains:
            domain_interactions = [
                i for i in interaction_history 
                if i.get("domain") == domain
            ]
            
            if domain_interactions:
                correct_count = sum(1 for i in domain_interactions if i.get("correct", False))
                score = correct_count / len(domain_interactions)
            else:
                score = 0.0
            
            scores[domain] = round(score, 2)
        
        return scores
    
    def _identify_trends(
        self,
        interaction_history: List[Dict[str, Any]],
        time_period: int
    ) -> Dict[str, Any]:
        """Identify learning trends over time."""
        cutoff_date = datetime.utcnow() - timedelta(days=time_period)
        
        # Split history into time buckets
        recent_interactions = [
            i for i in interaction_history 
            if datetime.fromisoformat(i.get("timestamp", datetime.utcnow().isoformat())) > cutoff_date
        ]
        
        # Calculate trend direction
        trends = {
            "overall_trend": self._calculate_trend_direction(recent_interactions),
            "most_improved_domain": self._find_most_improved_domain(interaction_history),
            "needs_attention_domain": self._find_needs_attention_domain(interaction_history),
            "activity_level": self._assess_activity_level(recent_interactions, time_period),
            "consistency_score": self._calculate_consistency(recent_interactions)
        }
        
        return trends
    
    def _calculate_trend_direction(self, interactions: List[Dict[str, Any]]) -> str:
        """Calculate overall trend direction."""
        if len(interactions) < 5:
            return "insufficient_data"
        
        # Split into first half and second half
        mid_point = len(interactions) // 2
        first_half = interactions[:mid_point]
        second_half = interactions[mid_point:]
        
        first_accuracy = sum(1 for i in first_half if i.get("correct", False)) / len(first_half)
        second_accuracy = sum(1 for i in second_half if i.get("correct", False)) / len(second_half)
        
        if second_accuracy > first_accuracy + 0.1:
            return "improving"
        elif second_accuracy < first_accuracy - 0.1:
            return "declining"
        else:
            return "stable"
    
    def _find_most_improved_domain(self, history: List[Dict[str, Any]]) -> Optional[str]:
        """Find the domain with most improvement."""
        if len(history) < 10:
            return None
        
        domain_improvements = {}
        
        for domain in self.competency_domains:
            domain_history = [i for i in history if i.get("domain") == domain]
            
            if len(domain_history) >= 5:
                mid = len(domain_history) // 2
                early = domain_history[:mid]
                recent = domain_history[mid:]
                
                early_score = sum(1 for i in early if i.get("correct", False)) / len(early)
                recent_score = sum(1 for i in recent if i.get("correct", False)) / len(recent)
                
                improvement = recent_score - early_score
                domain_improvements[domain] = improvement
        
        if domain_improvements:
            return max(domain_improvements, key=domain_improvements.get)
        
        return None
    
    def _find_needs_attention_domain(self, history: List[Dict[str, Any]]) -> Optional[str]:
        """Find domain that needs most attention."""
        domain_scores = {}
        
        for domain in self.competency_domains:
            domain_history = [i for i in history if i.get("domain") == domain]
            
            if domain_history:
                score = sum(1 for i in domain_history if i.get("correct", False)) / len(domain_history)
                domain_scores[domain] = score
        
        if domain_scores:
            return min(domain_scores, key=domain_scores.get)
        
        return None
    
    def _assess_activity_level(self, interactions: List[Dict[str, Any]], days: int) -> str:
        """Assess user's activity level."""
        interactions_per_day = len(interactions) / days if days > 0 else 0
        
        if interactions_per_day >= 3:
            return "highly_active"
        elif interactions_per_day >= 1:
            return "active"
        elif interactions_per_day >= 0.5:
            return "moderate"
        else:
            return "low"
    
    def _calculate_consistency(self, interactions: List[Dict[str, Any]]) -> float:
        """Calculate consistency score based on regular engagement."""
        if len(interactions) < 7:
            return 0.5
        
        # Check for gaps in activity
        timestamps = [datetime.fromisoformat(i.get("timestamp", datetime.utcnow().isoformat())) 
                     for i in interactions]
        timestamps.sort()
        
        gaps = [(timestamps[i+1] - timestamps[i]).days 
                for i in range(len(timestamps)-1)]
        
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        
        # Lower average gap = higher consistency
        if avg_gap <= 1:
            return 0.9
        elif avg_gap <= 3:
            return 0.7
        elif avg_gap <= 7:
            return 0.5
        else:
            return 0.3
    
    def _generate_insights(
        self,
        competency_scores: Dict[str, float],
        trends: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate actionable insights."""
        insights = []
        
        # Insight about overall trend
        trend = trends["overall_trend"]
        if trend == "improving":
            insights.append({
                "type": "positive",
                "title": "Great Progress!",
                "description": "Your skills are improving consistently. Keep up the excellent work!"
            })
        elif trend == "declining":
            insights.append({
                "type": "attention",
                "title": "Let's Refocus",
                "description": "Your recent performance suggests you might benefit from reviewing fundamentals."
            })
        
        # Insight about strengths
        strong_domains = [d for d, s in competency_scores.items() if s >= 0.8]
        if strong_domains:
            insights.append({
                "type": "strength",
                "title": "Your Strengths",
                "description": f"You excel in: {', '.join([d.replace('_', ' ') for d in strong_domains])}"
            })
        
        # Insight about improvement areas
        weak_domains = [d for d, s in competency_scores.items() if s < 0.6]
        if weak_domains:
            insights.append({
                "type": "improvement",
                "title": "Growth Opportunities",
                "description": f"Focus on improving: {', '.join([d.replace('_', ' ') for d in weak_domains])}"
            })
        
        # Insight about consistency
        if trends["consistency_score"] >= 0.7:
            insights.append({
                "type": "positive",
                "title": "Consistent Learner",
                "description": "Your regular practice is paying off!"
            })
        
        return insights
    
    def _generate_recommendations(
        self,
        competency_scores: Dict[str, float],
        trends: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate personalized learning recommendations."""
        recommendations = []
        
        # Recommend focus on weak areas
        needs_attention = trends.get("needs_attention_domain")
        if needs_attention:
            recommendations.append({
                "priority": "high",
                "domain": needs_attention,
                "title": f"Strengthen {needs_attention.replace('_', ' ').title()}",
                "description": f"Complete 5 more challenges in {needs_attention.replace('_', ' ')}",
                "estimated_time": "30 minutes"
            })
        
        # Recommend building on strengths
        most_improved = trends.get("most_improved_domain")
        if most_improved:
            recommendations.append({
                "priority": "medium",
                "domain": most_improved,
                "title": f"Advance Your {most_improved.replace('_', ' ').title()} Skills",
                "description": "Try advanced challenges to further develop this strength",
                "estimated_time": "20 minutes"
            })
        
        # Recommend consistency if needed
        if trends["consistency_score"] < 0.5:
            recommendations.append({
                "priority": "medium",
                "domain": "general",
                "title": "Build a Learning Routine",
                "description": "Try to practice at least 3 times per week for better retention",
                "estimated_time": "15 minutes per session"
            })
        
        return recommendations
    
    def _calculate_overall_progress(
        self,
        competency_scores: Dict[str, float],
        trends: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate overall progress metrics."""
        avg_score = sum(competency_scores.values()) / len(competency_scores) if competency_scores else 0
        
        return {
            "average_competency": round(avg_score, 2),
            "level": self._determine_level(avg_score),
            "trend": trends["overall_trend"],
            "next_milestone": self._get_next_milestone(avg_score)
        }
    
    def _determine_level(self, avg_score: float) -> str:
        """Determine user's overall level."""
        if avg_score >= 0.8:
            return "advanced"
        elif avg_score >= 0.6:
            return "intermediate"
        elif avg_score >= 0.4:
            return "developing"
        else:
            return "beginner"
    
    def _get_next_milestone(self, avg_score: float) -> Dict[str, Any]:
        """Get next milestone for user."""
        if avg_score < 0.5:
            return {
                "title": "Reach Developing Level",
                "target_score": 0.5,
                "progress": avg_score / 0.5
            }
        elif avg_score < 0.7:
            return {
                "title": "Reach Intermediate Level",
                "target_score": 0.7,
                "progress": (avg_score - 0.5) / 0.2
            }
        else:
            return {
                "title": "Reach Advanced Level",
                "target_score": 0.8,
                "progress": (avg_score - 0.7) / 0.1
            }
    
    def _identify_achievements(
        self,
        competency_scores: Dict[str, float],
        interaction_history: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify earned achievements."""
        achievements = []
        
        # Domain mastery achievements
        for domain, score in competency_scores.items():
            if score >= 0.9:
                achievements.append({
                    "type": "mastery",
                    "title": f"{domain.replace('_', ' ').title()} Master",
                    "description": f"Achieved 90%+ accuracy in {domain.replace('_', ' ')}",
                    "earned_at": datetime.utcnow().isoformat()
                })
        
        # Activity achievements
        if len(interaction_history) >= 50:
            achievements.append({
                "type": "activity",
                "title": "Dedicated Learner",
                "description": "Completed 50+ learning activities",
                "earned_at": datetime.utcnow().isoformat()
            })
        
        return achievements
    
    def generate_peer_comparison(
        self,
        user_scores: Dict[str, float],
        anonymized_peer_data: List[Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Generate anonymized peer comparison.
        
        Args:
            user_scores: User's competency scores
            anonymized_peer_data: Anonymized scores from other users
            
        Returns:
            Peer comparison analysis
        """
        if not anonymized_peer_data:
            return {"available": False}
        
        # Calculate percentiles
        percentiles = {}
        for domain in self.competency_domains:
            user_score = user_scores.get(domain, 0)
            peer_scores = [p.get(domain, 0) for p in anonymized_peer_data]
            
            if peer_scores:
                percentile = sum(1 for s in peer_scores if s <= user_score) / len(peer_scores)
                percentiles[domain] = round(percentile * 100, 1)
        
        avg_percentile = sum(percentiles.values()) / len(percentiles) if percentiles else 0
        
        return {
            "available": True,
            "overall_percentile": round(avg_percentile, 1),
            "domain_percentiles": percentiles,
            "interpretation": self._interpret_percentile(avg_percentile),
            "privacy_note": "All peer data is anonymized and aggregated"
        }
    
    def _interpret_percentile(self, percentile: float) -> str:
        """Interpret percentile ranking."""
        if percentile >= 90:
            return "You're performing better than most learners!"
        elif percentile >= 75:
            return "You're doing great compared to your peers!"
        elif percentile >= 50:
            return "You're making solid progress!"
        elif percentile >= 25:
            return "Keep practicing - you're on the right track!"
        else:
            return "Focus on consistent practice to improve!"
