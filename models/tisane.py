"""
Tisane Model - Herbal Teas (non-Camellia sinensis)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Tisane:
    """Herbal tea (tisane) model"""
    
    tisane_id: Optional[int] = None
    name: str = ""
    scientific_name: str = ""
    plant_family: str = ""
    common_names: str = ""
    plant_part_used: str = ""
    origin_region: str = ""
    cultivation_countries: str = ""
    tradition: str = ""
    traditional_uses: str = ""
    research_benefits: str = ""
    key_compounds: str = ""
    flavor_profile: str = ""
    aroma: str = ""
    appearance_dry: str = ""
    appearance_brew: str = ""
    brew_temp_c: Optional[int] = None
    brew_temp_f: Optional[int] = None
    steep_time: str = ""
    tea_water_ratio: str = ""
    caffeine_content: str = ""
    caffeine_mg_per_cup: str = ""
    price_range: str = ""
    availability: str = ""
    tcm_properties: str = ""
    ayurvedic_properties: str = ""
    cultural_significance: str = ""
    
    @staticmethod
    def from_db_row(row) -> 'Tisane':
        """Create Tisane from database row"""
        # Helper to safely get value from row
        def get_val(key, default=''):
            try:
                return row[key] if row[key] is not None else default
            except (KeyError, IndexError):
                return default
        
        return Tisane(
            tisane_id=get_val('id'),
            name=get_val('name'),
            scientific_name=get_val('scientific_name'),
            plant_family=get_val('plant_family'),
            common_names=get_val('common_names_json'),
            plant_part_used=get_val('plant_part_used'),
            origin_region=get_val('origin_region'),
            cultivation_countries=get_val('cultivation_countries'),
            tradition=get_val('tradition'),
            traditional_uses=get_val('traditional_uses'),
            research_benefits=get_val('research_benefits'),
            key_compounds=get_val('key_compounds'),
            flavor_profile=get_val('flavor_profile'),
            aroma=get_val('aroma'),
            appearance_dry=get_val('appearance_dry'),
            appearance_brew=get_val('appearance_brew'),
            brew_temp_c=get_val('brew_temp_c'),
            brew_temp_f=get_val('brew_temp_f'),
            steep_time=get_val('steep_time'),
            tea_water_ratio=get_val('tea_water_ratio'),
            caffeine_content=get_val('caffeine_content'),
            caffeine_mg_per_cup=get_val('caffeine_mg_per_cup'),
            price_range=get_val('price_range'),
            availability=get_val('availability'),
            tcm_properties=get_val('tcm_properties_json'),
            ayurvedic_properties=get_val('ayurvedic_properties_json'),
            cultural_significance=get_val('cultural_significance')
        )
    
    def get_temperature_display(self) -> str:
        """Get formatted temperature"""
        if self.brew_temp_c and self.brew_temp_f:
            return f"{self.brew_temp_c}°C / {self.brew_temp_f}°F"
        elif self.brew_temp_c:
            return f"{self.brew_temp_c}°C"
        return "Not specified"
    
    def is_caffeine_free(self) -> bool:
        """Check if caffeine free"""
        if self.caffeine_content:
            return 'caffeine-free' in self.caffeine_content.lower() or \
                   'none' in self.caffeine_content.lower()
        return True
