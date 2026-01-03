"""
Tea Database Creation and Management - CORRECTED VERSION
Creates and populates a SQLite database with comprehensive tea information

FIXES:
- Corrected schema to match actual database
- Fixed brewing temperatures (especially Gyokuro and Silver Needle)
- Removed cultivars from main tea table
- Fixed oxidation percentages
- Created separate cultivars table
- Corrected factual errors
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
    
    def drop_tables(self):
        """Drop existing tables for fresh start"""
        self.cursor.execute('DROP TABLE IF EXISTS teas')
        self.cursor.execute('DROP TABLE IF EXISTS regions')
        self.cursor.execute('DROP TABLE IF EXISTS cultivars')
        self.conn.commit()
    
    def create_tables(self):
        """Create database tables with corrected schema"""
        
        # Main tea varieties table - matches actual database structure
        self.cursor.execute('''
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
        
        # NEW: Cultivars table for tea plant varieties
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cultivars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                species TEXT,
                origin_country TEXT,
                leaf_size TEXT,
                characteristics TEXT,
                common_uses TEXT,
                notes TEXT
            )
        ''')
        
        self.conn.commit()
    
    def populate_teas(self):
        """Populate database with tea varieties - CORRECTED DATA"""
        teas_data = [
            # WHITE TEAS - Fixed brewing temperatures
            ("Bai Hao Yin Zhen (Silver Needle)", "White", "China - Fujian Province (Fuding/Zhenghe)",
             "Withering and air-drying only, no rolling", "0% (enzymatic oxidation prevented)",
             "Sweet, delicate, vegetal, fresh hay, honeydew melon, cucumber",
             "Subtle floral, honey, clean",
             "Silvery-white downy buds, pale champagne-golden liquor",
             85, 185, "4-5 minutes",
             "3g per 150ml (Western) or 5g per 100ml (Gongfu)",
             8, "Low (15-30mg per cup)",
             "Extremely high in antioxidants (3-5x more than oxidized teas), antibacterial properties, supports cardiovascular health, anti-inflammatory, may help prevent cancer",
             "Most prized white tea, made exclusively from unopened buds harvested in early spring (2-3 day window). Fuding style is more delicate, Zhenghe fuller-bodied. Only tips covered in white downy hairs are used.",
             "$$$$", "Da Bai, Xiao Bai"),
            
            ("Bai Mu Dan (White Peony)", "White", "China - Fujian Province",
             "Withering and drying, minimal processing", "5-8% (natural withering)",
             "Floral, honey, white peach, hay, slightly vegetal",
             "Delicate floral with honey sweetness",
             "Mix of silvery buds and green-brown leaves, pale golden liquor",
             80, 176, "3-4 minutes",
             "3g per 150ml",
             6, "Low (15-25mg per cup)",
             "High antioxidants, anti-inflammatory, supports immune system, aids digestion, gentle on stomach",
             "One bud with two young leaves. The most popular white tea. Chinese saying: 'one year tea, three years medicine, seven years treasure' - improves with aging like wine.",
             "$$$", "Fuding Da Bai Cha"),
            
            ("Yue Guang Bai (Moonlight White)", "White", "China - Yunnan Province",
             "Withered in moonlight/shade (dark withering)", "10-15% (controlled withering)",
             "Honey, malt, dried longan fruit, cooling herbal sensation, sweet potato",
             "Sweet, fruity, mineral undertones",
             "Distinctive bicolor leaves (dark top, white bottom), golden-amber liquor",
             85, 185, "2-3 minutes",
             "5g per 100ml",
             8, "Low-Medium (20-35mg per cup)",
             "Cooling properties (Chinese medicine), aids digestion, antioxidants, gentle energy",
             "Uses Yunnan large-leaf assamica variety (same species as pu-erh). Unique processing creates yin-yang appearance. Night withering reduces bitterness and creates cooling effect.",
             "$$$", "Yunnan large-leaf variety"),
            
            ("Gong Mei (Tribute Eyebrow)", "White", "China - Fujian Province",
             "Traditional withering, includes some stems", "8-12% (natural)",
             "Sweet, fruity, honey, slightly earthy",
             "Honey, hay, mild",
             "Small leaves with stems, orange-amber liquor",
             85, 185, "3-5 minutes",
             "4g per 150ml",
             5, "Low (15-25mg per cup)",
             "Antioxidants, digestive support, calming",
             "Lower grade than Silver Needle or White Peony, but rich flavor. Often aged. Made from Xiao Bai (Small White) cultivar.",
             "$$", "Xiao Bai"),
            
            ("Shou Mei (Longevity Eyebrow)", "White", "China - Fujian Province",
             "Later harvest, includes larger leaves and stems", "10-15% (natural)",
             "Robust, fruity, woody, honey, dates",
             "Rich, fruity, earthy",
             "Darker leaves with stems, deep golden-amber liquor",
             85, 185, "4-6 minutes",
             "4g per 150ml",
             6, "Low-Medium (20-30mg per cup)",
             "Antioxidants, aids digestion, aging potential, immune support",
             "Latest harvest white tea, full-bodied. Excellent for aging (5-10+ years). Lower price makes it accessible for daily drinking.",
             "$$", "Da Bai or Xiao Bai"),
            
            ("Darjeeling White Tea", "White", "India - Darjeeling, West Bengal",
             "Minimal processing, withering only", "5-10% (natural)",
             "Delicate, floral, peach, apricot, light muscatel",
             "Floral, fruity, clean",
             "Silvery tips, pale golden liquor",
             80, 176, "3-4 minutes",
             "3g per 150ml",
             5, "Low (15-25mg per cup)",
             "Antioxidants, gentle energy, supports metabolism",
             "Relatively new category from Darjeeling estates. Combines white tea processing with Himalayan terroir.",
             "$$$", "Chinary hybrid"),
            
            ("Ceylon Silver Tips", "White", "Sri Lanka - Nuwara Eliya region",
             "Minimal processing, buds only", "5-10% (natural)",
             "Sweet, honey, malt, subtle fruit",
             "Delicate, honey-like",
             "Golden-brown tips, pale amber liquor",
             80, 176, "3-5 minutes",
             "3g per 150ml",
             5, "Low (15-25mg per cup)",
             "Antioxidants, gentle caffeine, immune support",
             "Premium Ceylon white tea from high-elevation estates. Unique golden color distinguishes it from Chinese white teas.",
             "$$$", "Ceylon variety"),
            
            # GREEN TEAS - JAPANESE (CORRECTED TEMPERATURES)
            ("Gyokuro", "Green", "Japan - Uji (Kyoto), Yame (Fukuoka), Shizuoka",
             "Steamed, shaded 20-21 days before harvest, rolled into needles", "0% (steaming stops oxidation)",
             "Intense umami, sweet, marine-like, broth-like richness, minimal astringency",
             "Deep vegetal, ocean-like, fresh seaweed, sweet grass",
             "Deep green needle-shaped leaves, vibrant emerald-green liquor",
             50, 122, "2-2.5 minutes (first infusion), 10-20 seconds (later)",
             "10g per 60ml (traditional) or 3g per 100ml (lighter)",
             4, "Medium (30-50mg per cup despite low temp due to high leaf quantity)",
             "Extremely high L-theanine (promotes calm alertness without jitters), high chlorophyll, amino acids, catechins, supports mental clarity and relaxation",
             "Japan's most prestigious green tea, created 1835 in Uji by Yamamoto Kahei VI. Shading 20+ days increases chlorophyll, L-theanine, and amino acids while reducing catechins and bitterness. Premium grade can cost $100+/100g.",
             "$$$$$", "Yabukita, Samidori, Okumidori, Asahi"),
            
            ("Sencha", "Green", "Japan - Shizuoka, Kagoshima, Mie",
             "Steamed (15-80 seconds), rolled into needles", "0% (steaming stops oxidation)",
             "Fresh, grassy, vegetal, sweet finish, slight astringency, clean",
             "Green, refreshing, ocean breeze",
             "Thin, dark green needle-like leaves, yellow-green liquor",
             70, 158, "1-2 minutes",
             "3g per 200ml or 2 tsp per 365ml",
             3, "Medium (30-50mg per cup)",
             "High in EGCG catechins, supports metabolism, cardiovascular health, cancer prevention, rich in antioxidants, vitamins C and E",
             "Most common Japanese tea, accounts for 60% of production. Grown in full sunlight unlike gyokuro. Fukamushi (deep-steamed) variety has richer flavor and color. First flush (shin sencha) is most prized.",
             "$$", "Yabukita (75% of Japanese tea), Okumidori, Saemidori"),
            
            ("Matcha", "Green", "Japan - Uji, Nishio, Shizuoka",
             "Stone-ground shaded tea leaves into fine powder", "0% (steaming stops oxidation)",
             "Rich umami, creamy, sweet, vegetal, slightly bitter (culinary grade)",
             "Intense green tea aroma, fresh grass",
             "Fine bright green powder, jade-green frothy suspension when whisked",
             80, 176, "Not applicable (whisked, not steeped)",
             "2g (1 tsp) per 70ml usucha style, 4g per 40ml koicha style",
             1, "High (70mg per serving - consuming whole leaf)",
             "Maximum EGCG and catechins (consuming whole leaf vs steeping), extremely high L-theanine, sustained energy without crash, enhanced focus, metabolism support, chlorophyll",
             "Only tea where entire leaf is consumed. Tencha (shade-grown leaf) is stone-ground. Ceremonial grade (vibrant green, smooth) vs culinary grade (slightly bitter, cooking). Used in Japanese tea ceremony (chanoyu).",
             "$$$$", "Samidori, Okumidori, Asahi, Yabukita"),
            
            ("Genmaicha", "Green", "Japan - Various regions",
             "Green tea (usually Bancha) blended 1:1 with roasted brown rice", "0% (green tea component)",
             "Nutty, toasty, popcorn-like, light fresh tea flavor, comforting",
             "Roasted grain, popped corn, mild tea",
             "Green tea leaves mixed with brown roasted rice (some puffed), yellow-green liquor",
             80, 176, "30 seconds to 1 minute",
             "1 tbsp per 250ml",
             3, "Low (15-25mg per cup - diluted by rice)",
             "Lower caffeine, digestive aid, comforting, gentle on stomach, some added nutrients from rice",
             "Originally consumed by poor who stretched expensive tea with rice. Now appreciated for unique nutty flavor and lower caffeine. Called 'popcorn tea' in English.",
             "$", "Usually Bancha base, sometimes Sencha"),
            
            ("Hojicha", "Green", "Japan - Various regions",
             "Roasted at 200°C (392°F) after steaming, uses Bancha or Kukicha", "0% (green tea base, roasted)",
             "Caramel, nutty, toasty, roasted grain, slightly smoky, no grassiness",
             "Roasted, coffee-like, warm",
             "Brown roasted leaves and stems, reddish-brown liquor",
             100, 212, "30 seconds to 1 minute",
             "1 tbsp per 250ml",
             2, "Very Low (5-10mg per cup - caffeine sublimated during high-heat roasting)",
             "Gentle on stomach, virtually no caffeine (safe for evening/children), digestive support, warming",
             "Roasting at 200°C removes most caffeine through sublimation. Popular evening tea in Japan. Often made from Bancha or Kukicha (twigs). Developed in Kyoto in 1920s.",
             "$", "Roasted Bancha or Kukicha (twig tea)"),
            
            ("Kukicha (Twig Tea)", "Green", "Japan - By-product of Sencha or Gyokuro production",
             "Steamed stems and twigs, roasted or unroasted", "0%",
             "Light, slightly sweet, creamy, nutty (if roasted), mild",
             "Subtle, fresh, slightly sweet",
             "Light brown stems and twigs, pale yellow-green liquor",
             80, 176, "1-2 minutes",
             "1 tbsp per 250ml",
             3, "Very Low (5-15mg per cup - stems contain minimal caffeine)",
             "Very low caffeine, high in minerals, gentle, slightly alkaline, good for children",
             "Made from stems and twigs removed during processing. Karigane is kukicha from gyokuro. Sweet flavor from theanine in stems. Very economical.",
             "$", "Stems from various cultivars"),
            
            # GREEN TEAS - CHINESE
            ("Xi Hu Longjing (West Lake Dragon Well)", "Green", "China - Hangzhou, Zhejiang (West Lake region)",
             "Pan-fired, hand-pressed flat against heated wok", "0% (pan-firing stops oxidation)",
             "Chestnut-sweet, smooth, mellow, vegetal, orchid notes, umami",
             "Fresh, nutty, sweet chestnut, floral",
             "Flat, sword-shaped leaves, jade-green, clear yellow-green liquor",
             80, 176, "1-3 minutes",
             "3g per 150ml",
             3, "Low-Medium (30-40mg per cup)",
             "High antioxidants, supports cardiovascular health, anti-inflammatory, calming",
             "One of China's top 10 famous teas. Ming Qian (pre-Qingming festival, before April 5th) is most prized. Yu Qian (pre-Grain Rain) is second best. Hand-pressed flat in heated wok using 10 traditional techniques.",
             "$$$$", "Longjing #43"),
            
            ("Dong Ting Bi Luo Chun (Green Snail Spring)", "Green", "China - Dongting Mountains, Jiangsu",
             "Hand-rolled into tight spirals, pan-fired", "0%",
             "Fruity, floral, delicate, sweet, peach, apricot",
             "Fruit blossoms, delicate, sweet",
             "Tightly spiraled green leaves with white downy fuzz, pale green liquor",
             75, 167, "2-3 minutes",
             "3g per 150ml",
             3, "Low (25-35mg per cup)",
             "High antioxidants, supports immune system, gentle energy",
             "One of China's top 10 famous teas. Requires 13,000-15,000 shoots per kilogram. Intercropped with fruit trees (peach, plum, apricot), creating natural fruity notes. Harvest window is only 15-20 days in early spring.",
             "$$$$", "Local small-leaf variety"),
            
            ("Huangshan Mao Feng (Yellow Mountain Fur Peak)", "Green", "China - Huangshan (Yellow Mountain), Anhui",
             "Pan-fired, slightly curled", "0%",
             "Delicate, floral, orchid, apricot, sweet, smooth",
             "Floral, sweet, clean",
             "Slightly curled leaves with white tips, clear pale yellow liquor",
             80, 176, "2-3 minutes",
             "3g per 150ml",
             3, "Low-Medium (30-40mg per cup)",
             "Antioxidants, supports digestion, calming",
             "One of China's top 10 famous teas. Grown at 800-1,200m elevation on Yellow Mountain. Harvested around Qingming festival. White downy tips are quality indicator.",
             "$$$", "Local variety"),
            
            ("Liu An Gua Pian (Melon Seed)", "Green", "China - Lu'an, Anhui",
             "Pan-fired, unique pulling technique, leaf only (no buds or stems)", "0%",
             "Rich, full-bodied, orchid, slightly sweet, no astringency",
             "Orchid, fresh, clean",
             "Melon seed-shaped leaves, bright green liquor",
             85, 185, "2-3 minutes",
             "3g per 150ml",
             3, "Medium (35-45mg per cup)",
             "High antioxidants, supports metabolism, robust health benefits",
             "One of China's top 10 famous teas. Unique - only tea made from leaf blade only (no buds, no stems). This creates fuller body and no astringency. Labor-intensive production.",
             "$$$$", "Local variety"),
            
            ("Tai Ping Hou Kui (Peaceful Monkey Chief)", "Green", "China - Huangshan, Anhui",
             "Pressed between cloth to create long flat leaves with vein pattern", "0%",
             "Orchid, fresh, sweet, smooth, mellow",
             "Orchid, sweet, delicate",
             "Extraordinarily long flat leaves (15cm+) with mesh pattern from cloth pressing, pale green liquor",
             85, 185, "2-3 minutes",
             "3-4g per 150ml",
             3, "Medium (35-45mg per cup)",
             "Antioxidants, supports cardiovascular health",
             "One of China's top 10 famous teas. The longest flat tea leaf in the world. Pressed between fabric, creating distinctive vein pattern. Legend says it was created by a monkey.",
             "$$$$$", "Shi Da Cha cultivar"),
            
            ("Anji Bai Cha (Anji White Tea)", "Green", "China - Anji County, Zhejiang",
             "Pan-fired (it's green tea despite 'white' name)", "0%",
             "Delicate, sweet, fresh, amino acid richness, minimal astringency",
             "Fresh, clean, sweet",
             "Pale green-white leaves, nearly clear liquor",
             80, 176, "2-3 minutes",
             "3g per 150ml",
             3, "Low-Medium (30-40mg per cup)",
             "Extremely high amino acids (especially theanine), antioxidants, calming energy",
             "Named 'white tea' because leaves appear white during early spring growth due to rare genetic mutation. Actually a green tea (pan-fired). Very high amino acid content. Prized variety rediscovered in 1980s.",
             "$$$", "Anji Bai Cha cultivar (genetic variant)"),
            
            ("Gunpowder Tea (Zhu Cha)", "Green", "China - Zhejiang Province",
             "Rolled into tight pellets, pan-fired", "0%",
             "Bold, slightly smoky, assertive, hints of coppery astringency",
             "Strong, assertive, smoky",
             "Tightly rolled pellets resembling gunpowder, yellow-green liquor",
             80, 176, "2-3 minutes",
             "1 tsp per 250ml",
             3, "Medium (40-50mg per cup)",
             "Antioxidants, energizing, supports metabolism",
             "Named by British for resemblance to gunpowder pellets. Tight rolling preserves freshness. Popular base for Moroccan mint tea. Temple of Heaven is premium grade.",
             "$$", "Various cultivars"),
            
            # OOLONG TEAS
            ("Tie Guan Yin (Iron Goddess)", "Oolong", "China - Anxi County, Fujian",
             "Rolled into tight balls, lightly to moderately oxidized", "15-40% oxidation",
             "Floral, orchid, honey, butter, chestnut (traditional roasted style more robust)",
             "Orchid fragrance, floral, sweet",
             "Tightly rolled pellets, golden-green to amber liquor (depends on style)",
             95, 203, "30 seconds to 1 minute (Gongfu)",
             "7-8g per 110ml (Gongfu) or 3g per 200ml (Western)",
             7, "Medium (30-50mg per cup)",
             "Antioxidants, supports metabolism, digestive health, mental clarity",
             "One of China's top 10 famous teas. Legend says discovered by tea farmer Wei Yin in 1720s. Two styles: Qing Xiang (light, modern, greener, 15-25% oxidation) and Nong Xiang (traditional roasted, darker, 30-40% oxidation).",
             "$$$", "Tie Guan Yin cultivar"),
            
            ("High Mountain Oolong (Gao Shan)", "Oolong", "Taiwan - Ali Shan, Li Shan, Da Yu Ling (1,000-2,600m elevation)",
             "Lightly oxidized, hand-rolled into tight balls", "15-25% oxidation",
             "Floral, orchid, buttery, creamy, sweet, clean, complex",
             "Clean, floral, orchid-like, elegant",
             "Tightly rolled emerald-green balls, pale golden liquor",
             95, 203, "45 seconds to 1 minute (Gongfu)",
             "5g per 100ml (Gongfu)",
             8, "Low-Medium (20-35mg per cup)",
             "High antioxidants, L-theanine (promotes calm alertness), supports mental clarity, gentle energy",
             "Cool high-altitude temperatures (often below 18°C/64°F) and frequent fog slow leaf growth, concentrating flavor compounds and creating sweeter, more complex flavor. Da Yu Ling (2,600m) is highest, rarest, most expensive.",
             "$$$$", "Qing Xin, Jin Xuan (Milk Oolong)"),
            
            ("Da Hong Pao (Big Red Robe)", "Oolong", "China - Wuyi Mountains, Fujian",
             "Heavily oxidized, charcoal roasted (traditional), yancha (rock tea)", "60-70% oxidation",
             "Roasted nuts, dark chocolate, stone fruit, honey, distinctive mineral 'rock rhyme' (yan yun)",
             "Rich, roasted, complex, fruity",
             "Dark brown twisted leaves, deep amber-red liquor",
             100, 212, "10-20 seconds (Gongfu first infusion)",
             "7g per 100ml (Gongfu)",
             10, "Medium-High (50-70mg per cup)",
             "Antioxidants, aids digestion, warming properties, supports metabolism",
             "One of China's top 10 famous teas. Original 6 mother trees (360+ years old) on Tianxin Rock are national treasures - now protected, no longer harvested. 20g sold for ¥208,000 (~$28,000) in 2005 auction. Commercial Da Hong Pao is from cloned bushes.",
             "$$$$$", "Qidan, Beidou cultivars (clones of mother trees)"),
            
            ("Dong Fang Mei Ren (Oriental Beauty)", "Oolong", "Taiwan - Hsinchu, Miaoli counties",
             "Insect-bitten (tea jassid), heavily oxidized, unroasted", "60-85% oxidation",
             "Natural honey, peach, ripe fruit, rose petal, muscatel wine-like notes",
             "Natural honey sweetness, fruity, floral",
             "Multicolored leaves (white, green, yellow, red, brown tips), bright amber-red liquor",
             85, 185, "1-2 minutes",
             "5g per 100ml",
             5, "Low (20-30mg per cup)",
             "Unique terpenes from insect interaction, antioxidants, gentle energy",
             "Requires tea jassid insects (jacobiasca formosana) to bite young leaves, triggering plant defense - releasing monoterpene alcohols that create honey flavor. Must be pesticide-free. Queen Victoria named it 'Oriental Beauty'. Also called Bai Hao Oolong or Champagne Oolong.",
             "$$$$", "Qing Xin Da Mao"),
            
            ("Rou Gui (Cassia/Cinnamon)", "Oolong", "China - Wuyi Mountains, Fujian",
             "Moderately oxidized, charcoal roasted, yancha (rock tea)", "40-50% oxidation",
             "Cinnamon, spice, brown sugar, fruity, mineral rock character",
             "Spicy cinnamon, sweet, roasted",
             "Dark twisted leaves, orange-amber liquor",
             100, 212, "10-20 seconds (Gongfu)",
             "7g per 100ml",
             8, "Medium (40-60mg per cup)",
             "Warming properties, aids digestion, antioxidants, metabolism support",
             "Most popular modern Wuyi yancha. Named for natural cinnamon-like flavor. Became popular in 1980s-90s, now one of Wuyi's most produced teas alongside Shui Xian.",
             "$$$", "Rou Gui cultivar"),
            
            ("Shui Xian (Narcissus/Water Sprite)", "Oolong", "China - Wuyi Mountains, Fujian (also Phoenix Mountain)",
             "Moderately oxidized, roasted, yancha or Dan Cong style", "40-60% oxidation",
             "Floral, orchid, mineral, roasted, fruity, complex",
             "Floral, roasted, elegant",
             "Long twisted dark leaves, orange-amber liquor",
             100, 212, "10-20 seconds (Gongfu)",
             "7g per 100ml",
             8, "Medium (40-60mg per cup)",
             "Antioxidants, digestive support, warming",
             "One of Wuyi's traditional teas. Lao Cong (old bush, 50+ years) is especially prized. Also grown in Phoenix Mountain as Dan Cong style. Versatile cultivar with floral character.",
             "$$$", "Shui Xian cultivar"),
            
            ("Feng Huang Dan Cong (Phoenix Single Bush)", "Oolong", "China - Fenghuang Mountain, Guangdong",
             "Moderately to heavily oxidized, often from single old trees", "60-80% oxidation",
             "Varies by variety: honey orchid, almond, ginger flower, osmanthus, magnolia, lychee",
             "Intensely aromatic, floral, fruity (depends on variety)",
             "Long twisted dark leaves, golden-orange liquor",
             100, 212, "10-15 seconds (Gongfu)",
             "7-8g per 100ml",
             8, "Medium-High (50-70mg per cup)",
             "High antioxidants, energizing, supports metabolism",
             "Over 80 varieties, each named for distinctive aroma (Mi Lan Xiang=Honey Orchid, Ya Shi Xiang=Duck Shit Aroma, etc.). Traditionally from single old trees (dan cong = single bush). Song Zhong variety trees over 600 years old exist.",
             "$$$$", "Multiple varieties/cultivars within Dan Cong family"),
            
            ("Baozhong/Pouchong", "Oolong", "Taiwan - Wenshan area, Taipei",
             "Very lightly oxidized, twisted", "10-15% oxidation (most lightly oxidized oolong)",
             "Floral, gardenia, jasmine, fresh, green, delicate",
             "Floral, fresh, clean",
             "Twisted green-brown leaves, pale yellow-green liquor",
             85, 185, "1-2 minutes",
             "5g per 100ml",
             5, "Low-Medium (25-40mg per cup)",
             "Antioxidants, gentle energy, supports metabolism",
             "Taiwan's most lightly oxidized oolong, closer to green tea. Traditional name Baozhong from paper-wrapping. Wenshan area has 200+ year tea history. Delicate, aromatic style.",
             "$$$", "Qing Xin"),
            
            ("Dong Ding (Frozen Summit)", "Oolong", "Taiwan - Dong Ding Mountain, Nantou",
             "Medium oxidation, medium roast, ball-rolled", "30-40% oxidation",
             "Roasted, nutty, fruity, honey, complex, smooth",
             "Toasted, fruity, floral undertones",
             "Tightly rolled balls, golden-amber liquor",
             95, 203, "45 seconds to 1 minute",
             "5g per 100ml",
             7, "Medium (35-50mg per cup)",
             "Antioxidants, digestive support, warming",
             "One of Taiwan's most famous oolongs. Grown at 600-800m on Dong Ding Mountain. Traditional medium-roasted style. Name means 'Frozen Summit' from misty growing conditions.",
             "$$$", "Qing Xin"),
            
            ("Jin Xuan (Milk Oolong)", "Oolong", "Taiwan - Various mid-elevation regions",
             "Lightly oxidized, ball-rolled, may be lightly roasted", "20-30% oxidation",
             "Creamy, milky, buttery, floral, smooth (natural, not flavored)",
             "Creamy, floral, sweet",
             "Rolled green balls, pale golden liquor",
             90, 194, "1-2 minutes",
             "5g per 100ml",
             6, "Low-Medium (25-40mg per cup)",
             "Antioxidants, gentle energy, smooth caffeine delivery",
             "TTES #12 cultivar developed by Taiwan Tea Research Station in 1980s. Natural creamy character (not artificially flavored despite marketing). Very popular internationally. Named after developer's grandmother 'Jin Xuan'.",
             "$$", "Jin Xuan / TTES #12 cultivar"),
            
            # BLACK TEAS
            ("First Flush Darjeeling", "Black", "India - Darjeeling, West Bengal (7,000 ft average elevation)",
             "Orthodox processing (withering, rolling, oxidation, drying)", "100% oxidation",
             "Delicate, floral, jasmine, green, muscatel hints, apricot, light astringency",
             "Floral, fruity, light",
             "Light, wiry leaves with greenish tint, pale golden liquor (lighter than typical black tea)",
             85, 185, "3-4 minutes",
             "2.5g per 250ml",
             3, "Medium (40-60mg per cup)",
             "Antioxidants, supports cardiovascular health, energizing but not overpowering",
             "Harvested late February to mid-April after winter dormancy. Most prized and expensive Darjeeling flush. Only 87 estates in limited area produce ~600,000-700,000 kg annually. Light processing preserves floral character.",
             "$$$$", "Chinary (Chinese hybrid cultivar)"),
            
            ("Second Flush Darjeeling", "Black", "India - Darjeeling, West Bengal",
             "Orthodox processing", "100% oxidation",
             "Muscatel grape, honey, caramel, fuller body, fruity, complex",
             "Wine-like, fruity, complex",
             "Darker leaves with golden tips, amber-reddish liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             3, "Medium (50-70mg per cup)",
             "Antioxidants, theaflavins, supports heart health, robust energy",
             "Harvested May-June. Most famous and sought-after Darjeeling. Distinctive muscatel (wine-like) character develops during this season. Golden tips indicate quality. Summer sun intensity creates fuller flavor than first flush.",
             "$$$$", "Chinary hybrid"),
            
            ("Assam Orthodox", "Black", "India - Brahmaputra Valley, Assam",
             "Orthodox processing (full leaf)", "100% oxidation",
             "Malty, bold, brisk, dark chocolate, caramel, robust, full-bodied",
             "Strong, malty, robust, slightly earthy",
             "Dark brown-black leaves, deep reddish-brown liquor",
             100, 212, "3-5 minutes",
             "2.5g per 250ml",
             2, "High (60-90mg per cup)",
             "High caffeine for morning energy, antioxidants, robust",
             "Camellia sinensis var. assamica discovered wild in 1823 by Robert Bruce and Charles Bruce. Large-leaf variety native to Assam. Tropical lowland production. Strong malty character perfect for breakfast, handles milk well. India's largest tea-producing region.",
             "$$", "Assamica variety"),
            
            ("CTC Assam", "Black", "India - Assam",
             "CTC (Crush-Tear-Curl) processing - granular", "100% oxidation",
             "Very malty, bold, astringent, strong, brisk",
             "Strong, malty, powerful",
             "Small uniform granules, very dark reddish-brown liquor",
             100, 212, "2-3 minutes",
             "2.5g per 250ml",
             2, "High (70-100mg per cup)",
             "Very high caffeine, strong antioxidants, energizing",
             "CTC process invented 1930s for faster production and stronger brew. Creates uniform granules that infuse quickly with intense color and flavor. Ideal for tea bags. Most Assam for export is CTC.",
             "$", "Assamica variety"),
            
            ("Keemun (Qimen)", "Black", "China - Qimen County, Anhui Province",
             "Orthodox processing, careful oxidation control", "100% oxidation",
             "Wine-like, orchid-like, fruity, floral, unsweetened cocoa, slight smokiness, pine",
             "Fragrant, wine-like, floral, distinctive 'Keemun aroma'",
             "Thin, tight, well-formed dark leaves, clear red liquor",
             95, 203, "3-4 minutes",
             "2.5g per 250ml",
             3, "Medium (40-60mg per cup)",
             "Antioxidants, supports digestion, gentle on stomach for black tea",
             "Created 1875 by Yu Ganchen after studying black tea processing in Fujian. Quickly became famous, exported worldwide. Traditional base for Earl Grey. Considered China's finest black tea. Smooth, no bitterness, complex flavor. Several grades: Hao Ya, Mao Feng, etc.",
             "$$$", "Qimen cultivar"),
            
            ("Lapsang Souchong (Zhengshan Xiaozhong)", "Black", "China - Wuyi Mountains, Fujian",
             "Smoked over pine wood fires (modern) or traditionally sun-withered and dried", "100% oxidation",
             "Pine smoke, bacon-like, campfire (smoked version) OR honey, sweet potato, longan (unsmoked traditional)",
             "Distinctive pine smoke or natural sweet fruity (traditional)",
             "Large, dark leaves, deep red-amber liquor",
             100, 212, "3-5 minutes",
             "2.5g per 250ml",
             4, "Medium (40-60mg per cup)",
             "Antioxidants, warming properties, digestive support",
             "World's first black tea, created Ming Dynasty (1500s-1600s). Traditional Zhengshan Xiaozhong is unsmoked, fruity. Pine-smoked version developed for export market. Authentic production area very limited in Tongmu village, Wuyi Nature Reserve. Smoked version popular in West, traditional version preferred in China.",
             "$$$", "Wuyi variety"),
            
            ("Dian Hong (Yunnan Gold)", "Black", "China - Yunnan Province",
             "Orthodox processing using large-leaf assamica", "100% oxidation",
             "Honey, sweet, malty, fruity, sweet potato, chocolate, pepper, hazelnut",
             "Sweet, malty, rich, slightly peppery",
             "Large leaves with abundant golden tips, bright orange-red liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             4, "Medium (40-60mg per cup)",
             "Antioxidants, naturally sweet (low bitterness), gentle energy",
             "Created 1939 during WWII when transport routes from Fujian were cut. Uses large-leaf Yunnan assamica variety (same as pu-erh). More golden tips = higher quality. Jin Ya (Golden Bud) is pure tips. Smooth, naturally sweet, little astringency.",
             "$$$", "Yunnan large-leaf assamica"),
            
            ("Nuwara Eliya", "Black", "Sri Lanka - Nuwara Eliya region (6,000+ ft elevation)",
             "Orthodox processing", "100% oxidation",
             "Delicate, floral, citrus, light-bodied, bright, fragrant",
             "Fragrant, delicate, floral",
             "Wiry leaves, light copper-amber liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             3, "Medium (40-60mg per cup)",
             "Antioxidants, supports metabolism, bright energy",
             "Highest elevation Ceylon tea region, called 'Champagne of Ceylon teas'. Light and delicate, similar character to Darjeeling. Cool climate (10-15°C) creates refined flavor. Year-round production but January-March produces finest tea.",
             "$$$", "Ceylon variety (Assam cultivar adapted)"),
            
            ("Keemun Hao Ya", "Black", "China - Qimen County, Anhui",
             "Orthodox processing, highest grade Keemun", "100% oxidation",
             "Refined orchid, wine-like, fruity, smooth, complex, delicate cocoa",
             "Orchid, wine-like, sophisticated",
             "Beautiful whole leaves with golden tips, clear ruby-red liquor",
             95, 203, "3-4 minutes",
             "2.5g per 250ml",
             3, "Medium (40-60mg per cup)",
             "High antioxidants, smooth, refined energy",
             "Highest grade of Keemun tea. Hao Ya means 'fine bud'. Carefully hand-processed whole leaves with tips. Most refined, expensive Keemun. Smooth, complex, no astringency.",
             "$$$$", "Qimen cultivar"),
            
            ("Jin Jun Mei (Golden Eyebrow)", "Black", "China - Wuyi Mountains, Fujian (Tongmu village)",
             "Orthodox processing, made only from golden buds", "100% oxidation",
             "Honey, fruity, sweet, smooth, chocolate, longan fruit, no astringency",
             "Sweet, honey, fruity, complex",
             "Pure golden buds, bright golden-orange liquor",
             90, 194, "2-3 minutes (very quick due to bud tenderness)",
             "3-4g per 150ml",
             5, "Medium (40-60mg per cup)",
             "High antioxidants, smooth energy, gentle on stomach",
             "Created 2005 in Tongmu village (same area as Lapsang Souchong). Requires 50,000-60,000 buds per 500g. Extremely expensive premium tea. Sweet, fruity, smooth, zero bitterness. Revolutionary modern Chinese black tea.",
             "$$$$$", "Wuyi variety"),
            
            ("Nilgiri", "Black", "India - Nilgiri Hills (Blue Mountains), Tamil Nadu",
             "Orthodox or CTC processing", "100% oxidation",
             "Fragrant, bright, brisk, smooth, slight fruity notes",
             "Clean, bright, fresh",
             "Dark leaves, bright red-brown liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             3, "Medium (40-60mg per cup)",
             "Antioxidants, smooth caffeine, bright energy",
             "Grown at 1,000-2,500m elevation in South India. Year-round production due to tropical climate with two monsoons. Known for bright, clean, fragrant character. Often blended. Good value for quality.",
             "$$", "South Indian variety"),
            
            ("Uva", "Black", "Sri Lanka - Uva Province (3,000-5,000 ft)",
             "Orthodox processing", "100% oxidation",
             "Bold, full-bodied, slightly astringent, menthol-like cooling, rose-like",
             "Strong, distinctive, wine-like",
             "Long wiry leaves, deep reddish-brown liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             3, "Medium-High (50-70mg per cup)",
             "Antioxidants, energizing, robust",
             "Famous Ceylon tea region. Dry season (July-September) produces best quality with distinctive seasonal character. Unique cooling, menthol-like astringency. Strong, full flavor. Famous estates include Kahawatte, Aislaby.",
             "$$$", "Ceylon variety"),
            
            ("Dimbula", "Black", "Sri Lanka - Dimbula region (3,500-5,000 ft)",
             "Orthodox processing", "100% oxidation",
             "Full-bodied, strong, crisp, slightly fruity",
             "Robust, crisp",
             "Wiry dark leaves, bright red-brown liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             3, "Medium (45-65mg per cup)",
             "Antioxidants, energizing",
             "Western slope of central Sri Lankan hills. January-February produces finest tea. Strong, crisp character. One of Ceylon's major tea regions.",
             "$$", "Ceylon variety"),
            
            ("Kandy", "Black", "Sri Lanka - Kandy district (2,000-4,000 ft mid-elevation)",
             "Orthodox processing", "100% oxidation",
             "Full-bodied, strong, slightly harsh, powerful",
             "Strong, robust",
             "Dark leaves, deep copper-red liquor",
             95, 203, "3-5 minutes",
             "2.5g per 250ml",
             3, "Medium-High (50-70mg per cup)",
             "Antioxidants, high energy",
             "Historic region where James Taylor established Ceylon's first commercial tea estate in 1867 at Loolecondera. Mid-elevation teas. Strong, full-bodied character.",
             "$$", "Ceylon variety"),
            
            # PU-ERH TEAS
            ("Sheng Pu-erh (Raw)", "Pu-erh", "China - Yunnan Province (various mountains: Bulang, Yiwu, etc.)",
             "Sun-dried maocha, naturally aged or stored young", "Varies with age (minimal when young, complex when aged)",
             "Bright, vegetal, floral, fruity (young) transforming to dried fruits, plum, camphor, leather, tobacco (aged 10-30+ years)",
             "Fresh and vegetal (young) or deep, complex, earthy-sweet (aged)",
             "Compressed cakes (bing), tuo, brick; golden-green (young) to dark amber-brown (aged) liquor",
             95, 203, "10-20 seconds first infusion (rinse), then 15-30 seconds",
             "6-8g per 100ml (Gongfu)",
             15, "Medium-High (60-80mg per cup for young, less for aged)",
             "Supports digestion, may aid weight management, complex antioxidants (age-dependent), microbial benefits from aging",
             "Designed for long-term aging (15-50+ years optimal). Transforms dramatically with proper storage (humidity 60-70%, temp 20-28°C). Young sheng can be very astringent. Ancient tree (gushu) material is most prized. Major mountains: Bulang, Yiwu, Bada, Ban Zhang.",
             "$$$-$$$$$", "Ancient tree, wild arbor, plantation"),
            
            ("Shou Pu-erh (Ripe/Cooked)", "Pu-erh", "China - Yunnan Province",
             "Pile fermentation (wo dui) 45-90 days, accelerated microbial aging", "Post-fermented (microbial, not oxidation)",
             "Earthy, smooth, dark chocolate, forest floor, leather, dates, woody, sweet",
             "Earthy, woody, aged, loamy",
             "Dark brown-black compressed cakes, very dark brown opaque liquor",
             100, 212, "5-10 seconds first infusion (rinse twice!), then 10-20 seconds",
             "6-8g per 100ml (Gongfu)",
             20, "Low-Medium (20-40mg per cup - caffeine reduced during fermentation)",
             "Excellent for digestion, may aid weight loss, modulates gut microbiota, may lower cholesterol, very gentle on stomach",
             "Developed 1973 by Kunming Tea Factory (Menghai Factory) to mimic aged sheng quickly. Uses controlled microbial fermentation (wo dui = wet piling). Ready to drink immediately. MUST rinse twice before drinking to remove dust and wake tea. Improves with 3-5 years aging.",
             "$$-$$$$", "Various plantation cultivars"),
            
            # YELLOW TEAS
            ("Jun Shan Yin Zhen (Junshan Silver Needle)", "Yellow", "China - Junshan Island, Dongting Lake, Hunan",
             "Men huan (sealed yellowing) 24-72 hours - unique to yellow tea", "5-10% oxidation (slow enzymatic during sealing)",
             "Fresh sugarcane, wildflowers, smooth, mellow, sweet, delicate",
             "Delicate, sweet, sophisticated, floral",
             "Golden-yellow uniform buds, bright yellow liquor, 'dancing leaves' stand upright in glass",
             80, 176, "3-4 minutes",
             "3g per 150ml",
             3, "Low (20-30mg per cup)",
             "Gentler on stomach than green tea, antioxidants, aids digestion, less caffeine than green",
             "Most prestigious yellow tea. One of China's top 10 famous teas. Only ~500-1,000 kg produced annually from tiny island (0.96 km²). Yellow tea nearly extinct - few producers remain. Leaves perform 'dance' standing vertically in glass 3 times. Tribute tea for emperors.",
             "$$$$$", "Local variety"),
            
            ("Meng Ding Huang Ya (Yellow Buds)", "Yellow", "China - Mount Meng, Sichuan",
             "Men huan (sealed yellowing) process", "5-10% oxidation",
             "Sweet, mellow, floral, nutty, smooth",
             "Sweet, delicate, pleasant",
             "Yellow-green buds and leaves, yellow liquor",
             80, 176, "2-3 minutes",
             "3g per 150ml",
             3, "Low (20-30mg per cup)",
             "Gentle on stomach, antioxidants, calming",
             "Mount Meng is legendary birthplace of tea cultivation. Yellow tea produced here for over 2,000 years. Milder than green tea due to yellowing process.",
             "$$$$", "Local variety"),
            
            ("Huo Shan Huang Ya (Yellow Buds)", "Yellow", "China - Huoshan County, Anhui",
             "Men huan (sealed yellowing)", "5-10% oxidation",
             "Sweet, mellow, slightly nutty",
             "Delicate, sweet",
             "Small yellow-green leaves, yellow liquor",
             80, 176, "2-3 minutes",
             "3g per 150ml",
             3, "Low (20-30mg per cup)",
             "Gentle energy, digestive support, antioxidants",
             "Historic yellow tea from Anhui province. Rare production. Yellow tea processing creates mellow, sweet flavor without green tea's grassiness.",
             "$$$$", "Local variety"),
        ]
        
        # Insert tea data
        self.cursor.executemany('''
            INSERT INTO teas (name, category, origin, processing, oxidation,
                            flavor_profile, aroma, appearance, brew_temp_c, brew_temp_f,
                            steep_time, tea_water_ratio, reinfusions, caffeine_level,
                            health_benefits, history, price_range, cultivars)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', teas_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(teas_data)} tea varieties (corrected data)")
    
    def populate_cultivars(self):
        """NEW: Populate cultivars table with tea plant varieties"""
        cultivars_data = [
            # SPECIES
            ("Camellia sinensis var. sinensis", "C. sinensis var. sinensis", "China",
             "Small leaf", "Small leaves (4-6cm), cold-hardy, high quality",
             "Most Chinese and Japanese teas, high-quality teas",
             "Original Chinese variety, adapted to cooler climates"),
            
            ("Camellia sinensis var. assamica", "C. sinensis var. assamica", "Assam, India / Yunnan, China",
             "Large leaf", "Large leaves (15-20cm), tropical, robust growth",
             "Assam black teas, Yunnan black and pu-erh teas",
             "Discovered wild in Assam 1823, also native to Yunnan"),
            
            # JAPANESE CULTIVARS
            ("Yabukita", "C. sinensis var. sinensis", "Japan",
             "Small leaf", "Cold-resistant, high-yielding, balanced flavor",
             "75% of Japanese tea production - Sencha, Gyokuro, Matcha",
             "Developed 1908, selected 1953. Dominates Japanese tea industry"),
            
            ("Samidori", "C. sinensis var. sinensis", "Japan",
             "Small leaf", "Rich umami, high amino acids, excellent for shading",
             "Premium Gyokuro, ceremonial Matcha",
             "Prized for sweet flavor and umami richness"),
            
            ("Okumidori", "C. sinensis var. sinensis", "Japan",
             "Small leaf", "Sweet, mild, high theanine",
             "Gyokuro, Matcha, premium Sencha",
             "Literally 'Deep Green', excellent shaded tea cultivar"),
            
            ("Asahi", "C. sinensis var. sinensis", "Japan",
             "Small leaf", "Natural sweetness, delicate, vivid green color",
             "High-grade Matcha, Gyokuro",
             "Rare, difficult to cultivate, highly prized for matcha"),
            
            ("Saemidori", "C. sinensis var. sinensis", "Japan",
             "Small leaf", "Strong umami, sweet, vibrant green",
             "Sencha, Gyokuro, Matcha",
             "Popular in Kagoshima, good balance of flavor and yield"),
            
            ("Benifuuki", "C. sinensis var. sinensis", "Japan",
             "Small leaf", "High in methylated catechins (anti-allergy)",
             "Black tea, specialty green tea for health",
             "Originally for black tea, now studied for allergy relief"),
            
            # CHINESE CULTIVARS
            ("Longjing #43", "C. sinensis var. sinensis", "China",
             "Small leaf", "Early-budding, suited for Longjing production",
             "Longjing (Dragon Well) green tea",
             "Developed for West Lake Longjing, accounts for 80% of production"),
            
            ("Tieguanyin cultivar", "C. sinensis var. sinensis", "China",
             "Small leaf", "Distinctive orchid aroma, thick leaves",
             "Tieguanyin oolong tea",
             "Origin variety from Anxi, Fujian. Authentic TGY must use this cultivar"),
            
            ("Fuding Da Bai (Fuding Big White)", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Large buds, abundant white hair, early-budding",
             "White teas (Silver Needle, White Peony), some green teas",
             "National Tea Cultivar #1, essential for authentic Fujian white tea"),
            
            ("Da Bai", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Large white downy buds",
             "White teas, particularly Silver Needle",
             "Big White cultivar, prized for white tea production"),
            
            ("Xiao Bai", "C. sinensis var. sinensis", "China",
             "Small leaf", "Smaller buds, traditional variety",
             "Gong Mei, Shou Mei white teas",
             "Small White cultivar, used for lower-grade white teas"),
            
            ("Qimen cultivar", "C. sinensis var. sinensis", "China",
             "Small leaf", "Suited for black tea processing, aromatic",
             "Keemun black tea",
             "Specific to Qimen County, Anhui, creates distinctive Keemun aroma"),
            
            ("Qi Lan (Rare Orchid)", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Natural orchid fragrance",
             "Wuyi Rock Oolong",
             "Wuyi cultivar with distinctive orchid aroma"),
            
            ("Rou Gui cultivar", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Natural cinnamon-spice character",
             "Rou Gui Wuyi Rock Oolong",
             "Creates natural cinnamon flavor, very popular Wuyi cultivar"),
            
            ("Shui Xian cultivar", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Versatile, floral, ages well",
             "Shui Xian oolong (Wuyi and Fenghuang styles)",
             "One of oldest and most widespread oolong cultivars"),
            
            ("Qidan", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Clone of original Da Hong Pao mother trees",
             "Da Hong Pao and Wuyi Rock Oolongs",
             "Asexually propagated from the original ancient mother bushes"),
            
            ("Beidou", "C. sinensis var. sinensis", "China",
             "Medium leaf", "Another clone of Da Hong Pao mother trees",
             "Da Hong Pao and Wuyi Rock Oolongs",
             "Alternative clone lineage from mother trees"),
            
            # TAIWANESE CULTIVARS
            ("Qing Xin (Green Heart)", "C. sinensis var. sinensis", "Taiwan",
             "Medium leaf", "Complex flavor, traditional Taiwan oolong cultivar",
             "High Mountain Oolong, Dong Ding, Baozhong, Oriental Beauty",
             "Original Taiwan oolong cultivar, brought from Fujian 200+ years ago"),
            
            ("Jin Xuan (TTES #12)", "C. sinensis var. sinensis", "Taiwan",
             "Medium leaf", "Natural creamy, milky character",
             "Milk Oolong, various Taiwan oolongs",
             "Developed by Taiwan Tea Research Station, released 1981. Named after grandmother"),
            
            ("Cui Yu (TTES #13)", "C. sinensis var. sinensis", "Taiwan",
             "Medium leaf", "Floral, light, aromatic",
             "Jade Oolong, light oolongs",
             "Developed alongside Jin Xuan, lighter character"),
            
            ("Qing Xin Da Mao", "C. sinensis var. sinensis", "Taiwan",
             "Large leaf", "Large leaf mutation, essential for Oriental Beauty",
             "Oriental Beauty (Dong Fang Mei Ren)",
             "Attracts tea jassid insects essential for Oriental Beauty's unique flavor"),
            
            ("Ruan Zhi", "C. sinensis var. sinensis", "Taiwan",
             "Medium leaf", "Soft stem, easy processing",
             "Various Taiwan oolongs",
             "Literally 'Soft Stem', easier to process than Qing Xin"),
            
            ("Si Ji Chun (Four Seasons Spring)", "C. sinensis var. sinensis", "Taiwan",
             "Medium leaf", "Produces quality tea year-round",
             "Four Seasons Oolong",
             "Can harvest 5-6 times yearly with consistent quality"),
            
            # INDIAN CULTIVARS
            ("Chinary", "Hybrid", "Darjeeling, India",
             "Medium leaf", "Chinese-Indian hybrid, adapted to Darjeeling altitude",
             "Darjeeling First and Second Flush",
             "Chinese tea plants adapted to Himalayan conditions, creates Darjeeling character"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO cultivars (name, species, origin_country, leaf_size, characteristics, common_uses, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', cultivars_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(cultivars_data)} cultivar varieties")
    
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
        print(f"✓ Inserted {len(regions_data)} tea regions")
    
    def initialize_database(self, force_rebuild=False):
        """Create and populate the entire database"""
        self.connect()
        
        if force_rebuild:
            print("Rebuilding database from scratch...")
            self.drop_tables()
        
        self.create_tables()
        
        # Check if already populated
        self.cursor.execute("SELECT COUNT(*) FROM teas")
        tea_count = self.cursor.fetchone()[0]
        
        if tea_count == 0 or force_rebuild:
            print("Populating database with corrected tea data...")
            self.populate_teas()
            self.populate_cultivars()
            self.populate_regions()
            print("\n✓ Database initialization complete!")
            print(f"  Total teas: {len([1 for _ in self.cursor.execute('SELECT * FROM teas')])} varieties")
            print(f"  Total cultivars: {len([1 for _ in self.cursor.execute('SELECT * FROM cultivars')])} varieties")
            print(f"  Total regions: {len([1 for _ in self.cursor.execute('SELECT * FROM regions')])} regions")
        else:
            print(f"Database already contains {tea_count} teas")
            print("Use force_rebuild=True to recreate database")
        
        self.close()

def main():
    """Initialize the tea database"""
    import sys
    force = '--force' in sys.argv or '-f' in sys.argv
    
    db = TeaDatabase()
    db.initialize_database(force_rebuild=force)
    
    if not force:
        print("\nTo force rebuild database, run: python tea_database_corrected.py --force")

if __name__ == "__main__":
    main()
