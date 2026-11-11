// Blends and flavoured teas (desktop Blends tab) and tea-plant cultivars (desktop Cultivars tab), with detail pages:
// a blend links to the companies that sell it, a cultivar to the teas made from it.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, words, or } from './ui.js';
import { mountTimer, parseSteepTime } from './timer.js';
import { teaCard } from './teas.js';

route('blends', async (_args, query) => {
  const f = (await api('/facets')).blends;
  await listPage({
    routeName: 'blends', kind: 'blends', kicker: 'Teas', title: 'Blends and flavoured teas', query,
    lead: 'Earl Grey to masala chai: base tea, ingredients, flavour, serving suggestions, popular brands and brewing for each blend.',
    placeholder: 'e.g. bergamot, chai, jasmine, rose',
    filters: [
      { id: 'category', label: 'Category', options: f.category },
      { id: 'caffeine', label: 'Caffeine', options: f.caffeine },
    ],
    card: b => `<a class="card" href="#/blend/${b.blend_id}"><small>${esc(b.category)}</small>
      <b>${esc(b.blend_name)}</b><span>${esc(trim(b.ingredients, 110))}</span>
      <div class="meta"><span>${b.brew_temp_c ? b.brew_temp_c + ' °C' : ''}</span><span>${esc(trim(b.steep_time, 32))}</span></div></a>`,
  });
});

route('blend', async ([id]) => {
  const b = await api('/blends/' + encodeURIComponent(id));
  const temp = b.brew_temp_c ? `${b.brew_temp_c} °C${b.brew_temp_f ? ` / ${b.brew_temp_f} °F` : ''}` : '—';
  app().innerHTML = `
    ${crumb('#/blends', 'Blends', b.category)}
    <h1>${esc(b.blend_name)}</h1>
    <p class="lead">${esc(b.description || '')}</p>
    <div class="side rev">
      <div>
        ${kv([['category', b.category], ['base tea', b.base_tea], ['water temperature', temp], ['steep time', b.steep_time],
          ['caffeine', b.caffeine_level], ['origin', b.origin_region], ['price range', b.price_range]])}
        <h3>Ingredients</h3><p>${tags(words(b.ingredients), 'b')}</p>
        <h3>Flavour profile</h3><p>${esc(or(b.flavor_profile))}</p>
        ${sections([['Aroma', b.aroma], ['Appearance', b.appearance]])}
      </div>
      <div id="timer"></div>
    </div>
    <div class="two">
      <div>${sections([['Serving suggestions', b.serving_suggestions], ['Health benefits', b.health_benefits]])}</div>
      <div>${sections([['History', b.history], ['Popular brands', b.popular_brands]])}
        ${b.companies.length ? `<p>${list(b.companies, c => `<a class="tag c" href="#/company/${c.id}">${esc(c.name)}</a>`)}</p>` : ''}</div>
    </div>
    <p><a class="btn alt" href="#/journal?tea=${encodeURIComponent(b.blend_name)}">Log a tasting</a></p>`;
  mountTimer(document.getElementById('timer'), parseSteepTime(b.steep_time), b.blend_name);
});

// --- cultivars -----------------------------------------------------------------------------------------------------
// Same choices as the desktop species filter, matched as a substring ("var. sinensis" finds both spellings in the data).
const SPECIES = [['var. sinensis', 'var. sinensis (China type)'], ['var. assamica', 'var. assamica (Assam type)'], ['Hybrid', 'Hybrid']];

route('cultivars', async (_args, query) => {
  const f = (await api('/facets')).cultivars;
  await listPage({
    routeName: 'cultivars', kind: 'cultivars', kicker: 'Teas', title: 'Tea cultivars', query,
    lead: 'The tea plants behind the leaf: Chinese small-leaf and Assam large-leaf varieties and clonal cultivars, with leaf size, characteristics and common uses.',
    placeholder: 'e.g. Yabukita, clonal, frost, oolong',
    filters: [
      { id: 'species', label: 'Species', options: SPECIES },
      { id: 'country', label: 'Origin', options: f.country },
    ],
    card: c => `<a class="card" href="#/cultivar/${c.id}"><small>${esc(c.species || '')} · ${esc(c.origin_country || '')}</small>
      <b>${esc(c.name)}</b><span>${esc(trim(c.characteristics, 120))}</span></a>`,
  });
});

route('cultivar', async ([id]) => {
  const c = await api('/cultivars/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/cultivars', 'Cultivars', c.species)}
    <h1>${esc(c.name)}</h1>
    <p class="lead">${esc(c.characteristics || '')}</p>
    ${kv([['species', c.species], ['origin', c.origin_country], ['leaf size', c.leaf_size]])}
    ${sections([['Common uses', c.common_uses], ['Notes', c.notes]])}
    <h2>Teas made from ${esc(c.name)}</h2>
    ${c.teas.length ? `<div class="grid">${list(c.teas, teaCard)}</div>`
      : '<p class="mute">No tea in the database names this cultivar.</p>'}`;
});
