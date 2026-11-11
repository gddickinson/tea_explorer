// Brewing timer page: the desktop Timer tab's presets (brewing_presets.py, via /api/timer), manual minutes and seconds,
// or the steep time of any tea, blend or tisane in the databases.
import { route, api, app, esc, list } from './core.js';
import { mountTimer, parseSteepTime } from './timer.js';

const GROUPS = [['teas', 'Teas'], ['blends', 'Blends'], ['tisanes', 'Tisanes']];

route('timer', async (_args, query) => {
  const t = await api('/timer');
  const opt = (kind, r) => `<option value="${kind}:${r.id}">${esc(r.name)} (${esc(r.steep_time || '—')})</option>`;
  app().innerHTML = `<p class="kicker">Brew</p><h1>Brewing timer</h1>
    <p class="lead">Pick a preset, set minutes and seconds yourself, or load the steep time of any tea, blend or tisane.</p>
    <div class="side rev">
      <div>
        <h3>Presets</h3><div class="presets">${list(t.presets, (p, i) => `<button class="alt" type="button" data-p="${i}">${esc(p.label)}</button>`)}</div>
        <label for="t-pick">From the collection</label><select id="t-pick"><option value="">Custom</option>
          ${list(GROUPS, ([k, label]) => `<optgroup label="${label}">${list(t[k], r => opt(k, r))}</optgroup>`)}</select>
        <p class="small mute" id="t-note">Ranges such as "3-4 minutes" start at the lower bound; gongfu times are for the first infusion.</p>
      </div>
      <div id="timer"></div>
    </div>`;
  const host = document.getElementById('timer');
  const note = document.getElementById('t-note');
  const load = (secs, label, extra = '') => { mountTimer(host, secs, label); note.textContent = extra; };
  mountTimer(host);
  app().querySelector('.presets').addEventListener('click', e => {
    const b = e.target.closest('button[data-p]');
    if (!b) return;
    const p = t.presets[+b.dataset.p];
    document.getElementById('t-pick').value = '';
    load(p.seconds, p.name);
  });
  const pick = value => {
    const [kind, id] = value.split(':');
    const r = (t[kind] || []).find(x => String(x.id) === id);
    if (!r) { load(null, ''); return; }
    const secs = parseSteepTime(r.steep_time);
    load(secs, r.name, `${r.temp_c ? `Water: ${r.temp_c} °C. ` : ''}Steep time in the database: "${r.steep_time || '—'}"${secs === null ? ' (not a countdown; set the timer yourself)' : ''}.`);
  };
  const sel = document.getElementById('t-pick');
  sel.addEventListener('change', e => pick(e.target.value));
  if (query.pick) { sel.value = query.pick; pick(query.pick); }
});
