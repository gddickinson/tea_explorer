"""Web interface for the Tea & Tisane Collection Explorer (FastAPI + plain ES-module front end).

Contents:
- app.py      FastAPI app: JSON API under /api, front end at /, STATIC_ENDPOINTS for the static site
- data.py     read-only access to tea_collection.db and tisane_collection.db (paths from config.py), derived fields
- links.py    cross-links between tables (name mentions) and similar teas (recommendations.RecommendationEngine)
- search.py   search/filter rules for list endpoints (mirrored by static/search_engine.js)
- summary.py  dashboard counts and brewing-timer presets (brewing_presets.py)
- journal.py  tea journal via controllers.JournalController (local server only, never exported)
- static/     index.html, theme, page modules, static_api.js for GitHub Pages
"""
