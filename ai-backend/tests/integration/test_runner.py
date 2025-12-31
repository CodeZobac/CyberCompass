"""
Integration test runner for CrewAI workflows.

This module provides utilities for running integration tests with proper
setup, teardown, and reporting for CrewAI workflow testing.

Requirements tested: 9.1, 9.2
"""

import pytest
import asyncio
import time
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import patch
import logging

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from test_crewai_flows import *
from test_agent_collaboration import *
from test_memory_persistence import *


class IntegrationTestRunner:
    """Runner for integration tests with comprehensive reporting."""
    
    def __init__(self):
        self.test_results: Dict[str, Any] = {}
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def run_all_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """Run all integration tests and return comprehensive results."""
        self.start_time = time.time()
        self.logger.info("Starting CrewAI integration test suite...")
        
        # Test categories to run
        test_categories = [
            {
                "name": "CrewAI Flow Execution",
                "module": "test_crewai_flows",
                "description": "Tests complete flow executions from start to finish"
            },
            {
                "name": "Agent Collaboration",
                "module": "test_agent_collaboration", 
                "description": "Tests agent collaboration and task delegation"
            },
            {
                "name": "Memory Persistence",
                "module": "test_memory_persistence",
                "description": "Tests memory persistence and context preservation"
            }
        ]
        
        results = {}
        
        for category in test_categories:
            self.logger.info(f"Running {category['name']} tests...")
            
            category_result = self._run_test_category(
                category["module"],
                verbose=verbose
            )
            
            results[category["name"]] = {
                "description": category["description"],
                "results": category_result,
                "status": "PASSED" if category_result["failed"] == 0 else "FAILED"
            }
            
            self.logger.info(
                f"{category['name']}: {category_result['passed']} passed, "
                f"{category_result['failed']} failed"
            )
        
        self.end_time = time.time()
        
        # Generate summary
        summary = self._generate_test_summary(results)
        
        if verbose:
            self._print_detailed_results(results, summary)
        
        return {
            "summary": summary,
            "categories": results,
            "execution_time": self.end_time - self.start_time
        }
    
    def _run_test_category(self, module_name: str, verbose: bool = False) -> Dict[str, Any]:
        """Run tests for a specific category."""
        # Use pytest to run tests programmatically
        pytest_args = [
            f"tests/integration/{module_name}.py",
            "-v" if verbose else "-q",
            "--tb=short",
            "--no-header"
        ]
        
        # Capture pytest results
        result = pytest.main(pytest_args)
        
        # Parse results (simplified for this example)
        # In a real implementation, you'd use pytest's programmatic API
        # to get detailed results
        
        if result == 0:
            return {"passed": 1, "failed": 0, "skipped": 0, "errors": []}
        else:
            return {"passed": 0, "failed": 1, "skipped": 0, "errors": ["Test execution failed"]}
    
    def _generate_test_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall test summary."""
        total_passed = sum(r["results"]["passed"] for r in results.values())
        total_failed = sum(r["results"]["failed"] for r in results.values())
        total_skipped = sum(r["results"]["skipped"] for r in results.values())
        
        categories_passed = sum(1 for r in results.values() if r["status"] == "PASSED")
        categories_failed = sum(1 for r in results.values() if r["status"] == "FAILED")
        
        return {
            "total_tests": total_passed + total_failed + total_skipped,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "categories_passed": categories_passed,
            "categories_failed": categories_failed,
            "overall_status": "PASSED" if total_failed == 0 else "FAILED",
            "success_rate": (total_passed / (total_passed + total_failed)) * 100 if (total_passed + total_failed) > 0 else 0
        }
    
    def _print_detailed_results(self, results: Dict[str, Any], summary: Dict[str, Any]):
        """Print detailed test results."""
        print("\n" + "="*80)
        print("CREWAI INTEGRATION TEST RESULTS")
        print("="*80)
        
        # Print category results
        for category_name, category_data in results.items():
            status_symbol = "✓" if category_data["status"] == "PASSED" else "✗"
            print(f"\n{status_symbol} {category_name}")
            print(f"   {category_data['description']}")
            
            results_data = category_data["results"]
            print(f"   Passed: {results_data['passed']}, Failed: {results_data['failed']}, Skipped: {results_data['skipped']}")
            
            if results_data["errors"]:
                print("   Errors:")
                for error in results_data["errors"]:
                    print(f"     - {error}")
        
        # Print summary
        print("\n" + "-"*80)
        print("SUMMARY")
        print("-"*80)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['total_passed']}")
        print(f"Failed: {summary['total_failed']}")
        print(f"Skipped: {summary['total_skipped']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Execution Time: {self.end_time - self.start_time:.2f} seconds")
        
        overall_symbol = "✓" if summary["overall_status"] == "PASSED" else "✗"
        print(f"\nOverall Status: {overall_symbol} {summary['overall_status']}")


class PerformanceTestRunner:
    """Runner for performance and load testing of CrewAI workflows."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def run_concurrent_flow_test(self, num_concurrent: int = 5) -> Dict[str, Any]:
        """Test concurrent execution of multiple flows."""
        self.logger.info(f"Running concurrent flow test with {num_concurrent} flows...")
        
        start_time = time.time()
        
        # Create mock factory
        mock_factory = MockAgentFactory()
        
        # Create multiple flows
        flows = [
            DeepfakeDetectionFlow(mock_factory, locale="en"),
            SocialMediaSimulationFlow(mock_factory, locale="en"),
            CatfishDetectionFlow(mock_factory, locale="en")
        ]
        
        # Create test requests
        requests = [
            DeepfakeChallengeRequest(user_id=f"user_{i}", difficulty_level=1, locale=LocaleEnum.EN),
            SocialMediaSimulationRequest(user_id=f"user_{i}", session_duration_minutes=5, locale=LocaleEnum.EN),
            CatfishChatStartRequest(user_id=f"user_{i}", difficulty_level=1, locale=LocaleEnum.EN)
        ]
        
        # Run concurrent operations
        async def run_flow_operation(flow_index: int):
            flow = flows[flow_index % len(flows)]
            request = requests[flow_index % len(requests)]
            
            with patch('crewai.Crew.kickoff') as mock_kickoff:
                mock_kickoff.return_value = Mock(raw="Concurrent test result")
                
                if isinstance(flow, DeepfakeDetectionFlow):
                    return flow.initialize_challenge(request)
                elif isinstance(flow, SocialMediaSimulationFlow):
                    return flow.initialize_simulation(request)
                elif isinstance(flow, CatfishDetectionFlow):
                    return flow.initialize_character(request)
        
        # Execute concurrent tasks
        tasks = [run_flow_operation(i) for i in range(num_concurrent)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        
        # Analyze results
        successful_results = [r for r in results if not isinstance(r, Exception)]
        failed_results = [r for r in results if isinstance(r, Exception)]
        
        return {
            "concurrent_flows": num_concurrent,
            "successful": len(successful_results),
            "failed": len(failed_results),
            "execution_time": end_time - start_time,
            "avg_time_per_flow": (end_time - start_time) / num_concurrent,
            "errors": [str(e) for e in failed_results]
        }
    
    def run_memory_stress_test(self, num_sessions: int = 10) -> Dict[str, Any]:
        """Test memory system under stress with multiple sessions."""
        self.logger.info(f"Running memory stress test with {num_sessions} sessions...")
        
        start_time = time.time()
        
        # Create memory system
        memory_systems = {
            "long_term": MockMemorySystem("long_term"),
            "short_term": MockMemorySystem("short_term")
        }
        
        # Create multiple agents with different sessions
        agents = []
        for i in range(num_sessions):
            agent = MockAgentWithMemory(f"agent_{i}", memory_systems["long_term"])
            agent.set_session(str(uuid.uuid4()))
            agents.append(agent)
        
        # Perform memory operations
        operations_per_agent = 50
        
        for agent in agents:
            for j in range(operations_per_agent):
                # Store data
                agent.remember(f"key_{j}", {"value": j, "data": f"test_data_{j}"})
                
                # Retrieve data
                retrieved = agent.recall(f"key_{j}")
                assert retrieved is not None
                
                # Search memory
                search_results = agent.search_memory(f"test_data_{j}")
                assert len(search_results) > 0
        
        end_time = time.time()
        
        # Analyze memory performance
        long_term_stats = memory_systems["long_term"].get_access_stats()
        
        return {
            "sessions": num_sessions,
            "operations_per_session": operations_per_agent * 3,  # store + retrieve + search
            "total_operations": long_term_stats["total_operations"],
            "execution_time": end_time - start_time,
            "operations_per_second": long_term_stats["total_operations"] / (end_time - start_time),
            "memory_stats": long_term_stats
        }


def run_integration_tests():
    """Main function to run all integration tests."""
    runner = IntegrationTestRunner()
    results = runner.run_all_tests(verbose=True)
    
    # Return exit code based on results
    return 0 if results["summary"]["overall_status"] == "PASSED" else 1


async def run_performance_tests():
    """Run performance tests."""
    perf_runner = PerformanceTestRunner()
    
    print("\n" + "="*80)
    print("PERFORMANCE TESTS")
    print("="*80)
    
    # Test concurrent flows
    concurrent_results = await perf_runner.run_concurrent_flow_test(num_concurrent=5)
    print(f"\nConcurrent Flow Test:")
    print(f"  Flows: {concurrent_results['concurrent_flows']}")
    print(f"  Successful: {concurrent_results['successful']}")
    print(f"  Failed: {concurrent_results['failed']}")
    print(f"  Total Time: {concurrent_results['execution_time']:.2f}s")
    print(f"  Avg Time per Flow: {concurrent_results['avg_time_per_flow']:.2f}s")
    
    # Test memory stress
    memory_results = perf_runner.run_memory_stress_test(num_sessions=10)
    print(f"\nMemory Stress Test:")
    print(f"  Sessions: {memory_results['sessions']}")
    print(f"  Total Operations: {memory_results['total_operations']}")
    print(f"  Operations/Second: {memory_results['operations_per_second']:.1f}")
    print(f"  Execution Time: {memory_results['execution_time']:.2f}s")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--performance":
        # Run performance tests
        asyncio.run(run_performance_tests())
    else:
        # Run integration tests
        exit_code = run_integration_tests()
        sys.exit(exit_code)