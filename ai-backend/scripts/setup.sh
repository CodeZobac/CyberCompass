#!/bin/bash
# Setup script for AI Backend development environment using uv

set -e

echo "🚀 Setting up Cyber Compass AI Backend..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    echo "✅ uv installed successfully!"
else
    echo "✅ uv is already installed"
fi

# Install dependencies with uv
echo "📥 Installing dependencies with uv..."
uv sync

echo "✅ Dependencies installed!"

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration (especially OPENAI_API_KEY)"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p logs
mkdir -p migrations/versions

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. Update .env with your configuration"
echo "  3. Start development server: make dev or uv run uvicorn src.main:app --reload"
echo "  4. Visit http://localhost:8000/docs for API documentation"
echo ""
