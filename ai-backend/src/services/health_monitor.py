"""
Service health monitoring and automatic recovery system.

This module monitors the health of AI services and implements automatic
recovery strategies when failures are detected.
"""

import asyncio
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from enum import Enum

from ..utils.error_handler import logger, health_checker
from ..utils.exceptions import AIServiceError, ExternalServiceError


class ServiceStatus(str, Enum):
    """Service health status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    RECOVERING = "recovering"


class RecoveryStrategy(str, Enum):
    """Recovery strategies for service failures."""
    RESTART = "restart"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    RETRY = "retry"


class ServiceHealthMonitor:
    """
    Monitor service health and implement automatic recovery.
    
    This class tracks the health of various AI services and implements
    recovery strategies when failures are detected.
    """
    
    def __init__(self):
        self.service_status: Dict[str, ServiceStatus] = {}
        self.failure_counts: Dict[str, int] = {}
        self.last_check: Dict[str, datetime] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.recovery_callbacks: Dict[str, Callable] = {}
        self.monitoring_tasks: List[asyncio.Task] = []
        self.is_monitoring = False
    
    async def start_monitoring(self, check_interval: int = 30):
        """
        Start continuous health monitoring.
        
        Args:
            check_interval: Seconds between health checks
        """
        if self.is_monitoring:
            logger.warning("Health monitoring already running")
            return
        
        self.is_monitoring = True
        logger.info("Starting health monitoring", interval=check_interval)
        
        # Start monitoring task
        task = asyncio.create_task(self._monitoring_loop(check_interval))
        self.monitoring_tasks.append(task)
    
    async def stop_monitoring(self):
        """Stop health monitoring."""
        self.is_monitoring = False
        
        # Cancel all monitoring tasks
        for task in self.monitoring_tasks:
            task.cancel()
        
        await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
        self.monitoring_tasks.clear()
        
        logger.info("Health monitoring stopped")
    
    async def _monitoring_loop(self, check_interval: int):
        """Continuous monitoring loop."""
        while self.is_monitoring:
            try:
                await self.check_all_services()
                await asyncio.sleep(check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.exception("Error in monitoring loop", exc=e)
                await asyncio.sleep(check_interval)
    
    def register_service(
        self,
        service_name: str,
        health_check: Callable,
        recovery_callback: Optional[Callable] = None
    ):
        """
        Register a service for health monitoring.
        
        Args:
            service_name: Name of the service
            health_check: Async function that returns True if service is healthy
            recovery_callback: Optional async function to call for recovery
        """
        self.service_status[service_name] = ServiceStatus.HEALTHY
        self.failure_counts[service_name] = 0
        self.circuit_breakers[service_name] = CircuitBreaker(service_name)
        
        if recovery_callback:
            self.recovery_callbacks[service_name] = recovery_callback
        
        logger.info(f"Registered service for monitoring: {service_name}")
    
    async def check_service_health(
        self,
        service_name: str,
        health_check: Callable
    ) -> ServiceStatus:
        """
        Check health of a specific service.
        
        Args:
            service_name: Name of the service to check
            health_check: Async function that returns True if healthy
        
        Returns:
            Current service status
        """
        try:
            # Check if circuit breaker is open
            circuit_breaker = self.circuit_breakers.get(service_name)
            if circuit_breaker and circuit_breaker.is_open():
                logger.warning(
                    f"Circuit breaker open for {service_name}",
                    status=ServiceStatus.UNHEALTHY
                )
                return ServiceStatus.UNHEALTHY
            
            # Perform health check
            is_healthy = await health_check()
            
            if is_healthy:
                # Service is healthy
                self.failure_counts[service_name] = 0
                self.service_status[service_name] = ServiceStatus.HEALTHY
                
                if circuit_breaker:
                    circuit_breaker.record_success()
                
                logger.info(f"Service healthy: {service_name}")
            else:
                # Service is unhealthy
                await self._handle_service_failure(service_name)
            
            self.last_check[service_name] = datetime.utcnow()
            return self.service_status[service_name]
            
        except Exception as e:
            logger.exception(f"Health check failed for {service_name}", exc=e)
            await self._handle_service_failure(service_name)
            return ServiceStatus.UNHEALTHY
    
    async def _handle_service_failure(self, service_name: str):
        """Handle service failure and attempt recovery."""
        self.failure_counts[service_name] = self.failure_counts.get(service_name, 0) + 1
        failure_count = self.failure_counts[service_name]
        
        logger.warning(
            f"Service failure detected: {service_name}",
            failure_count=failure_count
        )
        
        # Update circuit breaker
        circuit_breaker = self.circuit_breakers.get(service_name)
        if circuit_breaker:
            circuit_breaker.record_failure()
        
        # Determine status based on failure count
        if failure_count >= 5:
            self.service_status[service_name] = ServiceStatus.UNHEALTHY
        elif failure_count >= 2:
            self.service_status[service_name] = ServiceStatus.DEGRADED
        
        # Attempt recovery
        await self._attempt_recovery(service_name)
    
    async def _attempt_recovery(self, service_name: str):
        """Attempt to recover a failed service."""
        recovery_callback = self.recovery_callbacks.get(service_name)
        
        if not recovery_callback:
            logger.warning(f"No recovery callback for {service_name}")
            return
        
        try:
            self.service_status[service_name] = ServiceStatus.RECOVERING
            logger.info(f"Attempting recovery for {service_name}")
            
            # Call recovery callback
            await recovery_callback()
            
            # Reset failure count on successful recovery
            self.failure_counts[service_name] = 0
            self.service_status[service_name] = ServiceStatus.HEALTHY
            
            logger.info(f"Recovery successful for {service_name}")
            
        except Exception as e:
            logger.exception(f"Recovery failed for {service_name}", exc=e)
            self.service_status[service_name] = ServiceStatus.UNHEALTHY
    
    async def check_all_services(self) -> Dict[str, ServiceStatus]:
        """Check health of all registered services."""
        results = {}
        
        for service_name in self.service_status.keys():
            # Use health_checker for the actual check
            is_healthy = await health_checker.check_component(
                service_name,
                lambda: self._default_health_check(service_name)
            )
            
            if is_healthy:
                results[service_name] = ServiceStatus.HEALTHY
            else:
                await self._handle_service_failure(service_name)
                results[service_name] = self.service_status[service_name]
        
        return results
    
    async def _default_health_check(self, service_name: str) -> bool:
        """Default health check implementation."""
        # This is a placeholder - actual health checks should be registered
        return self.service_status.get(service_name) == ServiceStatus.HEALTHY
    
    def get_service_status(self, service_name: str) -> ServiceStatus:
        """Get current status of a service."""
        return self.service_status.get(service_name, ServiceStatus.UNHEALTHY)
    
    def is_service_available(self, service_name: str) -> bool:
        """Check if service is available for use."""
        status = self.get_service_status(service_name)
        return status in [ServiceStatus.HEALTHY, ServiceStatus.DEGRADED]
    
    def get_health_report(self) -> Dict[str, Any]:
        """Get comprehensive health report."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                name: {
                    "status": status.value,
                    "failure_count": self.failure_counts.get(name, 0),
                    "last_check": self.last_check.get(name, datetime.utcnow()).isoformat(),
                    "circuit_breaker": self.circuit_breakers[name].get_state() if name in self.circuit_breakers else None
                }
                for name, status in self.service_status.items()
            },
            "overall_health": self._calculate_overall_health()
        }
    
    def _calculate_overall_health(self) -> str:
        """Calculate overall system health."""
        if not self.service_status:
            return "unknown"
        
        statuses = list(self.service_status.values())
        
        if all(s == ServiceStatus.HEALTHY for s in statuses):
            return "healthy"
        elif any(s == ServiceStatus.UNHEALTHY for s in statuses):
            return "unhealthy"
        else:
            return "degraded"


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for service protection.
    
    Prevents cascading failures by temporarily blocking requests to
    failing services.
    """
    
    def __init__(
        self,
        service_name: str,
        failure_threshold: int = 5,
        timeout: int = 60,
        success_threshold: int = 2
    ):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half_open
    
    def record_failure(self):
        """Record a service failure."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        self.success_count = 0
        
        if self.failure_count >= self.failure_threshold:
            self._open_circuit()
    
    def record_success(self):
        """Record a successful service call."""
        self.success_count += 1
        
        if self.state == "half_open" and self.success_count >= self.success_threshold:
            self._close_circuit()
    
    def _open_circuit(self):
        """Open the circuit breaker."""
        self.state = "open"
        logger.warning(
            f"Circuit breaker opened for {self.service_name}",
            failure_count=self.failure_count
        )
    
    def _close_circuit(self):
        """Close the circuit breaker."""
        self.state = "closed"
        self.failure_count = 0
        self.success_count = 0
        logger.info(f"Circuit breaker closed for {self.service_name}")
    
    def is_open(self) -> bool:
        """Check if circuit breaker is open."""
        if self.state == "open":
            # Check if timeout has elapsed
            if self.last_failure_time:
                elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
                if elapsed >= self.timeout:
                    self.state = "half_open"
                    logger.info(f"Circuit breaker half-open for {self.service_name}")
                    return False
            return True
        return False
    
    def get_state(self) -> Dict[str, Any]:
        """Get circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None
        }


# Global health monitor instance
health_monitor = ServiceHealthMonitor()
