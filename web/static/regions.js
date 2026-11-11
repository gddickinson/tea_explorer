// World map of tea-growing regions (tea_collection.db) and herb-growing regions (tisane_collection.db): inline SVG,
// equirectangular, Natural Earth 1:110m land outlines served by /api/world from world_shapes.py. Plus a searchable
// region list and a page per region with its teas or herbs.
import { route, api, app, esc, list } from './core.js';
import { listPage, kv, sections, crumb, trim } from './ui.js';
import { teaCard } from './teas.js';
import { tisaneCard } from './tisanes.js';
import { project } from './geo.js';

const W = 1000, H = 500;
const px = lon => project(lon, 0, W, H)[0];
const py = lat => project(0, lat, W, H)[1];
const ring = pts => 'M' + pts.map(([lo, la]) => `${px(lo).toFixed(1)},${py(la).toFixed(1)}`).join('L') + 'Z';
const ll = (lat, lon) => `${Math.abs(lat)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lon)}° ${lon >= 0 ? 'E' : 'W'}`;

function pins(items, cls, href, focus) {
  let s = '';
  for (const r of items) {
    if (r.latitude == null || r.longitude == null) continue;
    const x = px(r.longitude), y = py(r.latitude), on = focus === `${cls}${r.id}`;
    // The class sits on the <g> so markers keep their colours where the links are stripped (home page).
    s += `<a href="${href}${r.id}" aria-label="${esc(r.name)}, ${esc(r.country)}"><g class="${cls}${on ? ' on' : ''}">
      <circle cx="${x}" cy="${y}" r="${on ? 11 : 7}" class="halo"/><circle cx="${x}" cy="${y}" r="${on ? 6 : 4}" class="dot"/>
      <title>${esc(r.name)} (${esc(r.country)})</title></g></a>`;
  }
  return s;
}

// SVG map; markers link to region pages. layers: which marker sets to draw; focus: 'pin<id>' or 'hpin<id>'.
export function worldSvg(world, { layers = ['tea', 'herb'], focus = null, crop = null } = {}) {
  const view = crop ? crop.join(' ') : `0 0 ${W} ${H}`;
  let s = `<svg class="world" viewBox="${view}" role="img" aria-label="World map of tea- and herb-growing regions">`;
  for (const lat of [23.4, 0, -23.4]) s += `<line x1="0" x2="${W}" y1="${py(lat)}" y2="${py(lat)}" class="${lat ? 'tropic' : 'equator'}"/>`;
  // One path for all land; even-odd fill keeps holes (e.g. the Caspian Sea) open.
  s += `<path class="land" fill-rule="evenodd" d="${world.land.map(poly => poly.map(ring).join('')).join('')}"/>`;
  if (layers.includes('herb')) s += pins(world.herb_regions, 'hpin', '#/herbregion/', focus);
  if (layers.includes('tea')) s += pins(world.regions, 'pin', '#/region/', focus);
  return s + `<text x="${W - 8}" y="${py(23.4) - 6}" text-anchor="end" class="axisl">Tropic of Cancer</text>
    <text x="${W - 8}" y="${py(-23.4) + 16}" text-anchor="end" class="axisl">Tropic of Capricorn</text></svg>`;
}

const LEGEND = '<p class="legend"><span><i style="background:var(--accent)"></i>tea-growing region</span><span><i style="background:var(--accent3)"></i>herb-growing region</span></p>';

route('map', async (_args, query) => {
  const [world, f] = await Promise.all([api('/world'), api('/facets')]);
  const layers = (query.show || 'tea,herb').split(',');
  await listPage({
    routeName: 'map', kind: 'regions', kicker: 'Atlas', title: 'Tea- and herb-growing regions', query,
    lead: `${world.regions.length} tea-growing regions and ${world.herb_regions.length} regions known for herbal-tea plants, with elevation, climate and the teas or herbs each is famous for. Click a marker or a card.`,
    placeholder: 'e.g. Fujian, monsoon, oolong',
    extra: `<div class="panel"><label><input type="checkbox" id="m-tea" ${layers.includes('tea') ? 'checked' : ''}> Tea regions</label>
        <label><input type="checkbox" id="m-herb" ${layers.includes('herb') ? 'checked' : ''}> Herb regions</label></div>
      <div class="stage map" id="m-svg">${worldSvg(world, { layers })}</div>${LEGEND}
      <p class="small mute">Land outlines: Natural Earth 1:110m (public domain). Marker positions are the database coordinates.</p>
      <h2>Tea-growing regions</h2>`,
    filters: [{ id: 'country', label: 'Country', options: f.regions.country }],
    card: r => `<a class="card" href="#/region/${r.id}"><small>${esc(r.country)}${r.elevation_min != null ? ` · ${r.elevation_min}–${r.elevation_max} m` : ''}</small>
      <b>${esc(r.name)}</b><span>${esc(trim(r.famous_teas || r.description, 110))}</span></a>`,
  });
  const redraw = () => {
    const on = [['tea', 'm-tea'], ['herb', 'm-herb']].filter(([, id]) => document.getElementById(id).checked).map(([k]) => k);
    document.getElementById('m-svg').innerHTML = worldSvg(world, { layers: on });
  };
  ['m-tea', 'm-herb'].forEach(id => document.getElementById(id).addEventListener('change', redraw));
  const herbs = await api('/herb_regions');
  app().insertAdjacentHTML('beforeend', `<h2>Herb-growing regions</h2><div class="grid">${list(herbs, r =>
    `<a class="card" href="#/herbregion/${r.id}"><small>${esc(r.country)}</small><b>${esc(r.name)}</b><span>${esc(trim(r.primary_herbs, 110))}</span></a>`)}</div>`);
});

const cropAround = r => {
  const x = px(r.longitude), y = py(r.latitude);
  return [Math.max(0, Math.min(W - 400, x - 200)), Math.max(0, Math.min(H - 200, y - 100)), 400, 200];
};

route('region', async ([id]) => {
  const [r, world] = await Promise.all([api('/regions/' + encodeURIComponent(id)), api('/world')]);
  const { matched, country } = r.teas;
  app().innerHTML = `
    ${crumb('#/map', 'Regions', r.country)}
    <h1>${esc(r.name)}</h1>
    <p class="lead">${esc(r.description || '')}</p>
    <div class="two">
      <div>
        ${kv([['country', r.country], ['coordinates', ll(r.latitude, r.longitude)],
          ['elevation', r.elevation_min != null ? `${r.elevation_min}–${r.elevation_max} m` : undefined], ['climate', r.climate]])}
        ${sections([['Famous teas', r.famous_teas]])}
      </div>
      <div class="stage map">${worldSvg(world, { layers: ['tea'], focus: 'pin' + r.id, crop: cropAround(r) })}</div>
    </div>
    <h2>Teas from ${esc(r.name)}</h2>
    ${matched.length ? `<div class="grid">${list(matched, teaCard)}</div>`
      : '<p class="mute">No tea in the database names this region in its origin.</p>'}
    ${country.length ? `<h2>Other teas from ${esc(r.country)} (${country.length})</h2><div class="grid">${list(country, teaCard)}</div>` : ''}`;
});

route('herbregion', async ([id]) => {
  const [r, world] = await Promise.all([api('/herb_regions/' + encodeURIComponent(id)), api('/world')]);
  app().innerHTML = `
    ${crumb('#/map', 'Regions', r.country)}
    <h1>${esc(r.name)}</h1>
    <p class="lead">${esc(r.description || '')}</p>
    <div class="two">
      <div>
        ${kv([['country', r.country], ['coordinates', ll(r.latitude, r.longitude)], ['climate', r.climate_type],
          ['annual production', r.annual_production]])}
        ${sections([['Primary herbs', r.primary_herbs], ['Key producers', r.key_producers]])}
      </div>
      <div class="stage map">${worldSvg(world, { layers: ['herb'], focus: 'hpin' + r.id, crop: cropAround(r) })}</div>
    </div>
    <h2>Tisanes from this region</h2>
    ${r.tisanes.length ? `<div class="grid">${list(r.tisanes, tisaneCard)}</div>`
      : '<p class="mute">No tisane in the database matches this region\'s primary herbs.</p>'}`;
});
