"""
List Panel Widget - Reusable list display component
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional


class ListPanel(ttk.Frame):
    """Reusable list panel with selection support"""
    
    def __init__(
        self,
        parent,
        title: str = "Items",
        on_select: Optional[Callable[[int], None]] = None,
        height: int = 20
    ):
        """
        Initialize list panel
        
        Args:
            parent: Parent widget
            title: Panel title
            on_select: Callback function(index) when item selected
            height: List height in rows
        """
        super().__init__(parent)
        self.on_select = on_select
        self._items = []
        
        # Title
        title_label = ttk.Label(self, text=title, font=('', 10, 'bold'))
        title_label.pack(fill='x', padx=5, pady=5)
        
        # List with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=height
        )
        self.listbox.pack(side='left', fill='both', expand=True)
        self.listbox.bind('<<ListboxSelect>>', self._on_select_change)
        
        scrollbar.config(command=self.listbox.yview)
        
        # Item count label
        self.count_var = tk.StringVar(value="0 items")
        count_label = ttk.Label(self, textvariable=self.count_var, font=('', 9))
        count_label.pack(fill='x', padx=5, pady=5)
    
    def _on_select_change(self, event=None):
        """Handle selection change"""
        selection = self.listbox.curselection()
        if selection and self.on_select:
            self.on_select(selection[0])
    
    def set_items(self, items: List[str]):
        """
        Set list items
        
        Args:
            items: List of item strings to display
        """
        self._items = items
        
        # Clear and repopulate
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
        
        # Update count
        self.count_var.set(f"{len(items)} items")
    
    def clear(self):
        """Clear all items"""
        self.set_items([])
    
    def get_selected_index(self) -> Optional[int]:
        """Get selected item index"""
        selection = self.listbox.curselection()
        return selection[0] if selection else None
    
    def get_selected_item(self) -> Optional[str]:
        """Get selected item text"""
        index = self.get_selected_index()
        return self._items[index] if index is not None else None
    
    def select_index(self, index: int):
        """Select item by index"""
        if 0 <= index < len(self._items):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.see(index)
            self._on_select_change()
