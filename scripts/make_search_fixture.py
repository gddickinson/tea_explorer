"""Write tests/fixtures/search_cases.json: sample rows from the real databases plus the ids web/search.py returns for
a set of queries. web/static/search_engine.test.mjs checks the JS filters give the same ids; tests/test_web.py checks
this file is still current.

Run: python scripts/make_search_fixture.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web import data  # noqa: E402
from web.search import SPECS, filter_rows  # noqa: E402

OUT = ROOT / "tests" / "fixtures" / "search_cases.json"
SAMPLE = 30  # rows per kind (every 5th row, so the sample spans the alphabet)
CASES = [
    ("teas", {}), ("teas", {"q": "smoky"}), ("teas", {"category": "Oolong"}), ("teas", {"country": "Japan", "q": "steamed"}),
    ("teas", {"caffeine": "Medium"}), ("teas", {"q": "FLORAL honey"}), ("teas", {"category": "Black", "caffeine": "High"}),
    ("blends", {"q": "bergamot"}), ("blends", {"caffeine": "Low"}),
    ("cultivars", {"species": "assamica"}), ("cultivars", {"species": "var. sinensis", "country": "Japan"}),
    ("regions", {"country": "China"}), ("regions", {"q": "mist"}),
    ("companies", {"country": "United Kingdom"}), ("companies", {"cert": "Rainforest Alliance"}),
    ("companies", {"segment": "premium", "q": "london"}),
    ("products", {"organic": "1"}), ("products", {"type": "black", "currency": "GBP"}), ("products", {"company": "1"}),
    ("tisanes", {"caffeine_free": "1"}), ("tisanes", {"tradition": "Ayurveda"}), ("tisanes", {"family": "Lamiaceae"}),
    ("tisanes", {"q": "sleep", "caffeine_free": "1"}), ("families", {"q": "aromatic"}),
    ("herb_regions", {"q": "rooibos"}), ("makers", {"country": "USA"}), ("makers", {"cert": "Organic"}),
    ("herb_products", {"q": "sleep"}), ("herb_products", {"maker": "1"}), ("teas", {"q": "zzzz"}),
]


def build() -> dict:
    rows = {kind: data.rows(kind)[::5][:SAMPLE] for kind in SPECS}
    cases = [{"kind": k, "params": p, "ids": [r[SPECS[k]["id"]] for r in filter_rows(k, rows[k], p)]} for k, p in CASES]
    return {"rows": rows, "cases": cases}


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build(), ensure_ascii=False, indent=0, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
