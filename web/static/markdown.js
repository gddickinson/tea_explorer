// Tiny, safe Markdown renderer for the guide, history, glossary and herbal reference (tea_varieties_list.md,
// tea_history.md, tea_glossary.md, tisanes.md): headings (#..####), paragraphs, bullet and numbered lists, pipe tables,
// horizontal rules, **bold**, *italic*, `code` and [links](http...). A paragraph that starts with a bold-only line (the
// glossary's "**Term**" + definition) keeps its line break. All text is HTML-escaped first, so no raw HTML from the
// source reaches the page. Headings get ids for the table of contents.
const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
const escape = s => String(s).replace(/[&<>"']/g, c => ESC[c]);

export function slug(text) {
  return text.toLowerCase().replace(/<[^>]+>/g, '').replace(/&[a-z#0-9]+;/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

export function inline(text) {
  return escape(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?!\w)/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
}

// Returns { html, toc: [{level, text, id}] }.
export function render(md) {
  const out = [], toc = [], used = new Map();
  let para = [], list = null, table = null;
  const flushPara = () => {
    if (!para.length) return;
    const term = para.length > 1 && /^\*\*[^*]+\*\*$/.test(para[0]);
    out.push(term ? `<p class="term">${inline(para[0])}<br>${inline(para.slice(1).join(' '))}</p>` : `<p>${inline(para.join(' '))}</p>`);
    para = [];
  };
  const cells = line => line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
  const flushTable = () => {
    if (!table) return;
    const [head, ...body] = table.filter(r => !r.every(c => /^:?-{2,}:?$/.test(c)));
    out.push(`<div class="scroll"><table><tr>${head.map(c => `<th>${inline(c)}</th>`).join('')}</tr>`
      + body.map(r => `<tr>${r.map(c => `<td>${inline(c)}</td>`).join('')}</tr>`).join('') + '</table></div>');
    table = null;
  };
  const flushList = () => { if (list) { out.push(`<${list.tag}>${list.items.map(i => `<li>${inline(i)}</li>`).join('')}</${list.tag}>`); list = null; } };
  for (const raw of String(md).replace(/\r\n?/g, '\n').split('\n')) {
    const line = raw.trimEnd();
    let m;
    if (!line.trim()) { flushPara(); flushList(); flushTable(); continue; }
    if (/^\s*\|.*\|\s*$/.test(line)) { flushPara(); flushList(); (table = table || []).push(cells(line)); continue; }
    flushTable();
    if ((m = line.match(/^(#{1,4})\s+(.*)$/))) {
      flushPara(); flushList();
      const level = m[1].length, text = m[2].trim();
      let id = slug(text) || 'section';
      const n = used.get(id) || 0; used.set(id, n + 1);
      if (n) id += '-' + n;
      toc.push({ level, text, id });
      out.push(`<h${level + 1} id="${id}">${inline(text)}</h${level + 1}>`);
    } else if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flushPara(); flushList(); out.push('<hr>');
    } else if ((m = line.match(/^\s*[-*+]\s+(.*)$/)) || (m = line.match(/^\s*\d+[.)]\s+(.*)$/))) {
      flushPara();
      const tag = /^\s*\d/.test(line) ? 'ol' : 'ul';
      if (!list || list.tag !== tag) { flushList(); list = { tag, items: [] }; }
      list.items.push(m[1]);
    } else if (list && /^\s{2,}\S/.test(raw)) {
      list.items[list.items.length - 1] += ' ' + line.trim();
    } else {
      flushList(); para.push(line.trim());
    }
  }
  flushPara(); flushList(); flushTable();
  return { html: out.join('\n'), toc };
}
