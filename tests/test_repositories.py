"""Repository/controller tests against the real tea_collection.db (opened read-only).

Regression tests for the Tea Browser search: TeaRepository.search() and find_by_id() referred to columns that do not
exist (origin_region, tea_id), and TeaController.search_teas() ignored the query when a category was also given.
"""
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from controllers import BlendController, TeaController  # noqa: E402
from database import BlendRepository, TeaRepository  # noqa: E402


@pytest.fixture(scope="module")
def conn():
    c = sqlite3.connect(f"file:{(ROOT / 'tea_collection.db').as_posix()}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    yield c
    c.close()


def test_tea_search_by_name_and_flavour(conn):
    teas = TeaRepository(conn).search("jasmine")
    assert teas and all("jasmine" in (t.name + t.flavor_profile + t.origin).lower() for t in teas)


def test_tea_search_matches_origin(conn):
    names = {t.name for t in TeaRepository(conn).search("Darjeeling")}
    assert any("Darjeeling" in n for n in names)
    assert any(t.origin.startswith("Kenya") for t in TeaRepository(conn).search("Kenya"))


def test_tea_find_by_id(conn):
    tea = TeaRepository(conn).find_by_id(1)
    assert tea is not None and tea.tea_id == 1 and tea.name


def test_tea_find_by_origin_country(conn):
    teas = TeaRepository(conn).find_by_origin("Japan")
    assert teas and all(t.origin.startswith("Japan") for t in teas)
    assert any(t.origin.startswith("Japan - ") for t in teas)  # "Japan - Shizuoka, Kagoshima" counts as Japan


def test_controller_combines_query_category_and_country(conn):
    ctl = TeaController(TeaRepository(conn))
    green = ctl.search_teas("sencha", category="Green")
    assert green and all(t.category == "Green" and "sencha" in (t.name + t.flavor_profile + t.origin).lower()
                     for t in green)
    assert ctl.search_teas("sencha", category="Black") == []
    jp = ctl.search_teas("", category="Green", country="Japan")
    assert jp and all(t.category == "Green" and t.origin.startswith("Japan") for t in jp)
    assert len(ctl.search_teas()) == 160


def test_blend_search_with_category(conn):
    ctl = BlendController(BlendRepository(conn))
    hits = ctl.search_blends("earl", category="Flavored Black Blend")
    assert hits and all(b.category == "Flavored Black Blend" and "earl" in (b.blend_name + b.ingredients + b.flavor_profile).lower()
                    for b in hits)
    assert ctl.search_blends("earl", category="Wellness Blend") == []
