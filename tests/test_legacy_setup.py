"""Regression: README/QUICKSTART told users to run setup_database.py, a legacy script with an older schema that
fails on the shipped database and, on a fresh checkout, replaced tea_journal.json with sample entries. It now lives
in _archive/, nothing imports it, and it refuses to overwrite an existing database or journal."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY = ROOT / "_archive" / "setup_database.py"


def test_archived_and_not_imported():
    assert not (ROOT / "setup_database.py").exists() and LEGACY.exists()
    for py in ROOT.rglob("*.py"):
        if "_archive" in py.parts or ".venv" in py.parts:
            continue
        assert not re.search(r"^\s*(from|import)\s+setup_database\b", py.read_text(encoding="utf-8"), re.M), py


def test_refuses_to_overwrite_existing_files(tmp_path):
    (tmp_path / "tea_journal.json").write_text('[{"tea_name": "mine"}]')
    r = subprocess.run([sys.executable, str(LEGACY)], cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode != 0 and "legacy" in (r.stdout + r.stderr).lower()
    assert (tmp_path / "tea_journal.json").read_text() == '[{"tea_name": "mine"}]'
    assert not (tmp_path / "tea_collection.db").exists()
