"""
Test runner script for unit tests.
Uses uv package manager to run pytest with proper configuration.
"""

import subprocess
import sys
from pathlib import Path


def run_tests(test_path=None, verbose=True, coverage=False):
    """
    Run unit tests using uv and pytest.
    
    Args:
        test_path: Specific test file or directory to run (optional)
        verbose: Enable verbose output
        coverage: Enable coverage reporting
    """
    # Base command using uv
    cmd = ["uv", "run", "pytest"]
    
    # Add test path or default to unit tests
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/unit/")
    
    # Add verbose flag
    if verbose:
        cmd.append("-v")
    
    # Add coverage flags
    if coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    # Add short traceback for cleaner output
    cmd.append("--tb=short")
    
    print("=" * 70)
    print("Running Unit Tests with uv")
    print("=" * 70)
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("❌ Error: 'uv' command not found.")
        print("Please install uv: https://docs.astral.sh/uv/")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def main():
    """Main entry point for test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run unit tests using uv")
    parser.add_argument(
        "test_path",
        nargs="?",
        help="Specific test file or directory to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=True,
        help="Enable verbose output (default: True)"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Enable coverage reporting"
    )
    parser.add_argument(
        "--agents",
        action="store_true",
        help="Run only agent tests"
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Run only API endpoint tests"
    )
    parser.add_argument(
        "--websocket",
        action="store_true",
        help="Run only WebSocket tests"
    )
    
    args = parser.parse_args()
    
    # Determine test path
    test_path = args.test_path
    
    if args.agents:
        test_path = "tests/unit/test_agents.py"
    elif args.api:
        test_path = "tests/unit/test_api_endpoints.py"
    elif args.websocket:
        test_path = "tests/unit/test_websocket.py"
    
    # Run tests
    exit_code = run_tests(
        test_path=test_path,
        verbose=args.verbose,
        coverage=args.coverage
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
