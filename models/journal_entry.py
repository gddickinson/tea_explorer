"""
Journal Entry Model - Represents a tea tasting note
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class JournalEntry:
    """Represents a tea tasting journal entry"""
    
    entry_id: Optional[int] = None
    tea_name: str = ""
    date: str = ""
    rating: int = 0  # 1-5 stars
    brewing: str = ""
    notes: str = ""
    
    def __post_init__(self):
        """Validate after initialization"""
        if self.tea_name:
            self.tea_name = self.tea_name.strip()
        # Ensure rating is 1-5
        if self.rating < 1:
            self.rating = 1
        elif self.rating > 5:
            self.rating = 5
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JournalEntry':
        """Create from dictionary"""
        return cls(
            entry_id=data.get('entry_id'),
            tea_name=data.get('tea_name', ''),
            date=data.get('date', ''),
            rating=data.get('rating', 0),
            brewing=data.get('brewing', ''),
            notes=data.get('notes', ''),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'entry_id': self.entry_id,
            'tea_name': self.tea_name,
            'date': self.date,
            'rating': self.rating,
            'brewing': self.brewing,
            'notes': self.notes,
        }
    
    def get_star_display(self) -> str:
        """Get star rating as string"""
        return '★' * self.rating + '☆' * (5 - self.rating)
