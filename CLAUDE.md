# Tea & Tisane Collection Explorer

See @INTERFACE.md for the project navigation map.

## Quick Start
```bash
pip install -r requirements.txt
python main.py                 # databases ship with the repo; do not run setup_database.py
```

## Testing
```bash
python -m pytest -q tests/                  # all tests (test_web.py needs requirements-web.txt)
python -m pytest -q tests/test_web.py       # web interface only
```

## Web interface
`python run_web.py` (port 8114); `python scripts/build_static.py` builds the GitHub Pages site. Keep `web/search.py`
and `web/static/search_engine.js` in step (parity test in tests/test_web.py); after changing search rules or data,
run `python scripts/make_search_fixture.py`. Never write to the databases from the web app; the journal stays local.

See @SESSION_LOG.md for progress notes.
