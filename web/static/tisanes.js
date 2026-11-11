// Herbal tisanes (desktop Tisanes tab): filterable list (plant family, tradition, caffeine-free), a page per tisane
// with every safety record, plant families, and the traditional medicine systems.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, words, or } from './ui.js';
import { mountTimer, parseSteepTime } from './timer.js';

export function tisaneCard(t) {
  return `<a class="card" href="#/tisane/${t.id}"><small><i>${esc(t.scientific_name || '')}</i> · ${esc(t.plant_family || '')}</small>
    <b>${esc(t.name)}</b><span>${esc(trim(t.traditional_uses, 110))}</span>
    <div class="meta"><span>${esc(trim(t.plant_part_used, 30))}</span><span>${t.caffeine_free ? 'caffeine-free' : esc(trim(t.caffeine_content, 30))}</span></div></a>`;
}

const LANG = { en: 'English', es: 'Spanish', fr: 'French', de: 'German', ar: 'Arabic', zh: 'Chinese', hi: 'Hindi', pt: 'Portuguese', it: 'Italian', ja: 'Japanese' };
const dict = (obj, names = {}) => list(Object.entries(obj || {}), ([k, v]) => `<div><b>${esc(v)}</b><span>${esc(names[k] || k.replace(/_/g, ' '))}</span></div>`);

route('tisanes', async (_args, query) => {
  const f = (await api('/facets')).tisanes;
  await listPage({
    routeName: 'tisanes', kind: 'tisanes', kicker: 'Herbal', title: 'Herbal tisanes', query,
    lead: 'Herbal infusions from Western herbalism, Traditional Chinese Medicine, Ayurveda and traditions worldwide: scientific names, traditional uses, research, key compounds, flavour and brewing. Read the safety notes before use.',
    placeholder: 'e.g. sleep, digestion, mint, rooibos',
    filters: [
      { id: 'family', label: 'Plant family', options: f.family },
      { id: 'tradition', label: 'Tradition', options: f.tradition, min: 3 },
      { id: 'caffeine_free', label: 'Caffeine-free', checkbox: true },
    ],
    extra: '<p><a class="btn alt" href="#/families">Plant families</a> <a class="btn alt" href="#/traditions">Traditions</a> <a class="btn alt" href="#/herbal">Herbal reference</a></p>',
    card: tisaneCard,
  });
});

const safetyPanel = s => `<div class="panel safety"><p class="risk">Risk level: ${esc(or(s.risk_level))}</p>
  ${kv([['pregnancy', s.pregnancy_safety], ['nursing', s.nursing_safety], ['children', s.child_safety], ['before surgery', s.pre_surgery_warning],
    ['maximum daily dose', s.max_daily_dosage], ['duration', s.duration_limits]])}
  ${sections([['Contraindications', s.contraindications], ['Drug interactions', s.drug_interactions], ['Adverse effects', s.adverse_effects],
    ['Evidence quality', s.evidence_quality]])}</div>`;

route('tisane', async ([id]) => {
  const t = await api('/tisanes/' + encodeURIComponent(id));
  const temp = t.brew_temp_c ? `${t.brew_temp_c} °C${t.brew_temp_f ? ` / ${t.brew_temp_f} °F` : ''}` : '—';
  const caffeine = `${t.caffeine_content || '—'}${t.caffeine_mg_per_cup ? ` (${t.caffeine_mg_per_cup} mg per cup)` : ''}`;
  app().innerHTML = `
    ${crumb('#/tisanes', 'Tisanes', t.plant_family)}
    <h1>${esc(t.name)}</h1>
    <p class="lead"><i>${esc(t.scientific_name || '')}</i>${t.family ? ` · <a href="#/family/${t.family.id}">${esc(t.plant_family)}</a>` : t.plant_family ? ' · ' + esc(t.plant_family) : ''}</p>
    <div class="side rev">
      <div>
        ${kv([['part used', t.plant_part_used], ['origin', t.origin_region], ['water temperature', temp], ['steep time', t.steep_time],
          ['herb : water', t.tea_water_ratio], ['caffeine', caffeine], ['price range', t.price_range], ['availability', t.availability]])}
        <h3>Flavour</h3><p>${tags(words(t.flavor_profile), 'a')}</p>
        ${sections([['Aroma', t.aroma], ['Dry appearance', t.appearance_dry], ['In the cup', t.appearance_brew]])}
      </div>
      <div id="timer"></div>
    </div>
    <div class="two">
      <div>
        <h3>Tradition</h3><p>${list(t.tradition_terms, x => `<a class="tag c" href="#/tisanes?tradition=${encodeURIComponent(x)}">${esc(x)}</a>`)}</p>
        ${sections([['Traditional uses', t.traditional_uses], ['Research', t.research_benefits], ['Key compounds', t.key_compounds],
          ['Cultural significance', t.cultural_significance], ['Grown in', t.cultivation_countries]])}
      </div>
      <div>
        ${Object.keys(t.common_names).length ? `<h3>Common names</h3><div class="kv">${dict(t.common_names, LANG)}</div>` : ''}
        ${Object.keys(t.tcm).length ? `<h3>Traditional Chinese Medicine</h3><div class="kv">${dict(t.tcm)}</div>` : ''}
        ${Object.keys(t.ayurvedic).length ? `<h3>Ayurveda</h3><div class="kv">${dict(t.ayurvedic)}</div>` : ''}
        ${t.herb_regions.length ? `<h3>Growing regions</h3><p>${list(t.herb_regions, r => `<a class="tag a" href="#/herbregion/${r.id}">${esc(r.name)} (${esc(r.country)})</a>`)}</p>` : ''}
        ${t.products.length ? `<h3>Products</h3><p>${list(t.products, p => `<a class="tag b" href="#/maker/${p.manufacturer_id}">${esc(p.product_name)} · ${esc(p.maker_name)}</a>`)}</p>` : ''}
      </div>
    </div>
    <h2>Safety</h2>
    ${t.safety.length ? (t.safety.length > 1 ? `<p class="small mute">The database holds ${t.safety.length} safety records for this herb; all are shown.</p>` : '') + list(t.safety, safetyPanel)
      : '<p class="mute">The database has no safety record for this herb. Ask a qualified practitioner before medicinal use, especially in pregnancy or with medication.</p>'}
    <p><a class="btn alt" href="#/journal?tea=${encodeURIComponent(t.name)}">Log a tasting</a></p>`;
  mountTimer(document.getElementById('timer'), parseSteepTime(t.steep_time), t.name);
});

// --- plant families ------------------------------------------------------------------------------------------------
route('families', async (_args, query) => {
  const f = (await api('/facets')).tisanes.family;
  await listPage({
    routeName: 'families', kind: 'families', kicker: 'Herbal', title: 'Plant families', query,
    lead: 'The botanical families behind herbal teas: the mints, daisies, roses, legumes and more, with their characteristics, major genera and uses.',
    placeholder: 'e.g. aromatic, mint, digestive',
    card: x => `<a class="card" href="#/family/${x.id}"><small>${f[x.family_name] ? f[x.family_name] + ' tisanes' : 'no tisanes listed'}</small>
      <b>${esc(x.family_name)}</b><span>${esc(trim(x.common_uses || x.characteristics, 110))}</span></a>`,
  });
});

route('family', async ([id]) => {
  const x = await api('/families/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/families', 'Plant families')}
    <h1>${esc(x.family_name)}</h1>
    <p class="lead">${esc(x.characteristics || '')}</p>
    ${sections([['Major genera', x.major_genera], ['Common uses', x.common_uses], ['Notes', x.notes]])}
    <h2>Tisanes in this family (${x.tisanes.length})</h2>
    ${x.tisanes.length ? `<div class="grid">${list(x.tisanes, tisaneCard)}</div>` : '<p class="mute">No tisane in the database belongs to this family.</p>'}`;
});

// --- traditional systems -------------------------------------------------------------------------------------------
route('traditions', async () => {
  const systems = await api('/traditions');
  app().innerHTML = `<p class="kicker">Herbal</p><h1>Traditional medicine systems</h1>
    <p class="lead">The healing traditions the tisanes come from: where and when they arose, their key texts and figures, and their principles.</p>
    ${list(systems, s => `<div class="panel"><h2>${esc(s.system_name)}</h2><p>${esc(s.description || '')}</p>
      ${kv([['origin', s.origin_region], ['period', s.time_period], ['key figures', s.key_figures], ['key texts', s.key_texts]])}
      ${sections([['Principles', s.principles]])}
      ${s.tisanes ? `<p><a class="btn alt" href="#/tisanes?tradition=${encodeURIComponent(s.system_name)}">${s.tisanes} tisanes from ${esc(s.system_name)}</a></p>` : ''}</div>`)}`;
});
