"""Web interface tests: every exported endpoint answers, the static build is complete, and the JS engine tests pass.

Run: python -m pytest -q tests/test_web.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from web.app import STATIC, STATIC_ENDPOINTS, app  # noqa: E402

client = TestClient(app)


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200 and "static/main.js" in r.text


@pytest.mark.parametrize("path", STATIC_ENDPOINTS)
def test_endpoint(path):
    r = client.get("/api" + path)
    assert r.status_code == 200, r.text
    assert r.json() is not None


def test_static_build(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert (tmp_path / "site" / "index.html").read_text().count("APP_STATIC") == 1
    for path in STATIC_ENDPOINTS:
        assert (tmp_path / "site" / "api" / (path.strip("/") + ".json")).exists()


def test_static_assets_referenced_exist():
    html = (STATIC / "index.html").read_text()
    for name in ("style.css", "main.js"):
        assert f"static/{name}" in html and (STATIC / name).exists()


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_js_engine():
    tests = sorted(STATIC.glob("*.test.mjs"))
    for t in tests:
        r = subprocess.run(["node", str(t)], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr


# --- Tea & Tisane Collection Explorer: project-specific API tests ---------------------------------------------------
import hashlib  # noqa: E402
import json  # noqa: E402

from web import data, links  # noqa: E402
from web.app import KINDS  # noqa: E402
from web.search import SPECS  # noqa: E402


def _md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def test_counts_match_database():
    s = client.get("/api/stats").json()
    assert (s["teas"], s["blends"], s["cultivars"], s["regions"], s["companies"], s["products"]) == (160, 70, 59, 42, 54, 117)
    assert (s["tisanes"], s["families"], s["herb_regions"], s["makers"], s["herb_products"]) == (154, 43, 20, 39, 58)
    for kind in KINDS:
        assert len(client.get(f"/api/{kind}").json()) == len(data.rows(kind))


def test_databases_opened_read_only():
    before = [_md5(data.db_path(w)) for w in ("tea", "tisane")]
    for which, table in (("tea", "teas"), ("tisane", "tisanes")):
        conn = data.connect(which)
        with pytest.raises(Exception):
            conn.execute(f"UPDATE {table} SET name = 'x'")
        conn.close()
    for path in STATIC_ENDPOINTS[:40]:
        client.get("/api" + path)
    assert [_md5(data.db_path(w)) for w in ("tea", "tisane")] == before


def test_filters():
    oolong = client.get("/api/teas", params={"category": "Oolong"}).json()
    assert len(oolong) == 36 and all(t["category"] == "Oolong" for t in oolong)
    jp = client.get("/api/teas", params={"country": "Japan"}).json()
    assert len(jp) == 17 and all(t["origin"].startswith("Japan") for t in jp)
    assert all("assamica" in c["species"] for c in client.get("/api/cultivars", params={"species": "var. assamica"}).json())
    uk = client.get("/api/companies", params={"country": "United Kingdom"}).json()
    assert {c["country_of_origin"] for c in uk} == {"UK", "United Kingdom"}  # one filter for both spellings
    cf = client.get("/api/tisanes", params={"caffeine_free": "1"}).json()
    assert len(cf) == 149 and all(t["caffeine_free"] for t in cf)
    ayur = client.get("/api/tisanes", params={"tradition": "Ayurveda"}).json()
    assert ayur and all("Ayurveda" in t["tradition_terms"] for t in ayur)
    org = client.get("/api/products", params={"organic": "1"}).json()
    assert org and all(p["organic"] for p in org)
    assert client.get("/api/teas", params={"q": "zzzz-none"}).json() == []
    res = client.get("/api/search", params={"q": "chamomile"}).json()
    assert set(res) == set(KINDS) and res["tisanes"] and res["herb_regions"]


def test_details_and_links():
    assert client.get("/api/teas/99999").status_code == 404
    assert client.get("/api/content/nope").status_code == 404
    assert client.get("/api/herb_products/1").status_code == 404  # listed on maker pages only
    silver = client.get("/api/teas/1").json()
    assert silver["name"].startswith("Bai Hao Yin Zhen")
    assert {c["name"] for c in silver["cultivar_links"]} >= {"Da Bai", "Xiao Bai"}
    assert "Fujian Province" in {r["name"] for r in silver["regions"]["matched"]}
    assert len(silver["similar"]) == 5 and all(s["id"] != 1 for s in silver["similar"])
    fujian = next(r for r in data.rows("regions") if r["name"] == "Fujian Province")
    assert 1 in {t["id"] for t in client.get(f"/api/regions/{fujian['id']}").json()["teas"]["matched"]}
    yabukita = next(c for c in data.rows("cultivars") if c["name"] == "Yabukita")
    assert len(client.get(f"/api/cultivars/{yabukita['id']}").json()["teas"]) >= 5
    valerian = next(t for t in data.rows("tisanes") if t["name"] == "Valerian Root")
    assert len(client.get(f"/api/tisanes/{valerian['id']}").json()["safety"]) == 3  # every record, not just the first
    ceder = next(r for r in data.rows("herb_regions") if r["name"] == "Cederberg Region")
    assert {"Rooibos", "Honeybush"} <= {t["name"] for t in client.get(f"/api/herb_regions/{ceder['id']}").json()["tisanes"]}
    twinings = next(c for c in data.rows("companies") if c["company_name"] == "Twinings")
    tw = client.get(f"/api/companies/{twinings['company_id']}").json()
    assert tw["products"] and tw["distribution"] and tw["blends"]
    w = client.get("/api/world").json()
    assert len(w["regions"]) == 42 and len(w["herb_regions"]) == 20 and "Natural Earth" in w["source"]
    assert client.get("/api/content/guide").json()["markdown"].startswith("# Complete List of Tea Varieties")
    assert client.get("/api/content/herbal").json()["markdown"].startswith("# Tisane Explorer Documentation")


def test_similar_teas_use_recommendation_engine():
    from models import Tea
    from recommendations import RecommendationEngine
    teas = [Tea.from_dict(t) for t in data.rows("teas")]
    want = [t.tea_id for t in RecommendationEngine().get_similar_teas(teas[10], teas, 5)]
    assert [s["id"] for s in links.similar_teas(teas[10].tea_id)] == want


def test_mentions_word_boundaries():
    assert links.mentions("Da Bai or Xiao Bai (aged)", "Da Bai")
    assert not links.mentions("Fuding Da Baicha", "Da Bai")
    assert links.mentions("Goji berries (Gou Qi Zi)", "Goji Berries (Gou Qi Zi)")
    assert links.region_key("Fujian Province") == "fujian" and links.region_key("Uji, Kyoto") == "uji"


def test_dashboard_and_timer():
    d = client.get("/api/dashboard").json()
    assert dict(d["tea_categories"])["Black"] == 47 and sum(n for _, n in d["tea_categories"]) == 160
    assert sum(n for _, n in d["caffeine_free"]) == 154
    t = client.get("/api/timer").json()
    from brewing_presets import TIMER_PRESETS
    assert [(p["name"], p["seconds"]) for p in t["presets"]] == TIMER_PRESETS
    assert t["presets"][0]["label"] == "Green Tea (3 min)"
    assert len(t["teas"]) == 160 and len(t["tisanes"]) == 154


def test_journal_local_only(tmp_path, monkeypatch):
    jf = tmp_path / "journal.json"
    monkeypatch.setenv("TEA_JOURNAL", str(jf))
    assert client.get("/api/journal").json()["entries"] == []
    r = client.post("/api/journal", json={"tea_name": "Gyokuro", "rating": 5, "notes": "umami"})
    assert r.status_code == 200 and r.json()["entry_id"] == 1
    saved = json.loads(jf.read_text())
    assert saved[0]["tea_name"] == "Gyokuro" and saved[0]["rating"] == 5
    assert client.post("/api/journal", json={"tea_name": "", "rating": 4}).status_code == 400
    assert client.post("/api/journal", json={"tea_name": "Sencha", "rating": 9}).status_code == 400
    client.post("/api/journal", json={"tea_name": "Sencha", "rating": 3})
    assert client.post("/api/journal/delete", json={"entry_id": 1}).status_code == 200
    assert [e["tea_name"] for e in client.get("/api/journal").json()["entries"]] == ["Sencha"]
    assert client.post("/api/journal/delete", json={"entry_id": 42}).status_code == 404
    assert not any(p.startswith("/journal") for p in STATIC_ENDPOINTS)


def test_static_build_has_no_journal(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import build_static
    build_static.build(tmp_path / "site")
    assert not list((tmp_path / "site" / "api").rglob("*journal*"))
    text = "".join(p.read_text() for p in (tmp_path / "site" / "api").rglob("*.json"))
    assert "admiring look" not in text  # a phrase from the shipped tea_journal.json


def test_search_fixture_is_current():
    """tests/fixtures/search_cases.json (used by search_engine.test.mjs) matches web/search.py on today's data."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import make_search_fixture
    fx = json.loads(make_search_fixture.OUT.read_text())
    assert fx == json.loads(json.dumps(make_search_fixture.build())), "run python scripts/make_search_fixture.py"


PARITY = [("teas", {"category": "Green", "q": "japan"}), ("teas", {"caffeine": "Low"}), ("teas", {"country": "India"}),
          ("blends", {"q": "spice"}), ("cultivars", {"species": "var. sinensis", "q": "japan"}), ("regions", {"q": "mountain"}),
          ("companies", {"cert": "Rainforest Alliance"}), ("companies", {"segment": "luxury"}),
          ("products", {"fair_trade": "1"}), ("products", {"company": "1", "q": "tea"}), ("products", {"bag": "pyramid"}),
          ("tisanes", {"family": "Lamiaceae", "caffeine_free": "1"}), ("tisanes", {"tradition": "Traditional Chinese Medicine"}),
          ("families", {"q": "mint"}), ("herb_regions", {"country": "Egypt"}), ("makers", {"cert": "Fair Trade"}),
          ("herb_products", {"q": "sleep"})]


@pytest.mark.skipif(not shutil.which("node"), reason="node not installed")
def test_static_search_parity(tmp_path):
    """static_api.js filtering (search_engine.js) returns the same ids as the server for the same queries, on all rows."""
    full = {kind: client.get(f"/api/{kind}").json() for kind in KINDS}
    (tmp_path / "full.json").write_text(json.dumps(full))
    (tmp_path / "cases.json").write_text(json.dumps(PARITY))
    script = (f"import {{ filterRows, SPECS }} from {json.dumps((STATIC / 'search_engine.js').as_uri())};\n"
              "import { readFileSync } from 'node:fs';\n"
              f"const full = JSON.parse(readFileSync({json.dumps(str(tmp_path / 'full.json'))}, 'utf8'));\n"
              f"const cases = JSON.parse(readFileSync({json.dumps(str(tmp_path / 'cases.json'))}, 'utf8'));\n"
              "console.log(JSON.stringify(cases.map(([k, q]) => filterRows(k, full[k], q).map(r => r[SPECS[k].id]))));")
    r = subprocess.run(["node", "--input-type=module", "-e", script], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    for (kind, q), got in zip(PARITY, json.loads(r.stdout)):
        want = [row[SPECS[kind]["id"]] for row in client.get(f"/api/{kind}", params=q).json()]
        assert got == want, (kind, q)
        assert want, (kind, q)  # every case should exercise a non-empty result


def test_map_projection_and_alignment():
    """Land outlines and region markers share one equirectangular projection; markers fall on (or next to) land."""
    import world_shapes as ws
    assert ws.project(-180, 90, 1000, 500) == (0, 0) and ws.project(180, -90, 1000, 500) == (1000, 500)
    x, y = ws.project(118.0, 26.5, 1000, 500)  # Fujian Province (geo.test.mjs checks the JS side)
    assert abs(x - 827.7778) < 1e-3 and abs(y - 176.3889) < 1e-3
    near = lambda lon, lat: any(ws.on_land(lon + dx, lat + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))  # noqa: E731
    for r in data.rows("regions") + data.rows("herb_regions"):
        assert near(r["longitude"], r["latitude"]), r["name"]
    for lon, lat in [(0, 0), (-150, 0), (-30, 30), (80, -30)]:  # open ocean
        assert not ws.on_land(lon, lat), (lon, lat)
    assert ws.LAND_FILE.stat().st_size < 150_000
