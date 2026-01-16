"""
Company Controller - Business logic for tea companies and products
"""

from typing import List, Optional
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin, log_method_call
from models import Company, Product
from database import CompanyRepository, ProductRepository
from performance import profile_method


class CompanyController(LoggerMixin):
    """Controller for company and product operations"""
    
    def __init__(self, company_repository: CompanyRepository, product_repository: ProductRepository):
        """Initialize controller"""
        self.company_repo = company_repository
        self.product_repo = product_repository
        self.logger.info("CompanyController initialized")
    
    @profile_method
    @log_method_call
    def get_all_companies(self) -> List[Company]:
        """Get all companies"""
        return self.company_repo.find_all()
    
    @lru_cache(maxsize=64)
    def get_company_by_name(self, name: str) -> Optional[Company]:
        """Get company by name (cached)"""
        return self.company_repo.find_by_name(name)
    
    def get_companies_by_country(self, country: str) -> List[Company]:
        """Get companies by country"""
        return self.company_repo.find_by_country(country)
    
    @lru_cache(maxsize=1)
    @profile_method
    def get_countries(self) -> List[str]:
        """Get list of countries (cached)"""
        return self.company_repo.get_countries()
    
    @profile_method
    def search_companies(self, query: str) -> List[Company]:
        """Search companies"""
        return self.company_repo.search(query)
    
    def get_company_count(self) -> int:
        """Get total company count"""
        return self.company_repo.count()
    
    # Product methods
    @profile_method
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.product_repo.find_all()
    
    def get_products_for_company(self, company_id: int) -> List[Product]:
        """Get products for a company"""
        return self.product_repo.find_by_company(company_id)
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return self.product_repo.find_by_category(category)
    
    @profile_method
    def search_products(self, query: str) -> List[Product]:
        """Search products"""
        return self.product_repo.search(query)
    
    def get_product_count(self) -> int:
        """Get total product count"""
        return self.product_repo.count()
    
    def clear_cache(self):
        """Clear controller caches"""
        self.get_company_by_name.cache_clear()
        self.get_countries.cache_clear()
