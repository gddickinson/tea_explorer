# Tea & Tisane Collection Explorer -- Interface Map

## Desktop app (Tkinter, MVC + repositories)

| File / Directory | Purpose |
|------------------|---------|
| `main.py` | `TeaExplorerEnhanced` (all tabs, timer, comparison, charts, export), `main()` entry point. 1700+ lines: over the 500-line budget, split pending |
| `config.py` | `Config` / `get_config()`: database, journal and markdown paths (env overrides `TEA_DB_PATH`, `TISANE_DB_PATH`, `THEME`, ...) |
| `logger_setup.py` | `LoggerSetup`, `get_logger()`, `LoggerMixin`, `log_method_call` (log file `logs/tea_explorer.log`, untracked) |
| `validation.py` | Input validation helpers |
| `brewing_presets.py` | `TIMER_PRESETS`, `preset_label()` -- timer presets shared by the desktop Timer tab and the web timer |
| `models/` | Dataclasses: `Tea`, `Blend`, `JournalEntry`, `Cultivar`, `Company`, `Product`, `Tisane` (`is_caffeine_free()`), `Region` |
| `database/` | `DatabaseConnection`; repositories `TeaRepository`, `BlendRepository`, `CultivarRepository`, `CompanyRepository`, `ProductRepository`, `RegionRepository`, `TisaneRepository` (own connection to tisane_collection.db), `JournalRepository` (JSON file) |
| `controllers/` | `TeaController` (`search_teas(query, category, country, caffeine_level)`), `BlendController`, `CultivarController`, `CompanyController`, `TisaneController`, `JournalController` |
| `recommendations/engine.py` | `RecommendationEngine.get_similar_teas()` and other suggestion strategies |
| `visualizations/chart_generator.py` | `ChartGenerator`, `DashboardGenerator` (Matplotlib) |
| `themes/theme_manager.py` | `ThemeManager` (light / dark / tea), module instance `theme_manager` (prefs in `theme_config.json`) |
| `services/export_service.py` | CSV / JSON export |
| `performance/` | `cache.py` (caching decorators), `profiler.py` (`profile_method`) |
| `utils/formatters.py` | Formatting helpers |
| `views/` | Earlier tab/widget classes (main.py builds the UI itself) |
| `setup_indexes.py`, `benchmarks/`, `tools/generate_screenshots.py` | Index creation, performance benchmarks, desktop screenshots (macOS Quartz) |
| `_archive/` | Old versions, not used (incl. `setup_database.py`: legacy Phase 2 schema, refuses to overwrite existing files) |

## Web interface (FastAPI + plain ES modules, no build step)

| File | Purpose |
|------|---------|
| `run_web.py` | Starts the web app (uvicorn, http://127.0.0.1:8114) |
| `requirements-web.txt` | Pinned web/test dependencies |
| `web/app.py` | FastAPI app: `/api/*` routes (lists, details, stats, facets, dashboard, timer, traditions, world, content, search), journal POST (local only), `STATIC_ENDPOINTS` |
| `web/data.py` | Read-only access to both databases (`connect()` uses SQLite `mode=ro`, paths from `config.py`), `KINDS`, derived filter fields, `stats()` |
| `web/links.py` | Cross-links by name mention (`mentions()`): tea<->region/cultivar, blend<->company, tisane<->family/herb region/products; `similar_teas()` via `RecommendationEngine` |
| `web/search.py` | `SPECS`, `filter_rows()`, `facets()` -- search/filter rules for every list endpoint |
| `web/summary.py` | `dashboard()` counts, `timer()` presets and steep times |
| `web/journal.py` | Journal load/add/delete through `JournalController` (`TEA_JOURNAL` env overrides the file) |
| `web/static/index.html`, `style.css`, `core.js` | Shell page, shared kit theme and router (kit files, unchanged) |
| `web/static/style_app.css` | Jade/amber/lavender accents and page styles |
| `web/static/main.js` | Registers lazy page modules, mode line, background, starts router |
| `web/static/ui.js` | `listPage()` (filterable lists synced to the URL), `kv()`, `sections()`, `crumb()`, `options()` |
| `web/static/static_api.js` | Static site: answers `api()` from exported JSON; filters lists/search in the browser; journal -> needs server |
| `web/static/search_engine.js` | JS mirror of `web/search.py` (+ `search_engine.test.mjs`, also tests `parseSteepTime`) |
| `web/static/markdown.js` | Small safe markdown renderer incl. pipe tables and glossary terms (+ `markdown.test.mjs`) |
| `web/static/timer.js` | Countdown timer `mountTimer()`, `parseSteepTime()` |
| `web/static/geo.js` | `project()` -- JS copy of `world_shapes.project()` (+ `geo.test.mjs`) |
| `web/static/home.js` | Pages: home, search (all tables), about |
| `web/static/teas.js` | teas / tea / compare |
| `web/static/blends.js` | blends / blend / cultivars / cultivar |
| `web/static/brands.js` | companies / company / products / product |
| `web/static/tisanes.js` | tisanes / tisane (safety records) / families / family / traditions |
| `web/static/makers.js` | makers / maker (herbal brands and their products) |
| `web/static/regions.js` | map (tea + herb layers) / region / herbregion, `worldSvg()` |
| `web/static/brewing.js`, `dashboard.js`, `guide.js`, `journal.js` | timer; dashboard (`bars()`); guide / history / glossary / herbal; journal (local only) |
| `web/static/background.js`, `icon.svg` | Animated background (off under reduced motion), favicon |
| `world_shapes.py` | `LAND_POLYGONS` (Natural Earth 1:110m from `THIRD_PARTY/ne_110m_land.json`), `project()`, `on_land()` |
| `THIRD_PARTY/` | `ne_110m_land.json` + `README.md` (source, checksum, public-domain licence) |
| `scripts/build_static.py` | Exports the static site to `site/` (all `STATIC_ENDPOINTS` as JSON) |
| `scripts/screenshots.py` | Playwright smoke test + README screenshots (`docs/img/`) |
| `scripts/make_search_fixture.py` | Writes `tests/fixtures/search_cases.json` (Python search results for the JS test) |
| `scripts/convert_natural_earth.py` | Regenerates `THIRD_PARTY/ne_110m_land.json` from the Natural Earth GeoJSON |
| `.github/workflows/pages.yml` | Test, build and publish the static site on push to main |

## Tests

`tests/test_models.py`, `tests/test_recommendations.py` (original); `tests/test_repositories.py` (tea search on the real
DB), `tests/test_app_paths.py` (desktop app from another directory; needs Tk), `tests/test_config.py`,
`tests/test_journal_repository.py`, `tests/test_web.py` (endpoints, filters, read-only DBs, journal, static build, node
tests, JS/Python search parity, fixture currency, map).

## Module connections

```
main.py -> config, database/*, controllers/*, models, themes, visualizations, recommendations, brewing_presets
run_web.py -> web/app.py -> web/data.py (-> config, models.Tisane), web/links.py (-> recommendations, models.Tea),
                            web/search.py, web/summary.py (-> brewing_presets), web/journal.py (-> controllers, database)
                         -> world_shapes.py
           -> web/static/main.js -> page modules -> core.js api() -> /api/* (local) or static_api.js (GitHub Pages)
scripts/build_static.py -> web/app.py via TestClient -> site/api/*.json
```

## Data files

- `tea_collection.db`, `tisane_collection.db` -- SQLite databases (tracked; the web app opens them read-only)
- `tea_journal.json` -- personal tasting notes (local only, never exported to the static site)
- `tea_varieties_list.md`, `tea_history.md`, `tea_glossary.md`, `tisanes.md` -- reading material (desktop and web)
- `world_map_bg.png` -- desktop map background; `docs/img/` -- README screenshots of the web interface
