"""
Blend Model - Represents a tea blend or flavored tea
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Blend:
    """Represents a tea blend"""
    
    # Identity
    blend_id: Optional[int] = None
    blend_name: str = ""
    
    # Classification
    category: str = ""
    base_tea: Optional[str] = None
    ingredients: str = ""
    
    # Sensory
    flavor_profile: Optional[str] = None
    aroma: Optional[str] = None
    appearance: Optional[str] = None
    
    # Brewing
    brew_temp_c: Optional[int] = None
    brew_temp_f: Optional[int] = None
    steep_time: Optional[str] = None
    
    # Properties
    caffeine_level: Optional[str] = None
    health_benefits: Optional[str] = None
    
    # Additional info
    origin_region: Optional[str] = None
    history: Optional[str] = None
    price_range: Optional[str] = None
    popular_brands: Optional[str] = None
    description: Optional[str] = None
    serving_suggestions: Optional[str] = None
    
    def __post_init__(self):
        """Validate blend data"""
        if self.blend_name:
            self.blend_name = self.blend_name.strip()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Blend':
        """Create from dictionary"""
        return cls(
            blend_id=data.get('blend_id'),
            blend_name=data.get('blend_name', ''),
            category=data.get('category', ''),
            base_tea=data.get('base_tea'),
            ingredients=data.get('ingredients', ''),
            flavor_profile=data.get('flavor_profile'),
            aroma=data.get('aroma'),
            appearance=data.get('appearance'),
            brew_temp_c=data.get('brew_temp_c'),
            brew_temp_f=data.get('brew_temp_f'),
            steep_time=data.get('steep_time'),
            caffeine_level=data.get('caffeine_level'),
            health_benefits=data.get('health_benefits'),
            origin_region=data.get('origin_region'),
            history=data.get('history'),
            price_range=data.get('price_range'),
            popular_brands=data.get('popular_brands'),
            description=data.get('description'),
            serving_suggestions=data.get('serving_suggestions'),
        )
    
    @classmethod
    def from_db_row(cls, row) -> 'Blend':
        """Create from database row"""
        return cls.from_dict(dict(row))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'blend_id': self.blend_id,
            'blend_name': self.blend_name,
            'category': self.category,
            'base_tea': self.base_tea,
            'ingredients': self.ingredients,
            'flavor_profile': self.flavor_profile,
            'aroma': self.aroma,
            'appearance': self.appearance,
            'brew_temp_c': self.brew_temp_c,
            'brew_temp_f': self.brew_temp_f,
            'steep_time': self.steep_time,
            'caffeine_level': self.caffeine_level,
            'health_benefits': self.health_benefits,
            'origin_region': self.origin_region,
            'history': self.history,
            'price_range': self.price_range,
            'popular_brands': self.popular_brands,
            'description': self.description,
            'serving_suggestions': self.serving_suggestions,
        }
    
    def get_display_name(self) -> str:
        """Get formatted display name"""
        return self.blend_name
    
    def get_temperature_display(self) -> str:
        """Get temperature as formatted string"""
        if self.brew_temp_c and self.brew_temp_f:
            return f"{self.brew_temp_c}°C / {self.brew_temp_f}°F"
        elif self.brew_temp_c:
            return f"{self.brew_temp_c}°C"
        elif self.brew_temp_f:
            return f"{self.brew_temp_f}°F"
        return "Not specified"
