# Tea Collection Explorer - Enhanced Edition v2.1

A Python-based GUI application for exploring tea varieties, **tea blends**, brewing methods, history, tea-growing regions, **tea manufacturers**, and **herbal tisanes** from around the world.

## 🆕 What's New in v2.1

### Tea Blends & Flavoured Teas Database
- **26 popular tea blends** from around the world
- Categories include:
  - Traditional British blends (English Breakfast, Earl Grey, Irish Breakfast)
  - Chai & spiced teas (Masala Chai, Chocolate Chai)
  - Fruity & floral blends (Peach Tea, Rose Tea, Jasmine Pearl)
  - Dessert blends (Chocolate Mint, Vanilla Caramel)
  - Seasonal blends (Christmas Tea, Gingerbread)
  - Wellness blends (Detox Tea, Sleep & Relaxation)
  - Asian-inspired blends (Genmaicha, Thai Tea)
- Comprehensive information for each blend:
  - Base tea and ingredients
  - Flavor profiles and brewing instructions
  - Caffeine levels and health benefits
  - History and cultural significance
  - Popular brands offering each blend
  - Serving suggestions
- Advanced search and filtering:
  - By category, caffeine level, or origin
  - Full-text search across all blend attributes
- Integration with brewing timer and tea journal
- Export blends database to CSV

## Features

### 1. **Tea Database Browser**
- Browse 49+ meticulously documented tea varieties
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

### 2. **Tea Blends Browser** 🆕
- Browse 26+ popular tea blends and flavoured teas
- Search by name, ingredients, or popular brands
- Filter by:
  - Category (Flavoured Black, Traditional Blend, Spiced, etc.)
  - Caffeine level (None to Very High)
  - Origin region (England, India, Japan, Modern blends, etc.)
- View comprehensive blend information:
  - Base tea and complete ingredient list
  - Detailed flavor profiles and aromas
  - Precise brewing parameters
  - Caffeine content and health benefits
  - Historical background and cultural context
  - Popular brands that produce each blend
  - Serving suggestions and food pairings
- Quick actions:
  - Start brewing timer with blend's recommended time
  - Add blend to your tea journal
  - Export blends database to CSV

### 3. **Tea Cultivars Database**
- Browse 26+ tea plant cultivars
- Information on:
  - Species (Camellia sinensis var. sinensis/assamica)
  - Origin country and characteristics
  - Common uses and growing notes

### 4. **Tea Brands Database**
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

### 5. **Tisanes & Herbal Teas Database**
- Comprehensive database of 45+ herbal teas from global traditions
- Browse herbs from:
  - Western Herbalism
  - Traditional Chinese Medicine (TCM)
  - Ayurveda
  - African traditions
  - South American traditions
  - Middle Eastern traditions
  - Indigenous cultures
- Search and filter by:
  - Tradition/origin
  - Caffeine content
  - Safety level
- View detailed information for each tisane:
  - Scientific name and plant family
  - Traditional uses and research-backed benefits
  - Active compounds and properties
  - **Prominent safety information** including:
    - Risk level assessment
    - Pregnancy/nursing safety
    - Contraindications
    - Drug interactions
    - Maximum dosages
  - TCM and Ayurvedic properties where applicable
  - Brewing instructions and flavor profiles
  - Cultural significance
- Browse 19+ tisane manufacturers worldwide
- Safety warnings clearly displayed with color coding

### 6. **Brewing Timer**
- Set custom brewing times
- Visual and audio alerts
- Pre-populated with recommended times from selected teas/blends
- Perfect steep every time

### 7. **Tea Journal**
- Record tasting notes with ratings (1-5 stars)
- Track brewing parameters
- Date-stamped entries
- Export journal to JSON
- Quick-add from any tea or blend selection

### 8. **Tea Comparison Tool**
- Compare up to 3 teas side-by-side
- View differences in:
  - Processing and origin
  - Flavor profiles
  - Brewing parameters
  - Caffeine levels
  - Price ranges

### 9. **Tea Guide Viewer**
- Complete reference guide to tea varieties
- Organized by category with detailed descriptions
- Includes over 200 named varieties
- Processing methods and cultivation information

### 10. **Tea History Timeline**
- Detailed history from 2737 BCE to present
- Stories of legendary origins
- Lu Yu and the Classic of Tea
- Spread to Japan, Korea, and Europe
- Boston Tea Party and the Opium Wars
- Robert Fortune's tea espionage
- Development of Indian and Ceylon tea industries
- Modern tea culture and global industry

### 11. **Interactive World Map**
- Visual representation of major tea-growing regions
- 12 documented regions across Asia
- Clickable markers for detailed region information
- Geographic coordinates and elevation data
- Climate information and famous teas from each region

### 12. **Tea Glossary**
- 30+ essential tea terms
- Clear definitions and context
- Searchable reference

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
   - `tea_explorer.py` - Main GUI application
   - `blends_database.py` - Blends database initialization (optional)
   - `tea_collection.db` - SQLite database (includes blends table)
   - `tisane_collection.db` - Tisane database
   - `run_tea_explorer.py` - Application launcher
   - `tea_varieties_list.md` - Complete tea varieties guide
   - `tea_history.md` - Detailed tea history
   - `tea_journal.json` - Tea journal data
   - `README.md` - This file

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
2. Load all tea data, blends, and manufacturer information
3. Open the GUI with multiple tabs

## Using the Application

### Tea Database Tab
1. **Browse** all teas in the left panel
2. **Search** using the search box at the top
3. **Filter** by category using the dropdown
4. **Click** on any tea to see detailed information
5. **Clear** search to reset filters

### Tea Blends Tab 🆕
1. **Browse** 26+ popular tea blends
2. **Search** by blend name, ingredients, or brands
3. **Filter** by:
   - Category (Traditional Blend, Flavoured, Spiced, etc.)
   - Caffeine level (None, Low, Medium, High, Very High)
   - Origin region (England, India, Modern blend, etc.)
4. **Click** on any blend to see:
   - Complete ingredient list and base tea
   - Detailed flavor profiles and brewing instructions
   - Historical background and cultural significance
   - Popular brands that make this blend
   - Serving suggestions and pairings
5. **Quick Actions**:
   - 🫖 **Start Brewing Timer** - Automatically sets recommended brewing time
   - 📝 **Add to Journal** - Pre-fills journal entry with blend details
   - 📤 **Export Blends** - Save blends database to CSV

### Cultivars Tab
1. **Browse** tea plant varieties
2. **Search** by name or species
3. **View** detailed cultivation information

### Tea Brands Tab
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

### Tisanes Tab
1. **Browse** 45+ herbal teas from global traditions
2. **Search** by name or traditional uses
3. **Filter** by:
   - Tradition (Western Herbalism, TCM, Ayurveda, African, etc.)
   - Caffeine content (None, Low, Contains Caffeine)
   - Safety level (Generally Safe, Use with Caution, High Risk)
4. **Click** on any tisane to see:
   - Complete botanical and traditional information
   - **Safety warnings** prominently displayed
   - TCM and Ayurvedic properties
   - Research-backed benefits
   - Brewing instructions
   - Cultural significance
5. **View Manufacturers** button to browse 19+ tisane companies
6. **Safety indicators** in the list:
   - ⚠️ = High risk herbs
   - ⚡ = Use with caution

### Brewing Timer Tab
1. **Select tea/blend** or enter custom name
2. **Set minutes and seconds**
3. **Click "Start Timer"**
4. **Wait for alert** when brewing is complete

### Tea Journal Tab
1. **Enter tea/blend name** or select from recent entries
2. **Add brewing details** (temperature, steep time, infusion number)
3. **Rate your experience** (1-5 stars)
4. **Write tasting notes**
5. **Save entry** to journal
6. **Export** journal to JSON file

### Comparison Tool Tab
1. **Search and add** up to 3 teas to compare
2. **View side-by-side** information
3. **Clear comparison** to start over

### Glossary Tab
1. **Browse** 30+ tea terms
2. **Search** for specific terms
3. **Learn** tea vocabulary

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

### Tea Collection Database (tea_collection.db)

#### Teas Table
Contains detailed information about each tea variety

#### Blends Table 🆕
Contains detailed information about tea blends:
- Blend name, category, base tea
- Complete ingredient lists
- Flavor profiles and aromas
- Brewing parameters (temperature, time)
- Caffeine levels
- Health benefits
- Origin and historical background
- Popular brands
- Serving suggestions

#### Cultivars Table
Tea plant variety information

#### Regions Table
Geographic and climate data for tea-growing regions

#### Companies Table
Tea manufacturers and brands worldwide

#### Products Table
Complete product catalog for each manufacturer

#### Distribution Table
Distribution and availability information

### Tisane Collection Database (tisane_collection.db)

#### Tisanes Table
Comprehensive herbal tea information

#### Safety Info Table
Critical safety information for each tisane

#### Manufacturers Table (Tisanes)
Herbal tea and tisane manufacturers

#### Plant Families Table
Information about botanical families

#### Regions Table (Tisanes)
Geographic data for herb cultivation

#### Traditional Systems Table
Information about herbal medicine traditions

## Customization

### Adding New Blends
Edit `blends_database.py` and add entries to the `blends_data` list in the `populate_blends()` method. Then run:
```bash
python3 blends_database.py
```

### Adding New Teas
Edit the database directly or create your own population script following the existing pattern.

### Adding New Companies/Products
Edit the database directly or extend the companies/products tables.

## Keyboard Shortcuts

- **Tab Navigation**: Ctrl+Tab (Windows/Linux) or Cmd+Tab (Mac)
- **Search Box**: Start typing to search immediately
- **Clear Search**: Click "Clear" button or delete search text

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
rm tea_collection.db
python3 blends_database.py
```

### Missing Files
Ensure all markdown and database files are in the same directory as `tea_explorer.py`.

### Display Issues
- Ensure your screen resolution is at least 1200x800
- The application is resizable - adjust window size as needed
- Map regions scale automatically with window size

## Technical Details

### Database: SQLite3
- Lightweight, file-based database
- No server required
- Fast queries for teas, blends, and regions

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

## Database Statistics

- **Tea Varieties**: 49 authentic teas
- **Tea Blends**: 26 popular blends
- **Cultivars**: 26 tea plant varieties
- **Tea Brands**: 28+ manufacturers
- **Products**: 117+ tea products
- **Tisanes**: 45+ herbal teas
- **Regions**: 12 major tea-growing areas
- **Glossary Terms**: 30+ definitions

## Tea Blend Categories

- **Traditional Black Blends**: English Breakfast, Irish Breakfast, Scottish Breakfast
- **Flavoured Black Teas**: Earl Grey, Lady Grey, Peach Tea, Strawberry, Mango
- **Spiced Teas**: Masala Chai, Chai Latte, Chocolate Chai, Gingerbread
- **Floral Blends**: Rose Tea, Jasmine Pearl
- **Mint Blends**: Moroccan Mint, Chocolate Mint
- **Berry Blends**: Wild Berry Blast, Passion Fruit
- **Citrus Blends**: Lemon Ginger
- **Dessert Blends**: Vanilla Caramel, Chocolate flavours
- **Wellness Blends**: Detox Tea, Sleep & Relaxation
- **Asian Blends**: Genmaicha, Thai Tea
- **Seasonal Blends**: Christmas Tea
- **Smoky Blends**: Russian Caravan

## Future Enhancements

Potential improvements for future versions:
- More tea blends (regional specialties, modern fusion blends)
- Blend recipe creator (create your own custom blends)
- Vendor price comparison for blends
- Tea pairing recommendations (food & tea)
- Blend of the day/week feature
- Integration with tea suppliers' APIs
- Advanced blend search (by ingredient, flavor notes)
- Blend popularity ratings and reviews
- Photos of tea blends
- Tea brewing technique videos

## Credits

**Database Content**: Compiled from extensive research including:
- Lu Yu's Classic of Tea
- Historical tea trade documents
- Modern scientific research on tea health benefits
- Tea master interviews and expert sources
- Traditional blend recipes from around the world
- Tea manufacturer websites and product information

**Application Development**: Built with Python, Tkinter, SQLite, and Pillow

## Version History

- **v2.1** (January 2026) - Added Tea Blends database and browser with 26 popular blends
- **v2.0** (January 2026) - Added Brands, Tisanes, Cultivars, Journal, Comparison, and enhanced features
- **v1.0** - Initial release with tea database, history, and map

## License

This application is provided for educational and personal use.

Tea and blend data compiled from public domain sources and general knowledge.
Historical information synthesized from multiple sources.

---

**Version**: 2.1  
**Last Updated**: January 2026

Enjoy exploring the wonderful world of tea and tea blends! 🫖☕🍵

## Support

If you encounter any issues or have suggestions for new blends to add, please provide feedback through the application or contact the developers.

Happy brewing! 🫖
