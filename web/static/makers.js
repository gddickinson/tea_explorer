// Herbal tea brands (manufacturers in tisane_collection.db) and their products.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, or } from './ui.js';
import { site } from './brands.js';

route('makers', async (_args, query) => {
  const f = (await api('/facets')).makers;
  await listPage({
    routeName: 'makers', kind: 'makers', kicker: 'Herbal', title: 'Herbal tea brands', query,
    lead: 'Companies making herbal teas, from medicinal-herb specialists to supermarket brands: headquarters, certifications, notable products and their range.',
    placeholder: 'e.g. organic, Ayurvedic, sleep, Oregon',
    filters: [
      { id: 'country', label: 'Country', options: f.country },
      { id: 'cert', label: 'Certification', options: f.cert, min: 2 },
    ],
    card: m => `<a class="card" href="#/maker/${m.id}"><small>${esc(m.headquarters_city || '')}${m.headquarters_city ? ', ' : ''}${esc(m.headquarters_country || '')}${m.founded_year ? ' · since ' + m.founded_year : ''}</small>
      <b>${esc(m.company_name)}</b><span>${esc(trim(m.description, 120))}</span>
      <div class="meta"><span>${esc(trim(m.market_segment, 30))}</span></div></a>`,
  });
});

route('maker', async ([id]) => {
  const m = await api('/makers/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/makers', 'Herbal tea brands', m.country)}
    <h1>${esc(m.company_name)}</h1>
    <p class="lead">${esc(m.description || '')}</p>
    ${kv([['founded', m.founded_year], ['headquarters', [m.headquarters_city, m.headquarters_country].filter(Boolean).join(', ')],
      ['parent company', m.parent_company], ['market segment', m.market_segment], ['website', site(m.website), true]])}
    ${m.cert_terms.length ? `<h3>Certifications</h3><p>${tags(m.cert_terms, 'c')}</p>` : ''}
    ${sections([['Notable products', m.notable_products]])}
    <h2>Products in the database (${m.products.length})</h2>
    ${m.products.length ? `<div class="scroll"><table><tr><th>Product</th><th>Type</th><th>Format</th><th>Certifications</th><th>Price</th><th>Features</th></tr>
      ${list(m.products, p => `<tr><td>${esc(p.product_name)}</td><td>${esc(or(p.tisane_type))}</td><td>${esc(or(p.format))}</td>
        <td>${esc(or(p.certifications))}</td><td class="mono">${esc(or(p.price_range))}</td><td>${esc(or(p.special_features))}</td></tr>`)}</table></div>`
      : '<p class="mute">No individual products listed for this brand.</p>'}`;
});
