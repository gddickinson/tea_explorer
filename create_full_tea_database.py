#!/usr/bin/env python3
"""
Comprehensive Tea Database Generator
Automatically generates database from tea varieties list
"""

import sqlite3
import os
import re

# Brewing parameters and characteristics by category
CATEGORY_DEFAULTS = {
    'White': {
        'brew_temp_c': 75,
        'brew_temp_f': 167,
        'steep_time': '3-5 minutes',
        'tea_water_ratio': '2g per 150ml',
        'reinfusions': 3,
        'oxidation': '5-15% oxidation',
        'caffeine_level': 'Low (15-30mg per cup)',
        'base_flavor': 'delicate, sweet, floral',
        'base_aroma': 'light floral, fresh, subtle',
        'appearance': 'pale golden to light amber liquor',
        'health_benefits': 'Highest antioxidants, anti-aging, immune support, skin health',
        'price_range': '$15-80 per 50g'
    },
    'Green': {
        'brew_temp_c': 80,
        'brew_temp_f': 176,
        'steep_time': '2-3 minutes',
        'tea_water_ratio': '2.5g per 150ml',
        'reinfusions': 3,
        'oxidation': '0-5% oxidation (minimal)',
        'caffeine_level': 'Medium (25-50mg per cup)',
        'base_flavor': 'fresh, vegetal, grassy, slightly astringent',
        'base_aroma': 'fresh grass, vegetal, marine',
        'appearance': 'light green to yellow-green liquor',
        'health_benefits': 'High in antioxidants, metabolism boost, heart health, mental alertness',
        'price_range': '$10-60 per 50g'
    },
    'Oolong': {
        'brew_temp_c': 95,
        'brew_temp_f': 203,
        'steep_time': '3-4 minutes',
        'tea_water_ratio': '3g per 150ml',
        'reinfusions': 5,
        'oxidation': '10-70% oxidation (varies widely)',
        'caffeine_level': 'Medium (30-50mg per cup)',
        'base_flavor': 'complex, floral to roasted, smooth',
        'base_aroma': 'floral, fruity, or roasted depending on oxidation',
        'appearance': 'golden to amber liquor',
        'health_benefits': 'Antioxidants, weight management, heart health, bone strength',
        'price_range': '$15-100 per 50g'
    },
    'Black': {
        'brew_temp_c': 95,
        'brew_temp_f': 203,
        'steep_time': '3-5 minutes',
        'tea_water_ratio': '2.5g per 150ml',
        'reinfusions': 2,
        'oxidation': '85-100% oxidation (fully oxidized)',
        'caffeine_level': 'High (40-70mg per cup)',
        'base_flavor': 'malty, robust, full-bodied, brisk',
        'base_aroma': 'malt, honey, fruit, wood',
        'appearance': 'deep amber to dark brown liquor',
        'health_benefits': 'Heart health, alertness, antioxidants, digestive support',
        'price_range': '$8-50 per 50g'
    },
    'Pu-erh': {
        'brew_temp_c': 100,
        'brew_temp_f': 212,
        'steep_time': '3-5 minutes',
        'tea_water_ratio': '5g per 150ml',
        'reinfusions': 8,
        'oxidation': 'Post-fermented (aged)',
        'caffeine_level': 'Medium-High (30-60mg per cup)',
        'base_flavor': 'earthy, woody, smooth, sweet',
        'base_aroma': 'earthy, forest floor, aged wood',
        'appearance': 'dark reddish-brown to black liquor',
        'health_benefits': 'Digestive aid, cholesterol management, weight loss, detoxification',
        'price_range': '$12-200+ per 50g (varies by age)'
    },
    'Yellow': {
        'brew_temp_c': 80,
        'brew_temp_f': 176,
        'steep_time': '2-3 minutes',
        'tea_water_ratio': '2.5g per 150ml',
        'reinfusions': 3,
        'oxidation': '5-10% oxidation (slightly more than green)',
        'caffeine_level': 'Medium (25-45mg per cup)',
        'base_flavor': 'mellow, sweet, smooth, less grassy than green',
        'base_aroma': 'sweet, subtle floral, fresh',
        'appearance': 'yellow to golden liquor',
        'health_benefits': 'Antioxidants, digestive health, similar to green tea benefits',
        'price_range': '$20-100 per 50g'
    },
    'Scented': {
        'brew_temp_c': 85,
        'brew_temp_f': 185,
        'steep_time': '3-4 minutes',
        'tea_water_ratio': '2.5g per 150ml',
        'reinfusions': 2,
        'oxidation': 'Varies by base tea',
        'caffeine_level': 'Varies (depends on base tea)',
        'base_flavor': 'floral, fragrant, sweet, base tea character',
        'base_aroma': 'strong floral or fruit scent',
        'appearance': 'varies by base tea',
        'health_benefits': 'Depends on base tea plus aromatherapy benefits',
        'price_range': '$10-50 per 50g'
    }
}

# Regional characteristics
REGIONAL_CHARACTERISTICS = {
    'Fujian, China': {
        'description': 'Historic tea region, birthplace of white tea and oolong',
        'climate': 'Subtropical monsoon'
    },
    'Zhejiang, China': {
        'description': 'Famous for Dragon Well and other premium green teas',
        'climate': 'Humid subtropical'
    },
    'Anhui, China': {
        'description': 'Yellow Mountain region, premium green and black teas',
        'climate': 'Humid subtropical'
    },
    'Yunnan, China': {
        'description': 'Ancient tea forests, birthplace of tea, pu-erh heartland',
        'climate': 'Subtropical highland'
    },
    'Sichuan, China': {
        'description': 'High altitude tea production, yellow and green teas',
        'climate': 'Subtropical monsoon'
    },
    'Guangdong, China': {
        'description': 'Phoenix Mountain region, famous for Dan Cong oolongs',
        'climate': 'Tropical monsoon'
    },
    'Taiwan': {
        'description': 'High mountain oolongs, innovative processing',
        'climate': 'Subtropical mountain'
    },
    'Japan': {
        'description': 'Precision steaming, shade-grown teas, unique cultivars',
        'climate': 'Humid subtropical'
    },
    'India': {
        'description': 'Colonial tea estates, diverse terroirs, orthodox and CTC processing',
        'climate': 'Varies: tropical to highland'
    },
    'Sri Lanka': {
        'description': 'Ceylon teas, elevation-based quality gradations',
        'climate': 'Tropical highland'
    },
    'Nepal': {
        'description': 'Himalayan teas, similar to Darjeeling character',
        'climate': 'Himalayan'
    },
    'Kenya': {
        'description': 'Large-scale CTC production, some orthodox specialty teas',
        'climate': 'Tropical highland'
    }
}

def parse_tea_varieties_list(filepath='tea_varieties_list.md'):
    """Parse the tea varieties markdown file and extract all varieties"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    varieties = []
    current_category = None
    current_subcategory = None
    current_region = None
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Main category headers
        if line.startswith('## ') and not line.startswith('###'):
            category_text = line[3:].strip()
            
            if 'WHITE' in category_text:
                current_category = 'White'
            elif 'GREEN' in category_text:
                current_category = 'Green'
            elif 'OOLONG' in category_text:
                current_category = 'Oolong'
            elif 'BLACK' in category_text or 'RED TEA' in category_text:
                current_category = 'Black'
            elif 'PU-ERH' in category_text or "PU'ER" in category_text:
                current_category = 'Pu-erh'
            elif 'YELLOW' in category_text:
                current_category = 'Yellow'
            elif 'SPECIALTY' in category_text or 'SCENTED' in category_text or 'FLAVORED' in category_text:
                current_category = 'Scented'
            
            continue
        
        # Subcategory headers (### level)
        if line.startswith('###'):
            current_subcategory = line[4:].strip()
            
            # Extract region from subcategory
            if 'Chinese' in current_subcategory or 'China' in current_subcategory:
                current_region = 'China'
            elif 'Japanese' in current_subcategory or 'Japan' in current_subcategory:
                current_region = 'Japan'
            elif 'Taiwanese' in current_subcategory or 'Taiwan' in current_subcategory:
                current_region = 'Taiwan'
            elif 'Indian' in current_subcategory or 'India' in current_subcategory:
                current_region = 'India'
            elif 'Sri Lankan' in current_subcategory or 'Ceylon' in current_subcategory:
                current_region = 'Sri Lanka'
            elif 'Nepalese' in current_subcategory or 'Nepal' in current_subcategory:
                current_region = 'Nepal'
            elif 'Kenyan' in current_subcategory or 'Kenya' in current_subcategory:
                current_region = 'Kenya'
            
            continue
        
        # Individual tea varieties (lines starting with '- **')
        if line.startswith('- **') and current_category:
            # Extract tea name
            match = re.search(r'\*\*([^*]+)\*\*', line)
            if match:
                tea_name = match.group(1).strip()
                
                # Extract additional info in parentheses
                desc_match = re.search(r'\(([^)]+)\)', line)
                description_note = desc_match.group(1) if desc_match else ''
                
                # Determine origin
                origin = determine_origin(tea_name, current_subcategory, current_region, description_note)
                
                varieties.append({
                    'name': tea_name,
                    'category': current_category,
                    'subcategory': current_subcategory,
                    'origin': origin,
                    'description_note': description_note
                })
    
    return varieties

def determine_origin(tea_name, subcategory, region, description_note):
    """Determine the origin of a tea based on context"""
    
    # Check description for location clues
    location_map = {
        'Fujian': 'Fujian, China',
        'Yunnan': 'Yunnan, China',
        'Zhejiang': 'Zhejiang, China',
        'Anhui': 'Anhui, China',
        'Sichuan': 'Sichuan, China',
        'Guangdong': 'Guangdong, China',
        'Hunan': 'Hunan, China',
        'Jiangsu': 'Jiangsu, China',
        'Hubei': 'Hubei, China',
        'Jiangxi': 'Jiangxi, China',
        'Wuyi': 'Fujian, China (Wuyi Mountains)',
        'Anxi': 'Fujian, China (Anxi County)',
        'Fenghuang': 'Guangdong, China (Phoenix Mountain)',
        'Phoenix': 'Guangdong, China (Phoenix Mountain)',
        'Taiwan': 'Taiwan',
        'Ali Shan': 'Taiwan',
        'Japan': 'Japan',
        'Uji': 'Uji, Japan',
        'Shizuoka': 'Shizuoka, Japan',
        'Darjeeling': 'Darjeeling, India',
        'Assam': 'Assam, India',
        'Nilgiri': 'Nilgiri, India',
        'Sikkim': 'Sikkim, India',
        'Kangra': 'Kangra Valley, India',
        'Ceylon': 'Sri Lanka',
        'Nuwara Eliya': 'Nuwara Eliya, Sri Lanka',
        'Uva': 'Uva, Sri Lanka',
        'Dimbula': 'Dimbula, Sri Lanka',
        'Kandy': 'Kandy, Sri Lanka',
        'Ruhuna': 'Ruhuna, Sri Lanka',
        'Nepal': 'Nepal',
        'Ilam': 'Ilam, Nepal',
        'Kenya': 'Kenya',
        'Indonesia': 'Indonesia',
        'Java': 'Java, Indonesia',
        'Sumatra': 'Sumatra, Indonesia',
        'Vietnam': 'Vietnam',
        'Thailand': 'Thailand',
        'Georgia': 'Georgia',
        'Turkey': 'Turkey',
        'Korea': 'Korea'
    }
    
    # Check description note and tea name
    full_text = (tea_name + ' ' + description_note + ' ' + (subcategory or '')).lower()
    
    for location, full_origin in location_map.items():
        if location.lower() in full_text:
            return full_origin
    
    # Check for pu-erh specific regions
    if any(word in tea_name.lower() for word in ['bulang', 'bada', 'nannuo', 'yiwu', 'ban zhang', 'menghai', 'mengku', 'jingmai', 'gedeng', 'manzhuan', 'yibang', 'xi gui', 'bing dao']):
        return 'Yunnan, China'
    
    # Default based on category
    if 'pu-erh' in tea_name.lower() or 'puer' in tea_name.lower():
        return 'Yunnan, China'
    
    # Specific Japanese teas
    if any(word in tea_name.lower() for word in ['gyokuro', 'sencha', 'matcha', 'genmaicha', 'hojicha', 'kukicha', 'bancha', 'shincha', 'kabusecha', 'tamaryokucha', 'aracha']):
        return 'Japan'
    
    # Specific Chinese teas
    if any(word in tea_name.lower() for word in ['longjing', 'dragon well', 'bi luo chun', 'mao feng', 'gua pian', 'hou kui', 'yin zhen', 'mu dan', 'gong mei', 'shou mei']):
        return 'China'
    
    # Tieguanyin
    if 'tieguanyin' in tea_name.lower() or 'tie guan yin' in tea_name.lower():
        if region == 'Taiwan':
            return 'Taiwan'
        else:
            return 'Fujian, China (Anxi County)'
    
    # Rock teas
    if any(word in tea_name.lower() for word in ['da hong pao', 'rou gui', 'shui xian', 'qi lan', 'yancha', 'rock tea']):
        return 'Fujian, China (Wuyi Mountains)'
    
    # Dan Cong
    if 'dan cong' in tea_name.lower() or 'dancong' in tea_name.lower():
        return 'Guangdong, China (Phoenix Mountain)'
    
    # Scented/flavored - usually China or various
    if 'jasmine' in tea_name.lower() or 'osmanthus' in tea_name.lower() or 'rose' in tea_name.lower():
        return 'China (various regions)'
    
    # Earl Grey and British blends
    if any(word in tea_name.lower() for word in ['earl grey', 'english breakfast', 'irish breakfast', 'scottish breakfast']):
        return 'Blend (various origins)'
    
    # Default based on region if specified
    if region and region != 'Kenya':  # Don't default to Kenya
        if region == 'China':
            return 'China'
        elif region == 'Japan':
            return 'Japan'
        elif region == 'India':
            return 'India'
        elif region == 'Sri Lanka':
            return 'Sri Lanka'
        elif region == 'Taiwan':
            return 'Taiwan'
        elif region == 'Nepal':
            return 'Nepal'
        elif region == 'Kenya':
            return 'Kenya'
        return region
    
    return 'Various'

def generate_tea_data(variety, category_defaults):
    """Generate complete tea data entry from variety info"""
    
    category = variety['category']
    defaults = category_defaults.get(category, category_defaults['Green'])
    
    # Build flavor profile based on tea name and type
    flavor_profile = build_flavor_profile(variety, defaults)
    processing = build_processing_description(variety, category)
    history = build_history(variety)
    cultivars = build_cultivars(variety)
    
    return {
        'name': variety['name'],
        'category': category,
        'origin': variety['origin'],
        'processing': processing,
        'oxidation': defaults['oxidation'],
        'flavor_profile': flavor_profile,
        'aroma': defaults['base_aroma'],
        'appearance': defaults['appearance'],
        'brew_temp_c': defaults['brew_temp_c'],
        'brew_temp_f': defaults['brew_temp_f'],
        'steep_time': defaults['steep_time'],
        'tea_water_ratio': defaults['tea_water_ratio'],
        'reinfusions': defaults['reinfusions'],
        'caffeine_level': defaults['caffeine_level'],
        'health_benefits': defaults['health_benefits'],
        'history': history,
        'price_range': defaults['price_range'],
        'cultivars': cultivars
    }

def build_flavor_profile(variety, defaults):
    """Build specific flavor profile based on tea characteristics"""
    base = defaults['base_flavor']
    name = variety['name'].lower()
    desc = variety.get('description_note', '').lower()
    
    # Specific flavor notes
    specific_flavors = []
    
    if 'silver needle' in name or 'yin zhen' in name:
        specific_flavors.append('extremely delicate, sweet, subtle hay-like sweetness')
    elif 'white peony' in name or 'mu dan' in name:
        specific_flavors.append('sweet, floral, light body with honey notes')
    elif 'longjing' in name or 'dragon well' in name:
        specific_flavors.append('nutty, chestnut, fresh, vegetal, smooth')
    elif 'bi luo chun' in name:
        specific_flavors.append('fruity, sweet, floral, spiral shape releases layered flavors')
    elif 'gyokuro' in name:
        specific_flavors.append('umami-rich, sweet, marine, full-bodied for green tea')
    elif 'sencha' in name:
        specific_flavors.append('fresh, grassy, slightly astringent, balanced')
    elif 'matcha' in name:
        specific_flavors.append('rich umami, creamy, vegetal, sweet finish')
    elif 'tieguanyin' in name or 'tie guan yin' in name:
        specific_flavors.append('floral, orchid notes, creamy, complex')
    elif 'da hong pao' in name or 'big red robe' in name:
        specific_flavors.append('roasted, mineral, complex, long finish')
    elif 'dan cong' in name or 'dancong' in name:
        specific_flavors.append('intensely aromatic, fruity, floral, complex')
    elif 'keemun' in name or 'qimen' in name:
        specific_flavors.append('wine-like, floral, slightly smoky, chocolate notes')
    elif 'lapsang' in name:
        specific_flavors.append('smoky, pine, campfire, bold')
    elif 'darjeeling' in name:
        specific_flavors.append('muscatel, floral, fruity, bright')
    elif 'assam' in name:
        specific_flavors.append('malty, robust, full-bodied, brisk')
    elif 'pu-erh' in name or 'puer' in name or variety['category'] == 'Pu-erh':
        if 'sheng' in name or 'raw' in desc:
            specific_flavors.append('fresh, vegetal, becoming complex with age')
        else:
            specific_flavors.append('earthy, smooth, sweet, woody')
    elif 'oriental beauty' in name or 'dongfang meiren' in name:
        specific_flavors.append('honey, fruity, muscatel, sweet')
    
    if specific_flavors:
        return specific_flavors[0]
    else:
        return base

def build_processing_description(variety, category):
    """Generate processing description based on category"""
    
    processing_map = {
        'White': 'Minimal processing - withering and air drying. Preserves natural antioxidants.',
        'Green': 'Heated (steamed or pan-fired) to prevent oxidation, then rolled and dried.',
        'Oolong': 'Partial oxidation (10-70%), withered, bruised, oxidized, fired. Complex multi-step process.',
        'Black': 'Fully oxidized (85-100%). Withered, rolled, oxidized, fired. Develops malty flavors.',
        'Pu-erh': 'Post-fermented through microbial aging. Can be raw (sheng) or ripe (shou).',
        'Yellow': 'Similar to green tea but with additional smothering/wrapping step for mellowing.',
        'Scented': 'Base tea (usually green or white) scented with flowers or flavored with oils.'
    }
    
    base_processing = processing_map.get(category, 'Traditional tea processing methods.')
    
    # Add specific notes
    name = variety['name'].lower()
    if 'fukamushi' in name or 'deep-steam' in variety.get('description_note', '').lower():
        base_processing += ' Deep-steamed for extra body and umami.'
    elif 'gyokuro' in name or 'shade' in variety.get('description_note', '').lower():
        base_processing += ' Shade-grown for 3-4 weeks before harvest.'
    elif 'roasted' in name or 'hojicha' in name:
        base_processing += ' Roasted to develop nutty, toasted flavors.'
    elif 'compressed' in name or 'cake' in name or 'brick' in name:
        base_processing += ' Compressed into cakes or bricks for aging.'
    
    return base_processing

def build_history(variety):
    """Generate brief history based on tea type"""
    name = variety['name'].lower()
    category = variety['category']
    
    if 'silver needle' in name:
        return 'Originated in Fujian during Song Dynasty. Reserved for imperial court. Most prized white tea.'
    elif 'longjing' in name:
        return 'One of China\'s Ten Famous Teas. Originated in West Lake region during Tang Dynasty. Hand-processed in woks.'
    elif 'gyokuro' in name:
        return 'Created in 1835 in Uji by Yamamoto Kahei. Shade-growing technique developed for unique umami flavor.'
    elif 'matcha' in name:
        return 'Used in Japanese tea ceremonies for over 800 years. Introduced to Japan by Eisai in 1191.'
    elif 'tieguanyin' in name:
        return 'Named "Iron Goddess of Mercy". Legend dates to Qing Dynasty. One of China\'s most famous oolongs.'
    elif 'da hong pao' in name:
        return 'Legend says saved a Ming Dynasty emperor. Original bushes over 350 years old. Most expensive tea ever sold.'
    elif 'darjeeling' in name:
        return 'Established by British in 1850s using Chinese seeds stolen by Robert Fortune. "Champagne of Teas".'
    elif 'pu-erh' in name or category == 'Pu-erh':
        return 'Ancient tea from Yunnan, historically traded on Tea Horse Road. Can age for decades like fine wine.'
    elif 'assam' in name:
        return 'Discovered by Robert Bruce in 1823. First Indian tea not from Chinese seeds. Powers British breakfast tea.'
    elif 'lapsang' in name:
        return 'World\'s first black tea. Created accidentally during Ming Dynasty when army occupied tea factory.'
    elif 'earl grey' in name:
        return 'Named after Charles Grey, 2nd Earl Grey (1830s). Flavored with bergamot oil from Italy.'
    else:
        return f'Traditional {category} tea with centuries of cultivation and refinement. Part of rich tea heritage.'

def build_cultivars(variety):
    """Identify cultivars based on tea name and origin"""
    name = variety['name'].lower()
    origin = variety['origin'].lower()
    
    if 'japan' in origin:
        if 'gyokuro' in name or 'sencha' in name:
            return 'Primarily Yabukita (75% of Japanese tea), also Saemidori, Okumidori'
        elif 'matcha' in name:
            return 'Samidori, Okumidori, Asahi, Uji Midori'
        else:
            return 'Yabukita, various Japanese cultivars'
    elif 'fujian' in origin:
        if 'silver needle' in name or 'white' in variety['category']:
            return 'Fuding Da Bai Hao, Zhenghe Da Bai Hao'
        elif 'tieguanyin' in name:
            return 'Tieguanyin cultivar'
        else:
            return 'Fujian local cultivars'
    elif 'taiwan' in origin:
        if 'jin xuan' in name or 'milk oolong' in name:
            return 'Jin Xuan (TTES #12)'
        elif 'cui yu' in name:
            return 'Cui Yu (TTES #13)'
        else:
            return 'Qing Xin, Jin Xuan, Cui Yu, and other Taiwan cultivars'
    elif 'yunnan' in origin:
        return 'Yunnan Da Ye (large leaf variety), ancient tea tree cultivars'
    elif 'darjeeling' in origin or 'assam' in origin:
        return 'Clonal varieties (AV2, P312, T78, etc.), Chinese hybrids'
    elif 'china' in origin:
        return 'Local Chinese cultivars specific to region'
    else:
        return 'Regional cultivars'

def create_comprehensive_database(db_path='tea_collection.db'):
    """Create comprehensive database from varieties list"""
    
    print("="*70)
    print("Creating Comprehensive Tea Database")
    print("="*70)
    
    # Parse varieties
    print("\n📖 Parsing tea varieties list...")
    varieties_path = os.path.join(os.path.dirname(__file__), 'tea_varieties_list.md')
    varieties = parse_tea_varieties_list(varieties_path)
    print(f"✓ Found {len(varieties)} tea varieties")
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            origin TEXT,
            processing TEXT,
            oxidation TEXT,
            flavor_profile TEXT,
            aroma TEXT,
            appearance TEXT,
            brew_temp_c INTEGER,
            brew_temp_f INTEGER,
            steep_time TEXT,
            tea_water_ratio TEXT,
            reinfusions INTEGER,
            caffeine_level TEXT,
            health_benefits TEXT,
            history TEXT,
            price_range TEXT,
            cultivars TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            elevation_range TEXT,
            climate TEXT,
            famous_teas TEXT,
            description TEXT
        )
    ''')
    
    print(f"\n🍵 Generating detailed information for each tea...")
    
    # Generate and insert tea data
    tea_count = 0
    category_counts = {}
    
    for variety in varieties:
        tea_data = generate_tea_data(variety, CATEGORY_DEFAULTS)
        
        cursor.execute('''
            INSERT INTO teas (
                name, category, origin, processing, oxidation, flavor_profile,
                aroma, appearance, brew_temp_c, brew_temp_f, steep_time,
                tea_water_ratio, reinfusions, caffeine_level, health_benefits,
                history, price_range, cultivars
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tea_data['name'], tea_data['category'], tea_data['origin'],
            tea_data['processing'], tea_data['oxidation'], tea_data['flavor_profile'],
            tea_data['aroma'], tea_data['appearance'], tea_data['brew_temp_c'],
            tea_data['brew_temp_f'], tea_data['steep_time'], tea_data['tea_water_ratio'],
            tea_data['reinfusions'], tea_data['caffeine_level'], tea_data['health_benefits'],
            tea_data['history'], tea_data['price_range'], tea_data['cultivars']
        ))
        
        tea_count += 1
        category_counts[tea_data['category']] = category_counts.get(tea_data['category'], 0) + 1
    
    # Insert regions
    regions = [
        {'name': 'Fujian', 'country': 'China', 'latitude': 26.5, 'longitude': 118.0,
         'elevation_range': '200-1200m', 'climate': 'Subtropical monsoon',
         'famous_teas': 'Silver Needle, White Peony, Tieguanyin, Lapsang Souchong, Wuyi Rock Teas',
         'description': 'Historic tea region, birthplace of white tea, oolong tea, and many famous varieties'},
        
        {'name': 'Yunnan', 'country': 'China', 'latitude': 25.0, 'longitude': 101.0,
         'elevation_range': '1200-2200m', 'climate': 'Subtropical highland',
         'famous_teas': 'Pu-erh, Dian Hong, Moonlight White',
         'description': 'Ancient tea forests, home to tea tree origin, famous for pu-erh production'},
        
        {'name': 'Zhejiang', 'country': 'China', 'latitude': 30.0, 'longitude': 120.5,
         'elevation_range': '200-800m', 'climate': 'Subtropical monsoon',
         'famous_teas': 'Longjing (Dragon Well), Anji Bai Cha',
         'description': 'Famous for green teas, especially Longjing from West Lake region'},
        
        {'name': 'Anhui', 'country': 'China', 'latitude': 30.5, 'longitude': 117.0,
         'elevation_range': '400-1600m', 'climate': 'Humid subtropical',
         'famous_teas': 'Keemun, Huangshan Mao Feng, Lu An Gua Pian',
         'description': 'Produces famous green and black teas from Yellow Mountain region'},
        
        {'name': 'Uji', 'country': 'Japan', 'latitude': 34.88, 'longitude': 135.8,
         'elevation_range': '50-400m', 'climate': 'Humid subtropical',
         'famous_teas': 'Gyokuro, Matcha, Sencha',
         'description': 'Historic Japanese tea region near Kyoto, famous for shade-grown teas'},
        
        {'name': 'Shizuoka', 'country': 'Japan', 'latitude': 34.98, 'longitude': 138.38,
         'elevation_range': '100-600m', 'climate': 'Humid subtropical',
         'famous_teas': 'Sencha, Fukamushi Sencha',
         'description': 'Largest tea-producing region in Japan, produces over 40% of Japanese tea'},
        
        {'name': 'Darjeeling', 'country': 'India', 'latitude': 27.05, 'longitude': 88.27,
         'elevation_range': '600-2000m', 'climate': 'Subtropical highland',
         'famous_teas': 'Darjeeling First Flush, Second Flush, White Tea',
         'description': 'The "Champagne of Teas," known for muscatel flavor and four seasonal flushes'},
        
        {'name': 'Assam', 'country': 'India', 'latitude': 26.75, 'longitude': 94.25,
         'elevation_range': '50-500m', 'climate': 'Tropical wet',
         'famous_teas': 'Assam Orthodox, CTC Assam',
         'description': 'World\'s largest tea-growing region by production, known for malty, robust black teas'},
        
        {'name': 'Nilgiri', 'country': 'India', 'latitude': 11.41, 'longitude': 76.7,
         'elevation_range': '1000-2500m', 'climate': 'Tropical highland',
         'famous_teas': 'Nilgiri Black Tea',
         'description': 'Blue Mountains of South India, produces fragrant, brisk teas year-round'},
        
        {'name': 'Nuwara Eliya', 'country': 'Sri Lanka', 'latitude': 6.95, 'longitude': 80.78,
         'elevation_range': '1800-2500m', 'climate': 'Tropical highland',
         'famous_teas': 'Ceylon High-grown, Silver Tips',
         'description': 'Highest elevation Ceylon tea region, produces delicate, fragrant teas'},
        
        {'name': 'Kandy', 'country': 'Sri Lanka', 'latitude': 7.29, 'longitude': 80.63,
         'elevation_range': '600-1200m', 'climate': 'Tropical mid-elevation',
         'famous_teas': 'Kandy Ceylon',
         'description': 'Mid-grown Ceylon teas, full-bodied with copper-colored liquor'},
        
        {'name': 'Taiwan High Mountains', 'country': 'Taiwan', 'latitude': 24.0, 'longitude': 121.0,
         'elevation_range': '1000-2600m', 'climate': 'Subtropical mountain',
         'famous_teas': 'Ali Shan, Li Shan, Dong Ding Oolong',
         'description': 'High mountain oolongs from Central Mountain Range, prized for floral character'}
    ]
    
    for region in regions:
        cursor.execute('''
            INSERT INTO regions (
                name, country, latitude, longitude, elevation_range,
                climate, famous_teas, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            region['name'], region['country'], region['latitude'], region['longitude'],
            region['elevation_range'], region['climate'], region['famous_teas'], region['description']
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✓ Added {tea_count} teas to database")
    print(f"\n📊 Tea Breakdown by Category:")
    for category, count in sorted(category_counts.items()):
        print(f"   {category:15} : {count:3} varieties")
    
    print(f"\n✓ Added {len(regions)} tea regions")
    print(f"\n✅ Database created successfully: {db_path}")
    print("="*70)

if __name__ == "__main__":
    create_comprehensive_database()
