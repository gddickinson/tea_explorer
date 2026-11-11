// Tea companies and their products (desktop Brands tab): companies with country / segment / certification filters,
// company pages with products, distribution and the blends they are known for, and a filterable product table.
import { route, api, app, esc, list, tags } from './core.js';
import { listPage, kv, sections, crumb, trim, or } from './ui.js';

export const SEG = { 'mass-market': 'Mass-market', premium: 'Premium', specialty: 'Specialty', luxury: 'Luxury' };
const yes = b => (b ? 'yes' : 'no');
const price = p => (p.price != null ? `${p.price.toFixed(2)} ${esc(p.price_currency || '')}` : '—');
const flags = p => tags([p.organic && 'Organic', p.fair_trade && 'Fair Trade'].filter(Boolean), 'a');
export const site = url => (url ? `<a href="https://${esc(url.replace(/^https?:\/\//, ''))}" target="_blank" rel="noopener">${esc(url)}</a>` : '—');

route('companies', async (_args, query) => {
  const f = (await api('/facets')).companies;
  await listPage({
    routeName: 'companies', kind: 'companies', kicker: 'Brands', title: 'Tea companies', query,
    lead: 'Tea brands from supermarket staples to luxury tea houses: owners, headquarters, history, certifications and products.',
    placeholder: 'e.g. London, Royal Warrant, Darjeeling, B Corp',
    filters: [
      { id: 'country', label: 'Country', options: f.country },
      { id: 'segment', label: 'Market segment', options: f.segment, names: SEG },
      { id: 'cert', label: 'Certification', options: f.cert, min: 2 },
    ],
    card: c => `<a class="card" href="#/company/${c.company_id}"><small>${esc(c.headquarters_city || '')}${c.headquarters_city ? ', ' : ''}${esc(c.country_of_origin)}${c.founded_year ? ' · since ' + c.founded_year : ''}</small>
      <b>${esc(c.company_name)}</b><span>${esc(trim(c.description, 120))}</span>
      <div class="meta"><span class="seg-${esc(c.market_segment)}">${esc(SEG[c.market_segment] || c.market_segment || '')}</span><span>${esc(trim(c.parent_company, 36))}</span></div></a>`,
  });
});

export function productTable(rows, withCompany = false) {
  return `<div class="scroll"><table><tr><th>Product</th>${withCompany ? '<th>Company</th>' : ''}<th>Type</th><th>Category</th><th>Bag</th><th>Format</th><th>Price</th><th></th></tr>
    ${list(rows, p => `<tr class="click" data-href="#/product/${p.product_id}"><td><a href="#/product/${p.product_id}">${esc(p.product_name)}</a></td>
      ${withCompany ? `<td>${esc(p.company_name)}</td>` : ''}<td>${esc(or(p.tea_type))}</td><td>${esc(or(p.tea_category))}</td>
      <td>${esc(or(p.bag_type))}</td><td>${esc(or(p.format))}</td><td class="mono">${price(p)}</td><td>${flags(p)}</td></tr>`)}</table></div>`;
}

// Whole-row click on product tables.
document.addEventListener('click', e => {
  const tr = e.target.closest('tr[data-href]');
  if (tr && !e.target.closest('a')) location.hash = tr.dataset.href;
});

route('company', async ([id]) => {
  const c = await api('/companies/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/companies', 'Tea companies', c.country)}
    <h1>${esc(c.company_name)}</h1>
    <p class="lead">${esc(c.description || '')}</p>
    ${kv([['founded', c.founded_year], ['headquarters', [c.headquarters_city, c.country_of_origin].filter(Boolean).join(', ')],
      ['parent company', c.parent_company], ['market segment', SEG[c.market_segment] || c.market_segment], ['website', site(c.website), true]])}
    ${c.cert_terms.length ? `<h3>Certifications</h3><p>${tags(c.cert_terms, 'c')}</p>` : ''}
    <h2>Products (${c.products.length})</h2>
    ${c.products.length ? productTable(c.products) : '<p class="mute">No products listed for this company.</p>'}
    ${c.distribution.length ? `<h2>Where it is sold</h2><div class="scroll"><table><tr><th>Country</th><th>Channel</th><th>Retailers</th></tr>
      ${list(c.distribution, d => `<tr><td>${esc(d.country)}</td><td>${esc(or(d.distribution_type))}</td><td>${esc(or(d.retailers))}</td></tr>`)}</table></div>` : ''}
    ${c.blends.length ? `<h2>Blends it is known for</h2><p>${list(c.blends, b => `<a class="tag b" href="#/blend/${b.id}">${esc(b.name)}</a>`)}</p>
      <p class="small mute">Blends whose "popular brands" name this company.</p>` : ''}
    <p><a class="btn alt" href="#/companies?country=${encodeURIComponent(c.country)}">More companies in ${esc(c.country)}</a></p>`;
});

route('products', async (_args, query) => {
  const [f, companies] = await Promise.all([api('/facets'), api('/companies')]);
  const names = Object.fromEntries(companies.map(c => [c.company_id, c.company_name]));
  await listPage({
    routeName: 'products', kind: 'products', kicker: 'Brands', title: 'Tea products', query, grid: '',
    lead: 'Tea bags, pyramids and loose-leaf tins from the companies in the database, with type, bag style, size, price and certifications.',
    placeholder: 'e.g. English Breakfast, decaf, pyramid, Assam',
    filters: [
      { id: 'company', label: 'Company', options: f.products.company, names },
      { id: 'type', label: 'Tea type', options: f.products.type },
      { id: 'category', label: 'Category', options: f.products.category },
      { id: 'bag', label: 'Bag', options: f.products.bag },
      { id: 'currency', label: 'Currency', options: f.products.currency },
      { id: 'organic', label: 'Organic', checkbox: true },
      { id: 'fair_trade', label: 'Fair Trade', checkbox: true },
    ],
    render: rows => productTable(rows, true),
  });
});

route('product', async ([id]) => {
  const p = await api('/products/' + encodeURIComponent(id));
  app().innerHTML = `
    ${crumb('#/products', 'Products', p.company_name)}
    <h1>${esc(p.product_name)}</h1>
    <p class="lead">by <a href="#/company/${p.company_id}">${esc(p.company_name)}</a></p>
    ${kv([['tea type', p.tea_type], ['category', p.tea_category], ['bag', p.bag_type], ['format', p.format], ['quantity', p.quantity],
      ['price', price(p), true], ['organic', yes(p.organic)], ['Fair Trade', yes(p.fair_trade)]])}
    ${sections([['Special features', p.special_features], ['Available in', p.countries_available]])}`;
});
