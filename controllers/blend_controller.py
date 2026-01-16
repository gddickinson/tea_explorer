"""
Blend Controller - Business logic for blend operations
"""

from typing import List, Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call

from models import Blend
from database import BlendRepository


class BlendController(LoggerMixin):
    """Controller for blend operations"""
    
    def __init__(self, blend_repository: BlendRepository):
        """
        Initialize controller
        
        Args:
            blend_repository: Blend repository for data access
        """
        self.repository = blend_repository
        self.logger.info("BlendController initialized")
    
    @log_method_call
    def get_all_blends(self) -> List[Blend]:
        """Get all blends"""
        blends = self.repository.find_all()
        self.logger.debug(f"Retrieved {len(blends)} blends")
        return blends
    
    @log_method_call
    def get_blend_by_name(self, name: str) -> Optional[Blend]:
        """Get specific blend by name"""
        return self.repository.find_by_name(name)
    
    @log_method_call
    def search_blends(
        self,
        query: str = "",
        category: Optional[str] = None
    ) -> List[Blend]:
        """
        Search blends
        
        Args:
            query: Search query
            category: Filter by category
            
        Returns:
            List of matching blends
        """
        self.logger.info(f"Searching blends: query='{query}', category={category}")
        
        if category and category != "All":
            blends = self.repository.find_by_category(category)
        elif query:
            blends = self.repository.search(query)
        else:
            blends = self.repository.find_all()
        
        # Apply additional category filter if needed
        if category and category != "All" and query:
            blends = [b for b in blends if b.category == category]
        
        self.logger.debug(f"Search returned {len(blends)} results")
        return blends
    
    @log_method_call
    def get_categories(self) -> List[str]:
        """Get all blend categories"""
        return self.repository.get_categories()
    
    @log_method_call
    def get_blend_count(self) -> int:
        """Get total number of blends"""
        count = self.repository.count()
        self.logger.debug(f"Total blend count: {count}")
        return count
