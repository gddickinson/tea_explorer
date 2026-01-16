"""
Database Initialization Script
Creates the database schema for Tea Collection Explorer
"""

import sqlite3
from pathlib import Path


def create_tea_database(db_path: str = 'tea_collection.db'):
    """
    Create and initialize tea database with schema and sample data
    
    Args:
        db_path: Path to database file
    """
    print(f"Creating database at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create teas table
    print("Creating 'teas' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teas (
            tea_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            origin_country TEXT,
            origin_region TEXT,
            processing_method TEXT,
            oxidation_level TEXT,
            flavor_profile TEXT,
            aroma TEXT,
            appearance TEXT,
            brew_temp_c INTEGER,
            brew_temp_f INTEGER,
            steep_time TEXT,
            caffeine_level TEXT,
            health_benefits TEXT,
            history TEXT,
            cultural_significance TEXT
        )
    """)
    
    # Create blends table
    print("Creating 'blends' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blends (
            blend_id INTEGER PRIMARY KEY AUTOINCREMENT,
            blend_name TEXT NOT NULL,
            category TEXT,
            base_tea TEXT,
            ingredients TEXT,
            flavor_profile TEXT,
            aroma TEXT,
            appearance TEXT,
            brew_temp_c INTEGER,
            brew_temp_f INTEGER,
            steep_time TEXT,
            caffeine_level TEXT,
            description TEXT
        )
    """)
    
    # Insert sample teas
    print("Inserting sample tea data...")
    sample_teas = [
        ('Sencha', 'Green', 'Japan', 'Shizuoka', None, 'Unoxidized',
         'Fresh, grassy, slightly sweet', 'Fresh cut grass, oceanic', 'Bright green',
         70, 158, '1-2 minutes', 'Medium', 'Antioxidants, boosts metabolism',
         'Popular everyday tea in Japan', None),
        
        ('Dragonwell (Longjing)', 'Green', 'China', 'Zhejiang', 'Pan-fired', 'Unoxidized',
         'Sweet, nutty, vegetal', 'Chestnut, fresh beans', 'Flat, jade green leaves',
         75, 167, '2-3 minutes', 'Low to Medium', 'Rich in antioxidants, calming',
         'One of China\'s most famous teas, named after Dragon Well village', 'Imperial tribute tea'),
        
        ('Gyokuro', 'Green', 'Japan', None, 'Shade-grown', 'Unoxidized',
         'Sweet, umami-rich, delicate', 'Marine, sweet grass', 'Dark green, needle-like',
         50, 122, '2 minutes', 'High', 'High in L-theanine, relaxing yet focusing',
         'Premium Japanese tea, shade-grown for 3 weeks before harvest', None),
        
        ('Silver Needle (Bai Hao Yin Zhen)', 'White', 'China', 'Fujian', 'Minimal processing', 'Minimal',
         'Delicate, sweet, subtle', 'Light floral, honey', 'Silvery-white buds',
         75, 167, '3-5 minutes', 'Very Low', 'Antioxidants, gentle on stomach',
         'Made only from unopened buds, highest grade of white tea', None),
        
        ('Tie Guan Yin', 'Oolong', 'China', 'Fujian', 'Partially oxidized', '30-40%',
         'Floral, creamy, orchid-like', 'Orchid, honey', 'Tightly rolled green-brown',
         90, 194, '3-4 minutes', 'Medium', 'Aids digestion, promotes relaxation',
         'Named after the Iron Goddess of Mercy', 'One of China\'s famous oolongs'),
        
        ('Da Hong Pao', 'Oolong', 'China', 'Wuyi Mountains', 'Roasted', '60-70%',
         'Rich, mineral, roasted', 'Roasted nuts, stone fruit', 'Dark, twisted leaves',
         95, 203, '3-5 minutes', 'Medium', 'Metabolism boost, antioxidants',
         'Big Red Robe - legendary Wuyi rock tea', 'Imperial tribute tea'),
        
        ('Keemun', 'Black', 'China', 'Anhui', 'Fully oxidized', 'Fully oxidized',
         'Winey, fruity, slight smokiness', 'Orchid, pine, dried fruit', 'Dark, twisted',
         90, 194, '3-4 minutes', 'Medium to High', 'Energy boost, heart health',
         'Famous Anhui black tea, used in English Breakfast blends', None),
        
        ('Darjeeling First Flush', 'Black', 'India', 'Darjeeling', 'Orthodox', 'Lightly oxidized',
         'Floral, fruity, muscatel', 'Floral, grape', 'Light, golden liquor',
         85, 185, '3-4 minutes', 'Medium', 'Antioxidants, gentle stimulant',
         'Champagne of teas, harvested in spring', 'Protected designation of origin'),
        
        ('Ceylon', 'Black', 'Sri Lanka', None, 'Orthodox', 'Fully oxidized',
         'Brisk, citrusy, slightly astringent', 'Citrus, spice', 'Bright, coppery',
         90, 194, '3-5 minutes', 'Medium to High', 'Energy, antioxidants',
         'Sri Lankan tea, formerly Ceylon', None),
        
        ('Pu-erh (Shou/Ripe)', 'Pu-erh', 'China', 'Yunnan', 'Fermented', 'Post-fermented',
         'Earthy, smooth, woody', 'Forest floor, earth', 'Dark red-brown',
         95, 203, '3-5 minutes', 'Medium', 'Aids digestion, reduces cholesterol',
         'Aged and fermented tea, improves with time', 'Traditional digestive aid'),
    ]
    
    cursor.executemany("""
        INSERT INTO teas (
            name, category, origin_country, origin_region, processing_method,
            oxidation_level, flavor_profile, aroma, appearance,
            brew_temp_c, brew_temp_f, steep_time, caffeine_level,
            health_benefits, history, cultural_significance
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_teas)
    
    # Insert sample blends
    print("Inserting sample blend data...")
    sample_blends = [
        ('Earl Grey', 'Black', 'Black tea', 'Black tea, bergamot oil',
         'Citrusy, floral, bold', 'Bergamot, citrus', 'Dark liquor',
         90, 194, '3-4 minutes', 'Medium',
         'Classic British blend with bergamot flavoring'),
        
        ('English Breakfast', 'Black', 'Black tea', 'Assam, Ceylon, Keemun blend',
         'Full-bodied, malty, robust', 'Malty, sweet', 'Rich amber',
         95, 203, '4-5 minutes', 'High',
         'Traditional British morning blend, strong enough for milk'),
        
        ('Jasmine Pearl', 'Green', 'Green tea', 'Green tea, jasmine flowers',
         'Floral, sweet, delicate', 'Jasmine blossoms', 'Light yellow-green',
         75, 167, '2-3 minutes', 'Low to Medium',
         'Hand-rolled green tea pearls scented with jasmine'),
        
        ('Moroccan Mint', 'Green', 'Green tea', 'Gunpowder green tea, spearmint',
         'Fresh, minty, sweet', 'Peppermint, green tea', 'Light green',
         80, 176, '3-5 minutes', 'Medium',
         'Traditional North African blend with spearmint'),
    ]
    
    cursor.executemany("""
        INSERT INTO blends (
            blend_name, category, base_tea, ingredients,
            flavor_profile, aroma, appearance,
            brew_temp_c, brew_temp_f, steep_time, caffeine_level,
            description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_blends)
    
    conn.commit()
    
    # Verify
    tea_count = cursor.execute("SELECT COUNT(*) FROM teas").fetchone()[0]
    blend_count = cursor.execute("SELECT COUNT(*) FROM blends").fetchone()[0]
    
    print(f"\n✓ Database created successfully!")
    print(f"✓ Inserted {tea_count} sample teas")
    print(f"✓ Inserted {blend_count} sample blends")
    print(f"\nDatabase location: {Path(db_path).absolute()}")
    
    conn.close()
    

def create_journal_file(journal_path: str = 'tea_journal.json'):
    """
    Create sample journal file
    
    Args:
        journal_path: Path to journal JSON file
    """
    import json
    from datetime import datetime, timedelta
    
    print(f"\nCreating journal file at: {journal_path}")
    
    # Sample journal entries
    sample_entries = [
        {
            'entry_id': 1,
            'tea_name': 'Sencha',
            'date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"),
            'rating': 5,
            'brewing': '70°C, 1.5 minutes',
            'notes': 'Excellent morning tea. Fresh and energizing with sweet grass notes.'
        },
        {
            'entry_id': 2,
            'tea_name': 'Dragonwell (Longjing)',
            'date': (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
            'rating': 5,
            'brewing': '75°C, 2 minutes',
            'notes': 'Beautiful chestnut flavor. Very smooth and calming.'
        },
        {
            'entry_id': 3,
            'tea_name': 'Earl Grey',
            'date': (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            'rating': 4,
            'brewing': '90°C, 3 minutes, with milk',
            'notes': 'Classic afternoon blend. Bergamot is well-balanced.'
        },
    ]
    
    with open(journal_path, 'w') as f:
        json.dump(sample_entries, f, indent=2)
    
    print(f"✓ Created journal with {len(sample_entries)} sample entries")
    print(f"Journal location: {Path(journal_path).absolute()}")


if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Tea Collection Explorer - Database Setup")
    print("=" * 60)
    print()
    
    # Get database path from command line or use default
    db_path = sys.argv[1] if len(sys.argv) > 1 else 'tea_collection.db'
    journal_path = 'tea_journal.json'
    
    # Create database
    create_tea_database(db_path)
    
    # Create journal
    create_journal_file(journal_path)
    
    print("\n" + "=" * 60)
    print("Setup Complete! 🎉")
    print("=" * 60)
    print("\nYou can now run: python main.py")
