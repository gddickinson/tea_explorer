"""
Cultivar Repository - Data access for tea cultivars
"""

from typing import List, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger_setup import LoggerMixin, log_method_call
from models import Cultivar


class CultivarRepository(LoggerMixin):
    """Repository for cultivar data access"""
    
    def __init__(self, connection):
        """
        Initialize repository
        
        Args:
            connection: Database connection
        """
        self.conn = connection
        self.logger.info("CultivarRepository initialized")
    
    @log_method_call
    def find_all(self) -> List[Cultivar]:
        """
        Get all cultivars
        
        Returns:
            List of Cultivar objects
        """
        cursor = self.conn.execute("""
            SELECT * FROM cultivars
            ORDER BY name
        """)
        
        cultivars = [Cultivar.from_db_row(row) for row in cursor.fetchall()]
        self.logger.debug(f"Retrieved {len(cultivars)} cultivars")
        return cultivars
    
    def find_by_id(self, cultivar_id: int) -> Optional[Cultivar]:
        """
        Get cultivar by ID
        
        Args:
            cultivar_id: Cultivar ID
            
        Returns:
            Cultivar object or None
        """
        cursor = self.conn.execute("""
            SELECT * FROM cultivars
            WHERE id = ?
        """, (cultivar_id,))
        
        row = cursor.fetchone()
        return Cultivar.from_db_row(row) if row else None
    
    def find_by_name(self, name: str) -> Optional[Cultivar]:
        """
        Get cultivar by name
        
        Args:
            name: Cultivar name
            
        Returns:
            Cultivar object or None
        """
        cursor = self.conn.execute("""
            SELECT * FROM cultivars
            WHERE name = ?
        """, (name,))
        
        row = cursor.fetchone()
        return Cultivar.from_db_row(row) if row else None
    
    def find_by_species(self, species: str) -> List[Cultivar]:
        """
        Get cultivars by species
        
        Args:
            species: Species name
            
        Returns:
            List of Cultivar objects
        """
        cursor = self.conn.execute("""
            SELECT * FROM cultivars
            WHERE species LIKE ?
            ORDER BY name
        """, (f'%{species}%',))
        
        return [Cultivar.from_db_row(row) for row in cursor.fetchall()]
    
    def find_by_country(self, country: str) -> List[Cultivar]:
        """
        Get cultivars by origin country
        
        Args:
            country: Country name
            
        Returns:
            List of Cultivar objects
        """
        cursor = self.conn.execute("""
            SELECT * FROM cultivars
            WHERE origin_country LIKE ?
            ORDER BY name
        """, (f'%{country}%',))
        
        return [Cultivar.from_db_row(row) for row in cursor.fetchall()]
    
    def get_species_list(self) -> List[str]:
        """
        Get list of unique species
        
        Returns:
            List of species names
        """
        cursor = self.conn.execute("""
            SELECT DISTINCT species
            FROM cultivars
            WHERE species IS NOT NULL AND species != ''
            ORDER BY species
        """)
        
        return [row['species'] for row in cursor.fetchall()]
    
    def get_countries(self) -> List[str]:
        """
        Get list of unique origin countries
        
        Returns:
            List of country names
        """
        cursor = self.conn.execute("""
            SELECT DISTINCT origin_country
            FROM cultivars
            WHERE origin_country IS NOT NULL AND origin_country != ''
            ORDER BY origin_country
        """)
        
        return [row['origin_country'] for row in cursor.fetchall()]
    
    def search(self, query: str) -> List[Cultivar]:
        """
        Search cultivars by name, species, or characteristics
        
        Args:
            query: Search query
            
        Returns:
            List of matching Cultivar objects
        """
        cursor = self.conn.execute("""
            SELECT * FROM cultivars
            WHERE name LIKE ? 
               OR species LIKE ?
               OR characteristics LIKE ?
               OR common_uses LIKE ?
            ORDER BY name
        """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
        
        return [Cultivar.from_db_row(row) for row in cursor.fetchall()]
    
    def count(self) -> int:
        """
        Get total number of cultivars
        
        Returns:
            Count of cultivars
        """
        cursor = self.conn.execute("SELECT COUNT(*) FROM cultivars")
        return cursor.fetchone()[0]
