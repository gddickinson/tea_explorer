"""
Main Window - Application main window
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger_setup import LoggerMixin


class MainWindow(LoggerMixin):
    """Main application window"""
    
    def __init__(self, root, config, tea_controller=None, blend_controller=None, 
                 journal_controller=None):
        """
        Initialize main window
        
        Args:
            root: Tkinter root
            config: Configuration object
            tea_controller: Tea controller (optional)
            blend_controller: Blend controller (optional)
            journal_controller: Journal controller (optional)
        """
        self.root = root
        self.config = config
        self.tea_controller = tea_controller
        self.blend_controller = blend_controller
        self.journal_controller = journal_controller
        
        # Configure window
        self.root.title("Tea Collection Explorer - Phase 2")
        self.root.geometry(f"{config.ui.window_width}x{config.ui.window_height}")
        
        # Create UI
        self.create_ui()
        
        self.logger.info("Main window initialized")
    
    def create_ui(self):
        """Create user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(
            main_frame,
            text="🍵 Tea Collection Explorer",
            font=(self.config.ui.font_family, 16, 'bold')
        )
        title.grid(row=0, column=0, pady=10)
        
        # Subtitle
        subtitle = ttk.Label(
            main_frame,
            text="Phase 2: Clean Architecture with MVC Pattern",
            font=(self.config.ui.font_family, 10, 'italic')
        )
        subtitle.grid(row=1, column=0, pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Add tabs (if controllers provided)
        if self.tea_controller:
            self.add_tea_tab()
        if self.blend_controller:
            self.add_blend_tab()
        if self.journal_controller:
            self.add_journal_tab()
        
        # Add info tab
        self.add_info_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def add_tea_tab(self):
        """Add tea browser tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🍵 Teas")
        
        label = ttk.Label(
            tab,
            text="Tea Browser (Ready for implementation)",
            font=(self.config.ui.font_family, 12)
        )
        label.pack(pady=20)
    
    def add_blend_tab(self):
        """Add blend browser tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🫖 Blends")
        
        label = ttk.Label(
            tab,
            text="Blend Browser (Ready for implementation)",
            font=(self.config.ui.font_family, 12)
        )
        label.pack(pady=20)
    
    def add_journal_tab(self):
        """Add journal tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📓 Journal")
        
        label = ttk.Label(
            tab,
            text="Tea Journal (Ready for implementation)",
            font=(self.config.ui.font_family, 12)
        )
        label.pack(pady=20)
    
    def add_info_tab(self):
        """Add architecture info tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="ℹ️ Info")
        
        info_text = tk.Text(tab, wrap='word', padx=10, pady=10)
        info_text.pack(fill='both', expand=True)
        
        info_content = """
Phase 2: Architecture Refactoring
==================================

This is a clean, modular architecture demonstrating:

✅ MVC Pattern
   • Models - Domain objects (Tea, Blend, JournalEntry)
   • Views - UI components (this window)
   • Controllers - Business logic

✅ Repository Pattern
   • TeaRepository - Tea data access
   • BlendRepository - Blend data access
   • JournalRepository - Journal data access

✅ Dependency Injection
   • Controllers injected with repositories
   • Views injected with controllers
   • Easy to test and maintain

✅ Type Safety
   • Full type hints throughout
   • Dataclasses with validation

✅ Automatic Logging
   • All operations logged
   • LoggerMixin for easy integration

Project Structure:
------------------
models/          - Domain objects
database/        - Data access layer
controllers/     - Business logic
views/           - UI components
services/        - Business services
utils/           - Utilities
tests/           - Test suite

Next Steps:
-----------
1. Implement widget components
2. Create tab modules
3. Add services layer
4. Write comprehensive tests
5. Migrate from monolithic code

Ready for Phase 3: Performance Optimization! 🚀
        """
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
    
    def set_status(self, message: str):
        """Update status bar"""
        self.status_var.set(message)
        self.logger.debug(f"Status: {message}")
