// Cuanto cobro de paro: cuantia de la prestacion contributiva (2026). Parametros generados desde data/params.json -> cuanto_cobro_paro_2026 (fuentes y fechas alli).
// tope/minimo: cuantia maxima y minima mensual por hijos a cargo (0, 1, 2 o mas) = IPREM 600 + 1/6 = 700, x 175/200/225 % y 80/107 %. escala: [dias cotizados minimos, dias de prestacion].
var P = {"tope": [1225, 1400, 1575], "minimo": [560, 749, 749], "pctAlto": 70, "pctBajo": 60, "diasAlto": 180, "minDias": 360, "diasMes": 30, "escala": [[2160, 720], [1980, 660], [1800, 600], [1620, 540], [1440, 480], [1260, 420], [1080, 360], [900, 300], [720, 240], [540, 180], [360, 120]]};
function duracion(dias) {
  for (var i = 0; i < P.escala.length; i++) if (dias >= P.escala[i][0]) return P.escala[i][1];
  return 0;
}
function calcular(d) {
  var dias = Math.round(d.dias);
  if (dias < P.minDias) return { bloqueo: 1 };
  var h = Math.min(Math.max(Math.round(d.hijos), 0), 2), j = d.jornada / 100;
  var br = d.base * (d.extras === "no" ? 14 / 12 : 1);
  var hi = P.tope[h] * j, lo = P.minimo[h] * j;
  var r = { bloqueo: 0, br: br, tope: hi, minimo: lo, hijos: h }, n, raw, pct;
  for (n = 1; n <= 2; n++) {
    pct = n === 1 ? P.pctAlto : P.pctBajo;
    raw = br * pct / 100;
    r["raw" + n] = raw;
    r["m" + n] = Math.min(Math.max(raw, lo), hi);
    r["dia" + n] = r["m" + n] / P.diasMes;
    r["ap" + n] = raw > hi ? 1 : (raw < lo ? -1 : 0);
  }
  var D = duracion(dias), d1 = Math.min(D, P.diasAlto), d2 = Math.max(D - P.diasAlto, 0);
  r.dur = D; r.d1 = d1; r.d2 = d2; r.meses = D / P.diasMes; r.dias = dias;
  r.t1 = r.dia1 * d1; r.t2 = r.dia2 * d2; r.total = r.t1 + r.t2;
  return r;
}
function eur(x) { return EM.eur(x); }
function txtMeses(n) { var r = Math.round(n * 10) / 10; return EM.num(r, Number.isInteger(r) ? 0 : 1) + (r === 1 ? " mes" : " meses"); }
var IDS = ["base", "hijos", "jornada", "dias"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.extras = document.getElementById("extras").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
function txtTope(ap, tope, minimo) { return ap === 1 ? " (limitada por el máximo de " + eur(tope) + ")" : (ap === -1 ? " (subida al mínimo de " + eur(minimo) + ")" : ""); }
function pintar() {
  var d = leer();
  if (d.base <= 0 || d.hijos < 0 || d.dias < 0) { aviso("Revisa los datos: la base de cotización debe ser mayor que 0 y los hijos y los días no pueden ser negativos."); return; }
  if (d.jornada < 1 || d.jornada > 100) { aviso("Revisa la jornada: indica el porcentaje medio de jornada de los últimos 180 días, entre 1 y 100."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("Con menos de 360 días cotizados en los seis años anteriores no te corresponde la prestación contributiva (la escala del art. 269.1 de la LGSS empieza en 360 días). Es posible que te corresponda un subsidio, que esta calculadora no calcula: consúltalo en el SEPE."); return; }
  var verdict = "Con tus datos cobrarías " + eur(r.m1) + " al mes los primeros " + P.diasAlto + " días (" + eur(r.dia1) + " al día)" + txtTope(r.ap1, r.tope, r.minimo) +
    (r.d2 > 0 ? " y " + eur(r.m2) + " al mes después (" + eur(r.dia2) + " al día)" + txtTope(r.ap2, r.tope, r.minimo) : "") +
    ", durante " + EM.num(r.dur, 0) + " días (" + txtMeses(r.meses) + "): unos " + eur(r.total) + " brutos en total, antes de IRPF y de la cotización a la Seguridad Social.";
  var note = "<p><strong>Cómo sale:</strong> tu base reguladora es " + eur(r.br) + " al mes" + (d.extras === "no" ? " (tu base sin pagas extra multiplicada por 14/12, para incluir su prorrateo)" : "") + ". La prestación es el " + P.pctAlto + " % de esa base los " + P.diasAlto + " primeros días (" + eur(r.raw1) + ") y el " + P.pctBajo + " % desde el día " + (P.diasAlto + 1) + " (" + eur(r.raw2) + "), con un máximo de " + eur(r.tope) + " y un mínimo de " + eur(r.minimo) + " al mes" + " con " + (r.hijos === 0 ? "ningún hijo" : (r.hijos === 1 ? "1 hijo" : "2 o más hijos")) + " a cargo" + (d.jornada < 100 ? " y ajustados a tu jornada del " + EM.num(d.jornada, 0) + " %" : "") + ".</p>";
  if (r.ap1 === 1) note += "<p>Tu base supera el máximo: aunque cotizaras más, no cobrarías más de " + eur(r.tope) + " al mes.</p>";
  if (r.ap1 === -1 || r.ap2 === -1) note += "<p>La prestación calculada queda por debajo del mínimo y se sube a " + eur(r.minimo) + " al mes.</p>";
  note += "<p><strong>Duración:</strong> con " + EM.num(r.dias, 0) + " días cotizados en los seis años anteriores te corresponden " + EM.num(r.dur, 0) + " días de prestación (art. 269.1 de la LGSS). Si te quedan dudas sobre capitalizar la prestación para ser autónomo, mira <a href=\"/decidir/capitalizar-paro-o-cobrarlo/\">capitalizar el paro o cobrarlo cada mes</a>.</p>";
  note += "<p><strong>No incluye:</strong> la retención del IRPF (tampoco la foral) ni la cotización a la Seguridad Social que se descuentan de lo que cobras (tu ingreso en la cuenta será menor que el importe bruto), los subsidios, la compatibilidad con un trabajo, las horas extra (se excluyen de la base reguladora), los fijos discontinuos, la pérdida de un empleo a tiempo parcial entre varios, las sanciones o suspensiones y el trabajo con reducción de jornada por cuidado de hijos.</p>";
  EM.renderResult({
    winner: r.ap1 === 1 ? "maximo" : (r.ap1 === -1 ? "minimo" : "normal"), verdict: verdict, tone: "info",
    bigNumber: r.m1, bigLabel: "al mes los primeros " + P.diasAlto + " días (bruto)", format: eur,
    barsLabel: "Prestación mensual bruta",
    bars: r.d2 > 0 ? [{ label: "Primeros " + P.diasAlto + " días", value: r.m1, color: "a" }, { label: "Desde el día " + (P.diasAlto + 1), value: r.m2, color: "b" }] : [{ label: "Primeros " + P.diasAlto + " días", value: r.m1, color: "a" }],
    cols: ["Primeros " + P.diasAlto + " días", "Desde el día " + (P.diasAlto + 1)],
    rows: [
      ["Porcentaje de la base reguladora", EM.num(P.pctAlto, 0) + " %", EM.num(P.pctBajo, 0) + " %"],
      ["Prestación mensual", eur(r.m1), r.d2 > 0 ? eur(r.m2) : "no llegas a este tramo"],
      ["Prestación diaria", eur(r.dia1), r.d2 > 0 ? eur(r.dia2) : "-"],
      ["Días de prestación", EM.num(r.d1, 0), EM.num(r.d2, 0)],
      ["Máximo / mínimo aplicado", r.ap1 === 1 ? "máximo" : (r.ap1 === -1 ? "mínimo" : "ninguno"), r.d2 > 0 ? (r.ap2 === 1 ? "máximo" : (r.ap2 === -1 ? "mínimo" : "ninguno")) : "-"],
      { label: "Total estimado (bruto)", values: [eur(r.t1), r.d2 > 0 ? eur(r.t2) : eur(0)], strong: true },
      ["Total de la prestación", eur(r.total), txtMeses(r.meses)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
