// Tea varieties: filterable list (the desktop Tea Browser), a detail page per tea with its brewing timer, regions,
// cultivars and similar teas (the repo's RecommendationEngine), and a side-by-side comparison of up to 3 teas.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, words, or } from './ui.js';
import { mountTimer, parseSteepTime } from './timer.js';

const temp = r => (r.brew_temp_c ? `${r.brew_temp_c} °C${r.brew_temp_f ? ` / ${r.brew_temp_f} °F` : ''}` : '—');
const BANDS = ['Very Low', 'Low', 'Low-Medium', 'Medium', 'Medium-High', 'High'];

export function teaCard(t) {
  return `<a class="card" href="#/tea/${t.id}"><small>${esc(t.category)} · ${esc(t.country || t.origin || '')}</small>
    <b>${esc(t.name)}</b><span>${esc(trim(t.flavor_profile, 110))}</span>
    <div class="meta"><span>${t.brew_temp_c ? t.brew_temp_c + ' °C' : ''}</span><span>${esc(trim(t.steep_time, 32))}</span></div></a>`;
}
export const miniCard = (href, small, name) => `<a class="card" href="${href}"><small>${esc(small || '')}</small><b>${esc(name)}</b></a>`;

route('teas', async (_args, query) => {
  const f = (await api('/facets')).teas;
  const bands = BANDS.filter(b => f.caffeine[b]).map(b => [b, `${b} (${f.caffeine[b]})`]);
  await listPage({
    routeName: 'teas', kind: 'teas', kicker: 'Camellia sinensis', title: 'Tea varieties', query,
    lead: 'White, green, yellow, oolong, black and pu-erh teas: origin, processing, flavour, brewing parameters, caffeine, health benefits and history. Search by name, origin, flavour or cultivar.',
    placeholder: 'e.g. Darjeeling, smoky, Gyokuro, honey',
    filters: [
      { id: 'category', label: 'Category', options: f.category },
      { id: 'country', label: 'Country', options: f.country },
      { id: 'caffeine', label: 'Caffeine', options: bands },
    ],
    extra: '<p><a class="btn alt" href="#/compare">Compare teas</a> <a class="btn alt" href="#/dashboard">Collection dashboard</a></p>',
    card: teaCard,
  });
});

route('tea', async ([id]) => {
  const t = await api('/teas/' + encodeURIComponent(id));
  const regs = [...t.regions.matched, ...t.regions.country];
  app().innerHTML = `
    ${crumb('#/teas', 'Tea varieties', t.category)}
    <h1>${esc(t.name)}</h1>
    <p class="lead">${esc(t.origin || '')}</p>
    <div class="side rev">
      <div>
        ${kv([['category', t.category], ['oxidation', t.oxidation], ['water temperature', temp(t)], ['steep time', t.steep_time],
          ['leaf : water', t.tea_water_ratio], ['infusions', t.reinfusions], ['caffeine', t.caffeine_level], ['price range', t.price_range]])}
        <h3>Flavour profile</h3><p>${tags(words(t.flavor_profile), 'a')}</p>
        ${sections([['Aroma', t.aroma], ['Appearance', t.appearance], ['Processing', t.processing]])}
      </div>
      <div id="timer"></div>
    </div>
    <div class="two">
      <div>${sections([['Health benefits', t.health_benefits], ['History', t.history]])}</div>
      <div>
        <h3>Cultivars</h3><p>${esc(or(t.cultivars))}</p>
        ${t.cultivar_links.length ? `<p>${list(t.cultivar_links, c => `<a class="tag c" href="#/cultivar/${c.id}">${esc(c.name)}</a>`)}</p>` : ''}
        ${regs.length ? `<h3>Growing regions in ${esc(t.country)}</h3>
          <p>${list(t.regions.matched, r => `<a class="tag a" href="#/region/${r.id}">${esc(r.name)}</a>`)}${list(t.regions.country, r => `<a class="tag" href="#/region/${r.id}">${esc(r.name)}</a>`)}</p>
          ${t.regions.matched.length ? '<p class="small mute">Highlighted: regions named in this tea\'s origin or listing it among their famous teas.</p>' : ''}` : ''}
      </div>
    </div>
    ${t.similar.length ? `<h2>Similar teas</h2>
      <p class="small mute">Scored by the desktop app's recommendation engine: same category, origin, caffeine level and processing, and shared flavour words.</p>
      <div class="grid">${list(t.similar, s => miniCard(`#/tea/${s.id}`, `${s.category} · ${s.country}`, s.name))}</div>` : ''}
    <p><a class="btn alt" href="#/compare?ids=${t.id}">Compare with…</a>
    <a class="btn alt" href="#/teas?category=${encodeURIComponent(t.category)}">More ${esc(t.category)} teas</a>
    <a class="btn alt" href="#/journal?tea=${encodeURIComponent(t.name)}">Log a tasting</a></p>`;
  const preset = parseSteepTime(t.steep_time);
  mountTimer(document.getElementById('timer'), preset, t.name);
  if (preset === null) {
    document.getElementById('timer').insertAdjacentHTML('beforeend',
      `<p class="small mute">Steep time "${esc(t.steep_time)}" is not a countdown; set the timer yourself.</p>`);
  }
});

// --- comparison (desktop "Compare" tab: up to 3 teas side by side) -------------------------------------------------
const ROWS = [['Category', t => t.category], ['Origin', t => t.origin], ['Caffeine', t => t.caffeine_level],
  ['Steep time', t => t.steep_time], ['Temperature', temp], ['Leaf : water', t => t.tea_water_ratio],
  ['Infusions', t => t.reinfusions], ['Oxidation', t => t.oxidation], ['Flavour', t => t.flavor_profile],
  ['Aroma', t => t.aroma], ['Price range', t => t.price_range]];

route('compare', async (_args, query) => {
  const teas = await api('/teas');
  const picked = String(query.ids || '').split(',').filter(Boolean).slice(0, 3);
  const select = (i, cur) => `<div><label for="c-${i}">Tea ${i + 1}</label><select id="c-${i}"><option value="">—</option>
    ${list(teas, t => `<option value="${t.id}" ${String(t.id) === cur ? 'selected' : ''}>${esc(t.name)}</option>`)}</select></div>`;
  app().innerHTML = `<p class="kicker">Teas</p><h1>Compare teas</h1>
    <p class="lead">Pick up to three teas to compare category, origin, caffeine, steep time, temperature and flavour side by side.</p>
    <div class="three panel">${[0, 1, 2].map(i => select(i, picked[i] || '')).join('')}</div>
    <div id="cmp" aria-live="polite"></div>`;
  async function show() {
    const ids = [0, 1, 2].map(i => document.getElementById('c-' + i).value).filter(Boolean);
    history.replaceState(null, '', '#/compare' + (ids.length ? '?ids=' + ids.join(',') : ''));
    const rows = await Promise.all(ids.map(id => api('/teas/' + id)));
    document.getElementById('cmp').innerHTML = !rows.length ? '<p class="mute">Choose a tea above.</p>'
      : `<div class="scroll"><table class="cmp"><tr><th></th>${list(rows, t => `<th><a href="#/tea/${t.id}">${esc(t.name)}</a></th>`)}</tr>
        ${list(ROWS, ([label, fn]) => `<tr><th>${label}</th>${list(rows, t => `<td>${esc(or(fn(t)))}</td>`)}</tr>`)}</table></div>`;
  }
  [0, 1, 2].forEach(i => document.getElementById('c-' + i).addEventListener('change', show));
  await show();
});
