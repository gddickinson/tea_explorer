"""
Tea Controller - Phase 3 Optimized Version
Business logic for tea operations with caching and profiling
"""

from typing import List, Optional
from functools import lru_cache

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger_setup import LoggerMixin, log_method_call
from models import Tea
from database import TeaRepository
from performance import cached_permanent, profile_method


class TeaControllerOptimized(LoggerMixin):
    """
    Optimized controller for tea operations
    Includes caching and performance profiling
    """
    
    def __init__(self, tea_repository: TeaRepository):
        """
        Initialize controller
        
        Args:
            tea_repository: Tea repository for data access
        """
        self.repository = tea_repository
        self.logger.info("TeaControllerOptimized initialized (Phase 3)")
    
    @profile_method
    @log_method_call
    def get_all_teas(self) -> List[Tea]:
        """
        Get all teas (profiled)
        
        Returns:
            List of all Tea objects
        """
        teas = self.repository.find_all()
        self.logger.debug(f"Retrieved {len(teas)} teas")
        return teas
    
    @profile_method
    def get_tea_by_name(self, name: str) -> Optional[Tea]:
        """Get specific tea by name"""
        return self.repository.find_by_name(name)
    
    @profile_method
    @log_method_call
    def search_teas(
        self,
        query: str = "",
        category: Optional[str] = None,
        country: Optional[str] = None,
        caffeine_level: Optional[str] = None
    ) -> List[Tea]:
        """
        Search teas with multiple filters (profiled)
        
        Args:
            query: Search query for name/flavor
            category: Filter by category
            country: Filter by origin country
            caffeine_level: Filter by caffeine level
            
        Returns:
            List of matching Tea objects
        """
        self.logger.info(
            f"Searching teas: query='{query}', category={category}, "
            f"country={country}, caffeine={caffeine_level}"
        )
        
        # Start with base results
        if category and category != "All":
            teas = self.repository.find_by_category(category)
        elif country and country != "All":
            teas = self.repository.find_by_origin(country)
        elif query:
            teas = self.repository.search(query)
        else:
            teas = self.repository.find_all()
        
        # Apply additional filters
        if category and category != "All" and (country or query):
            teas = [t for t in teas if t.category == category]
        
        if country and country != "All" and (category or query):
            teas = [t for t in teas if t.origin_country == country]
        
        if caffeine_level and caffeine_level != "All":
            teas = [t for t in teas if t.caffeine_level == caffeine_level]
        
        self.logger.debug(f"Search returned {len(teas)} results")
        return teas
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_categories(self) -> List[str]:
        """
        Get all tea categories (cached permanently)
        
        This is cached because categories rarely change.
        First call queries DB, subsequent calls return cached result.
        
        Returns:
            List of category names
        """
        categories = self.repository.get_categories()
        self.logger.debug(f"Retrieved {len(categories)} categories (cached)")
        return categories
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_countries(self) -> List[str]:
        """
        Get all origin countries (cached permanently)
        
        This is cached because countries rarely change.
        
        Returns:
            List of country names
        """
        countries = self.repository.get_countries()
        self.logger.debug(f"Retrieved {len(countries)} countries (cached)")
        return countries
    
    @profile_method
    def get_teas_by_category(self, category: str) -> List[Tea]:
        """
        Get all teas in a category
        
        Args:
            category: Category name
            
        Returns:
            List of Tea objects
        """
        return self.repository.find_by_category(category)
    
    @cached_permanent
    @profile_method
    def get_tea_count(self) -> int:
        """
        Get total number of teas (cached)
        
        Returns:
            Count of teas
        """
        count = self.repository.count()
        self.logger.debug(f"Total tea count: {count}")
        return count
    
    def get_brewing_info(self, tea: Tea) -> dict:
        """
        Get formatted brewing information for a tea
        
        Args:
            tea: Tea object
            
        Returns:
            Dictionary of brewing info
        """
        return {
            'temperature': tea.get_temperature_display(),
            'steep_time': tea.steep_time or 'Not specified',
            'caffeine': tea.caffeine_level or 'Not specified',
        }
    
    def clear_cache(self):
        """Clear all caches (useful after data updates)"""
        self.get_categories.cache_clear()
        self.get_countries.cache_clear()
        self.logger.info("Cleared controller caches")
