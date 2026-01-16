"""
Tea Tab - Tea database browser tab
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from views.tabs.base_tab import BaseTab
from views.widgets import SearchPanel, ListPanel, DetailPanel


class TeaTab(BaseTab):
    """Tea database browser tab"""
    
    def __init__(self, parent, tea_controller):
        """
        Initialize tea tab
        
        Args:
            parent: Parent widget
            tea_controller: Tea controller instance
        """
        super().__init__(parent, "Tea Database")
        self.controller = tea_controller
        self.current_teas = []
        self.current_tea = None
        
        self.create_ui()
        self.load_data()
    
    def create_ui(self):
        """Create tab UI"""
        # Search panel
        categories = self.controller.get_categories()
        self.search_panel = SearchPanel(
            self.container,
            on_search=self.on_search,
            categories=categories,
            placeholder="Search teas..."
        )
        self.search_panel.pack(fill='x', pady=(0, 10))
        
        # Content area (list + details)
        content = ttk.Frame(self.container)
        content.pack(fill='both', expand=True)
        
        # List panel
        self.list_panel = ListPanel(
            content,
            title="Tea Varieties",
            on_select=self.on_tea_select
        )
        self.list_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Details panel
        self.detail_panel = DetailPanel(content, title="Tea Details")
        self.detail_panel.pack(side='right', fill='both', expand=True)
    
    def load_data(self):
        """Load initial tea data"""
        try:
            self.current_teas = self.controller.get_all_teas()
            self.update_list()
            self.logger.info(f"Loaded {len(self.current_teas)} teas")
        except Exception as e:
            self.show_error(f"Failed to load teas: {e}")
    
    def on_search(self, query: str, category: Optional[str]):
        """
        Handle search
        
        Args:
            query: Search query
            category: Category filter
        """
        try:
            self.logger.debug(f"Searching: query='{query}', category={category}")
            
            if category and category != "All":
                self.current_teas = self.controller.search_teas(
                    query=query,
                    category=category
                )
            elif query:
                self.current_teas = self.controller.search_teas(query=query)
            else:
                self.current_teas = self.controller.get_all_teas()
            
            self.update_list()
            self.logger.info(f"Search returned {len(self.current_teas)} results")
            
        except Exception as e:
            self.show_error(f"Search failed: {e}")
    
    def update_list(self):
        """Update tea list display"""
        items = [tea.get_display_name() for tea in self.current_teas]
        self.list_panel.set_items(items)
    
    def on_tea_select(self, index: int):
        """
        Handle tea selection
        
        Args:
            index: Selected index
        """
        if 0 <= index < len(self.current_teas):
            self.current_tea = self.current_teas[index]
            self.display_tea_details()
    
    def display_tea_details(self):
        """Display selected tea details"""
        if not self.current_tea:
            return
        
        tea = self.current_tea
        
        # Build details dictionary
        details = {
            "Name": tea.name,
            "Category": tea.category,
            "Origin": tea.origin_country,
        }
        
        if tea.origin_region:
            details["Region"] = tea.origin_region
        
        if tea.flavor_profile:
            details["Flavor Profile"] = tea.flavor_profile
        
        if tea.aroma:
            details["Aroma"] = tea.aroma
        
        # Brewing info
        details["Brewing Temperature"] = tea.get_temperature_display()
        
        if tea.steep_time:
            details["Steep Time"] = tea.steep_time
        
        if tea.caffeine_level:
            details["Caffeine"] = tea.caffeine_level
        
        if tea.health_benefits:
            details["Health Benefits"] = tea.health_benefits
        
        if tea.history:
            details["History"] = tea.history
        
        # Display
        self.detail_panel.display(details)
    
    def refresh(self):
        """Refresh tea data"""
        self.load_data()
