"""
Performance Caching System
Provides caching decorators and utilities for improved performance
"""

from functools import wraps, lru_cache
from typing import Callable, Any, Dict, Optional
import time
import threading
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin


class CacheStats:
    """Track cache performance statistics"""
    
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.lock = threading.Lock()
    
    def record_hit(self):
        with self.lock:
            self.hits += 1
    
    def record_miss(self):
        with self.lock:
            self.misses += 1
    
    def record_eviction(self):
        with self.lock:
            self.evictions += 1
    
    def get_hit_rate(self) -> float:
        """Calculate cache hit rate as percentage"""
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return (self.hits / total) * 100
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all cache statistics"""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_rate': self.get_hit_rate(),
            'total_accesses': self.hits + self.misses
        }
    
    def reset(self):
        """Reset all statistics"""
        with self.lock:
            self.hits = 0
            self.misses = 0
            self.evictions = 0


class TTLCache:
    """Time-To-Live cache with automatic expiration"""
    
    def __init__(self, ttl: int = 300, maxsize: int = 128):
        """
        Initialize TTL cache
        
        Args:
            ttl: Time to live in seconds (default 5 minutes)
            maxsize: Maximum number of cached items
        """
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache: Dict[str, Any] = {}
        self.timestamps: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.stats = CacheStats()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/missing
        """
        with self.lock:
            # Check if key exists
            if key not in self.cache:
                self.stats.record_miss()
                return None
            
            # Check if expired
            if time.time() - self.timestamps[key] > self.ttl:
                del self.cache[key]
                del self.timestamps[key]
                self.stats.record_eviction()
                self.stats.record_miss()
                return None
            
            self.stats.record_hit()
            return self.cache[key]
    
    def set(self, key: str, value: Any):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self.lock:
            # Evict oldest if at capacity
            if len(self.cache) >= self.maxsize and key not in self.cache:
                oldest_key = min(self.timestamps, key=self.timestamps.get)
                del self.cache[oldest_key]
                del self.timestamps[oldest_key]
                self.stats.record_eviction()
            
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def clear(self):
        """Clear all cached items"""
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def size(self) -> int:
        """Get number of cached items"""
        return len(self.cache)


class CacheManager(LoggerMixin):
    """
    Global cache manager for coordinating caches across the application
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.caches: Dict[str, TTLCache] = {}
            self.stats = CacheStats()
            self.initialized = True
            self.logger.info("CacheManager initialized")
    
    def get_cache(self, name: str, ttl: int = 300, maxsize: int = 128) -> TTLCache:
        """
        Get or create a named cache
        
        Args:
            name: Cache name
            ttl: Time to live in seconds
            maxsize: Maximum cache size
            
        Returns:
            TTLCache instance
        """
        if name not in self.caches:
            self.caches[name] = TTLCache(ttl=ttl, maxsize=maxsize)
            self.logger.info(f"Created cache '{name}' (ttl={ttl}s, maxsize={maxsize})")
        return self.caches[name]
    
    def clear_cache(self, name: Optional[str] = None):
        """
        Clear cache(s)
        
        Args:
            name: Cache name to clear, or None to clear all
        """
        if name:
            if name in self.caches:
                self.caches[name].clear()
                self.logger.info(f"Cleared cache '{name}'")
        else:
            for cache in self.caches.values():
                cache.clear()
            self.logger.info("Cleared all caches")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all caches"""
        stats = {}
        for name, cache in self.caches.items():
            stats[name] = {
                'size': cache.size(),
                'stats': cache.stats.get_stats()
            }
        return stats
    
    def log_stats(self):
        """Log cache statistics"""
        stats = self.get_stats()
        for name, cache_stats in stats.items():
            hit_rate = cache_stats['stats']['hit_rate']
            size = cache_stats['size']
            self.logger.info(
                f"Cache '{name}': {size} items, "
                f"hit rate: {hit_rate:.1f}%"
            )


def cached(ttl: int = 300, maxsize: int = 128, cache_name: Optional[str] = None):
    """
    Decorator for caching function results with TTL
    
    Args:
        ttl: Time to live in seconds
        maxsize: Maximum cache size
        cache_name: Name for the cache (defaults to function name)
        
    Usage:
        @cached(ttl=60)
        def expensive_function(arg):
            return slow_computation(arg)
    """
    def decorator(func: Callable) -> Callable:
        name = cache_name or f"{func.__module__}.{func.__name__}"
        manager = CacheManager()
        cache = manager.get_cache(name, ttl=ttl, maxsize=maxsize)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = str(args) + str(sorted(kwargs.items()))
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        # Add cache management methods
        wrapper.cache = cache
        wrapper.clear_cache = cache.clear
        
        return wrapper
    return decorator


# Convenience decorators with preset TTL values

def cached_short(func: Callable) -> Callable:
    """Cache with 1 minute TTL"""
    return cached(ttl=60)(func)


def cached_medium(func: Callable) -> Callable:
    """Cache with 5 minute TTL"""
    return cached(ttl=300)(func)


def cached_long(func: Callable) -> Callable:
    """Cache with 1 hour TTL"""
    return cached(ttl=3600)(func)


def cached_permanent(func: Callable) -> Callable:
    """Cache with 24 hour TTL (effectively permanent for session)"""
    return cached(ttl=86400)(func)


# Global cache manager instance
cache_manager = CacheManager()


if __name__ == '__main__':
    # Demo usage
    import time
    
    @cached(ttl=2, maxsize=5)
    def slow_function(x):
        """Simulates slow function"""
        time.sleep(0.1)
        return x * 2
    
    print("Testing TTL cache:")
    print(f"First call: {slow_function(5)}")  # Slow
    print(f"Second call: {slow_function(5)}")  # Fast (cached)
    
    time.sleep(3)  # Wait for TTL expiration
    
    print(f"After TTL: {slow_function(5)}")  # Slow again
    
    # Show stats
    stats = cache_manager.get_stats()
    print(f"\nCache stats: {stats}")
