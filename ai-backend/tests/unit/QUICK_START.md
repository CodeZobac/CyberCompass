# Quick Start Guide - Unit Tests

## 🚀 Run Tests Immediately

```bash
# Navigate to ai-backend directory
cd ai-backend

# Ensure dependencies are synced
uv sync --extra test --extra dev

# Run all unit tests
uv run pytest tests/unit/ -v
```

## 📊 Validate Test Structure

```bash
cd ai-backend/tests/unit
uv run python validate_tests.py
```

Expected output:
```
✅ Has 50 test methods (target: 50+)
✅ Has 20 test classes (target: 15+)
✅ Has 3 test files (target: 3)
🎉 All validation checks passed!
```

## 🎯 Run Specific Tests

### By Test File
```bash
# Agent tests
uv run python tests/unit/test_runner.py --agents

# API endpoint tests
uv run python tests/unit/test_runner.py --api

# WebSocket tests
uv run python tests/unit/test_runner.py --websocket
```

### By Test Class
```bash
# Test a specific agent
uv run pytest tests/unit/test_agents.py::TestEthicsMentorAgent -v

# Test authentication endpoints
uv run pytest tests/unit/test_api_endpoints.py::TestAuthenticationEndpoints -v

# Test WebSocket connections
uv run pytest tests/unit/test_websocket.py::TestWebSocketConnection -v
```

### By Test Method
```bash
# Test agent initialization
uv run pytest tests/unit/test_agents.py::TestEthicsMentorAgent::test_agent_initialization -v

# Test root endpoint
uv run pytest tests/unit/test_api_endpoints.py::TestRootEndpoints::test_root_endpoint -v

# Test WebSocket connection
uv run pytest tests/unit/test_websocket.py::TestWebSocketConnection::test_websocket_connect_success -v
```

## 📈 Generate Coverage Report

```bash
# Run tests with coverage
uv run python tests/unit/test_runner.py --coverage

# View HTML report (opens in browser)
# Linux/macOS:
open htmlcov/index.html

# Windows:
start htmlcov/index.html
```

## 🔍 Common Commands

```bash
# Run all tests with short output
uv run pytest tests/unit/ -v --tb=short

# Run tests and stop on first failure
uv run pytest tests/unit/ -v -x

# Run tests matching a pattern
uv run pytest tests/unit/ -v -k "agent"

# Run tests with detailed output
uv run pytest tests/unit/ -vv

# Run tests quietly (only show failures)
uv run pytest tests/unit/ -q
```

## 📝 Test Files Overview

| File | Tests | Focus |
|------|-------|-------|
| `test_agents.py` | 14 | CrewAI agents, multilingual support |
| `test_api_endpoints.py` | 29 | FastAPI endpoints, validation, security |
| `test_websocket.py` | 7 | WebSocket connections, message routing |

## ✅ Requirements Covered

- ✅ Tests for individual CrewAI agents and their responses
- ✅ Tests for FastAPI endpoints with various input scenarios
- ✅ Tests for WebSocket connection handling and message routing

## 🛠️ Troubleshooting

### Missing Dependencies
```bash
uv sync --extra test --extra dev
```

### Import Errors
```bash
# Ensure you're in the ai-backend directory
cd ai-backend
uv run pytest tests/unit/ -v
```

### Test Discovery Issues
```bash
# Run from project root
cd ai-backend
uv run pytest tests/unit/ -v
```

## 📚 More Information

- Full documentation: `README.md`
- Test summary: `TEST_SUMMARY.md`
- Implementation details: `IMPLEMENTATION_SUMMARY.md`

## 🎉 Success Criteria

Your tests are working correctly if:
1. ✅ Validation script shows 50+ test methods
2. ✅ All tests can be discovered by pytest
3. ✅ No import errors when running tests
4. ✅ Test runner executes without errors

---

**Note**: These tests use mocking, so they don't require actual AI models or external services to run.
