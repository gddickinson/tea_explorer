"""Regression: the desktop Tisanes tab showed no safety record at all (only a generic warning), and the repository's
get_safety_info() returned just the first record, although some herbs have several (Valerian Root has 3, the third
saying "Avoid" in pregnancy). All records must reach the detail text."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from controllers import TisaneController  # noqa: E402
from database import TisaneRepository  # noqa: E402
from utils.formatters import format_safety_records  # noqa: E402


@pytest.fixture(scope="module")
def ctl():
    repo = TisaneRepository(str(ROOT / "tisane_collection.db"))
    yield TisaneController(repo)
    repo.close()


def _valerian(ctl):
    return ctl.get_tisane_by_name("Valerian Root")


def test_all_safety_records_returned(ctl):
    records = ctl.get_safety_records(_valerian(ctl).tisane_id)
    assert len(records) == 3 and [r["id"] for r in records] == sorted(r["id"] for r in records)
    assert ctl.get_safety_info(_valerian(ctl).tisane_id) == records[0]  # unchanged: first record


def test_format_lists_every_record(ctl):
    text = format_safety_records(ctl.get_safety_records(_valerian(ctl).tisane_id))
    assert text.count("Risk level:") == 3 and "Avoid - insufficient safety data" in text
    assert "no safety record" in format_safety_records([]).lower()


def test_desktop_tab_shows_all_records():
    tk = pytest.importorskip("tkinter")
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display")
    root.withdraw()
    try:
        import main
        app = main.TeaExplorerEnhanced(root)
        names = app.tisane_listbox.get(0, tk.END)
        app.tisane_listbox.selection_set(names.index("Valerian Root"))
        app.on_tisane_select(None)
        text = app.tisane_detail_text.get("1.0", tk.END)
        assert text.count("Risk level:") == 3 and "Avoid - insufficient safety data" in text
    finally:
        root.destroy()
