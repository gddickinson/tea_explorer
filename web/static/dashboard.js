// Collection dashboard (desktop Dashboard tab): category, origin and caffeine distributions of the teas, products,
// companies and tisanes as bar charts. The journal-rating chart needs the journal, so it appears only in the local app.
import { route, api, app, esc, list, isStatic } from './core.js';

// Horizontal bar chart from [[label, count], ...]; href(label) makes the labels links (optional).
export function bars(rows, { href = null, cls = '', unit = '' } = {}) {
  const max = Math.max(1, ...rows.map(r => r[1]));
  return `<div class="bars chart ${cls}">${list(rows, ([label, n]) => {
    const name = href ? `<a href="${href(label)}">${esc(label)}${unit}</a>` : `<span class="l">${esc(label)}${unit}</span>`;
    return `${name}<div class="bar" aria-hidden="true" style="width:${(100 * n / max).toFixed(1)}%"></div><span class="n">${n}</span>`;
  })}</div>`;
}

const q = (route, key) => label => `#/${route}?${key}=${encodeURIComponent(label)}`;

route('dashboard', async () => {
  const [d, s] = await Promise.all([api('/dashboard'), api('/stats')]);
  app().innerHTML = `<p class="kicker">Teas</p><h1>Collection dashboard</h1>
    <p class="lead">${s.teas} teas from ${s.tea_countries} countries, ${s.blends} blends, ${s.products} products from ${s.companies} companies and
    ${s.tisanes} tisanes. Click a bar label to open the matching list.</p>
    <div class="two">
      <div class="panel"><h3>Teas by category</h3>${bars(d.tea_categories, { href: q('teas', 'category') })}</div>
      <div class="panel"><h3>Teas by country (top 12)</h3>${bars(d.tea_countries, { href: q('teas', 'country'), cls: 'b' })}</div>
      <div class="panel"><h3>Teas by caffeine level</h3>${bars(d.tea_caffeine, { href: q('teas', 'caffeine'), cls: 'c' })}</div>
      <div class="panel"><h3>Brewing temperature of the teas</h3>${bars(d.tea_temps, { unit: ' °C' })}</div>
      <div class="panel"><h3>Products by tea type</h3>${bars(d.product_types, { href: q('products', 'type'), cls: 'b' })}</div>
      <div class="panel"><h3>Companies by market segment</h3>${bars(d.company_segments, { href: q('companies', 'segment'), cls: 'c' })}</div>
      <div class="panel"><h3>Companies by country (top 10)</h3>${bars(d.company_countries, { href: q('companies', 'country') })}</div>
      <div class="panel"><h3>Tisanes by plant family (top 12)</h3>${bars(d.tisane_families, { href: q('tisanes', 'family'), cls: 'b' })}</div>
      <div class="panel"><h3>Tisanes by tradition (top 10)</h3>${bars(d.tisane_traditions, { href: q('tisanes', 'tradition'), cls: 'c' })}</div>
      <div class="panel"><h3>Tisanes by caffeine</h3>${bars(d.caffeine_free)}
        <h3>Plant part used (top 10)</h3>${bars(d.tisane_parts, { cls: 'b' })}</div>
    </div>
    <div class="panel" id="ratings"><h3>Journal ratings</h3>${isStatic()
      ? '<p class="small mute">Journal ratings come from your own tea_journal.json, so this chart is only in the local app.</p>'
      : '<p class="mute">Loading...</p>'}</div>`;
  if (isStatic()) return;
  const { entries } = await api('/journal', { fresh: true });
  const counts = [5, 4, 3, 2, 1].map(n => [`${'★'.repeat(n)}`, entries.filter(e => e.rating === n).length]);
  document.getElementById('ratings').innerHTML = `<h3>Journal ratings (${entries.length} entries)</h3>`
    + (entries.length ? bars(counts) : '<p class="mute">No journal entries yet.</p>');
});
