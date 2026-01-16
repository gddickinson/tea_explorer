"""
Tea Blends Database
Comprehensive database of popular tea blends and flavoured teas
"""

import sqlite3
from pathlib import Path

class BlendsDatabase:
    def __init__(self, db_path="tea_collection.db"):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
    def create_tables(self):
        """Create blends table"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blends (
                blend_id INTEGER PRIMARY KEY AUTOINCREMENT,
                blend_name TEXT NOT NULL,
                category TEXT NOT NULL,
                base_tea TEXT,
                ingredients TEXT NOT NULL,
                flavor_profile TEXT,
                aroma TEXT,
                appearance TEXT,
                brew_temp_c INTEGER,
                brew_temp_f INTEGER,
                steep_time TEXT,
                caffeine_level TEXT,
                health_benefits TEXT,
                origin_region TEXT,
                history TEXT,
                price_range TEXT,
                popular_brands TEXT,
                description TEXT,
                serving_suggestions TEXT
            )
        ''')
        
        self.conn.commit()
        
    def populate_blends(self):
        """Populate with blend data"""
        cursor = self.conn.cursor()
        
        # First, clear existing data
        cursor.execute("DELETE FROM blends")
        
        blends_data = [
            # TRADITIONAL BRITISH BLENDS
            {
                'blend_name': 'Earl Grey',
                'category': 'Flavoured Black Tea',
                'base_tea': 'Black tea (typically Chinese Keemun)',
                'ingredients': 'Black tea, bergamot oil (from Citrus bergamia)',
                'flavor_profile': 'Citrusy, floral, slightly sweet with distinctive bergamot character',
                'aroma': 'Strong citrus, aromatic bergamot essence',
                'appearance': 'Dark brown-black liquor',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Medium-High (40-70mg per cup)',
                'health_benefits': 'Antioxidants from black tea, bergamot may aid digestion and stress relief, supports heart health',
                'origin_region': 'England (created for 2nd Earl Grey)',
                'history': 'Created in the 1830s for Charles Grey, 2nd Earl Grey. Legend says it was designed to offset the lime flavor in well water at his estate. Named after British Prime Minister Earl Grey.',
                'price_range': '$5-25 per 100g',
                'popular_brands': 'Twinings, Fortnum & Mason, Harney & Sons, Ahmad Tea, Bigelow, Tazo',
                'description': 'The most famous flavoured tea in the world, beloved for its distinctive bergamot citrus note.',
                'serving_suggestions': 'Traditionally served with milk and sugar, also excellent iced or as London Fog (with steamed milk and vanilla)'
            },
            {
                'blend_name': 'Lady Grey',
                'category': 'Flavoured Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, bergamot oil, lemon peel, orange peel, cornflower petals',
                'flavor_profile': 'Lighter, more floral than Earl Grey with citrus notes',
                'aroma': 'Delicate bergamot with sweet citrus and floral hints',
                'appearance': 'Medium brown with blue cornflower petals',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '3-4 minutes',
                'caffeine_level': 'Medium (40-60mg per cup)',
                'health_benefits': 'Similar to Earl Grey, with additional vitamin C from citrus peels',
                'origin_region': 'England (Twinings creation)',
                'history': 'Created by Twinings in the 1990s as a lighter alternative to Earl Grey. Named to complement the Earl Grey name.',
                'price_range': '$6-20 per 100g',
                'popular_brands': 'Twinings (original), Ahmad Tea',
                'description': 'A gentler, more floral interpretation of Earl Grey with additional citrus elements.',
                'serving_suggestions': 'Delightful on its own or with light sweetener, excellent iced'
            },
            {
                'blend_name': 'English Breakfast',
                'category': 'Traditional Black Blend',
                'base_tea': 'Blend of Assam, Ceylon, and/or Kenyan black teas',
                'ingredients': 'Assam black tea, Ceylon black tea, sometimes Kenyan tea',
                'flavor_profile': 'Full-bodied, robust, malty, slightly sweet',
                'aroma': 'Rich, malty, warming',
                'appearance': 'Deep amber to reddish-brown',
                'brew_temp_c': 100,
                'brew_temp_f': 212,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'High (50-90mg per cup)',
                'health_benefits': 'High in antioxidants, may improve heart health, aids alertness and focus',
                'origin_region': 'England',
                'history': 'Developed in the 1800s as a hearty tea to accompany the traditional English breakfast. Designed to stand up to milk and sugar.',
                'price_range': '$4-30 per 100g',
                'popular_brands': 'Twinings, Yorkshire Tea, PG Tips, Tetley, Harney & Sons, Fortnum & Mason',
                'description': 'The quintessential British tea, strong enough to wake you up and pair with a full breakfast.',
                'serving_suggestions': 'Best with milk and sugar, pairs excellently with breakfast foods, scones, or biscuits'
            },
            {
                'blend_name': 'Irish Breakfast',
                'category': 'Traditional Black Blend',
                'base_tea': 'Primarily Assam black tea',
                'ingredients': 'Assam black tea (higher proportion than English Breakfast)',
                'flavor_profile': 'Very robust, strong, malty, full-bodied',
                'aroma': 'Intense, malty, rich',
                'appearance': 'Deep reddish-brown',
                'brew_temp_c': 100,
                'brew_temp_f': 212,
                'steep_time': '4-5 minutes',
                'caffeine_level': 'Very High (60-90mg per cup)',
                'health_benefits': 'High antioxidants, excellent for morning alertness, supports cardiovascular health',
                'origin_region': 'Ireland',
                'history': 'Developed for the Irish preference for a stronger, more robust morning tea. Traditionally paired with hearty Irish breakfasts.',
                'price_range': '$5-25 per 100g',
                'popular_brands': 'Barry\'s Tea, Lyons, Bewley\'s, Nambarrie, Thompson\'s',
                'description': 'Stronger and maltier than English Breakfast, designed for those who like their tea bold.',
                'serving_suggestions': 'Almost always served with milk, traditionally quite strong ("builder\'s tea"), excellent with hearty breakfast'
            },
            {
                'blend_name': 'Scottish Breakfast',
                'category': 'Traditional Black Blend',
                'base_tea': 'Blend of strong black teas',
                'ingredients': 'Assam, Ceylon, sometimes Chinese black tea',
                'flavor_profile': 'Bold, malty, full-bodied, slightly smoky',
                'aroma': 'Robust, malty',
                'appearance': 'Deep amber-brown',
                'brew_temp_c': 100,
                'brew_temp_f': 212,
                'steep_time': '4-5 minutes',
                'caffeine_level': 'High (60-85mg per cup)',
                'health_benefits': 'High in antioxidants, energizing',
                'origin_region': 'Scotland',
                'history': 'Created to pair with traditional Scottish breakfast foods and the Scottish preference for strong tea.',
                'price_range': '$6-28 per 100g',
                'popular_brands': 'Twinings, Harney & Sons, Scottish Blend, Brodies',
                'description': 'A robust blend for those who enjoy their tea strong and malty.',
                'serving_suggestions': 'Typically served with milk, pairs well with oatmeal and traditional Scottish breakfast'
            },
            
            # CHAI & SPICED BLENDS
            {
                'blend_name': 'Masala Chai',
                'category': 'Spiced Black Tea',
                'base_tea': 'Strong black tea (usually Assam or CTC)',
                'ingredients': 'Black tea, cardamom, cinnamon, ginger, cloves, black pepper, sometimes star anise, fennel seeds',
                'flavor_profile': 'Spicy, warming, sweet when prepared with milk and sugar',
                'aroma': 'Aromatic spices, warming, complex',
                'appearance': 'Milky brown when prepared traditionally',
                'brew_temp_c': 100,
                'brew_temp_f': 212,
                'steep_time': '5-10 minutes (boiled with spices)',
                'caffeine_level': 'Medium-High (40-70mg per cup)',
                'health_benefits': 'Aids digestion, anti-inflammatory from ginger and spices, warming properties',
                'origin_region': 'India',
                'history': 'Ancient blend from India, traditionally prepared by boiling tea, spices, milk, and sugar together. Each family has their own recipe.',
                'price_range': '$6-20 per 100g',
                'popular_brands': 'Vahdam, Organic India, Tazo, Oregon Chai, Yogi Tea',
                'description': 'India\'s beloved spiced tea, traditionally prepared with milk and served as a warming, comforting beverage.',
                'serving_suggestions': 'Traditionally boiled with milk and sugar, can also be made as concentrate or latte, pairs with samosas or biscuits'
            },
            {
                'blend_name': 'Chai Latte Blend',
                'category': 'Spiced Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, cinnamon, cardamom, ginger, cloves, vanilla, sometimes honey powder',
                'flavor_profile': 'Sweet-spicy, creamy when prepared with milk, vanilla undertones',
                'aroma': 'Sweet spices, vanilla, cinnamon-forward',
                'appearance': 'Light brown with milk',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '5-7 minutes',
                'caffeine_level': 'Medium (35-60mg per cup)',
                'health_benefits': 'Antioxidants, digestive support from spices',
                'origin_region': 'Western adaptation of Indian chai',
                'history': 'Popularized by coffee shops in the 1990s as a sweeter, more accessible version of traditional masala chai.',
                'price_range': '$8-25 per 100g',
                'popular_brands': 'Starbucks, Tazo, Oregon Chai, David\'s Tea, Teavana',
                'description': 'A Western interpretation of chai, designed for latte-style preparation with a sweeter profile.',
                'serving_suggestions': 'Mix with steamed milk and sweetener, can add vanilla syrup, popular as both hot and iced latte'
            },
            
            # FRUITY & FLORAL BLENDS
            {
                'blend_name': 'Peach Tea',
                'category': 'Flavoured Black/White Tea',
                'base_tea': 'Black or white tea',
                'ingredients': 'Tea base, peach pieces, natural peach flavoring, sometimes marigold petals',
                'flavor_profile': 'Sweet, fruity, peachy, refreshing',
                'aroma': 'Sweet peach, fruity',
                'appearance': 'Golden amber with fruit pieces',
                'brew_temp_c': 90,
                'brew_temp_f': 194,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Low-Medium (20-40mg per cup)',
                'health_benefits': 'Antioxidants from tea base, vitamins from fruit',
                'origin_region': 'Modern creation',
                'history': 'Popularized in the 20th century, especially as iced tea in the American South.',
                'price_range': '$7-20 per 100g',
                'popular_brands': 'Celestial Seasonings, Lipton, Teavana, Harney & Sons',
                'description': 'A popular fruity blend, excellent both hot and iced.',
                'serving_suggestions': 'Delicious iced with sweetener, pairs with light desserts, refreshing on hot days'
            },
            {
                'blend_name': 'Strawberry Fields',
                'category': 'Flavoured Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, strawberry pieces, strawberry leaves, natural strawberry flavor',
                'flavor_profile': 'Sweet berry, slightly tart, fruity',
                'aroma': 'Fresh strawberries, sweet',
                'appearance': 'Reddish-brown with strawberry pieces',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '3-4 minutes',
                'caffeine_level': 'Medium (35-55mg per cup)',
                'health_benefits': 'Antioxidants, vitamin C from strawberries',
                'origin_region': 'Modern blend',
                'history': 'Created as part of the flavored tea boom in the late 20th century.',
                'price_range': '$8-22 per 100g',
                'popular_brands': 'Harney & Sons, David\'s Tea, Teavana',
                'description': 'A sweet, fruity blend perfect for those who enjoy berry flavors.',
                'serving_suggestions': 'Excellent iced, can add vanilla or cream, pairs with scones or fruit tarts'
            },
            {
                'blend_name': 'Mango Tea',
                'category': 'Flavoured Black/Green Tea',
                'base_tea': 'Black or green tea',
                'ingredients': 'Tea base, mango pieces, natural mango flavoring, calendula petals',
                'flavor_profile': 'Tropical, sweet, fruity, exotic',
                'aroma': 'Sweet mango, tropical fruit',
                'appearance': 'Golden with orange-yellow fruit pieces',
                'brew_temp_c': 85,
                'brew_temp_f': 185,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Low-Medium (20-45mg per cup)',
                'health_benefits': 'Vitamin A and C from mango, antioxidants from tea',
                'origin_region': 'Modern tropical blend',
                'history': 'Developed to capture tropical fruit flavors in tea form.',
                'price_range': '$8-24 per 100g',
                'popular_brands': 'Teavana, David\'s Tea, Adagio',
                'description': 'A tropical escape in a cup, popular for both hot and iced tea.',
                'serving_suggestions': 'Excellent iced with coconut milk, pairs with tropical fruits or Thai cuisine'
            },
            {
                'blend_name': 'Rose Tea',
                'category': 'Flavoured Black/Green Tea',
                'base_tea': 'Black, green, or oolong tea',
                'ingredients': 'Tea base, rose petals, rose buds, natural rose essence',
                'flavor_profile': 'Floral, delicate, slightly sweet, aromatic',
                'aroma': 'Rose garden, floral, perfumed',
                'appearance': 'Pink-tinted with rose petals',
                'brew_temp_c': 85,
                'brew_temp_f': 185,
                'steep_time': '3-4 minutes',
                'caffeine_level': 'Low-Medium (15-40mg per cup)',
                'health_benefits': 'Relaxation, aromatherapy benefits, antioxidants, may reduce anxiety',
                'origin_region': 'Middle East, China, France',
                'history': 'Used in Chinese and Middle Eastern tea traditions for centuries. Popular in Persian and Moroccan tea culture.',
                'price_range': '$10-35 per 100g',
                'popular_brands': 'Harney & Sons, Mariage Frères, Dammann Frères',
                'description': 'An elegant, aromatic blend perfect for afternoon tea.',
                'serving_suggestions': 'Serve plain or lightly sweetened, pairs with delicate pastries, Turkish delight, or Persian sweets'
            },
            {
                'blend_name': 'Jasmine Pearl Tea',
                'category': 'Scented Green Tea',
                'base_tea': 'Green tea (hand-rolled pearls)',
                'ingredients': 'Green tea leaves rolled with jasmine flowers',
                'flavor_profile': 'Floral, sweet, delicate green tea base',
                'aroma': 'Intensely floral jasmine',
                'appearance': 'Pearl-shaped leaves unfurling, pale yellow-green liquor',
                'brew_temp_c': 80,
                'brew_temp_f': 176,
                'steep_time': '2-3 minutes',
                'caffeine_level': 'Low-Medium (25-45mg per cup)',
                'health_benefits': 'Antioxidants, calming properties, may aid relaxation',
                'origin_region': 'Fujian Province, China',
                'history': 'Traditional Chinese scenting process where tea is layered with jasmine flowers over multiple nights.',
                'price_range': '$15-60 per 100g',
                'popular_brands': 'Rishi Tea, Harney & Sons, Teavana',
                'description': 'A beautiful display tea where pearls unfurl to release jasmine aroma.',
                'serving_suggestions': 'Best enjoyed plain to appreciate delicate flavors, excellent as a palate cleanser'
            },
            
            # CHOCOLATE & DESSERT BLENDS
            {
                'blend_name': 'Chocolate Chai',
                'category': 'Flavoured Spiced Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, cacao nibs, cinnamon, cardamom, ginger, cloves, natural chocolate flavor',
                'flavor_profile': 'Rich chocolate with warm spices, slightly sweet',
                'aroma': 'Chocolate and cinnamon, warming spices',
                'appearance': 'Dark brown',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '5-7 minutes',
                'caffeine_level': 'Medium (40-60mg per cup)',
                'health_benefits': 'Antioxidants from tea and cacao, mood-boosting from chocolate',
                'origin_region': 'Modern fusion blend',
                'history': 'Created in the 21st century as a fusion of chai spices and chocolate.',
                'price_range': '$10-28 per 100g',
                'popular_brands': 'David\'s Tea, Tazo, Teavana',
                'description': 'A decadent blend combining the warmth of chai with chocolate richness.',
                'serving_suggestions': 'Excellent with milk and sweetener, makes a great dessert tea, pairs with chocolate or spice cookies'
            },
            {
                'blend_name': 'Vanilla Caramel Tea',
                'category': 'Flavoured Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, vanilla pieces, natural caramel flavoring, sometimes toffee pieces',
                'flavor_profile': 'Sweet, creamy, vanilla-caramel, dessert-like',
                'aroma': 'Sweet vanilla, caramel',
                'appearance': 'Dark amber',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Medium (40-65mg per cup)',
                'health_benefits': 'Antioxidants from black tea, comforting properties',
                'origin_region': 'Modern dessert blend',
                'history': 'Part of the dessert tea trend of the early 2000s.',
                'price_range': '$9-25 per 100g',
                'popular_brands': 'David\'s Tea, Teavana, Harney & Sons',
                'description': 'A sweet, indulgent blend for those with a sweet tooth.',
                'serving_suggestions': 'Lovely with milk, excellent dessert substitute, pairs with biscotti or shortbread'
            },
            
            # MINT & HERBAL BLENDS
            {
                'blend_name': 'Moroccan Mint',
                'category': 'Flavoured Green Tea',
                'base_tea': 'Chinese gunpowder green tea',
                'ingredients': 'Gunpowder green tea, spearmint leaves',
                'flavor_profile': 'Fresh, minty, slightly bitter green tea base, sweet mint',
                'aroma': 'Cool mint, fresh',
                'appearance': 'Bright green-yellow',
                'brew_temp_c': 80,
                'brew_temp_f': 176,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Medium (30-50mg per cup)',
                'health_benefits': 'Digestive aid, refreshing, antioxidants, may help with nausea',
                'origin_region': 'Morocco, North Africa',
                'history': 'Traditional Moroccan tea, central to hospitality and social customs. Served throughout the day.',
                'price_range': '$6-18 per 100g',
                'popular_brands': 'Numi, Harney & Sons, Traditional Moroccan brands',
                'description': 'The beloved tea of Morocco, served sweet as a symbol of hospitality.',
                'serving_suggestions': 'Traditionally served very sweet, poured from height for aeration, excellent after meals'
            },
            {
                'blend_name': 'Chocolate Mint',
                'category': 'Flavoured Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, peppermint leaves, cacao nibs, natural chocolate-mint flavoring',
                'flavor_profile': 'Cool mint with chocolate undertones, refreshing',
                'aroma': 'Peppermint and chocolate',
                'appearance': 'Dark brown',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Medium (35-55mg per cup)',
                'health_benefits': 'Digestive aid from mint, antioxidants from tea and cacao',
                'origin_region': 'Modern blend',
                'history': 'Inspired by the popular chocolate-mint flavor combination.',
                'price_range': '$8-22 per 100g',
                'popular_brands': 'David\'s Tea, Teavana, Harney & Sons',
                'description': 'Like drinking a mint chocolate treat, refreshing yet indulgent.',
                'serving_suggestions': 'Delicious hot or iced, pairs with chocolate desserts, refreshing after dinner'
            },
            
            # FRUIT & BERRY BLENDS
            {
                'blend_name': 'Wild Berry Blast',
                'category': 'Flavoured Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, strawberry, raspberry, blueberry, elderberry, hibiscus',
                'flavor_profile': 'Tart berries, sweet-tangy, fruity',
                'aroma': 'Mixed berries, fruity',
                'appearance': 'Deep purple-red',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '4-6 minutes',
                'caffeine_level': 'Medium (40-60mg per cup)',
                'health_benefits': 'High in antioxidants, vitamin C, immune support',
                'origin_region': 'Modern blend',
                'history': 'Created to capture summer berry flavors year-round.',
                'price_range': '$8-20 per 100g',
                'popular_brands': 'Celestial Seasonings, David\'s Tea, Teavana',
                'description': 'A vibrant berry medley perfect for fruit tea lovers.',
                'serving_suggestions': 'Excellent iced with honey, refreshing summer drink, pairs with berry desserts'
            },
            {
                'blend_name': 'Lemon Ginger',
                'category': 'Flavoured Green/Herbal Tea',
                'base_tea': 'Green tea or herbal base',
                'ingredients': 'Tea base, lemon peel, ginger root, lemongrass, natural lemon flavor',
                'flavor_profile': 'Zesty lemon, spicy ginger, refreshing',
                'aroma': 'Citrus, warming ginger',
                'appearance': 'Pale yellow-green',
                'brew_temp_c': 85,
                'brew_temp_f': 185,
                'steep_time': '4-6 minutes',
                'caffeine_level': 'Low-Medium (15-40mg per cup)',
                'health_benefits': 'Digestive aid, immune support, anti-inflammatory, helps with nausea',
                'origin_region': 'Modern wellness blend',
                'history': 'Popular in wellness culture for its soothing and healing properties.',
                'price_range': '$7-18 per 100g',
                'popular_brands': 'Yogi Tea, Traditional Medicinals, Bigelow',
                'description': 'A warming, soothing blend perfect for wellness and comfort.',
                'serving_suggestions': 'Excellent with honey, soothing when sick, refreshing iced, pairs with Asian cuisine'
            },
            {
                'blend_name': 'Passion Fruit',
                'category': 'Flavoured Black/White Tea',
                'base_tea': 'Black or white tea',
                'ingredients': 'Tea base, passion fruit pieces, hibiscus, orange peel, natural passion fruit flavor',
                'flavor_profile': 'Tropical, tangy, sweet-tart',
                'aroma': 'Exotic fruit, tropical',
                'appearance': 'Golden-orange with fruit pieces',
                'brew_temp_c': 90,
                'brew_temp_f': 194,
                'steep_time': '3-5 minutes',
                'caffeine_level': 'Low-Medium (20-45mg per cup)',
                'health_benefits': 'Vitamin C, antioxidants, refreshing',
                'origin_region': 'Modern tropical blend',
                'history': 'Created to bring tropical flavors to tea enthusiasts.',
                'price_range': '$9-25 per 100g',
                'popular_brands': 'Teavana, David\'s Tea, Republic of Tea',
                'description': 'An exotic, tropical blend that transports you to paradise.',
                'serving_suggestions': 'Perfect iced, pairs with tropical fruit, excellent summer refreshment'
            },
            
            # CHRISTMAS & SEASONAL BLENDS
            {
                'blend_name': 'Christmas Tea',
                'category': 'Spiced Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, cinnamon, orange peel, cloves, almonds, sometimes vanilla',
                'flavor_profile': 'Warm spices, orange, festive',
                'aroma': 'Cinnamon, clove, orange',
                'appearance': 'Dark brown with spices',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '4-5 minutes',
                'caffeine_level': 'Medium (40-60mg per cup)',
                'health_benefits': 'Warming spices, antioxidants, festive comfort',
                'origin_region': 'Scandinavia, adapted worldwide',
                'history': 'Traditional holiday blend, especially popular in Scandinavia. Each family may have their own recipe.',
                'price_range': '$8-25 per 100g',
                'popular_brands': 'Harney & Sons, Fortnum & Mason, Nordic brands',
                'description': 'A festive blend that captures the spirit of the holidays.',
                'serving_suggestions': 'Perfect with holiday cookies, gingerbread, pairs with Christmas desserts'
            },
            {
                'blend_name': 'Gingerbread Tea',
                'category': 'Spiced Black Tea',
                'base_tea': 'Black tea',
                'ingredients': 'Black tea, ginger, cinnamon, cloves, cardamom, vanilla, sometimes molasses flavor',
                'flavor_profile': 'Sweet-spicy, gingerbread cookie flavor, warm',
                'aroma': 'Gingerbread, warm spices',
                'appearance': 'Dark brown',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '4-6 minutes',
                'caffeine_level': 'Medium (40-60mg per cup)',
                'health_benefits': 'Warming, digestive support from ginger, antioxidants',
                'origin_region': 'Modern seasonal blend',
                'history': 'Created to capture the beloved gingerbread flavor in tea form.',
                'price_range': '$9-24 per 100g',
                'popular_brands': 'David\'s Tea, Harney & Sons, Celestial Seasonings',
                'description': 'Like drinking a gingerbread cookie, perfect for winter.',
                'serving_suggestions': 'Delicious with milk and sweetener, pairs with gingerbread or spice cookies'
            },
            
            # WELLNESS & DETOX BLENDS
            {
                'blend_name': 'Detox Tea',
                'category': 'Wellness Blend',
                'base_tea': 'Green tea or herbal base',
                'ingredients': 'Green tea, dandelion root, milk thistle, ginger, lemon peel, sometimes senna',
                'flavor_profile': 'Earthy, slightly bitter, herbal',
                'aroma': 'Herbal, earthy',
                'appearance': 'Yellow-green',
                'brew_temp_c': 85,
                'brew_temp_f': 185,
                'steep_time': '5-7 minutes',
                'caffeine_level': 'Low (10-30mg per cup)',
                'health_benefits': 'Supports liver function, aids digestion, may support natural detoxification',
                'origin_region': 'Modern wellness blend',
                'history': 'Part of the wellness tea movement of the 21st century.',
                'price_range': '$8-22 per 100g',
                'popular_brands': 'Yogi Tea, Traditional Medicinals, Pukka',
                'description': 'A wellness-focused blend designed to support the body\'s natural cleansing processes.',
                'serving_suggestions': 'Best consumed plain, drink plenty of water, consult healthcare provider for regular use'
            },
            {
                'blend_name': 'Sleep & Relaxation',
                'category': 'Wellness Herbal Blend',
                'base_tea': 'Herbal blend (caffeine-free)',
                'ingredients': 'Chamomile, lavender, valerian root, passionflower, lemon balm',
                'flavor_profile': 'Floral, calming, slightly sweet',
                'aroma': 'Lavender, chamomile, soothing',
                'appearance': 'Pale yellow with flowers',
                'brew_temp_c': 100,
                'brew_temp_f': 212,
                'steep_time': '7-10 minutes',
                'caffeine_level': 'None (caffeine-free)',
                'health_benefits': 'Promotes relaxation, may aid sleep, reduces anxiety, calming effect',
                'origin_region': 'Modern wellness blend',
                'history': 'Combines traditional sleep herbs from various cultures.',
                'price_range': '$7-20 per 100g',
                'popular_brands': 'Celestial Seasonings Sleepytime, Yogi Bedtime, Traditional Medicinals',
                'description': 'A soothing bedtime blend designed to promote restful sleep.',
                'serving_suggestions': 'Drink 30-60 minutes before bed, can add honey, avoid if pregnant/nursing without doctor approval'
            },
            
            # ASIAN-INSPIRED BLENDS
            {
                'blend_name': 'Genmaicha (Brown Rice Tea)',
                'category': 'Japanese Green Blend',
                'base_tea': 'Japanese green tea (bancha or sencha)',
                'ingredients': 'Green tea, roasted brown rice (sometimes popped rice)',
                'flavor_profile': 'Nutty, toasted rice, mild green tea',
                'aroma': 'Popcorn-like, toasted, nutty',
                'appearance': 'Yellow-green with rice grains',
                'brew_temp_c': 80,
                'brew_temp_f': 176,
                'steep_time': '2-3 minutes',
                'caffeine_level': 'Low (15-30mg per cup)',
                'health_benefits': 'Lower caffeine than regular green tea, antioxidants, soothing',
                'origin_region': 'Japan',
                'history': 'Originally created by Japanese merchants to stretch tea supplies. Now beloved for its unique flavor.',
                'price_range': '$8-25 per 100g',
                'popular_brands': 'Yamamotoyama, Ito En, Harada, O-Cha',
                'description': 'A traditional Japanese tea perfect for any time of day due to lower caffeine.',
                'serving_suggestions': 'Excellent with Japanese cuisine, pairs well with sushi or rice dishes, refreshing throughout the day'
            },
            {
                'blend_name': 'Thai Tea',
                'category': 'Spiced Black Tea',
                'base_tea': 'Strong black tea (often CTC)',
                'ingredients': 'Black tea, star anise, cardamom, sometimes tamarind, orange blossom water, vanilla',
                'flavor_profile': 'Sweet, creamy, spiced, distinctive orange color',
                'aroma': 'Sweet spices, vanilla',
                'appearance': 'Bright orange when prepared',
                'brew_temp_c': 100,
                'brew_temp_f': 212,
                'steep_time': '5-7 minutes',
                'caffeine_level': 'High (60-80mg per cup)',
                'health_benefits': 'Antioxidants from black tea',
                'origin_region': 'Thailand',
                'history': 'Popular Thai street beverage, traditionally served iced with condensed milk and sugar.',
                'price_range': '$7-18 per 100g',
                'popular_brands': 'Pantai, Number One Brand, Cha Tra Mue',
                'description': 'The iconic orange tea of Thailand, sweet and creamy.',
                'serving_suggestions': 'Serve iced with sweetened condensed milk and evaporated milk, pairs with Thai desserts or spicy food'
            },
            
            # RUSSIAN & EASTERN EUROPEAN
            {
                'blend_name': 'Russian Caravan',
                'category': 'Smoky Black Blend',
                'base_tea': 'Blend of Chinese black teas',
                'ingredients': 'Keemun, Lapsang Souchong, sometimes Oolong',
                'flavor_profile': 'Smoky, malty, robust',
                'aroma': 'Campfire smoke, pine, earthy',
                'appearance': 'Deep reddish-brown',
                'brew_temp_c': 95,
                'brew_temp_f': 203,
                'steep_time': '4-5 minutes',
                'caffeine_level': 'Medium-High (50-70mg per cup)',
                'health_benefits': 'Antioxidants from black tea',
                'origin_region': 'Historical blend (Russia-China trade route)',
                'history': 'Named after the 18th-century camel caravans that carried tea from China to Russia. The smoky flavor supposedly came from tea being transported near campfires.',
                'price_range': '$10-30 per 100g',
                'popular_brands': 'Harney & Sons, Fortnum & Mason, Mariage Frères',
                'description': 'A legendary blend with a distinctive smoky character.',
                'serving_suggestions': 'Traditional Russian style with lemon and sugar, pairs with hearty foods'
            }
        ]
        
        for blend in blends_data:
            cursor.execute('''
                INSERT INTO blends (
                    blend_name, category, base_tea, ingredients, flavor_profile,
                    aroma, appearance, brew_temp_c, brew_temp_f, steep_time,
                    caffeine_level, health_benefits, origin_region, history,
                    price_range, popular_brands, description, serving_suggestions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                blend['blend_name'], blend['category'], blend['base_tea'],
                blend['ingredients'], blend['flavor_profile'], blend['aroma'],
                blend['appearance'], blend['brew_temp_c'], blend['brew_temp_f'],
                blend['steep_time'], blend['caffeine_level'], blend['health_benefits'],
                blend['origin_region'], blend['history'], blend['price_range'],
                blend['popular_brands'], blend['description'], blend['serving_suggestions']
            ))
        
        self.conn.commit()
        print(f"Populated {len(blends_data)} tea blends")
        
    def initialize_database(self):
        """Initialize the complete database"""
        self.connect()
        self.create_tables()
        self.populate_blends()
        self.conn.close()
        print("Blends database initialization complete!")


if __name__ == "__main__":
    # Initialize database
    db = BlendsDatabase("tea_collection.db")
    db.initialize_database()
