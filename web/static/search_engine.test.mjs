// node search_engine.test.mjs: the JS filters give the same ids as web/search.py on rows from the real databases.
// Expected ids come from tests/fixtures/search_cases.json, written by scripts/make_search_fixture.py with the Python
// code (tests/test_web.py checks the fixture is current and also compares both on the full data).
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { filterRows, SPECS } from './search_engine.js';
import { parseSteepTime } from './timer.js';

const fx = JSON.parse(readFileSync(new URL('../../tests/fixtures/search_cases.json', import.meta.url), 'utf8'));
let nonEmpty = 0;
for (const { kind, params, ids } of fx.cases) {
  assert.deepEqual(filterRows(kind, fx.rows[kind], params).map(r => r[SPECS[kind].id]), ids, `${kind} ${JSON.stringify(params)}`);
  nonEmpty += ids.length > 0;
}
assert.ok(nonEmpty >= 20, 'most cases exercise a non-empty result');
assert.deepEqual(Object.keys(SPECS).sort(), Object.keys(fx.rows).sort(), 'same kinds as web/search.py');

// Steep-time presets for the timer (texts as they appear in the databases).
const steeps = [['3-4 minutes', 180], ['2-3 minutes', 120], ['10-15 seconds gongfu', 10], ['10-20 seconds (Gongfu)', 10],
  ['30 seconds to 1 minute (Gongfu)', 30], ['1-1.5 minutes', 60], ['45 seconds to 1 minute', 45], ['1 minute', 60],
  ['2-2.5 minutes (first infusion), 10-20 seconds (later)', 120], ['5-10 minutes (crush pods first)', 300],
  ['Boil 5-10 min, steep 20-30 min (requires decoction)', 300], ['Simmer 10-15 minutes', 600], ['30 minutes', 1800],
  ['4-8 hours (cold infusion) or 10-15 min hot', null], ['2-3 hours (long decoction) or powder in hot water', null],
  ['Not applicable (whisked, not steeped)', null], ['Continuous infusion in gourd (not boiling water)', null], ['', null], [null, null]];
for (const [text, secs] of steeps) assert.equal(parseSteepTime(text), secs, String(text));
console.log('search_engine: all ok');
