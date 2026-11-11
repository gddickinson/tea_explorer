// Home (hero, live counts, entry cards, map), search across every table, and About.
import { route, api, app, esc, list, isStatic } from './core.js';
import { worldSvg } from './regions.js';
import { trim } from './ui.js';

const DOORS = [
  ['#/teas', 'Tea varieties', 'White, green, yellow, oolong, black and pu-erh: origin, flavour, brewing, caffeine and history.', 'teas'],
  ['#/blends', 'Blends', 'Earl Grey, chai, jasmine and more: ingredients, serving suggestions and popular brands.', 'blends'],
  ['#/cultivars', 'Cultivars', 'The tea plants behind the leaf, from Da Bai to Yabukita, and the teas made from them.', 'cultivars'],
  ['#/tisanes', 'Herbal tisanes', 'Herbs from many traditions: uses, research, compounds, brewing and safety notes.', 'tisanes'],
  ['#/companies', 'Tea companies', 'Brands from supermarket staples to luxury tea houses, with their products and retailers.', 'companies'],
  ['#/map', 'Regions map', 'Tea- and herb-growing regions on a world map, with climate, elevation and famous teas.', 'regions'],
  ['#/timer', 'Brewing timer', 'Presets for each tea type, or the steep time of any tea, blend or tisane.', null],
  ['#/compare', 'Compare teas', 'Up to three teas side by side: caffeine, temperature, steep time and flavour.', null],
  ['#/dashboard', 'Dashboard', 'The collection in charts: categories, countries, caffeine, brands and plant families.', null],
  ['#/guide', 'Varieties guide', 'A list of tea varieties by type and country, plus the history of tea and a glossary.', null],
  ['#/herbal', 'Herbal reference', 'The tisane research notes: herbs, manufacturers, regions, history and safety.', null],
  ['#/journal', 'Tea journal', 'Rate and note the teas you taste (local app only).', null],
];

route('home', async () => {
  const [s, world] = await Promise.all([api('/stats'), api('/world')]);
  app().innerHTML = `
  <section class="hero">
    <p class="kicker">Teas · Tisanes · Brands · Regions</p>
    <h1 class="glow">Tea &amp; Tisane Collection Explorer</h1>
    <p class="lead">Explore tea varieties, blends and cultivars, herbal tisanes, tea companies and their products, and
    the regions where tea and herbs grow, with a brewing timer, a varieties guide, the history of tea and a glossary.</p>
    <form id="hsearch" role="search" class="row"><div><label for="hs-q">Search everything</label>
      <input id="hs-q" type="search" placeholder="e.g. Darjeeling, bergamot, chamomile, Twinings"></div>
      <div style="flex:0"><button type="submit">Search</button></div></form>
  </section>
  <div class="tiles">
    <a class="tile" href="#/teas"><b>${s.teas}</b><span>tea varieties</span></a>
    <a class="tile" href="#/blends"><b>${s.blends}</b><span>blends</span></a>
    <a class="tile" href="#/cultivars"><b>${s.cultivars}</b><span>cultivars</span></a>
    <a class="tile" href="#/tisanes"><b>${s.tisanes}</b><span>herbal tisanes</span></a>
    <a class="tile" href="#/companies"><b>${s.companies + s.makers}</b><span>tea and herbal brands</span></a>
    <a class="tile" href="#/map"><b>${s.regions + s.herb_regions}</b><span>growing regions</span></a>
  </div>
  <div class="grid wide">${list(DOORS, ([href, t, d, k]) => `<a class="card door" href="${href}"><b>${t}${k ? ` <em class="n">${s[k]}</em>` : ''}</b><span>${d}</span></a>`)}</div>
  <h2>Where tea and herbs grow</h2>
  <a class="stage map" href="#/map" aria-label="Open the regions map">${worldSvg(world).replace(/<a [^>]*>|<\/a>/g, '')}</a>`;
  document.getElementById('hsearch').addEventListener('submit', e => {
    e.preventDefault();
    location.hash = '#/search?q=' + encodeURIComponent(document.getElementById('hs-q').value.trim());
  });
});

const GROUPS = [
  ['teas', 'Teas', t => [`#/tea/${t.id}`, t.name, `${t.category} · ${t.country}`, t.flavor_profile]],
  ['blends', 'Blends', b => [`#/blend/${b.blend_id}`, b.blend_name, b.category, b.ingredients]],
  ['cultivars', 'Cultivars', c => [`#/cultivar/${c.id}`, c.name, c.species, c.characteristics]],
  ['tisanes', 'Tisanes', t => [`#/tisane/${t.id}`, t.name, t.scientific_name, t.traditional_uses]],
  ['families', 'Plant families', f => [`#/family/${f.id}`, f.family_name, f.major_genera, f.common_uses]],
  ['regions', 'Tea regions', r => [`#/region/${r.id}`, r.name, r.country, r.famous_teas]],
  ['herb_regions', 'Herb regions', r => [`#/herbregion/${r.id}`, r.name, r.country, r.primary_herbs]],
  ['companies', 'Tea companies', c => [`#/company/${c.company_id}`, c.company_name, c.country_of_origin, c.description]],
  ['products', 'Tea products', p => [`#/product/${p.product_id}`, p.product_name, p.company_name, p.special_features]],
  ['makers', 'Herbal brands', m => [`#/maker/${m.id}`, m.company_name, m.headquarters_country, m.description]],
  ['herb_products', 'Herbal products', p => [`#/maker/${p.manufacturer_id}`, p.product_name, p.maker_name, p.special_features]],
];

route('search', async (_args, query) => {
  app().innerHTML = `<p class="kicker">Search</p><h1>Search everything</h1>
    <div class="panel"><label for="s-q">Search teas, blends, cultivars, tisanes, brands, products and regions</label>
    <input id="s-q" type="search" value="${esc(query.q || '')}" placeholder="e.g. smoky, Japan, sleep, Rainforest Alliance"></div>
    <div id="s-out" aria-live="polite"></div>`;
  const input = document.getElementById('s-q');
  let seq = 0;
  async function run() {
    const n = ++seq, q = input.value.trim();
    history.replaceState(null, '', '#/search' + (q ? '?q=' + encodeURIComponent(q) : ''));
    const res = await api('/search?q=' + encodeURIComponent(q));
    if (n !== seq) return;
    const total = GROUPS.reduce((a, [k]) => a + res[k].length, 0);
    document.getElementById('s-out').innerHTML = !q ? '<p class="mute">Type a word or two; every word must match.</p>'
      : `<p class="mute small">${total} results</p>` + list(GROUPS.filter(([k]) => res[k].length), ([k, title, fn]) =>
        `<h2>${title} <span class="mute small">${res[k].length}</span></h2><div class="grid">${list(res[k], r => {
          const [href, name, sub, text] = fn(r);
          return `<a class="card" href="${href}"><small>${esc(sub || '')}</small><b>${esc(name)}</b><span>${esc(trim(text, 100))}</span></a>`;
        })}</div>`);
  }
  input.addEventListener('input', run);
  input.focus();
  await run();
});

route('about', async () => {
  const s = await api('/stats');
  app().innerHTML = `<p class="kicker">About</p><h1>Tea &amp; Tisane Collection Explorer</h1>
    <p class="lead">A Python application for exploring teas, blends, cultivars, tisanes and tea companies from around the
    world. This web interface shows the same two SQLite databases as the desktop app: ${s.teas} tea varieties,
    ${s.blends} blends, ${s.cultivars} cultivars, ${s.companies} tea companies with ${s.products} products, ${s.regions}
    tea-growing regions, and ${s.tisanes} herbal tisanes with ${s.families} plant families, ${s.herb_regions} herb-growing
    regions, ${s.makers} herbal brands, ${s.safety_records} safety records and ${s.traditions} traditional systems.</p>
    ${isStatic() ? '<p class="callout">This is the static (GitHub Pages) version: everything is browsable and searchable, but the tea journal only works in the local app.</p>' : ''}
    <p class="callout a">Health and safety notes come from the database and are for information only, not medical advice.</p>
    <h2>Run the desktop app</h2>
    <pre>pip install -r requirements.txt
python main.py</pre>
    <p>A Tkinter app with tabs for teas, blends, cultivars, brands, tisanes, the tea journal, a brewing timer, tea
    comparison, a dashboard of Matplotlib charts, the varieties guide, tea history and a world map.</p>
    <h2>Run the web app</h2>
    <pre>pip install -r requirements-web.txt
python run_web.py        # http://127.0.0.1:8114</pre>
    <p>The local web app opens tea_collection.db and tisane_collection.db read-only and can add and delete
    tea-journal entries in tea_journal.json (the file the desktop app uses). <code>python scripts/build_static.py</code>
    exports the static site.</p>
    <h2>Credits</h2>
    <p>Teas, blends, cultivars, companies, tisanes and regions come from the repository's databases; the varieties guide,
    history, glossary and herbal reference are the repository's markdown files. World map land outlines: Natural Earth
    1:110m (public domain).</p>
    <p>Built with Python, Tkinter, SQLite and Matplotlib (desktop) and FastAPI with plain JavaScript (web), with AI
    assistance from <a href="https://claude.com/" target="_blank" rel="noopener">Claude (Anthropic)</a>.
    Released under the MIT licence. <a href="https://github.com/gddickinson/tea_explorer" target="_blank" rel="noopener">Source on GitHub</a>.</p>`;
});
