"""
Analytics API Routes - Real-time analytics dashboard endpoints.

This module provides endpoints for:
- User progress analytics
- Real-time analytics streaming via Server-Sent Events
- Peer comparison data
- Background analytics processing
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from src.models.requests import AnalyticsRequest, LocaleEnum
from src.models.responses import SuccessResponse, ErrorResponse
from src.services.analytics_engine import AnalyticsEngine, CompetencyDomain
from src.api.middleware.auth import get_current_user


router = APIRouter(prefix="/analytics", tags=["analytics"])


# Initialize analytics engine (will be properly initialized in lifespan)
analytics_engine = AnalyticsEngine()


@router.post("/progress", response_model=Dict[str, Any])
async def get_user_progress(
    request: AnalyticsRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get comprehensive user progress analytics.
    
    This endpoint calculates:
    - Competency scores across all domains
    - Learning trends and patterns
    - Personalized recommendations
    - Peer comparison (if enabled)
    
    Args:
        request: Analytics request with user_id and preferences
        current_user: Authenticated user from JWT token
        
    Returns:
        Comprehensive analytics data
    """
    try:
        # Verify user authorization
        if request.user_id != current_user.get("user_id"):
            raise HTTPException(status_code=403, detail="Not authorized to access this user's data")
        
        # Fetch user interaction history (mock data for now - will integrate with database)
        interaction_history = await _fetch_user_interactions(request.user_id, request.time_range_days)
        
        if not interaction_history:
            return {
                "user_id": request.user_id,
                "message": "No interaction history found",
                "competency_scores": {},
                "trends": {},
                "recommendations": [],
                "peer_comparison": {"available": False}
            }
        
        # Calculate competency scores
        competency_scores = analytics_engine.calculate_competency_scores(
            interaction_history,
            use_weighted_recency=True
        )
        
        # Analyze trends
        trends = analytics_engine.analyze_trends(
            interaction_history,
            time_window_days=request.time_range_days
        )
        
        # Generate recommendations
        recommendations = analytics_engine.generate_recommendations(
            competency_scores,
            trends
        )
        
        # Calculate peer comparison if requested
        peer_comparison = {"available": False}
        if request.include_peer_comparison:
            peer_data = await _fetch_anonymized_peer_data(request.user_id)
            peer_comparison = analytics_engine.calculate_peer_percentiles(
                competency_scores,
                peer_data
            )
        
        # Calculate overall metrics
        total_challenges = len(interaction_history)
        correct_count = sum(1 for i in interaction_history if i.get("correct", False))
        accuracy_rate = correct_count / total_challenges if total_challenges > 0 else 0.0
        
        return {
            "user_id": request.user_id,
            "generated_at": datetime.utcnow().isoformat(),
            "time_range_days": request.time_range_days,
            "total_challenges_completed": total_challenges,
            "overall_accuracy": round(accuracy_rate, 3),
            "competency_scores": competency_scores,
            "trends": trends,
            "recommendations": recommendations,
            "peer_comparison": peer_comparison,
            "locale": request.locale
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics processing failed: {str(e)}")


@router.get("/stream/{user_id}")
async def stream_analytics(
    user_id: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Stream real-time analytics updates via Server-Sent Events.
    
    This endpoint provides continuous analytics updates as the user
    completes challenges and activities.
    
    Args:
        user_id: User identifier
        request: FastAPI request object
        current_user: Authenticated user
        
    Returns:
        EventSourceResponse with streaming analytics data
    """
    # Verify authorization
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    async def event_generator():
        """Generate Server-Sent Events for analytics updates."""
        try:
            # Send initial connection confirmation
            yield {
                "event": "connected",
                "data": json.dumps({
                    "message": "Analytics stream connected",
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat()
                })
            }
            
            # Stream analytics updates
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                
                # Fetch latest interaction data
                interaction_history = await _fetch_user_interactions(user_id, time_range_days=30)
                
                if interaction_history:
                    # Calculate current scores
                    competency_scores = analytics_engine.calculate_competency_scores(
                        interaction_history,
                        use_weighted_recency=True
                    )
                    
                    # Calculate trends
                    trends = analytics_engine.analyze_trends(interaction_history)
                    
                    # Send update event
                    yield {
                        "event": "analytics_update",
                        "data": json.dumps({
                            "user_id": user_id,
                            "timestamp": datetime.utcnow().isoformat(),
                            "competency_scores": competency_scores,
                            "overall_trend": trends.get("overall_trend"),
                            "activity_level": trends.get("activity_level"),
                            "total_challenges": len(interaction_history)
                        })
                    }
                
                # Wait before next update (every 10 seconds)
                await asyncio.sleep(10)
                
        except asyncio.CancelledError:
            # Client disconnected
            yield {
                "event": "disconnected",
                "data": json.dumps({
                    "message": "Analytics stream disconnected",
                    "timestamp": datetime.utcnow().isoformat()
                })
            }
    
    return EventSourceResponse(event_generator())


@router.post("/process-background")
async def process_analytics_background(
    user_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> SuccessResponse:
    """
    Trigger background analytics processing for a user.
    
    This endpoint queues analytics processing as a background task,
    useful for heavy computations that don't need immediate results.
    
    Args:
        user_id: User identifier
        background_tasks: FastAPI background tasks
        current_user: Authenticated user
        
    Returns:
        Success response with task ID
    """
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Add background task
    task_id = f"analytics_{user_id}_{datetime.utcnow().timestamp()}"
    background_tasks.add_task(_process_analytics_task, user_id, task_id)
    
    return SuccessResponse(
        message="Analytics processing queued",
        data={
            "task_id": task_id,
            "user_id": user_id,
            "status": "queued"
        }
    )


@router.get("/peer-comparison/{user_id}")
async def get_peer_comparison(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get anonymized peer comparison data.
    
    Args:
        user_id: User identifier
        current_user: Authenticated user
        
    Returns:
        Peer comparison analysis
    """
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        # Fetch user scores
        interaction_history = await _fetch_user_interactions(user_id, time_range_days=90)
        
        if not interaction_history:
            return {
                "available": False,
                "message": "Insufficient user data for comparison"
            }
        
        competency_scores = analytics_engine.calculate_competency_scores(interaction_history)
        
        # Fetch anonymized peer data
        peer_data = await _fetch_anonymized_peer_data(user_id)
        
        # Calculate percentiles
        peer_comparison = analytics_engine.calculate_peer_percentiles(
            competency_scores,
            peer_data
        )
        
        return peer_comparison
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Peer comparison failed: {str(e)}")


@router.get("/domains")
async def get_competency_domains() -> Dict[str, List[str]]:
    """
    Get list of all competency domains.
    
    Returns:
        List of competency domain identifiers and descriptions
    """
    domains = [
        {
            "id": domain,
            "name": domain.replace("_", " ").title(),
            "description": _get_domain_description(domain)
        }
        for domain in CompetencyDomain.all_domains()
    ]
    
    return {"domains": domains}


# Helper functions

async def _fetch_user_interactions(
    user_id: str,
    time_range_days: int = 30
) -> List[Dict[str, Any]]:
    """
    Fetch user interaction history from database.
    
    TODO: Integrate with actual database in Task 9
    For now, returns mock data for testing.
    """
    # Mock data for testing
    cutoff_date = datetime.utcnow() - timedelta(days=time_range_days)
    
    mock_interactions = []
    for i in range(20):
        timestamp = cutoff_date + timedelta(days=i, hours=i % 24)
        mock_interactions.append({
            "user_id": user_id,
            "timestamp": timestamp.isoformat(),
            "domain": CompetencyDomain.all_domains()[i % 6],
            "correct": i % 3 != 0,  # 66% accuracy
            "difficulty": (i % 3) + 1,
            "challenge_type": "ethics_feedback"
        })
    
    return mock_interactions


async def _fetch_anonymized_peer_data(user_id: str) -> List[Dict[str, float]]:
    """
    Fetch anonymized peer score data.
    
    TODO: Integrate with actual database in Task 9
    Returns mock peer data for testing.
    """
    # Mock peer data (50 anonymized users)
    import random
    
    peer_data = []
    for _ in range(50):
        peer_scores = {
            domain: random.uniform(0.4, 0.9)
            for domain in CompetencyDomain.all_domains()
        }
        peer_data.append(peer_scores)
    
    return peer_data


async def _process_analytics_task(user_id: str, task_id: str):
    """
    Background task for processing analytics.
    
    This runs asynchronously and can perform heavy computations
    without blocking the API response.
    """
    try:
        # Simulate heavy processing
        await asyncio.sleep(2)
        
        # Fetch and process data
        interaction_history = await _fetch_user_interactions(user_id, time_range_days=365)
        
        if interaction_history:
            competency_scores = analytics_engine.calculate_competency_scores(interaction_history)
            trends = analytics_engine.analyze_trends(interaction_history, time_window_days=90)
            recommendations = analytics_engine.generate_recommendations(competency_scores, trends)
            
            # TODO: Store results in database (Task 9)
            print(f"✅ Background analytics task {task_id} completed for user {user_id}")
        
    except Exception as e:
        print(f"❌ Background analytics task {task_id} failed: {str(e)}")


def _get_domain_description(domain: str) -> str:
    """Get description for a competency domain."""
    descriptions = {
        "privacy_awareness": "Understanding and protecting personal information online",
        "security_practices": "Implementing secure behaviors and recognizing threats",
        "disinformation_detection": "Identifying false or misleading information",
        "social_engineering_resistance": "Recognizing and resisting manipulation tactics",
        "deepfake_detection": "Identifying manipulated audio, video, and images",
        "ethical_decision_making": "Making informed ethical choices in digital contexts"
    }
    return descriptions.get(domain, "Cyber ethics competency domain")



# Gamification endpoints

from src.services.gamification import GamificationSystem

# Initialize gamification system
gamification_system = GamificationSystem()


@router.get("/achievements/{user_id}")
async def get_user_achievements(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get user's earned achievements and badges.
    
    Args:
        user_id: User identifier
        current_user: Authenticated user
        
    Returns:
        User's achievements, level, and progress
    """
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        # Fetch user data
        interaction_history = await _fetch_user_interactions(user_id, time_range_days=365)
        
        if not interaction_history:
            return {
                "user_id": user_id,
                "level": gamification_system.level_thresholds[0],
                "achievements": [],
                "badges_earned": 0,
                "total_badges": len(gamification_system.badges)
            }
        
        # Calculate competency scores
        competency_scores = analytics_engine.calculate_competency_scores(interaction_history)
        
        # Get existing achievements (mock - will integrate with database in Task 9)
        existing_achievements = []  # TODO: Fetch from database
        
        # Check for new achievements
        new_achievements = gamification_system.check_new_achievements(
            user_id,
            competency_scores,
            interaction_history,
            existing_achievements
        )
        
        # Calculate level
        avg_score = sum(s["score"] for s in competency_scores.values()) / len(competency_scores)
        level_info = gamification_system.calculate_level(avg_score, len(interaction_history))
        
        # Get achievement progress
        achievement_progress = gamification_system.get_achievement_progress(
            user_id,
            competency_scores,
            interaction_history,
            existing_achievements
        )
        
        # Generate motivational message
        motivational_message = gamification_system.generate_motivational_message(
            level_info,
            new_achievements,
            locale="en"  # TODO: Get from user preferences
        )
        
        return {
            "user_id": user_id,
            "level": level_info,
            "achievements": [a.to_dict() for a in new_achievements],
            "achievement_progress": achievement_progress,
            "badges_earned": len(existing_achievements) + len(new_achievements),
            "total_badges": len(gamification_system.badges),
            "motivational_message": motivational_message,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch achievements: {str(e)}")


@router.get("/badges")
async def get_all_badges() -> Dict[str, Any]:
    """
    Get all available badges in the system.
    
    Returns:
        List of all badges with descriptions and criteria
    """
    badges = gamification_system.get_all_badges()
    
    # Group badges by type
    badges_by_type = {}
    for badge in badges:
        badge_type = badge["type"]
        if badge_type not in badges_by_type:
            badges_by_type[badge_type] = []
        badges_by_type[badge_type].append(badge)
    
    return {
        "total_badges": len(badges),
        "badges_by_type": badges_by_type,
        "all_badges": badges
    }


@router.get("/leaderboard")
async def get_leaderboard(
    time_range: str = "all_time",
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get anonymized leaderboard data.
    
    Args:
        time_range: Time range for leaderboard (all_time, monthly, weekly)
        limit: Maximum number of entries to return
        current_user: Authenticated user
        
    Returns:
        Anonymized leaderboard with rankings
    """
    try:
        # TODO: Implement actual leaderboard with database in Task 9
        # For now, return mock data
        
        import random
        
        leaderboard_entries = []
        for i in range(min(limit, 50)):
            leaderboard_entries.append({
                "rank": i + 1,
                "username": f"User{random.randint(1000, 9999)}",  # Anonymized
                "level": random.randint(1, 10),
                "total_score": random.randint(100, 10000),
                "badges_earned": random.randint(5, 50),
                "is_current_user": False
            })
        
        return {
            "time_range": time_range,
            "total_entries": len(leaderboard_entries),
            "leaderboard": leaderboard_entries,
            "privacy_note": "All usernames are anonymized for privacy"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leaderboard: {str(e)}")


@router.post("/celebrate-milestone")
async def celebrate_milestone(
    user_id: str,
    milestone_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Trigger milestone celebration animation/notification.
    
    Args:
        user_id: User identifier
        milestone_type: Type of milestone (level_up, new_badge, streak, etc.)
        current_user: Authenticated user
        
    Returns:
        Celebration data for frontend animation
    """
    if user_id != current_user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    celebrations = {
        "level_up": {
            "title": "🎊 Level Up!",
            "message": "You've reached a new level!",
            "animation": "confetti",
            "sound": "level_up.mp3",
            "duration_ms": 3000
        },
        "new_badge": {
            "title": "🏆 New Badge!",
            "message": "You've earned a new badge!",
            "animation": "badge_reveal",
            "sound": "achievement.mp3",
            "duration_ms": 2500
        },
        "streak": {
            "title": "🔥 Streak!",
            "message": "You're on fire!",
            "animation": "fire",
            "sound": "streak.mp3",
            "duration_ms": 2000
        },
        "milestone": {
            "title": "🎯 Milestone!",
            "message": "You've reached an important milestone!",
            "animation": "fireworks",
            "sound": "milestone.mp3",
            "duration_ms": 3500
        }
    }
    
    celebration = celebrations.get(milestone_type, celebrations["milestone"])
    
    return {
        "user_id": user_id,
        "milestone_type": milestone_type,
        "celebration": celebration,
        "timestamp": datetime.utcnow().isoformat()
    }
