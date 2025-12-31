"""
Memory usage and system resource monitoring for AI Backend performance testing.

This module provides comprehensive monitoring of system resources during
performance tests, including memory usage, CPU utilization, and resource leaks.

Requirements: 9.3, 9.4
"""

import asyncio
import time
import psutil
import threading
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import statistics
import json
import gc
import tracemalloc
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ResourceSnapshot:
    """Single point-in-time resource usage snapshot."""
    timestamp: float
    memory_mb: float
    memory_percent: float
    cpu_percent: float
    num_threads: int
    num_connections: int
    num_file_descriptors: int
    system_memory_percent: float
    system_cpu_percent: float
    gc_collections: Dict[int, int] = field(default_factory=dict)


@dataclass
class MemoryProfile:
    """Memory profiling results from tracemalloc."""
    peak_memory_mb: float
    current_memory_mb: float
    top_allocations: List[Dict[str, Any]]
    memory_blocks: int
    total_size_mb: float


class SystemResourceMonitor:
    """
    Comprehensive system resource monitoring for performance testing.
    
    Monitors:
    - Memory usage (RSS, VMS, percent)
    - CPU utilization
    - Thread count
    - File descriptor usage
    - Network connections
    - Garbage collection statistics
    - Memory leak detection
    """
    
    def __init__(self, monitoring_interval: float = 1.0, enable_memory_profiling: bool = True):
        self.monitoring_interval = monitoring_interval
        self.enable_memory_profiling = enable_memory_profiling
        self.monitoring = False
        self.snapshots: List[ResourceSnapshot] = []
        self.monitor_thread: Optional[threading.Thread] = None
        self.process = psutil.Process()
        
        # Memory profiling
        if self.enable_memory_profiling:
            tracemalloc.start()
        
        # Baseline measurements
        self.baseline_snapshot: Optional[ResourceSnapshot] = None
        
    def start_monitoring(self) -> None:
        """Start continuous resource monitoring in background thread."""
        if self.monitoring:
            logger.warning("Monitoring already started")
            return
        
        self.monitoring = True
        self.snapshots.clear()
        
        # Take baseline snapshot
        self.baseline_snapshot = self._take_snapshot()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Started resource monitoring (interval: {self.monitoring_interval}s)")
    
    def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return comprehensive statistics."""
        if not self.monitoring:
            logger.warning("Monitoring not started")
            return {}
        
        self.monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)
        
        # Take final snapshot
        final_snapshot = self._take_snapshot()
        
        # Calculate statistics
        stats = self._calculate_statistics(final_snapshot)
        
        logger.info("Stopped resource monitoring")
        return stats
    
    def get_current_memory_profile(self) -> MemoryProfile:
        """Get current memory profiling information."""
        if not self.enable_memory_profiling:
            return MemoryProfile(0, 0, [], 0, 0)
        
        # Get current memory usage
        current, peak = tracemalloc.get_traced_memory()
        
        # Get top memory allocations
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        top_allocations = []
        for stat in top_stats[:10]:  # Top 10 allocations
            top_allocations.append({
                "filename": stat.traceback.format()[-1] if stat.traceback else "unknown",
                "size_mb": stat.size / 1024 / 1024,
                "count": stat.count,
            })
        
        return MemoryProfile(
            peak_memory_mb=peak / 1024 / 1024,
            current_memory_mb=current / 1024 / 1024,
            top_allocations=top_allocations,
            memory_blocks=len(top_stats),
            total_size_mb=sum(stat.size for stat in top_stats) / 1024 / 1024
        )
    
    def detect_memory_leaks(self, threshold_mb: float = 50.0) -> Dict[str, Any]:
        """
        Detect potential memory leaks by comparing current usage to baseline.
        
        Args:
            threshold_mb: Memory increase threshold to consider as potential leak
            
        Returns:
            Dictionary containing leak detection results
        """
        if not self.baseline_snapshot or not self.snapshots:
            return {"error": "Insufficient data for leak detection"}
        
        current_snapshot = self.snapshots[-1] if self.snapshots else self._take_snapshot()
        
        memory_increase = current_snapshot.memory_mb - self.baseline_snapshot.memory_mb
        thread_increase = current_snapshot.num_threads - self.baseline_snapshot.num_threads
        fd_increase = current_snapshot.num_file_descriptors - self.baseline_snapshot.num_file_descriptors
        
        # Analyze memory trend
        if len(self.snapshots) >= 10:
            recent_memory = [s.memory_mb for s in self.snapshots[-10:]]
            memory_trend = statistics.linear_regression(range(len(recent_memory)), recent_memory).slope
        else:
            memory_trend = 0
        
        leak_indicators = []
        
        if memory_increase > threshold_mb:
            leak_indicators.append(f"Memory increased by {memory_increase:.2f} MB")
        
        if thread_increase > 10:
            leak_indicators.append(f"Thread count increased by {thread_increase}")
        
        if fd_increase > 50:
            leak_indicators.append(f"File descriptor count increased by {fd_increase}")
        
        if memory_trend > 1.0:  # More than 1MB/sample increase trend
            leak_indicators.append(f"Positive memory trend: {memory_trend:.2f} MB/sample")
        
        # Get memory profile for detailed analysis
        memory_profile = self.get_current_memory_profile()
        
        return {
            "potential_leak_detected": len(leak_indicators) > 0,
            "leak_indicators": leak_indicators,
            "memory_increase_mb": memory_increase,
            "thread_increase": thread_increase,
            "fd_increase": fd_increase,
            "memory_trend_mb_per_sample": memory_trend,
            "current_memory_profile": memory_profile,
            "baseline_memory_mb": self.baseline_snapshot.memory_mb,
            "current_memory_mb": current_snapshot.memory_mb,
        }
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop running in background thread."""
        while self.monitoring:
            try:
                snapshot = self._take_snapshot()
                self.snapshots.append(snapshot)
                
                # Log warnings for high resource usage
                if snapshot.memory_percent > 80:
                    logger.warning(f"High memory usage: {snapshot.memory_percent:.1f}%")
                
                if snapshot.cpu_percent > 90:
                    logger.warning(f"High CPU usage: {snapshot.cpu_percent:.1f}%")
                
                if snapshot.num_file_descriptors > 1000:
                    logger.warning(f"High file descriptor usage: {snapshot.num_file_descriptors}")
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            time.sleep(self.monitoring_interval)
    
    def _take_snapshot(self) -> ResourceSnapshot:
        """Take a single resource usage snapshot."""
        try:
            # Process-specific metrics
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            memory_percent = self.process.memory_percent()
            cpu_percent = self.process.cpu_percent()
            num_threads = self.process.num_threads()
            
            # Network connections
            try:
                connections = self.process.connections()
                num_connections = len(connections)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                num_connections = 0
            
            # File descriptors
            try:
                num_fds = self.process.num_fds() if hasattr(self.process, 'num_fds') else 0
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                num_fds = 0
            
            # System-wide metrics
            system_memory = psutil.virtual_memory()
            system_cpu = psutil.cpu_percent()
            
            # Garbage collection stats
            gc_stats = {}
            for generation in range(3):
                gc_stats[generation] = gc.get_count()[generation]
            
            return ResourceSnapshot(
                timestamp=time.time(),
                memory_mb=memory_mb,
                memory_percent=memory_percent,
                cpu_percent=cpu_percent,
                num_threads=num_threads,
                num_connections=num_connections,
                num_file_descriptors=num_fds,
                system_memory_percent=system_memory.percent,
                system_cpu_percent=system_cpu,
                gc_collections=gc_stats,
            )
            
        except Exception as e:
            logger.error(f"Error taking resource snapshot: {e}")
            return ResourceSnapshot(
                timestamp=time.time(),
                memory_mb=0, memory_percent=0, cpu_percent=0,
                num_threads=0, num_connections=0, num_file_descriptors=0,
                system_memory_percent=0, system_cpu_percent=0
            )
    
    def _calculate_statistics(self, final_snapshot: ResourceSnapshot) -> Dict[str, Any]:
        """Calculate comprehensive statistics from collected snapshots."""
        if not self.snapshots:
            return {"error": "No snapshots collected"}
        
        # Extract time series data
        timestamps = [s.timestamp for s in self.snapshots]
        memory_mb = [s.memory_mb for s in self.snapshots]
        memory_percent = [s.memory_percent for s in self.snapshots]
        cpu_percent = [s.cpu_percent for s in self.snapshots]
        num_threads = [s.num_threads for s in self.snapshots]
        num_connections = [s.num_connections for s in self.snapshots]
        
        # Calculate duration
        duration_seconds = timestamps[-1] - timestamps[0] if len(timestamps) > 1 else 0
        
        # Memory statistics
        memory_stats = {
            "initial_mb": memory_mb[0] if memory_mb else 0,
            "final_mb": memory_mb[-1] if memory_mb else 0,
            "peak_mb": max(memory_mb) if memory_mb else 0,
            "min_mb": min(memory_mb) if memory_mb else 0,
            "mean_mb": statistics.mean(memory_mb) if memory_mb else 0,
            "median_mb": statistics.median(memory_mb) if memory_mb else 0,
            "increase_mb": (memory_mb[-1] - memory_mb[0]) if len(memory_mb) > 1 else 0,
        }
        
        # CPU statistics
        cpu_stats = {
            "mean_percent": statistics.mean(cpu_percent) if cpu_percent else 0,
            "peak_percent": max(cpu_percent) if cpu_percent else 0,
            "min_percent": min(cpu_percent) if cpu_percent else 0,
        }
        
        # Thread statistics
        thread_stats = {
            "initial_count": num_threads[0] if num_threads else 0,
            "final_count": num_threads[-1] if num_threads else 0,
            "peak_count": max(num_threads) if num_threads else 0,
            "increase": (num_threads[-1] - num_threads[0]) if len(num_threads) > 1 else 0,
        }
        
        # Connection statistics
        connection_stats = {
            "initial_count": num_connections[0] if num_connections else 0,
            "final_count": num_connections[-1] if num_connections else 0,
            "peak_count": max(num_connections) if num_connections else 0,
        }
        
        # Memory profiling results
        memory_profile = self.get_current_memory_profile() if self.enable_memory_profiling else None
        
        # Leak detection
        leak_detection = self.detect_memory_leaks()
        
        return {
            "monitoring_duration_seconds": duration_seconds,
            "samples_collected": len(self.snapshots),
            "sampling_interval_seconds": self.monitoring_interval,
            "memory_statistics": memory_stats,
            "cpu_statistics": cpu_stats,
            "thread_statistics": thread_stats,
            "connection_statistics": connection_stats,
            "memory_profile": memory_profile.__dict__ if memory_profile else None,
            "leak_detection": leak_detection,
            "baseline_snapshot": self.baseline_snapshot.__dict__ if self.baseline_snapshot else None,
            "final_snapshot": final_snapshot.__dict__,
        }


@asynccontextmanager
async def monitor_performance(
    monitoring_interval: float = 1.0,
    enable_memory_profiling: bool = True,
    leak_detection_threshold_mb: float = 50.0
):
    """
    Context manager for performance monitoring during tests.
    
    Usage:
        async with monitor_performance() as monitor:
            # Run performance tests
            await run_tests()
            
            # Check for memory leaks
            leak_info = monitor.detect_memory_leaks()
    """
    monitor = SystemResourceMonitor(
        monitoring_interval=monitoring_interval,
        enable_memory_profiling=enable_memory_profiling
    )
    
    try:
        monitor.start_monitoring()
        yield monitor
    finally:
        stats = monitor.stop_monitoring()
        
        # Log performance summary
        if stats:
            logger.info("=== PERFORMANCE MONITORING RESULTS ===")
            if "memory_statistics" in stats:
                mem_stats = stats["memory_statistics"]
                logger.info(f"Memory: {mem_stats['initial_mb']:.1f} → {mem_stats['final_mb']:.1f} MB (peak: {mem_stats['peak_mb']:.1f} MB)")
            
            if "cpu_statistics" in stats:
                cpu_stats = stats["cpu_statistics"]
                logger.info(f"CPU: mean {cpu_stats['mean_percent']:.1f}%, peak {cpu_stats['peak_percent']:.1f}%")
            
            if "leak_detection" in stats and stats["leak_detection"].get("potential_leak_detected"):
                logger.warning("⚠️  Potential memory leak detected!")
                for indicator in stats["leak_detection"]["leak_indicators"]:
                    logger.warning(f"  - {indicator}")
        
        # Save detailed results
        timestamp = int(time.time())
        with open(f"performance_monitoring_{timestamp}.json", "w") as f:
            json.dump(stats, f, indent=2, default=str)


class PerformanceTestRunner:
    """
    Utility class for running performance tests with comprehensive monitoring.
    """
    
    @staticmethod
    async def run_with_monitoring(
        test_function: Callable,
        test_name: str,
        monitoring_interval: float = 1.0,
        **test_kwargs
    ) -> Dict[str, Any]:
        """
        Run a test function with comprehensive performance monitoring.
        
        Args:
            test_function: Async function to test
            test_name: Name of the test for logging
            monitoring_interval: Resource monitoring interval
            **test_kwargs: Arguments to pass to test function
            
        Returns:
            Dictionary containing test results and performance metrics
        """
        logger.info(f"Starting performance test: {test_name}")
        
        async with monitor_performance(monitoring_interval=monitoring_interval) as monitor:
            start_time = time.time()
            
            try:
                # Run the test
                test_results = await test_function(**test_kwargs)
                test_duration = time.time() - start_time
                
                # Get final performance stats
                performance_stats = monitor.stop_monitoring()
                
                # Combine results
                combined_results = {
                    "test_name": test_name,
                    "test_duration_seconds": test_duration,
                    "test_results": test_results,
                    "performance_metrics": performance_stats,
                    "success": True,
                }
                
                logger.info(f"Performance test '{test_name}' completed successfully in {test_duration:.2f}s")
                return combined_results
                
            except Exception as e:
                test_duration = time.time() - start_time
                logger.error(f"Performance test '{test_name}' failed after {test_duration:.2f}s: {e}")
                
                return {
                    "test_name": test_name,
                    "test_duration_seconds": test_duration,
                    "error": str(e),
                    "performance_metrics": monitor.stop_monitoring(),
                    "success": False,
                }


# Example usage and test functions
async def example_memory_intensive_task():
    """Example task that uses memory for testing."""
    data = []
    for i in range(1000):
        # Simulate memory allocation
        data.append([0] * 1000)  # 1000 integers per iteration
        
        if i % 100 == 0:
            await asyncio.sleep(0.1)  # Yield control
    
    return {"allocated_arrays": len(data)}


async def run_memory_monitoring_tests():
    """Run comprehensive memory monitoring tests."""
    logger.info("Starting memory monitoring tests")
    
    # Test 1: Basic monitoring
    test_results = await PerformanceTestRunner.run_with_monitoring(
        example_memory_intensive_task,
        "Memory Intensive Task",
        monitoring_interval=0.5
    )
    
    # Test 2: Memory leak detection
    async def potential_leak_task():
        """Task that might have memory leaks."""
        leaked_data = []
        for i in range(100):
            leaked_data.append([0] * 10000)  # Don't clean up
            await asyncio.sleep(0.01)
        
        # Simulate some cleanup (but not all)
        del leaked_data[::2]  # Delete every other item
        
        return {"potential_leaks": len(leaked_data)}
    
    leak_test_results = await PerformanceTestRunner.run_with_monitoring(
        potential_leak_task,
        "Memory Leak Detection Test",
        monitoring_interval=0.2
    )
    
    # Generate summary report
    logger.info("=== MEMORY MONITORING TEST SUMMARY ===")
    for test_result in [test_results, leak_test_results]:
        if test_result["success"]:
            perf_metrics = test_result["performance_metrics"]
            if "memory_statistics" in perf_metrics:
                mem_stats = perf_metrics["memory_statistics"]
                logger.info(f"{test_result['test_name']}: {mem_stats['increase_mb']:.2f} MB increase")
            
            if "leak_detection" in perf_metrics:
                leak_info = perf_metrics["leak_detection"]
                if leak_info.get("potential_leak_detected"):
                    logger.warning(f"⚠️  {test_result['test_name']}: Potential leak detected")
        else:
            logger.error(f"❌ {test_result['test_name']}: Failed")
    
    return [test_results, leak_test_results]


if __name__ == "__main__":
    # Run memory monitoring tests
    asyncio.run(run_memory_monitoring_tests())