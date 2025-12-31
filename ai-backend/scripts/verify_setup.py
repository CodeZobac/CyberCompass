#!/usr/bin/env python3
"""Verify that the AI backend project structure is correctly set up."""

import sys
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists and report status."""
    if path.exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description}: {path} (MISSING)")
        return False


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if a directory exists and report status."""
    if path.is_dir():
        print(f"✅ {description}: {path}/")
        return True
    else:
        print(f"❌ {description}: {path}/ (MISSING)")
        return False


def main() -> int:
    """Run verification checks."""
    print("🔍 Verifying AI Backend Project Structure...\n")

    root = Path(__file__).parent.parent
    all_checks_passed = True

    # Core configuration files
    print("📋 Configuration Files:")
    all_checks_passed &= check_file_exists(root / "pyproject.toml", "Project config")
    all_checks_passed &= check_file_exists(root / "requirements.txt", "Requirements")
    all_checks_passed &= check_file_exists(root / ".env.example", "Environment template")
    all_checks_passed &= check_file_exists(root / ".gitignore", "Git ignore")
    all_checks_passed &= check_file_exists(root / "README.md", "README")
    all_checks_passed &= check_file_exists(root / "QUICKSTART.md", "Quick start guide")
    print()

    # Docker files
    print("🐳 Docker Configuration:")
    all_checks_passed &= check_file_exists(root / "Dockerfile", "Dockerfile")
    all_checks_passed &= check_file_exists(root / "docker-compose.yml", "Docker Compose")
    print()

    # Source code structure
    print("📦 Source Code Structure:")
    all_checks_passed &= check_directory_exists(root / "src", "Source directory")
    all_checks_passed &= check_file_exists(root / "src" / "__init__.py", "Package init")
    all_checks_passed &= check_file_exists(root / "src" / "main.py", "Main application")
    all_checks_passed &= check_file_exists(root / "src" / "config.py", "Configuration")
    print()

    # Source subdirectories
    print("📁 Source Subdirectories:")
    subdirs = ["agents", "api", "flows", "models", "services", "tools", "utils"]
    for subdir in subdirs:
        all_checks_passed &= check_directory_exists(root / "src" / subdir, f"{subdir.title()}")
        all_checks_passed &= check_file_exists(
            root / "src" / subdir / "__init__.py", f"{subdir.title()} init"
        )
    print()

    # API structure
    print("🌐 API Structure:")
    all_checks_passed &= check_directory_exists(root / "src" / "api" / "routes", "Routes")
    all_checks_passed &= check_directory_exists(
        root / "src" / "api" / "middleware", "Middleware"
    )
    print()

    # Test structure
    print("🧪 Test Structure:")
    all_checks_passed &= check_directory_exists(root / "tests", "Tests directory")
    test_subdirs = ["unit", "integration", "performance"]
    for subdir in test_subdirs:
        all_checks_passed &= check_directory_exists(
            root / "tests" / subdir, f"{subdir.title()} tests"
        )
    print()

    # Configuration
    print("⚙️  Configuration:")
    all_checks_passed &= check_directory_exists(root / "config", "Config directory")
    all_checks_passed &= check_file_exists(root / "config" / "agents.yaml", "Agent config")
    print()

    # Scripts
    print("📜 Setup Scripts:")
    all_checks_passed &= check_directory_exists(root / "scripts", "Scripts directory")
    all_checks_passed &= check_file_exists(root / "scripts" / "setup.sh", "Linux setup")
    all_checks_passed &= check_file_exists(root / "scripts" / "setup.ps1", "Windows setup")
    print()

    # Build tools
    print("🔨 Build Tools:")
    all_checks_passed &= check_file_exists(root / "Makefile", "Makefile")
    all_checks_passed &= check_file_exists(root / "setup.py", "Setup script")
    print()

    # Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("✅ All checks passed! Project structure is complete.")
        print("\nNext steps:")
        print("  1. Run setup script: ./scripts/setup.sh (or setup.ps1 on Windows)")
        print("  2. Configure .env file with your API keys")
        print("  3. Start development: make dev")
        return 0
    else:
        print("❌ Some checks failed. Please review the missing items above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
