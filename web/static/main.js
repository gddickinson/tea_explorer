// Entry point: registers the page modules (loaded on first visit), sets the mode line, draws the background, starts
// the router.
import { start, route, lazy, app, $, isStatic } from './core.js';
import { background } from './background.js';

const PAGES = {
  'home.js': ['home', 'search', 'about'], 'teas.js': ['teas', 'tea', 'compare'], 'blends.js': ['blends', 'blend', 'cultivars', 'cultivar'],
  'brands.js': ['companies', 'company', 'products', 'product'], 'tisanes.js': ['tisanes', 'tisane', 'families', 'family', 'traditions'],
  'makers.js': ['makers', 'maker'], 'regions.js': ['map', 'region', 'herbregion'], 'brewing.js': ['timer'],
  'dashboard.js': ['dashboard'], 'guide.js': ['guide', 'history', 'glossary', 'herbal'], 'journal.js': ['journal'],
};
lazy(Object.fromEntries(Object.entries(PAGES).flatMap(([file, names]) => names.map(n => [n, () => import('./' + file)]))));

route('notfound', () => { app().innerHTML = '<h1>Not found</h1><p><a href="#/">Back to the start</a></p>'; });

$('#mode').textContent = isStatic() ? 'static site (journal needs the local app)' : 'local app';
background($('#bg'));
start();
