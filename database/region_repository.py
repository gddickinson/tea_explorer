"""
Region Repository - Data access for tea growing regions
"""

from typing import List, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin
from models import Region


class RegionRepository(LoggerMixin):
    """Repository for region data access"""
    
    def __init__(self, connection):
        """Initialize repository"""
        self.conn = connection
        self.logger.info("RegionRepository initialized")
    
    def find_all(self) -> List[Region]:
        """Get all regions"""
        cursor = self.conn.execute("""
            SELECT * FROM regions
            ORDER BY country, name
        """)
        
        return [Region.from_db_row(row) for row in cursor.fetchall()]
    
    def find_by_id(self, region_id: int) -> Optional[Region]:
        """Get region by ID"""
        cursor = self.conn.execute("""
            SELECT * FROM regions
            WHERE id = ?
        """, (region_id,))
        
        row = cursor.fetchone()
        return Region.from_db_row(row) if row else None
    
    def find_by_country(self, country: str) -> List[Region]:
        """Get regions by country"""
        cursor = self.conn.execute("""
            SELECT * FROM regions
            WHERE country LIKE ?
            ORDER BY name
        """, (f'%{country}%',))
        
        return [Region.from_db_row(row) for row in cursor.fetchall()]
    
    def find_with_coordinates(self) -> List[Region]:
        """Get regions that have coordinate data"""
        cursor = self.conn.execute("""
            SELECT * FROM regions
            WHERE latitude IS NOT NULL 
              AND longitude IS NOT NULL
            ORDER BY country, name
        """)
        
        return [Region.from_db_row(row) for row in cursor.fetchall()]
    
    def get_countries(self) -> List[str]:
        """Get list of unique countries"""
        cursor = self.conn.execute("""
            SELECT DISTINCT country
            FROM regions
            WHERE country IS NOT NULL AND country != ''
            ORDER BY country
        """)
        
        return [row['country'] for row in cursor.fetchall()]
    
    def count(self) -> int:
        """Get total number of regions"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM regions")
        return cursor.fetchone()[0]
