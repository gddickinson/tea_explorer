// node geo.test.mjs: the JS projection gives the same pixels as world_shapes.project() (values computed in Python on a
// 1000 x 500 map; tests/test_web.py checks the Python side and that every region marker falls on land).
import assert from 'node:assert/strict';
import { project } from './geo.js';

// Fujian Province, Darjeeling, Cederberg Region (rooibos), plus the corners and the origin.
const cases = [[118.0, 26.5, 827.7778, 176.3889], [88.3, 27.0, 745.2778, 175], [19.0, -32.1, 552.7778, 339.1667],
  [0, 0, 500, 250], [180, -90, 1000, 500], [-180, 90, 0, 0]];
for (const [lon, lat, x, y] of cases) {
  const [px, py] = project(lon, lat, 1000, 500);
  assert.ok(Math.abs(px - x) < 1e-3 && Math.abs(py - y) < 1e-3, `${lon},${lat} -> ${px},${py}`);
}
console.log('geo: all ok');
