// Auditoría UX por iframe (pegar en javascript_tool con la ventana a 375/1280 px). Devuelve una fila por URL.
async function uxAudit(urls, W, H) {
  W = W || innerWidth; H = H || 812;
  const out = [];
  for (const u of urls) {
    const f = document.createElement("iframe");
    f.style.cssText = `position:fixed;left:0;top:0;width:${W}px;height:${H}px;border:0;opacity:0;pointer-events:none`;
    document.body.appendChild(f);
    await new Promise(r => { f.onload = r; f.src = u; });
    await new Promise(r => setTimeout(r, 900));
    const d = f.contentDocument, w = f.contentWindow;
    const vis = e => { const r = e.getBoundingClientRect(); const s = w.getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility != "hidden" && s.display != "none"; };
    const taps = [...d.querySelectorAll("a,button,input,select,summary,[role=button]")].filter(vis);
    const small = taps.filter(e => { const r = e.getBoundingClientRect(); const inline = e.tagName == "A" && w.getComputedStyle(e).display == "inline" && e.closest("p,li,td"); return !inline && (r.height < 44 || r.width < 24); });
    const inputs = [...d.querySelectorAll("input:not([type=hidden]),select,textarea")];
    const nolabel = inputs.filter(i => !(i.labels && i.labels.length) && !i.getAttribute("aria-label") && !i.getAttribute("aria-labelledby"));
    const numIn = inputs.filter(i => i.type == "number" || /\d/.test(i.value || ""));
    const noIm = numIn.filter(i => i.tagName == "INPUT" && i.type == "text" && !i.inputMode);
    const firstIn = inputs.find(vis), res = d.querySelector("[aria-live],.result,#result,.em-result");
    const fy = e => e ? Math.round(e.getBoundingClientRect().top + w.scrollY) : -1;
    const res_ = performance.getEntriesByType("resource").filter(r => r.name.includes(location.host));
    const nav = w.performance.getEntriesByType("navigation")[0];
    const sub = w.performance.getEntriesByType("resource").filter(r => r.name.startsWith(location.origin));
    out.push({
      u: u.replace(location.origin, ""), sw: d.documentElement.scrollWidth, h: d.documentElement.scrollHeight,
      htmlKB: +((nav ? nav.transferSize || nav.encodedBodySize : 0) / 1024).toFixed(1), subKB: +(sub.reduce((a, r) => a + (r.encodedBodySize || 0), 0) / 1024).toFixed(1),
      taps: taps.length, small: small.length, smallEx: small.slice(0, 4).map(e => (e.textContent || e.name || e.id || e.tagName).trim().slice(0, 18) + ":" + Math.round(e.getBoundingClientRect().height)),
      inputs: inputs.length, nolabel: nolabel.length, numText_noInputmode: noIm.length, typeNumber: inputs.filter(i => i.type == "number").length,
      firstInputY: fy(firstIn), resultY: fy(res), h1: (d.querySelector("h1") || {}).textContent?.slice(0, 50),
      landmarks: ["header", "nav", "main", "footer"].filter(t => d.querySelector(t)).join(","), skip: !!d.querySelector("a[href='#main']"),
      imgNoDim: [...d.querySelectorAll("img")].filter(i => !i.getAttribute("width") || !i.getAttribute("height")).length,
      fontSizeMin: Math.min(...[...d.querySelectorAll("p,li,td,label,small,span")].filter(vis).slice(0, 400).map(e => parseFloat(w.getComputedStyle(e).fontSize))),
      tables: d.querySelectorAll("table").length, wideTables: [...d.querySelectorAll("table")].filter(t => t.scrollWidth > W).length,
    });
    f.remove();
  }
  return out;
}
