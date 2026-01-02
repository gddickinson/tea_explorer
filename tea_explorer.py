"""
Tea Collection Explorer - Main GUI Application
A comprehensive tea database browser with guides and interactive map
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from pathlib import Path
import webbrowser
import tempfile
import markdown
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class TeaExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tea Collection Explorer")
        self.root.geometry("1200x800")
        
        # Database connection
        self.db_path = "tea_collection.db"
        self.conn = None
        self.connect_db()
        
        # Markdown files paths - relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.guide_path = os.path.join(script_dir, "tea_varieties_list.md")
        self.history_path = os.path.join(script_dir, "tea_history.md")
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_database_tab()
        self.create_guide_tab()
        self.create_history_tab()
        self.create_map_tab()
        
        # Style configuration
        self.configure_styles()
    
    def connect_db(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
    
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    
    def create_database_tab(self):
        """Create the database browser tab"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="Tea Database")
        
        # Search frame
        search_frame = ttk.Frame(db_frame)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Label(search_frame, text="Category:").pack(side='left', padx=5)
        self.category_var = tk.StringVar(value="All")
        self.category_combo = ttk.Combobox(search_frame, textvariable=self.category_var, 
                                          values=["All", "White", "Green", "Oolong", "Black", "Pu-erh", "Yellow"],
                                          state='readonly', width=15)
        self.category_combo.pack(side='left', padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_search)
        
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side='left', padx=5)
        
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
        
        # Dictionary to map listbox index to tea name
        self.tea_names = []
        
        # Right: Tea details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)
        
        ttk.Label(details_frame, text="Tea Details", style='Header.TLabel').pack(anchor='w', pady=5)
        
        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, 
                                                      font=('Arial', 10), height=30)
        self.details_text.pack(fill='both', expand=True)
        
        # Configure text tags for formatting
        self.details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#2c5f2d')
        self.details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.details_text.tag_configure('value', font=('Arial', 10))
        
        # Load initial data
        self.load_tea_list()
    
    def create_guide_tab(self):
        """Create the tea guide tab"""
        guide_frame = ttk.Frame(self.notebook)
        self.notebook.add(guide_frame, text="Tea Guide")
        
        # Toolbar
        toolbar = ttk.Frame(guide_frame)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(toolbar, text="Complete Guide to Tea Varieties", 
                 style='Title.TLabel').pack(side='left')
        ttk.Button(toolbar, text="Reload", command=self.load_guide).pack(side='right')
        
        # Text widget
        self.guide_text = scrolledtext.ScrolledText(guide_frame, wrap=tk.WORD, 
                                                   font=('Arial', 10))
        self.guide_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Configure tags
        self.configure_markdown_tags(self.guide_text)
        
        # Load guide
        self.load_guide()
    
    def create_history_tab(self):
        """Create the tea history tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="Tea History")
        
        # Toolbar
        toolbar = ttk.Frame(history_frame)
        toolbar.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(toolbar, text="The History of Tea", 
                 style='Title.TLabel').pack(side='left')
        ttk.Button(toolbar, text="Reload", command=self.load_history).pack(side='right')
        
        # Text widget
        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, 
                                                     font=('Arial', 10))
        self.history_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Configure tags
        self.configure_markdown_tags(self.history_text)
        
        # Load history
        self.load_history()
    
    def create_map_tab(self):
        """Create the interactive world map tab"""
        map_frame = ttk.Frame(self.notebook)
        self.notebook.add(map_frame, text="World Map")
        
        # Title
        title_frame = ttk.Frame(map_frame)
        title_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(title_frame, text="Tea-Growing Regions of the World", 
                 style='Title.TLabel').pack(side='left')
        
        # Map canvas
        self.map_canvas = tk.Canvas(map_frame, bg='white')
        self.map_canvas.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Info panel
        info_frame = ttk.Frame(map_frame)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        self.map_info_label = ttk.Label(info_frame, text="Click on a region to see details", 
                                       font=('Arial', 10, 'italic'))
        self.map_info_label.pack(side='left')
        
        # Bind resize event
        self.map_canvas.bind('<Configure>', self.on_map_resize)
        
        # Store map data
        self.map_regions = []
        self.map_image = None
        self.map_photo = None
        
        # Create the map
        self.create_world_map()
    
    def configure_markdown_tags(self, text_widget):
        """Configure tags for markdown-style formatting"""
        text_widget.tag_configure('h1', font=('Arial', 18, 'bold'), foreground='#2c5f2d', 
                                 spacing3=10, spacing1=10)
        text_widget.tag_configure('h2', font=('Arial', 16, 'bold'), foreground='#3d7c3f', 
                                 spacing3=8, spacing1=8)
        text_widget.tag_configure('h3', font=('Arial', 14, 'bold'), foreground='#4a914c', 
                                 spacing3=6, spacing1=6)
        text_widget.tag_configure('bold', font=('Arial', 10, 'bold'))
        text_widget.tag_configure('italic', font=('Arial', 10, 'italic'))
        text_widget.tag_configure('code', font=('Courier', 9), background='#f5f5f5')
    
    def get_world_map_image(self, width, height):
        """Get a world map image - download if needed, or create one"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        map_file = os.path.join(script_dir, "world_map_bg.png")
        
        # Check if we already have a downloaded map
        if os.path.exists(map_file):
            try:
                img = Image.open(map_file)
                img = img.resize((width, height), Image.Resampling.LANCZOS)
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
            # Using more realistic shapes based on major landmasses
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
        # Using equirectangular projection coordinates
        
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
        
        # Add ocean color variations for depth
        for i in range(5):
            alpha = int(20 - i*3)
            overlay = Image.new('RGBA', (width, height), (70, 130, 180, alpha))
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        return img
    
    def load_tea_list(self, search_term='', category='All'):
        """Load tea list from database"""
        self.tea_listbox.delete(0, tk.END)
        self.tea_names = []  # Clear the names list
        
        try:
            cursor = self.conn.cursor()
            
            if category == 'All':
                if search_term:
                    cursor.execute("""
                        SELECT id, name, category FROM teas 
                        WHERE name LIKE ? OR flavor_profile LIKE ? OR origin_region LIKE ?
                        ORDER BY category, name
                    """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                else:
                    cursor.execute("SELECT id, name, category FROM teas ORDER BY category, name")
            else:
                if search_term:
                    cursor.execute("""
                        SELECT id, name, category FROM teas 
                        WHERE category = ? AND (name LIKE ? OR flavor_profile LIKE ? OR origin_region LIKE ?)
                        ORDER BY name
                    """, (category, f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                else:
                    cursor.execute("""
                        SELECT id, name, category FROM teas 
                        WHERE category = ?
                        ORDER BY name
                    """, (category,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                display_name = f"{row['name']} ({row['category']})"
                self.tea_listbox.insert(tk.END, display_name)
                # Store the tea name in our list
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
        self.load_tea_list(search_term, category)
    
    def clear_search(self):
        """Clear search and reload all teas"""
        self.search_var.set('')
        self.category_var.set('All')
        self.load_tea_list()
    
    def on_tea_select(self, event):
        """Handle tea selection"""
        selection = self.tea_listbox.curselection()
        if not selection:
            return
        
        # Get the tea name from our stored list
        index = selection[0]
        if index < len(self.tea_names):
            tea_name = self.tea_names[index]
            
            # Load tea details
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM teas WHERE name = ?", (tea_name,))
                tea = cursor.fetchone()
                
                if tea:
                    self.display_tea_details(tea)
            
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error loading tea details: {e}")
    
    def display_tea_details(self, tea):
        """Display detailed information about a tea"""
        self.details_text.delete('1.0', tk.END)
        
        # Title
        self.details_text.insert(tk.END, f"{tea['name']}\n", 'title')
        self.details_text.insert(tk.END, f"{tea['category']} Tea\n\n", 'header')
        
        # Origin
        self.details_text.insert(tk.END, "Origin\n", 'header')
        self.details_text.insert(tk.END, f"Country: {tea['origin_country']}\n", 'value')
        self.details_text.insert(tk.END, f"Region: {tea['origin_region']}\n\n", 'value')
        
        # Processing
        self.details_text.insert(tk.END, "Processing\n", 'header')
        self.details_text.insert(tk.END, f"Method: {tea['processing_method']}\n", 'value')
        self.details_text.insert(tk.END, f"Oxidation: {tea['oxidation_level']}\n\n", 'value')
        
        # Flavor & Aroma
        self.details_text.insert(tk.END, "Flavor & Aroma\n", 'header')
        self.details_text.insert(tk.END, f"Flavor: {tea['flavor_profile']}\n", 'value')
        self.details_text.insert(tk.END, f"Aroma: {tea['aroma']}\n", 'value')
        self.details_text.insert(tk.END, f"Appearance: {tea['appearance']}\n\n", 'value')
        
        # Brewing
        self.details_text.insert(tk.END, "Brewing Instructions\n", 'header')
        self.details_text.insert(tk.END, 
            f"Water Temperature: {tea['water_temp_celsius']}°C ({tea['water_temp_fahrenheit']}°F)\n", 'value')
        self.details_text.insert(tk.END, 
            f"Steep Time: {tea['steep_time_min']}-{tea['steep_time_max']} minutes\n", 'value')
        self.details_text.insert(tk.END, f"Ratio: {tea['tea_to_water_ratio']}\n", 'value')
        self.details_text.insert(tk.END, f"Re-infusions: Up to {tea['reinfusions']} times\n", 'value')
        self.details_text.insert(tk.END, f"Caffeine: {tea['caffeine_level']}\n\n", 'value')
        
        # Health Benefits
        self.details_text.insert(tk.END, "Health Benefits\n", 'header')
        self.details_text.insert(tk.END, f"{tea['health_benefits']}\n\n", 'value')
        
        # History
        self.details_text.insert(tk.END, "History & Notes\n", 'header')
        self.details_text.insert(tk.END, f"{tea['history']}\n\n", 'value')
        
        # Additional Info
        self.details_text.insert(tk.END, "Additional Information\n", 'header')
        self.details_text.insert(tk.END, f"Best Time: {tea['best_time']}\n", 'value')
        self.details_text.insert(tk.END, f"Price Range: {tea['price_range']}\n", 'value')
        if tea['notable_cultivars']:
            self.details_text.insert(tk.END, f"Notable Cultivars: {tea['notable_cultivars']}\n", 'value')
    
    def load_guide(self):
        """Load the tea guide markdown file"""
        self.guide_text.delete('1.0', tk.END)
        
        try:
            if Path(self.guide_path).exists():
                with open(self.guide_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.render_markdown(self.guide_text, content)
            else:
                self.guide_text.insert(tk.END, "Tea guide file not found.\n")
                self.guide_text.insert(tk.END, f"Expected location: {self.guide_path}")
        except Exception as e:
            self.guide_text.insert(tk.END, f"Error loading guide: {e}")
    
    def load_history(self):
        """Load the tea history markdown file"""
        self.history_text.delete('1.0', tk.END)
        
        try:
            if Path(self.history_path).exists():
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.render_markdown(self.history_text, content)
            else:
                self.history_text.insert(tk.END, "Tea history file not found.\n")
                self.history_text.insert(tk.END, f"Expected location: {self.history_path}")
        except Exception as e:
            self.history_text.insert(tk.END, f"Error loading history: {e}")
    
    def render_markdown(self, text_widget, markdown_content):
        """Simple markdown rendering in text widget"""
        lines = markdown_content.split('\n')
        
        for line in lines:
            # Headers
            if line.startswith('# '):
                text_widget.insert(tk.END, line[2:] + '\n', 'h1')
            elif line.startswith('## '):
                text_widget.insert(tk.END, line[3:] + '\n', 'h2')
            elif line.startswith('### '):
                text_widget.insert(tk.END, line[4:] + '\n', 'h3')
            # Bold
            elif '**' in line:
                self.insert_formatted_line(text_widget, line, '**', 'bold')
            # Italic
            elif '*' in line and '**' not in line:
                self.insert_formatted_line(text_widget, line, '*', 'italic')
            # Code
            elif '`' in line:
                self.insert_formatted_line(text_widget, line, '`', 'code')
            else:
                text_widget.insert(tk.END, line + '\n')
    
    def insert_formatted_line(self, text_widget, line, marker, tag):
        """Insert a line with inline formatting"""
        parts = line.split(marker)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                text_widget.insert(tk.END, part)
            else:
                text_widget.insert(tk.END, part, tag)
        text_widget.insert(tk.END, '\n')
    
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
        
        # Draw semi-transparent background for title using alpha compositing
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
        
        # Draw background for legend using alpha compositing
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
                
                # Bind click event
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
    
    def __del__(self):
        """Cleanup when app closes"""
        if self.conn:
            self.conn.close()

def main():
    """Main entry point"""
    # Initialize database first
    import tea_database
    db = tea_database.TeaDatabase()
    db.initialize_database()
    
    # Create and run GUI
    root = tk.Tk()
    app = TeaExplorerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
