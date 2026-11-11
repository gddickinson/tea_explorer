"""Aggregates for the web dashboard and the brewing timer.

Dashboard counts follow the desktop Dashboard (visualizations/chart_generator.py counts categories and origins with
collections.Counter); origins are grouped by country here (the desktop chart uses the full origin text). The journal
rating chart is drawn in the browser from /api/journal, so it exists only in the local app.
"""
from collections import Counter

from brewing_presets import TIMER_PRESETS, preset_label

from . import data

BAND_ORDER = ["Very Low", "Low", "Low-Medium", "Medium", "Medium-High", "High"]


def _counts(values, top: int | None = None) -> list[list]:
    """[[value, count], ...] most common first (ties by value), optionally only the top N."""
    c = Counter(v for v in values if v)
    return [[k, n] for k, n in sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0]).lower()))][:top]


def dashboard() -> dict:
    teas, tisanes = data.rows("teas"), data.rows("tisanes")
    bands = Counter(t["caffeine"] for t in teas if t["caffeine"])
    return {
        "tea_categories": _counts(t["category"] for t in teas),
        "tea_countries": _counts((t["country"] for t in teas), 12),
        "tea_caffeine": [[b, bands[b]] for b in BAND_ORDER if bands[b]]
                        + [[b, n] for b, n in sorted(bands.items()) if b not in BAND_ORDER],
        "tea_temps": sorted(_counts(t["brew_temp_c"] for t in teas)),
        "product_types": _counts(p["tea_type"] for p in data.rows("products")),
        "company_segments": _counts(c["market_segment"] for c in data.rows("companies")),
        "company_countries": _counts((c["country"] for c in data.rows("companies")), 10),
        "tisane_families": _counts((t["plant_family"] for t in tisanes), 12),
        "tisane_traditions": _counts((x for t in tisanes for x in t["tradition_terms"]), 10),
        "tisane_parts": _counts((t["plant_part_used"] for t in tisanes), 10),
        "caffeine_free": [["caffeine-free", sum(t["caffeine_free"] for t in tisanes)],
                          ["contains caffeine", sum(not t["caffeine_free"] for t in tisanes)]],
    }


def timer() -> dict:
    """The desktop presets plus every steep time in the databases, for the timer's picker."""
    def steep(kind, r, label, temp="brew_temp_c"):
        return {"kind": kind, "id": r[data.pk(kind)], "name": r[label], "steep_time": r.get("steep_time") or "",
                "temp_c": r.get(temp)}
    return {"presets": [{"name": n, "seconds": s, "label": preset_label(n, s)} for n, s in TIMER_PRESETS],
            "teas": [steep("teas", t, "name") for t in data.rows("teas")],
            "blends": [steep("blends", b, "blend_name") for b in data.rows("blends")],
            "tisanes": [steep("tisanes", t, "name") for t in data.rows("tisanes")]}
