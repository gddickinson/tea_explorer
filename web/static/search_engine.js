// Search and filter rules for list pages: an exact mirror of web/search.py, used by static_api.js to answer
// /api/<kind>?... and /api/search?q=... on the static site from the exported full lists.
const S = (text, exact = {}, contains = {}, flag = {}, anyof = {}, id = 'id') => ({ text, exact, contains, flag, anyof, id });
export const SPECS = {
  teas: S(['name', 'category', 'origin', 'processing', 'flavor_profile', 'aroma', 'appearance', 'cultivars', 'history'],
    { category: 'category', country: 'country', caffeine: 'caffeine' }),
  blends: S(['blend_name', 'category', 'base_tea', 'ingredients', 'flavor_profile', 'aroma', 'popular_brands', 'description'],
    { category: 'category', caffeine: 'caffeine' }, {}, {}, {}, 'blend_id'),
  cultivars: S(['name', 'species', 'origin_country', 'leaf_size', 'characteristics', 'common_uses', 'notes'],
    { country: 'origin_country' }, { species: 'species' }),
  regions: S(['name', 'country', 'climate', 'famous_teas', 'description'], { country: 'country' }),
  companies: S(['company_name', 'parent_company', 'headquarters_city', 'country_of_origin', 'certifications', 'description'],
    { country: 'country', segment: 'market_segment' }, {}, {}, { cert: 'cert_terms' }, 'company_id'),
  products: S(['product_name', 'company_name', 'tea_type', 'tea_category', 'bag_type', 'format', 'special_features', 'countries_available'],
    { company: 'company_id', type: 'tea_type', category: 'tea_category', bag: 'bag_type', currency: 'price_currency' }, {},
    { organic: 'organic', fair_trade: 'fair_trade' }, {}, 'product_id'),
  tisanes: S(['name', 'scientific_name', 'plant_family', 'plant_part_used', 'origin_region', 'tradition', 'traditional_uses',
    'research_benefits', 'key_compounds', 'flavor_profile', 'aroma'],
  { family: 'plant_family' }, {}, { caffeine_free: 'caffeine_free' }, { tradition: 'tradition_terms' }),
  families: S(['family_name', 'characteristics', 'major_genera', 'common_uses', 'notes']),
  herb_regions: S(['name', 'country', 'climate_type', 'primary_herbs', 'key_producers', 'description'], { country: 'country' }),
  makers: S(['company_name', 'headquarters_city', 'headquarters_country', 'parent_company', 'certifications', 'market_segment',
    'notable_products', 'description'], { country: 'country' }, {}, {}, { cert: 'cert_terms' }),
  herb_products: S(['product_name', 'maker_name', 'tisane_type', 'format', 'certifications', 'special_features', 'countries_available'],
    { maker: 'manufacturer_id', type: 'tisane_type' }),
};
export const KINDS = Object.keys(SPECS);

// Python's str(): None -> 'None', True -> 'True', numbers as written. Only used for exact comparisons.
const pyStr = v => v === null || v === undefined ? 'None' : v === true ? 'True' : v === false ? 'False' : String(v);
const given = v => v !== undefined && v !== null && v !== '';

export function filterRows(kind, rows, params = {}) {
  const spec = SPECS[kind];
  const words = String(params.q || '').toLowerCase().split(/\s+/).filter(Boolean);
  return rows.filter(r => {
    for (const [p, col] of Object.entries(spec.exact)) if (given(params[p]) && pyStr(r[col]) !== String(params[p])) return false;
    for (const [p, col] of Object.entries(spec.contains))
      if (given(params[p]) && !String(r[col] || '').toLowerCase().includes(String(params[p]).toLowerCase())) return false;
    for (const [p, col] of Object.entries(spec.flag)) if (String(params[p] || '') === '1' && !r[col]) return false;
    for (const [p, col] of Object.entries(spec.anyof)) if (given(params[p]) && !(r[col] || []).includes(String(params[p]))) return false;
    if (words.length) {
      const text = spec.text.map(f => String(r[f] || '')).join(' ').toLowerCase();
      if (!words.every(w => text.includes(w))) return false;
    }
    return true;
  });
}
