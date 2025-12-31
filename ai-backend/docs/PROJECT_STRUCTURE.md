# AI Backend Project Structure

Complete overview of the Cyber Compass AI Backend project organization.

## Directory Structure

```
ai-backend/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration management
│   │
│   ├── agents/                  # CrewAI agent implementations
│   │   ├── __init__.py
│   │   ├── ethics_mentor.py     # [Task 3] Ethics education agent
│   │   ├── deepfake_analyst.py  # [Task 3] Deepfake detection agent
│   │   ├── social_media_simulator.py  # [Task 3] Social media agent
│   │   ├── catfish_character.py # [Task 3] Catfishing simulation agent
│   │   └── analytics_agent.py   # [Task 3] Progress analytics agent
│   │
│   ├── api/                     # API layer
│   │   ├── __init__.py
│   │   ├── routes/              # Route handlers
│   │   │   ├── __init__.py
│   │   │   ├── feedback.py      # [Task 2] Feedback endpoints
│   │   │   ├── challenges.py    # [Task 2] Challenge endpoints
│   │   │   ├── conversations.py # [Task 5] Chat endpoints
│   │   │   └── analytics.py     # [Task 6] Analytics endpoints
│   │   │
│   │   └── middleware/          # Custom middleware
│   │       ├── __init__.py
│   │       ├── auth.py          # [Task 2] JWT authentication
│   │       ├── rate_limit.py    # [Task 2] Rate limiting
│   │       └── error_handler.py # [Task 10] Error handling
│   │
│   ├── flows/                   # CrewAI Flow implementations
│   │   ├── __init__.py
│   │   ├── deepfake_detection.py    # [Task 4] Deepfake flow
│   │   ├── social_media_simulation.py # [Task 4] Social media flow
│   │   └── catfish_detection.py     # [Task 4] Catfish flow
│   │
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── crew_manager.py      # [Task 3] CrewAI orchestration
│   │   ├── conversation_engine.py # [Task 5] Chat management
│   │   └── analytics_engine.py  # [Task 6] Analytics processing
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   ├── database.py          # [Task 9] Database models
│   │   └── schemas.py           # [Task 2] Pydantic schemas
│   │
│   ├── tools/                   # Custom CrewAI tools
│   │   ├── __init__.py
│   │   ├── deepfake_analysis.py # [Task 7] Deepfake analysis tool
│   │   ├── typing_delay.py      # [Task 5] Typing simulation tool
│   │   ├── content_generator.py # [Task 7] Content generation tool
│   │   └── character_consistency.py # [Task 7] Character tool
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── logging.py           # [Task 12] Logging utilities
│       └── validators.py        # [Task 2] Validation helpers
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   ├── test_agents.py       # [Task 11] Agent tests
│   │   ├── test_flows.py        # [Task 11] Flow tests
│   │   └── test_api.py          # [Task 11] API tests
│   │
│   ├── integration/             # Integration tests
│   │   ├── __init__.py
│   │   └── test_workflows.py    # [Task 11] Workflow tests
│   │
│   └── performance/             # Performance tests
│       ├── __init__.py
│       └── test_load.py         # [Task 11] Load tests
│
├── config/                      # Configuration files
│   └── agents.yaml              # Agent configurations
│
├── scripts/                     # Utility scripts
│   ├── setup.sh                 # Linux/macOS setup
│   ├── setup.ps1                # Windows setup
│   └── verify_setup.py          # Structure verification
│
├── migrations/                  # Database migrations
│   └── versions/                # [Task 9] Migration files
│
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── .python-version              # Python version specification
├── docker-compose.yml           # Docker Compose configuration
├── Dockerfile                   # Docker image definition
├── Makefile                     # Build automation
├── pyproject.toml               # Project configuration
├── requirements.txt             # Python dependencies
├── setup.py                     # Setup script
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
└── PROJECT_STRUCTURE.md         # This file
```

## Key Files

### Configuration Files

- **pyproject.toml**: Modern Python project configuration with dependencies, build settings, and tool configurations
- **.env.example**: Template for environment variables (copy to .env and configure)
- **config/agents.yaml**: CrewAI agent definitions and configurations

### Application Entry Points

- **src/main.py**: FastAPI application with lifespan management, CORS, and health endpoints
- **src/config.py**: Pydantic-based configuration management with environment variable loading

### Docker Files

- **Dockerfile**: Multi-stage build for production deployment
- **docker-compose.yml**: Complete stack with PostgreSQL and Redis

### Development Tools

- **Makefile**: Common development commands (install, dev, test, lint, format)
- **scripts/setup.sh**: Automated setup for Linux/macOS
- **scripts/setup.ps1**: Automated setup for Windows
- **scripts/verify_setup.py**: Project structure verification

## Implementation Status

### ✅ Task 1: Completed
- [x] Python project directory structure
- [x] Configuration files (pyproject.toml, .env.example)
- [x] FastAPI application skeleton
- [x] Docker configuration
- [x] Development tooling (Makefile, scripts)
- [x] Documentation (README, QUICKSTART)

### 🔜 Next Tasks
- [ ] Task 2: Implement FastAPI server with modern architecture
- [ ] Task 3: Create CrewAI agent configurations and base classes
- [ ] Task 4: Implement CrewAI Flows for complex scenarios
- [ ] Task 5: Create conversation engine with WebSocket support
- [ ] Task 6: Develop analytics and progress tracking
- [ ] Task 7: Create custom CrewAI tools
- [ ] Task 8: Implement multilingual support
- [ ] Task 9: Set up database integration
- [ ] Task 10: Implement error handling
- [ ] Task 11: Create comprehensive testing suite
- [ ] Task 12: Set up deployment and monitoring
- [ ] Task 13: Update Next.js frontend integration

## Technology Stack

### Package Management
- **uv**: Modern, fast Python package manager (replaces pip and venv)

### Core Framework
- **FastAPI 0.115+**: Modern async web framework
- **CrewAI 0.70+**: Multi-agent AI orchestration
- **Pydantic 2.9+**: Data validation and settings management

### AI & ML
- **OpenAI API**: Language model integration
- **LangChain 0.3+**: LLM application framework
- **CrewAI Tools 0.12+**: Specialized agent tools

### Database & Cache
- **PostgreSQL 14+**: Primary database (via asyncpg)
- **Redis 7+**: Caching and session management
- **SQLAlchemy 2.0+**: ORM with async support
- **Alembic 1.13+**: Database migrations

### Development Tools
- **pytest 8.3+**: Testing framework
- **black 24.8+**: Code formatting
- **ruff 0.6+**: Fast Python linter
- **mypy 1.11+**: Static type checking

### Deployment
- **Docker**: Containerization
- **Uvicorn 0.30+**: ASGI server
- **Docker Compose**: Multi-container orchestration

## Development Workflow

1. **Setup**: Run `./scripts/setup.sh` (or `setup.ps1` on Windows) - installs uv and dependencies
2. **Configure**: Edit `.env` with your API keys and settings
3. **Develop**: Run `make dev` or `uv run uvicorn src.main:app --reload`
4. **Test**: Run `make test` or `uv run pytest`
5. **Format**: Run `make format` or `uv run black src tests`
6. **Lint**: Run `make lint` or `uv run ruff check src tests`

## API Documentation

Once running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Requirements Mapping

This structure addresses the following requirements from the specification:

- **Req 1.1**: Separate Python service architecture ✅
- **Req 8.1**: RESTful API endpoints (structure ready)
- **Req 8.2**: Authentication middleware (structure ready)
- **Req 9.1**: Database integration (structure ready)
- **Req 10.1-10.5**: Multilingual support (structure ready)

## Next Steps

1. **Task 2**: Implement FastAPI endpoints and middleware
2. **Task 3**: Configure and implement CrewAI agents
3. **Task 4**: Build CrewAI Flows for educational scenarios
4. **Task 5**: Create WebSocket-based conversation engine
5. Continue through remaining tasks in sequence

## Notes

- All `__init__.py` files are in place for proper Python package structure
- Directory structure follows modern Python best practices
- Configuration uses Pydantic Settings for type-safe environment management
- Docker setup includes PostgreSQL and Redis for complete development environment
- Testing structure supports unit, integration, and performance tests
- Scripts support both Linux/macOS and Windows development environments
