// Auditoría UX pasada 2 (iframe). Uso: copiar a la raíz servida y en javascript_tool:
//   await import('/audit2.js'); R = await audit2(['/','/decidir/x/'], 375, 812)
// Devuelve por URL: scrollWidth, altura, CLS (buffered), LCP, y de primer input / resultado / bloques
// (Ejemplo resuelto, Casos típicos, FAQ, En las noticias), objetivos < 24 px (no inline), fallos de contraste AA
// (texto sobre el primer fondo opaco de sus ancestros; ignora degradados e imágenes) y tablas largas/anchas.
const parse = c => {
  let m = c.match(/^color\(srgb ([\d.]+) ([\d.]+) ([\d.]+)(?: \/ ([\d.]+))?\)/);
  let r, g, b, a = 1;
  if (m) { [r, g, b] = m.slice(1, 4).map(Number); if (m[4] !== undefined) a = +m[4]; }
  else { m = c.match(/[\d.]+/g); if (!m) return null; [r, g, b] = m.slice(0, 3).map(v => v / 255); if (m[3] !== undefined) a = +m[3]; }
  const f = v => v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4);
  return { L: .2126 * f(r) + .7152 * f(g) + .0722 * f(b), a };
};
export async function audit2(urls, W, H) {
  H = H || 812; const out = [];
  for (const u of urls) {
    const fr = document.createElement('iframe');
    fr.style.cssText = `position:fixed;left:0;top:0;width:${W}px;height:${H}px;border:0;opacity:0;pointer-events:none`;
    document.body.appendChild(fr); await new Promise(r => { fr.onload = r; fr.src = u; });
    const w = fr.contentWindow, d = fr.contentDocument; let cls = 0, lcp = null;
    try {
      new w.PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
      new w.PerformanceObserver(l => { const e = l.getEntries().pop(); lcp = { t: Math.round(e.startTime), el: e.element ? (e.element.tagName + '.' + e.element.className).slice(0, 30) : null, y: e.element ? Math.round(e.element.getBoundingClientRect().top) : null }; }).observe({ type: 'largest-contentful-paint', buffered: true });
    } catch (e) {}
    await new Promise(r => setTimeout(r, 1200));
    const vis = e => { const r = e.getBoundingClientRect(), s = w.getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility != 'hidden' && s.display != 'none'; };
    const Y = e => e ? Math.round(e.getBoundingClientRect().top + w.scrollY) : -1;
    const Hh = e => e ? Math.round(e.getBoundingClientRect().height) : -1;
    const taps = [...d.querySelectorAll('a,button,input,select,summary,[role=button]')].filter(vis);
    const small = taps.filter(e => { const r = e.getBoundingClientRect(); const inl = e.tagName == 'A' && w.getComputedStyle(e).display == 'inline' && e.closest('p,li,td,dd,figcaption,small'); return !inl && (r.height < 24 || r.width < 24); });
    const bgOf = e => { while (e && e.nodeType == 1) { const s = w.getComputedStyle(e); if (s.backgroundImage != 'none' && !/url/.test(s.backgroundImage)) return null; const l = parse(s.backgroundColor); if (l && l.a > .5) return l.L; e = e.parentElement; } return parse(w.getComputedStyle(d.documentElement).backgroundColor).L; };
    const fails = []; const tw = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT); let n, cnt = 0;
    while ((n = tw.nextNode()) && cnt < 3000) {
      const t = n.textContent.trim(); if (!t) continue; const e = n.parentElement; if (!vis(e) || e.closest('[aria-hidden=true],svg,.sr-only')) continue; cnt++;
      const s = w.getComputedStyle(e); if (/text/.test(s.backgroundClip || s.webkitBackgroundClip || '')) continue;
      const fg = parse(s.color); const b = bgOf(e); if (!fg || b == null || fg.a < .5) continue;
      const cr = (Math.max(fg.L, b) + .05) / (Math.min(fg.L, b) + .05);
      const fs = parseFloat(s.fontSize), big = fs >= 24 || (fs >= 18.66 && +s.fontWeight >= 700);
      if (cr < (big ? 3 : 4.5)) fails.push(t.slice(0, 22) + ':' + cr.toFixed(2) + ':' + e.tagName + '.' + String(e.className).slice(0, 18));
    }
    const q = s => d.querySelector(s);
    const hd = t => [...d.querySelectorAll('h2,h3')].find(h => h.textContent.includes(t));
    const sec = t => { const h = hd(t); return h ? (h.closest('section,aside') || h) : null; };
    const firstIn = [...d.querySelectorAll('form input:not([type=hidden]),form select')].find(vis);
    const verd = q('.result');
    const tbls = [...d.querySelectorAll('table')].filter(vis).map(t => { let p = t.parentElement, sc = false; while (p && p != d.body) { if (/auto|scroll/.test(w.getComputedStyle(p).overflowX)) { sc = true; break; } p = p.parentElement; } return { w: Math.round(t.scrollWidth), rows: t.rows.length, cols: t.rows[0] ? t.rows[0].cells.length : 0, sc, ov: t.scrollWidth > W, stickyHead: t.tHead ? w.getComputedStyle(t.tHead.rows[0].cells[0]).position : '-', y: Y(t) }; });
    out.push({
      u, W, sw: d.documentElement.scrollWidth, h: d.documentElement.scrollHeight, cls: +cls.toFixed(3), lcp,
      firstIn: Y(firstIn), res: Y(verd), resH: Hh(verd),
      ejemplo: [Y(sec('Ejemplo resuelto')), Hh(sec('Ejemplo resuelto'))], casos: [Y(sec('Casos típicos')), Hh(sec('Casos típicos'))],
      faq: [Y(sec('Preguntas frecuentes')), Hh(sec('Preguntas frecuentes'))], enNot: [Y(sec('En las noticias')), Hh(sec('En las noticias'))],
      ultimas: Y(hd('Últimas noticias')), empieza: Y(hd('Empieza por aquí')),
      small: small.length, smallEx: small.slice(0, 6).map(e => (e.textContent || e.getAttribute('aria-label') || e.tagName).trim().slice(0, 16) + ':' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height)),
      lt44: taps.filter(e => e.getBoundingClientRect().height < 44).length, taps: taps.length,
      cfail: fails.length, cEx: fails.slice(0, 5), nodes: cnt, tbls: tbls.filter(t => t.ov || t.rows > 10),
      dark: w.matchMedia('(prefers-color-scheme: dark)').matches,
    });
    fr.remove();
  }
  return out;
}
window.audit2 = audit2;
