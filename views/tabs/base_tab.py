"""
Base Tab - Base class for tab implementations
"""

import tkinter as tk
from tkinter import ttk

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from logger_setup import LoggerMixin


class BaseTab(ttk.Frame, LoggerMixin):
    """Base class for tab implementations"""
    
    def __init__(self, parent, title: str = "Tab"):
        """
        Initialize base tab
        
        Args:
            parent: Parent widget
            title: Tab title
        """
        ttk.Frame.__init__(self, parent)
        self.title = title
        
        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.logger.info(f"Initialized {self.__class__.__name__}")
    
    def create_header(self, text: str):
        """
        Create header section
        
        Args:
            text: Header text
        """
        header = ttk.Label(
            self.container,
            text=text,
            font=('', 12, 'bold')
        )
        header.pack(fill='x', pady=(0, 10))
        return header
    
    def create_section(self, title: str) -> ttk.LabelFrame:
        """
        Create labeled section
        
        Args:
            title: Section title
            
        Returns:
            LabelFrame widget
        """
        section = ttk.LabelFrame(self.container, text=title, padding=10)
        section.pack(fill='both', expand=True, pady=5)
        return section
    
    def show_message(self, message: str):
        """
        Show message to user
        
        Args:
            message: Message text
        """
        from tkinter import messagebox
        messagebox.showinfo(self.title, message)
    
    def show_error(self, error: str):
        """
        Show error to user
        
        Args:
            error: Error text
        """
        from tkinter import messagebox
        messagebox.showerror(self.title, error)
        self.logger.error(error)
    
    def refresh(self):
        """Refresh tab data (override in subclass)"""
        pass
