# Session Log

## 2026-11-11 -- Bug fixes, web interface and static GitHub Pages site (branch `web-interface`)
Bugs found and fixed (each in its own commit with a regression test):
- Tea Browser search crashed: `TeaRepository.search()` used a missing `origin_region` column, `find_by_id()` a missing
  `tea_id` column, `find_by_origin()` matched only an exact country; the tea and blend controllers ignored the query
  when a category was set. Now query + category combine (`tests/test_repositories.py`).
- Desktop app crashed when launched from another directory (relative DB/markdown/map paths created empty databases in
  the current directory); now uses `config.py` paths, theme prefs anchored to the repo (`tests/test_app_paths.py`).
- `THEME=tea` (documented) was rejected by `UIConfig.validate()` (`tests/test_config.py`).
- Deleting one journal entry without an `entry_id` deleted all such entries; ids are now assigned on load
  (`tests/test_journal_repository.py`).
- `logs/tea_explorer.log` was tracked despite `.gitignore`; untracked.
- Docs: README told users to run `setup_database.py` (legacy schema; fails on the shipped DB, overwrites the journal on
  a fresh checkout); counts corrected; QUICKSTART.md marked outdated.

Web interface (`web/`, `run_web.py`, port 8114) and static site (`scripts/build_static.py`, `.github/workflows/pages.yml`):
- Pages: home, teas/tea (timer, regions, cultivars, similar teas from `RecommendationEngine`), compare, blends/blend,
  cultivars/cultivar, companies/company (products, distribution, blends), products/product, tisanes/tisane (all safety
  records), plant families, traditions, herbal brands, map (Natural Earth outlines, tea + herb layers)/region/herb
  region, brewing timer (presets factored into `brewing_presets.py`, used by main.py too), dashboard, guide, history,
  glossary, herbal reference (tables), search, journal (local only), about.
- Databases opened read-only (`mode=ro`); journal through `JournalController`, never exported (test checks the build).
- Search rules in `web/search.py` mirrored by `search_engine.js`; fixture `tests/fixtures/search_cases.json` plus a
  full-data parity test.
- `THIRD_PARTY/ne_110m_land.json` reused from coffee_explorer (identical file, public domain, note in THIRD_PARTY/README.md).
- Local environment: tests run with `DYLD_LIBRARY_PATH=/opt/anaconda3/pkgs/libsqlite-3.53.3-h1b79a29_0/lib`.

Open questions for George: what to do with `setup_database.py` (archive?); the desktop Tisanes tab shows only the first
of several safety records per herb (the web shows all); duplicate rows in the data (regions Boseong and Nilgiri twice,
Rize / Rize Province; companies Harney and Sons / Harney & Sons, Teapigs twice); `main.py` is 1700+ lines.
