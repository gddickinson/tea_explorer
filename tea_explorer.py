"""
Tea Collection Explorer - Enhanced Edition v2.0
A comprehensive tea database browser with advanced features

NEW FEATURES:
- Cultivars browser (26 varieties)
- Brewing timer with alerts
- Tea journal with ratings
- Comparison tool (up to 3 teas)
- Enhanced search (category, caffeine, price)
- Export functions (CSV, TXT, JSON)
- Glossary (30+ tea terms)
- Quick actions and status bar
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sqlite3
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import csv
import json
from datetime import datetime
import threading
import time

class TeaExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tea Collection Explorer - Enhanced Edition")
        self.root.geometry("1400x900")

        # Database connection
        self.db_path = "tea_collection.db"
        self.conn = None
        self.connect_db()

        # File paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.guide_path = os.path.join(script_dir, "tea_varieties_list.md")
        self.history_path = os.path.join(script_dir, "tea_history.md")
        self.journal_path = os.path.join(script_dir, "tea_journal.json")

        # Load journal
        self.load_journal()

        # Timer state
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_thread = None

        # Comparison state
        self.comparison_teas = []

        # Current tea
        self.current_tea = None

        # Create menu bar
        self.create_menu_bar()

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.create_database_tab()
        self.create_cultivars_tab()
        self.create_brewing_tab()
        self.create_journal_tab()
        self.create_comparison_tab()
        self.create_glossary_tab()
        self.create_guide_tab()
        self.create_history_tab()
        self.create_map_tab()

        # Style configuration
        self.configure_styles()

        # Status bar
        self.create_status_bar()

    def connect_db(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")

    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Tea Database (CSV)", command=self.export_teas_csv)
        file_menu.add_command(label="Export Tea Database (Text)", command=self.export_teas_txt)
        file_menu.add_command(label="Export Journal (JSON)", command=self.export_journal)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Tea Database", command=lambda: self.notebook.select(0))
        view_menu.add_command(label="Cultivars", command=lambda: self.notebook.select(1))
        view_menu.add_command(label="Brewing Timer", command=lambda: self.notebook.select(2))
        view_menu.add_command(label="Tea Journal", command=lambda: self.notebook.select(3))

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status()

    def update_status(self):
        """Update status bar with database stats"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM teas")
            tea_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM cultivars")
            cultivar_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM regions")
            region_count = cursor.fetchone()[0]

            journal_count = len(self.journal_entries)

            status_text = f"Database: {tea_count} teas | {cultivar_count} cultivars | {region_count} regions | Journal: {journal_count} entries"
            self.status_bar.config(text=status_text)
        except:
            self.status_bar.config(text="Ready")

    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Timer.TLabel', font=('Arial', 48, 'bold'), foreground='#2c5f2d')
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))

    # ==============================================
    # TAB CREATION METHODS
    # ==============================================

    def create_database_tab(self):
        """Create the database browser tab with enhanced search"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="🍵 Tea Database")

        # Enhanced search frame
        search_frame = ttk.Frame(db_frame)
        search_frame.pack(fill='x', padx=10, pady=10)

        # Row 1: Basic search
        row1 = ttk.Frame(search_frame)
        row1.pack(fill='x', pady=(0, 5))

        ttk.Label(row1, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(row1, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        ttk.Label(row1, text="Category:").pack(side='left', padx=5)
        self.category_var = tk.StringVar(value="All")
        self.category_combo = ttk.Combobox(row1, textvariable=self.category_var,
                                          values=["All", "White", "Green", "Oolong", "Black", "Pu-erh", "Yellow"],
                                          state='readonly', width=15)
        self.category_combo.pack(side='left', padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_search)

        ttk.Button(row1, text="Clear", command=self.clear_search).pack(side='left', padx=5)

        # Row 2: Advanced filters
        row2 = ttk.Frame(search_frame)
        row2.pack(fill='x')

        ttk.Label(row2, text="Caffeine:").pack(side='left', padx=5)
        self.caffeine_var = tk.StringVar(value="All")
        caffeine_combo = ttk.Combobox(row2, textvariable=self.caffeine_var,
                                     values=["All", "Very Low", "Low", "Medium", "High"],
                                     state='readonly', width=12)
        caffeine_combo.pack(side='left', padx=5)
        caffeine_combo.bind('<<ComboboxSelected>>', self.on_search)

        ttk.Label(row2, text="Price:").pack(side='left', padx=5)
        self.price_var = tk.StringVar(value="All")
        price_combo = ttk.Combobox(row2, textvariable=self.price_var,
                                   values=["All", "$", "$$", "$$$", "$$$$", "$$$$$"],
                                   state='readonly', width=10)
        price_combo.pack(side='left', padx=5)
        price_combo.bind('<<ComboboxSelected>>', self.on_search)

        # Main content frame
        content_frame = ttk.Frame(db_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left: Tea list
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        ttk.Label(list_frame, text="Tea Varieties", style='Header.TLabel').pack(anchor='w', pady=5)

        # Listbox with scrollbar
        list_scroll_frame = ttk.Frame(list_frame)
        list_scroll_frame.pack(fill='both', expand=True)

        self.tea_listbox = tk.Listbox(list_scroll_frame, font=('Arial', 10))
        list_scrollbar = ttk.Scrollbar(list_scroll_frame, orient='vertical', command=self.tea_listbox.yview)
        self.tea_listbox.configure(yscrollcommand=list_scrollbar.set)

        self.tea_listbox.pack(side='left', fill='both', expand=True)
        list_scrollbar.pack(side='right', fill='y')

        self.tea_listbox.bind('<<ListboxSelect>>', self.on_tea_select)
        self.tea_listbox.bind('<Double-Button-1>', self.add_to_comparison)

        self.tea_names = []

        # Right: Tea details with action buttons
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)

        # Action buttons
        actions_frame = ttk.Frame(details_frame)
        actions_frame.pack(fill='x', pady=(0, 5))

        ttk.Button(actions_frame, text="⏱️ Start Timer",
                  command=self.quick_timer).pack(side='left', padx=2)
        ttk.Button(actions_frame, text="📝 Journal",
                  command=self.quick_journal).pack(side='left', padx=2)
        ttk.Button(actions_frame, text="🔄 Compare",
                  command=self.add_to_comparison).pack(side='left', padx=2)

        ttk.Label(details_frame, text="Tea Details", style='Header.TLabel').pack(anchor='w', pady=5)

        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                      font=('Arial', 10), height=30)
        self.details_text.pack(fill='both', expand=True)

        # Configure text tags
        self.details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#2c5f2d')
        self.details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.details_text.tag_configure('value', font=('Arial', 10))

        # Load initial data
        self.load_tea_list()

    def create_cultivars_tab(self):
        """Create the cultivars browser tab"""
        cultivars_frame = ttk.Frame(self.notebook)
        self.notebook.add(cultivars_frame, text="🌱 Cultivars")

        # Header
        header_frame = ttk.Frame(cultivars_frame)
        header_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(header_frame, text="Tea Plant Cultivars & Varieties",
                 style='Title.TLabel').pack(side='left')

        ttk.Label(header_frame, text="Search:").pack(side='left', padx=(20, 5))
        self.cultivar_search_var = tk.StringVar()
        cultivar_search = ttk.Entry(header_frame, textvariable=self.cultivar_search_var, width=25)
        cultivar_search.pack(side='left', padx=5)
        cultivar_search.bind('<KeyRelease>', self.on_cultivar_search)

        ttk.Button(header_frame, text="Clear",
                  command=lambda: [self.cultivar_search_var.set(''), self.load_cultivars()]).pack(side='left', padx=5)

        # Main content
        content_frame = ttk.Frame(cultivars_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left: Cultivar list
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        ttk.Label(list_frame, text="Cultivar List", style='Header.TLabel').pack(anchor='w', pady=5)

        list_scroll = ttk.Frame(list_frame)
        list_scroll.pack(fill='both', expand=True)

        self.cultivar_listbox = tk.Listbox(list_scroll, font=('Arial', 10))
        cultivar_scrollbar = ttk.Scrollbar(list_scroll, orient='vertical', command=self.cultivar_listbox.yview)
        self.cultivar_listbox.configure(yscrollcommand=cultivar_scrollbar.set)

        self.cultivar_listbox.pack(side='left', fill='both', expand=True)
        cultivar_scrollbar.pack(side='right', fill='y')

        self.cultivar_listbox.bind('<<ListboxSelect>>', self.on_cultivar_select)
        self.cultivar_names = []

        # Right: Cultivar details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)

        ttk.Label(details_frame, text="Cultivar Details", style='Header.TLabel').pack(anchor='w', pady=5)

        self.cultivar_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                               font=('Arial', 10), height=30)
        self.cultivar_details_text.pack(fill='both', expand=True)

        self.cultivar_details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#2c5f2d')
        self.cultivar_details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.cultivar_details_text.tag_configure('value', font=('Arial', 10))

        # Load cultivars
        self.load_cultivars()

    def create_brewing_tab(self):
        """Create brewing timer tab"""
        brewing_frame = ttk.Frame(self.notebook)
        self.notebook.add(brewing_frame, text="⏱️ Brewing Timer")

        ttk.Label(brewing_frame, text="Brewing Timer", style='Title.TLabel').pack(pady=10)

        # Tea selection
        select_frame = ttk.Frame(brewing_frame)
        select_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(select_frame, text="Select Tea:").pack(side='left', padx=5)
        self.timer_tea_var = tk.StringVar()
        self.timer_tea_combo = ttk.Combobox(select_frame, textvariable=self.timer_tea_var, width=40)
        self.timer_tea_combo.pack(side='left', padx=5, fill='x', expand=True)
        self.timer_tea_combo.bind('<<ComboboxSelected>>', self.on_timer_tea_select)

        # Load tea names
        self.load_timer_tea_list()

        # Timer display
        self.timer_label = ttk.Label(brewing_frame, text="00:00", style='Timer.TLabel')
        self.timer_label.pack(pady=30)

        # Recommended time display
        rec_frame = ttk.Frame(brewing_frame)
        rec_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(rec_frame, text="Recommended:").pack(side='left', padx=5)
        self.timer_recommended = ttk.Label(rec_frame, text="Select a tea", font=('Arial', 10, 'bold'))
        self.timer_recommended.pack(side='left')

        # Timer controls
        controls_frame = ttk.Frame(brewing_frame)
        controls_frame.pack(pady=20)

        self.start_button = ttk.Button(controls_frame, text="▶ Start", command=self.start_timer,
                                       style='Action.TButton', width=12)
        self.start_button.pack(side='left', padx=5)

        self.pause_button = ttk.Button(controls_frame, text="⏸ Pause", command=self.pause_timer,
                                       width=12, state='disabled')
        self.pause_button.pack(side='left', padx=5)

        self.reset_button = ttk.Button(controls_frame, text="⏹ Reset", command=self.reset_timer,
                                       width=12)
        self.reset_button.pack(side='left', padx=5)

        # Custom time
        custom_frame = ttk.Frame(brewing_frame)
        custom_frame.pack(pady=10)

        ttk.Label(custom_frame, text="Custom Time (mm:ss):").pack(side='left', padx=5)
        self.custom_minutes = tk.StringVar(value="3")
        self.custom_seconds = tk.StringVar(value="00")

        ttk.Entry(custom_frame, textvariable=self.custom_minutes, width=5).pack(side='left', padx=2)
        ttk.Label(custom_frame, text=":").pack(side='left')
        ttk.Entry(custom_frame, textvariable=self.custom_seconds, width=5).pack(side='left', padx=2)

        ttk.Button(custom_frame, text="Set", command=self.set_custom_time).pack(side='left', padx=10)

    def create_journal_tab(self):
        """Create tea journal tab"""
        journal_frame = ttk.Frame(self.notebook)
        self.notebook.add(journal_frame, text="📝 Journal")

        # Header
        header_frame = ttk.Frame(journal_frame)
        header_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(header_frame, text="Tea Tasting Journal", style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="+ New Entry", command=self.new_journal_entry,
                  style='Action.TButton').pack(side='right', padx=5)
        ttk.Button(header_frame, text="🗑️ Delete", command=self.delete_journal_entry).pack(side='right')

        # Main content
        content_frame = ttk.Frame(journal_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left: Entry list
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        ttk.Label(list_frame, text="Journal Entries", style='Header.TLabel').pack(anchor='w', pady=5)

        list_scroll = ttk.Frame(list_frame)
        list_scroll.pack(fill='both', expand=True)

        self.journal_listbox = tk.Listbox(list_scroll, font=('Arial', 10))
        journal_scrollbar = ttk.Scrollbar(list_scroll, orient='vertical', command=self.journal_listbox.yview)
        self.journal_listbox.configure(yscrollcommand=journal_scrollbar.set)

        self.journal_listbox.pack(side='left', fill='both', expand=True)
        journal_scrollbar.pack(side='right', fill='y')

        self.journal_listbox.bind('<<ListboxSelect>>', self.on_journal_select)

        # Right: Entry details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)

        ttk.Label(details_frame, text="Entry Details", style='Header.TLabel').pack(anchor='w', pady=5)

        self.journal_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, font=('Arial', 10))
        self.journal_details_text.pack(fill='both', expand=True)

        self.journal_details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#2c5f2d')
        self.journal_details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.journal_details_text.tag_configure('value', font=('Arial', 10))
        self.journal_details_text.tag_configure('rating', font=('Arial', 12, 'bold'), foreground='#d4af37')

        # Load journal
        self.load_journal_list()

    def create_comparison_tab(self):
        """Create tea comparison tab"""
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text="🔄 Compare")

        # Header
        header_frame = ttk.Frame(comparison_frame)
        header_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(header_frame, text="Tea Comparison Tool", style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="Clear All", command=self.clear_comparison).pack(side='right')

        # Instructions
        info = ttk.Label(comparison_frame,
                        text="Double-click teas in the Tea Database tab to add them (up to 3)",
                        font=('Arial', 9, 'italic'), foreground='#666')
        info.pack(padx=10, pady=5)

        # Comparison display frame
        self.comparison_scroll = scrolledtext.ScrolledText(comparison_frame, wrap=tk.WORD, font=('Courier', 9))
        self.comparison_scroll.pack(fill='both', expand=True, padx=10, pady=10)

    def create_glossary_tab(self):
        """Create glossary tab"""
        glossary_frame = ttk.Frame(self.notebook)
        self.notebook.add(glossary_frame, text="📖 Glossary")

        # Header
        header_frame = ttk.Frame(glossary_frame)
        header_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(header_frame, text="Tea Terminology Glossary", style='Title.TLabel').pack(side='left')

        ttk.Label(header_frame, text="Search:").pack(side='left', padx=(20, 5))
        self.glossary_search_var = tk.StringVar()
        glossary_search = ttk.Entry(header_frame, textvariable=self.glossary_search_var, width=25)
        glossary_search.pack(side='left', padx=5)
        glossary_search.bind('<KeyRelease>', self.on_glossary_search)

        # Glossary content
        self.glossary_text = scrolledtext.ScrolledText(glossary_frame, wrap=tk.WORD, font=('Arial', 10))
        self.glossary_text.pack(fill='both', expand=True, padx=10, pady=10)

        self.glossary_text.tag_configure('term', font=('Arial', 11, 'bold'), foreground='#2c5f2d')
        self.glossary_text.tag_configure('definition', font=('Arial', 10))

        # Load glossary
        self.load_glossary()

    def create_guide_tab(self):
        """Create tea guide tab"""
        guide_frame = ttk.Frame(self.notebook)
        self.notebook.add(guide_frame, text="📚 Tea Guide")

        toolbar = ttk.Frame(guide_frame)
        toolbar.pack(fill='x', padx=10, pady=5)

        ttk.Label(toolbar, text="Complete Guide to Tea Varieties", style='Title.TLabel').pack(side='left')
        ttk.Button(toolbar, text="Reload", command=self.load_guide).pack(side='right')

        self.guide_text = scrolledtext.ScrolledText(guide_frame, wrap=tk.WORD, font=('Arial', 10))
        self.guide_text.pack(fill='both', expand=True, padx=10, pady=5)

        self.configure_markdown_tags(self.guide_text)
        self.load_guide()

    def create_history_tab(self):
        """Create tea history tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📜 History")

        toolbar = ttk.Frame(history_frame)
        toolbar.pack(fill='x', padx=10, pady=5)

        ttk.Label(toolbar, text="The History of Tea", style='Title.TLabel').pack(side='left')
        ttk.Button(toolbar, text="Reload", command=self.load_history).pack(side='right')

        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, font=('Arial', 10))
        self.history_text.pack(fill='both', expand=True, padx=10, pady=5)

        self.configure_markdown_tags(self.history_text)
        self.load_history()

    def create_map_tab(self):
        """Create world map tab"""
        map_frame = ttk.Frame(self.notebook)
        self.notebook.add(map_frame, text="🗺️ World Map")

        title_frame = ttk.Frame(map_frame)
        title_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(title_frame, text="Tea-Growing Regions of the World", style='Title.TLabel').pack(side='left')

        self.map_canvas = tk.Canvas(map_frame, bg='#cfe2f3')
        self.map_canvas.pack(fill='both', expand=True, padx=10, pady=5)

        info_frame = ttk.Frame(map_frame)
        info_frame.pack(fill='x', padx=10, pady=5)

        self.map_info_label = ttk.Label(info_frame, text="Click on a region to see details",
                                       font=('Arial', 10, 'italic'))
        self.map_info_label.pack(side='left')

        # Bind resize event
        self.map_canvas.bind('<Configure>', self.on_map_resize)

        # Initialize map data
        self.map_regions = []
        self.map_image = None
        self.map_photo = None

        # Create the map
        self.create_world_map()

    def configure_markdown_tags(self, text_widget):
        """Configure markdown tags"""
        text_widget.tag_configure('h1', font=('Arial', 18, 'bold'), foreground='#2c5f2d', spacing3=10, spacing1=10)
        text_widget.tag_configure('h2', font=('Arial', 16, 'bold'), foreground='#3d7c3f', spacing3=8, spacing1=8)
        text_widget.tag_configure('h3', font=('Arial', 14, 'bold'), foreground='#4a914c', spacing3=6, spacing1=6)
        text_widget.tag_configure('bold', font=('Arial', 10, 'bold'))
        text_widget.tag_configure('italic', font=('Arial', 10, 'italic'))

    # ==============================================
    # DATABASE TAB FUNCTIONS
    # ==============================================

    def load_tea_list(self, search_term='', category='All', caffeine='All', price='All'):
        """Load tea list with filters"""
        self.tea_listbox.delete(0, tk.END)
        self.tea_names = []

        try:
            cursor = self.conn.cursor()

            query = "SELECT id, name, category FROM teas WHERE 1=1"
            params = []

            if category != 'All':
                query += " AND category = ?"
                params.append(category)

            if caffeine != 'All':
                query += " AND caffeine_level LIKE ?"
                params.append(f'%{caffeine}%')

            if price != 'All':
                query += " AND price_range = ?"
                params.append(price)

            if search_term:
                query += " AND (name LIKE ? OR flavor_profile LIKE ? OR origin LIKE ?)"
                params.extend([f'%{search_term}%'] * 3)

            query += " ORDER BY category, name"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            for row in rows:
                display_name = f"{row['name']} ({row['category']})"
                self.tea_listbox.insert(tk.END, display_name)
                self.tea_names.append(row['name'])

            if rows:
                self.tea_listbox.select_set(0)
                self.on_tea_select(None)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading teas: {e}")

    def on_search(self, event=None):
        """Handle search"""
        search_term = self.search_var.get()
        category = self.category_var.get()
        caffeine = self.caffeine_var.get()
        price = self.price_var.get()
        self.load_tea_list(search_term, category, caffeine, price)

    def clear_search(self):
        """Clear all filters"""
        self.search_var.set('')
        self.category_var.set('All')
        self.caffeine_var.set('All')
        self.price_var.set('All')
        self.load_tea_list()

    def on_tea_select(self, event):
        """Handle tea selection"""
        selection = self.tea_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index < len(self.tea_names):
            tea_name = self.tea_names[index]
            self.current_tea = tea_name

            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM teas WHERE name = ?", (tea_name,))
                tea = cursor.fetchone()

                if tea:
                    self.display_tea_details(tea)

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")

    def display_tea_details(self, tea):
        """Display tea details"""
        self.details_text.delete('1.0', tk.END)

        self.details_text.insert(tk.END, f"{tea['name']}\n", 'title')
        self.details_text.insert(tk.END, f"{tea['category']} Tea\n\n", 'header')

        self.details_text.insert(tk.END, "🌍 Origin\n", 'header')
        self.details_text.insert(tk.END, f"{tea['origin']}\n\n", 'value')

        self.details_text.insert(tk.END, "⚙️ Processing\n", 'header')
        self.details_text.insert(tk.END, f"{tea['processing']}\n", 'value')
        self.details_text.insert(tk.END, f"Oxidation: {tea['oxidation']}\n\n", 'value')

        self.details_text.insert(tk.END, "👃 Flavor & Aroma\n", 'header')
        self.details_text.insert(tk.END, f"Flavor: {tea['flavor_profile']}\n", 'value')
        self.details_text.insert(tk.END, f"Aroma: {tea['aroma']}\n", 'value')
        self.details_text.insert(tk.END, f"Appearance: {tea['appearance']}\n\n", 'value')

        self.details_text.insert(tk.END, "☕ Brewing Instructions\n", 'header')
        self.details_text.insert(tk.END,
            f"Water Temperature: {tea['brew_temp_c']}°C ({tea['brew_temp_f']}°F)\n", 'value')
        self.details_text.insert(tk.END, f"Steep Time: {tea['steep_time']}\n", 'value')
        self.details_text.insert(tk.END, f"Ratio: {tea['tea_water_ratio']}\n", 'value')
        self.details_text.insert(tk.END, f"Re-infusions: Up to {tea['reinfusions']} times\n", 'value')
        self.details_text.insert(tk.END, f"Caffeine: {tea['caffeine_level']}\n\n", 'value')

        self.details_text.insert(tk.END, "💊 Health Benefits\n", 'header')
        self.details_text.insert(tk.END, f"{tea['health_benefits']}\n\n", 'value')

        self.details_text.insert(tk.END, "📜 History & Notes\n", 'header')
        self.details_text.insert(tk.END, f"{tea['history']}\n\n", 'value')

        self.details_text.insert(tk.END, "ℹ️ Additional Information\n", 'header')
        self.details_text.insert(tk.END, f"Price Range: {tea['price_range']}\n", 'value')
        if tea['cultivars']:
            self.details_text.insert(tk.END, f"Cultivars: {tea['cultivars']}\n", 'value')

    # ==============================================
    # CULTIVARS TAB FUNCTIONS
    # ==============================================

    def load_cultivars(self, search_term=''):
        """Load cultivars list"""
        self.cultivar_listbox.delete(0, tk.END)
        self.cultivar_names = []

        try:
            cursor = self.conn.cursor()

            if search_term:
                cursor.execute("""
                    SELECT name FROM cultivars
                    WHERE name LIKE ? OR characteristics LIKE ?
                    ORDER BY name
                """, (f'%{search_term}%', f'%{search_term}%'))
            else:
                cursor.execute("SELECT name FROM cultivars ORDER BY name")

            rows = cursor.fetchall()

            for row in rows:
                self.cultivar_listbox.insert(tk.END, row['name'])
                self.cultivar_names.append(row['name'])

            if rows:
                self.cultivar_listbox.select_set(0)
                self.on_cultivar_select(None)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading cultivars: {e}")

    def on_cultivar_search(self, event=None):
        """Handle cultivar search"""
        search_term = self.cultivar_search_var.get()
        self.load_cultivars(search_term)

    def on_cultivar_select(self, event):
        """Handle cultivar selection"""
        selection = self.cultivar_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index < len(self.cultivar_names):
            cultivar_name = self.cultivar_names[index]

            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM cultivars WHERE name = ?", (cultivar_name,))
                cultivar = cursor.fetchone()

                if cultivar:
                    self.display_cultivar_details(cultivar)

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")

    def display_cultivar_details(self, cultivar):
        """Display cultivar details"""
        self.cultivar_details_text.delete('1.0', tk.END)

        self.cultivar_details_text.insert(tk.END, f"{cultivar['name']}\n", 'title')
        self.cultivar_details_text.insert(tk.END, f"{cultivar['species']}\n\n", 'header')

        self.cultivar_details_text.insert(tk.END, "🌍 Origin\n", 'header')
        self.cultivar_details_text.insert(tk.END, f"Country: {cultivar['origin_country']}\n\n", 'value')

        self.cultivar_details_text.insert(tk.END, "🌱 Characteristics\n", 'header')
        self.cultivar_details_text.insert(tk.END, f"Leaf Size: {cultivar['leaf_size']}\n", 'value')
        self.cultivar_details_text.insert(tk.END, f"{cultivar['characteristics']}\n\n", 'value')

        self.cultivar_details_text.insert(tk.END, "☕ Common Uses\n", 'header')
        self.cultivar_details_text.insert(tk.END, f"{cultivar['common_uses']}\n\n", 'value')

        if cultivar['notes']:
            self.cultivar_details_text.insert(tk.END, "📝 Notes\n", 'header')
            self.cultivar_details_text.insert(tk.END, f"{cultivar['notes']}\n\n", 'value')

        # Find teas using this cultivar
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM teas WHERE cultivars LIKE ?", (f'%{cultivar["name"]}%',))
            teas = cursor.fetchall()

            if teas:
                self.cultivar_details_text.insert(tk.END, "🍵 Teas Using This Cultivar\n", 'header')
                for tea in teas:
                    self.cultivar_details_text.insert(tk.END, f"  • {tea['name']}\n", 'value')
        except:
            pass

    # ==============================================
    # BREWING TIMER FUNCTIONS
    # ==============================================

    def load_timer_tea_list(self):
        """Load tea names for timer"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM teas ORDER BY name")
            teas = [row['name'] for row in cursor.fetchall()]
            self.timer_tea_combo['values'] = teas
        except:
            pass

    def on_timer_tea_select(self, event=None):
        """Handle tea selection in timer"""
        tea_name = self.timer_tea_var.get()
        if not tea_name:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT steep_time, brew_temp_c, brew_temp_f FROM teas WHERE name = ?", (tea_name,))
            tea = cursor.fetchone()

            if tea:
                steep_time = tea['steep_time']
                self.timer_recommended.config(text=f"{steep_time} @ {tea['brew_temp_c']}°C/{tea['brew_temp_f']}°F")

                # Try to parse time
                import re
                match = re.search(r'(\d+)', steep_time)
                if match:
                    minutes = int(match.group(1))
                    if 'second' in steep_time.lower():
                        self.custom_minutes.set("0")
                        self.custom_seconds.set(str(minutes).zfill(2))
                    else:
                        self.custom_minutes.set(str(minutes))
                        self.custom_seconds.set("00")
        except:
            pass

    def start_timer(self):
        """Start timer"""
        if not self.timer_running:
            try:
                minutes = int(self.custom_minutes.get() or 0)
                seconds = int(self.custom_seconds.get() or 0)
                self.timer_seconds = minutes * 60 + seconds

                if self.timer_seconds > 0:
                    self.timer_running = True
                    self.start_button.config(state='disabled')
                    self.pause_button.config(state='normal')
                    self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
                    self.timer_thread.start()
            except ValueError:
                messagebox.showerror("Error", "Invalid time format")

    def pause_timer(self):
        """Pause timer"""
        self.timer_running = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')

    def reset_timer(self):
        """Reset timer"""
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_label.config(text="00:00")
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')

    def run_timer(self):
        """Timer thread"""
        while self.timer_running and self.timer_seconds > 0:
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.root.after(0, lambda m=minutes, s=seconds: self.timer_label.config(text=f"{m:02d}:{s:02d}"))
            time.sleep(1)
            self.timer_seconds -= 1

        if self.timer_seconds == 0 and self.timer_running:
            self.root.after(0, lambda: self.timer_label.config(text="00:00"))
            self.root.after(0, lambda: messagebox.showinfo("Timer", "🍵 Tea is ready!"))
            self.root.after(0, self.reset_timer)
            try:
                self.root.bell()
            except:
                pass

    def set_custom_time(self):
        """Set custom time"""
        try:
            minutes = int(self.custom_minutes.get() or 0)
            seconds = int(self.custom_seconds.get() or 0)
            total = minutes * 60 + seconds
            if total > 0:
                self.timer_seconds = total
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format")

    def quick_timer(self):
        """Quick start timer"""
        if self.current_tea:
            self.timer_tea_var.set(self.current_tea)
            self.on_timer_tea_select()
            self.notebook.select(2)

    # ==============================================
    # JOURNAL FUNCTIONS
    # ==============================================

    def load_journal(self):
        """Load journal from file"""
        self.journal_entries = []
        if os.path.exists(self.journal_path):
            try:
                with open(self.journal_path, 'r', encoding='utf-8') as f:
                    self.journal_entries = json.load(f)
            except:
                self.journal_entries = []

    def save_journal(self):
        """Save journal to file"""
        try:
            with open(self.journal_path, 'w', encoding='utf-8') as f:
                json.dump(self.journal_entries, f, indent=2, ensure_ascii=False)
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save journal: {e}")

    def load_journal_list(self):
        """Load journal entries"""
        self.journal_listbox.delete(0, tk.END)

        for entry in sorted(self.journal_entries, key=lambda x: x.get('date', ''), reverse=True):
            tea_name = entry.get('tea_name', 'Unknown')
            date = entry.get('date', '')
            rating = entry.get('rating', 0)
            stars = '⭐' * rating
            display = f"{date} - {tea_name} {stars}"
            self.journal_listbox.insert(tk.END, display)

    def new_journal_entry(self):
        """Create new journal entry"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Journal Entry")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()

        # Tea selection
        ttk.Label(dialog, text="Tea Name:").pack(anchor='w', padx=10, pady=(10, 0))
        tea_var = tk.StringVar()
        if self.current_tea:
            tea_var.set(self.current_tea)
        tea_combo = ttk.Combobox(dialog, textvariable=tea_var, width=50)
        tea_combo.pack(padx=10, pady=5, fill='x')

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM teas ORDER BY name")
            tea_combo['values'] = [row['name'] for row in cursor.fetchall()]
        except:
            pass

        # Rating
        ttk.Label(dialog, text="Rating:").pack(anchor='w', padx=10, pady=(10, 0))
        rating_var = tk.IntVar(value=3)
        rating_frame = ttk.Frame(dialog)
        rating_frame.pack(padx=10, pady=5)
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, text=f"{'⭐' * i}", variable=rating_var,
                           value=i).pack(side='left', padx=5)

        # Brewing details
        ttk.Label(dialog, text="Brewing Details:").pack(anchor='w', padx=10, pady=(10, 0))
        brewing_text = tk.Text(dialog, height=3, width=50)
        brewing_text.pack(padx=10, pady=5)
        brewing_text.insert('1.0', "Temperature: \nSteep time: \nInfusion #: ")

        # Notes
        ttk.Label(dialog, text="Tasting Notes:").pack(anchor='w', padx=10, pady=(10, 0))
        notes_text = scrolledtext.ScrolledText(dialog, height=10, width=50)
        notes_text.pack(padx=10, pady=5, fill='both', expand=True)

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def save_entry():
            tea_name = tea_var.get()
            if not tea_name:
                messagebox.showerror("Error", "Please select a tea")
                return

            entry = {
                'tea_name': tea_name,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'rating': rating_var.get(),
                'brewing': brewing_text.get('1.0', tk.END).strip(),
                'notes': notes_text.get('1.0', tk.END).strip()
            }

            self.journal_entries.append(entry)
            self.save_journal()
            self.load_journal_list()
            dialog.destroy()

        ttk.Button(button_frame, text="Save", command=save_entry,
                  style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)

    def on_journal_select(self, event):
        """Handle journal selection"""
        selection = self.journal_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        sorted_entries = sorted(self.journal_entries, key=lambda x: x.get('date', ''), reverse=True)
        if index < len(sorted_entries):
            entry = sorted_entries[index]
            self.display_journal_entry(entry)

    def display_journal_entry(self, entry):
        """Display journal entry"""
        self.journal_details_text.delete('1.0', tk.END)

        self.journal_details_text.insert(tk.END, f"{entry.get('tea_name', 'Unknown')}\n", 'title')

        stars = '⭐' * entry.get('rating', 0)
        self.journal_details_text.insert(tk.END, f"{stars}\n", 'rating')
        self.journal_details_text.insert(tk.END, f"{entry.get('date', '')}\n\n", 'value')

        self.journal_details_text.insert(tk.END, "☕ Brewing Details\n", 'header')
        self.journal_details_text.insert(tk.END, f"{entry.get('brewing', 'N/A')}\n\n", 'value')

        self.journal_details_text.insert(tk.END, "📝 Tasting Notes\n", 'header')
        self.journal_details_text.insert(tk.END, f"{entry.get('notes', 'N/A')}\n", 'value')

    def delete_journal_entry(self):
        """Delete selected entry"""
        selection = self.journal_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return

        if messagebox.askyesno("Confirm", "Delete this journal entry?"):
            index = selection[0]
            sorted_entries = sorted(self.journal_entries, key=lambda x: x.get('date', ''), reverse=True)
            if index < len(sorted_entries):
                entry_to_remove = sorted_entries[index]
                self.journal_entries.remove(entry_to_remove)
                self.save_journal()
                self.load_journal_list()
                self.journal_details_text.delete('1.0', tk.END)

    def quick_journal(self):
        """Quick journal entry"""
        self.notebook.select(3)
        self.new_journal_entry()

    # ==============================================
    # COMPARISON FUNCTIONS
    # ==============================================

    def add_to_comparison(self, event=None):
        """Add tea to comparison"""
        if not self.current_tea:
            messagebox.showwarning("Warning", "Please select a tea first")
            return

        if len(self.comparison_teas) >= 3:
            messagebox.showwarning("Warning", "Maximum 3 teas")
            return

        if self.current_tea not in self.comparison_teas:
            self.comparison_teas.append(self.current_tea)
            self.update_comparison_display()
            messagebox.showinfo("Added", f"Added {self.current_tea} to comparison")

    def clear_comparison(self):
        """Clear comparison"""
        self.comparison_teas = []
        self.update_comparison_display()

    def update_comparison_display(self):
        """Update comparison display"""
        self.comparison_scroll.delete('1.0', tk.END)

        if not self.comparison_teas:
            self.comparison_scroll.insert(tk.END, "No teas selected.\nDouble-click teas in database to add.\n")
            return

        try:
            cursor = self.conn.cursor()
            teas_data = []
            for tea_name in self.comparison_teas:
                cursor.execute("SELECT * FROM teas WHERE name = ?", (tea_name,))
                tea = cursor.fetchone()
                if tea:
                    teas_data.append(dict(tea))

            if not teas_data:
                return

            # Create comparison table
            self.comparison_scroll.insert(tk.END, "="*100 + "\n")
            self.comparison_scroll.insert(tk.END, "TEA COMPARISON\n")
            self.comparison_scroll.insert(tk.END, "="*100 + "\n\n")

            fields = [
                ('Name', 'name'),
                ('Category', 'category'),
                ('Origin', 'origin'),
                ('Brew Temp', lambda t: f"{t['brew_temp_c']}°C"),
                ('Steep Time', 'steep_time'),
                ('Caffeine', 'caffeine_level'),
                ('Price', 'price_range'),
            ]

            for field_name, field_key in fields:
                self.comparison_scroll.insert(tk.END, f"\n{field_name}:\n")
                self.comparison_scroll.insert(tk.END, "-" * 80 + "\n")
                for i, tea in enumerate(teas_data, 1):
                    if callable(field_key):
                        value = field_key(tea)
                    else:
                        value = tea.get(field_key, 'N/A')
                    self.comparison_scroll.insert(tk.END, f"  [{i}] {value}\n")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    # ==============================================
    # EXPORT FUNCTIONS
    # ==============================================

    def export_teas_csv(self):
        """Export to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filename:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM teas ORDER BY category, name")
            teas = cursor.fetchall()

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if teas:
                    writer = csv.DictWriter(f, fieldnames=teas[0].keys())
                    writer.writeheader()
                    for tea in teas:
                        writer.writerow(dict(tea))

            messagebox.showinfo("Success", f"Exported {len(teas)} teas to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    def export_teas_txt(self):
        """Export to text"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if not filename:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM teas ORDER BY category, name")
            teas = cursor.fetchall()

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("TEA COLLECTION EXPLORER - DATABASE EXPORT\n")
                f.write("="*80 + "\n\n")

                for tea in teas:
                    f.write(f"{tea['name']}\n")
                    f.write(f"Category: {tea['category']}\n")
                    f.write(f"Origin: {tea['origin']}\n")
                    f.write(f"Brewing: {tea['brew_temp_c']}°C for {tea['steep_time']}\n")
                    f.write(f"Flavor: {tea['flavor_profile']}\n")
                    f.write("-"*80 + "\n\n")

            messagebox.showinfo("Success", f"Exported {len(teas)} teas to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    def export_journal(self):
        """Export journal"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not filename:
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.journal_entries, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Success", f"Exported {len(self.journal_entries)} journal entries")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    # ==============================================
    # GLOSSARY FUNCTIONS
    # ==============================================

    def load_glossary(self):
        """Load tea glossary"""
        self.glossary_text.delete('1.0', tk.END)

        glossary = {
            "Oxidation": "The enzymatic process where tea leaves darken and develop flavor through exposure to oxygen. Stopped by heat in green tea, partial in oolong, complete in black tea.",
            "Gongfu Cha": "Chinese 'skill tea' brewing method using small teapot/gaiwan, high leaf-to-water ratio, and multiple short infusions.",
            "First Flush": "The first harvest of tea in spring (March-April), producing the most delicate and prized tea, especially in Darjeeling.",
            "Cultivar": "A tea plant variety cultivated for specific characteristics (e.g., Yabukita, Qing Xin, Assamica).",
            "Gaiwan": "Traditional Chinese lidded bowl used for brewing tea, typically 100-150ml capacity.",
            "Umami": "Savory, brothy flavor characteristic of high-quality Japanese green teas, especially gyokuro and matcha.",
            "Catechins": "Antioxidant compounds in tea, especially EGCG in green tea, linked to health benefits.",
            "L-theanine": "Amino acid in tea that promotes calm alertness and reduces caffeine jitters.",
            "Terroir": "Environmental factors (soil, climate, elevation) that give tea from a specific region its unique character.",
            "Withering": "First step in tea processing where fresh leaves lose moisture, becoming pliable.",
            "Rolling": "Process of twisting/rolling tea leaves to break cell walls and release enzymes for oxidation.",
            "Firing": "Applying heat to stop oxidation and dry tea leaves.",
            "CTC": "Crush-Tear-Curl method of processing black tea for tea bags, producing small uniform granules.",
            "Orthodox": "Traditional hand-processing method producing whole or broken leaf tea (opposite of CTC).",
            "Pu-erh": "Aged Chinese tea from Yunnan, either raw (sheng) or fermented (shou).",
            "Yancha": "Rock tea from Wuyi Mountains, known for mineral 'rock rhyme' (yan yun) character.",
            "Shading": "Covering tea plants before harvest to increase chlorophyll and L-theanine (gyokuro, matcha).",
            "Men Huan": "Yellowing process unique to yellow tea, creating mellow, sweet flavor.",
            "Astringency": "Drying, puckering sensation from tannins in tea, reduced with proper brewing.",
            "Golden Tips": "Young tea buds covered in golden downy hairs, indicating high quality.",
            "Reinfusion": "Steeping the same leaves multiple times, common in gongfu brewing.",
            "Muscatel": "Wine-like, grape flavor characteristic of Darjeeling second flush.",
            "Tribute Tea": "Premium tea historically reserved for emperors, now indicates highest grade.",
            "Single Origin": "Tea from one estate, garden, or specific region.",
            "Flush": "Harvest period or season for tea picking.",
            "Liquor": "The brewed tea liquid (not alcoholic).",
            "Infusion": "The act of steeping tea or the resulting liquid.",
        }

        for term in sorted(glossary.keys()):
            self.glossary_text.insert(tk.END, f"{term}\n", 'term')
            self.glossary_text.insert(tk.END, f"{glossary[term]}\n\n", 'definition')

    def on_glossary_search(self, event=None):
        """Search glossary"""
        search_term = self.glossary_search_var.get().lower()

        self.glossary_text.tag_remove('highlight', '1.0', tk.END)

        if search_term:
            start_pos = '1.0'
            while True:
                pos = self.glossary_text.search(search_term, start_pos, tk.END, nocase=True)
                if not pos:
                    break
                end_pos = f"{pos}+{len(search_term)}c"
                self.glossary_text.tag_add('highlight', pos, end_pos)
                start_pos = end_pos

            self.glossary_text.tag_configure('highlight', background='yellow')

    # ==============================================
    # GUIDE AND HISTORY FUNCTIONS
    # ==============================================

    def load_guide(self):
        """Load tea guide"""
        self.guide_text.delete('1.0', tk.END)

        try:
            if Path(self.guide_path).exists():
                with open(self.guide_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.render_markdown(self.guide_text, content)
            else:
                self.guide_text.insert(tk.END, "Tea guide file not found.\n")
                self.guide_text.insert(tk.END, f"Expected: {self.guide_path}")
        except Exception as e:
            self.guide_text.insert(tk.END, f"Error loading guide: {e}")

    def load_history(self):
        """Load tea history"""
        self.history_text.delete('1.0', tk.END)

        try:
            if Path(self.history_path).exists():
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.render_markdown(self.history_text, content)
            else:
                self.history_text.insert(tk.END, "Tea history file not found.\n")
                self.history_text.insert(tk.END, f"Expected: {self.history_path}")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error loading history: {e}")

    def render_markdown(self, text_widget, markdown_content):
        """Simple markdown rendering"""
        lines = markdown_content.split('\n')

        for line in lines:
            if line.startswith('# '):
                text_widget.insert(tk.END, line[2:] + '\n', 'h1')
            elif line.startswith('## '):
                text_widget.insert(tk.END, line[3:] + '\n', 'h2')
            elif line.startswith('### '):
                text_widget.insert(tk.END, line[4:] + '\n', 'h3')
            elif '**' in line:
                self.insert_formatted_line(text_widget, line, '**', 'bold')
            elif '*' in line and '**' not in line:
                self.insert_formatted_line(text_widget, line, '*', 'italic')
            else:
                text_widget.insert(tk.END, line + '\n')

    def insert_formatted_line(self, text_widget, line, marker, tag):
        """Insert formatted line"""
        parts = line.split(marker)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                text_widget.insert(tk.END, part)
            else:
                text_widget.insert(tk.END, part, tag)
        text_widget.insert(tk.END, '\n')

    # ==============================================
    # MAP FUNCTIONS
    # ==============================================

    def get_world_map_image(self, width, height):
        """Get a world map image - download if needed, or create one"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        map_file = os.path.join(script_dir, "world_map_bg.png")

        # Check if we already have a downloaded map
        if os.path.exists(map_file):
            try:
                img = Image.open(map_file)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                print("✓ Loaded existing world_map_bg.png")
                return img
            except Exception as e:
                print(f"Error loading existing map: {e}")

        # Try multiple download sources
        download_sources = [
            {
                'url': 'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73909/world.topo.bathy.200412.3x5400x2700.jpg',
                'name': 'NASA Blue Marble'
            },
            {
                'url': 'https://upload.wikimedia.org/wikipedia/commons/8/83/Equirectangular_projection_SW.jpg',
                'name': 'Wikimedia Equirectangular'
            },
            {
                'url': 'https://raw.githubusercontent.com/nvkelso/natural-earth-raster/master/50m_rasters/HYP_50M_SR/HYP_50M_SR.png',
                'name': 'Natural Earth Raster'
            }
        ]

        for source in download_sources:
            try:
                import urllib.request

                print(f"Trying to download world map from {source['name']}...")

                # Create request with proper headers to avoid 403
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                }
                req = urllib.request.Request(source['url'], headers=headers)

                with urllib.request.urlopen(req, timeout=15) as response:
                    with open(map_file, 'wb') as out_file:
                        out_file.write(response.read())

                img = Image.open(map_file)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
                img.save(map_file)  # Save resized version
                print(f"✓ World map downloaded successfully from {source['name']}!")
                return img

            except Exception as e:
                print(f"  Failed to download from {source['name']}: {e}")
                continue

        print("Could not download from any source.")
        print("Creating custom world map with GeoPandas...")

        # Fallback: Create world map using GeoPandas
        return self.create_geopandas_world_map(width, height, map_file)

    def create_geopandas_world_map(self, width, height, save_path):
        """Create a world map using GeoPandas with manually defined geometries"""
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            import geopandas as gpd
            from shapely.geometry import Polygon

            print("Creating world map with GeoPandas...")

            # Define detailed continent polygons (longitude, latitude)
            continents_data = {
                'Asia': [
                    (26, 40), (35, 45), (45, 42), (55, 48), (75, 50), (90, 55),
                    (105, 50), (115, 48), (125, 53), (135, 48), (145, 50), (150, 45),
                    (145, 40), (142, 35), (138, 30), (130, 20), (125, 10), (120, 5),
                    (105, 0), (100, -5), (95, -10), (92, -8), (85, -5), (78, 0),
                    (68, 8), (60, 15), (55, 25), (48, 28), (42, 32), (35, 36), (26, 40)
                ],
                'Europe': [
                    (-10, 36), (-5, 43), (0, 48), (10, 50), (15, 54), (25, 58),
                    (30, 65), (28, 70), (20, 68), (10, 64), (5, 60), (0, 56),
                    (-5, 51), (-8, 46), (-10, 40), (-10, 36)
                ],
                'Africa': [
                    (-18, 28), (-10, 32), (10, 37), (25, 32), (35, 30), (40, 25),
                    (42, 15), (50, 12), (52, 5), (48, -5), (42, -10), (40, -15),
                    (35, -25), (30, -32), (22, -35), (18, -34), (12, -32),
                    (8, -28), (5, -20), (0, -10), (-5, 0), (-8, 10), (-12, 18),
                    (-15, 24), (-18, 28)
                ],
                'North America': [
                    (-170, 65), (-160, 68), (-145, 70), (-130, 70), (-110, 72),
                    (-95, 70), (-80, 68), (-70, 62), (-60, 50), (-65, 45),
                    (-75, 42), (-80, 38), (-85, 35), (-95, 30), (-105, 28),
                    (-110, 22), (-115, 18), (-105, 15), (-100, 18), (-95, 20),
                    (-88, 18), (-85, 15), (-82, 10), (-79, 8), (-95, 15),
                    (-110, 25), (-120, 32), (-125, 40), (-132, 52), (-145, 60),
                    (-160, 62), (-170, 65)
                ],
                'South America': [
                    (-80, 10), (-75, 8), (-70, 0), (-65, -5), (-60, -10),
                    (-55, -18), (-50, -25), (-45, -20), (-42, -15), (-38, -8),
                    (-35, 0), (-35, 5), (-40, 8), (-50, 10), (-60, 8),
                    (-70, 5), (-75, -2), (-78, -10), (-75, -20), (-70, -30),
                    (-68, -40), (-70, -48), (-72, -54), (-68, -55), (-58, -52),
                    (-52, -45), (-48, -35), (-46, -25), (-48, -15), (-52, -8),
                    (-58, -3), (-65, 0), (-72, 3), (-80, 10)
                ],
                'Australia': [
                    (113, -10), (125, -12), (135, -15), (142, -18), (148, -24),
                    (152, -32), (153, -38), (148, -42), (142, -40), (135, -36),
                    (128, -32), (120, -28), (115, -22), (112, -15), (113, -10)
                ],
                'Antarctica': [
                    (-180, -65), (-90, -68), (0, -70), (90, -68), (180, -65),
                    (180, -85), (-180, -85), (-180, -65)
                ]
            }

            # Create GeoDataFrame
            geometries = []
            names = []
            for name, coords in continents_data.items():
                geometries.append(Polygon(coords))
                names.append(name)

            world = gpd.GeoDataFrame({'name': names, 'geometry': geometries})

            # Create figure with exact dimensions
            dpi = 100
            figsize = (width/dpi, height/dpi)
            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

            # Plot the world map
            world.plot(
                ax=ax,
                color='#b8d4a8',
                edgecolor='#5a8a5a',
                linewidth=0.8,
                alpha=0.92
            )

            # Set ocean color (background)
            ax.set_facecolor('#d4e8f7')
            fig.patch.set_facecolor('#d4e8f7')

            # Remove axis ticks and labels
            ax.set_xticks([])
            ax.set_yticks([])

            # Remove the axis frame
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Set proper extent for equirectangular projection
            ax.set_xlim(-180, 180)
            ax.set_ylim(-90, 90)

            # Adjust layout to remove whitespace
            plt.tight_layout(pad=0)

            # Save to file
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight', pad_inches=0, facecolor='#d4e8f7')
            plt.close(fig)

            # Load the saved image and ensure exact size
            img = Image.open(save_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(save_path)

            print(f"✓ GeoPandas world map created successfully!")
            return img

        except ImportError as e:
            print(f"GeoPandas not available: {e}")
            print("Falling back to basic custom map...")
            return self.create_custom_world_map(width, height)
        except Exception as e:
            print(f"Error creating GeoPandas map: {e}")
            import traceback
            traceback.print_exc()
            print("Falling back to basic custom map...")
            return self.create_custom_world_map(width, height)

    def create_custom_world_map(self, width, height):
        """Create a custom world map with better continent shapes"""
        img = Image.new('RGB', (width, height), color='#d4e8f7')
        draw = ImageDraw.Draw(img)

        # More detailed continent outlines
        # Asia
        asia_points = [
            (width*0.55, height*0.15), (width*0.85, height*0.15),
            (width*0.90, height*0.25), (width*0.87, height*0.35),
            (width*0.82, height*0.42), (width*0.77, height*0.45),
            (width*0.70, height*0.45), (width*0.65, height*0.48),
            (width*0.60, height*0.52), (width*0.55, height*0.50),
            (width*0.52, height*0.45), (width*0.50, height*0.35),
            (width*0.52, height*0.25), (width*0.55, height*0.15)
        ]
        draw.polygon(asia_points, fill='#b8d4a8', outline='#5a8a5a', width=2)

        # Europe
        europe_points = [
            (width*0.45, height*0.20), (width*0.52, height*0.18),
            (width*0.54, height*0.22), (width*0.52, height*0.28),
            (width*0.48, height*0.30), (width*0.44, height*0.28),
            (width*0.43, height*0.24), (width*0.45, height*0.20)
        ]
        draw.polygon(europe_points, fill='#c8d8b8', outline='#6a9a6a', width=2)

        # Africa
        africa_points = [
            (width*0.47, height*0.33), (width*0.54, height*0.32),
            (width*0.56, height*0.38), (width*0.57, height*0.50),
            (width*0.55, height*0.65), (width*0.52, height*0.70),
            (width*0.48, height*0.72), (width*0.45, height*0.68),
            (width*0.44, height*0.58), (width*0.43, height*0.48),
            (width*0.45, height*0.38), (width*0.47, height*0.33)
        ]
        draw.polygon(africa_points, fill='#d8c8a8', outline='#8a7a5a', width=2)

        # North America
        na_points = [
            (width*0.15, height*0.20), (width*0.28, height*0.18),
            (width*0.32, height*0.25), (width*0.30, height*0.35),
            (width*0.25, height*0.42), (width*0.20, height*0.45),
            (width*0.15, height*0.42), (width*0.12, height*0.35),
            (width*0.13, height*0.25), (width*0.15, height*0.20)
        ]
        draw.polygon(na_points, fill='#b8d4b8', outline='#5a8a6a', width=2)

        # South America
        sa_points = [
            (width*0.24, height*0.48), (width*0.30, height*0.47),
            (width*0.32, height*0.52), (width*0.31, height*0.62),
            (width*0.28, height*0.72), (width*0.25, height*0.75),
            (width*0.22, height*0.72), (width*0.21, height*0.62),
            (width*0.22, height*0.52), (width*0.24, height*0.48)
        ]
        draw.polygon(sa_points, fill='#b8d4c8', outline='#5a8a7a', width=2)

        # Australia
        australia_points = [
            (width*0.72, height*0.60), (width*0.82, height*0.58),
            (width*0.85, height*0.62), (width*0.84, height*0.68),
            (width*0.80, height*0.72), (width*0.75, height*0.73),
            (width*0.71, height*0.70), (width*0.70, height*0.64),
            (width*0.72, height*0.60)
        ]
        draw.polygon(australia_points, fill='#d8c8b8', outline='#8a7a6a', width=2)

        return img

    def create_world_map(self):
        """Create the interactive world map"""
        width = 1200
        height = 600

        # Try to get a world map image
        img = self.get_world_map_image(width, height)

        draw = ImageDraw.Draw(img)

        # Load tea regions from database
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM regions")
            regions = cursor.fetchall()

            # Plot tea regions
            for region in regions:
                # Convert lat/long to pixel coordinates (simplified projection)
                x = int((region['longitude'] + 180) * (width / 360))
                y = int((90 - region['latitude']) * (height / 180))

                # Draw marker with a larger, more visible design
                marker_size = 12

                # Draw outer glow/shadow for visibility
                for offset in range(4, 0, -1):
                    alpha = int(60 - offset * 10)
                    shadow_color = (0, 0, 0, alpha)
                    # Create temporary RGBA image for shadow
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    shadow_draw = ImageDraw.Draw(shadow_layer)
                    shadow_draw.ellipse([x-marker_size-offset, y-marker_size-offset,
                                        x+marker_size+offset, y+marker_size+offset],
                                       fill=(196, 69, 54, alpha))
                    img = Image.alpha_composite(img, shadow_layer)

                # Convert back to RGB for drawing
                img = img.convert('RGB')
                draw = ImageDraw.Draw(img)

                # Draw main marker (pin shape with border)
                # Outer border (white for contrast)
                draw.ellipse([x-marker_size-2, y-marker_size-2, x+marker_size+2, y+marker_size+2],
                           fill='white', outline='white')
                # Main pin body (red)
                draw.ellipse([x-marker_size, y-marker_size, x+marker_size, y+marker_size],
                           fill='#c44536', outline='#8b2e20', width=3)
                # Pin highlight (lighter red for 3D effect)
                draw.ellipse([x-marker_size//2, y-marker_size//2,
                            x+marker_size//2, y+marker_size//2],
                           fill='#e85544')

                # Store region data
                self.map_regions.append({
                    'name': region['name'],
                    'country': region['country'],
                    'x': x,
                    'y': y,
                    'radius': marker_size + 4,
                    'data': dict(region)
                })

        except sqlite3.Error as e:
            print(f"Error loading regions: {e}")

        # Add title and legend with backgrounds for visibility
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            try:
                # Try alternative font paths (for macOS)
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
                small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()

        # Title with background
        title_text = "Major Tea-Growing Regions of the World"
        title_bbox = draw.textbbox((0, 0), title_text, font=font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        title_x = width//2 - title_width//2
        title_y = 15

        # Draw semi-transparent background for title
        padding = 10
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        title_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        title_bg_draw = ImageDraw.Draw(title_bg)
        title_bg_draw.rectangle([title_x - padding, title_y - padding,
                                 title_x + title_width + padding, title_y + title_height + padding],
                                fill=(255, 255, 255, 220), outline=(44, 95, 45, 255), width=3)
        img = Image.alpha_composite(img, title_bg)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)

        draw.text((title_x, title_y), title_text, fill='#2c5f2d', font=font)

        # Legend with background
        legend_x = 40
        legend_y = height - 60
        legend_text = " = Tea-growing region (click for details)"
        legend_bbox = draw.textbbox((0, 0), legend_text, font=small_font)
        legend_width = legend_bbox[2] - legend_bbox[0]
        legend_height = legend_bbox[3] - legend_bbox[1]

        # Draw background for legend
        img = img.convert('RGBA')
        legend_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        legend_bg_draw = ImageDraw.Draw(legend_bg)
        legend_bg_draw.rectangle([legend_x - 10, legend_y - 10,
                                  legend_x + 30 + legend_width + 10, legend_y + legend_height + 10],
                                 fill=(255, 255, 255, 200), outline=(90, 138, 90, 255), width=2)
        img = Image.alpha_composite(img, legend_bg)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)

        # Draw legend marker
        draw.ellipse([legend_x, legend_y + 2, legend_x + 16, legend_y + 18],
                    fill='#c44536', outline='#8b2e20', width=2)
        draw.ellipse([legend_x + 4, legend_y + 6, legend_x + 12, legend_y + 14],
                    fill='#e85544')

        # Draw legend text
        draw.text((legend_x + 25, legend_y), legend_text, fill='#2c5f2d', font=small_font)

        self.map_image = img
        self.display_map()

    def display_map(self):
        """Display the map on canvas"""
        if self.map_image:
            # Get canvas size
            canvas_width = self.map_canvas.winfo_width()
            canvas_height = self.map_canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                # Resize image to fit canvas while maintaining aspect ratio
                img_width, img_height = self.map_image.size
                scale = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)

                resized_img = self.map_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.map_photo = ImageTk.PhotoImage(resized_img)

                # Clear canvas and display image
                self.map_canvas.delete('all')
                self.map_canvas.create_image(canvas_width//2, canvas_height//2,
                                            image=self.map_photo, anchor='center')

                # Update clickable regions coordinates
                self.scale_factor = scale
                self.map_offset_x = (canvas_width - new_width) // 2
                self.map_offset_y = (canvas_height - new_height) // 2

                # Bind events
                self.map_canvas.bind('<Button-1>', self.on_map_click)
                self.map_canvas.bind('<Motion>', self.on_map_hover)

    def on_map_resize(self, event):
        """Handle map canvas resize"""
        self.root.after(100, self.display_map)

    def on_map_click(self, event):
        """Handle map click"""
        # Convert canvas coordinates to image coordinates
        img_x = (event.x - self.map_offset_x) / self.scale_factor
        img_y = (event.y - self.map_offset_y) / self.scale_factor

        # Check if click is on a region
        for region in self.map_regions:
            dist = ((img_x - region['x'])**2 + (img_y - region['y'])**2)**0.5
            if dist <= region['radius'] + 5:
                self.show_region_details(region)
                break

    def on_map_hover(self, event):
        """Handle mouse hover on map"""
        # Convert canvas coordinates to image coordinates
        img_x = (event.x - self.map_offset_x) / self.scale_factor
        img_y = (event.y - self.map_offset_y) / self.scale_factor

        # Check if hovering over a region
        for region in self.map_regions:
            dist = ((img_x - region['x'])**2 + (img_y - region['y'])**2)**0.5
            if dist <= region['radius'] + 5:
                self.map_canvas.config(cursor='hand2')
                self.map_info_label.config(text=f"{region['name']}, {region['country']}")
                return

        self.map_canvas.config(cursor='')
        self.map_info_label.config(text="Click on a region to see details")

    def show_region_details(self, region):
        """Show detailed information about a tea region"""
        data = region['data']

        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title(f"{data['name']}, {data['country']}")
        popup.geometry("600x500")

        # Title
        title_label = ttk.Label(popup, text=f"{data['name']}", style='Title.TLabel')
        title_label.pack(pady=10)

        # Details
        details_frame = ttk.Frame(popup)
        details_frame.pack(fill='both', expand=True, padx=20, pady=10)

        details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, font=('Arial', 10))
        details_text.pack(fill='both', expand=True)

        # Add information
        details_text.insert(tk.END, f"Country: {data['country']}\n\n", 'bold')
        details_text.insert(tk.END, f"Location\n", 'header')
        details_text.insert(tk.END, f"Latitude: {data['latitude']}°\n")
        details_text.insert(tk.END, f"Longitude: {data['longitude']}°\n")
        details_text.insert(tk.END, f"Elevation: {data['elevation_min']}-{data['elevation_max']} meters\n\n")

        details_text.insert(tk.END, f"Climate\n", 'header')
        details_text.insert(tk.END, f"{data['climate']}\n\n")

        details_text.insert(tk.END, f"Famous Teas\n", 'header')
        details_text.insert(tk.END, f"{data['famous_teas']}\n\n")

        details_text.insert(tk.END, f"Description\n", 'header')
        details_text.insert(tk.END, f"{data['description']}\n")

        # Configure tags
        details_text.tag_configure('bold', font=('Arial', 12, 'bold'))
        details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#2c5f2d')

        details_text.config(state='disabled')

        # Close button
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

        # Find related teas
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM teas WHERE origin_region LIKE ? LIMIT 5",
                         (f"%{data['name']}%",))
            teas = cursor.fetchall()

            if teas:
                details_text.config(state='normal')
                details_text.insert(tk.END, f"\nTeas from this region:\n", 'header')
                for tea in teas:
                    details_text.insert(tk.END, f"  • {tea['name']}\n")
                details_text.config(state='disabled')
        except sqlite3.Error:
            pass

    # ==============================================
    # UTILITY FUNCTIONS
    # ==============================================

    def show_about(self):
        """Show about dialog"""
        about_text = """Tea Collection Explorer - Enhanced Edition
Version 2.0

Features:
• 49 authentic tea varieties
• 26 tea plant cultivars
• Brewing timer with alerts
• Tea tasting journal
• Comparison tool
• Enhanced search
• Export functionality
• Complete glossary

Database corrections and enhancements
January 2026
        """
        messagebox.showinfo("About", about_text)

    def __del__(self):
        """Cleanup when app closes"""
        if self.conn:
            self.conn.close()


def main():
    """Run the Tea Collection Explorer"""
    root = tk.Tk()
    app = TeaExplorerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
