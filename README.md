# Tea Collection Explorer

A Python-based GUI application for exploring tea varieties, brewing methods, history, tea-growing regions, and **tea manufacturers** around the world.

## Features

### 1. **Tea Database Browser**
- Browse 24+ meticulously documented tea varieties
- Search by name, category, flavor profile, or region
- Filter by tea category (White, Green, Oolong, Black, Pu-erh, Yellow)
- View detailed information including:
  - Origin (country and specific region)
  - Processing methods and oxidation levels
  - Flavor profiles and aroma descriptions
  - Precise brewing instructions (temperature, time, ratios)
  - Health benefits backed by research
  - Historical context and interesting facts
  - Price ranges and notable cultivars

### 2. **Tea Brands Database** (NEW!)
- Browse 28+ global tea manufacturers and brands
- Search by company name, country, market segment, or certifications
- Filter by:
  - Country of origin (UK, USA, Japan, India, Sri Lanka, etc.)
  - Market segment (mass-market, premium, specialty, luxury)
  - Certifications (Organic, Fairtrade, B Corp, Royal Warrant, etc.)
- View detailed company information:
  - Company history and founding year
  - Parent company and ownership
  - Headquarters location
  - Certifications and sustainability credentials
- Browse 117+ tea products with details on:
  - Tea type and category
  - Bag type (pyramid, round, loose-leaf, etc.)
  - Pricing in multiple currencies (GBP, USD, EUR, AUD)
  - Countries where available
  - Organic and Fair Trade status
  - Special features

### 3. **Tea Guide Viewer**
- Complete reference guide to tea varieties
- Organized by category with detailed descriptions
- Includes over 200 named varieties
- Processing methods and cultivation information

### 3. **Tea History Timeline**
- Detailed history from 2737 BCE to present
- Stories of legendary origins
- Lu Yu and the Classic of Tea
- Spread to Japan, Korea, and Europe
- Boston Tea Party and the Opium Wars
- Robert Fortune's tea espionage
- Development of Indian and Ceylon tea industries
- Modern tea culture and global industry

### 4. **Interactive World Map**
- Visual representation of major tea-growing regions
- 12 documented regions across Asia
- Clickable markers for detailed region information
- Geographic coordinates and elevation data
- Climate information and famous teas from each region

## Installation & Requirements

### Requirements
- Python 3.7 or higher
- Required packages:
  - tkinter (usually included with Python)
  - sqlite3 (usually included with Python)
  - Pillow (PIL)
  - markdown

### Installation

1. **Ensure Python packages are installed:**
   ```bash
   pip install Pillow markdown
   ```

2. **Files included:**
   - `tea_database.py` - Database creation and management
   - `tea_explorer.py` - Main GUI application
   - `tea_collection.db` - SQLite database (auto-created)
   - `run_tea_explorer.py` - Application launcher
   - `tea_varieties_list.md` - Complete tea varieties guide
   - `tea_history.md` - Detailed tea history

## Running the Application

### Option 1: Using the launcher (recommended)
```bash
python3 run_tea_explorer.py
```

### Option 2: Direct execution
```bash
python3 tea_explorer.py
```

The application will:
1. Initialize the database if needed
2. Load all tea data and manufacturer information
3. Open the GUI with multiple tabs

## Using the Application

### Tea Database Tab
1. **Browse** all teas in the left panel
2. **Search** using the search box at the top
3. **Filter** by category using the dropdown
4. **Click** on any tea to see detailed information
5. **Clear** search to reset filters

### Tea Brands Tab (NEW!)
1. **Browse** 28+ tea manufacturers worldwide
2. **Search** by company name
3. **Filter** by:
   - Country of origin
   - Market segment (mass-market, premium, specialty, luxury)
   - Certifications (Organic, Fairtrade, B Corp, etc.)
4. **Click** on any company to see:
   - Company details (history, headquarters, certifications)
   - Complete product catalog (117+ products)
5. **Filter products** by name or tea type
6. **Click** on any product to see detailed pricing and availability

### Tea Guide Tab
- Automatically loads the complete tea varieties guide
- Scroll through comprehensive information
- Click "Reload" to refresh if needed

### Tea History Tab
- Displays the complete history of tea
- From ancient origins to modern industry
- Click "Reload" to refresh if needed

### World Map Tab
- **Hover** over red markers to see region names
- **Click** markers to open detailed information window
- View coordinates, elevation, climate, and famous teas
- See which teas come from each region

## Database Structure

### Teas Table
Contains detailed information about each tea variety including:
- Name, category, origin
- Processing and oxidation
- Flavor, aroma, appearance
- Brewing parameters
- Health benefits and history
- Cultivar information

### Regions Table
Geographic and climate data for tea-growing regions:
- Location coordinates
- Elevation ranges
- Climate descriptions
- Famous teas from each region

### Companies Table (NEW!)
Tea manufacturers and brands worldwide:
- Company name and parent company
- Founded year and headquarters
- Country of origin
- Website and certifications
- Market segment (mass-market, premium, specialty, luxury)
- Company description

### Products Table (NEW!)
Complete product catalog for each manufacturer:
- Product name and company
- Tea type and category
- Bag type (pyramid, round, loose-leaf, etc.)
- Format and quantity
- Price and currency
- Countries available
- Organic and Fair Trade status
- Special features

### Distribution Table (NEW!)
Distribution and availability information:
- Company and country
- Distribution type (retail, online, wholesale, hospitality)
- Retailers and channels

## Customization

### Adding New Teas
Edit `tea_database.py` and add entries to the `teas_data` list in the `populate_teas()` method.

### Adding New Companies
Edit `tea_database.py` and add entries to the `companies_data` list in the `populate_companies()` method.

### Adding New Products
Edit `tea_database.py` and add entries to the `products_data` list in the `populate_products()` method.

### Adding New Regions
Edit `tea_database.py` and add entries to the `regions_data` list in the `populate_regions()` method.

### Modifying the Map
The world map is generated in `create_world_map()` method in `tea_explorer.py`. You can:
- Adjust marker sizes
- Change colors
- Add more geographic features
- Modify clickable region definitions

## Keyboard Shortcuts

- **Tab Navigation**: Ctrl+Tab (Windows/Linux) or Cmd+Tab (Mac)
- **Search Box**: Start typing to search immediately
- **Clear Search**: Click "Clear" button or delete search text

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
rm tea_collection.db
python3 tea_database.py
```

### Missing Markdown Files
Ensure `tea_varieties_list.md` and `tea_history.md` are in the same directory or update the paths in `tea_explorer.py`:
```python
self.guide_path = "path/to/tea_varieties_list.md"
self.history_path = "path/to/tea_history.md"
```

### Display Issues
- Ensure your screen resolution is at least 1200x800
- The application is resizable - adjust window size as needed
- Map regions scale automatically with window size

## Technical Details

### Database: SQLite3
- Lightweight, file-based database
- No server required
- Fast queries for tea varieties and regions

### GUI Framework: Tkinter
- Cross-platform (Windows, Mac, Linux)
- Native look and feel
- Included with Python

### Image Processing: Pillow (PIL)
- Generates interactive world map
- Handles image scaling and display
- Creates clickable regions

### Markdown Rendering
- Simple custom renderer for text display
- Supports headers, bold, italic, code blocks
- Fast and lightweight

## Tea Categories in Database

- **White Tea**: 4 varieties (Silver Needle, White Peony, Moonlight White, etc.)
- **Green Tea**: 8 varieties (Gyokuro, Sencha, Matcha, Longjing, etc.)
- **Oolong Tea**: 4 varieties (Tie Guan Yin, High Mountain, Da Hong Pao, etc.)
- **Black Tea**: 6 varieties (Darjeeling, Assam, Keemun, Lapsang Souchong, etc.)
- **Pu-erh Tea**: 2 types (Sheng/Raw, Shou/Ripe)
- **Yellow Tea**: 1 variety (Junshan Yinzhen)

## Geographic Regions Covered

- **China**: Fujian, Yunnan, Zhejiang, Anhui
- **Japan**: Uji, Shizuoka
- **India**: Darjeeling, Assam, Nilgiri
- **Sri Lanka**: Nuwara Eliya, Kandy
- **Taiwan**: High Mountain regions

## Future Enhancements

Potential improvements for future versions:
- Export tea database to CSV/Excel
- Print tea information
- Tea brewing timer
- Personal tea journal/tasting notes
- More detailed maps with topography
- Photos of tea varieties
- Vendor recommendations
- Price comparisons

## Credits

**Database Content**: Compiled from extensive research including:
- Lu Yu's Classic of Tea
- Historical tea trade documents
- Modern scientific research on tea health benefits
- Tea master interviews and expert sources

**Application Development**: Built with Python, Tkinter, SQLite, and Pillow

## License

This application is provided for educational and personal use.

Tea data compiled from public domain sources and general knowledge.
Historical information synthesized from multiple sources.

---

**Version**: 1.0
**Last Updated**: January 2026

Enjoy exploring the wonderful world of tea! 🍵
