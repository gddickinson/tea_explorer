"""
Tea Model - Represents a tea variety from Camellia sinensis
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Tea:
    """Represents a tea variety"""
    
    # Identity
    tea_id: Optional[int] = None
    name: str = ""
    
    # Classification
    category: str = ""  # White, Green, Oolong, Black, Pu-erh, Yellow
    origin: str = ""  # Changed from origin_country to match DB
    
    # Processing
    processing: Optional[str] = None
    oxidation: Optional[str] = None
    
    # Sensory characteristics
    flavor_profile: Optional[str] = None
    aroma: Optional[str] = None
    appearance: Optional[str] = None
    
    # Brewing parameters
    brew_temp_c: Optional[int] = None
    brew_temp_f: Optional[int] = None
    steep_time: Optional[str] = None
    tea_water_ratio: Optional[str] = None
    reinfusions: Optional[int] = None
    
    # Properties
    caffeine_level: Optional[str] = None
    health_benefits: Optional[str] = None
    
    # Additional info
    history: Optional[str] = None
    price_range: Optional[str] = None
    cultivars: Optional[str] = None
    
    def __post_init__(self):
        """Validate tea data after initialization"""
        if self.name:
            self.name = self.name.strip()
        if self.category:
            self.category = self.category.strip()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tea':
        """Create Tea instance from dictionary"""
        return cls(
            tea_id=data.get('tea_id') or data.get('id'),
            name=data.get('name', ''),
            category=data.get('category', ''),
            origin=data.get('origin', ''),
            processing=data.get('processing'),
            oxidation=data.get('oxidation'),
            flavor_profile=data.get('flavor_profile'),
            aroma=data.get('aroma'),
            appearance=data.get('appearance'),
            brew_temp_c=data.get('brew_temp_c'),
            brew_temp_f=data.get('brew_temp_f'),
            steep_time=data.get('steep_time'),
            tea_water_ratio=data.get('tea_water_ratio'),
            reinfusions=data.get('reinfusions'),
            caffeine_level=data.get('caffeine_level'),
            health_benefits=data.get('health_benefits'),
            history=data.get('history'),
            price_range=data.get('price_range'),
            cultivars=data.get('cultivars'),
        )
    
    @classmethod
    def from_db_row(cls, row) -> 'Tea':
        """Create Tea instance from database row"""
        return cls.from_dict(dict(row))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        return {
            'tea_id': self.tea_id,
            'name': self.name,
            'category': self.category,
            'origin': self.origin,
            'processing': self.processing,
            'oxidation': self.oxidation,
            'flavor_profile': self.flavor_profile,
            'aroma': self.aroma,
            'appearance': self.appearance,
            'brew_temp_c': self.brew_temp_c,
            'brew_temp_f': self.brew_temp_f,
            'steep_time': self.steep_time,
            'tea_water_ratio': self.tea_water_ratio,
            'reinfusions': self.reinfusions,
            'caffeine_level': self.caffeine_level,
            'health_benefits': self.health_benefits,
            'history': self.history,
            'price_range': self.price_range,
            'cultivars': self.cultivars,
        }
    
    def get_display_name(self) -> str:
        """Get formatted display name"""
        if self.origin:
            return f"{self.name} ({self.origin})"
        return self.name
    
    def get_temperature_display(self) -> str:
        """Get temperature as formatted string"""
        if self.brew_temp_c and self.brew_temp_f:
            return f"{self.brew_temp_c}°C / {self.brew_temp_f}°F"
        elif self.brew_temp_c:
            return f"{self.brew_temp_c}°C"
        elif self.brew_temp_f:
            return f"{self.brew_temp_f}°F"
        return "Not specified"
