// Hipoteca bonificada (con vinculaciones) o sin vinculaciones. Amortizacion francesa a plazo x 12 cuotas.
// Bonificada: tipo = TIN. Sin vinculaciones: tipo = TIN + bonif (puntos). Coste a H anos = intereses efectivos (cuotas pagadas + capital pendiente - capital inicial)
// + comision de apertura (% del capital) + coste anual de las vinculaciones x H (solo la bonificada).
function saldo(P, i, n, m) {
  if (i === 0) return P - P / n * m;
  var c = P * i / (1 - Math.pow(1 + i, -n)), g = Math.pow(1 + i, m);
  return P * g - c * (g - 1) / i;
}
function cuota(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
function opcion(P, plazo, H, tinPct, apertura, vinc) {
  var n = plazo * 12, m = H * 12, i = tinPct / 1200, c = cuota(P, i, n);
  var inter = c * m + saldo(P, i, n, m) - P, com = P * apertura / 100, vv = vinc * H;
  return { cuota: c, intereses: inter, comision: com, vinc: vv, coste: inter + com + vv };
}
function calcular(d) {
  var plazo = Math.max(Math.round(d.plazo), 1), H = Math.min(Math.max(Math.round(d.horizonte), 1), plazo);
  var b = opcion(d.capital, plazo, H, d.tin, d.aperturaBon, d.vinc), s = opcion(d.capital, plazo, H, d.tin + d.bonif, d.aperturaSin, 0);
  function f(x) { return opcion(d.capital, plazo, H, d.tin + x, d.aperturaSin, 0).coste - b.coste; }
  var bm, lo = 0, hi = 10, k;
  if (f(0) >= 0) bm = 0; else if (f(hi) < 0) bm = -1;
  else { for (k = 0; k < 100; k++) { var mid = (lo + hi) / 2; if (f(mid) < 0) lo = mid; else hi = mid; } bm = (lo + hi) / 2; }
  var dif = s.coste - b.coste;
  var vincMax = Math.max((s.coste - b.intereses - b.comision) / H, 0);
  return {
    H: H, cuotaBon: b.cuota, cuotaSin: s.cuota, interesesBon: b.intereses, interesesSin: s.intereses,
    comisionBon: b.comision, comisionSin: s.comision, vincTotal: b.vinc, costeBon: b.coste, costeSin: s.coste,
    diferencia: dif, ahorroIntereses: s.intereses - b.intereses, ahorroCuotaMes: s.cuota - b.cuota, bonifMin: bm, vincMax: vincMax,
    mejor: dif > 1 ? 0 : (dif < -1 ? 1 : 2)
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["capital", "plazo", "tin", "bonif", "vinc", "aperturaBon", "aperturaSin", "horizonte"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pts(x) { return EM.num(x, 2) + " puntos"; }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.capital <= 0 || d.plazo < 1 || d.horizonte < 1) { aviso("Escribe un capital mayor que 0, al menos 1 año de plazo y 1 de horizonte.", "Sin capital, plazo u horizonte no hay hipoteca que comparar."); return; }
  if (d.plazo > 40 || d.tin > 15 || d.bonif > 5 || d.aperturaBon > 5 || d.aperturaSin > 5) { aviso("Revisa los límites: plazo de hasta 40 años, TIN de hasta el 15 %, bonificación de hasta 5 puntos y comisión de apertura de hasta el 5 %.", "Fuera de esos valores el resultado no sería realista."); return; }
  var r = calcular(d), H = r.H, anos = EM.num(H, 0) + (H === 1 ? " año" : " años"), w, v, bm = r.bonifMin;
  var umbral = bm < 0 ? "más de 10 puntos (ninguna bonificación realista lo cubre)" : (bm === 0 ? "0 puntos (con estas vinculaciones y comisiones la bonificada ya compensa sin rebaja)" : pts(bm));
  if (r.mejor === 0) {
    w = "bonificada";
    v = "Con estos datos, la hipoteca bonificada sale " + eur(r.diferencia) + " más barata en " + anos + " que la de sin vinculaciones: ahorras " + eur(r.ahorroIntereses) + " de intereses y las vinculaciones suman " + eur(r.vincTotal) + ". Compensa mientras la bonificación sea de al menos " + umbral + " o las vinculaciones cuesten menos de " + eur(r.vincMax) + " al año.";
  } else if (r.mejor === 1) {
    w = "sin";
    v = "Con estos datos, la hipoteca sin vinculaciones sale " + eur(-r.diferencia) + " más barata en " + anos + ": la bonificación de " + pts(d.bonif) + " ahorra " + eur(r.ahorroIntereses) + " de intereses, pero las vinculaciones suman " + eur(r.vincTotal) + (r.comisionBon > r.comisionSin ? " y la comisión de apertura es mayor" : "") + ". La bonificada solo compensaría con una bonificación de " + umbral + " o con vinculaciones por debajo de " + eur(r.vincMax) + " al año.";
  } else {
    w = "empate";
    v = "Con estos datos, las dos hipotecas cuestan lo mismo en " + anos + " (unos " + eur(r.costeBon) + "): la bonificación compensa justo el coste de las vinculaciones y las comisiones.";
  }
  var note = "<p><strong>Lectura:</strong> la cuota mensual es " + eur(r.cuotaBon, 2) + " con bonificación y " + eur(r.cuotaSin, 2) + " sin ella (" + eur(r.ahorroCuotaMes, 2) + " de diferencia al mes). ";
  note += "En " + anos + " pagas " + eur(r.interesesBon) + " de intereses con la bonificada y " + eur(r.interesesSin) + " sin vinculaciones. ";
  note += "La bonificación mínima que iguala los costes es " + umbral + "; tú tienes " + pts(d.bonif) + ". Las vinculaciones que puedes asumir son " + eur(r.vincMax) + " al año como máximo; tú pones " + eur(d.vinc) + ".</p>";
  if (d.horizonte > d.plazo) note += "<p>El horizonte se ha limitado al plazo (" + anos + ").</p>";
  note += "<p><strong>Condiciones y límites:</strong> mete en las vinculaciones solo el coste adicional respecto a lo que contratarías de todos modos (si el seguro del banco cuesta lo mismo que uno externo equivalente, su coste extra es 0; si cobras nómina ahí de todos modos, también). Si te quitan la bonificación al incumplir una vinculación, el tipo sube: los puntos de bonificación y su condición están en la escritura y en la oferta vinculante. No incluye tasación, notaría ni gestoría, cambios del Euríbor en variables ni amortizaciones anticipadas, y el tipo se supone fijo durante todo el plazo. Información orientativa, no asesoramiento.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: r.mejor === 2 ? "warn" : "ok",
    bigNumber: Math.abs(r.diferencia), bigLabel: r.mejor === 0 ? "menos con la bonificada en " + anos : (r.mejor === 1 ? "menos sin vinculaciones en " + anos : "de diferencia en " + anos), format: EM.eur,
    barsLabel: "Coste total en " + anos + " (intereses + comisión + vinculaciones)",
    bars: [{ label: "Bonificada" + (r.mejor === 0 ? " (más barata)" : ""), value: r.costeBon, color: "a" }, { label: "Sin vinculaciones" + (r.mejor === 1 ? " (más barata)" : ""), value: r.costeSin, color: "b" }],
    cols: ["Bonificada", "Sin vinculaciones"],
    rows: [
      ["Tipo (TIN)", EM.num(d.tin, 2) + " %", EM.num(d.tin + d.bonif, 2) + " %"],
      ["Cuota mensual", eur(r.cuotaBon, 2), eur(r.cuotaSin, 2)],
      ["Intereses en " + anos, eur(r.interesesBon), eur(r.interesesSin)],
      ["Comisión de apertura", eur(r.comisionBon), eur(r.comisionSin)],
      ["Vinculaciones en " + anos, eur(r.vincTotal), eur(0)],
      { label: "Coste total en " + anos, values: [eur(r.costeBon), eur(r.costeSin)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
