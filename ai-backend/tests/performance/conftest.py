"""
Pytest configuration and fixtures for performance testing.

This module provides shared fixtures and configuration for all performance tests,
including test server setup, monitoring utilities, and common test data.
"""

import pytest
import asyncio
import logging
from typing import Dict, Any, AsyncGenerator
import aiohttp
import time
from test_memory_monitoring import SystemResourceMonitor

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_server_url():
    """
    Provide the test server URL.
    
    In a real implementation, this would start the AI backend server
    for testing. For now, it assumes the server is running locally.
    """
    base_url = "http://localhost:8000"
    
    # TODO: In a complete implementation, add server startup/shutdown logic here
    # For now, assume server is running
    
    yield base_url


@pytest.fixture
async def performance_monitor():
    """Provide a performance monitor for test cases."""
    monitor = SystemResourceMonitor(monitoring_interval=0.5, enable_memory_profiling=True)
    
    try:
        monitor.start_monitoring()
        yield monitor
    finally:
        stats = monitor.stop_monitoring()
        logger.info(f"Test completed - Memory: {stats.get('memory_statistics', {}).get('peak_mb', 0):.1f} MB peak")


@pytest.fixture
async def http_client():
    """Provide an HTTP client for API testing."""
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
def test_user_data():
    """Provide test user data for performance tests."""
    return {
        "user_id": "perf_test_user",
        "session_id": "perf_test_session",
        "auth_token": "mock_token_perf_test_user",
        "locale": "en"
    }


@pytest.fixture
def performance_thresholds():
    """Define performance thresholds for validation."""
    return {
        "max_response_time_seconds": 5.0,
        "max_memory_increase_mb": 500.0,
        "max_error_rate_percent": 5.0,
        "min_requests_per_second": 10.0,
        "max_cpu_usage_percent": 80.0,
    }


@pytest.fixture
async def websocket_connection(test_server_url):
    """Provide a WebSocket connection for testing."""
    import websockets
    
    ws_url = test_server_url.replace("http://", "ws://")
    uri = f"{ws_url}/ws/chat/test/perf_test_session"
    
    try:
        async with websockets.connect(uri, timeout=10) as websocket:
            yield websocket
    except Exception as e:
        logger.error(f"Failed to establish WebSocket connection: {e}")
        yield None


@pytest.fixture
def sample_feedback_request():
    """Provide sample feedback request data."""
    return {
        "user_id": "perf_test_user",
        "challenge_id": "perf_test_challenge",
        "selected_option": "A",
        "correct_option": "B",
        "locale": "en",
        "context": {
            "difficulty": "medium",
            "topic": "privacy"
        }
    }


@pytest.fixture
def sample_deepfake_challenge_request():
    """Provide sample deepfake challenge request data."""
    return {
        "user_id": "perf_test_user",
        "difficulty_level": 2,
        "media_type": "image"
    }


@pytest.fixture
def sample_social_media_request():
    """Provide sample social media simulation request data."""
    return {
        "user_id": "perf_test_user",
        "simulation_type": "mixed",
        "num_posts": 10,
        "locale": "en"
    }


@pytest.mark.asyncio
async def validate_performance_requirements(
    test_results: Dict[str, Any],
    thresholds: Dict[str, float]
) -> Dict[str, bool]:
    """
    Validate test results against performance requirements.
    
    Args:
        test_results: Dictionary containing test metrics
        thresholds: Performance thresholds to validate against
        
    Returns:
        Dictionary indicating which requirements were met
    """
    validation_results = {}
    
    # Response time validation
    if "avg_response_time" in test_results:
        validation_results["response_time_ok"] = (
            test_results["avg_response_time"] <= thresholds["max_response_time_seconds"]
        )
    
    # Memory usage validation
    if "memory_usage_mb" in test_results:
        validation_results["memory_usage_ok"] = (
            test_results["memory_usage_mb"] <= thresholds["max_memory_increase_mb"]
        )
    
    # Error rate validation
    if "error_rate" in test_results:
        validation_results["error_rate_ok"] = (
            test_results["error_rate"] <= thresholds["max_error_rate_percent"]
        )
    
    # Throughput validation
    if "requests_per_second" in test_results:
        validation_results["throughput_ok"] = (
            test_results["requests_per_second"] >= thresholds["min_requests_per_second"]
        )
    
    # CPU usage validation
    if "cpu_usage_percent" in test_results:
        validation_results["cpu_usage_ok"] = (
            test_results["cpu_usage_percent"] <= thresholds["max_cpu_usage_percent"]
        )
    
    return validation_results


# Performance test markers
pytest.mark.performance = pytest.mark.mark("performance")
pytest.mark.load_test = pytest.mark.mark("load_test")
pytest.mark.stress_test = pytest.mark.mark("stress_test")
pytest.mark.websocket_test = pytest.mark.mark("websocket_test")
pytest.mark.memory_test = pytest.mark.mark("memory_test")


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "load_test: mark test as a load test"
    )
    config.addinivalue_line(
        "markers", "stress_test: mark test as a stress test"
    )
    config.addinivalue_line(
        "markers", "websocket_test: mark test as a WebSocket test"
    )
    config.addinivalue_line(
        "markers", "memory_test: mark test as a memory test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add performance marker to all tests in performance directory
        if "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        
        # Add specific markers based on test names
        if "load" in item.name.lower():
            item.add_marker(pytest.mark.load_test)
        
        if "stress" in item.name.lower():
            item.add_marker(pytest.mark.stress_test)
        
        if "websocket" in item.name.lower():
            item.add_marker(pytest.mark.websocket_test)
        
        if "memory" in item.name.lower():
            item.add_marker(pytest.mark.memory_test)


@pytest.fixture(autouse=True)
async def performance_test_setup_teardown():
    """Automatic setup and teardown for performance tests."""
    # Setup
    start_time = time.time()
    logger.info("Starting performance test")
    
    yield
    
    # Teardown
    duration = time.time() - start_time
    logger.info(f"Performance test completed in {duration:.2f} seconds")