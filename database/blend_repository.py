"""
Blend Repository - Data access for Blend entities
"""

from typing import List, Optional
import sqlite3

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'tea_explorer_v3'))
from logger_setup import LoggerMixin, log_method_call

from models import Blend


class BlendRepository(LoggerMixin):
    """Repository for Blend data access"""
    
    def __init__(self, connection: sqlite3.Connection):
        """
        Initialize repository
        
        Args:
            connection: SQLite database connection
        """
        self.conn = connection
        self.logger.info("BlendRepository initialized")
    
    @log_method_call
    def find_all(self) -> List[Blend]:
        """Get all blends"""
        cursor = self.conn.execute("SELECT * FROM blends ORDER BY blend_name")
        rows = cursor.fetchall()
        blends = [Blend.from_db_row(row) for row in rows]
        self.logger.debug(f"Found {len(blends)} blends")
        return blends
    
    @log_method_call
    def find_by_id(self, blend_id: int) -> Optional[Blend]:
        """Get blend by ID"""
        cursor = self.conn.execute(
            "SELECT * FROM blends WHERE blend_id = ?",
            (blend_id,)
        )
        row = cursor.fetchone()
        return Blend.from_db_row(row) if row else None
    
    @log_method_call
    def find_by_name(self, name: str) -> Optional[Blend]:
        """Get blend by name"""
        cursor = self.conn.execute(
            "SELECT * FROM blends WHERE blend_name = ?",
            (name,)
        )
        row = cursor.fetchone()
        return Blend.from_db_row(row) if row else None
    
    @log_method_call
    def find_by_category(self, category: str) -> List[Blend]:
        """Get blends by category"""
        cursor = self.conn.execute(
            "SELECT * FROM blends WHERE category = ? ORDER BY blend_name",
            (category,)
        )
        rows = cursor.fetchall()
        blends = [Blend.from_db_row(row) for row in rows]
        self.logger.debug(f"Found {len(blends)} blends in category '{category}'")
        return blends
    
    @log_method_call
    def search(self, query: str) -> List[Blend]:
        """Search blends"""
        search_pattern = f'%{query}%'
        cursor = self.conn.execute(
            """SELECT * FROM blends 
               WHERE blend_name LIKE ? 
                  OR ingredients LIKE ?
                  OR flavor_profile LIKE ?
               ORDER BY blend_name""",
            (search_pattern, search_pattern, search_pattern)
        )
        rows = cursor.fetchall()
        blends = [Blend.from_db_row(row) for row in rows]
        self.logger.debug(f"Search for '{query}' returned {len(blends)} results")
        return blends
    
    @log_method_call
    def get_categories(self) -> List[str]:
        """Get all unique blend categories"""
        cursor = self.conn.execute(
            "SELECT DISTINCT category FROM blends WHERE category IS NOT NULL ORDER BY category"
        )
        return [row['category'] for row in cursor.fetchall()]
    
    def count(self) -> int:
        """Get total number of blends"""
        cursor = self.conn.execute("SELECT COUNT(*) as count FROM blends")
        return cursor.fetchone()['count']
