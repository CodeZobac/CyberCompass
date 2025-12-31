# Unit Tests

Comprehensive unit tests for the AI Backend components, covering CrewAI agents, FastAPI endpoints, and WebSocket connections.

## Overview

This test suite implements **Task 11.1** requirements:
- ✅ Tests for individual CrewAI agents and their responses
- ✅ Tests for FastAPI endpoints with various input scenarios  
- ✅ Tests for WebSocket connection handling and message routing

## Test Files

### `test_agents.py`
Tests for all CrewAI agents:
- EthicsMentorAgent
- DeepfakeAnalystAgent
- SocialMediaSimulatorAgent
- CatfishCharacterAgent
- AnalyticsAgent
- AgentFactory

**Coverage**: 14 test methods across 7 test classes

### `test_api_endpoints.py`
Tests for FastAPI endpoints:
- Root and health check endpoints
- Authentication endpoints
- Conversation endpoints
- Analytics endpoints
- Cultural content endpoints
- Error handling and validation
- Security features (rate limiting, CORS)

**Coverage**: 29 test methods across 9 test classes

### `test_websocket.py`
Tests for WebSocket functionality:
- Connection lifecycle
- Message routing
- Error handling
- Message types
- Security features

**Coverage**: 7 test methods across 4 test classes

## Running Tests

### Prerequisites

Ensure you have `uv` installed and dependencies synced:

```bash
# Sync dependencies with test extras
uv sync --extra test --extra dev
```

### Run All Tests

```bash
# Using the test runner script
uv run python test_runner.py

# Or directly with pytest
uv run pytest tests/unit/ -v
```

### Run Specific Test Files

```bash
# Agent tests only
uv run python test_runner.py --agents

# API endpoint tests only
uv run python test_runner.py --api

# WebSocket tests only
uv run python test_runner.py --websocket
```

### Run with Coverage

```bash
# Generate coverage report
uv run python test_runner.py --coverage

# View HTML coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Run Specific Test Classes

```bash
# Run a specific test class
uv run pytest tests/unit/test_agents.py::TestEthicsMentorAgent -v

# Run a specific test method
uv run pytest tests/unit/test_agents.py::TestEthicsMentorAgent::test_agent_initialization -v
```

## Test Validation

Validate test structure and count:

```bash
uv run python validate_tests.py
```

This will show:
- Number of test classes per file
- Number of test methods per file
- Total test coverage
- Validation checks

## Test Structure

All tests follow pytest conventions:
- Test files start with `test_`
- Test classes start with `Test`
- Test methods start with `test_`
- Fixtures are used for common setup
- Mocking is used to avoid external dependencies

## Mocking Strategy

Tests use `unittest.mock` to:
- Mock agent responses
- Mock database calls
- Mock external API calls
- Mock WebSocket connections

This ensures tests:
- Run quickly
- Don't require external services
- Are deterministic and reliable

## Requirements Coverage

### Requirement 9.1: Comprehensive Test Coverage
✅ All major components have unit tests
✅ Tests cover normal and edge cases
✅ Tests validate error handling

### Requirement 9.2: Various Input Scenarios
✅ Valid input scenarios
✅ Invalid input scenarios
✅ Edge cases and boundary conditions
✅ Multilingual support (English and Portuguese)

## Test Statistics

- **Total Test Files**: 3
- **Total Test Classes**: 20
- **Total Test Methods**: 50+
- **Coverage Areas**: Agents, API, WebSockets, Error Handling, Security

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example CI configuration
- name: Run Unit Tests
  run: |
    uv sync --extra test
    uv run pytest tests/unit/ -v --cov=src
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure dependencies are synced:

```bash
uv sync --extra test --extra dev
```

### Test Discovery Issues

Ensure you're running tests from the project root:

```bash
cd ai-backend
uv run pytest tests/unit/ -v
```

### Slow Tests

For faster test execution, run without coverage:

```bash
uv run pytest tests/unit/ -v --tb=short
```

## Contributing

When adding new tests:
1. Follow existing test patterns
2. Use descriptive test names
3. Add docstrings to test methods
4. Mock external dependencies
5. Ensure tests are independent
6. Run validation script to verify structure

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [uv Documentation](https://docs.astral.sh/uv/)
