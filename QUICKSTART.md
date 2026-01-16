# Quick Start Guide - Tea Collection Explorer Phase 2

## 🚀 Getting Started in 3 Steps

### Step 1: Extract the Archive

```bash
tar -xzf tea_explorer_phase2.tar.gz
cd tea_explorer_phase2_complete
```

### Step 2: Set Up the Database

```bash
python setup_database.py
```

**Output:**
```
============================================================
Tea Collection Explorer - Database Setup
============================================================

Creating database at: tea_collection.db
Creating 'teas' table...
Creating 'blends' table...
Inserting sample tea data...
Inserting sample blend data...

✓ Database created successfully!
✓ Inserted 10 sample teas
✓ Inserted 4 sample blends

Creating journal file at: tea_journal.json
✓ Created journal with 3 sample entries

============================================================
Setup Complete! 🎉
============================================================

You can now run: python main.py
```

### Step 3: Run the Application

```bash
python main.py
```

The application will launch with:
- 10 sample teas in the database
- 4 sample blends
- 3 sample journal entries
- Working search, browse, and statistics

---

## 📊 What You'll See

### Tea Browser Tab
- **Search teas** by name or description
- **Filter by category** (Green, Black, Oolong, etc.)
- **View details** including brewing parameters, flavor profiles
- **Browse 10 sample teas** from around the world

### Blends Tab
- Browse tea blends
- (Ready for implementation)

### Journal Tab
- View recent journal entries
- See ratings and tasting notes
- (Ready for expansion)

### Statistics Tab
- Total tea count
- Teas by category
- Top rated teas from journal
- Collection statistics

### Info Tab
- Architecture documentation
- Project structure
- Next steps

---

## 📦 Sample Data Included

### Teas (10 varieties)

**Green Teas:**
- Sencha (Japan) - Fresh, grassy
- Dragonwell/Longjing (China) - Sweet, nutty
- Gyokuro (Japan) - Umami-rich, premium

**White Tea:**
- Silver Needle (China) - Delicate, sweet

**Oolong Teas:**
- Tie Guan Yin (China) - Floral, orchid-like
- Da Hong Pao (China) - Rich, roasted

**Black Teas:**
- Keemun (China) - Winey, fruity
- Darjeeling First Flush (India) - Muscatel, floral
- Ceylon (Sri Lanka) - Brisk, citrusy

**Pu-erh:**
- Shou Pu-erh (China) - Earthy, smooth

### Blends (4 varieties)
- Earl Grey - Classic bergamot blend
- English Breakfast - Robust morning blend
- Jasmine Pearl - Floral green tea
- Moroccan Mint - Refreshing mint blend

### Journal Entries (3 samples)
- Sencha tasting (5 stars)
- Dragonwell tasting (5 stars)
- Earl Grey tasting (4 stars)

---

## 🔧 Configuration

### Database Location

By default, creates `tea_collection.db` in current directory.

To use a different location:
```bash
python setup_database.py /path/to/your/database.db
```

Then update `config.py`:
```python
tea_db_path: str = '/path/to/your/database.db'
```

### Journal Location

Default: `tea_journal.json` in current directory

Update in `config.py`:
```python
journal_path: str = '/path/to/your/journal.json'
```

---

## 🧪 Testing

Run tests to verify installation:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=. --cov-report=html
```

**Expected:** 10 tests pass

---

## ❓ Troubleshooting

### Issue: "No such table: teas"

**Solution:** Run the database setup script:
```bash
python setup_database.py
```

### Issue: Import errors

**Solution:** Make sure you're in the project directory:
```bash
cd tea_explorer_phase2_complete
python main.py
```

### Issue: "No module named 'pytest'"

**Solution:** Install test dependencies:
```bash
pip install -r requirements.txt
```

---

## 📚 Next Steps

### Explore the Code

1. **Models** (`models/`) - See domain objects
2. **Repositories** (`database/`) - See data access
3. **Controllers** (`controllers/`) - See business logic
4. **Views** (`views/`) - See UI components

### Add Your Own Data

#### Add a Tea
```python
from models import Tea
from database import DatabaseConnection, TeaRepository

db = DatabaseConnection('tea_collection.db')
repo = TeaRepository(db.get_connection())

new_tea = Tea(
    name="Your Tea Name",
    category="Green",
    origin_country="Japan",
    flavor_profile="Describe the flavor..."
)

# Add SQL insert logic here
```

#### Add Journal Entry

Edit `tea_journal.json` or use the application (when fully implemented).

### Extend the Application

See `README.md` for:
- Adding new features
- Creating new tabs
- Adding new widgets
- Writing tests

---

## 🎯 Key Commands

```bash
# Setup database
python setup_database.py

# Run application
python main.py

# Run tests
pytest tests/ -v

# Check code
python -m py_compile main.py

# View coverage
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

## ✅ Checklist

- [ ] Extract archive
- [ ] Run `python setup_database.py`
- [ ] Verify `tea_collection.db` created
- [ ] Verify `tea_journal.json` created
- [ ] Run `python main.py`
- [ ] Application launches successfully
- [ ] Browse sample teas
- [ ] View statistics
- [ ] Check journal entries

---

**Ready to explore! 🫖**

If you have any issues, check:
1. This QUICKSTART.md
2. README.md for detailed info
3. SYNTAX_ERROR_FIX.md if syntax errors
4. Code comments and docstrings

Happy tea exploring! 🍵
