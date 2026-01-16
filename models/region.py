"""
Region Model - Tea Growing Regions
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Region:
    """Tea/herb growing region model"""
    
    region_id: Optional[int] = None
    name: str = ""
    country: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_min: Optional[int] = None
    elevation_max: Optional[int] = None
    climate: str = ""
    famous_teas: str = ""
    description: str = ""
    
    @staticmethod
    def from_db_row(row) -> 'Region':
        """Create Region from database row"""
        def get_val(key, default=''):
            try:
                val = row[key]
                return val if val is not None else default
            except (KeyError, IndexError):
                return default
        
        return Region(
            region_id=get_val('id'),
            name=get_val('name'),
            country=get_val('country'),
            latitude=get_val('latitude', None),
            longitude=get_val('longitude', None),
            elevation_min=get_val('elevation_min', None),
            elevation_max=get_val('elevation_max', None),
            climate=get_val('climate'),
            famous_teas=get_val('famous_teas'),
            description=get_val('description')
        )
    
    def get_display_name(self) -> str:
        """Get display name with country"""
        return f"{self.name}, {self.country}"
    
    def get_coordinates(self) -> tuple:
        """Get (latitude, longitude) tuple"""
        return (self.latitude, self.longitude)
    
    def has_coordinates(self) -> bool:
        """Check if has valid coordinates"""
        return self.latitude is not None and self.longitude is not None
    
    def get_elevation_range(self) -> str:
        """Get formatted elevation range"""
        if self.elevation_min and self.elevation_max:
            return f"{self.elevation_min}-{self.elevation_max}m"
        elif self.elevation_min:
            return f"{self.elevation_min}m+"
        return "Not specified"
