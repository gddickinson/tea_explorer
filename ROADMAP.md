# Tea & Tisane Collection Explorer -- Roadmap

## Current State
The most feature-complete application in the collection. Clean MVC architecture
with 7 model classes, 7 repository classes, 6 controllers, a theme system, chart
generation, recommendation engine, performance caching/profiling, export service,
and validation. Built with tkinter, backed by two SQLite databases (443+ items).
Has tests (`tests/test_models.py`), benchmarks, and screenshots. However,
`main.py` is a monolith that reimplements much of what the MVC layers provide.
A `tea_explorer_v1/` legacy directory and `*_OLD.db` files add clutter. Two
controllers exist for tea (`tea_controller.py` and `tea_controller_optimized.py`).

## Short-term Improvements
- [x] Remove or archive `tea_explorer_v1/` -- it duplicates the current codebase
- [x] Remove `tea_collection_OLD.db` and `tisane_collection_OLD.db`
- [x] Merge `tea_controller.py` and `tea_controller_optimized.py` -- keep the
      optimized version and delete the old one
- [ ] Reduce `main.py`: it should delegate to `views/main_window.py` and
      controllers, not reimplement UI logic
- [x] Expand test suite beyond `test_models.py`: add tests for repositories,
      controllers, and the recommendation engine
- [ ] Add type hints to all controller and repository methods
- [x] Add `.gitignore` to exclude `*.db`, `__pycache__`, `logs/`, and generated
      screenshots

## Feature Enhancements
- [ ] Add a brewing timer notification system (desktop notifications via
      `plyer` or system tray integration)
- [ ] Implement tea pairing suggestions: recommend food pairings based on tea
      flavor profiles using the recommendation engine
- [ ] Add import from external sources: load tea data from CSV, Steepster API,
      or other tea databases
- [ ] Implement a "tea of the day" random suggestion on the dashboard
- [ ] Add advanced search: boolean queries, flavor profile matching, multi-field
      filtering
- [ ] Implement data backup/restore to JSON for portability across machines
- [ ] Add caffeine tracker: log daily tea consumption and chart caffeine intake

## Long-term Vision
- [ ] Web version using Flask or Django with the same SQLite backend
- [ ] Mobile companion app (Kivy or React Native) syncing with the desktop DB
- [ ] Community features: share tasting notes, compare collections with friends
- [ ] Integration with tea vendor APIs for price tracking and reorder reminders
- [ ] AI-powered flavor profile analysis: cluster teas by chemical similarity
      using NLP on tasting notes
- [ ] Barcode/QR scanning for quick tea identification and logging

## Technical Debt
- [ ] `main.py` is almost certainly over 500 lines and duplicates logic from
      `views/main_window.py` -- consolidate into a thin entry point
- [x] `main_simple.py` exists alongside `main.py` -- clarify purpose or remove
- [x] `generate_screenshots.py` is a dev utility -- move to a `tools/` directory
- [ ] `setup_indexes.py` should run automatically on first launch, not require
      a separate manual step
- [ ] The `benchmarks/` directory structure is unclear -- integrate into the
      test suite with `pytest-benchmark`
- [ ] `claude/` directory in the project root suggests AI-generated content --
      clean up or document its purpose
- [ ] `theme_config.json` and `tea_journal.json` should have documented schemas
- [x] Fixed `processing_method` attribute reference in recommendation engine
      (should be `processing` to match Tea model)
- [x] Fixed test_models.py to use correct field names (`origin` instead of
      `origin_country`/`origin_region`)
