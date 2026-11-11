"""The desktop app must find its databases and documents wherever it is launched from.

Regression test: main.py opened "tea_collection.db", "tisane_collection.db", the markdown guides and the map image
relative to the current directory, so launching it from anywhere else created empty database files there and crashed
("no such table: teas"). Needs Tk and a display; skipped otherwise.
"""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def test_app_starts_from_another_directory(tmp_path):
    tk = pytest.importorskip("tkinter")
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display")
    root.withdraw()
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        import main
        app = main.TeaExplorerEnhanced(root)
        assert "Teas: 160" in app.status_bar.cget("text")
        assert app.tisane_controller.get_tisane_count() == 154
        assert len(app.journal_controller.get_all_entries()) >= 1
        assert list(tmp_path.iterdir()) == []  # nothing created in the launch directory
    finally:
        os.chdir(cwd)
        root.destroy()
