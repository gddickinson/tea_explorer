"""
Detail Panel Widget - Reusable detail display component
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class DetailPanel(ttk.Frame):
    """Reusable detail display panel"""
    
    def __init__(self, parent, title: str = "Details"):
        """
        Initialize detail panel
        
        Args:
            parent: Parent widget
            title: Panel title
        """
        super().__init__(parent)
        
        # Title
        title_label = ttk.Label(self, text=title, font=('', 10, 'bold'))
        title_label.pack(fill='x', padx=5, pady=5)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.text = tk.Text(
            text_frame,
            wrap='word',
            yscrollcommand=scrollbar.set,
            state='disabled'
        )
        self.text.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=self.text.yview)
    
    def display(self, details: Dict[str, Any]):
        """
        Display details
        
        Args:
            details: Dictionary of field: value pairs
        """
        self.text.config(state='normal')
        self.text.delete('1.0', tk.END)
        
        for field, value in details.items():
            # Field name (bold)
            self.text.insert(tk.END, f"{field}:\n", 'field')
            # Value
            self.text.insert(tk.END, f"{value}\n\n")
        
        # Configure tags
        self.text.tag_config('field', font=('', 10, 'bold'))
        
        self.text.config(state='disabled')
    
    def display_text(self, text: str):
        """
        Display plain text
        
        Args:
            text: Text to display
        """
        self.text.config(state='normal')
        self.text.delete('1.0', tk.END)
        self.text.insert('1.0', text)
        self.text.config(state='disabled')
    
    def clear(self):
        """Clear display"""
        self.text.config(state='normal')
        self.text.delete('1.0', tk.END)
        self.text.config(state='disabled')
