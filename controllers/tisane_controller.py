"""
Tisane Controller - Business logic for herbal teas
"""

from typing import List, Optional
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin, log_method_call
from models import Tisane
from database import TisaneRepository
from performance import profile_method


class TisaneController(LoggerMixin):
    """Controller for tisane operations"""
    
    def __init__(self, tisane_repository: TisaneRepository):
        """Initialize controller"""
        self.repository = tisane_repository
        self.logger.info("TisaneController initialized")
    
    @profile_method
    @log_method_call
    def get_all_tisanes(self) -> List[Tisane]:
        """Get all tisanes"""
        return self.repository.find_all()
    
    @lru_cache(maxsize=64)
    def get_tisane_by_name(self, name: str) -> Optional[Tisane]:
        """Get tisane by name (cached)"""
        return self.repository.find_by_name(name)
    
    def get_tisanes_by_family(self, family: str) -> List[Tisane]:
        """Get tisanes by plant family"""
        return self.repository.find_by_plant_family(family)
    
    @profile_method
    def get_caffeine_free_tisanes(self) -> List[Tisane]:
        """Get caffeine-free tisanes"""
        return self.repository.find_caffeine_free()
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_plant_families(self) -> List[str]:
        """Get list of plant families (cached)"""
        return self.repository.get_plant_families()
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_traditions(self) -> List[str]:
        """Get list of traditions (cached)"""
        return self.repository.get_traditions()
    
    @profile_method
    def search_tisanes(self, query: str) -> List[Tisane]:
        """Search tisanes"""
        return self.repository.search(query)
    
    def get_tisane_count(self) -> int:
        """Get total tisane count"""
        return self.repository.count()
    
    def get_safety_info(self, tisane_id: int) -> Optional[dict]:
        """Get safety information for tisane"""
        return self.repository.get_safety_info(tisane_id)
    
    def clear_cache(self):
        """Clear controller caches"""
        self.get_tisane_by_name.cache_clear()
        self.get_plant_families.cache_clear()
        self.get_traditions.cache_clear()
