// node markdown.test.mjs: the renderer handles the constructs used in the repo's markdown files and never passes raw HTML.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { render, inline } from './markdown.js';

const { html, toc } = render('# Title\n\n## White Teas\n\n### Chinese White Teas\n- **Bai Mu Dan (White Peony)**\n  - Fuding\n- two\n  continued\n\n1. first\n2. second\n\n---\n\n## White Teas\n');
assert.match(html, /<h2 id="title">Title<\/h2>/);
assert.match(html, /<h3 id="white-teas">White Teas<\/h3>/);
assert.match(html, /<h3 id="white-teas-1">/, 'duplicate headings get unique ids');
assert.match(html, /<h4 id="chinese-white-teas">/);
assert.match(html, /<li><strong>Bai Mu Dan \(White Peony\)<\/strong><\/li><li>Fuding<\/li>/);
assert.match(html, /<li>two continued<\/li>/);
assert.match(html, /<ol><li>first<\/li><li>second<\/li><\/ol>/);
assert.match(html, /<hr>/);
assert.deepEqual(toc.map(t => t.level), [1, 2, 3, 2]);

// Pipe tables (tisanes.md) and glossary terms (tea_glossary.md).
const t = render('| Field | Data |\n|-------|------|\n| **Scientific Name** | *Matricaria chamomilla* L. |\n').html;
assert.equal(t, '<div class="scroll"><table><tr><th>Field</th><th>Data</th></tr><tr><td><strong>Scientific Name</strong></td><td><em>Matricaria chamomilla</em> L.</td></tr></table></div>');
assert.equal(render('**Oxidation**\nThe enzymatic browning of tea leaves.').html, '<p class="term"><strong>Oxidation</strong><br>The enzymatic browning of tea leaves.</p>');
assert.equal(render('**Bold** start of a\nnormal paragraph').html, '<p><strong>Bold</strong> start of a normal paragraph</p>');

// Safety: HTML in the source is escaped; only http(s) links become anchors.
assert.equal(inline('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;');
assert.equal(inline('[x](javascript:alert(1))'), '[x](javascript:alert(1))');
assert.match(inline('[RA](https://example.org)'), /<a href="https:\/\/example.org" target="_blank" rel="noopener">RA<\/a>/);
assert.equal(inline('2 * 3 * 4'), '2 * 3 * 4');

// The real files render without leftover markdown markers in headings, and tisanes.md's tables become tables.
for (const f of ['tea_varieties_list.md', 'tea_history.md', 'tea_glossary.md', 'tisanes.md']) {
  const r = render(readFileSync(new URL('../../' + f, import.meta.url), 'utf8'));
  assert.ok(r.toc.length > 5, f);
  assert.ok(!/<h\d[^>]*>#/.test(r.html), f);
  assert.ok(!/<p>\|/.test(r.html), f + ': no table rows left as paragraphs');
}
assert.ok((render(readFileSync(new URL('../../tisanes.md', import.meta.url), 'utf8')).html.match(/<table>/g) || []).length > 20);
console.log('markdown: all ok');
