"""
Journal Controller - Business logic for journal operations
"""

from typing import List
from datetime import datetime

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call

from models import JournalEntry
from database import JournalRepository


class JournalController(LoggerMixin):
    """Controller for journal operations"""
    
    def __init__(self, journal_repository: JournalRepository):
        """
        Initialize controller
        
        Args:
            journal_repository: Journal repository for data access
        """
        self.repository = journal_repository
        self.logger.info("JournalController initialized")
    
    @log_method_call
    def get_all_entries(self) -> List[JournalEntry]:
        """Get all journal entries"""
        entries = self.repository.find_all()
        self.logger.debug(f"Retrieved {len(entries)} journal entries")
        return entries
    
    @log_method_call
    def get_recent_entries(self, limit: int = 10) -> List[JournalEntry]:
        """
        Get recent journal entries
        
        Args:
            limit: Maximum number of entries
            
        Returns:
            List of recent entries
        """
        return self.repository.find_recent(limit)
    
    @log_method_call
    def get_entries_for_tea(self, tea_name: str) -> List[JournalEntry]:
        """
        Get all entries for a specific tea
        
        Args:
            tea_name: Name of tea
            
        Returns:
            List of entries
        """
        return self.repository.find_by_tea_name(tea_name)
    
    @log_method_call
    def add_entry(
        self,
        tea_name: str,
        rating: int,
        brewing: str = "",
        notes: str = ""
    ) -> JournalEntry:
        """
        Add new journal entry
        
        Args:
            tea_name: Name of tea
            rating: Rating (1-5)
            brewing: Brewing details
            notes: Tasting notes
            
        Returns:
            Created journal entry
        """
        # Create entry with current timestamp
        entry = JournalEntry(
            tea_name=tea_name,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            rating=rating,
            brewing=brewing,
            notes=notes
        )
        
        # Add to repository
        entry = self.repository.add(entry)
        self.logger.info(f"Created journal entry for '{tea_name}' with rating {rating}")
        return entry
    
    @log_method_call
    def search_entries(self, query: str) -> List[JournalEntry]:
        """
        Search journal entries
        
        Args:
            query: Search query
            
        Returns:
            List of matching entries
        """
        results = self.repository.search(query)
        self.logger.debug(f"Search for '{query}' returned {len(results)} entries")
        return results
    
    @log_method_call
    def get_entry_count(self) -> int:
        """Get total number of entries"""
        count = self.repository.count()
        self.logger.debug(f"Total entry count: {count}")
        return count
    
    @log_method_call
    def delete_entry(self, entry_id: int):
        """
        Delete journal entry
        
        Args:
            entry_id: Entry ID to delete
        """
        self.repository.delete(entry_id)
        self.logger.info(f"Deleted journal entry #{entry_id}")
    
    def get_average_rating_for_tea(self, tea_name: str) -> float:
        """
        Calculate average rating for a tea
        
        Args:
            tea_name: Name of tea
            
        Returns:
            Average rating or 0.0 if no entries
        """
        entries = self.repository.find_by_tea_name(tea_name)
        if not entries:
            return 0.0
        
        avg = sum(e.rating for e in entries) / len(entries)
        self.logger.debug(f"Average rating for '{tea_name}': {avg:.1f}")
        return avg
    
    def get_top_rated_teas(self, limit: int = 5) -> List[tuple]:
        """
        Get top rated teas
        
        Args:
            limit: Number of teas to return
            
        Returns:
            List of (tea_name, avg_rating, entry_count) tuples
        """
        entries = self.repository.find_all()
        
        # Group by tea name
        tea_ratings = {}
        for entry in entries:
            if entry.tea_name not in tea_ratings:
                tea_ratings[entry.tea_name] = []
            tea_ratings[entry.tea_name].append(entry.rating)
        
        # Calculate averages
        tea_averages = [
            (name, sum(ratings) / len(ratings), len(ratings))
            for name, ratings in tea_ratings.items()
        ]
        
        # Sort by average rating
        tea_averages.sort(key=lambda x: x[1], reverse=True)
        
        return tea_averages[:limit]
