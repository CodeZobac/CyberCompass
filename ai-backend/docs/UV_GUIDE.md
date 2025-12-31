# UV Package Manager Guide

This project uses [uv](https://docs.astral.sh/uv/), a modern, fast Python package manager.

## Installation

### Linux/macOS
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Basic Commands

```bash
# Install dependencies
uv sync

# Add new package
uv add package-name

# Run command
uv run python script.py

# Create virtual environment
uv venv
```

## Quick Reference

- `uv sync` - Install all dependencies
- `uv add <pkg>` - Add a package
- `uv remove <pkg>` - Remove a package
- `uv run <cmd>` - Run command in venv
- `uv --help` - Get help

For full documentation: https://docs.astral.sh/uv/
