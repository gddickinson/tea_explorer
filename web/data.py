"""Read-only access to the two databases (tea_collection.db, tisane_collection.db) for the web app.

Paths come from the repo's own config.py (so TEA_DB_PATH / TISANE_DB_PATH work as for the desktop app). Every
connection is opened with SQLite `mode=ro`: the web app never writes to a database. Rows are returned as plain dicts
with a few derived fields for filtering (documented in `ROW_EXTRAS`); the stored values are never changed.
"""
import json
import re
import sqlite3
from functools import lru_cache
from pathlib import Path

from config import get_config
from models import Tisane

ROOT = Path(__file__).resolve().parent.parent
CONFIG = get_config(ROOT)
DOCS = {"guide": CONFIG.guide_path, "history": CONFIG.history_path, "glossary": ROOT / "tea_glossary.md",
        "herbal": CONFIG.tisanes_path}

# kind -> (database, table, primary key, display-name column). Kinds are the API names.
KINDS = {
    "teas": ("tea", "teas", "id", "name"),
    "blends": ("tea", "blends", "blend_id", "blend_name"),
    "cultivars": ("tea", "cultivars", "id", "name"),
    "regions": ("tea", "regions", "id", "name"),
    "companies": ("tea", "companies", "company_id", "company_name"),
    "products": ("tea", "products", "product_id", "product_name"),
    "tisanes": ("tisane", "tisanes", "id", "name"),
    "families": ("tisane", "plant_families", "id", "family_name"),
    "herb_regions": ("tisane", "regions", "id", "name"),
    "makers": ("tisane", "manufacturers", "id", "company_name"),
    "herb_products": ("tisane", "products", "id", "product_name"),
}
# Tables read whole but not listed as their own pages.
EXTRA_TABLES = {"distribution": ("tea", "distribution", "distribution_id"),
                "safety": ("tisane", "safety_info", "id"),
                "traditions": ("tisane", "traditional_systems", "id")}

# One spelling per country for filters (the database uses both).
COUNTRY_ALIASES = {"UK": "United Kingdom"}
ROW_EXTRAS = """teas: country (origin before " - "), caffeine (caffeine_level before "(");
blends: caffeine; companies: country (aliases merged), cert_terms; products: company_name, booleans;
tisanes: caffeine_free (models.Tisane.is_caffeine_free), tradition_terms, common_names/tcm/ayurvedic parsed from JSON;
makers: country (last part of headquarters_country), cert_terms; herb_products: maker_name"""


def db_path(which: str) -> Path:
    return CONFIG.database.tea_db_path if which == "tea" else CONFIG.database.tisane_db_path


def connect(which: str) -> sqlite3.Connection:
    """Read-only connection (the web app never modifies a database)."""
    uri = "file:" + Path(db_path(which)).resolve().as_posix() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@lru_cache(maxsize=None)
def _table(which: str, table: str, order: str) -> tuple:
    conn = connect(which)
    try:
        return tuple(dict(r) for r in conn.execute(f"SELECT * FROM {table} ORDER BY {order} COLLATE NOCASE"))
    finally:
        conn.close()


def _band(text) -> str:
    """'Low-Medium (25-35mg per cup)' -> 'Low-Medium'."""
    return (text or "").split("(")[0].strip()


def _country(value) -> str:
    v = (value or "").strip()
    return COUNTRY_ALIASES.get(v, v)


def _terms(value, aliases=None) -> list[str]:
    """'Organic, FairWild / Non-GMO (some)' -> ['Organic', 'FairWild', 'Non-GMO'] (de-duplicated, order kept)."""
    out = []
    for part in re.sub(r"\([^)]*\)", "", value or "").replace("/", ",").split(","):
        t = part.strip()
        t = (aliases or {}).get(t, t)
        if t and t not in out:
            out.append(t)
    return out


def _json(value) -> dict:
    try:
        v = json.loads(value) if value else {}
    except (TypeError, ValueError):
        return {}
    return v if isinstance(v, dict) else {}


TRADITION_ALIASES = {"TCM": "Traditional Chinese Medicine"}


def _extras(kind: str, r: dict) -> dict:
    if kind == "teas":
        r["country"] = (r.get("origin") or "").split(" - ")[0].strip()
        r["caffeine"] = _band(r.get("caffeine_level"))
    elif kind == "blends":
        r["caffeine"] = _band(r.get("caffeine_level"))
    elif kind == "companies":
        r["country"] = _country(r.get("country_of_origin"))
        r["cert_terms"] = _terms(r.get("certifications"))
    elif kind == "products":
        for k in ("organic", "fair_trade"):
            r[k] = bool(r[k])
    elif kind == "tisanes":
        r["caffeine_free"] = Tisane.from_db_row(r).is_caffeine_free()
        r["tradition_terms"] = _terms(r.get("tradition"), TRADITION_ALIASES)
        r["common_names"] = _json(r.pop("common_names_json", None))
        r["tcm"] = _json(r.pop("tcm_properties_json", None))
        r["ayurvedic"] = _json(r.pop("ayurvedic_properties_json", None))
    elif kind == "makers":
        r["country"] = _country((r.get("headquarters_country") or "").split(",")[-1])
        r["cert_terms"] = _terms(r.get("certifications"))
    return r


@lru_cache(maxsize=None)
def _rows(kind: str) -> tuple:
    which, table, _pk, label = KINDS[kind]
    out = [_extras(kind, dict(r)) for r in _table(which, table, label)]
    if kind == "products":
        names = {c["company_id"]: c["company_name"] for c in _rows("companies")}
        for p in out:
            p["company_name"] = names.get(p["company_id"], "")
    if kind == "herb_products":
        names = {m["id"]: m["company_name"] for m in _rows("makers")}
        for p in out:
            p["maker_name"] = names.get(p["manufacturer_id"], "")
    return tuple(out)


def rows(kind: str) -> list[dict]:
    """All rows of a kind (fresh dict copies; ordered by display name)."""
    return [dict(r) for r in _rows(kind)]


def extra(name: str) -> list[dict]:
    which, table, pk = EXTRA_TABLES[name]
    return [dict(r) for r in _table(which, table, pk)]


def get(kind: str, item_id: int) -> dict | None:
    pk = KINDS[kind][2]
    return next((dict(r) for r in _rows(kind) if r[pk] == item_id), None)


def pk(kind: str) -> str:
    return KINDS[kind][2]


def stats() -> dict:
    s = {kind: len(_rows(kind)) for kind in KINDS}
    s["tea_countries"] = len({t["country"] for t in _rows("teas") if t["country"]})
    s["tea_categories"] = len({t["category"] for t in _rows("teas")})
    s["safety_records"] = len(extra("safety"))
    s["traditions"] = len(extra("traditions"))
    return s


def read_markdown(name: str) -> str:
    p = DOCS[name]
    return p.read_text(encoding="utf-8") if p.exists() else ""
