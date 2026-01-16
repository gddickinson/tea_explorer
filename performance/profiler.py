"""
Performance Profiling and Monitoring
Provides decorators and utilities for tracking performance metrics
"""

from functools import wraps
from typing import Callable, Dict, Any, List
import time
import threading
from pathlib import Path
import sys
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin


class PerformanceMetrics:
    """Store and manage performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.call_counts: Dict[str, int] = defaultdict(int)
        self.lock = threading.Lock()
    
    def record(self, operation: str, duration: float):
        """Record an operation's execution time"""
        with self.lock:
            self.metrics[operation].append(duration)
            self.call_counts[operation] += 1
    
    def get_stats(self, operation: str) -> Dict[str, Any]:
        """Get statistics for an operation"""
        if operation not in self.metrics or not self.metrics[operation]:
            return {}
        
        durations = self.metrics[operation]
        return {
            'count': self.call_counts[operation],
            'total_time': sum(durations),
            'avg_time': sum(durations) / len(durations),
            'min_time': min(durations),
            'max_time': max(durations),
            'last_time': durations[-1]
        }
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all operations"""
        return {op: self.get_stats(op) for op in self.metrics.keys()}
    
    def get_slowest(self, n: int = 10) -> List[tuple]:
        """Get N slowest operations by average time"""
        all_stats = self.get_all_stats()
        sorted_ops = sorted(
            all_stats.items(),
            key=lambda x: x[1].get('avg_time', 0),
            reverse=True
        )
        return sorted_ops[:n]
    
    def get_most_called(self, n: int = 10) -> List[tuple]:
        """Get N most frequently called operations"""
        sorted_ops = sorted(
            self.call_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_ops[:n]
    
    def reset(self):
        """Reset all metrics"""
        with self.lock:
            self.metrics.clear()
            self.call_counts.clear()


class PerformanceMonitor(LoggerMixin):
    """
    Global performance monitor
    Singleton that tracks all profiled operations
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.metrics = PerformanceMetrics()
            self.enabled = True
            self.initialized = True
            self.logger.info("PerformanceMonitor initialized")
    
    def record(self, operation: str, duration: float):
        """Record an operation"""
        if self.enabled:
            self.metrics.record(operation, duration)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all performance statistics"""
        return {
            'all_operations': self.metrics.get_all_stats(),
            'slowest_operations': self.metrics.get_slowest(10),
            'most_called': self.metrics.get_most_called(10),
        }
    
    def print_report(self):
        """Print performance report"""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)
        
        print("\n📊 SLOWEST OPERATIONS (by average time):")
        print("-" * 60)
        for op, op_stats in stats['slowest_operations']:
            avg = op_stats['avg_time'] * 1000  # Convert to ms
            count = op_stats['count']
            print(f"  {op:40s} {avg:8.2f}ms (x{count})")
        
        print("\n📈 MOST CALLED OPERATIONS:")
        print("-" * 60)
        for op, count in stats['most_called']:
            op_stats = self.metrics.get_stats(op)
            avg = op_stats['avg_time'] * 1000 if op_stats else 0
            print(f"  {op:40s} {count:6d} calls ({avg:.2f}ms avg)")
        
        print("\n" + "="*60)
    
    def log_stats(self):
        """Log performance statistics"""
        stats = self.get_stats()
        
        self.logger.info("="*60)
        self.logger.info("PERFORMANCE STATISTICS")
        self.logger.info("="*60)
        
        for op, op_stats in stats['slowest_operations'][:5]:
            avg = op_stats['avg_time'] * 1000
            count = op_stats['count']
            self.logger.info(f"{op}: {avg:.2f}ms avg (x{count})")
    
    def reset(self):
        """Reset all metrics"""
        self.metrics.reset()
        self.logger.info("Performance metrics reset")
    
    def enable(self):
        """Enable performance monitoring"""
        self.enabled = True
        self.logger.info("Performance monitoring enabled")
    
    def disable(self):
        """Disable performance monitoring"""
        self.enabled = False
        self.logger.info("Performance monitoring disabled")


def profile(func: Callable) -> Callable:
    """
    Decorator to profile function execution time
    
    Usage:
        @profile
        def slow_function():
            pass
    """
    monitor = PerformanceMonitor()
    operation_name = f"{func.__module__}.{func.__name__}"
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            monitor.record(operation_name, duration)
    
    return wrapper


def profile_method(func: Callable) -> Callable:
    """
    Decorator to profile class method execution time
    Includes class name in operation name
    
    Usage:
        class MyClass:
            @profile_method
            def slow_method(self):
                pass
    """
    monitor = PerformanceMonitor()
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        class_name = self.__class__.__name__
        operation_name = f"{class_name}.{func.__name__}"
        
        start_time = time.time()
        try:
            result = func(self, *args, **kwargs)
            return result
        finally:
            duration = time.time() - start_time
            monitor.record(operation_name, duration)
    
    return wrapper


class Timer:
    """Context manager for timing code blocks"""
    
    def __init__(self, name: str, log: bool = True):
        """
        Initialize timer
        
        Args:
            name: Name for this timer
            log: Whether to log the result
        """
        self.name = name
        self.log = log
        self.start_time = None
        self.duration = None
        self.monitor = PerformanceMonitor()
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.duration = time.time() - self.start_time
        self.monitor.record(self.name, self.duration)
        
        if self.log:
            duration_ms = self.duration * 1000
            print(f"[TIMER] {self.name}: {duration_ms:.2f}ms")
    
    def elapsed(self) -> float:
        """Get elapsed time (call after __exit__)"""
        return self.duration if self.duration else 0


# Global monitor instance
monitor = PerformanceMonitor()


if __name__ == '__main__':
    # Demo usage
    import time
    
    @profile
    def slow_function(n):
        """Simulates slow function"""
        time.sleep(0.01 * n)
        return n * 2
    
    @profile
    def fast_function(n):
        """Simulates fast function"""
        return n * 2
    
    # Call functions multiple times
    for i in range(5):
        slow_function(i + 1)
        fast_function(i)
    
    # Using Timer context manager
    with Timer("manual_operation"):
        time.sleep(0.05)
    
    # Print report
    monitor.print_report()
