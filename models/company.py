"""
Company and Product Models - Tea Brands and Their Products
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Company:
    """Tea company/brand model"""
    
    company_id: Optional[int] = None
    company_name: str = ""
    parent_company: str = ""
    founded_year: Optional[int] = None
    headquarters_city: str = ""
    country_of_origin: str = ""
    website: str = ""
    certifications: str = ""
    market_segment: str = ""
    description: str = ""
    
    @staticmethod
    def from_db_row(row) -> 'Company':
        """Create Company from database row"""
        def get_val(key, default=''):
            try:
                val = row[key]
                return val if val is not None else default
            except (KeyError, IndexError):
                return default
        
        return Company(
            company_id=get_val('company_id'),
            company_name=get_val('company_name'),
            parent_company=get_val('parent_company'),
            founded_year=get_val('founded_year'),
            headquarters_city=get_val('headquarters_city'),
            country_of_origin=get_val('country_of_origin'),
            website=get_val('website'),
            certifications=get_val('certifications'),
            market_segment=get_val('market_segment'),
            description=get_val('description')
        )
    
    def get_display_name(self) -> str:
        """Get display name with country"""
        if self.country_of_origin:
            return f"{self.company_name} ({self.country_of_origin})"
        return self.company_name


@dataclass
class Product:
    """Tea product model"""
    
    product_id: Optional[int] = None
    company_id: Optional[int] = None
    product_name: str = ""
    tea_type: str = ""
    tea_category: str = ""
    bag_type: str = ""
    format: str = ""
    quantity: str = ""
    price: str = ""
    price_currency: str = ""
    countries_available: str = ""
    organic: str = ""
    fair_trade: str = ""
    special_features: str = ""
    
    # For display
    company_name: str = ""
    
    @staticmethod
    def from_db_row(row) -> 'Product':
        """Create Product from database row"""
        def get_val(key, default=''):
            try:
                val = row[key]
                return val if val is not None else default
            except (KeyError, IndexError):
                return default
        
        return Product(
            product_id=get_val('product_id'),
            company_id=get_val('company_id'),
            product_name=get_val('product_name'),
            tea_type=get_val('tea_type'),
            tea_category=get_val('tea_category'),
            bag_type=get_val('bag_type'),
            format=get_val('format'),
            quantity=get_val('quantity'),
            price=get_val('price'),
            price_currency=get_val('price_currency'),
            countries_available=get_val('countries_available'),
            organic=get_val('organic'),
            fair_trade=get_val('fair_trade'),
            special_features=get_val('special_features')
        )
    
    def get_display_name(self) -> str:
        """Get display name"""
        if self.company_name:
            return f"{self.product_name} by {self.company_name}"
        return self.product_name
