"""Journal repository tests. Regression: entries written without an entry_id (as in the shipped tea_journal.json) all
had entry_id None, so deleting one of them from the Journal tab deleted every such entry."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import JournalRepository  # noqa: E402


def _journal(tmp_path, entries):
    p = tmp_path / "journal.json"
    p.write_text(json.dumps(entries))
    return p


def test_delete_one_entry_without_ids_keeps_the_others(tmp_path):
    p = _journal(tmp_path, [{"tea_name": "Sencha", "date": "2026-01-01 08:00", "rating": 4},
                            {"tea_name": "Assam", "date": "2026-01-02 08:00", "rating": 5}])
    repo = JournalRepository(p)
    first = repo.find_all()[0]
    repo.delete(first.entry_id)
    assert [e.tea_name for e in JournalRepository(p).find_all()] == ["Assam"]


def test_missing_ids_are_unique_and_new_entries_follow(tmp_path):
    p = _journal(tmp_path, [{"tea_name": "A", "rating": 3}, {"entry_id": 7, "tea_name": "B", "rating": 3},
                            {"tea_name": "C", "rating": 3}])
    repo = JournalRepository(p)
    ids = [e.entry_id for e in repo.find_all()]
    assert None not in ids and len(set(ids)) == 3 and 7 in ids
    from models import JournalEntry
    assert repo.add(JournalEntry(tea_name="D", rating=5)).entry_id == max(ids) + 1
