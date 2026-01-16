"""
Export Service - Data export functionality
"""

import csv
import json
from pathlib import Path
from typing import List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger_setup import LoggerMixin, log_method_call
from models import Tea, Blend, JournalEntry


class ExportService(LoggerMixin):
    """Service for exporting data"""
    
    @log_method_call
    def export_teas_to_csv(self, teas: List[Tea], filename: str):
        """
        Export teas to CSV
        
        Args:
            teas: List of Tea objects
            filename: Output filename
        """
        filepath = Path(filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not teas:
                self.logger.warning("No teas to export")
                return
            
            # Get all fields from first tea
            fieldnames = list(teas[0].to_dict().keys())
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for tea in teas:
                writer.writerow(tea.to_dict())
        
        self.logger.info(f"Exported {len(teas)} teas to {filepath}")
    
    @log_method_call
    def export_teas_to_json(self, teas: List[Tea], filename: str):
        """
        Export teas to JSON
        
        Args:
            teas: List of Tea objects
            filename: Output filename
        """
        filepath = Path(filename)
        
        data = [tea.to_dict() for tea in teas]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Exported {len(teas)} teas to {filepath}")
    
    @log_method_call
    def export_journal_to_csv(self, entries: List[JournalEntry], filename: str):
        """
        Export journal entries to CSV
        
        Args:
            entries: List of JournalEntry objects
            filename: Output filename
        """
        filepath = Path(filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not entries:
                self.logger.warning("No journal entries to export")
                return
            
            fieldnames = list(entries[0].to_dict().keys())
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in entries:
                writer.writerow(entry.to_dict())
        
        self.logger.info(f"Exported {len(entries)} journal entries to {filepath}")
