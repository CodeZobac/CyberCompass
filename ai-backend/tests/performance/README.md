# AI Backend Performance Testing Suite

This directory contains comprehensive performance testing tools for the AI Backend service, designed to validate system performance under various load conditions and ensure compliance with performance requirements.

## Overview

The performance testing suite covers:

- **Concurrent User Simulation**: Tests system behavior with multiple simultaneous users
- **WebSocket Performance**: Validates real-time communication limits and stability
- **Memory Usage Monitoring**: Tracks resource usage and detects memory leaks
- **Load Testing**: Measures throughput and response times under sustained load

## Requirements Validation

The tests validate the following performance requirements:

- **Requirement 9.3**: Response times remain under 5 seconds for text-based interactions
- **Requirement 9.4**: System handles multiple concurrent users without performance degradation
- **Memory Efficiency**: Memory usage remains within acceptable limits
- **WebSocket Stability**: Real-time connections maintain stability under load

## Test Modules

### 1. `test_load_testing.py`
Locust-based load testing with realistic user behavior simulation.

**Features:**
- HTTP endpoint load testing
- Response time monitoring
- Error rate tracking
- System resource monitoring
- Performance metrics collection

### 2. `test_websocket_performance.py`
WebSocket-specific performance testing for real-time features.

**Features:**
- Connection limit testing
- Message throughput measurement
- Typing delay validation
- Connection stability testing
- Memory usage under WebSocket load

### 3. `test_memory_monitoring.py`
Comprehensive memory usage and leak detection.

**Features:**
- Real-time memory monitoring
- Memory leak detection
- Resource usage tracking
- Garbage collection analysis
- Performance profiling

### 4. `test_concurrent_users.py`
Realistic concurrent user simulation with mixed behavior patterns.

**Features:**
- Multiple user behavior patterns (light, mixed, heavy)
- Realistic interaction timing
- WebSocket chat simulation
- API endpoint testing
- Performance metrics aggregation

### 5. `test_performance_suite.py`
Comprehensive test suite that orchestrates all performance tests.

**Features:**
- Complete performance validation
- Requirement compliance checking
- Performance recommendations
- Detailed reporting
- Results aggregation

## Quick Start

### Prerequisites

Install performance testing dependencies:

```bash
cd ai-backend
pip install -e ".[test]"
```

Ensure the AI Backend server is running:

```bash
# In one terminal
cd ai-backend
python -m uvicorn src.main:app --reload --port 8000
```

### Running Tests

#### 1. Run All Performance Tests

```bash
cd ai-backend/tests/performance
python run_performance_tests.py --all
```

#### 2. Run Specific Test Categories

```bash
# Load testing with 50 users for 5 minutes
python run_performance_tests.py --load-test --users 50 --duration 5

# WebSocket testing with 100 connections
python run_performance_tests.py --websocket-test --connections 100

# Memory performance testing
python run_performance_tests.py --memory-test

# Concurrent users testing
python run_performance_tests.py --concurrent-users --users 25 --duration 3
```

#### 3. Using Pytest

```bash
# Run all performance tests
pytest tests/performance/ -m performance -v

# Run specific test categories
pytest tests/performance/ -m load_test -v
pytest tests/performance/ -m websocket_test -v
pytest tests/performance/ -m memory_test -v
```

#### 4. Using Locust (Advanced Load Testing)

```bash
# Start Locust web interface
locust -f tests/performance/test_load_testing.py --host=http://localhost:8000

# Run headless load test
locust -f tests/performance/test_load_testing.py --host=http://localhost:8000 \
       --users 50 --spawn-rate 5 --run-time 5m --headless
```

## Test Configuration

### Environment Variables

```bash
# Test server configuration
export AI_BACKEND_URL="http://localhost:8000"
export WEBSOCKET_URL="ws://localhost:8000"

# Performance test parameters
export MAX_CONCURRENT_USERS=100
export TEST_DURATION_MINUTES=5
export MAX_WEBSOCKET_CONNECTIONS=200

# Monitoring configuration
export MONITORING_INTERVAL=1.0
export MEMORY_LEAK_THRESHOLD_MB=50.0
```

### Test Parameters

Common parameters for performance tests:

- `--users`: Number of concurrent users (default: 25)
- `--duration`: Test duration in minutes (default: 3)
- `--connections`: Maximum WebSocket connections (default: 100)
- `--url`: Base URL for testing (default: http://localhost:8000)
- `--verbose`: Enable detailed logging

## Performance Thresholds

The tests validate against these performance thresholds:

| Metric | Threshold | Requirement |
|--------|-----------|-------------|
| Response Time | < 5 seconds | 9.3 |
| Error Rate | < 5% | 9.4 |
| Memory Increase | < 500 MB | 9.4 |
| WebSocket Success Rate | > 90% | 9.3 |
| Concurrent Users | 50+ users | 9.4 |

## Results and Reporting

### Output Files

Performance tests generate detailed results in JSON format:

- `performance_suite_results_<timestamp>.json`: Complete test suite results
- `load_test_results_<timestamp>.json`: Load testing results
- `websocket_performance_results_<timestamp>.json`: WebSocket test results
- `memory_monitoring_<timestamp>.json`: Memory usage analysis
- `concurrent_user_test_results_<timestamp>.json`: Concurrent user results

### Report Structure

```json
{
  "suite_info": {
    "start_time": 1234567890,
    "duration_seconds": 300,
    "test_categories": ["concurrent_users", "websocket_performance", "memory_performance"]
  },
  "test_results": {
    "concurrent_users": [...],
    "websocket_performance": {...},
    "memory_performance": {...}
  },
  "performance_summary": {
    "overall_metrics": {...},
    "performance_highlights": [...],
    "performance_concerns": [...]
  },
  "requirement_validation": {
    "response_time_under_5s": {"status": "pass", "details": [...]},
    "concurrent_user_handling": {"status": "pass", "details": [...]},
    "memory_efficiency": {"status": "pass", "details": [...]},
    "websocket_stability": {"status": "pass", "details": [...]}
  },
  "recommendations": [...]
}
```

## Interpreting Results

### Performance Metrics

**Response Time Metrics:**
- `avg_response_time`: Average response time across all requests
- `p95_response_time`: 95th percentile response time
- `p99_response_time`: 99th percentile response time
- `max_response_time`: Maximum response time observed

**Throughput Metrics:**
- `requests_per_second`: Average requests processed per second
- `successful_requests`: Number of successful requests
- `error_rate`: Percentage of failed requests

**Resource Metrics:**
- `memory_usage_mb`: Peak memory usage in megabytes
- `cpu_usage_percent`: Average CPU utilization
- `websocket_connections`: Peak concurrent WebSocket connections

### Performance Analysis

**✅ Good Performance Indicators:**
- Response times consistently under 3 seconds
- Error rates below 2%
- Memory usage increases linearly with load
- WebSocket connection success rates above 95%

**⚠️ Performance Concerns:**
- Response times approaching 5-second limit
- Error rates above 5%
- Memory usage growing exponentially
- WebSocket connection failures above 10%

**❌ Performance Issues:**
- Response times exceeding 5 seconds
- Error rates above 10%
- Memory leaks detected
- WebSocket connection success rates below 80%

## Troubleshooting

### Common Issues

**1. Connection Refused Errors**
```
Solution: Ensure AI Backend server is running on the specified port
Check: curl http://localhost:8000/health
```

**2. WebSocket Connection Failures**
```
Solution: Verify WebSocket endpoints are properly configured
Check: WebSocket URL format and authentication
```

**3. High Memory Usage**
```
Solution: Check for memory leaks in AI agent implementations
Monitor: CrewAI memory usage and cleanup processes
```

**4. Slow Response Times**
```
Solution: Optimize AI model inference and database queries
Profile: Identify bottlenecks in request processing
```

### Performance Optimization Tips

**1. AI Model Optimization**
- Use model caching for frequently accessed models
- Implement async processing for heavy AI operations
- Consider model quantization for faster inference

**2. Database Optimization**
- Add appropriate indexes for frequent queries
- Use connection pooling
- Implement query result caching

**3. WebSocket Optimization**
- Implement connection pooling
- Add proper cleanup mechanisms
- Use message queuing for high-throughput scenarios

**4. Memory Management**
- Implement proper garbage collection tuning
- Use memory pooling for large objects
- Monitor CrewAI agent memory usage

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Performance Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  performance-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd ai-backend
        pip install -e ".[test]"
    
    - name: Start AI Backend
      run: |
        cd ai-backend
        python -m uvicorn src.main:app --port 8000 &
        sleep 10
    
    - name: Run Performance Tests
      run: |
        cd ai-backend/tests/performance
        python run_performance_tests.py --concurrent-users --users 10 --duration 1
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: ai-backend/tests/performance/performance_results/
```

## Contributing

When adding new performance tests:

1. Follow the existing test structure and naming conventions
2. Include comprehensive docstrings and type hints
3. Add appropriate pytest markers (`@pytest.mark.performance`)
4. Validate against performance requirements
5. Update this README with new test descriptions

## Support

For questions or issues with performance testing:

1. Check the troubleshooting section above
2. Review test logs for detailed error information
3. Ensure all dependencies are properly installed
4. Verify the AI Backend server is running and accessible

## Performance Test Checklist

Before running performance tests:

- [ ] AI Backend server is running and accessible
- [ ] All test dependencies are installed
- [ ] Database is properly configured and accessible
- [ ] Sufficient system resources available (CPU, memory)
- [ ] Network connectivity is stable
- [ ] Test parameters are appropriate for the environment

After running performance tests:

- [ ] Review all test results for failures
- [ ] Check performance metrics against requirements
- [ ] Analyze any performance concerns or recommendations
- [ ] Save results for historical comparison
- [ ] Update performance baselines if needed