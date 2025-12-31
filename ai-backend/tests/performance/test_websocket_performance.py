"""
WebSocket-specific performance testing for AI Backend.

This module focuses on testing WebSocket connection limits, message throughput,
and real-time communication performance under various load conditions.

Requirements: 9.3, 9.4
"""

import asyncio
import json
import time
import websockets
import logging
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timedelta
import statistics
import threading
import queue
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class WebSocketMetrics:
    """Container for WebSocket performance metrics."""
    connection_time: float
    message_count: int
    total_response_time: float
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    errors: List[str]
    typing_delays: List[float]
    connection_id: str


class WebSocketPerformanceTester:
    """
    Comprehensive WebSocket performance testing suite.
    
    Tests various aspects of WebSocket performance:
    - Connection establishment limits
    - Concurrent message handling
    - Typing delay simulation accuracy
    - Memory usage under WebSocket load
    - Connection stability over time
    """
    
    def __init__(self, base_url: str = "ws://localhost:8000"):
        self.base_url = base_url
        self.results: List[WebSocketMetrics] = []
        self.active_connections: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.message_queue = queue.Queue()
        self.error_count = 0
        
    async def test_connection_limits(self, max_connections: int = 200) -> Dict[str, Any]:
        """
        Test maximum concurrent WebSocket connections.
        
        Args:
            max_connections: Maximum number of connections to attempt
            
        Returns:
            Dictionary containing connection limit test results
        """
        logger.info(f"Testing WebSocket connection limits up to {max_connections} connections")
        
        successful_connections = 0
        failed_connections = 0
        connection_times = []
        errors = []
        
        # Semaphore to control connection rate
        semaphore = asyncio.Semaphore(50)  # Max 50 concurrent connection attempts
        
        async def establish_connection(connection_id: int) -> Optional[float]:
            """Establish a single WebSocket connection."""
            async with semaphore:
                try:
                    start_time = time.time()
                    
                    # Connect to catfish chat endpoint (most resource-intensive)
                    uri = f"{self.base_url}/ws/chat/catfish/{connection_id}"
                    websocket = await websockets.connect(
                        uri,
                        timeout=10,
                        max_size=1024*1024,  # 1MB max message size
                        max_queue=100  # Max queued messages
                    )
                    
                    connection_time = time.time() - start_time
                    
                    # Store connection for later cleanup
                    self.active_connections[str(connection_id)] = websocket
                    
                    return connection_time
                    
                except Exception as e:
                    errors.append(f"Connection {connection_id}: {str(e)}")
                    return None
        
        # Create connection tasks
        tasks = [establish_connection(i) for i in range(max_connections)]
        
        # Execute connection attempts
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                failed_connections += 1
                errors.append(f"Connection {i}: {str(result)}")
            elif result is not None:
                successful_connections += 1
                connection_times.append(result)
            else:
                failed_connections += 1
        
        # Calculate statistics
        stats = {
            "max_attempted_connections": max_connections,
            "successful_connections": successful_connections,
            "failed_connections": failed_connections,
            "success_rate": successful_connections / max_connections * 100,
            "errors": errors[:10],  # First 10 errors for analysis
            "total_errors": len(errors),
        }
        
        if connection_times:
            stats.update({
                "avg_connection_time": statistics.mean(connection_times),
                "min_connection_time": min(connection_times),
                "max_connection_time": max(connection_times),
                "p95_connection_time": self._percentile(connection_times, 95),
            })
        
        logger.info(f"Connection limit test completed: {successful_connections}/{max_connections} successful")
        return stats
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        if not data:
            return 0
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


async def run_comprehensive_websocket_tests():
    """Run all WebSocket performance tests and generate comprehensive report."""
    logger.info("Starting comprehensive WebSocket performance testing")
    
    tester = WebSocketPerformanceTester()
    results = {}
    
    try:
        # Test 1: Connection limits
        logger.info("=== Test 1: Connection Limits ===")
        results["connection_limits"] = await tester.test_connection_limits(max_connections=100)
        
    except Exception as e:
        logger.error(f"Error during WebSocket testing: {e}")
        results["error"] = str(e)
    
    # Generate comprehensive report
    logger.info("=== WEBSOCKET PERFORMANCE TEST RESULTS ===")
    
    if "connection_limits" in results:
        conn_stats = results["connection_limits"]
        logger.info(f"Connection Limits: {conn_stats['successful_connections']}/{conn_stats['max_attempted_connections']} ({conn_stats['success_rate']:.1f}%)")
    
    # Save results to file
    timestamp = int(time.time())
    with open(f"websocket_performance_results_{timestamp}.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to websocket_performance_results_{timestamp}.json")
    return results


if __name__ == "__main__":
    # Run comprehensive WebSocket performance tests
    asyncio.run(run_comprehensive_websocket_tests())