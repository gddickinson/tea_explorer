"""
Cultivar Model - Tea Plant Varieties
Represents tea plant cultivars (Camellia sinensis varieties)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cultivar:
    """Tea plant cultivar model"""
    
    cultivar_id: Optional[int] = None
    name: str = ""
    species: str = ""
    origin_country: str = ""
    leaf_size: str = ""
    characteristics: str = ""
    common_uses: str = ""
    notes: str = ""
    
    @staticmethod
    def from_db_row(row) -> 'Cultivar':
        """
        Create Cultivar from database row
        
        Args:
            row: Database row (dict-like)
            
        Returns:
            Cultivar instance
        """
        # Helper to safely get value
        def get_val(key, default=''):
            try:
                val = row[key]
                return val if val is not None else default
            except (KeyError, IndexError):
                return default
        
        return Cultivar(
            cultivar_id=get_val('id'),
            name=get_val('name'),
            species=get_val('species'),
            origin_country=get_val('origin_country'),
            leaf_size=get_val('leaf_size'),
            characteristics=get_val('characteristics'),
            common_uses=get_val('common_uses'),
            notes=get_val('notes')
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'cultivar_id': self.cultivar_id,
            'name': self.name,
            'species': self.species,
            'origin_country': self.origin_country,
            'leaf_size': self.leaf_size,
            'characteristics': self.characteristics,
            'common_uses': self.common_uses,
            'notes': self.notes
        }
    
    def get_display_name(self) -> str:
        """Get display name with origin"""
        if self.origin_country:
            return f"{self.name} ({self.origin_country})"
        return self.name
