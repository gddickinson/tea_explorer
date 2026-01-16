"""
Search Panel Widget - Reusable search/filter component
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional


class SearchPanel(ttk.Frame):
    """Reusable search panel with query and category filter"""
    
    def __init__(
        self,
        parent,
        on_search: Callable[[str, Optional[str]], None],
        categories: List[str] = None,
        placeholder: str = "Search..."
    ):
        """
        Initialize search panel
        
        Args:
            parent: Parent widget
            on_search: Callback function(query, category)
            categories: List of categories for filter
            placeholder: Placeholder text for search box
        """
        super().__init__(parent)
        self.on_search = on_search
        
        # Search label
        ttk.Label(self, text="Search:").grid(row=0, column=0, padx=5, sticky='w')
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, sticky='ew')
        self.search_entry.bind('<KeyRelease>', self._on_search_change)
        
        # Category filter (if provided)
        if categories:
            ttk.Label(self, text="Category:").grid(row=0, column=2, padx=5, sticky='w')
            
            self.category_var = tk.StringVar(value="All")
            self.category_combo = ttk.Combobox(
                self,
                textvariable=self.category_var,
                values=["All"] + categories,
                state='readonly',
                width=15
            )
            self.category_combo.grid(row=0, column=3, padx=5, sticky='ew')
            self.category_combo.bind('<<ComboboxSelected>>', self._on_search_change)
        else:
            self.category_var = None
        
        # Clear button
        ttk.Button(self, text="Clear", command=self.clear).grid(
            row=0, column=4, padx=5
        )
        
        # Configure column weights
        self.columnconfigure(1, weight=1)
    
    def _on_search_change(self, event=None):
        """Handle search change"""
        query = self.search_var.get()
        category = self.category_var.get() if self.category_var else None
        self.on_search(query, category)
    
    def clear(self):
        """Clear search"""
        self.search_var.set('')
        if self.category_var:
            self.category_var.set('All')
        self._on_search_change()
    
    def get_query(self) -> str:
        """Get current search query"""
        return self.search_var.get()
    
    def get_category(self) -> Optional[str]:
        """Get selected category"""
        if self.category_var:
            cat = self.category_var.get()
            return None if cat == "All" else cat
        return None
    
    def set_query(self, query: str):
        """Set search query"""
        self.search_var.set(query)
        self._on_search_change()
    
    def focus(self):
        """Focus search entry"""
        self.search_entry.focus()
