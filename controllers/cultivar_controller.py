"""
Cultivar Controller - Business logic for tea cultivars
"""

from typing import List, Optional
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin, log_method_call
from models import Cultivar
from database import CultivarRepository
from performance import profile_method


class CultivarController(LoggerMixin):
    """Controller for cultivar operations"""
    
    def __init__(self, cultivar_repository: CultivarRepository):
        """
        Initialize controller
        
        Args:
            cultivar_repository: Cultivar repository
        """
        self.repository = cultivar_repository
        self.logger.info("CultivarController initialized")
    
    @profile_method
    @log_method_call
    def get_all_cultivars(self) -> List[Cultivar]:
        """Get all cultivars"""
        return self.repository.find_all()
    
    @lru_cache(maxsize=128)
    def get_cultivar_by_name(self, name: str) -> Optional[Cultivar]:
        """Get cultivar by name (cached)"""
        return self.repository.find_by_name(name)
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_species_list(self) -> List[str]:
        """Get list of species (cached)"""
        return self.repository.get_species_list()
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_countries(self) -> List[str]:
        """Get list of countries (cached)"""
        return self.repository.get_countries()
    
    def get_cultivars_by_species(self, species: str) -> List[Cultivar]:
        """Get cultivars by species"""
        return self.repository.find_by_species(species)
    
    def get_cultivars_by_country(self, country: str) -> List[Cultivar]:
        """Get cultivars by country"""
        return self.repository.find_by_country(country)
    
    @profile_method
    def search_cultivars(self, query: str) -> List[Cultivar]:
        """Search cultivars"""
        return self.repository.search(query)
    
    def get_cultivar_count(self) -> int:
        """Get total cultivar count"""
        return self.repository.count()
    
    def clear_cache(self):
        """Clear controller caches"""
        self.get_cultivar_by_name.cache_clear()
        self.get_species_list.cache_clear()
        self.get_countries.cache_clear()
