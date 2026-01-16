"""
Tisane Repository - Data access for herbal teas
Note: Uses separate tisane_collection.db database
"""

from typing import List, Optional
from pathlib import Path
import sys
import sqlite3

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin, log_method_call
from models import Tisane


class TisaneRepository(LoggerMixin):
    """Repository for tisane data access"""
    
    def __init__(self, db_path: str = "tisane_collection.db"):
        """
        Initialize repository with separate database
        
        Args:
            db_path: Path to tisane database
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.logger.info(f"TisaneRepository initialized with {db_path}")
    
    @log_method_call
    def find_all(self) -> List[Tisane]:
        """Get all tisanes"""
        cursor = self.conn.execute("""
            SELECT * FROM tisanes
            ORDER BY name
        """)
        
        tisanes = [Tisane.from_db_row(row) for row in cursor.fetchall()]
        self.logger.debug(f"Retrieved {len(tisanes)} tisanes")
        return tisanes
    
    def find_by_id(self, tisane_id: int) -> Optional[Tisane]:
        """Get tisane by ID"""
        cursor = self.conn.execute("""
            SELECT * FROM tisanes
            WHERE id = ?
        """, (tisane_id,))
        
        row = cursor.fetchone()
        return Tisane.from_db_row(row) if row else None
    
    def find_by_name(self, name: str) -> Optional[Tisane]:
        """Get tisane by name"""
        cursor = self.conn.execute("""
            SELECT * FROM tisanes
            WHERE name = ?
        """, (name,))
        
        row = cursor.fetchone()
        return Tisane.from_db_row(row) if row else None
    
    def find_by_plant_family(self, family: str) -> List[Tisane]:
        """Get tisanes by plant family"""
        cursor = self.conn.execute("""
            SELECT * FROM tisanes
            WHERE plant_family LIKE ?
            ORDER BY name
        """, (f'%{family}%',))
        
        return [Tisane.from_db_row(row) for row in cursor.fetchall()]
    
    def find_caffeine_free(self) -> List[Tisane]:
        """Get caffeine-free tisanes"""
        cursor = self.conn.execute("""
            SELECT * FROM tisanes
            WHERE caffeine_content LIKE '%caffeine-free%'
               OR caffeine_content LIKE '%none%'
            ORDER BY name
        """)
        
        return [Tisane.from_db_row(row) for row in cursor.fetchall()]
    
    def get_plant_families(self) -> List[str]:
        """Get list of unique plant families"""
        cursor = self.conn.execute("""
            SELECT DISTINCT plant_family
            FROM tisanes
            WHERE plant_family IS NOT NULL AND plant_family != ''
            ORDER BY plant_family
        """)
        
        return [row['plant_family'] for row in cursor.fetchall()]
    
    def get_traditions(self) -> List[str]:
        """Get list of unique traditions"""
        cursor = self.conn.execute("""
            SELECT DISTINCT tradition
            FROM tisanes
            WHERE tradition IS NOT NULL AND tradition != ''
            ORDER BY tradition
        """)
        
        return [row['tradition'] for row in cursor.fetchall()]
    
    def search(self, query: str) -> List[Tisane]:
        """Search tisanes"""
        cursor = self.conn.execute("""
            SELECT * FROM tisanes
            WHERE name LIKE ? 
               OR scientific_name LIKE ?
               OR traditional_uses LIKE ?
               OR flavor_profile LIKE ?
            ORDER BY name
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        return [Tisane.from_db_row(row) for row in cursor.fetchall()]
    
    def count(self) -> int:
        """Get total number of tisanes"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM tisanes")
        return cursor.fetchone()[0]
    
    def get_safety_info(self, tisane_id: int) -> Optional[dict]:
        """
        Get safety information for a tisane
        
        Args:
            tisane_id: Tisane ID
            
        Returns:
            Dictionary of safety info or None
        """
        try:
            cursor = self.conn.execute("""
                SELECT * FROM safety_info
                WHERE tisane_id = ?
            """, (tisane_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
        except:
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
