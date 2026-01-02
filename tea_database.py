"""
Tea Database Creation and Management
Creates and populates a SQLite database with comprehensive tea information
"""

import sqlite3
import os

class TeaDatabase:
    def __init__(self, db_path="tea_collection.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create database tables"""
        # Main tea varieties table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS teas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                origin_country TEXT,
                origin_region TEXT,
                processing_method TEXT,
                oxidation_level TEXT,
                flavor_profile TEXT,
                aroma TEXT,
                appearance TEXT,
                water_temp_celsius INTEGER,
                water_temp_fahrenheit INTEGER,
                steep_time_min INTEGER,
                steep_time_max INTEGER,
                tea_to_water_ratio TEXT,
                reinfusions INTEGER,
                caffeine_level TEXT,
                health_benefits TEXT,
                history TEXT,
                best_time TEXT,
                price_range TEXT,
                notable_cultivars TEXT
            )
        ''')
        
        # Tea regions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                country TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                elevation_min INTEGER,
                elevation_max INTEGER,
                climate TEXT,
                famous_teas TEXT,
                description TEXT
            )
        ''')
        
        self.conn.commit()
    
    def populate_teas(self):
        """Populate database with tea varieties"""
        teas_data = [
            # WHITE TEAS
            ("Silver Needle (Bai Hao Yin Zhen)", "White", "China", "Fujian Province (Fuding/Zhenghe)",
             "Withering and drying only", "0-5%", 
             "Sweet, vegetal, vanilla, fresh almonds, meadow grass", 
             "Delicate, floral, honey-like",
             "Silvery-white downy buds, pale golden liquor",
             90, 194, 3, 5, "2-2.5g per 250ml (Western) or 3-5g per 100ml (Gongfu)",
             8, "Low", 
             "High antioxidants (3x more than oxidized teas), antibacterial properties, supports cardiovascular health, may reduce colon polyps",
             "Most prized white tea, exclusively unopened buds, harvested in early spring. Fuding produces lighter style, Zhenghe fuller-bodied.",
             "Morning or afternoon", "$$$$", "Da Bai, Xiao Bai cultivars"),
            
            ("White Peony (Bai Mu Dan)", "White", "China", "Fujian Province",
             "Withering and drying", "5-10%",
             "Floral, honey, white grape, melon, apricot",
             "Rich floral with honey notes",
             "Mix of buds and leaves, unfurls like peony petals, amber-gold liquor",
             85, 185, 2, 4, "2-4g per 100ml",
             5, "Low",
             "Antioxidants, anti-inflammatory, supports immune system, aids digestion",
             "One bud with 1-2 leaves. Chinese saying: 'one year tea, three years medicine, seven years treasure' - improves with aging.",
             "Afternoon", "$$$", "Fuding Da Bai Cha"),
            
            ("Moonlight White (Yue Guang Bai)", "White", "China", "Yunnan Province",
             "Dark withering (away from sunlight)", "10-15%",
             "Honey, malt, dried longan, cooling herbal sensation",
             "Sweet, floral with mineral undertones",
             "Dark and light leaves (yin-yang appearance), golden liquor",
             85, 185, 1, 2, "5g per 100ml",
             8, "Low",
             "Cooling properties, aids digestion, antioxidants",
             "Uses large-leaf assamica variety (same as pu-erh). Unique processing creates distinctive appearance.",
             "Evening (cooling effect)", "$$$", "Yunnan large-leaf variety"),
            
            # GREEN TEAS - Japanese
            ("Gyokuro", "Green", "Japan", "Uji, Kyoto / Yame, Fukuoka",
             "Steamed, shaded 20+ days before harvest", "0%",
             "Rich umami, sweet, marine-seaweed, broth-like",
             "Deep vegetal, ocean-like",
             "Deep green needle-shaped leaves, bright green liquor",
             50, 122, 1.5, 2, "10g per 60ml",
             4, "Low-Medium",
             "High L-theanine (promotes calm alertness), amino acids, chlorophyll, antioxidants",
             "Japan's most prestigious green tea. Shading increases chlorophyll and L-theanine while reducing catechins.",
             "Morning meditation", "$$$$$", "Yabukita, Samidori, Okumidori"),
            
            ("Sencha", "Green", "Japan", "Shizuoka, Kagoshima",
             "Steamed, rolled", "0%",
             "Fresh, grassy, vegetal with sweet finish",
             "Green, refreshing, slight ocean breeze",
             "Thin, needle-like leaves, yellow-green liquor",
             70, 158, 1, 1.5, "2 tsp per 365ml",
             3, "Medium",
             "EGCG antioxidants, supports metabolism, cardiovascular health, cancer prevention",
             "Accounts for 60% of Japanese tea production. Grown in full sunlight.",
             "Morning or afternoon", "$$", "Yabukita (75% of Japanese tea)"),
            
            ("Matcha", "Green", "Japan", "Uji, Nishio",
             "Stone-ground shaded tea leaves", "0%",
             "Rich umami, sweet, creamy, vegetal",
             "Intense green tea aroma",
             "Fine bright green powder, jade-green frothy suspension",
             80, 176, 0, 0, "2g per 70ml (usucha) or 4g per 40ml (koicha)",
             1, "High",
             "Maximum EGCG (consuming whole leaf), L-theanine, sustained energy, enhanced focus, metabolism support",
             "Only tea where entire leaf is consumed. Ceremonial grade vs culinary grade quality levels.",
             "Morning (traditional ceremony)", "$$$$", "Samidori, Okumidori, Asahi"),
            
            ("Genmaicha", "Green", "Japan", "Various regions",
             "Green tea blended with roasted rice", "0%",
             "Nutty, toasty, popcorn-like, light tea flavor",
             "Roasted grain, comforting",
             "Green leaves mixed with brown rice, some puffed, yellow-green liquor",
             90, 194, 0.5, 1, "1 tbsp per 250ml",
             3, "Low",
             "Lower caffeine, digestive aid, comforting",
             "Originally consumed by poor who stretched tea with rice. Now appreciated for unique flavor.",
             "Meals, evening", "$", "Usually Bancha base"),
            
            ("Hojicha", "Green", "Japan", "Various regions",
             "Roasted at 200°C after steaming", "0%",
             "Caramel, nutty, slightly smoky, roasted grain",
             "Roasted, coffee-like",
             "Brown roasted leaves, reddish-brown liquor",
             100, 212, 0.5, 1, "1 tbsp per 250ml",
             2, "Very Low (caffeine sublimated during roasting)",
             "Gentle on stomach, low caffeine (safe for evening), digestive support",
             "Roasting process removes most caffeine. Popular evening tea in Japan.",
             "Evening, after meals", "$", "Roasted Bancha or Sencha"),
            
            # GREEN TEAS - Chinese
            ("Longjing (Dragon Well)", "Green", "China", "Hangzhou, Zhejiang (West Lake region)",
             "Pan-fired, hand-pressed flat", "0%",
             "Chestnut-sweet, smooth, mellow, vegetal",
             "Fresh, nutty, sweet",
             "Flat, sword-shaped leaves, jade-green, clear yellow-green liquor",
             80, 176, 0.5, 1, "3g per 150ml",
             3, "Low-Medium",
             "Antioxidants, supports cardiovascular health, anti-inflammatory",
             "One of China's most famous teas. Ming Qian (pre-Qingming, April 5th) is most prized.",
             "Afternoon", "$$$$", "Longjing #43"),
            
            ("Biluochun (Green Snail Spring)", "Green", "China", "Dongting Mountains, Jiangsu",
             "Hand-rolled into tight spirals", "0%",
             "Fruity, floral, delicate, sweet",
             "Fruit blossoms, delicate",
             "Tightly spiraled with white fuzz, pale green liquor",
             75, 167, 2, 3, "3g per 150ml",
             3, "Low",
             "High antioxidants, supports immune system",
             "14,000-15,000 shoots per kilogram. Intercropped with fruit trees, creating fruity notes.",
             "Morning", "$$$$", "Local small-leaf variety"),
            
            # OOLONG TEAS
            ("Tie Guan Yin (Iron Goddess)", "Oolong", "China", "Anxi County, Fujian",
             "Rolled, lightly to moderately oxidized", "15-40%",
             "Orchid, floral, honey, nut (traditional style)",
             "Orchid fragrance, sweet",
             "Tightly rolled balls, golden-green liquor",
             90, 194, 0.5, 1, "7-8g per 110ml",
             7, "Medium",
             "Antioxidants, supports metabolism, digestive health",
             "Named for legendary origin story. Two styles: Qing Xiang (light, modern) and Nong Xiang (traditional roasted).",
             "Afternoon", "$$$", "Tie Guan Yin cultivar"),
            
            ("High Mountain Oolong (Gao Shan)", "Oolong", "Taiwan", "Ali Shan, Li Shan, Da Yu Ling (1,000-2,600m)",
             "Lightly oxidized, hand-rolled", "10-25%",
             "Floral, orchid, buttery, creamy, sweet",
             "Clean, floral, orchid-like",
             "Tightly rolled balls, pale golden liquor",
             90, 194, 0.5, 1, "5g per 100ml",
             8, "Low-Medium",
             "Antioxidants, L-theanine (calming), supports mental clarity",
             "Cool temperatures and frequent fog slow leaf growth, concentrating flavor compounds.",
             "Morning or afternoon", "$$$$", "Qing Xin, Jin Xuan"),
            
            ("Da Hong Pao (Big Red Robe)", "Oolong", "China", "Wuyi Mountains, Fujian",
             "Heavily oxidized, charcoal roasted", "60-70%",
             "Roasted nuts, dark chocolate, stone fruit, mineral 'rock rhyme'",
             "Rich, roasted, complex",
             "Dark twisted leaves, deep amber-red liquor",
             100, 212, 0.1, 0.2, "7g per 100ml",
             10, "Medium-High",
             "Antioxidants, aids digestion, warming properties",
             "Original 6 mother trees on Tianxin Rock are national treasures. 20g sold for ¥208,000 in 2005.",
             "Evening", "$$$$$", "Qidan, Beidou cultivars"),
            
            ("Oriental Beauty (Dong Fang Mei Ren)", "Oolong", "Taiwan", "Hsinchu, Miaoli",
             "Insect-bitten, heavily oxidized, unroasted", "60-85%",
             "Honey, peach, rose petal, muscatel",
             "Natural honey, fruity",
             "Multicolored leaves (white, green, red, brown), amber-red liquor",
             85, 185, 1, 2, "5g per 100ml",
             5, "Low",
             "Unique terpenes from insect bites, antioxidants",
             "Requires tea jassid insects to bite leaves, triggering terpene release. Must be pesticide-free.",
             "Afternoon", "$$$$", "Qing Xin Da Mao"),
            
            # BLACK TEAS
            ("Darjeeling First Flush", "Black", "India", "Darjeeling, West Bengal (7,000 ft)",
             "Orthodox processing", "100%",
             "Floral, jasmine, apricot, peach, light astringency",
             "Delicate, floral, fruity",
             "Light, wiry leaves, pale golden liquor",
             80, 176, 2, 4, "2.5g per 250ml",
             3, "Low-Medium",
             "Antioxidants, supports cardiovascular health, energizing",
             "Harvested late February-April. 87 estates produce only 600,000-700,000 kg annually.",
             "Morning or afternoon", "$$$$", "Chinary (Chinese hybrid)"),
            
            ("Darjeeling Second Flush", "Black", "India", "Darjeeling, West Bengal",
             "Orthodox processing", "100%",
             "Muscatel, honey, caramel, fuller body",
             "Wine-like, fruity",
             "Darker leaves with golden tips, amber-reddish liquor",
             95, 203, 3, 5, "2.5g per 250ml",
             3, "Medium",
             "Antioxidants, theaflavins, supports heart health",
             "Harvested May-June. Distinctive muscatel character develops during this season.",
             "Afternoon", "$$$$", "Chinary hybrid"),
            
            ("Assam", "Black", "India", "Brahmaputra Valley, Assam",
             "Orthodox or CTC", "100%",
             "Malty, bold, dark chocolate, caramel, brisk",
             "Strong, malty, robust",
             "Dark brown-black leaves, deep reddish-brown liquor",
             100, 212, 3, 5, "2.5g per 250ml",
             2, "High",
             "High caffeine, supports energy, antioxidants",
             "Assamica variety discovered wild in 1823. Lowland tropical production.",
             "Morning (breakfast tea)", "$$", "Assamica variety"),
            
            ("Keemun", "Black", "China", "Anhui Province",
             "Orthodox processing", "100%",
             "Wine-like, fruity, floral, light smokiness, unsweetened chocolate",
             "Fragrant, wine-like",
             "Thin, dark leaves, clear red liquor",
             90, 194, 3, 4, "2.5g per 250ml",
             3, "Medium",
             "Antioxidants, supports digestion",
             "Created 1875. Traditional base for Earl Grey. Known for 'Keemun aroma'.",
             "Afternoon", "$$$", "Qimen cultivar"),
            
            ("Lapsang Souchong", "Black", "China", "Wuyi Mountains, Fujian",
             "Smoked over pine wood (or unsmoked traditional)", "100%",
             "Pine smoke, bacon-like (smoked) or honey, sweet potato (unsmoked)",
             "Distinctive pine smoke or natural sweet",
             "Large, dark leaves, deep red liquor",
             95, 203, 3, 5, "2.5g per 250ml",
             4, "Medium",
             "Antioxidants, warming properties",
             "World's first black tea (Ming Dynasty). Authentic Zhengshan Xiaozhong is unsmoked.",
             "Morning or afternoon", "$$$", "Wuyi variety"),
            
            ("Dian Hong (Yunnan Gold)", "Black", "China", "Yunnan Province",
             "Orthodox processing", "100%",
             "Honey, fruity, sweet potato, dark chocolate, hazelnut",
             "Sweet, malty, rich",
             "Golden tips, bright golden-red liquor",
             95, 203, 3, 5, "2.5g per 250ml",
             4, "Medium",
             "Antioxidants, naturally sweet (low bitterness)",
             "Uses large-leaf assamica variety. More golden tips indicate higher quality.",
             "Morning", "$$$", "Yunnan large-leaf"),
            
            ("Ceylon (Nuwara Eliya)", "Black", "Sri Lanka", "Nuwara Eliya (6,000+ ft)",
             "Orthodox processing", "100%",
             "Delicate, floral, citrusy, light-bodied",
             "Fragrant, delicate",
             "Wiry leaves, light amber liquor",
             95, 203, 3, 5, "2.5g per 250ml",
             3, "Medium",
             "Antioxidants, supports metabolism",
             "Highest elevation Ceylon tea, called 'champagne of Ceylon'. Light and delicate.",
             "Afternoon", "$$$", "Assam variety adapted to Ceylon"),
            
            # PU-ERH TEAS
            ("Sheng Pu-erh (Raw)", "Pu-erh", "China", "Yunnan (various mountains)",
             "Sun-dried, naturally aged or young", "Varies with age",
             "Bright, vegetal, floral (young) or dried fruits, plum, camphor, leather (aged)",
             "Fresh and vegetal or deep and complex",
             "Compressed cakes, golden (young) to dark amber (aged) liquor",
             90, 194, 0.2, 0.3, "6-8g per 100ml",
             15, "Medium-High",
             "Supports digestion, may aid weight management, antioxidants (age-dependent)",
             "Designed for long-term aging (15-30+ years). Transforms dramatically with proper storage.",
             "Morning or afternoon", "$$$-$$$$$", "Ancient tree, wild arbor"),
            
            ("Shou Pu-erh (Ripe)", "Pu-erh", "China", "Yunnan Province",
             "Pile fermentation (wo dui) 15-90 days", "Post-fermented",
             "Earthy, smooth, dark chocolate, forest floor, leather",
             "Earthy, woody, aged",
             "Dark brown-black compressed cakes, very dark liquor",
             100, 212, 0.2, 0.3, "6-8g per 100ml",
             20, "Low",
             "Supports digestion, may aid weight loss, modulates gut microbiota, lowers cholesterol",
             "Developed 1973 to mimic aged sheng. Uses microbial fermentation. Two quick rinses essential.",
             "After meals, evening", "$$-$$$$", "Various cultivars"),
            
            # YELLOW TEA
            ("Junshan Yinzhen", "Yellow", "China", "Junshan Island, Hunan",
             "Men huan (sealed yellowing) 24-72 hours", "5-10%",
             "Fresh sugarcane, wild flowers, smooth, mellow",
             "Delicate, sweet, sophisticated",
             "Golden-yellow buds, 'dancing leaves' stand upright in glass",
             80, 176, 3, 3, "3g per 150ml",
             3, "Low",
             "Gentler on stomach than green tea, antioxidants, aids digestion",
             "Most prestigious yellow tea. Only ~1,000 kg produced annually from tiny island (0.96 km²).",
             "Afternoon", "$$$$$", "Local variety"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO teas (name, category, origin_country, origin_region, processing_method,
                            oxidation_level, flavor_profile, aroma, appearance, water_temp_celsius,
                            water_temp_fahrenheit, steep_time_min, steep_time_max, tea_to_water_ratio,
                            reinfusions, caffeine_level, health_benefits, history, best_time, 
                            price_range, notable_cultivars)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', teas_data)
        
        self.conn.commit()
        print(f"Inserted {len(teas_data)} tea varieties")
    
    def populate_regions(self):
        """Populate tea-growing regions"""
        regions_data = [
            ("Fujian Province", "China", 26.5, 118.0, 100, 1500,
             "Subtropical monsoon", "White teas, Oolongs (Wuyi Rock, Anxi Iron Goddess)",
             "Historic tea province producing white, oolong, and black teas"),
            
            ("Yunnan Province", "China", 25.0, 101.0, 1000, 2500,
             "Subtropical highland", "Pu-erh, Dian Hong, Moonlight White",
             "Home of ancient tea trees and birthplace of tea cultivation"),
            
            ("Zhejiang Province", "China", 30.0, 120.0, 100, 800,
             "Humid subtropical", "Longjing (Dragon Well), Anji Bai Cha",
             "Famous for pan-fired green teas, especially from West Lake region"),
            
            ("Uji, Kyoto", "Japan", 34.9, 135.8, 20, 100,
             "Humid subtropical", "Gyokuro, Matcha, Sencha",
             "Japan's most prestigious tea region, producing finest matcha since 12th century"),
            
            ("Shizuoka", "Japan", 35.0, 138.4, 0, 800,
             "Temperate maritime", "Sencha, Fukamushi Sencha",
             "Largest tea-producing region in Japan, accounts for 40% of production"),
            
            ("Darjeeling", "India", 27.0, 88.3, 600, 2100,
             "Subtropical highland", "Darjeeling First & Second Flush",
             "87 estates in Himalayan foothills, 'Champagne of Teas', 6,000-7,000 ft elevation"),
            
            ("Assam", "India", 26.5, 93.0, 50, 500,
             "Tropical monsoon", "Assam Orthodox, CTC",
             "Brahmaputra River valley, world's largest tea-growing region, discovered 1823"),
            
            ("Nilgiri", "India", 11.4, 76.7, 1000, 2500,
             "Tropical highland", "Nilgiri Orthodox",
             "Blue Mountains of South India, year-round production"),
            
            ("Nuwara Eliya", "Sri Lanka", 6.95, 80.78, 1800, 2100,
             "Tropical highland", "Ceylon High-grown",
             "Highest elevation Ceylon tea, 6,000+ ft, delicate and fragrant"),
            
            ("Kandy", "Sri Lanka", 7.29, 80.63, 600, 1200,
             "Tropical mid-elevation", "Ceylon Mid-grown",
             "Historic region where James Taylor started Ceylon tea industry in 1867"),
            
            ("Taiwan High Mountains", "Taiwan", 23.9, 121.0, 1000, 2600,
             "Subtropical highland", "High Mountain Oolong, Oriental Beauty",
             "Ali Shan, Li Shan, Da Yu Ling - premium oolongs from extreme elevations"),
            
            ("Anhui Province", "China", 31.0, 117.0, 200, 1500,
             "Humid subtropical", "Keemun, Taiping Houkui, Huangshan Mao Feng",
             "Yellow Mountain region, produces famous green and black teas"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO regions (name, country, latitude, longitude, elevation_min, elevation_max,
                               climate, famous_teas, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', regions_data)
        
        self.conn.commit()
        print(f"Inserted {len(regions_data)} tea regions")
    
    def initialize_database(self):
        """Create and populate the entire database"""
        self.connect()
        self.create_tables()
        
        # Check if already populated
        self.cursor.execute("SELECT COUNT(*) FROM teas")
        tea_count = self.cursor.fetchone()[0]
        
        if tea_count == 0:
            print("Populating database with tea varieties...")
            self.populate_teas()
            self.populate_regions()
            print("Database initialization complete!")
        else:
            print(f"Database already contains {tea_count} teas")
        
        self.close()

def main():
    """Initialize the tea database"""
    db = TeaDatabase()
    db.initialize_database()

if __name__ == "__main__":
    main()
