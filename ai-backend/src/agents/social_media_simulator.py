"""
Social Media Simulator Agent - Creates realistic social media environments.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
from crewai import Agent, Task

from .base import BaseEducationalAgent


class SocialMediaSimulatorAgent(BaseEducationalAgent):
    """
    Specialized agent for creating realistic social media simulations
    with authentic and disinformation content for educational training.
    """
    
    def __init__(self, agent: Agent):
        """
        Initialize Social Media Simulator Agent.
        
        Args:
            agent: CrewAI Agent instance configured for content generation
        """
        super().__init__(agent)
        self.disinformation_categories = [
            "health_misinformation",
            "political_manipulation",
            "conspiracy_theories",
            "fake_news",
            "manipulated_statistics"
        ]
        self.engagement_patterns = {
            "authentic": {"like_rate": 0.05, "share_rate": 0.02, "comment_rate": 0.03},
            "disinformation": {"like_rate": 0.15, "share_rate": 0.08, "comment_rate": 0.10}
        }
    
    def generate_feed(
        self,
        num_posts: int = 10,
        disinformation_ratio: float = 0.3,
        user_interests: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a realistic social media feed with mixed content.
        
        Args:
            num_posts: Number of posts to generate
            disinformation_ratio: Ratio of disinformation posts (0.0-1.0)
            user_interests: User's interests for personalization
            
        Returns:
            Feed data with posts and metadata
        """
        posts = []
        num_disinfo = int(num_posts * disinformation_ratio)
        num_authentic = num_posts - num_disinfo
        
        # Generate authentic posts
        for i in range(num_authentic):
            post = self._generate_authentic_post(user_interests)
            posts.append(post)
        
        # Generate disinformation posts
        for i in range(num_disinfo):
            category = random.choice(self.disinformation_categories)
            post = self._generate_disinformation_post(category, user_interests)
            posts.append(post)
        
        # Shuffle posts to mix authentic and disinformation
        random.shuffle(posts)
        
        # Add engagement metrics
        for post in posts:
            post["engagement"] = self._simulate_engagement(post["is_disinformation"])
        
        feed = {
            "posts": posts,
            "total_posts": num_posts,
            "disinformation_count": num_disinfo,
            "authentic_count": num_authentic,
            "generated_at": datetime.utcnow().isoformat(),
            "educational_markers": self._create_educational_markers(posts)
        }
        
        return feed
    
    def _generate_authentic_post(
        self,
        user_interests: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate an authentic social media post."""
        topics = user_interests or ["technology", "education", "health", "environment"]
        topic = random.choice(topics)
        
        post = {
            "post_id": f"auth_{random.randint(1000, 9999)}",
            "author": self._generate_author_profile(credible=True),
            "content": self._generate_authentic_content(topic),
            "topic": topic,
            "is_disinformation": False,
            "timestamp": self._generate_timestamp(),
            "media": self._maybe_add_media(authentic=True),
            "sources": self._add_credible_sources(),
            "red_flags": []
        }
        
        return post
    
    def _generate_disinformation_post(
        self,
        category: str,
        user_interests: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate a disinformation post with educational markers."""
        post = {
            "post_id": f"disinfo_{random.randint(1000, 9999)}",
            "author": self._generate_author_profile(credible=False),
            "content": self._generate_disinformation_content(category),
            "topic": category,
            "is_disinformation": True,
            "category": category,
            "timestamp": self._generate_timestamp(),
            "media": self._maybe_add_media(authentic=False),
            "sources": self._add_questionable_sources(),
            "red_flags": self._identify_red_flags(category)
        }
        
        return post
    
    def _generate_author_profile(self, credible: bool) -> Dict[str, Any]:
        """Generate author profile."""
        if credible:
            return {
                "username": f"expert_{random.randint(100, 999)}",
                "display_name": "Dr. Expert Professional",
                "verified": True,
                "followers": random.randint(10000, 100000),
                "account_age_days": random.randint(1000, 3000),
                "bio": "Verified expert in the field"
            }
        else:
            return {
                "username": f"user{random.randint(10000, 99999)}",
                "display_name": "Anonymous User",
                "verified": False,
                "followers": random.randint(10, 500),
                "account_age_days": random.randint(1, 90),
                "bio": "Just sharing what I found"
            }
    
    def _generate_authentic_content(self, topic: str) -> str:
        """Generate authentic content."""
        templates = {
            "technology": "New research shows promising developments in {topic}. Study published in peer-reviewed journal.",
            "health": "Health officials recommend {action} based on latest scientific evidence.",
            "education": "Educational study finds {finding} in recent analysis of student outcomes.",
            "environment": "Environmental data indicates {trend} according to scientific measurements."
        }
        
        template = templates.get(topic, "Interesting developments in {topic}.")
        return template.format(
            topic=topic,
            action="evidence-based practices",
            finding="positive results",
            trend="measurable changes"
        )
    
    def _generate_disinformation_content(self, category: str) -> str:
        """Generate disinformation content with red flags."""
        templates = {
            "health_misinformation": "SHOCKING! Doctors don't want you to know this ONE WEIRD TRICK! Share before it's deleted!!!",
            "political_manipulation": "BREAKING: Unverified sources claim [sensational claim]. They're trying to hide the truth!",
            "conspiracy_theories": "Wake up people! Connect the dots! [vague connections] - it's all connected!",
            "fake_news": "URGENT: [Emotional headline] - This changes EVERYTHING! Share NOW!",
            "manipulated_statistics": "Studies show 99% of people agree! (Source: trust me bro)"
        }
        
        return templates.get(category, "Sensational claim without evidence!")
    
    def _generate_timestamp(self) -> str:
        """Generate realistic timestamp."""
        now = datetime.utcnow()
        random_past = now - timedelta(hours=random.randint(1, 48))
        return random_past.isoformat()
    
    def _maybe_add_media(self, authentic: bool) -> Optional[Dict[str, str]]:
        """Maybe add media to post."""
        if random.random() < 0.6:  # 60% chance of media
            return {
                "type": random.choice(["image", "video"]),
                "url": f"https://example.com/media/{random.randint(1000, 9999)}",
                "authentic": authentic
            }
        return None
    
    def _add_credible_sources(self) -> List[Dict[str, str]]:
        """Add credible sources."""
        return [
            {
                "title": "Peer-reviewed study",
                "url": "https://example.com/study",
                "credibility": "high"
            }
        ]
    
    def _add_questionable_sources(self) -> List[Dict[str, str]]:
        """Add questionable or missing sources."""
        if random.random() < 0.3:  # 30% chance of any source
            return [
                {
                    "title": "Unknown blog",
                    "url": "https://suspicious-site.com",
                    "credibility": "low"
                }
            ]
        return []  # No sources
    
    def _identify_red_flags(self, category: str) -> List[Dict[str, str]]:
        """Identify red flags in disinformation."""
        red_flags = [
            {
                "type": "emotional_manipulation",
                "description": "Uses ALL CAPS and excessive punctuation to trigger emotional response"
            },
            {
                "type": "urgency_pressure",
                "description": "Creates false urgency with 'SHARE NOW' or 'Before it's deleted'"
            },
            {
                "type": "lack_of_sources",
                "description": "No credible sources or citations provided"
            },
            {
                "type": "sensationalism",
                "description": "Sensational claims without evidence"
            }
        ]
        
        # Return 2-3 random red flags
        return random.sample(red_flags, k=random.randint(2, 3))
    
    def _simulate_engagement(self, is_disinformation: bool) -> Dict[str, int]:
        """Simulate engagement metrics."""
        pattern = self.engagement_patterns["disinformation" if is_disinformation else "authentic"]
        
        base_reach = random.randint(1000, 10000)
        
        return {
            "views": base_reach,
            "likes": int(base_reach * pattern["like_rate"]),
            "shares": int(base_reach * pattern["share_rate"]),
            "comments": int(base_reach * pattern["comment_rate"])
        }
    
    def _create_educational_markers(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create educational markers for the feed."""
        return {
            "simulation_notice": "This is an educational simulation. All content is generated for learning purposes.",
            "detection_tips": [
                "Check for credible sources",
                "Look for emotional manipulation",
                "Verify with multiple sources",
                "Check author credibility"
            ],
            "learning_objectives": [
                "Identify disinformation patterns",
                "Understand algorithmic amplification",
                "Practice critical evaluation"
            ]
        }
    
    def analyze_user_engagement(
        self,
        user_interactions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze user's engagement patterns and provide feedback.
        
        Args:
            user_interactions: List of user's interactions with posts
            
        Returns:
            Analysis of engagement patterns and recommendations
        """
        total_interactions = len(user_interactions)
        disinfo_engaged = sum(1 for i in user_interactions 
                             if i.get("post_is_disinformation", False))
        
        analysis = {
            "total_interactions": total_interactions,
            "disinformation_engaged": disinfo_engaged,
            "authentic_engaged": total_interactions - disinfo_engaged,
            "accuracy_rate": 1 - (disinfo_engaged / total_interactions) if total_interactions > 0 else 0,
            "algorithm_impact": self._calculate_algorithm_impact(user_interactions),
            "recommendations": self._generate_engagement_recommendations(disinfo_engaged, total_interactions),
            "learning_insights": self._generate_learning_insights(user_interactions)
        }
        
        return analysis
    
    def _calculate_algorithm_impact(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate how user's engagement affects algorithm."""
        disinfo_count = sum(1 for i in interactions if i.get("post_is_disinformation", False))
        
        return {
            "amplification_score": disinfo_count * 0.1,
            "feed_bias": "towards_disinformation" if disinfo_count > len(interactions) * 0.5 else "balanced",
            "explanation": "Engaging with disinformation signals the algorithm to show you more similar content"
        }
    
    def _generate_engagement_recommendations(
        self,
        disinfo_engaged: int,
        total: int
    ) -> List[str]:
        """Generate recommendations based on engagement."""
        recommendations = []
        
        if disinfo_engaged > total * 0.3:
            recommendations.append("Be more cautious about engaging with unverified content")
            recommendations.append("Check sources before liking or sharing")
        
        recommendations.append("Continue to verify information from multiple sources")
        recommendations.append("Consider the author's credibility and expertise")
        
        return recommendations
    
    def _generate_learning_insights(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Generate learning insights from interactions."""
        return [
            "Your engagement patterns influence what content you see",
            "Disinformation often uses emotional manipulation to encourage sharing",
            "Critical evaluation is key to responsible social media use"
        ]
