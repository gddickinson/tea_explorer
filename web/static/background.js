// Subtle animated background: a few slow-rising wisps of steam in jade and amber. Skipped under prefers-reduced-motion.
export function background(canvas) {
  if (!canvas || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const ctx = canvas.getContext('2d');
  const wisps = Array.from({ length: 14 }, (_, i) => ({ x: Math.random(), y: Math.random(), s: 0.00015 + Math.random() * 0.0003, p: i }));
  const size = () => { canvas.width = innerWidth; canvas.height = innerHeight; };
  size();
  addEventListener('resize', size);
  const tick = t => {
    const { width: w, height: h } = canvas;
    ctx.clearRect(0, 0, w, h);
    for (const k of wisps) {
      k.y -= k.s; if (k.y < -0.1) { k.y = 1.1; k.x = Math.random(); }
      const x = k.x * w + Math.sin(t / 2400 + k.p) * 40, y = k.y * h;
      const g = ctx.createRadialGradient(x, y, 0, x, y, 140);
      g.addColorStop(0, k.p % 2 ? 'rgba(111,227,165,.09)' : 'rgba(245,181,68,.07)');
      g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(x - 140, y - 140, 280, 280);
    }
    if (!document.hidden) requestAnimationFrame(tick); else setTimeout(() => requestAnimationFrame(tick), 500);
  };
  requestAnimationFrame(tick);
}
