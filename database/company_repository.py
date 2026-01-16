"""
Company Repository - Data access for tea companies and products
"""

from typing import List, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin, log_method_call
from models import Company, Product


class CompanyRepository(LoggerMixin):
    """Repository for company data access"""
    
    def __init__(self, connection):
        """Initialize repository"""
        self.conn = connection
        self.logger.info("CompanyRepository initialized")
    
    @log_method_call
    def find_all(self) -> List[Company]:
        """Get all companies"""
        cursor = self.conn.execute("""
            SELECT * FROM companies
            ORDER BY company_name
        """)
        
        companies = [Company.from_db_row(row) for row in cursor.fetchall()]
        self.logger.debug(f"Retrieved {len(companies)} companies")
        return companies
    
    def find_by_id(self, company_id: int) -> Optional[Company]:
        """Get company by ID"""
        cursor = self.conn.execute("""
            SELECT * FROM companies
            WHERE company_id = ?
        """, (company_id,))
        
        row = cursor.fetchone()
        return Company.from_db_row(row) if row else None
    
    def find_by_name(self, name: str) -> Optional[Company]:
        """Get company by name"""
        cursor = self.conn.execute("""
            SELECT * FROM companies
            WHERE company_name = ?
        """, (name,))
        
        row = cursor.fetchone()
        return Company.from_db_row(row) if row else None
    
    def find_by_country(self, country: str) -> List[Company]:
        """Get companies by country"""
        cursor = self.conn.execute("""
            SELECT * FROM companies
            WHERE country_of_origin LIKE ?
            ORDER BY company_name
        """, (f'%{country}%',))
        
        return [Company.from_db_row(row) for row in cursor.fetchall()]
    
    def get_countries(self) -> List[str]:
        """Get list of unique countries"""
        cursor = self.conn.execute("""
            SELECT DISTINCT country_of_origin
            FROM companies
            WHERE country_of_origin IS NOT NULL AND country_of_origin != ''
            ORDER BY country_of_origin
        """)
        
        return [row['country_of_origin'] for row in cursor.fetchall()]
    
    def search(self, query: str) -> List[Company]:
        """Search companies"""
        cursor = self.conn.execute("""
            SELECT * FROM companies
            WHERE company_name LIKE ? 
               OR description LIKE ?
            ORDER BY company_name
        """, (f'%{query}%', f'%{query}%'))
        
        return [Company.from_db_row(row) for row in cursor.fetchall()]
    
    def get_products_for_company(self, company_id: int) -> List[Product]:
        """Get all products for a company"""
        cursor = self.conn.execute("""
            SELECT * FROM products
            WHERE company_id = ?
            ORDER BY product_name
        """, (company_id,))
        
        return [Product.from_db_row(row) for row in cursor.fetchall()]
    
    def count(self) -> int:
        """Get total number of companies"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM companies")
        return cursor.fetchone()[0]


class ProductRepository(LoggerMixin):
    """Repository for product data access"""
    
    def __init__(self, connection):
        """Initialize repository"""
        self.conn = connection
        self.logger.info("ProductRepository initialized")
    
    def find_all(self) -> List[Product]:
        """Get all products"""
        cursor = self.conn.execute("""
            SELECT p.*, c.company_name
            FROM products p
            LEFT JOIN companies c ON p.company_id = c.company_id
            ORDER BY p.product_name
        """)
        
        products = []
        for row in cursor.fetchall():
            product = Product.from_db_row(row)
            product.company_name = row['company_name'] if row['company_name'] else ""
            products.append(product)
        
        return products
    
    def find_by_company(self, company_id: int) -> List[Product]:
        """Get products by company"""
        cursor = self.conn.execute("""
            SELECT p.*, c.company_name
            FROM products p
            LEFT JOIN companies c ON p.company_id = c.company_id
            WHERE p.company_id = ?
            ORDER BY p.product_name
        """, (company_id,))
        
        products = []
        for row in cursor.fetchall():
            product = Product.from_db_row(row)
            product.company_name = row['company_name'] if row['company_name'] else ""
            products.append(product)
        
        return products
    
    def find_by_category(self, category: str) -> List[Product]:
        """Get products by tea category"""
        cursor = self.conn.execute("""
            SELECT p.*, c.company_name
            FROM products p
            LEFT JOIN companies c ON p.company_id = c.company_id
            WHERE p.tea_category LIKE ?
            ORDER BY p.product_name
        """, (f'%{category}%',))
        
        products = []
        for row in cursor.fetchall():
            product = Product.from_db_row(row)
            product.company_name = row['company_name'] if row['company_name'] else ""
            products.append(product)
        
        return products
    
    def search(self, query: str) -> List[Product]:
        """Search products"""
        cursor = self.conn.execute("""
            SELECT p.*, c.company_name
            FROM products p
            LEFT JOIN companies c ON p.company_id = c.company_id
            WHERE p.product_name LIKE ? 
               OR p.tea_type LIKE ?
               OR c.company_name LIKE ?
            ORDER BY p.product_name
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        products = []
        for row in cursor.fetchall():
            product = Product.from_db_row(row)
            product.company_name = row['company_name'] if row['company_name'] else ""
            products.append(product)
        
        return products
    
    def count(self) -> int:
        """Get total number of products"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM products")
        return cursor.fetchone()[0]
