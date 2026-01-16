"""
Performance Tests - Phase 3
Benchmarks to measure and verify performance improvements
"""

import pytest
import time
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from controllers.tea_controller import TeaController
from controllers.tea_controller_optimized import TeaControllerOptimized
from database import DatabaseConnection, TeaRepository
from performance import monitor, cache_manager


class TestCachingPerformance:
    """Test caching performance improvements"""
    
    @pytest.fixture
    def controller(self):
        """Create optimized controller"""
        db = DatabaseConnection(':memory:')
        # Create test table
        db.conn.execute("""
            CREATE TABLE teas (
                tea_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                origin_country TEXT,
                caffeine_level TEXT
            )
        """)
        # Insert test data
        for i in range(100):
            db.conn.execute("""
                INSERT INTO teas (name, category, origin_country, caffeine_level)
                VALUES (?, ?, ?, ?)
            """, (f"Tea {i}", "Green", "China", "Medium"))
        db.conn.commit()
        
        repo = TeaRepository(db.get_connection())
        return TeaControllerOptimized(repo)
    
    def test_category_caching(self, controller):
        """Test that get_categories() is cached"""
        # First call - should query database
        start = time.time()
        categories1 = controller.get_categories()
        first_time = time.time() - start
        
        # Second call - should use cache
        start = time.time()
        categories2 = controller.get_categories()
        cached_time = time.time() - start
        
        # Verify results are same
        assert categories1 == categories2
        
        # Cached call should be MUCH faster (at least 10x)
        assert cached_time < first_time / 10
        
        # Cached call should be < 1ms
        assert cached_time < 0.001
        
        print(f"\n   First call:  {first_time*1000:.2f}ms")
        print(f"   Cached call: {cached_time*1000:.2f}ms")
        print(f"   Speedup:     {first_time/cached_time:.0f}x")
    
    def test_country_caching(self, controller):
        """Test that get_countries() is cached"""
        start = time.time()
        countries1 = controller.get_countries()
        first_time = time.time() - start
        
        start = time.time()
        countries2 = controller.get_countries()
        cached_time = time.time() - start
        
        assert countries1 == countries2
        assert cached_time < first_time / 10
        
        print(f"\n   First call:  {first_time*1000:.2f}ms")
        print(f"   Cached call: {cached_time*1000:.2f}ms")


class TestSearchPerformance:
    """Test search performance"""
    
    @pytest.fixture
    def controller(self):
        """Create controller with test data"""
        db = DatabaseConnection(':memory:')
        db.conn.execute("""
            CREATE TABLE teas (
                tea_id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                origin_country TEXT,
                flavor_profile TEXT,
                caffeine_level TEXT
            )
        """)
        
        # Create indexes
        db.conn.execute("CREATE INDEX idx_category ON teas(category)")
        db.conn.execute("CREATE INDEX idx_name ON teas(name)")
        
        # Insert test data
        for i in range(1000):
            db.conn.execute("""
                INSERT INTO teas (name, category, origin_country, flavor_profile, caffeine_level)
                VALUES (?, ?, ?, ?, ?)
            """, (f"Tea {i}", "Green", "China", "Grassy", "Medium"))
        db.conn.commit()
        
        repo = TeaRepository(db.get_connection())
        return TeaControllerOptimized(repo)
    
    def test_search_performance(self, controller):
        """Test search completes in reasonable time"""
        iterations = 10
        total_time = 0
        
        for _ in range(iterations):
            start = time.time()
            results = controller.search_teas(query="Tea")
            total_time += time.time() - start
        
        avg_time = (total_time / iterations) * 1000  # Convert to ms
        
        # Should complete in < 50ms on average
        assert avg_time < 50
        
        print(f"\n   Average search time: {avg_time:.2f}ms ({iterations} iterations)")
    
    def test_category_filter_performance(self, controller):
        """Test category filtering performance"""
        iterations = 20
        total_time = 0
        
        for _ in range(iterations):
            start = time.time()
            results = controller.search_teas(category="Green")
            total_time += time.time() - start
        
        avg_time = (total_time / iterations) * 1000
        
        # Should complete in < 30ms with index
        assert avg_time < 30
        
        print(f"\n   Average category filter: {avg_time:.2f}ms ({iterations} iterations)")


class TestProfilingSystem:
    """Test performance profiling"""
    
    def test_profiler_records_metrics(self):
        """Test that profiler records operation metrics"""
        from performance import profile
        
        # Reset monitor
        monitor.reset()
        
        @profile
        def test_function():
            time.sleep(0.01)
            return 42
        
        # Call function multiple times
        for _ in range(5):
            result = test_function()
            assert result == 42
        
        # Check metrics were recorded
        stats = monitor.get_stats()
        operation_name = f"{__name__}.test_function"
        
        assert operation_name in stats['all_operations']
        op_stats = stats['all_operations'][operation_name]
        
        assert op_stats['count'] == 5
        assert op_stats['avg_time'] > 0.01  # At least 10ms
        assert op_stats['avg_time'] < 0.02  # Less than 20ms
    
    def test_timer_context_manager(self):
        """Test Timer context manager"""
        from performance import Timer
        
        with Timer("test_operation", log=False) as timer:
            time.sleep(0.01)
        
        assert timer.elapsed() > 0.01
        assert timer.elapsed() < 0.02


class TestCacheManager:
    """Test cache management"""
    
    def test_cache_manager_stats(self):
        """Test cache manager provides statistics"""
        # Reset caches
        cache_manager.clear_cache()
        
        # Create a cached function
        from performance import cached
        
        @cached(ttl=60, cache_name="test_cache")
        def cached_func(x):
            return x * 2
        
        # Call multiple times
        for i in range(10):
            result = cached_func(i)
            assert result == i * 2
        
        # Get stats
        stats = cache_manager.get_stats()
        
        assert 'test_cache' in stats
        cache_stats = stats['test_cache']
        
        # Should have cached 10 different values
        assert cache_stats['size'] == 10
        assert cache_stats['stats']['total_accesses'] == 10


def benchmark_comparison():
    """
    Comprehensive benchmark comparing Phase 2 vs Phase 3
    Run manually with: pytest benchmarks/test_performance.py::benchmark_comparison -v -s
    """
    print("\n" + "="*70)
    print("PHASE 2 vs PHASE 3 PERFORMANCE COMPARISON")
    print("="*70)
    
    # Setup test database
    db = DatabaseConnection(':memory:')
    db.conn.execute("""
        CREATE TABLE teas (
            tea_id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            origin_country TEXT,
            flavor_profile TEXT,
            caffeine_level TEXT
        )
    """)
    
    # Create index for Phase 3
    db.conn.execute("CREATE INDEX idx_category ON teas(category)")
    
    # Insert test data
    for i in range(1000):
        db.conn.execute("""
            INSERT INTO teas (name, category, origin_country, flavor_profile, caffeine_level)
            VALUES (?, ?, ?, ?, ?)
        """, (f"Tea {i}", ["Green", "Black", "Oolong"][i % 3], "China", "Delicious", "Medium"))
    db.conn.commit()
    
    repo = TeaRepository(db.get_connection())
    
    # Phase 2 controller (no caching)
    controller_p2 = TeaController(repo)
    
    # Phase 3 controller (with caching)
    controller_p3 = TeaControllerOptimized(repo)
    
    # Benchmark tests
    tests = [
        ("Get Categories (1st call)", lambda c: c.get_categories()),
        ("Get Categories (2nd call)", lambda c: c.get_categories()),
        ("Get Countries (1st call)", lambda c: c.get_countries()),
        ("Get Countries (2nd call)", lambda c: c.get_countries()),
        ("Search by category", lambda c: c.search_teas(category="Green")),
        ("Search by query", lambda c: c.search_teas(query="Tea 5")),
    ]
    
    print(f"\n{'Operation':<30} {'Phase 2':>12} {'Phase 3':>12} {'Improvement':>12}")
    print("-" * 70)
    
    for name, test_func in tests:
        # Phase 2 timing
        start = time.time()
        for _ in range(10):
            test_func(controller_p2)
        p2_time = (time.time() - start) / 10 * 1000
        
        # Phase 3 timing
        start = time.time()
        for _ in range(10):
            test_func(controller_p3)
        p3_time = (time.time() - start) / 10 * 1000
        
        improvement = p2_time / p3_time if p3_time > 0 else 0
        
        print(f"{name:<30} {p2_time:>10.2f}ms {p3_time:>10.2f}ms {improvement:>10.1f}x")
    
    print("="*70)
    print("\n✅ Benchmark complete!\n")


if __name__ == '__main__':
    # Run benchmark when executed directly
    benchmark_comparison()
