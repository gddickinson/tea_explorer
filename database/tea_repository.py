"""
Tea Repository - Data access for Tea entities
"""

from typing import List, Optional
import sqlite3

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call

from models import Tea


class TeaRepository(LoggerMixin):
    """Repository for Tea data access"""
    
    def __init__(self, connection: sqlite3.Connection):
        """
        Initialize repository
        
        Args:
            connection: SQLite database connection
        """
        self.conn = connection
        self.logger.info("TeaRepository initialized")
    
    @log_method_call
    def find_all(self) -> List[Tea]:
        """
        Get all teas
        
        Returns:
            List of Tea objects
        """
        cursor = self.conn.execute("SELECT * FROM teas ORDER BY name")
        rows = cursor.fetchall()
        teas = [Tea.from_db_row(row) for row in rows]
        self.logger.debug(f"Found {len(teas)} teas")
        return teas
    
    @log_method_call
    def find_by_id(self, tea_id: int) -> Optional[Tea]:
        """
        Get tea by ID
        
        Args:
            tea_id: Tea ID
            
        Returns:
            Tea object or None
        """
        cursor = self.conn.execute(
            "SELECT * FROM teas WHERE tea_id = ?",
            (tea_id,)
        )
        row = cursor.fetchone()
        if row:
            self.logger.debug(f"Found tea with ID {tea_id}")
            return Tea.from_db_row(row)
        self.logger.debug(f"No tea found with ID {tea_id}")
        return None
    
    @log_method_call
    def find_by_name(self, name: str) -> Optional[Tea]:
        """
        Get tea by name
        
        Args:
            name: Tea name
            
        Returns:
            Tea object or None
        """
        cursor = self.conn.execute(
            "SELECT * FROM teas WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        return Tea.from_db_row(row) if row else None
    
    @log_method_call
    def find_by_category(self, category: str) -> List[Tea]:
        """
        Get teas by category
        
        Args:
            category: Tea category (White, Green, Oolong, etc.)
            
        Returns:
            List of Tea objects
        """
        cursor = self.conn.execute(
            "SELECT * FROM teas WHERE category = ? ORDER BY name",
            (category,)
        )
        rows = cursor.fetchall()
        teas = [Tea.from_db_row(row) for row in rows]
        self.logger.debug(f"Found {len(teas)} teas in category '{category}'")
        return teas
    
    @log_method_call
    def find_by_origin(self, country: str, region: Optional[str] = None) -> List[Tea]:
        """
        Get teas by origin
        
        Args:
            country: Origin country
            region: Origin region (optional)
            
        Returns:
            List of Tea objects
        """
        if region:
            cursor = self.conn.execute(
                """SELECT * FROM teas 
                   WHERE origin = ? AND origin_region = ? 
                   ORDER BY name""",
                (country, region)
            )
        else:
            cursor = self.conn.execute(
                "SELECT * FROM teas WHERE origin = ? ORDER BY name",
                (country,)
            )
        rows = cursor.fetchall()
        return [Tea.from_db_row(row) for row in rows]
    
    @log_method_call
    def search(self, query: str) -> List[Tea]:
        """
        Search teas by name or flavor profile
        
        Args:
            query: Search query
            
        Returns:
            List of Tea objects
        """
        search_pattern = f'%{query}%'
        cursor = self.conn.execute(
            """SELECT * FROM teas 
               WHERE name LIKE ? 
                  OR flavor_profile LIKE ? 
                  OR origin_region LIKE ?
               ORDER BY name""",
            (search_pattern, search_pattern, search_pattern)
        )
        rows = cursor.fetchall()
        teas = [Tea.from_db_row(row) for row in rows]
        self.logger.debug(f"Search for '{query}' returned {len(teas)} results")
        return teas
    
    @log_method_call
    def get_categories(self) -> List[str]:
        """
        Get all unique tea categories
        
        Returns:
            List of category names
        """
        cursor = self.conn.execute(
            "SELECT DISTINCT category FROM teas WHERE category IS NOT NULL ORDER BY category"
        )
        categories = [row['category'] for row in cursor.fetchall()]
        self.logger.debug(f"Found {len(categories)} categories")
        return categories
    
    @log_method_call
    def get_countries(self) -> List[str]:
        """
        Get all unique origin countries
        
        Returns:
            List of country names
        """
        cursor = self.conn.execute(
            """SELECT DISTINCT origin FROM teas 
               WHERE origin IS NOT NULL AND origin != ''
               ORDER BY origin"""
        )
        countries = [row['origin'] for row in cursor.fetchall()]
        self.logger.debug(f"Found {len(countries)} countries")
        return countries
    
    def count(self) -> int:
        """Get total number of teas"""
        cursor = self.conn.execute("SELECT COUNT(*) as count FROM teas")
        return cursor.fetchone()['count']
