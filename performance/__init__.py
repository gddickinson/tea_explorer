"""
Performance Module - Phase 3
Caching, profiling, and optimization utilities
"""

from .cache import (
    cached,
    cached_short,
    cached_medium,
    cached_long,
    cached_permanent,
    CacheManager,
    cache_manager
)

from .profiler import (
    profile,
    profile_method,
    Timer,
    PerformanceMonitor,
    monitor
)

__all__ = [
    # Caching
    'cached',
    'cached_short',
    'cached_medium',
    'cached_long',
    'cached_permanent',
    'CacheManager',
    'cache_manager',
    
    # Profiling
    'profile',
    'profile_method',
    'Timer',
    'PerformanceMonitor',
    'monitor',
]
