# Quick Start Guide

Get the AI Backend up and running in minutes.

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) - Modern Python package manager (replaces pip and venv)
- PostgreSQL 14+ (optional for development, can use SQLite)
- Redis 7+ (optional for development)

## Installation

### Option 1: Automated Setup (Recommended)

#### Linux/macOS:
```bash
cd ai-backend
chmod +x scripts/setup.sh
./scripts/setup.sh
```

#### Windows (PowerShell):
```powershell
cd ai-backend
.\scripts\setup.ps1
```

### Option 2: Manual Setup

1. **Install uv (if not already installed)**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or with pip
   pip install uv
   ```

2. **Install Dependencies with uv**
   ```bash
   # uv automatically creates .venv and installs dependencies
   uv sync
   
   # Activate the virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Create Directories**
   ```bash
   mkdir -p uploads logs migrations/versions
   ```

## Configuration

Edit `.env` file with your settings:

```env
# Required
OPENAI_API_KEY="your-api-key-here"

# Optional (defaults work for development)
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/cyber_compass_ai"
REDIS_URL="redis://localhost:6379/0"
```

## Running the Server

### Development Mode (with auto-reload)
```bash
# Using Make
make dev

# Using uv directly
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or activate venv first
source .venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
```bash
# Build and start all services
make docker-up

# Or manually
docker-compose up -d
```

## Verify Installation

1. **Check Health Endpoint**
   ```bash
   curl http://localhost:8000/health
   ```

2. **View API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Run Tests**
   ```bash
   uv run pytest
   ```

## Next Steps

1. **Implement CrewAI Agents** (Task 2)
   - Configure agents in `config/agents.yaml`
   - Implement agent classes in `src/agents/`

2. **Set Up API Endpoints** (Task 2)
   - Create route handlers in `src/api/routes/`
   - Add middleware in `src/api/middleware/`

3. **Develop Flows** (Task 4)
   - Implement CrewAI Flows in `src/flows/`

## Troubleshooting

### Import Errors
```bash
# Reinstall in editable mode with uv
uv pip install -e .

# Or resync dependencies
uv sync
```

### Port Already in Use
```bash
# Change port in .env or use different port
uvicorn src.main:app --reload --port 8001
```

### Database Connection Issues
```bash
# For development, you can use SQLite instead
# Update DATABASE_URL in .env:
DATABASE_URL="sqlite+aiosqlite:///./cyber_compass.db"
```

## Development Commands

```bash
# Run tests
make test
# or: uv run pytest

# Format code
make format
# or: uv run black src tests

# Lint code
make lint
# or: uv run ruff check src tests

# Clean temporary files
make clean
```

## Support

For issues or questions:
- Check the main README.md
- Review the design document in `.kiro/specs/ai-backend-separation/design.md`
- Check requirements in `.kiro/specs/ai-backend-separation/requirements.md`
