// Tea journal: personal tasting notes, read and written only through the local Python server (the repo's
// JournalController, same tea_journal.json as the desktop Journal tab). On the static site the journal is not
// published, so the page explains that.
import { route, api, app, esc, list, isStatic, needsServer } from './core.js';

const stars = n => '★'.repeat(n) + '☆'.repeat(5 - n);

route('journal', async (_args, query) => {
  if (isStatic()) {
    app().innerHTML = `<p class="kicker">Brew</p><h1>Tea journal</h1>
      <p class="lead">Record teas you taste: a 1–5 star rating, brewing details and tasting notes.</p>
      ${needsServer('The tea journal')}
      <p class="mute">Journal entries are personal notes stored in tea_journal.json on your own computer; they are never
      published on this site. Use the desktop app or the local web app to add and read them.</p>`;
    return;
  }
  const { entries, names } = await api('/journal', { fresh: true });
  app().innerHTML = `<p class="kicker">Brew</p><h1>Tea journal</h1>
    <p class="lead">${entries.length} ${entries.length === 1 ? 'entry' : 'entries'} in tea_journal.json (shared with the desktop app; local only, never published).</p>
    <div class="side rev">
      <div id="entries">${entries.length ? list(entries, e => `<div class="panel entry">
          <small class="mute">${esc(e.date)}</small><b>${esc(e.tea_name)}</b> <span class="stars" aria-label="${e.rating} of 5 stars">${stars(e.rating || 0)}</span>
          ${e.brewing ? `<h3>Brewing</h3><pre>${esc(e.brewing)}</pre>` : ''}${e.notes ? `<h3>Tasting notes</h3><p>${esc(e.notes)}</p>` : ''}
          <button class="alt" type="button" data-del="${e.entry_id}" aria-label="Delete the entry for ${esc(e.tea_name)} from ${esc(e.date)}">Delete</button></div>`)
        : '<p class="mute">No entries yet. Add your first tasting.</p>'}</div>
      <form class="panel" id="jform">
        <h3>New entry</h3>
        <label for="j-tea">Tea, blend or tisane</label><input id="j-tea" list="j-list" required value="${esc(query.tea || '')}">
        <datalist id="j-list">${list(names, n => `<option value="${esc(n)}">`)}</datalist>
        <label for="j-rating">Rating</label><select id="j-rating">${[5, 4, 3, 2, 1].map(n => `<option value="${n}" ${n === 3 ? 'selected' : ''}>${stars(n)}</option>`).join('')}</select>
        <label for="j-brew">Brewing details</label><textarea id="j-brew">Temperature: \nSteep time: \nInfusion #: </textarea>
        <label for="j-notes">Tasting notes</label><textarea id="j-notes"></textarea>
        <button type="submit">Save</button><p id="j-msg" class="small" aria-live="polite"></p>
      </form>
    </div>`;
  const msg = document.getElementById('j-msg');
  const fail = err => { msg.className = 'small err'; msg.textContent = err.message; };
  document.getElementById('jform').addEventListener('submit', async e => {
    e.preventDefault();
    try {
      await api('/journal', { body: { tea_name: document.getElementById('j-tea').value, rating: +document.getElementById('j-rating').value,
        brewing: document.getElementById('j-brew').value, notes: document.getElementById('j-notes').value } });
      location.hash = '#/journal?saved=' + Date.now();
    } catch (err) { fail(err); }
  });
  document.getElementById('entries').addEventListener('click', async e => {
    const b = e.target.closest('button[data-del]');
    if (!b || !confirm('Delete this journal entry?')) return;
    try {
      await api('/journal/delete', { body: { entry_id: +b.dataset.del } });
      location.hash = '#/journal?deleted=' + Date.now();
    } catch (err) { fail(err); }
  });
});
