"""
Tea Controller - Business logic for tea operations
"""

from typing import List, Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call

from models import Tea
from database import TeaRepository


class TeaController(LoggerMixin):
    """Controller for tea operations"""
    
    def __init__(self, tea_repository: TeaRepository):
        """
        Initialize controller
        
        Args:
            tea_repository: Tea repository for data access
        """
        self.repository = tea_repository
        self.logger.info("TeaController initialized")
    
    @log_method_call
    def get_all_teas(self) -> List[Tea]:
        """
        Get all teas
        
        Returns:
            List of all Tea objects
        """
        teas = self.repository.find_all()
        self.logger.debug(f"Retrieved {len(teas)} teas")
        return teas
    
    @log_method_call
    def get_tea_by_name(self, name: str) -> Optional[Tea]:
        """
        Get specific tea by name
        
        Args:
            name: Tea name
            
        Returns:
            Tea object or None
        """
        return self.repository.find_by_name(name)
    
    @log_method_call
    def search_teas(
        self,
        query: str = "",
        category: Optional[str] = None,
        country: Optional[str] = None,
        caffeine_level: Optional[str] = None
    ) -> List[Tea]:
        """
        Search teas with multiple filters
        
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
    
    @log_method_call
    def get_categories(self) -> List[str]:
        """
        Get all tea categories
        
        Returns:
            List of category names
        """
        return self.repository.get_categories()
    
    @log_method_call
    def get_countries(self) -> List[str]:
        """
        Get all origin countries
        
        Returns:
            List of country names
        """
        return self.repository.get_countries()
    
    @log_method_call
    def get_teas_by_category(self, category: str) -> List[Tea]:
        """
        Get all teas in a category
        
        Args:
            category: Category name
            
        Returns:
            List of Tea objects
        """
        return self.repository.find_by_category(category)
    
    @log_method_call
    def get_tea_count(self) -> int:
        """
        Get total number of teas
        
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
