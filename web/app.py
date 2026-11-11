"""FastAPI web app for the Tea & Tisane Collection Explorer: serves the front end in static/ and the JSON API under /api.

Run with `python run_web.py` (http://127.0.0.1:8114, local only). Data is read read-only from tea_collection.db and
tisane_collection.db via web/data.py. `scripts/build_static.py` exports every path in STATIC_ENDPOINTS to JSON for the
GitHub Pages site, so keep that list in step with the GET routes below. List endpoints with query parameters are
answered on the static site by static_api.js filtering the exported full lists (same rules as web/search.py).
The tea journal is personal and local-only: it is never exported.
"""
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from world_shapes import LAND_POLYGONS, LAND_SOURCE  # noqa: E402

from . import data, journal, links, summary  # noqa: E402
from .search import facets, filter_rows  # noqa: E402

STATIC = Path(__file__).resolve().parent / "static"
KINDS = list(data.KINDS)

app = FastAPI(title="Tea & Tisane Collection Explorer")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


def one(kind: str, item_id: int) -> dict:
    row = data.get(kind, item_id)
    if row is None:
        raise HTTPException(404, f"unknown {kind} id {item_id}")
    return row


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/stats")
def stats():
    return data.stats()


@app.get("/api/facets")
def all_facets():
    """Filter options with counts for every list page."""
    return {kind: facets(kind, data.rows(kind)) for kind in KINDS}


@app.get("/api/dashboard")
def dashboard():
    return summary.dashboard()


@app.get("/api/timer")
def timer():
    return summary.timer()


@app.get("/api/traditions")
def traditions():
    """The traditional medicine systems (tisane database), each with the number of tisanes naming it."""
    terms = facets("tisanes", data.rows("tisanes"))["tradition"]
    return [{**t, "tisanes": terms.get(t["system_name"], 0)} for t in data.extra("traditions")]


@app.get("/api/world")
def world():
    """Land outlines (Natural Earth 1:110m, via world_shapes.py) plus tea and herb region markers for the SVG map."""
    keep = ("id", "name", "country", "latitude", "longitude")
    land = [[[list(p) for p in ring] for ring in poly] for poly in LAND_POLYGONS]
    return {"land": land, "source": LAND_SOURCE,
            "regions": [{k: r[k] for k in keep} for r in data.rows("regions")],
            "herb_regions": [{k: r[k] for k in keep} for r in data.rows("herb_regions")]}


@app.get("/api/content/{name}")
def content(name: str):
    if name not in data.DOCS:
        raise HTTPException(404, "unknown content")
    return {"name": name, "markdown": data.read_markdown(name)}


@app.get("/api/search")
def search(q: str = ""):
    """Search every table at once (empty q returns nothing)."""
    return {kind: filter_rows(kind, data.rows(kind), {"q": q}) if q.strip() else [] for kind in KINDS}


def _list_route(kind: str):
    def handler(request: Request):
        return filter_rows(kind, data.rows(kind), dict(request.query_params))
    handler.__name__ = f"list_{kind}"
    app.get(f"/api/{kind}")(handler)


for _kind in KINDS:
    _list_route(_kind)

# Detail pages: the row plus its cross-links (web/links.py).
DETAIL = {
    "teas": lambda t: {**t, "regions": links.regions_for_tea(t), "cultivar_links": links.cultivars_for_tea(t),
                       "similar": links.similar_teas(t["id"])},
    "blends": lambda b: {**b, "companies": links.companies_for_blend(b)},
    "cultivars": lambda c: {**c, "teas": links.teas_for_cultivar(c)},
    "regions": lambda r: {**r, "teas": links.teas_for_region(r)},
    "companies": links.company_detail,
    "products": lambda p: p,
    "tisanes": links.tisane_detail,
    "families": lambda f: {**f, "tisanes": links.tisanes_in_family(f)},
    "herb_regions": lambda r: {**r, "tisanes": links.tisanes_for_herb_region(r)},
    "makers": lambda m: {**m, "products": [p for p in data.rows("herb_products") if p["manufacturer_id"] == m["id"]]},
}


@app.get("/api/{kind}/{item_id}")
def detail(kind: str, item_id: int):
    if kind not in DETAIL:
        raise HTTPException(404, f"no detail pages for {kind}")
    return DETAIL[kind](one(kind, item_id))


# --- local-only: tea journal (personal notes; never exported to the static site) -----------------------------------
class JournalEntry(BaseModel):
    tea_name: str
    rating: int = 3
    brewing: str = ""
    notes: str = ""


class JournalDelete(BaseModel):
    entry_id: int


@app.get("/api/journal")
def journal_list():
    names = sorted({t["name"] for t in data.rows("teas")} | {b["blend_name"] for b in data.rows("blends")}
                   | {t["name"] for t in data.rows("tisanes")}, key=str.lower)
    return {"entries": journal.load(), "names": names}


@app.post("/api/journal")
def journal_add(entry: JournalEntry):
    try:
        return journal.add(entry.tea_name, entry.rating, entry.brewing, entry.notes)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/api/journal/delete")
def journal_delete(req: JournalDelete):
    try:
        journal.delete(req.entry_id)
    except KeyError:
        raise HTTPException(404, f"no journal entry {req.entry_id}")
    return {"deleted": req.entry_id}


def _detail_paths() -> list[str]:
    return [f"/{kind}/{r[data.pk(kind)]}" for kind in DETAIL for r in data.rows(kind)]


# GET paths (without the /api prefix) written to the static site as api/<path>.json. The journal is deliberately absent.
STATIC_ENDPOINTS = (["/stats", "/facets", "/dashboard", "/timer", "/traditions", "/world"]
                    + [f"/content/{name}" for name in data.DOCS] + [f"/{kind}" for kind in KINDS] + _detail_paths())
