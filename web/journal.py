"""Tea journal for the local web app, through the repo's own JournalController / JournalRepository: the same
tea_journal.json and entry format ({entry_id, tea_name, date, rating, brewing, notes}) as the desktop Journal tab.

The journal holds personal tasting notes, so it is served only by the local server and never exported to the static
site. Set TEA_JOURNAL to use another file (the tests do).
"""
import os
from pathlib import Path

from controllers import JournalController
from database import JournalRepository

from .data import CONFIG


def path() -> Path:
    return Path(os.environ.get("TEA_JOURNAL") or CONFIG.journal_path)


def _controller() -> JournalController:
    # A fresh repository per request: the repository caches the file after its first read.
    return JournalController(JournalRepository(path()))


def load() -> list[dict]:
    """Entries, newest first."""
    entries = [e.to_dict() for e in _controller().get_all_entries()]
    return sorted(entries, key=lambda e: e.get("date") or "", reverse=True)


def add(tea_name: str, rating: int, brewing: str = "", notes: str = "") -> dict:
    tea_name = (tea_name or "").strip()
    if not tea_name:
        raise ValueError("Please choose a tea")
    if not 1 <= int(rating) <= 5:  # the model clamps silently; the web form reports it instead
        raise ValueError("Rating must be 1-5")
    return _controller().add_entry(tea_name, int(rating), (brewing or "").strip(), (notes or "").strip()).to_dict()


def delete(entry_id: int) -> None:
    ctl = _controller()
    if not any(e.entry_id == entry_id for e in ctl.get_all_entries()):
        raise KeyError(entry_id)
    ctl.delete_entry(entry_id)
