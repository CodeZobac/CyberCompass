# Cyber Compass AI Backend

CrewAI-powered backend service for cyber ethics education platform.

## Features

- **Multi-Agent AI System**: Specialized CrewAI agents for ethics mentoring, deepfake detection, social media simulation, and catfishing detection
- **Real-time Communication**: WebSocket support for live chat simulations with realistic typing delays
- **Advanced Analytics**: Progress tracking and personalized learning recommendations
- **Multilingual Support**: Full Portuguese and English support with cultural adaptation
- **Modern Architecture**: FastAPI with async/await patterns for high-performance operations

## Requirements

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) - Modern Python package manager
- PostgreSQL 14+
- Redis 7+

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Install Dependencies with uv

```bash
# uv will automatically create a virtual environment and install dependencies
uv sync

# Or manually create venv and install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### 3. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

### 4. Run Database Migrations

```bash
alembic upgrade head
```

## Development

### Run Development Server

```bash
# Using uv
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or activate venv first
source .venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Format code
uv run black src tests

# Lint code
uv run ruff check src tests

# Type checking
uv run mypy src
```

## Project Structure

```
ai-backend/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── api/                    # API endpoints
│   │   ├── routes/             # Route handlers
│   │   └── middleware/         # Custom middleware
│   ├── agents/                 # CrewAI agent implementations
│   │   ├── ethics_mentor.py
│   │   ├── deepfake_analyst.py
│   │   ├── social_media_simulator.py
│   │   └── catfish_character.py
│   ├── flows/                  # CrewAI Flow implementations
│   │   ├── deepfake_detection.py
│   │   ├── social_media_simulation.py
│   │   └── catfish_detection.py
│   ├── services/               # Business logic
│   │   ├── crew_manager.py
│   │   ├── conversation_engine.py
│   │   └── analytics_engine.py
│   ├── models/                 # Data models
│   │   ├── database.py
│   │   └── schemas.py
│   ├── tools/                  # Custom CrewAI tools
│   │   ├── deepfake_analysis.py
│   │   ├── typing_delay.py
│   │   └── character_consistency.py
│   └── utils/                  # Utility functions
├── tests/                      # Test suite
│   ├── unit/
│   ├── integration/
│   └── performance/
├── config/                     # Configuration files
│   └── agents.yaml             # Agent configurations
├── migrations/                 # Database migrations
├── pyproject.toml              # Project configuration
├── .env.example                # Environment variables template
└── README.md
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
