"""
Gamification System - Badges, achievements, and level progression.

This module implements the gamification layer that motivates learners through:
- Badge and achievement tracking
- Level progression based on competency scores
- Milestone celebrations
- Motivational feedback
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class BadgeType(str, Enum):
    """Types of badges that can be earned."""
    
    MASTERY = "mastery"
    STREAK = "streak"
    EXPLORER = "explorer"
    CONSISTENCY = "consistency"
    IMPROVEMENT = "improvement"
    MILESTONE = "milestone"
    SPECIAL = "special"


class BadgeRarity(str, Enum):
    """Badge rarity levels."""
    
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Badge:
    """Badge definition."""
    
    def __init__(
        self,
        badge_id: str,
        name: str,
        description: str,
        badge_type: BadgeType,
        rarity: BadgeRarity,
        icon: str,
        criteria: Dict[str, Any]
    ):
        self.badge_id = badge_id
        self.name = name
        self.description = description
        self.badge_type = badge_type
        self.rarity = rarity
        self.icon = icon
        self.criteria = criteria
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert badge to dictionary."""
        return {
            "badge_id": self.badge_id,
            "name": self.name,
            "description": self.description,
            "type": self.badge_type.value,
            "rarity": self.rarity.value,
            "icon": self.icon,
            "criteria": self.criteria
        }


class Achievement:
    """User achievement record."""
    
    def __init__(
        self,
        achievement_id: str,
        user_id: str,
        badge: Badge,
        earned_at: datetime,
        progress: float = 1.0
    ):
        self.achievement_id = achievement_id
        self.user_id = user_id
        self.badge = badge
        self.earned_at = earned_at
        self.progress = progress
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert achievement to dictionary."""
        return {
            "achievement_id": self.achievement_id,
            "user_id": self.user_id,
            "badge": self.badge.to_dict(),
            "earned_at": self.earned_at.isoformat(),
            "progress": self.progress
        }


class GamificationSystem:
    """
    Core gamification system managing badges, achievements, and progression.
    """
    
    def __init__(self):
        """Initialize gamification system with badge definitions."""
        self.badges = self._initialize_badges()
        self.level_thresholds = self._initialize_level_thresholds()
    
    def _initialize_badges(self) -> Dict[str, Badge]:
        """Initialize all available badges."""
        badges = {}
        
        # Mastery Badges (domain-specific)
        domains = [
            ("privacy_awareness", "Privacy Guardian"),
            ("security_practices", "Security Expert"),
            ("disinformation_detection", "Truth Seeker"),
            ("social_engineering_resistance", "Social Shield"),
            ("deepfake_detection", "Reality Checker"),
            ("ethical_decision_making", "Ethics Champion")
        ]
        
        for domain_id, domain_name in domains:
            badges[f"mastery_{domain_id}"] = Badge(
                badge_id=f"mastery_{domain_id}",
                name=f"{domain_name}",
                description=f"Achieved mastery level (85%+) in {domain_name.lower()}",
                badge_type=BadgeType.MASTERY,
                rarity=BadgeRarity.RARE,
                icon=f"🏆_{domain_id}",
                criteria={"domain": domain_id, "min_score": 0.85, "min_attempts": 10}
            )
        
        # Streak Badges
        streak_badges = [
            ("streak_5", "Hot Streak", "5 correct answers in a row", 5, BadgeRarity.COMMON),
            ("streak_10", "On Fire", "10 correct answers in a row", 10, BadgeRarity.UNCOMMON),
            ("streak_20", "Unstoppable", "20 correct answers in a row", 20, BadgeRarity.RARE),
            ("streak_50", "Legendary Streak", "50 correct answers in a row", 50, BadgeRarity.LEGENDARY)
        ]
        
        for badge_id, name, desc, count, rarity in streak_badges:
            badges[badge_id] = Badge(
                badge_id=badge_id,
                name=name,
                description=desc,
                badge_type=BadgeType.STREAK,
                rarity=rarity,
                icon="🔥",
                criteria={"streak_length": count}
            )
        
        # Explorer Badges
        badges["explorer_all_domains"] = Badge(
            badge_id="explorer_all_domains",
            name="Cyber Explorer",
            description="Completed challenges in all competency domains",
            badge_type=BadgeType.EXPLORER,
            rarity=BadgeRarity.UNCOMMON,
            icon="🗺️",
            criteria={"domains_explored": 6}
        )
        
        # Consistency Badges
        consistency_badges = [
            ("consistent_7", "Week Warrior", "Practiced 7 days in a row", 7, BadgeRarity.COMMON),
            ("consistent_30", "Monthly Master", "Practiced 30 days in a row", 30, BadgeRarity.RARE),
            ("consistent_100", "Century Champion", "Practiced 100 days in a row", 100, BadgeRarity.LEGENDARY)
        ]
        
        for badge_id, name, desc, days, rarity in consistency_badges:
            badges[badge_id] = Badge(
                badge_id=badge_id,
                name=name,
                description=desc,
                badge_type=BadgeType.CONSISTENCY,
                rarity=rarity,
                icon="📅",
                criteria={"consecutive_days": days}
            )
        
        # Improvement Badges
        badges["rapid_improver"] = Badge(
            badge_id="rapid_improver",
            name="Rapid Improver",
            description="Improved score by 30%+ in any domain",
            badge_type=BadgeType.IMPROVEMENT,
            rarity=BadgeRarity.UNCOMMON,
            icon="📈",
            criteria={"improvement_percentage": 0.30}
        )
        
        # Milestone Badges
        milestone_badges = [
            ("challenges_10", "Getting Started", "Completed 10 challenges", 10, BadgeRarity.COMMON),
            ("challenges_50", "Dedicated Learner", "Completed 50 challenges", 50, BadgeRarity.UNCOMMON),
            ("challenges_100", "Century Club", "Completed 100 challenges", 100, BadgeRarity.RARE),
            ("challenges_500", "Elite Learner", "Completed 500 challenges", 500, BadgeRarity.EPIC),
            ("challenges_1000", "Master Scholar", "Completed 1000 challenges", 1000, BadgeRarity.LEGENDARY)
        ]
        
        for badge_id, name, desc, count, rarity in milestone_badges:
            badges[badge_id] = Badge(
                badge_id=badge_id,
                name=name,
                description=desc,
                badge_type=BadgeType.MILESTONE,
                rarity=rarity,
                icon="🎯",
                criteria={"total_challenges": count}
            )
        
        # Special Badges
        badges["perfect_score"] = Badge(
            badge_id="perfect_score",
            name="Perfectionist",
            description="Achieved 100% accuracy on 10 consecutive challenges",
            badge_type=BadgeType.SPECIAL,
            rarity=BadgeRarity.EPIC,
            icon="💎",
            criteria={"perfect_streak": 10}
        )
        
        badges["early_adopter"] = Badge(
            badge_id="early_adopter",
            name="Early Adopter",
            description="One of the first users of Cyber Compass",
            badge_type=BadgeType.SPECIAL,
            rarity=BadgeRarity.RARE,
            icon="🌟",
            criteria={"user_number": 100}
        )
        
        return badges
    
    def _initialize_level_thresholds(self) -> List[Dict[str, Any]]:
        """Initialize level progression thresholds."""
        return [
            {"level": 1, "name": "Novice", "min_score": 0.0, "min_challenges": 0, "icon": "🌱"},
            {"level": 2, "name": "Learner", "min_score": 0.3, "min_challenges": 10, "icon": "📚"},
            {"level": 3, "name": "Apprentice", "min_score": 0.4, "min_challenges": 25, "icon": "🎓"},
            {"level": 4, "name": "Practitioner", "min_score": 0.5, "min_challenges": 50, "icon": "⚡"},
            {"level": 5, "name": "Skilled", "min_score": 0.6, "min_challenges": 100, "icon": "🔧"},
            {"level": 6, "name": "Proficient", "min_score": 0.7, "min_challenges": 150, "icon": "🎖️"},
            {"level": 7, "name": "Expert", "min_score": 0.75, "min_challenges": 250, "icon": "⭐"},
            {"level": 8, "name": "Advanced", "min_score": 0.8, "min_challenges": 400, "icon": "💫"},
            {"level": 9, "name": "Master", "min_score": 0.85, "min_challenges": 600, "icon": "👑"},
            {"level": 10, "name": "Grandmaster", "min_score": 0.9, "min_challenges": 1000, "icon": "🏆"}
        ]
    
    def check_new_achievements(
        self,
        user_id: str,
        competency_scores: Dict[str, Dict[str, Any]],
        interaction_history: List[Dict[str, Any]],
        existing_achievements: List[str]
    ) -> List[Achievement]:
        """
        Check for newly earned achievements.
        
        Args:
            user_id: User identifier
            competency_scores: User's competency scores
            interaction_history: User's interaction history
            existing_achievements: List of already earned achievement IDs
            
        Returns:
            List of newly earned achievements
        """
        new_achievements = []
        
        # Check mastery badges
        for domain, scores in competency_scores.items():
            badge_id = f"mastery_{domain}"
            if badge_id not in existing_achievements:
                if (scores["score"] >= 0.85 and scores["total_attempts"] >= 10):
                    achievement = Achievement(
                        achievement_id=f"{user_id}_{badge_id}_{datetime.utcnow().timestamp()}",
                        user_id=user_id,
                        badge=self.badges[badge_id],
                        earned_at=datetime.utcnow()
                    )
                    new_achievements.append(achievement)
        
        # Check streak badges
        max_streak = self._calculate_max_streak(interaction_history)
        for badge_id, badge in self.badges.items():
            if badge.badge_type == BadgeType.STREAK and badge_id not in existing_achievements:
                required_streak = badge.criteria["streak_length"]
                if max_streak >= required_streak:
                    achievement = Achievement(
                        achievement_id=f"{user_id}_{badge_id}_{datetime.utcnow().timestamp()}",
                        user_id=user_id,
                        badge=badge,
                        earned_at=datetime.utcnow()
                    )
                    new_achievements.append(achievement)
        
        # Check explorer badge
        if "explorer_all_domains" not in existing_achievements:
            domains_explored = len([d for d, s in competency_scores.items() if s["total_attempts"] > 0])
            if domains_explored >= 6:
                achievement = Achievement(
                    achievement_id=f"{user_id}_explorer_all_domains_{datetime.utcnow().timestamp()}",
                    user_id=user_id,
                    badge=self.badges["explorer_all_domains"],
                    earned_at=datetime.utcnow()
                )
                new_achievements.append(achievement)
        
        # Check consistency badges
        consecutive_days = self._calculate_consecutive_days(interaction_history)
        for badge_id, badge in self.badges.items():
            if badge.badge_type == BadgeType.CONSISTENCY and badge_id not in existing_achievements:
                required_days = badge.criteria["consecutive_days"]
                if consecutive_days >= required_days:
                    achievement = Achievement(
                        achievement_id=f"{user_id}_{badge_id}_{datetime.utcnow().timestamp()}",
                        user_id=user_id,
                        badge=badge,
                        earned_at=datetime.utcnow()
                    )
                    new_achievements.append(achievement)
        
        # Check milestone badges
        total_challenges = len(interaction_history)
        for badge_id, badge in self.badges.items():
            if badge.badge_type == BadgeType.MILESTONE and badge_id not in existing_achievements:
                required_challenges = badge.criteria["total_challenges"]
                if total_challenges >= required_challenges:
                    achievement = Achievement(
                        achievement_id=f"{user_id}_{badge_id}_{datetime.utcnow().timestamp()}",
                        user_id=user_id,
                        badge=badge,
                        earned_at=datetime.utcnow()
                    )
                    new_achievements.append(achievement)
        
        # Check improvement badge
        if "rapid_improver" not in existing_achievements:
            if self._check_rapid_improvement(interaction_history):
                achievement = Achievement(
                    achievement_id=f"{user_id}_rapid_improver_{datetime.utcnow().timestamp()}",
                    user_id=user_id,
                    badge=self.badges["rapid_improver"],
                    earned_at=datetime.utcnow()
                )
                new_achievements.append(achievement)
        
        # Check perfect score badge
        if "perfect_score" not in existing_achievements:
            if self._check_perfect_streak(interaction_history):
                achievement = Achievement(
                    achievement_id=f"{user_id}_perfect_score_{datetime.utcnow().timestamp()}",
                    user_id=user_id,
                    badge=self.badges["perfect_score"],
                    earned_at=datetime.utcnow()
                )
                new_achievements.append(achievement)
        
        return new_achievements
    
    def calculate_level(
        self,
        avg_competency_score: float,
        total_challenges: int
    ) -> Dict[str, Any]:
        """
        Calculate user's current level based on competency and activity.
        
        Args:
            avg_competency_score: Average competency score across all domains
            total_challenges: Total number of challenges completed
            
        Returns:
            Level information including current level, progress to next, and rewards
        """
        current_level = None
        next_level = None
        
        # Find current level
        for i, threshold in enumerate(self.level_thresholds):
            if (avg_competency_score >= threshold["min_score"] and 
                total_challenges >= threshold["min_challenges"]):
                current_level = threshold
                if i < len(self.level_thresholds) - 1:
                    next_level = self.level_thresholds[i + 1]
            else:
                break
        
        if not current_level:
            current_level = self.level_thresholds[0]
            next_level = self.level_thresholds[1]
        
        # Calculate progress to next level
        progress = 0.0
        if next_level:
            score_progress = (avg_competency_score - current_level["min_score"]) / (
                next_level["min_score"] - current_level["min_score"]
            ) if next_level["min_score"] > current_level["min_score"] else 1.0
            
            challenge_progress = (total_challenges - current_level["min_challenges"]) / (
                next_level["min_challenges"] - current_level["min_challenges"]
            ) if next_level["min_challenges"] > current_level["min_challenges"] else 1.0
            
            # Average of both progress metrics
            progress = min(1.0, (score_progress + challenge_progress) / 2)
        
        return {
            "current_level": current_level["level"],
            "level_name": current_level["name"],
            "level_icon": current_level["icon"],
            "next_level": next_level["level"] if next_level else None,
            "next_level_name": next_level["name"] if next_level else "Max Level",
            "progress_to_next": round(progress, 2),
            "requirements_met": {
                "score": avg_competency_score >= (next_level["min_score"] if next_level else 1.0),
                "challenges": total_challenges >= (next_level["min_challenges"] if next_level else 0)
            }
        }
    
    def get_achievement_progress(
        self,
        user_id: str,
        competency_scores: Dict[str, Dict[str, Any]],
        interaction_history: List[Dict[str, Any]],
        existing_achievements: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Get progress towards unearned achievements.
        
        Args:
            user_id: User identifier
            competency_scores: User's competency scores
            interaction_history: User's interaction history
            existing_achievements: List of already earned achievement IDs
            
        Returns:
            List of achievements in progress with completion percentage
        """
        progress_list = []
        
        # Mastery badges progress
        for domain, scores in competency_scores.items():
            badge_id = f"mastery_{domain}"
            if badge_id not in existing_achievements:
                score_progress = min(1.0, scores["score"] / 0.85)
                attempts_progress = min(1.0, scores["total_attempts"] / 10)
                overall_progress = (score_progress + attempts_progress) / 2
                
                progress_list.append({
                    "badge": self.badges[badge_id].to_dict(),
                    "progress": round(overall_progress, 2),
                    "requirements": {
                        "score": f"{scores['score']:.2f} / 0.85",
                        "attempts": f"{scores['total_attempts']} / 10"
                    }
                })
        
        # Streak badges progress
        max_streak = self._calculate_max_streak(interaction_history)
        for badge_id, badge in self.badges.items():
            if badge.badge_type == BadgeType.STREAK and badge_id not in existing_achievements:
                required_streak = badge.criteria["streak_length"]
                if max_streak < required_streak:
                    progress = min(1.0, max_streak / required_streak)
                    progress_list.append({
                        "badge": badge.to_dict(),
                        "progress": round(progress, 2),
                        "requirements": {
                            "current_streak": max_streak,
                            "required_streak": required_streak
                        }
                    })
        
        # Milestone badges progress
        total_challenges = len(interaction_history)
        for badge_id, badge in self.badges.items():
            if badge.badge_type == BadgeType.MILESTONE and badge_id not in existing_achievements:
                required_challenges = badge.criteria["total_challenges"]
                if total_challenges < required_challenges:
                    progress = min(1.0, total_challenges / required_challenges)
                    progress_list.append({
                        "badge": badge.to_dict(),
                        "progress": round(progress, 2),
                        "requirements": {
                            "current": total_challenges,
                            "required": required_challenges
                        }
                    })
        
        # Sort by progress (closest to completion first)
        progress_list.sort(key=lambda x: x["progress"], reverse=True)
        
        return progress_list[:10]  # Return top 10 closest achievements
    
    def generate_motivational_message(
        self,
        level_info: Dict[str, Any],
        new_achievements: List[Achievement],
        locale: str = "en"
    ) -> str:
        """
        Generate motivational message based on progress.
        
        Args:
            level_info: User's level information
            new_achievements: Newly earned achievements
            locale: User's locale (en or pt)
            
        Returns:
            Motivational message
        """
        messages_en = {
            "new_achievement": "🎉 Congratulations! You've earned: {badge_name}!",
            "level_up": "🎊 Level Up! You're now a {level_name}!",
            "close_to_level": "You're {progress}% of the way to {next_level}! Keep going!",
            "keep_practicing": "Great work! Keep practicing to unlock more achievements!",
            "milestone": "Amazing! You've reached a major milestone!"
        }
        
        messages_pt = {
            "new_achievement": "🎉 Parabéns! Você ganhou: {badge_name}!",
            "level_up": "🎊 Subiu de Nível! Agora você é {level_name}!",
            "close_to_level": "Você está {progress}% do caminho para {next_level}! Continue!",
            "keep_practicing": "Ótimo trabalho! Continue praticando para desbloquear mais conquistas!",
            "milestone": "Incrível! Você alcançou um marco importante!"
        }
        
        messages = messages_pt if locale == "pt" else messages_en
        
        if new_achievements:
            badge_names = ", ".join([a.badge.name for a in new_achievements])
            return messages["new_achievement"].format(badge_name=badge_names)
        
        progress = level_info.get("progress_to_next", 0) * 100
        if progress >= 80:
            return messages["close_to_level"].format(
                progress=int(progress),
                next_level=level_info.get("next_level_name", "next level")
            )
        
        return messages["keep_practicing"]
    
    # Helper methods
    
    def _calculate_max_streak(self, interaction_history: List[Dict[str, Any]]) -> int:
        """Calculate maximum correct answer streak."""
        max_streak = 0
        current_streak = 0
        
        for interaction in interaction_history:
            if interaction.get("correct", False):
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        
        return max_streak
    
    def _calculate_consecutive_days(self, interaction_history: List[Dict[str, Any]]) -> int:
        """Calculate consecutive days of activity."""
        if not interaction_history:
            return 0
        
        # Extract unique dates
        dates = set()
        for interaction in interaction_history:
            timestamp = datetime.fromisoformat(interaction.get("timestamp", datetime.utcnow().isoformat()))
            dates.add(timestamp.date())
        
        if not dates:
            return 0
        
        # Sort dates
        sorted_dates = sorted(dates)
        
        # Find longest consecutive sequence
        max_consecutive = 1
        current_consecutive = 1
        
        for i in range(1, len(sorted_dates)):
            diff = (sorted_dates[i] - sorted_dates[i-1]).days
            if diff == 1:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 1
        
        return max_consecutive
    
    def _check_rapid_improvement(self, interaction_history: List[Dict[str, Any]]) -> bool:
        """Check if user has shown rapid improvement (30%+ in any domain)."""
        if len(interaction_history) < 10:
            return False
        
        # Group by domain
        domain_history = {}
        for interaction in interaction_history:
            domain = interaction.get("domain")
            if domain:
                if domain not in domain_history:
                    domain_history[domain] = []
                domain_history[domain].append(interaction)
        
        # Check each domain for improvement
        for domain, history in domain_history.items():
            if len(history) >= 10:
                mid = len(history) // 2
                early = history[:mid]
                recent = history[mid:]
                
                early_score = sum(1 for i in early if i.get("correct", False)) / len(early)
                recent_score = sum(1 for i in recent if i.get("correct", False)) / len(recent)
                
                improvement = recent_score - early_score
                if improvement >= 0.30:
                    return True
        
        return False
    
    def _check_perfect_streak(self, interaction_history: List[Dict[str, Any]]) -> bool:
        """Check for perfect streak of 10 consecutive correct answers."""
        if len(interaction_history) < 10:
            return False
        
        # Check last 10 interactions
        recent = interaction_history[-10:]
        return all(i.get("correct", False) for i in recent)
    
    def get_all_badges(self) -> List[Dict[str, Any]]:
        """Get all available badges."""
        return [badge.to_dict() for badge in self.badges.values()]
    
    def get_badge_by_id(self, badge_id: str) -> Optional[Badge]:
        """Get badge by ID."""
        return self.badges.get(badge_id)
