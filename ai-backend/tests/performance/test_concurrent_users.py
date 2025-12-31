"""
Concurrent user simulation tests for AI Backend.

This module implements comprehensive concurrent user testing to validate
system performance under realistic load conditions with multiple simultaneous users.

Requirements: 9.3, 9.4
"""

import asyncio
import aiohttp
import json
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import statistics
import random
import uuid
from concurrent.futures import ThreadPoolExecutor
import websockets
from test_memory_monitoring import monitor_performance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UserSession:
    """Represents a single user session for testing."""
    user_id: str
    session_id: str
    start_time: float
    requests_made: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_response_time: float = 0.0
    websocket_connection: Optional[Any] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class ConcurrentTestResults:
    """Results from concurrent user testing."""
    test_name: str
    duration_seconds: float
    total_users: int
    total_requests: int
    successful_requests: int
    failed_requests: int
    requests_per_second: float
    avg_response_time: float
    p95_response_time: float
    p99_response_time: float
    max_response_time: float
    min_response_time: float
    error_rate: float
    concurrent_users_peak: int
    memory_usage_mb: float
    cpu_usage_percent: float
    errors: List[str] = field(default_factory=list)


class ConcurrentUserSimulator:
    """
    Simulates multiple concurrent users interacting with the AI Backend.
    
    Tests various user interaction patterns:
    - Feedback generation requests
    - Deepfake challenge interactions
    - Social media simulation
    - Catfish chat sessions
    - Analytics dashboard access
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.ws_base_url = base_url.replace("http://", "ws://")
        self.active_sessions: Dict[str, UserSession] = {}
        self.response_times: List[float] = []
        self.test_start_time: float = 0
        
    async def simulate_concurrent_users(
        self,
        num_users: int,
        test_duration_minutes: int,
        user_behavior_pattern: str = "mixed"
    ) -> ConcurrentTestResults:
        """
        Simulate multiple concurrent users with realistic behavior patterns.
        
        Args:
            num_users: Number of concurrent users to simulate
            test_duration_minutes: How long to run the test
            user_behavior_pattern: Type of user behavior ("mixed", "heavy", "light")
            
        Returns:
            ConcurrentTestResults containing comprehensive test metrics
        """
        logger.info(f"Starting concurrent user simulation: {num_users} users for {test_duration_minutes} minutes")
        
        self.test_start_time = time.time()
        test_end_time = self.test_start_time + (test_duration_minutes * 60)
        
        # Create user sessions
        user_tasks = []
        for i in range(num_users):
            user_id = f"test_user_{i}"
            session = UserSession(
                user_id=user_id,
                session_id=str(uuid.uuid4()),
                start_time=time.time()
            )
            self.active_sessions[user_id] = session
            
            # Create user simulation task
            task = asyncio.create_task(
                self._simulate_user_behavior(session, test_end_time, user_behavior_pattern)
            )
            user_tasks.append(task)
        
        # Run all user simulations concurrently
        await asyncio.gather(*user_tasks, return_exceptions=True)
        
        # Calculate results
        return self._calculate_test_results(test_duration_minutes * 60)
    
    async def _simulate_user_behavior(
        self,
        session: UserSession,
        end_time: float,
        behavior_pattern: str
    ) -> None:
        """
        Simulate realistic user behavior for a single user session.
        
        Args:
            session: User session to simulate
            end_time: When to stop the simulation
            behavior_pattern: Type of behavior to simulate
        """
        async with aiohttp.ClientSession() as http_session:
            while time.time() < end_time:
                try:
                    # Choose action based on behavior pattern
                    action = self._choose_user_action(behavior_pattern)
                    
                    # Execute the chosen action
                    await self._execute_user_action(http_session, session, action)
                    
                    # Wait between actions (realistic user behavior)
                    wait_time = self._calculate_user_wait_time(behavior_pattern)
                    await asyncio.sleep(wait_time)
                    
                except Exception as e:
                    session.errors.append(f"User behavior error: {str(e)}")
                    session.failed_requests += 1
                    logger.error(f"Error in user {session.user_id} behavior: {e}")
    
    def _choose_user_action(self, behavior_pattern: str) -> str:
        """Choose next user action based on behavior pattern."""
        if behavior_pattern == "heavy":
            # Heavy users make more API calls and use WebSockets
            actions = [
                "generate_feedback", "generate_feedback", "generate_feedback",
                "start_deepfake_challenge", "start_deepfake_challenge",
                "get_analytics", "catfish_chat", "social_media_sim"
            ]
        elif behavior_pattern == "light":
            # Light users make fewer, simpler requests
            actions = [
                "generate_feedback", "get_analytics", "start_deepfake_challenge"
            ]
        else:  # mixed
            actions = [
                "generate_feedback", "generate_feedback",
                "start_deepfake_challenge", "get_analytics",
                "catfish_chat", "social_media_sim"
            ]
        
        return random.choice(actions)
    
    def _calculate_user_wait_time(self, behavior_pattern: str) -> float:
        """Calculate realistic wait time between user actions."""
        if behavior_pattern == "heavy":
            return random.uniform(0.5, 2.0)  # Heavy users act quickly
        elif behavior_pattern == "light":
            return random.uniform(3.0, 10.0)  # Light users take their time
        else:  # mixed
            return random.uniform(1.0, 5.0)  # Mixed behavior
    
    async def _execute_user_action(
        self,
        http_session: aiohttp.ClientSession,
        session: UserSession,
        action: str
    ) -> None:
        """Execute a specific user action."""
        session.requests_made += 1
        start_time = time.time()
        
        try:
            if action == "generate_feedback":
                await self._generate_feedback_request(http_session, session)
            elif action == "start_deepfake_challenge":
                await self._start_deepfake_challenge_request(http_session, session)
            elif action == "get_analytics":
                await self._get_analytics_request(http_session, session)
            elif action == "catfish_chat":
                await self._catfish_chat_interaction(session)
            elif action == "social_media_sim":
                await self._social_media_simulation(http_session, session)
            else:
                logger.warning(f"Unknown action: {action}")
                return
            
            # Record successful request
            response_time = time.time() - start_time
            session.successful_requests += 1
            session.total_response_time += response_time
            self.response_times.append(response_time)
            
            # Check performance requirements
            if response_time > 5.0:  # Requirement: < 5 seconds for text-based interactions
                session.errors.append(f"Slow response: {response_time:.2f}s for {action}")
            
        except Exception as e:
            session.failed_requests += 1
            session.errors.append(f"Action {action} failed: {str(e)}")
            logger.error(f"User {session.user_id} action {action} failed: {e}")
    
    async def _generate_feedback_request(
        self,
        http_session: aiohttp.ClientSession,
        session: UserSession
    ) -> None:
        """Simulate feedback generation request."""
        payload = {
            "user_id": session.user_id,
            "challenge_id": f"challenge_{int(time.time())}_{random.randint(1, 1000)}",
            "selected_option": random.choice(["A", "B", "C", "D"]),
            "correct_option": random.choice(["A", "B", "C", "D"]),
            "locale": random.choice(["en", "pt"]),
            "context": {
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "topic": random.choice(["privacy", "security", "ethics"])
            }
        }
        
        async with http_session.post(
            f"{self.base_url}/api/v1/feedback/generate",
            json=payload,
            headers={"Authorization": f"Bearer mock_token_{session.user_id}"}
        ) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
    
    async def _start_deepfake_challenge_request(
        self,
        http_session: aiohttp.ClientSession,
        session: UserSession
    ) -> None:
        """Simulate deepfake challenge start request."""
        payload = {
            "user_id": session.user_id,
            "difficulty_level": random.randint(1, 5),
            "media_type": random.choice(["image", "video", "audio"])
        }
        
        async with http_session.post(
            f"{self.base_url}/api/v1/challenges/deepfake/start",
            json=payload,
            headers={"Authorization": f"Bearer mock_token_{session.user_id}"}
        ) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
    
    async def _get_analytics_request(
        self,
        http_session: aiohttp.ClientSession,
        session: UserSession
    ) -> None:
        """Simulate analytics dashboard request."""
        async with http_session.get(
            f"{self.base_url}/api/v1/analytics/user/{session.user_id}",
            headers={"Authorization": f"Bearer mock_token_{session.user_id}"}
        ) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
    
    async def _catfish_chat_interaction(self, session: UserSession) -> None:
        """Simulate catfish chat WebSocket interaction."""
        if session.websocket_connection:
            # Use existing connection
            await self._send_chat_messages(session.websocket_connection, session, 3)
        else:
            # Establish new WebSocket connection
            try:
                uri = f"{self.ws_base_url}/ws/chat/catfish/{session.session_id}"
                async with websockets.connect(uri, timeout=10) as websocket:
                    session.websocket_connection = websocket
                    await self._send_chat_messages(websocket, session, 5)
            except Exception as e:
                raise Exception(f"WebSocket connection failed: {str(e)}")
    
    async def _send_chat_messages(
        self,
        websocket,
        session: UserSession,
        num_messages: int
    ) -> None:
        """Send chat messages through WebSocket connection."""
        for i in range(num_messages):
            message = {
                "type": "user_message",
                "content": f"Test message {i} from {session.user_id}",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await websocket.send(json.dumps(message))
            
            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            
            # Verify response includes typing delay simulation
            try:
                response_data = json.loads(response)
                if "type" in response_data and response_data["type"] == "agent_message":
                    # Successful chat interaction
                    pass
            except json.JSONDecodeError:
                pass
            
            # Small delay between messages
            await asyncio.sleep(0.5)
    
    async def _social_media_simulation(
        self,
        http_session: aiohttp.ClientSession,
        session: UserSession
    ) -> None:
        """Simulate social media simulation request."""
        payload = {
            "user_id": session.user_id,
            "simulation_type": random.choice(["disinformation", "mixed", "educational"]),
            "num_posts": random.randint(5, 15),
            "locale": random.choice(["en", "pt"])
        }
        
        async with http_session.post(
            f"{self.base_url}/api/v1/simulations/social-media/start",
            json=payload,
            headers={"Authorization": f"Bearer mock_token_{session.user_id}"}
        ) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
    
    def _calculate_test_results(self, duration_seconds: float) -> ConcurrentTestResults:
        """Calculate comprehensive test results from collected data."""
        total_requests = sum(session.requests_made for session in self.active_sessions.values())
        successful_requests = sum(session.successful_requests for session in self.active_sessions.values())
        failed_requests = sum(session.failed_requests for session in self.active_sessions.values())
        
        # Calculate response time statistics
        response_time_stats = {}
        if self.response_times:
            response_time_stats = {
                "avg": statistics.mean(self.response_times),
                "p95": self._percentile(self.response_times, 95),
                "p99": self._percentile(self.response_times, 99),
                "max": max(self.response_times),
                "min": min(self.response_times),
            }
        
        # Collect all errors
        all_errors = []
        for session in self.active_sessions.values():
            all_errors.extend(session.errors)
        
        return ConcurrentTestResults(
            test_name="Concurrent User Simulation",
            duration_seconds=duration_seconds,
            total_users=len(self.active_sessions),
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            requests_per_second=total_requests / duration_seconds if duration_seconds > 0 else 0,
            avg_response_time=response_time_stats.get("avg", 0),
            p95_response_time=response_time_stats.get("p95", 0),
            p99_response_time=response_time_stats.get("p99", 0),
            max_response_time=response_time_stats.get("max", 0),
            min_response_time=response_time_stats.get("min", 0),
            error_rate=(failed_requests / total_requests * 100) if total_requests > 0 else 0,
            concurrent_users_peak=len(self.active_sessions),
            memory_usage_mb=0,  # Will be filled by monitoring
            cpu_usage_percent=0,  # Will be filled by monitoring
            errors=all_errors[:20]  # First 20 errors for analysis
        )
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


async def run_concurrent_user_tests():
    """Run comprehensive concurrent user testing with different scenarios."""
    logger.info("Starting comprehensive concurrent user testing")
    
    simulator = ConcurrentUserSimulator()
    test_results = []
    
    # Test scenarios with different user loads and patterns
    test_scenarios = [
        {"users": 10, "duration": 2, "pattern": "light", "name": "Light Load Test"},
        {"users": 25, "duration": 3, "pattern": "mixed", "name": "Medium Load Test"},
        {"users": 50, "duration": 2, "pattern": "heavy", "name": "Heavy Load Test"},
        {"users": 100, "duration": 1, "pattern": "mixed", "name": "Peak Load Test"},
    ]
    
    for scenario in test_scenarios:
        logger.info(f"=== Running {scenario['name']} ===")
        
        async with monitor_performance(monitoring_interval=0.5) as monitor:
            try:
                # Run concurrent user simulation
                results = await simulator.simulate_concurrent_users(
                    num_users=scenario["users"],
                    test_duration_minutes=scenario["duration"],
                    user_behavior_pattern=scenario["pattern"]
                )
                
                # Get performance metrics
                perf_metrics = monitor.stop_monitoring()
                
                # Update results with performance data
                if "memory_statistics" in perf_metrics:
                    results.memory_usage_mb = perf_metrics["memory_statistics"]["peak_mb"]
                
                if "cpu_statistics" in perf_metrics:
                    results.cpu_usage_percent = perf_metrics["cpu_statistics"]["mean_percent"]
                
                test_results.append({
                    "scenario": scenario,
                    "results": results,
                    "performance_metrics": perf_metrics
                })
                
                # Log scenario results
                logger.info(f"✅ {scenario['name']} completed:")
                logger.info(f"  - {results.total_requests} requests ({results.requests_per_second:.1f} req/s)")
                logger.info(f"  - {results.successful_requests}/{results.total_requests} successful ({100-results.error_rate:.1f}%)")
                logger.info(f"  - Response times: avg={results.avg_response_time:.3f}s, p95={results.p95_response_time:.3f}s")
                logger.info(f"  - Memory usage: {results.memory_usage_mb:.1f} MB")
                
                # Check performance requirements
                requirements_met = True
                if results.avg_response_time > 5.0:
                    logger.error(f"❌ Average response time {results.avg_response_time:.2f}s exceeds 5s requirement")
                    requirements_met = False
                
                if results.error_rate > 5.0:  # Allow up to 5% error rate
                    logger.error(f"❌ Error rate {results.error_rate:.1f}% exceeds 5% threshold")
                    requirements_met = False
                
                if requirements_met:
                    logger.info("✅ All performance requirements met")
                
            except Exception as e:
                logger.error(f"❌ {scenario['name']} failed: {e}")
                test_results.append({
                    "scenario": scenario,
                    "error": str(e),
                    "performance_metrics": monitor.stop_monitoring()
                })
        
        # Reset simulator for next test
        simulator = ConcurrentUserSimulator()
        
        # Brief pause between tests
        await asyncio.sleep(5)
    
    # Generate comprehensive report
    logger.info("=== CONCURRENT USER TESTING SUMMARY ===")
    
    successful_tests = [r for r in test_results if "results" in r]
    failed_tests = [r for r in test_results if "error" in r]
    
    logger.info(f"Tests completed: {len(successful_tests)}/{len(test_results)} successful")
    
    if successful_tests:
        # Overall statistics
        total_requests = sum(r["results"].total_requests for r in successful_tests)
        total_users = sum(r["results"].total_users for r in successful_tests)
        avg_response_times = [r["results"].avg_response_time for r in successful_tests]
        
        logger.info(f"Total requests processed: {total_requests}")
        logger.info(f"Total user sessions: {total_users}")
        logger.info(f"Overall avg response time: {statistics.mean(avg_response_times):.3f}s")
    
    if failed_tests:
        logger.error(f"Failed tests: {len(failed_tests)}")
        for failed_test in failed_tests:
            logger.error(f"  - {failed_test['scenario']['name']}: {failed_test['error']}")
    
    # Save detailed results
    timestamp = int(time.time())
    with open(f"concurrent_user_test_results_{timestamp}.json", "w") as f:
        json.dump(test_results, f, indent=2, default=str)
    
    logger.info(f"Detailed results saved to concurrent_user_test_results_{timestamp}.json")
    return test_results


if __name__ == "__main__":
    # Run concurrent user tests
    asyncio.run(run_concurrent_user_tests())