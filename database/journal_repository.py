"""
Journal Repository - JSON file-based storage for journal entries
"""

from typing import List, Optional
from pathlib import Path
import json

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call

from models import JournalEntry


class JournalRepository(LoggerMixin):
    """Repository for Journal Entry data access (JSON file)"""
    
    def __init__(self, journal_path: Path):
        """
        Initialize repository
        
        Args:
            journal_path: Path to JSON journal file
        """
        self.journal_path = Path(journal_path)
        self._entries: List[JournalEntry] = []
        self._loaded = False
        self.logger.info(f"JournalRepository initialized with path: {self.journal_path}")
    
    @log_method_call
    def _load(self):
        """Load journal from file"""
        if self._loaded:
            return
        
        if self.journal_path.exists():
            try:
                with open(self.journal_path, 'r') as f:
                    data = json.load(f)
                    self._entries = [JournalEntry.from_dict(entry) for entry in data]
                self.logger.info(f"Loaded {len(self._entries)} journal entries")
            except Exception as e:
                self.logger.error(f"Failed to load journal: {e}", exc_info=True)
                self._entries = []
        else:
            self.logger.info("No existing journal file, starting fresh")
            self._entries = []
        
        self._loaded = True
    
    @log_method_call
    def _save(self):
        """Save journal to file"""
        try:
            # Ensure parent directory exists
            self.journal_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert entries to dicts
            data = [entry.to_dict() for entry in self._entries]
            
            # Write to file
            with open(self.journal_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info(f"Saved {len(self._entries)} journal entries")
        except Exception as e:
            self.logger.error(f"Failed to save journal: {e}", exc_info=True)
            raise
    
    @log_method_call
    def find_all(self) -> List[JournalEntry]:
        """Get all journal entries"""
        self._load()
        return self._entries.copy()
    
    @log_method_call
    def find_by_tea_name(self, tea_name: str) -> List[JournalEntry]:
        """
        Get entries for specific tea
        
        Args:
            tea_name: Name of tea
            
        Returns:
            List of matching entries
        """
        self._load()
        entries = [e for e in self._entries if e.tea_name == tea_name]
        self.logger.debug(f"Found {len(entries)} entries for '{tea_name}'")
        return entries
    
    @log_method_call
    def find_by_rating(self, rating: int) -> List[JournalEntry]:
        """Get entries with specific rating"""
        self._load()
        return [e for e in self._entries if e.rating == rating]
    
    @log_method_call
    def find_recent(self, limit: int = 10) -> List[JournalEntry]:
        """
        Get recent journal entries
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of recent entries (most recent first)
        """
        self._load()
        # Sort by date descending (most recent first)
        sorted_entries = sorted(
            self._entries,
            key=lambda e: e.date,
            reverse=True
        )
        recent = sorted_entries[:limit]
        self.logger.debug(f"Retrieved {len(recent)} recent entries")
        return recent
    
    @log_method_call
    def add(self, entry: JournalEntry) -> JournalEntry:
        """
        Add new journal entry
        
        Args:
            entry: Journal entry to add
            
        Returns:
            Added entry with ID assigned
        """
        self._load()
        
        # Assign ID
        if self._entries:
            max_id = max(e.entry_id or 0 for e in self._entries)
            entry.entry_id = max_id + 1
        else:
            entry.entry_id = 1
        
        # Add and save
        self._entries.append(entry)
        self._save()
        
        self.logger.info(f"Added journal entry #{entry.entry_id} for '{entry.tea_name}'")
        return entry
    
    @log_method_call
    def update(self, entry: JournalEntry):
        """Update existing journal entry"""
        self._load()
        
        # Find and replace entry
        for i, e in enumerate(self._entries):
            if e.entry_id == entry.entry_id:
                self._entries[i] = entry
                self._save()
                self.logger.info(f"Updated journal entry #{entry.entry_id}")
                return
        
        self.logger.warning(f"Entry #{entry.entry_id} not found for update")
    
    @log_method_call
    def delete(self, entry_id: int):
        """Delete journal entry"""
        self._load()
        
        original_count = len(self._entries)
        self._entries = [e for e in self._entries if e.entry_id != entry_id]
        
        if len(self._entries) < original_count:
            self._save()
            self.logger.info(f"Deleted journal entry #{entry_id}")
        else:
            self.logger.warning(f"Entry #{entry_id} not found for deletion")
    
    @log_method_call
    def search(self, query: str) -> List[JournalEntry]:
        """Search journal entries"""
        self._load()
        query_lower = query.lower()
        results = [
            e for e in self._entries
            if query_lower in e.tea_name.lower() 
            or query_lower in e.notes.lower()
        ]
        self.logger.debug(f"Search for '{query}' returned {len(results)} results")
        return results
    
    def count(self) -> int:
        """Get total number of entries"""
        self._load()
        return len(self._entries)
