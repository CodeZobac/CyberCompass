"""
Load testing suite for AI Backend using Locust.

This module implements comprehensive load testing for:
- Concurrent user simulation
- API endpoint performance under load
- WebSocket connection limits
- Memory usage monitoring
- Response time analysis

Requirements: 9.3, 9.4
"""

import asyncio
import json
import time
from typing import Dict, List, Any
from locust import HttpUser, task, between, events
from locust.contrib.fastapi import FastAPIUser
import websocket
import threading
import psutil
import logging
from datetime import datetime, timedelta
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Collects and analyzes performance metrics during load testing."""
    
    def __init__(self):
        self.response_times: List[float] = []
        self.memory_usage: List[float] = []
        self.cpu_usage: List[float] = []
        self.websocket_connections: List[int] = []
        self.error_rates: List[float] = []
        self.start_time = time.time()
        
    def record_response_time(self, response_time: float):
        """Record API response time."""
        self.response_times.append(response_time)
        
    def record_system_metrics(self):
        """Record system resource usage."""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()
        
        self.memory_usage.append(memory_mb)
        self.cpu_usage.append(cpu_percent)
        
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate performance statistics."""
        return {
            "response_times": {
                "mean": statistics.mean(self.response_times) if self.response_times else 0,
                "median": statistics.median(self.response_times) if self.response_times else 0,
                "p95": self._percentile(self.response_times, 95) if self.response_times else 0,
                "p99": self._percentile(self.response_times, 99) if self.response_times else 0,
                "max": max(self.response_times) if self.response_times else 0,
                "min": min(self.response_times) if self.response_times else 0,
            },
            "memory_usage": {
                "mean_mb": statistics.mean(self.memory_usage) if self.memory_usage else 0,
                "max_mb": max(self.memory_usage) if self.memory_usage else 0,
                "min_mb": min(self.memory_usage) if self.memory_usage else 0,
            },
            "cpu_usage": {
                "mean_percent": statistics.mean(self.cpu_usage) if self.cpu_usage else 0,
                "max_percent": max(self.cpu_usage) if self.cpu_usage else 0,
            },
            "test_duration_seconds": time.time() - self.start_time,
            "total_requests": len(self.response_times),
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


# Global metrics collector
metrics = PerformanceMetrics()


class AIBackendUser(HttpUser):
    """
    Simulates a user interacting with the AI Backend API.
    
    Tests various endpoints under concurrent load to measure:
    - Response times under load
    - System resource usage
    - Error rates
    - Throughput capacity
    """
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    host = "http://localhost:8000"
    
    def on_start(self):
        """Initialize user session."""
        self.user_id = f"test_user_{self.environment.runner.user_count}"
        self.session_id = f"session_{int(time.time())}_{id(self)}"
        
        # Authenticate user (mock authentication)
        self.auth_token = self._get_auth_token()
        self.client.headers.update({"Authorization": f"Bearer {self.auth_token}"})
        
    def _get_auth_token(self) -> str:
        """Mock authentication token generation."""
        return f"mock_token_{self.user_id}"
    
    @task(3)
    def generate_feedback(self):
        """Test feedback generation endpoint under load."""
        start_time = time.time()
        
        payload = {
            "user_id": self.user_id,
            "challenge_id": f"challenge_{int(time.time())}",
            "selected_option": "A",
            "correct_option": "B",
            "locale": "en",
            "context": {"difficulty": "medium"}
        }
        
        with self.client.post(
            "/api/v1/feedback/generate",
            json=payload,
            catch_response=True
        ) as response:
            response_time = time.time() - start_time
            metrics.record_response_time(response_time)
            
            if response.status_code == 200:
                response.success()
                # Verify response time requirement (< 5 seconds for text-based interactions)
                if response_time > 5.0:
                    response.failure(f"Response time {response_time:.2f}s exceeds 5s requirement")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(2)
    def start_deepfake_challenge(self):
        """Test deepfake challenge endpoint under load."""
        start_time = time.time()
        
        payload = {
            "user_id": self.user_id,
            "difficulty_level": 1,
            "media_type": "image"
        }
        
        with self.client.post(
            "/api/v1/challenges/deepfake/start",
            json=payload,
            catch_response=True
        ) as response:
            response_time = time.time() - start_time
            metrics.record_response_time(response_time)
            
            if response.status_code == 200:
                response.success()
                # Verify content delivery requirement (< 5 seconds)
                if response_time > 5.0:
                    response.failure(f"Challenge start time {response_time:.2f}s exceeds 5s requirement")
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(2)
    def get_user_analytics(self):
        """Test analytics endpoint under load."""
        start_time = time.time()
        
        with self.client.get(
            f"/api/v1/analytics/user/{self.user_id}",
            catch_response=True
        ) as response:
            response_time = time.time() - start_time
            metrics.record_response_time(response_time)
            
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"HTTP {response.status_code}")
    
    @task(1)
    def upload_media_file(self):
        """Test media upload endpoint under load."""
        start_time = time.time()
        
        # Simulate small media file upload (1MB)
        mock_file_data = b"0" * (1024 * 1024)  # 1MB of zeros
        
        files = {
            "file": ("test_media.mp4", mock_file_data, "video/mp4")
        }
        
        with self.client.post(
            "/api/v1/media/upload",
            files=files,
            catch_response=True
        ) as response:
            response_time = time.time() - start_time
            metrics.record_response_time(response_time)
            
            if response.status_code == 200:
                response.success()
                # Verify media processing requirement (< 30 seconds for files up to 50MB)
                if response_time > 30.0:
                    response.failure(f"Media upload time {response_time:.2f}s exceeds 30s requirement")
            else:
                response.failure(f"HTTP {response.status_code}")


class WebSocketLoadTester:
    """
    Tests WebSocket connection limits and performance.
    
    Simulates multiple concurrent WebSocket connections to test:
    - Connection limits
    - Message throughput
    - Connection stability
    - Memory usage under WebSocket load
    """
    
    def __init__(self, base_url: str = "ws://localhost:8000"):
        self.base_url = base_url
        self.connections: List[websocket.WebSocket] = []
        self.message_counts: Dict[str, int] = {}
        self.connection_times: List[float] = []
        self.message_response_times: List[float] = []
        
    def test_websocket_connections(self, max_connections: int = 100) -> Dict[str, Any]:
        """
        Test WebSocket connection limits and performance.
        
        Args:
            max_connections: Maximum number of concurrent connections to test
            
        Returns:
            Dictionary containing test results and metrics
        """
        logger.info(f"Starting WebSocket load test with {max_connections} connections")
        
        results = {
            "successful_connections": 0,
            "failed_connections": 0,
            "connection_times": [],
            "message_response_times": [],
            "errors": []
        }
        
        # Test connection establishment
        for i in range(max_connections):
            try:
                start_time = time.time()
                ws = websocket.create_connection(
                    f"{self.base_url}/ws/chat/{i}",
                    timeout=10
                )
                connection_time = time.time() - start_time
                
                self.connections.append(ws)
                results["successful_connections"] += 1
                results["connection_times"].append(connection_time)
                
                logger.info(f"Connection {i+1}/{max_connections} established in {connection_time:.3f}s")
                
            except Exception as e:
                results["failed_connections"] += 1
                results["errors"].append(f"Connection {i}: {str(e)}")
                logger.error(f"Failed to establish connection {i}: {e}")
        
        # Test message throughput with established connections
        if self.connections:
            self._test_message_throughput(results)
        
        # Clean up connections
        self._cleanup_connections()
        
        # Calculate statistics
        if results["connection_times"]:
            results["avg_connection_time"] = statistics.mean(results["connection_times"])
            results["max_connection_time"] = max(results["connection_times"])
        
        if results["message_response_times"]:
            results["avg_message_response_time"] = statistics.mean(results["message_response_times"])
            results["p95_message_response_time"] = self._percentile(results["message_response_times"], 95)
        
        return results
    
    def _test_message_throughput(self, results: Dict[str, Any]):
        """Test message sending and response times."""
        logger.info(f"Testing message throughput with {len(self.connections)} connections")
        
        messages_per_connection = 10
        threads = []
        
        def send_messages(ws, connection_id):
            """Send messages through a WebSocket connection."""
            for msg_id in range(messages_per_connection):
                try:
                    start_time = time.time()
                    message = {
                        "type": "user_message",
                        "content": f"Test message {msg_id} from connection {connection_id}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    ws.send(json.dumps(message))
                    response = ws.recv()
                    response_time = time.time() - start_time
                    
                    results["message_response_times"].append(response_time)
                    
                    # Verify typing delay simulation (1-3 seconds requirement)
                    if response_time < 1.0 or response_time > 5.0:
                        logger.warning(f"Message response time {response_time:.2f}s outside expected range")
                    
                except Exception as e:
                    results["errors"].append(f"Message error on connection {connection_id}: {str(e)}")
        
        # Start message sending threads
        for i, ws in enumerate(self.connections[:10]):  # Test with first 10 connections
            thread = threading.Thread(target=send_messages, args=(ws, i))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=60)  # 60 second timeout
    
    def _cleanup_connections(self):
        """Close all WebSocket connections."""
        for ws in self.connections:
            try:
                ws.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket: {e}")
        
        self.connections.clear()
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


class SystemResourceMonitor:
    """
    Monitors system resources during load testing.
    
    Tracks:
    - Memory usage
    - CPU utilization
    - Network connections
    - Disk I/O
    """
    
    def __init__(self, monitoring_interval: float = 1.0):
        self.monitoring_interval = monitoring_interval
        self.monitoring = False
        self.metrics_history: List[Dict[str, Any]] = []
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start resource monitoring in background thread."""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.start()
        logger.info("Started system resource monitoring")
    
    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return collected metrics."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        
        logger.info("Stopped system resource monitoring")
        return self._calculate_resource_statistics()
    
    def _monitor_resources(self):
        """Monitor system resources continuously."""
        while self.monitoring:
            try:
                # Get current process info
                process = psutil.Process()
                
                # Collect metrics
                metrics_snapshot = {
                    "timestamp": time.time(),
                    "memory_mb": process.memory_info().rss / 1024 / 1024,
                    "memory_percent": process.memory_percent(),
                    "cpu_percent": process.cpu_percent(),
                    "num_threads": process.num_threads(),
                    "num_fds": process.num_fds() if hasattr(process, 'num_fds') else 0,
                    "connections": len(process.connections()),
                }
                
                # System-wide metrics
                system_memory = psutil.virtual_memory()
                metrics_snapshot.update({
                    "system_memory_percent": system_memory.percent,
                    "system_cpu_percent": psutil.cpu_percent(),
                    "system_load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0],
                })
                
                self.metrics_history.append(metrics_snapshot)
                
            except Exception as e:
                logger.error(f"Error collecting resource metrics: {e}")
            
            time.sleep(self.monitoring_interval)
    
    def _calculate_resource_statistics(self) -> Dict[str, Any]:
        """Calculate statistics from collected metrics."""
        if not self.metrics_history:
            return {}
        
        # Extract metric series
        memory_mb = [m["memory_mb"] for m in self.metrics_history]
        cpu_percent = [m["cpu_percent"] for m in self.metrics_history]
        connections = [m["connections"] for m in self.metrics_history]
        
        return {
            "monitoring_duration_seconds": len(self.metrics_history) * self.monitoring_interval,
            "memory_usage": {
                "mean_mb": statistics.mean(memory_mb),
                "max_mb": max(memory_mb),
                "min_mb": min(memory_mb),
                "final_mb": memory_mb[-1],
            },
            "cpu_usage": {
                "mean_percent": statistics.mean(cpu_percent),
                "max_percent": max(cpu_percent),
            },
            "connections": {
                "mean": statistics.mean(connections),
                "max": max(connections),
                "final": connections[-1],
            },
            "samples_collected": len(self.metrics_history),
        }


# Locust event handlers for metrics collection
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, context, **kwargs):
    """Handle request completion events."""
    if not exception:
        metrics.record_response_time(response_time / 1000.0)  # Convert to seconds
    
    # Record system metrics periodically
    if int(time.time()) % 5 == 0:  # Every 5 seconds
        metrics.record_system_metrics()


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Handle test start event."""
    logger.info("Load test started - initializing performance monitoring")
    metrics.start_time = time.time()


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Handle test stop event and generate performance report."""
    logger.info("Load test completed - generating performance report")
    
    stats = metrics.get_statistics()
    
    # Log performance summary
    logger.info("=== PERFORMANCE TEST RESULTS ===")
    logger.info(f"Test Duration: {stats['test_duration_seconds']:.2f} seconds")
    logger.info(f"Total Requests: {stats['total_requests']}")
    logger.info(f"Mean Response Time: {stats['response_times']['mean']:.3f}s")
    logger.info(f"95th Percentile Response Time: {stats['response_times']['p95']:.3f}s")
    logger.info(f"Max Response Time: {stats['response_times']['max']:.3f}s")
    logger.info(f"Mean Memory Usage: {stats['memory_usage']['mean_mb']:.2f} MB")
    logger.info(f"Max Memory Usage: {stats['memory_usage']['max_mb']:.2f} MB")
    logger.info(f"Mean CPU Usage: {stats['cpu_usage']['mean_percent']:.2f}%")
    
    # Check performance requirements
    requirements_met = True
    
    if stats['response_times']['mean'] > 5.0:
        logger.error("❌ REQUIREMENT VIOLATION: Mean response time exceeds 5 seconds")
        requirements_met = False
    
    if stats['response_times']['p95'] > 5.0:
        logger.error("❌ REQUIREMENT VIOLATION: 95th percentile response time exceeds 5 seconds")
        requirements_met = False
    
    if stats['memory_usage']['max_mb'] > 2048:  # 2GB limit
        logger.warning("⚠️  Memory usage exceeded 2GB - consider optimization")
    
    if requirements_met:
        logger.info("✅ All performance requirements met")
    else:
        logger.error("❌ Some performance requirements not met")
    
    # Save detailed results to file
    with open(f"performance_results_{int(time.time())}.json", "w") as f:
        json.dump(stats, f, indent=2)


if __name__ == "__main__":
    # Example usage for standalone testing
    print("AI Backend Performance Testing Suite")
    print("Use with Locust: locust -f test_load_testing.py --host=http://localhost:8000")
    
    # Example WebSocket testing
    ws_tester = WebSocketLoadTester()
    ws_results = ws_tester.test_websocket_connections(max_connections=50)
    print(f"WebSocket test results: {ws_results}")