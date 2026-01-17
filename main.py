"""
Tea Collection Explorer - Enhanced Edition with Full Feature Integration
Combines Phase 4 architecture with all original features
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from pathlib import Path
import sys
import sqlite3
import json
from datetime import datetime
import threading
import time

# Import Phase 4 architecture
from config import get_config
from logger_setup import LoggerSetup, get_logger
from database import (
    DatabaseConnection,
    TeaRepository,
    BlendRepository,
    JournalRepository,
    CultivarRepository,
    CompanyRepository,
    ProductRepository,
    TisaneRepository,
    RegionRepository
)
from controllers import (
    TeaController,
    BlendController,
    JournalController,
    CultivarController,
    CompanyController,
    TisaneController
)
from models import Tea, Blend, JournalEntry, Cultivar, Company, Product, Tisane, Region
from themes import theme_manager
from visualizations import ChartGenerator, DashboardGenerator
from recommendations import RecommendationEngine


class TeaExplorerEnhanced:
    """Enhanced Tea Explorer with all original features"""
    
    def __init__(self, root):
        """Initialize application"""
        self.root = root
        self.logger = get_logger(__name__)
        
        # Configuration
        self.config = get_config()
        
        # Window setup
        self.root.title("Tea & Tisane Collection Explorer - Enhanced Edition")
        self.root.geometry("1400x900")
        
        # Initialize databases
        self.logger.info("Initializing databases")
        self.tea_db = DatabaseConnection("tea_collection.db")
        
        # Create repositories
        self.logger.info("Creating repositories")
        tea_conn = self.tea_db.get_connection()
        self.tea_repo = TeaRepository(tea_conn)
        self.blend_repo = BlendRepository(tea_conn)
        self.journal_repo = JournalRepository("tea_journal.json")
        self.cultivar_repo = CultivarRepository(tea_conn)
        self.company_repo = CompanyRepository(tea_conn)
        self.product_repo = ProductRepository(tea_conn)
        self.region_repo = RegionRepository(tea_conn)
        self.tisane_repo = TisaneRepository("tisane_collection.db")
        
        # Create controllers
        self.logger.info("Creating controllers")
        self.tea_controller = TeaController(self.tea_repo)
        self.blend_controller = BlendController(self.blend_repo)
        self.journal_controller = JournalController(self.journal_repo)
        self.cultivar_controller = CultivarController(self.cultivar_repo)
        self.company_controller = CompanyController(self.company_repo, self.product_repo)
        self.tisane_controller = TisaneController(self.tisane_repo)
        
        # Create recommendation engine
        self.recommendation_engine = RecommendationEngine()
        
        # Create chart generators
        self.chart_generator = ChartGenerator()
        self.dashboard_generator = DashboardGenerator()
        
        # Brewing timer state
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_thread = None
        
        # Comparison state
        self.comparison_items = []
        
        # Create UI
        self.create_ui()
        
        # Apply theme
        self.apply_theme()
        
        # Load statistics
        self.update_status_bar()
        
        self.logger.info("Application initialized successfully")
    
    def create_ui(self):
        """Create complete user interface with all tabs"""
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar widget first (so it exists for update calls)
        self.status_bar = ttk.Label(self.root, text="", relief=tk.SUNKEN, anchor='w')
        # Pack it at bottom BEFORE packing notebook
        self.status_bar.pack(side='bottom', fill='x')
        
        # Main notebook for tabs - pack AFTER status bar
        # This way notebook expands to fill remaining space above status bar
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create all tabs
        self.create_tea_tab()
        self.create_blends_tab()
        self.create_cultivars_tab()
        self.create_brands_tab()
        self.create_tisanes_tab()
        self.create_journal_tab()
        self.create_brewing_timer_tab()
        self.create_comparison_tab()
        self.create_dashboard_tab()
        self.create_guide_tab()
        self.create_history_tab()
        self.create_map_tab()
        
        # Update status bar with initial values
        self.update_status_bar()
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Collection (CSV)", command=self.export_csv)
        file_menu.add_command(label="Export Collection (JSON)", command=self.export_json)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Dark Mode", command=lambda: self.change_theme('dark'))
        view_menu.add_command(label="Light Mode", command=lambda: self.change_theme('light'))
        view_menu.add_command(label="Tea Theme", command=lambda: self.change_theme('tea'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Tea Glossary", command=self.show_glossary)
        help_menu.add_command(label="User Guide", command=self.show_user_guide)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_tea_tab(self):
        """Create tea browser tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🍵 Teas")
        
        # Paned window
        paned = tk.PanedWindow(frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - list and search
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, width=300)
        
        # Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.tea_search_var = tk.StringVar()
        self.tea_search_var.trace('w', lambda *args: self.search_teas())
        search_entry = ttk.Entry(search_frame, textvariable=self.tea_search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Category filter
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(filter_frame, text="Category:").pack(side='left')
        self.tea_category_var = tk.StringVar(value="All")
        categories = ["All"] + self.tea_controller.get_categories()
        category_combo = ttk.Combobox(filter_frame, textvariable=self.tea_category_var,
                                      values=categories, state='readonly', width=15)
        category_combo.pack(side='left', padx=5)
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.search_teas())
        
        # Tea listbox
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tea_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        self.tea_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tea_listbox.yview)
        
        self.tea_listbox.bind('<<ListboxSelect>>', self.on_tea_select)
        
        # Right panel - details
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        # Details text
        self.tea_detail_text = scrolledtext.ScrolledText(right_frame, wrap='word', width=80, height=40)
        self.tea_detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(button_frame, text="Add to Journal", command=self.add_tea_to_journal).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Compare", command=self.add_tea_to_comparison).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Similar Teas", command=self.show_similar_teas).pack(side='left', padx=2)
        
        # Load teas
        self.load_teas()
    
    def create_blends_tab(self):
        """Create blends browser tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🫖 Blends")
        
        # Similar structure to tea tab
        paned = tk.PanedWindow(frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, width=300)
        
        # Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.blend_search_var = tk.StringVar()
        self.blend_search_var.trace('w', lambda *args: self.search_blends())
        search_entry = ttk.Entry(search_frame, textvariable=self.blend_search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Listbox
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.blend_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        self.blend_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.blend_listbox.yview)
        
        self.blend_listbox.bind('<<ListboxSelect>>', self.on_blend_select)
        
        # Right panel
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        self.blend_detail_text = scrolledtext.ScrolledText(right_frame, wrap='word', width=80)
        self.blend_detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load blends
        self.load_blends()
    
    def create_cultivars_tab(self):
        """Create cultivars browser tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌱 Cultivars")
        
        paned = tk.PanedWindow(frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, width=300)
        
        ttk.Label(left_frame, text="Tea Plant Cultivars", font=('', 12, 'bold')).pack(pady=5)
        
        # Species filter
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(filter_frame, text="Species:").pack(side='left')
        self.cultivar_species_var = tk.StringVar(value="All")
        species = ["All"] + self.cultivar_controller.get_species_list()
        species_combo = ttk.Combobox(filter_frame, textvariable=self.cultivar_species_var,
                                     values=species, state='readonly', width=20)
        species_combo.pack(side='left', padx=5)
        species_combo.bind('<<ComboboxSelected>>', lambda e: self.load_cultivars())
        
        # Listbox
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.cultivar_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        self.cultivar_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.cultivar_listbox.yview)
        
        self.cultivar_listbox.bind('<<ListboxSelect>>', self.on_cultivar_select)
        
        # Right panel
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        self.cultivar_detail_text = scrolledtext.ScrolledText(right_frame, wrap='word', width=80)
        self.cultivar_detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load cultivars
        self.load_cultivars()
    
    def create_brands_tab(self):
        """Create brands & products browser tab"""
        frame = ttk.Frame(self.notebook)
        companies_count = self.company_controller.get_company_count()
        products_count = self.company_controller.get_product_count()
        self.notebook.add(frame, text="🏢 Brands")
        
        paned = tk.PanedWindow(frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - companies
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, width=300)
        
        ttk.Label(left_frame, text="Tea Companies", font=('', 12, 'bold')).pack(pady=5)
        
        # Country filter
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(filter_frame, text="Country:").pack(side='left')
        self.company_country_var = tk.StringVar(value="All")
        countries = ["All"] + self.company_controller.get_countries()
        country_combo = ttk.Combobox(filter_frame, textvariable=self.company_country_var,
                                     values=countries, state='readonly', width=15)
        country_combo.pack(side='left', padx=5)
        country_combo.bind('<<ComboboxSelected>>', lambda e: self.load_companies())
        
        # Companies listbox
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.company_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        self.company_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.company_listbox.yview)
        
        self.company_listbox.bind('<<ListboxSelect>>', self.on_company_select)
        
        # Right panel - company details and products
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        # Company details
        self.company_detail_text = scrolledtext.ScrolledText(right_frame, wrap='word', width=80, height=15)
        self.company_detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Products label
        ttk.Label(right_frame, text="Products:", font=('', 11, 'bold')).pack(anchor='w', padx=5)
        
        # Products listbox
        product_frame = ttk.Frame(right_frame)
        product_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        product_scroll = ttk.Scrollbar(product_frame)
        product_scroll.pack(side='right', fill='y')
        
        self.product_listbox = tk.Listbox(product_frame, yscrollcommand=product_scroll.set, height=10)
        self.product_listbox.pack(side='left', fill='both', expand=True)
        product_scroll.config(command=self.product_listbox.yview)
        
        # Load companies
        self.load_companies()
    
    def create_tisanes_tab(self):
        """Create tisanes/herbal teas browser tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌿 Tisanes")
        
        paned = tk.PanedWindow(frame, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, width=300)
        
        ttk.Label(left_frame, text="Herbal Teas & Tisanes", font=('', 12, 'bold')).pack(pady=5)
        
        # Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.tisane_search_var = tk.StringVar()
        self.tisane_search_var.trace('w', lambda *args: self.search_tisanes())
        search_entry = ttk.Entry(search_frame, textvariable=self.tisane_search_var)
        search_entry.pack(side='left', fill='x', expand=True, padx=5)
        
        # Family filter
        filter_frame = ttk.Frame(left_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(filter_frame, text="Family:").pack(side='left')
        self.tisane_family_var = tk.StringVar(value="All")
        families = ["All"] + self.tisane_controller.get_plant_families()
        family_combo = ttk.Combobox(filter_frame, textvariable=self.tisane_family_var,
                                    values=families, state='readonly', width=15)
        family_combo.pack(side='left', padx=5)
        family_combo.bind('<<ComboboxSelected>>', lambda e: self.search_tisanes())
        
        # Caffeine-free filter
        self.tisane_caffeine_free_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left_frame, text="Caffeine-free only",
                       variable=self.tisane_caffeine_free_var,
                       command=self.search_tisanes).pack(anchor='w', padx=5, pady=5)
        
        # Listbox
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tisane_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        self.tisane_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tisane_listbox.yview)
        
        self.tisane_listbox.bind('<<ListboxSelect>>', self.on_tisane_select)
        
        # Right panel
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        self.tisane_detail_text = scrolledtext.ScrolledText(right_frame, wrap='word', width=80)
        self.tisane_detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load tisanes
        self.load_tisanes()
    
    def create_journal_tab(self):
        """Create tea journal tab"""
        frame = ttk.Frame(self.notebook)
        entries_count = len(self.journal_controller.get_all_entries())
        self.notebook.add(frame, text="📓 Journal")
        
        # Similar to existing journal implementation
        ttk.Label(frame, text="Tea Tasting Journal", font=('', 14, 'bold')).pack(pady=10)
        
        # Entry list
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.journal_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=15)
        self.journal_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.journal_listbox.yview)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="New Entry", command=self.new_journal_entry).pack(side='left', padx=5)
        ttk.Button(button_frame, text="View Entry", command=self.view_journal_entry).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete Entry", command=self.delete_journal_entry).pack(side='left', padx=5)
        
        # Load entries
        self.load_journal_entries(); self.update_status_bar()
    
    def create_brewing_timer_tab(self):
        """Create brewing timer tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⏱️ Timer")
        
        ttk.Label(frame, text="Brewing Timer", font=('', 14, 'bold')).pack(pady=10)
        
        # Timer display
        self.timer_label = ttk.Label(frame, text="00:00", font=('', 48, 'bold'))
        self.timer_label.pack(pady=20)
        
        # Time presets
        preset_frame = ttk.Frame(frame)
        preset_frame.pack(pady=10)
        
        ttk.Label(preset_frame, text="Presets:", font=('', 11, 'bold')).pack()
        
        presets = [
            ("Green Tea (3 min)", 180),
            ("Black Tea (5 min)", 300),
            ("Oolong (4 min)", 240),
            ("White Tea (4 min)", 240),
            ("Pu-erh (5 min)", 300)
        ]
        
        for label, seconds in presets:
            ttk.Button(preset_frame, text=label,
                      command=lambda s=seconds: self.set_timer(s)).pack(side='left', padx=5)
        
        # Manual input
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Minutes:").pack(side='left')
        self.timer_minutes_var = tk.IntVar(value=3)
        minutes_spin = ttk.Spinbox(input_frame, from_=1, to=30, textvariable=self.timer_minutes_var, width=5)
        minutes_spin.pack(side='left', padx=5)
        
        ttk.Button(input_frame, text="Set", command=self.set_timer_from_input).pack(side='left', padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(frame)
        control_frame.pack(pady=20)
        
        self.timer_start_btn = ttk.Button(control_frame, text="▶️ Start", command=self.start_timer)
        self.timer_start_btn.pack(side='left', padx=10)
        
        self.timer_pause_btn = ttk.Button(control_frame, text="⏸️ Pause", command=self.pause_timer, state='disabled')
        self.timer_pause_btn.pack(side='left', padx=10)
        
        self.timer_reset_btn = ttk.Button(control_frame, text="🔄 Reset", command=self.reset_timer)
        self.timer_reset_btn.pack(side='left', padx=10)
    
    def create_comparison_tab(self):
        """Create tea comparison tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚖️ Compare")
        
        ttk.Label(frame, text="Tea Comparison Tool", font=('', 14, 'bold')).pack(pady=10)
        ttk.Label(frame, text="Add teas from the Teas tab to compare side-by-side").pack(pady=5)
        
        # Comparison frame
        self.comparison_frame = ttk.Frame(frame)
        self.comparison_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Clear button
        ttk.Button(frame, text="Clear All", command=self.clear_comparison).pack(pady=5)
    
    def create_dashboard_tab(self):
        """Create dashboard with visualizations"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Dashboard")
        
        ttk.Label(frame, text="Collection Dashboard", font=('', 14, 'bold')).pack(pady=10)
        
        # Statistics
        stats_frame = ttk.LabelFrame(frame, text="Statistics", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        stats_text = f"""
Total Teas: {self.tea_controller.get_tea_count()}
Total Blends: {self.blend_controller.get_blend_count()}
Tea Cultivars: {self.cultivar_controller.get_cultivar_count()}
Tea Companies: {self.company_controller.get_company_count()}
Tea Products: {self.company_controller.get_product_count()}
Herbal Tisanes: {self.tisane_controller.get_tisane_count()}
Journal Entries: {len(self.journal_controller.get_all_entries())}
        """
        
        ttk.Label(stats_frame, text=stats_text, font=('', 11)).pack()
        
        # Visualization buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="📊 Category Distribution",
                  command=self.show_category_chart).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🌍 Origin Countries",
                  command=self.show_origin_chart).pack(side='left', padx=5)
        ttk.Button(button_frame, text="⭐ Rating Distribution",
                  command=self.show_rating_chart).pack(side='left', padx=5)
    
    def create_guide_tab(self):
        """Create tea varieties guide tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📖 Guide")
        
        ttk.Label(frame, text="Tea Varieties Guide", font=('', 14, 'bold')).pack(pady=10)
        
        # Load and display markdown file
        text_widget = scrolledtext.ScrolledText(frame, wrap='word', width=100, height=40)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            with open('tea_varieties_list.md', 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert('1.0', content)
                text_widget.config(state='disabled')
        except FileNotFoundError:
            text_widget.insert('1.0', "Guide file not found. Please ensure tea_varieties_list.md is in the application directory.")
            text_widget.config(state='disabled')
    
    def create_history_tab(self):
        """Create tea history tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📜 History")
        
        ttk.Label(frame, text="Tea History", font=('', 14, 'bold')).pack(pady=10)
        
        # Load and display markdown file
        text_widget = scrolledtext.ScrolledText(frame, wrap='word', width=100, height=40)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        
        try:
            with open('tea_history.md', 'r', encoding='utf-8') as f:
                content = f.read()
                text_widget.insert('1.0', content)
                text_widget.config(state='disabled')
        except FileNotFoundError:
            text_widget.insert('1.0', "History file not found. Please ensure tea_history.md is in the application directory.")
            text_widget.config(state='disabled')
    
    def create_map_tab(self):
        """Create interactive world map tab with plotted regions"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🗺️ Map")
        
        ttk.Label(frame, text="Tea Growing Regions of the World", font=('', 14, 'bold')).pack(pady=10)
        
        # Try to load map image and plot regions
        try:
            from PIL import Image, ImageTk, ImageDraw
            
            # Load and resize map
            img = Image.open('world_map_bg.png')
            img = img.resize((1200, 600), Image.Resampling.LANCZOS)
            
            # Create drawing context to add region markers
            draw = ImageDraw.Draw(img)
            
            # Get all regions with coordinates
            regions = self.region_repo.find_all()
            
            # Plot each region as a red dot
            for region in regions:
                if region.latitude and region.longitude:
                    # Convert lat/long to pixel coordinates
                    # Map longitude (-180 to 180) to x (0 to 1200)
                    # Map latitude (90 to -90) to y (0 to 600)
                    x = int((region.longitude + 180) * (1200 / 360))
                    y = int((90 - region.latitude) * (600 / 180))
                    
                    # Draw red circle for region
                    radius = 6
                    draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                                fill='red', outline='darkred', width=2)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Create canvas for map
            canvas = tk.Canvas(frame, width=1200, height=600, bg='white')
            canvas.pack(padx=10, pady=10)
            canvas.create_image(0, 0, image=photo, anchor='nw')
            canvas.image = photo  # Keep a reference
            
            # Legend
            legend_frame = ttk.LabelFrame(frame, text="Legend", padding=10)
            legend_frame.pack(fill='x', padx=10, pady=5)
            
            # Create a mini canvas for legend dot
            legend_canvas = tk.Canvas(legend_frame, width=20, height=20, bg='white', highlightthickness=0)
            legend_canvas.pack(side='left', padx=5)
            legend_canvas.create_oval(7, 7, 13, 13, fill='red', outline='darkred', width=2)
            ttk.Label(legend_frame, text="= Tea Growing Region").pack(side='left')
            
            # Region list
            info_frame = ttk.LabelFrame(frame, text=f"Tea Regions ({len(regions)} total)", padding=10)
            info_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            # Create scrolled text for region list
            region_text = scrolledtext.ScrolledText(info_frame, height=6, wrap='word')
            region_text.pack(fill='both', expand=True)
            
            # Format regions by country
            regions_by_country = {}
            for r in regions:
                if r.country not in regions_by_country:
                    regions_by_country[r.country] = []
                regions_by_country[r.country].append(r.name)
            
            # Display regions grouped by country
            for country in sorted(regions_by_country.keys()):
                region_text.insert(tk.END, f"\n{country}:\n", 'country')
                for region_name in regions_by_country[country]:
                    region_text.insert(tk.END, f"  • {region_name}\n")
            
            # Configure tag for country names (bold)
            region_text.tag_config('country', font=('', 10, 'bold'))
            region_text.config(state='disabled')
            
        except Exception as e:
            ttk.Label(frame, text=f"Map image not available: {e}").pack(pady=20)
    
    def create_status_bar(self):
        """Create comprehensive status bar showing database contents"""
        # Widget is created in create_ui, this method is no longer used
        # Keeping for compatibility
        pass
    
    def update_status_bar(self):
        """Update status bar with current database statistics"""
        teas_count = self.tea_controller.get_tea_count()
        blends_count = self.blend_controller.get_blend_count()
        cultivars_count = self.cultivar_controller.get_cultivar_count()
        companies_count = self.company_controller.get_company_count()
        products_count = self.company_controller.get_product_count()
        tisanes_count = self.tisane_controller.get_tisane_count()
        journal_count = len(self.journal_controller.get_all_entries())
        regions_count = len(self.region_repo.find_all())
        
        total = teas_count + blends_count + cultivars_count + companies_count + products_count + tisanes_count + regions_count
        
        status_text = (f"Database Contents: Teas: {teas_count} | Blends: {blends_count} | "
                      f"Cultivars: {cultivars_count} | Companies: {companies_count} | "
                      f"Products: {products_count} | Tisanes: {tisanes_count} | "
                      f"Regions: {regions_count} | Journal Entries: {journal_count} | "
                      f"Total: {total}")
        
        self.status_bar.config(text=status_text)
    
    # Data loading methods
    def load_teas(self):
        """Load teas into listbox"""
        self.tea_listbox.delete(0, tk.END)
        teas = self.tea_controller.get_all_teas()
        for tea in teas:
            self.tea_listbox.insert(tk.END, tea.name)
    
    def load_blends(self):
        """Load blends into listbox"""
        self.blend_listbox.delete(0, tk.END)
        blends = self.blend_controller.get_all_blends()
        for blend in blends:
            self.blend_listbox.insert(tk.END, blend.blend_name)
    
    def load_cultivars(self):
        """Load cultivars into listbox"""
        self.cultivar_listbox.delete(0, tk.END)
        
        species = self.cultivar_species_var.get()
        if species == "All":
            cultivars = self.cultivar_controller.get_all_cultivars()
        else:
            cultivars = self.cultivar_controller.get_cultivars_by_species(species)
        
        for cultivar in cultivars:
            self.cultivar_listbox.insert(tk.END, cultivar.name)
    
    def load_companies(self):
        """Load companies into listbox"""
        self.company_listbox.delete(0, tk.END)
        
        country = self.company_country_var.get()
        if country == "All":
            companies = self.company_controller.get_all_companies()
        else:
            companies = self.company_controller.get_companies_by_country(country)
        
        for company in companies:
            self.company_listbox.insert(tk.END, company.company_name)
    
    def load_tisanes(self):
        """Load tisanes into listbox"""
        self.tisane_listbox.delete(0, tk.END)
        tisanes = self.tisane_controller.get_all_tisanes()
        for tisane in tisanes:
            self.tisane_listbox.insert(tk.END, tisane.name)
    
    def load_journal_entries(self):
        """Load journal entries"""
        self.journal_listbox.delete(0, tk.END)
        entries = self.journal_controller.get_all_entries()
        for entry in entries:
            display = f"{entry.date} - {entry.tea_name} ({entry.rating}★)"
            self.journal_listbox.insert(tk.END, display)
    
    # Search methods
    def search_teas(self):
        """Search teas"""
        query = self.tea_search_var.get()
        category = self.tea_category_var.get()
        
        self.tea_listbox.delete(0, tk.END)
        
        if query:
            teas = self.tea_controller.search_teas(query)
        else:
            if category == "All":
                teas = self.tea_controller.get_all_teas()
            else:
                teas = self.tea_controller.get_teas_by_category(category)
        
        for tea in teas:
            self.tea_listbox.insert(tk.END, tea.name)
    
    def search_blends(self):
        """Search blends"""
        query = self.blend_search_var.get()
        self.blend_listbox.delete(0, tk.END)
        
        if query:
            blends = self.blend_controller.search_blends(query)
        else:
            blends = self.blend_controller.get_all_blends()
        
        for blend in blends:
            self.blend_listbox.insert(tk.END, blend.blend_name)
    
    def search_tisanes(self):
        """Search tisanes"""
        query = self.tisane_search_var.get()
        family = self.tisane_family_var.get()
        caffeine_free = self.tisane_caffeine_free_var.get()
        
        self.tisane_listbox.delete(0, tk.END)
        
        if caffeine_free:
            tisanes = self.tisane_controller.get_caffeine_free_tisanes()
        elif query:
            tisanes = self.tisane_controller.search_tisanes(query)
        elif family != "All":
            tisanes = self.tisane_controller.get_tisanes_by_family(family)
        else:
            tisanes = self.tisane_controller.get_all_tisanes()
        
        for tisane in tisanes:
            self.tisane_listbox.insert(tk.END, tisane.name)
    
    # Selection handlers
    def on_tea_select(self, event):
        """Handle tea selection"""
        selection = self.tea_listbox.curselection()
        if not selection:
            return
        
        name = self.tea_listbox.get(selection[0])
        tea = self.tea_controller.get_tea_by_name(name)
        
        if tea:
            # Format with clear sections and better spacing
            details = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  {tea.name.upper().center(68)}  ║
╚══════════════════════════════════════════════════════════════════════╝

CLASSIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Category:  {tea.category or 'N/A'}
  Origin:    {tea.origin or 'N/A'}
  Processing: {tea.processing or 'N/A'}
  Oxidation:  {tea.oxidation or 'N/A'}

SENSORY PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Flavor:     {tea.flavor_profile or 'N/A'}
  Aroma:      {tea.aroma or 'N/A'}
  Appearance: {tea.appearance or 'N/A'}

BREWING PARAMETERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Temperature:   {tea.brew_temp_c}°C ({tea.brew_temp_f}°F)
  Steep Time:    {tea.steep_time or 'N/A'}
  Water Ratio:   {tea.tea_water_ratio or 'N/A'}
  Reinfusions:   {tea.reinfusions or 'N/A'}

PROPERTIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Caffeine:      {tea.caffeine_level or 'N/A'}
  Price Range:   {tea.price_range or 'N/A'}
  Cultivars:     {tea.cultivars or 'N/A'}

HEALTH BENEFITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{tea.health_benefits or 'N/A'}

HISTORY & BACKGROUND
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{tea.history or 'N/A'}
            """
            
            self.tea_detail_text.delete('1.0', tk.END)
            self.tea_detail_text.insert('1.0', details)
            self.current_tea = tea
    
    def on_blend_select(self, event):
        """Handle blend selection"""
        selection = self.blend_listbox.curselection()
        if not selection:
            return
        
        name = self.blend_listbox.get(selection[0])
        blend = self.blend_controller.get_blend_by_name(name)
        
        if blend:
            details = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  {blend.blend_name.upper().center(68)}  ║
╚══════════════════════════════════════════════════════════════════════╝

BLEND INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Category:        {blend.category or 'N/A'}
  Base Tea:        {blend.base_tea or 'N/A'}
  Origin Region:   {blend.origin_region or 'N/A'}

INGREDIENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{blend.ingredients or 'N/A'}

SENSORY PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Flavor:      {blend.flavor_profile or 'N/A'}
  Aroma:       {blend.aroma or 'N/A'}
  Appearance:  {blend.appearance or 'N/A'}

BREWING PARAMETERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Temperature:   {blend.brew_temp_c}°C ({blend.brew_temp_f}°F)
  Steep Time:    {blend.steep_time or 'N/A'}

PROPERTIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Caffeine:         {blend.caffeine_level or 'N/A'}
  Price Range:      {blend.price_range or 'N/A'}
  Popular Brands:   {blend.popular_brands or 'N/A'}

DESCRIPTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{blend.description or 'N/A'}

HEALTH BENEFITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{blend.health_benefits or 'N/A'}

SERVING SUGGESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{blend.serving_suggestions or 'N/A'}

HISTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{blend.history or 'N/A'}
            """
            
            self.blend_detail_text.delete('1.0', tk.END)
            self.blend_detail_text.insert('1.0', details)
    
    def on_cultivar_select(self, event):
        """Handle cultivar selection"""
        selection = self.cultivar_listbox.curselection()
        if not selection:
            return
        
        name = self.cultivar_listbox.get(selection[0])
        cultivar = self.cultivar_controller.get_cultivar_by_name(name)
        
        if cultivar:
            details = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  {cultivar.name.upper().center(68)}  ║
╚══════════════════════════════════════════════════════════════════════╝

CULTIVAR INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Species:      {cultivar.species or 'N/A'}
  Origin:       {cultivar.origin_country or 'N/A'}
  Leaf Size:    {cultivar.leaf_size or 'N/A'}

CHARACTERISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{cultivar.characteristics or 'N/A'}

COMMON USES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{cultivar.common_uses or 'N/A'}

ADDITIONAL NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{cultivar.notes or 'N/A'}
            """
            
            self.cultivar_detail_text.delete('1.0', tk.END)
            self.cultivar_detail_text.insert('1.0', details)
    
    def on_company_select(self, event):
        """Handle company selection"""
        selection = self.company_listbox.curselection()
        if not selection:
            return
        
        name = self.company_listbox.get(selection[0])
        company = self.company_controller.get_company_by_name(name)
        
        if company:
            details = f"""
{company.company_name}
{'='*70}

Parent Company: {company.parent_company}
Founded: {company.founded_year}
Headquarters: {company.headquarters_city}, {company.country_of_origin}

Website: {company.website}
Certifications: {company.certifications}
Market Segment: {company.market_segment}

Description:
{company.description}
            """
            
            self.company_detail_text.delete('1.0', tk.END)
            self.company_detail_text.insert('1.0', details)
            
            # Load products
            self.product_listbox.delete(0, tk.END)
            products = self.company_controller.get_products_for_company(company.company_id)
            for product in products:
                self.product_listbox.insert(tk.END, product.product_name)
    
    def on_tisane_select(self, event):
        """Handle tisane selection"""
        selection = self.tisane_listbox.curselection()
        if not selection:
            return
        
        name = self.tisane_listbox.get(selection[0])
        tisane = self.tisane_controller.get_tisane_by_name(name)
        
        if tisane:
            caffeine_status = "✅ Caffeine-Free" if tisane.is_caffeine_free() else "Contains Caffeine"
            
            details = f"""
{tisane.name}
{'='*70}

Scientific Name: {tisane.scientific_name}
Plant Family: {tisane.plant_family}
Part Used: {tisane.plant_part_used}

Origin: {tisane.origin_region}
Tradition: {tisane.tradition}

Flavor Profile: {tisane.flavor_profile}
Aroma: {tisane.aroma}

Brewing:
• Temperature: {tisane.get_temperature_display()}
• Steep Time: {tisane.steep_time}

Caffeine: {caffeine_status}

Traditional Uses:
{tisane.traditional_uses}

Research Benefits:
{tisane.research_benefits}

Key Compounds:
{tisane.key_compounds}

⚠️ Safety: Always consult healthcare provider before use, especially if pregnant, nursing, or taking medications.
            """
            
            self.tisane_detail_text.delete('1.0', tk.END)
            self.tisane_detail_text.insert('1.0', details)
    
    # Timer methods
    def set_timer(self, seconds):
        """Set timer to specific seconds"""
        self.timer_seconds = seconds
        self.update_timer_display()
    
    def set_timer_from_input(self):
        """Set timer from manual input"""
        minutes = self.timer_minutes_var.get()
        self.set_timer(minutes * 60)
    
    def start_timer(self):
        """Start timer"""
        if self.timer_seconds == 0:
            messagebox.showwarning("Timer", "Please set a time first")
            return
        
        self.timer_running = True
        self.timer_start_btn.config(state='disabled')
        self.timer_pause_btn.config(state='normal')
        
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
    
    def pause_timer(self):
        """Pause timer"""
        self.timer_running = False
        self.timer_start_btn.config(state='normal')
        self.timer_pause_btn.config(state='disabled')
    
    def reset_timer(self):
        """Reset timer"""
        self.timer_running = False
        self.timer_seconds = 0
        self.update_timer_display()
        self.timer_start_btn.config(state='normal')
        self.timer_pause_btn.config(state='disabled')
    
    def run_timer(self):
        """Timer thread"""
        while self.timer_running and self.timer_seconds > 0:
            time.sleep(1)
            self.timer_seconds -= 1
            self.root.after(0, self.update_timer_display)
        
        if self.timer_seconds == 0:
            self.root.after(0, self.timer_complete)
    
    def update_timer_display(self):
        """Update timer display"""
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
    
    def timer_complete(self):
        """Timer completed"""
        self.timer_running = False
        self.timer_start_btn.config(state='normal')
        self.timer_pause_btn.config(state='disabled')
        messagebox.showinfo("Timer", "⏰ Brewing complete! Your tea is ready.")
    
    # Journal methods
    def add_tea_to_journal(self):
        """Add current tea to journal (quick add)"""
        if not hasattr(self, 'current_tea') or not self.current_tea:
            messagebox.showwarning("Selection", "Please select a tea first")
            return
        
        # Create dialog pre-filled with current tea
        dialog = tk.Toplevel(self.root)
        dialog.title("Add to Journal")
        dialog.geometry("500x600")
        
        # Tea name (pre-filled)
        ttk.Label(dialog, text="Tea Name:").pack(pady=5)
        tea_name_var = tk.StringVar(value=self.current_tea.name)
        tea_entry = ttk.Entry(dialog, textvariable=tea_name_var, width=40)
        tea_entry.pack(pady=5)
        
        # Rating
        ttk.Label(dialog, text="Rating (1-5):").pack(pady=5)
        rating_var = tk.IntVar(value=5)
        rating_scale = ttk.Scale(dialog, from_=1, to=5, variable=rating_var, orient='horizontal')
        rating_scale.pack(pady=5)
        
        # Brewing info (pre-filled)
        ttk.Label(dialog, text="Brewing Info:").pack(pady=5)
        brewing_text = tk.Text(dialog, width=50, height=5)
        brewing_info = f"Temperature: {self.current_tea.brew_temp_c}°C\nSteep time: {self.current_tea.steep_time}\nInfusion #:"
        brewing_text.insert('1.0', brewing_info)
        brewing_text.pack(pady=5)
        
        # Notes
        ttk.Label(dialog, text="Notes:").pack(pady=5)
        notes_text = tk.Text(dialog, width=50, height=10)
        notes_text.pack(pady=5)
        
        # Save button
        def save_entry():
            entry = JournalEntry(
                tea_name=tea_name_var.get(),
                date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                rating=rating_var.get(),
                brewing=brewing_text.get('1.0', tk.END).strip(),
                notes=notes_text.get('1.0', tk.END).strip()
            )
            self.journal_controller.create_entry(entry)
            self.load_journal_entries(); self.update_status_bar()
            dialog.destroy()
            messagebox.showinfo("Success", f"Added {self.current_tea.name} to journal!")
        
        ttk.Button(dialog, text="Save", command=save_entry).pack(pady=10)
    
    def new_journal_entry(self):
        """Create new journal entry"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("New Journal Entry")
        dialog.geometry("500x600")
        
        # Tea name
        ttk.Label(dialog, text="Tea Name:").pack(pady=5)
        tea_name_var = tk.StringVar()
        tea_entry = ttk.Entry(dialog, textvariable=tea_name_var, width=40)
        tea_entry.pack(pady=5)
        
        # Rating
        ttk.Label(dialog, text="Rating (1-5):").pack(pady=5)
        rating_var = tk.IntVar(value=5)
        rating_scale = ttk.Scale(dialog, from_=1, to=5, variable=rating_var, orient='horizontal')
        rating_scale.pack(pady=5)
        
        # Notes
        ttk.Label(dialog, text="Notes:").pack(pady=5)
        notes_text = tk.Text(dialog, width=50, height=15)
        notes_text.pack(pady=5)
        
        # Save button
        def save_entry():
            entry = JournalEntry(
                tea_name=tea_name_var.get(),
                date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                rating=rating_var.get(),
                notes=notes_text.get('1.0', tk.END).strip()
            )
            self.journal_controller.create_entry(entry)
            self.load_journal_entries(); self.update_status_bar()
            dialog.destroy()
            messagebox.showinfo("Success", "Journal entry saved!")
        
        ttk.Button(dialog, text="Save", command=save_entry).pack(pady=10)
    
    def view_journal_entry(self):
        """View journal entry"""
        selection = self.journal_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection", "Please select an entry")
            return
        
        idx = selection[0]
        entries = self.journal_controller.get_all_entries()
        entry = entries[idx]
        
        details = f"""
Tea: {entry.tea_name}
Date: {entry.date}
Rating: {entry.rating}★

Notes:
{entry.notes}
        """
        
        messagebox.showinfo("Journal Entry", details)
    
    def delete_journal_entry(self):
        """Delete journal entry"""
        selection = self.journal_listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection", "Please select an entry")
            return
        
        if messagebox.askyesno("Confirm", "Delete this journal entry?"):
            idx = selection[0]
            entries = self.journal_controller.get_all_entries()
            entry = entries[idx]
            self.journal_controller.delete_entry(entry.entry_id)
            self.load_journal_entries(); self.update_status_bar()
    
    # Comparison methods
    def add_tea_to_comparison(self):
        """Add current tea to comparison"""
        if hasattr(self, 'current_tea') and self.current_tea:
            if len(self.comparison_items) >= 3:
                messagebox.showwarning("Comparison", "Maximum 3 items for comparison")
                return
            
            self.comparison_items.append(self.current_tea)
            self.update_comparison_display()
            messagebox.showinfo("Added", f"{self.current_tea.name} added to comparison")
    
    def clear_comparison(self):
        """Clear comparison"""
        self.comparison_items = []
        self.update_comparison_display()
    
    def update_comparison_display(self):
        """Update comparison display"""
        # Clear frame
        for widget in self.comparison_frame.winfo_children():
            widget.destroy()
        
        # Show compared items
        for i, item in enumerate(self.comparison_items):
            frame = ttk.LabelFrame(self.comparison_frame, text=item.name, padding=10)
            frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            
            details = f"""
Category: {item.category}
Origin: {item.origin}
Caffeine: {item.caffeine_level}
Steep: {item.steep_time}
Temp: {item.brew_temp_c}°C
            """
            
            ttk.Label(frame, text=details, justify='left').pack()
    
    # Visualization methods
    def show_category_chart(self):
        """Show category distribution chart"""
        try:
            teas = self.tea_controller.get_all_teas()
            fig = self.chart_generator.create_category_distribution(teas)
            
            # Show in new window
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Category Distribution")
            chart_window.geometry("800x600")
            
            canvas = FigureCanvasTkAgg(fig, chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate chart: {e}")
    
    def show_origin_chart(self):
        """Show origin distribution chart"""
        try:
            teas = self.tea_controller.get_all_teas()
            fig = self.chart_generator.create_origin_distribution(teas)
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Origin Distribution")
            chart_window.geometry("1000x600")
            
            canvas = FigureCanvasTkAgg(fig, chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate chart: {e}")
    
    def show_rating_chart(self):
        """Show rating distribution chart"""
        try:
            entries = self.journal_controller.get_all_entries()
            fig = self.chart_generator.create_rating_distribution(entries)
            
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            chart_window = tk.Toplevel(self.root)
            chart_window.title("Rating Distribution")
            chart_window.geometry("800x600")
            
            canvas = FigureCanvasTkAgg(fig, chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate chart: {e}")
    
    def show_similar_teas(self):
        """Show similar teas"""
        if not hasattr(self, 'current_tea') or not self.current_tea:
            messagebox.showwarning("Selection", "Please select a tea first")
            return
        
        teas = self.tea_controller.get_all_teas()
        similar = self.recommendation_engine.get_similar_teas(self.current_tea, teas, max_results=5)
        
        if similar:
            names = "\n".join([f"• {tea.name}" for tea in similar])
            messagebox.showinfo("Similar Teas", f"Teas similar to {self.current_tea.name}:\n\n{names}")
        else:
            messagebox.showinfo("Similar Teas", "No similar teas found")
    
    # Export methods
    def export_csv(self):
        """Export collection to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import csv
                
                teas = self.tea_controller.get_all_teas()
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Name', 'Category', 'Origin', 'Caffeine', 'Price'])
                    
                    for tea in teas:
                        writer.writerow([
                            tea.name,
                            tea.category,
                            tea.origin,
                            tea.caffeine_level,
                            tea.price_range
                        ])
                
                messagebox.showinfo("Success", f"Exported {len(teas)} teas to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    def export_json(self):
        """Export collection to JSON"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                teas = self.tea_controller.get_all_teas()
                data = [tea.to_dict() for tea in teas]
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Exported {len(teas)} teas to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    # Theme methods
    def apply_theme(self):
        """Apply current theme"""
        # This would apply theme to widgets
        # For now, just using default ttk theme
        pass
    
    def change_theme(self, theme_name):
        """Change theme"""
        theme_manager.set_theme(theme_name)
        messagebox.showinfo("Theme", f"Theme changed to {theme_name}. Restart to see full effect.")
    
    # Utility methods
    def update_status_bar(self):
        """Update status bar"""
        total = (self.tea_controller.get_tea_count() +
                self.blend_controller.get_blend_count() +
                self.cultivar_controller.get_cultivar_count() +
                self.tisane_controller.get_tisane_count())
        
        self.status_bar.config(text=f"Total Items: {total} | Teas: {self.tea_controller.get_tea_count()} | Blends: {self.blend_controller.get_blend_count()} | Cultivars: {self.cultivar_controller.get_cultivar_count()} | Tisanes: {self.tisane_controller.get_tisane_count()}")
    
    def show_glossary(self):
        """Show tea terminology glossary"""
        glossary_window = tk.Toplevel(self.root)
        glossary_window.title("Tea Terminology Glossary")
        glossary_window.geometry("900x700")
        
        # Create frame with scrolled text
        frame = ttk.Frame(glossary_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(frame, text="Tea Terminology Glossary", 
                               font=('', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Scrolled text widget
        glossary_text = scrolledtext.ScrolledText(frame, wrap='word', 
                                                  font=('', 10))
        glossary_text.pack(fill='both', expand=True)
        
        # Load and display glossary
        try:
            with open('tea_glossary.md', 'r', encoding='utf-8') as f:
                content = f.read()
                glossary_text.insert('1.0', content)
        except FileNotFoundError:
            glossary_text.insert('1.0', "Glossary file not found.")
        
        glossary_text.config(state='disabled')
        
        # Close button
        ttk.Button(frame, text="Close", 
                  command=glossary_window.destroy).pack(pady=10)
    
    def show_user_guide(self):
        """Show user guide with application features"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("User Guide")
        guide_window.geometry("800x600")
        
        # Create frame with scrolled text
        frame = ttk.Frame(guide_window, padding=10)
        frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(frame, text="Tea Explorer User Guide", 
                               font=('', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Guide content
        guide_text = scrolledtext.ScrolledText(frame, wrap='word', font=('', 10))
        guide_text.pack(fill='both', expand=True)
        
        guide_content = """
═══════════════════════════════════════════════════════════════════════════
                         TEA EXPLORER USER GUIDE
═══════════════════════════════════════════════════════════════════════════

OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This comprehensive tea collection manager helps you explore, organize, and
learn about teas, blends, cultivars, and tisanes from around the world.

DATABASE CONTENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 49 Tea Varieties (from Camellia sinensis)
• 26 Tea Blends
• 26 Cultivars (tea plant varieties)
• 28 Tea Companies with 117 Products
• 45 Herbal Tisanes
• 12 Tea-Growing Regions
• Your Personal Journal Entries

TAB OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍵 TEAS TAB
Browse all tea varieties from Camellia sinensis. Search by name or filter
by category (White, Green, Oolong, Black, Pu-erh, Yellow).

Features:
  • Detailed information on origin, processing, and flavor profiles
  • Brewing parameters (temperature, time, water ratio, reinfusions)
  • Health benefits and historical background
  • Add to Journal button for quick tasting notes
  • Compare button to compare with other teas
  • Similar Teas button for AI-powered recommendations

🫖 BLENDS TAB
Explore tea blends and flavored teas. Search by name or browse all blends.

Features:
  • Base tea and ingredient information
  • Flavor profiles and serving suggestions
  • Popular brands producing each blend
  • Complete brewing instructions

🌱 CULTIVARS TAB
Learn about tea plant varieties (cultivars). Filter by species:
  • Camellia sinensis var. sinensis (Chinese variety)
  • Camellia sinensis var. assamica (Assam variety)

Features:
  • Leaf characteristics and origin information
  • Common uses for each cultivar
  • Growing conditions and notes

🏢 BRANDS TAB
Browse tea companies and their products. Filter companies by country.

Features:
  • Company information (headquarters, founding year, certifications)
  • Product listings for each company
  • Market segment and parent company details

🌿 TISANES TAB
Discover herbal infusions (not from tea plant). Search by name or filter
by plant family.

Features:
  • Scientific names and traditional uses
  • Health benefits and safety information
  • Caffeine-free filter option
  • Key compounds and TCM/Ayurvedic properties

📓 JOURNAL TAB
Record your tea tasting experiences.

Features:
  • Create new entries with tea name, rating (1-5 stars), and notes
  • View past entries with dates
  • Delete entries you no longer need
  • Quick access from Teas tab via "Add to Journal" button

⏱️ TIMER TAB
Perfect your brewing with the built-in timer.

Features:
  • Preset times for different tea types:
    - Green Tea: 3 minutes
    - Black Tea: 5 minutes
    - Oolong Tea: 4 minutes
    - White Tea: 4 minutes
    - Pu-erh Tea: 5 minutes
  • Manual time setting (1-30 minutes)
  • Start, Pause, and Reset controls
  • Alert notification when brewing is complete

⚖️ COMPARE TAB
Compare up to 3 teas side-by-side.

Features:
  • Add teas from Teas tab using Compare button
  • Side-by-side comparison of:
    - Category
    - Origin
    - Caffeine level
    - Steep time and temperature
  • Clear all button to start fresh comparison

📊 DASHBOARD TAB
Visualize your collection with statistics and charts.

Features:
  • Collection statistics summary
  • Category Distribution (pie chart)
  • Origin Countries (bar chart)
  • Rating Distribution from journal (histogram)

📖 GUIDE TAB
Comprehensive guide to tea varieties (200+ varieties documented).

Features:
  • Detailed descriptions of tea types
  • Processing methods
  • Regional specialties

📜 HISTORY TAB
Learn about tea's rich cultural history.

Features:
  • Origins of tea culture
  • Historical trade routes
  • Cultural significance across civilizations

🗺️ MAP TAB
Interactive world map showing tea-growing regions.

Features:
  • Visual map with red markers for each region
  • Complete list of regions grouped by country
  • Geographic distribution of tea production

MENU BAR FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILE MENU
  • Export Collection (CSV) - Export all teas to CSV format
  • Export Collection (JSON) - Export all teas to JSON format
  • Exit - Close the application

VIEW MENU
  • Dark Mode - Dark color scheme
  • Light Mode - Light color scheme
  • Tea Theme - Custom tea-inspired theme

HELP MENU
  • Tea Glossary - Comprehensive tea terminology reference
  • User Guide - This guide
  • About - Application information

STATUS BAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The status bar at the bottom shows complete database statistics:
  • Counts for each data type
  • Total items in collection
  • Journal entries count

KEYBOARD SHORTCUTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Click items in lists to view details
  • Use search boxes for quick filtering
  • Dropdown filters for category/family selection

TIPS & BEST PRACTICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Use the Journal to track your tea tastings and preferences
  2. Try the Similar Teas feature to discover new favorites
  3. Compare teas before purchasing to understand differences
  4. Check the Glossary when encountering unfamiliar terms
  5. Use the Timer for consistent brewing results
  6. Export your collection for backup or sharing
  7. Explore different themes for comfortable viewing

GETTING HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Check the Tea Glossary for terminology questions
  • Review this User Guide for feature explanations
  • See the About dialog for application information

═══════════════════════════════════════════════════════════════════════════
                          Enjoy exploring tea!
═══════════════════════════════════════════════════════════════════════════
        """
        
        guide_text.insert('1.0', guide_content)
        guide_text.config(state='disabled')
        
        # Close button
        ttk.Button(frame, text="Close", 
                  command=guide_window.destroy).pack(pady=10)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Tea & Tisane Collection Explorer
Enhanced Edition with Phase 4 Architecture

Features:
• 49+ Tea Varieties
• 26+ Tea Blends
• 26 Cultivars
• 28 Companies with 117 Products
• 45 Herbal Tisanes
• Tea Journal
• Brewing Timer
• Comparison Tool
• Data Visualizations
• Smart Recommendations

Built with Phase 4 Architecture:
• Clean MVC Design
• Performance Optimization
• Modern Themes
• Professional Quality
        """
        
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point"""
    # Setup logging
    LoggerSetup.setup_logging()
    logger = get_logger(__name__)
    
    logger.info("Starting Tea Collection Explorer - Enhanced Edition")
    
    # Create and run application
    root = tk.Tk()
    app = TeaExplorerEnhanced(root)
    
    logger.info("Application started successfully")
    
    root.mainloop()
    
    logger.info("Application closed")


if __name__ == '__main__':
    main()
