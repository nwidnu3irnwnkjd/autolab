// Fibra y movil: pack convergente o por separado. Coste en el horizonte, mes a mes (promocion y salto de precio).
// Los precios son del primer ano; a partir del mes 13 TODOS suben la subida anual (pack y suelto) en escalon anual.
// Pack: packPromo los primeros meses de promocion, packTras despues, mas un coste unico. Suelto: sin promocion ni coste unico.
function factor(t, s) { return Math.pow(1 + s / 100, Math.floor((t - 1) / 12)); }
function packMes(d, t) { return (t <= d.promoMeses ? d.packPromo : d.packTras) * factor(t, d.subida); }
function sepMes(d, t) { return d.suelto * factor(t, d.subida); }
function ventajaEn(d, H) { var a = -d.unico, t; for (t = 1; t <= H; t++) a += sepMes(d, t) - packMes(d, t); return a; }
function calcular(d) {
  var H = Math.max(Math.round(d.horizonte), 1), P = Math.max(Math.round(d.permanencia), 0), t, cp = d.unico, cs = 0;
  for (t = 1; t <= H; t++) { cp += packMes(d, t); cs += sepMes(d, t); }
  var a = -d.unico, rec = 0, agota = 0, maxA = -Infinity, maxMes = 0, prev = -d.unico;
  for (t = 1; t <= 600; t++) {
    a += sepMes(d, t) - packMes(d, t);
    if (rec === 0 && a >= 0) rec = t;
    if (agota === 0 && prev >= 0 && a < 0) agota = t;
    if (t <= H && a > maxA) { maxA = a; maxMes = t; }
    prev = a;
  }
  var caro = 0; if (d.packPromo > d.suelto && d.promoMeses > 0) caro = 1; else if (d.packTras > d.suelto) caro = d.promoMeses + 1;
  var exp = 0, atr = 0, lim = Math.min(P, H);
  for (t = 1; t <= lim; t++) { var df = packMes(d, t) - sepMes(d, t); if (df > 1e-9) { exp += df; atr++; } }
  return {
    costePack: cp, costeSuelto: cs, medioPack: cp / H, medioSuelto: cs / H, ventaja: cs - cp,
    ventaja12: ventajaEn(d, 12), ventaja24: ventajaEn(d, 24), ventaja36: ventajaEn(d, 36),
    mesRecupera: rec, mesAgota: agota, mesCaro: caro, ventajaMax: maxA, mesVentajaMax: maxMes,
    exposicion: exp, mesesAtrapado: atr, permanenciaMayorQueHorizonte: P > H ? 1 : 0, mejor: cp < cs - 1 ? 0 : (cs < cp - 1 ? 1 : 2)
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["packPromo", "promoMeses", "packTras", "suelto", "permanencia", "unico", "horizonte", "subida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function meses(n) { return EM.num(n, 0) + (n === 1 ? " mes" : " meses"); }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.packTras <= 0 || d.packPromo <= 0 || d.suelto <= 0 || d.horizonte < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe los precios del pack y de lo que pagarías por separado (mayores que 0) y un horizonte de al menos 1 mes.", tone: "warn",
      note: "<p>Sin precios no hay nada que comparar. Si el pack no tiene promoción, pon 0 meses de promoción y el mismo precio en los dos campos del pack.</p>" });
    return;
  }
  if (d.horizonte > 120 || d.subida > 30 || d.promoMeses > 120 || d.permanencia > 60) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: horizonte de hasta 120 meses, promoción de hasta 120, permanencia de hasta 60 y subida anual de hasta el 30 %.", tone: "warn",
      note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  if (d.promoMeses > 0 && d.packPromo > d.packTras) {
    EM.renderResult({ winner: "invalido", verdict: "El precio con promoción (" + EM.eur(d.packPromo, 2) + ") no puede ser mayor que el de después (" + EM.eur(d.packTras, 2) + ").", tone: "warn",
      note: "<p>Una promoción rebaja el precio los primeros meses. Si no hay promoción, pon 0 meses.</p>" });
    return;
  }
  var r = calcular(d), H = Math.round(d.horizonte), v = r.ventaja, verdict, w;
  if (r.mejor === 2) { w = "empate"; verdict = "Con estos datos el pack y la compra por separado cuestan lo mismo en " + meses(H) + ": " + eur(r.costePack) + " frente a " + eur(r.costeSuelto) + "."; }
  else if (r.mejor === 0) {
    w = "pack";
    verdict = "Con estos datos el pack sale " + eur(v) + " más barato en " + meses(H) + " (" + eur(r.costePack) + " frente a " + eur(r.costeSuelto) + ")";
    verdict += r.mesCaro > 0 ? ", pero deja de compensar cada mes desde el mes " + EM.num(r.mesCaro, 0) + (r.mesAgota > 0 ? " y esa ventaja se agota si te quedas más allá del mes " + EM.num(r.mesAgota, 0) + "." : " y esa ventaja se va reduciendo cada mes.") : " y seguirá siendo más barato después de la promoción.";
  } else {
    w = "separado";
    verdict = "Con estos datos, por separado sale " + eur(-v) + " más barato en " + meses(H) + " (" + eur(r.costeSuelto) + " frente a " + eur(r.costePack) + ")";
    verdict += r.ventajaMax > 1 ? "; el pack solo gana en horizontes cortos, con un máximo de " + eur(r.ventajaMax) + " a favor en el mes " + EM.num(r.mesVentajaMax, 0) + "." : ".";
  }
  var note = "<p><strong>Lectura:</strong> la respuesta depende del horizonte. Ventaja del pack frente a ir por separado (positivo = el pack ahorra): a 12 meses " + eur(r.ventaja12) + ", a 24 meses " + eur(r.ventaja24) + " y a 36 meses " + eur(r.ventaja36) + ". ";
  if (r.mesRecupera > 0 && r.mejor !== 2) note += "El pack empieza a ir por delante en el acumulado en el mes " + EM.num(r.mesRecupera, 0) + ". ";
  else if (d.unico > 0) note += "El pack no llega a recuperar el coste único de " + eur(d.unico) + " con los precios indicados. ";
  if (r.mesCaro > 0) note += "Desde el mes " + EM.num(r.mesCaro, 0) + " la cuota mensual del pack supera la de ir por separado; ";
  if (r.mesAgota > 0) note += "la ventaja acumulada se agotaría en el mes " + EM.num(r.mesAgota, 0) + ". ";
  note += "</p>";
  if (d.permanencia > 0) {
    note += "<p><strong>Permanencia:</strong> " + (r.mesesAtrapado > 0 ? "durante " + meses(r.mesesAtrapado) + " de los " + meses(Math.min(Math.round(d.permanencia), H)) + " de permanencia dentro de tu horizonte pagarías más que por separado, " + eur(r.exposicion) + " en total. " : "dentro de la permanencia que cae en tu horizonte el pack no te cuesta más al mes que ir por separado. ");
    if (r.permanenciaMayorQueHorizonte) note += "Tu permanencia es mayor que tu horizonte: irte antes tendría una penalización que esta página no calcula; si la conoces, súmala al coste único.";
    note += "</p>";
  }
  note += "<p><strong>Límites:</strong> los precios son tuyos o ejemplos, no ofertas de ninguna operadora. No incluye la calidad del servicio, la cobertura, los datos o la velocidad de cada opción, ni descuentos futuros por renegociar. Los precios por separado se suponen sin promoción. Todos los precios suben la misma subida anual a partir del mes 13.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: r.mejor === 1 && r.ventajaMax > 1 ? "warn" : (r.mejor === 2 ? "warn" : "ok"),
    bigNumber: Math.min(r.medioPack, r.medioSuelto), bigLabel: "al mes de media con la opción más barata", format: EM.eur,
    barsLabel: "Coste total en el horizonte",
    bars: [{ label: "Pack" + (r.mejor === 0 ? " (más barato)" : ""), value: Math.max(r.costePack, 0), color: "a" }, { label: "Por separado" + (r.mejor === 1 ? " (más barato)" : ""), value: Math.max(r.costeSuelto, 0), color: "b" }],
    cols: ["Pack", "Por separado"],
    rows: [
      ["Coste total en " + meses(H), eur(r.costePack), eur(r.costeSuelto)],
      ["Coste medio al mes", eur(r.medioPack, 2), eur(r.medioSuelto, 2)],
      ["Pago único de entrada", eur(d.unico), eur(0)],
      ["Ventaja del pack a 12 meses", eur(r.ventaja12), "—"],
      ["Ventaja del pack a 24 meses", eur(r.ventaja24), "—"],
      ["Ventaja del pack a 36 meses", eur(r.ventaja36), "—"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
