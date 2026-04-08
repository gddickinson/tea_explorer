"""
Tea Collection Explorer - Main Application Entry Point
Demonstrates Phase 2 Architecture with Dependency Injection
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys
import sqlite3

# Add Phase 1 modules to path
phase1_path = Path(__file__).parent.parent / 'tea_explorer_v3'
sys.path.insert(0, str(phase1_path))

from config import get_config
from logger_setup import LoggerSetup, get_logger

# Import Phase 2 modules
from database import DatabaseConnection, TeaRepository, BlendRepository, JournalRepository
from controllers import TeaController, BlendController, JournalController
from models import Tea, Blend, JournalEntry


class TeaExplorerApp:
    """Main Application with MVC Architecture"""
    
    def __init__(self, root):
        """
        Initialize application with dependency injection
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.logger = get_logger(__name__)
        
        # Get configuration
        self.config = get_config()
        
        # Initialize window
        self.root.title("Tea Collection Explorer - Phase 2 Architecture")
        self.root.geometry(f"{self.config.ui.window_width}x{self.config.ui.window_height}")
        
        # Create database connections
        self.logger.info("Initializing database connections")
        self.tea_db = DatabaseConnection(self.config.database.tea_db_path)
        
        # Create repositories
        self.logger.info("Creating repositories")
        self.tea_repo = TeaRepository(self.tea_db.get_connection())
        self.blend_repo = BlendRepository(self.tea_db.get_connection())
        self.journal_repo = JournalRepository(self.config.journal_path)
        
        # Create controllers
        self.logger.info("Creating controllers")
        self.tea_controller = TeaController(self.tea_repo)
        self.blend_controller = BlendController(self.blend_repo)
        self.journal_controller = JournalController(self.journal_repo)
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.load_data()
        
        self.logger.info("Application initialized successfully")
    
    def create_ui(self):
        """Create user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Tea Collection Explorer",
            font=(self.config.ui.font_family, self.config.ui.title_font_size, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Architecture info
        arch_label = ttk.Label(
            main_frame,
            text="Phase 2: MVC Architecture with Dependency Injection",
            font=(self.config.ui.font_family, self.config.ui.font_size, 'italic')
        )
        arch_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Create tabs
        self.create_tea_browser_tab()
        self.create_blend_browser_tab()
        self.create_journal_tab()
        self.create_stats_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def create_tea_browser_tab(self):
        """Create tea browser tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🍵 Tea Database")
        
        # Search frame
        search_frame = ttk.Frame(tab)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.tea_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.tea_search_var, width=30)
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.search_teas())
        
        ttk.Button(search_frame, text="Clear", command=self.clear_tea_search).pack(side='left', padx=5)
        
        # Content frame
        content_frame = ttk.Frame(tab)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tea list
        list_frame = ttk.LabelFrame(content_frame, text="Tea Varieties", padding="5")
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tea_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.tea_listbox.pack(side='left', fill='both', expand=True)
        self.tea_listbox.bind('<<ListboxSelect>>', self.on_tea_select)
        scrollbar.config(command=self.tea_listbox.yview)
        
        # Details frame
        details_frame = ttk.LabelFrame(content_frame, text="Details", padding="10")
        details_frame.pack(side='right', fill='both', expand=True)
        
        self.tea_details_text = tk.Text(details_frame, wrap='word', width=40, height=20)
        self.tea_details_text.pack(fill='both', expand=True)
        self.tea_details_text.config(state='disabled')
    
    def create_blend_browser_tab(self):
        """Create blend browser tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🫖 Blends")
        
        # Similar structure to tea browser
        ttk.Label(tab, text="Blend browser tab - Similar implementation").pack(pady=20)
    
    def create_journal_tab(self):
        """Create journal tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📓 Journal")
        
        # Journal list
        list_frame = ttk.LabelFrame(tab, text="Recent Entries", padding="5")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.journal_listbox = tk.Listbox(list_frame)
        self.journal_listbox.pack(fill='both', expand=True)
    
    def create_stats_tab(self):
        """Create statistics tab demonstrating controller usage"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Statistics")
        
        stats_frame = ttk.LabelFrame(tab, text="Collection Statistics", padding="10")
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_frame, wrap='word', height=15)
        self.stats_text.pack(fill='both', expand=True)
        
        ttk.Button(tab, text="Refresh Statistics", command=self.update_statistics).pack(pady=10)
    
    def load_data(self):
        """Load initial data using controllers"""
        self.logger.info("Loading initial data")
        
        try:
            # Load teas
            self.teas = self.tea_controller.get_all_teas()
            for tea in self.teas:
                self.tea_listbox.insert(tk.END, tea.get_display_name())
            
            # Load journal
            self.journal_entries = self.journal_controller.get_recent_entries(10)
            for entry in self.journal_entries:
                display = f"{entry.tea_name} - {entry.get_star_display()} - {entry.date}"
                self.journal_listbox.insert(tk.END, display)
            
            # Update statistics
            self.update_statistics()
            
            self.status_var.set(f"Loaded {len(self.teas)} teas and {len(self.journal_entries)} journal entries")
            
        except sqlite3.OperationalError as e:
            self.logger.error(f"Database error: {e}")
            self.show_database_setup_message()
            self.status_var.set("Database not found - see instructions")
        except Exception as e:
            self.logger.error(f"Error loading data: {e}", exc_info=True)
            self.show_error_message(str(e))
            self.status_var.set(f"Error: {e}")
    
    def show_database_setup_message(self):
        """Show database setup instructions"""
        from tkinter import messagebox
        
        message = """Database Not Found!

The tea database needs to be initialized.

To set up the database:

1. Run the setup script:
   python setup_database.py

2. Or create your own database at:
   tea_collection.db

The setup script will create sample data for you to explore.

Would you like to see the Phase 2 demo without a database?
(You can set up the database later)"""
        
        result = messagebox.askyesno(
            "Database Setup Required",
            message
        )
        
        if result:
            # Show info tab
            self.notebook.select(3)  # Select info tab
    
    def show_error_message(self, error: str):
        """Show error message to user"""
        from tkinter import messagebox
        messagebox.showerror("Error", f"An error occurred:\n\n{error}")
    
    def search_teas(self):
        """Search teas using controller"""
        query = self.tea_search_var.get()
        self.logger.debug(f"Searching teas: {query}")
        
        if query:
            self.teas = self.tea_controller.search_teas(query=query)
        else:
            self.teas = self.tea_controller.get_all_teas()
        
        # Update listbox
        self.tea_listbox.delete(0, tk.END)
        for tea in self.teas:
            self.tea_listbox.insert(tk.END, tea.get_display_name())
        
        self.status_var.set(f"Found {len(self.teas)} teas")
    
    def clear_tea_search(self):
        """Clear tea search"""
        self.tea_search_var.set('')
        self.search_teas()
    
    def on_tea_select(self, event):
        """Handle tea selection"""
        selection = self.tea_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        tea = self.teas[index]
        
        # Display details
        details_parts = [
            f"Name: {tea.name}",
            f"Category: {tea.category}",
            f"Origin: {tea.origin}",
        ]
        
        if tea.origin_region:
            details_parts.append(f"Region: {tea.origin_region}")
        
        details_parts.extend([
            "",
            "Flavor Profile:",
            tea.flavor_profile or 'Not specified',
            "",
            "Brewing:",
            f"Temperature: {tea.get_temperature_display()}",
            f"Steep Time: {tea.steep_time or 'Not specified'}",
            f"Caffeine: {tea.caffeine_level or 'Not specified'}",
        ])
        
        if tea.history:
            details_parts.extend(["", "History:", tea.history])
        
        details = "\n".join(details_parts)
        
        self.tea_details_text.config(state='normal')
        self.tea_details_text.delete('1.0', tk.END)
        self.tea_details_text.insert('1.0', details)
        self.tea_details_text.config(state='disabled')
    
    def update_statistics(self):
        """Update statistics display"""
        stats = f"""
COLLECTION STATISTICS

Teas: {self.tea_controller.get_tea_count()}
Blends: {self.blend_controller.get_blend_count()}
Journal Entries: {self.journal_controller.get_entry_count()}

TEA CATEGORIES:
"""
        
        categories = self.tea_controller.get_categories()
        for category in categories:
            count = len(self.tea_controller.get_teas_by_category(category))
            stats += f"  {category}: {count}\n"
        
        stats += "\nTOP RATED TEAS:\n"
        top_teas = self.journal_controller.get_top_rated_teas(5)
        for tea_name, avg_rating, count in top_teas:
            stars = '★' * int(round(avg_rating))
            stats += f"  {tea_name}: {stars} ({avg_rating:.1f}/5, {count} entries)\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert('1.0', stats)
    
    def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Cleaning up resources")
        self.tea_db.close()
        self.logger.info("Application closed")


def main():
    """Main entry point"""
    # Initialize configuration and logging
    config = get_config()
    LoggerSetup.setup_logging(config)
    logger = get_logger(__name__)
    
    logger.info("="*60)
    logger.info("Tea Collection Explorer - Phase 2 Architecture")
    logger.info("="*60)
    
    # Create and run application
    root = tk.Tk()
    app = TeaExplorerApp(root)
    
    # Handle window close
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
    # Run
    root.mainloop()


if __name__ == "__main__":
    main()
