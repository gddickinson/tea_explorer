"""Search and filter rules for every list endpoint.

Mirrored exactly by web/static/search_engine.js, which answers the same queries on the static site from the exported
full lists (tests/test_web.py checks both give the same ids on the real data). Rules:
- `q`: split into words; every word must occur (case-insensitive substring) in the row's searchable text fields.
- `exact` filters: str(column) must equal the value.
- `contains` filters: case-insensitive substring (like the desktop app's `species LIKE '%...%'`).
- `flag` filters: value "1" keeps rows where the column is true.
- `anyof` filters: the column is a list (derived terms, see web/data.py) and must contain the value.
"""

# kind -> searchable text fields, filters by type, id column
SPECS = {
    "teas": {"text": ["name", "category", "origin", "processing", "flavor_profile", "aroma", "appearance", "cultivars",
                      "history"],
             "exact": {"category": "category", "country": "country", "caffeine": "caffeine"},
             "contains": {}, "flag": {}, "anyof": {}, "id": "id"},
    "blends": {"text": ["blend_name", "category", "base_tea", "ingredients", "flavor_profile", "aroma", "popular_brands",
                        "description"],
               "exact": {"category": "category", "caffeine": "caffeine"}, "contains": {}, "flag": {}, "anyof": {},
               "id": "blend_id"},
    "cultivars": {"text": ["name", "species", "origin_country", "leaf_size", "characteristics", "common_uses", "notes"],
                  "exact": {"country": "origin_country"}, "contains": {"species": "species"}, "flag": {}, "anyof": {},
                  "id": "id"},
    "regions": {"text": ["name", "country", "climate", "famous_teas", "description"],
                "exact": {"country": "country"}, "contains": {}, "flag": {}, "anyof": {}, "id": "id"},
    "companies": {"text": ["company_name", "parent_company", "headquarters_city", "country_of_origin", "certifications",
                           "description"],
                  "exact": {"country": "country", "segment": "market_segment"}, "contains": {}, "flag": {},
                  "anyof": {"cert": "cert_terms"}, "id": "company_id"},
    "products": {"text": ["product_name", "company_name", "tea_type", "tea_category", "bag_type", "format",
                          "special_features", "countries_available"],
                 "exact": {"company": "company_id", "type": "tea_type", "category": "tea_category", "bag": "bag_type",
                           "currency": "price_currency"},
                 "contains": {}, "flag": {"organic": "organic", "fair_trade": "fair_trade"}, "anyof": {},
                 "id": "product_id"},
    "tisanes": {"text": ["name", "scientific_name", "plant_family", "plant_part_used", "origin_region", "tradition",
                         "traditional_uses", "research_benefits", "key_compounds", "flavor_profile", "aroma"],
                "exact": {"family": "plant_family"}, "contains": {},
                "flag": {"caffeine_free": "caffeine_free"}, "anyof": {"tradition": "tradition_terms"}, "id": "id"},
    "families": {"text": ["family_name", "characteristics", "major_genera", "common_uses", "notes"],
                 "exact": {}, "contains": {}, "flag": {}, "anyof": {}, "id": "id"},
    "herb_regions": {"text": ["name", "country", "climate_type", "primary_herbs", "key_producers", "description"],
                     "exact": {"country": "country"}, "contains": {}, "flag": {}, "anyof": {}, "id": "id"},
    "makers": {"text": ["company_name", "headquarters_city", "headquarters_country", "parent_company", "certifications",
                        "market_segment", "notable_products", "description"],
               "exact": {"country": "country"}, "contains": {}, "flag": {}, "anyof": {"cert": "cert_terms"}, "id": "id"},
    "herb_products": {"text": ["product_name", "maker_name", "tisane_type", "format", "certifications",
                               "special_features", "countries_available"],
                      "exact": {"maker": "manufacturer_id", "type": "tisane_type"}, "contains": {}, "flag": {},
                      "anyof": {}, "id": "id"},
}

# Facets (filter drop-downs with counts): exact and anyof filters. Contains filters use fixed choices in the UI.
FACETS = {kind: {**spec["exact"], **spec["anyof"]} for kind, spec in SPECS.items()}


def _text(row: dict, fields: list[str]) -> str:
    return " ".join(str(row.get(f) or "") for f in fields).lower()


def _given(params: dict, p: str) -> bool:
    return params.get(p) not in (None, "")


def filter_rows(kind: str, rows: list[dict], params: dict) -> list[dict]:
    spec = SPECS[kind]
    words = str(params.get("q") or "").lower().split()
    out = []
    for r in rows:
        if any(_given(params, p) and str(r.get(col)) != str(params[p]) for p, col in spec["exact"].items()):
            continue
        if any(_given(params, p) and str(params[p]).lower() not in str(r.get(col) or "").lower()
               for p, col in spec["contains"].items()):
            continue
        if any(str(params.get(p) or "") == "1" and not r.get(col) for p, col in spec["flag"].items()):
            continue
        if any(_given(params, p) and str(params[p]) not in (r.get(col) or []) for p, col in spec["anyof"].items()):
            continue
        if words:
            text = _text(r, spec["text"])
            if not all(w in text for w in words):
                continue
        out.append(r)
    return out


def facets(kind: str, rows: list[dict]) -> dict:
    """{param: {value: count}} for each facet of a kind, sorted by value (case-insensitive)."""
    out = {}
    for param, col in FACETS[kind].items():
        counts: dict = {}
        for r in rows:
            vals = r.get(col) if param in SPECS[kind]["anyof"] else [r.get(col)]
            for v in vals or []:
                if v not in (None, ""):
                    counts[str(v)] = counts.get(str(v), 0) + 1
        out[param] = dict(sorted(counts.items(), key=lambda kv: kv[0].lower()))
    return out
