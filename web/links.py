"""Cross-links between the tables for the web detail pages.

The databases store relationships as free text (a tea's `cultivars` and `origin`, a region's `famous_teas`, a blend's
`popular_brands`, a herb region's `primary_herbs`), so links are found by name mentions with word boundaries:
`mentions(text, name)` is true when the name (without a trailing "(...)"), or the alternative name inside the
parentheses, occurs in the text as whole words. Similar teas come from the repo's own RecommendationEngine.
"""
import re
from functools import lru_cache

from models import Tea
from recommendations import RecommendationEngine

from . import data

_ENGINE = RecommendationEngine()
# Words dropped from a region name before matching it in a tea's origin ("Fujian Province" -> "Fujian").
_REGION_NOISE = re.compile(r"\b(province|district|region|state|nature reserve|high mountains|valley)\b", re.I)


def name_keys(name: str) -> list[str]:
    """'Goji Berries (Gou Qi Zi)' -> ['goji berries', 'gou qi zi']; 'Uji, Kyoto' -> ['uji, kyoto']."""
    name = (name or "").strip().lower()
    keys = []
    m = re.match(r"^(.*?)\s*\((.*?)\)\s*$", name)
    if m:
        keys += [m.group(1).strip(), m.group(2).strip()]
    else:
        keys.append(name)
    return [k for k in keys if len(k) >= 3]


def mentions(text: str, name: str) -> bool:
    text = (text or "").lower()
    return any(re.search(r"(?<!\w)" + re.escape(k) + r"(?!\w)", text) for k in name_keys(name))


def _brief(kind: str, r: dict, *fields) -> dict:
    pk = data.pk(kind)
    label = data.KINDS[kind][3]
    return {"id": r[pk], "name": r[label], **{f: r.get(f) for f in fields}}


# --- teas, regions, cultivars --------------------------------------------------------------------------------------
def region_key(name: str) -> str:
    """'Fujian Province' -> 'fujian', 'Uji, Kyoto' -> 'uji', 'Phoenix Mountain (Fenghuang)' -> 'phoenix mountain'."""
    base = name.split("(")[0].split(",")[0]
    return " ".join(_REGION_NOISE.sub(" ", base).split()).lower()


def tea_in_region(tea: dict, region: dict) -> bool:
    """A tea belongs to a region if the region (name without "Province" etc.) is named in the tea's origin, or the
    region lists the tea among its famous teas."""
    if tea["country"] != region["country"]:
        return False
    key = region_key(region["name"])
    in_origin = key and key != tea["country"].lower() and re.search(r"(?<!\w)" + re.escape(key) + r"(?!\w)",
                                                                     (tea.get("origin") or "").lower())
    return bool(in_origin) or mentions(region.get("famous_teas"), tea["name"])


def regions_for_tea(tea: dict) -> dict:
    same = [r for r in data.rows("regions") if r["country"] == tea["country"]]
    matched = [r for r in same if tea_in_region(tea, r)]
    return {"matched": [_brief("regions", r, "country") for r in matched],
            "country": [_brief("regions", r, "country") for r in same if r not in matched]}


def teas_for_region(region: dict) -> dict:
    same = [t for t in data.rows("teas") if t["country"] == region["country"]]
    matched = [t for t in same if tea_in_region(t, region)]
    return {"matched": matched, "country": [t for t in same if t not in matched]}


def cultivars_for_tea(tea: dict) -> list[dict]:
    return [_brief("cultivars", c, "species") for c in data.rows("cultivars") if mentions(tea.get("cultivars"), c["name"])]


def teas_for_cultivar(cultivar: dict) -> list[dict]:
    return [t for t in data.rows("teas") if mentions(t.get("cultivars"), cultivar["name"])]


@lru_cache(maxsize=1)
def _tea_models() -> tuple:
    return tuple(Tea.from_dict(t) for t in data.rows("teas"))


def similar_teas(tea_id: int, n: int = 5) -> list[dict]:
    """RecommendationEngine.get_similar_teas (category, origin, caffeine, flavour words, processing), as on the
    desktop "Similar Teas" button."""
    teas = _tea_models()
    me = next(t for t in teas if t.tea_id == tea_id)
    by_id = {t["id"]: t for t in data.rows("teas")}
    return [_brief("teas", by_id[t.tea_id], "category", "country") for t in _ENGINE.get_similar_teas(me, list(teas), n)]


# --- blends and companies ------------------------------------------------------------------------------------------
def companies_for_blend(blend: dict) -> list[dict]:
    return [_brief("companies", c, "country") for c in data.rows("companies")
            if mentions(blend.get("popular_brands"), c["company_name"])]


def blends_for_company(company: dict) -> list[dict]:
    return [_brief("blends", b, "category") for b in data.rows("blends")
            if mentions(b.get("popular_brands"), company["company_name"])]


def company_detail(company: dict) -> dict:
    cid = company["company_id"]
    return {**company, "products": [p for p in data.rows("products") if p["company_id"] == cid],
            "distribution": [d for d in data.extra("distribution") if d["company_id"] == cid],
            "blends": blends_for_company(company)}


# --- tisanes -------------------------------------------------------------------------------------------------------
def family_for(tisane: dict) -> dict | None:
    fam = (tisane.get("plant_family") or "").split("/")[0].strip()
    return next((_brief("families", f) for f in data.rows("families") if f["family_name"] == fam), None)


def tisanes_in_family(family: dict) -> list[dict]:
    name = family["family_name"]
    return [t for t in data.rows("tisanes") if name in (t.get("plant_family") or "").split("/")]


def herb_regions_for(tisane: dict) -> list[dict]:
    return [_brief("herb_regions", r, "country") for r in data.rows("herb_regions")
            if mentions(r.get("primary_herbs"), tisane["name"])]


def tisanes_for_herb_region(region: dict) -> list[dict]:
    return [t for t in data.rows("tisanes") if mentions(region.get("primary_herbs"), t["name"])]


def herb_products_for(tisane: dict) -> list[dict]:
    keys = name_keys(tisane["name"])[:1]
    return [p for p in data.rows("herb_products")
            if any(mentions(p.get(f), k) for f in ("product_name", "special_features") for k in keys)]


def tisane_detail(tisane: dict) -> dict:
    tid = tisane["id"]
    return {**tisane, "safety": [s for s in data.extra("safety") if s["tisane_id"] == tid],
            "family": family_for(tisane), "herb_regions": herb_regions_for(tisane),
            "products": herb_products_for(tisane)}
