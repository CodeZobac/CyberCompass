# Setup script for AI Backend development environment using uv (Windows)

Write-Host "🚀 Setting up Cyber Compass AI Backend..." -ForegroundColor Green

# Check Python version
$pythonVersion = python --version 2>&1 | Select-String -Pattern '\d+\.\d+' | ForEach-Object { $_.Matches.Value }
$requiredVersion = [version]"3.11"
$currentVersion = [version]$pythonVersion

if ($currentVersion -lt $requiredVersion) {
    Write-Host "❌ Python 3.11 or higher is required. Found: $pythonVersion" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python version: $pythonVersion" -ForegroundColor Green

# Check if uv is installed
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvInstalled) {
    Write-Host "📦 Installing uv package manager..." -ForegroundColor Cyan
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Host "✅ uv installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✅ uv is already installed" -ForegroundColor Green
}

# Install dependencies with uv
Write-Host "📥 Installing dependencies with uv..." -ForegroundColor Cyan
uv sync

Write-Host "✅ Dependencies installed!" -ForegroundColor Green

# Copy environment file
if (-not (Test-Path .env)) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "⚠️  Please update .env with your configuration (especially OPENAI_API_KEY)" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host "📁 Creating directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path uploads | Out-Null
New-Item -ItemType Directory -Force -Path logs | Out-Null
New-Item -ItemType Directory -Force -Path migrations\versions | Out-Null

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Activate virtual environment: .\.venv\Scripts\Activate.ps1"
Write-Host "  2. Update .env with your configuration"
Write-Host "  3. Start development server: uv run uvicorn src.main:app --reload"
Write-Host "  4. Visit http://localhost:8000/docs for API documentation"
Write-Host ""
