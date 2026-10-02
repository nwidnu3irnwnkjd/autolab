// Pagas extra prorrateadas o en 14 pagas. Parámetros: data/params.json -> pagas_extra_prorrateo_2026 (fuentes y fechas allí).
// ET 31 (prorrateo solo por convenio), LGSS 147.1 (cotización igual: las pagas entran prorrateadas en 12 meses) y 270.1 (paro), Decreto 1646/1972 art. 13 (IT), RIRPF 83.2 y 86.1 (mismo tipo anual).
var P = {"bmax": 5101.2, "cot": [6.5, 6.55], "diasBR": 30, "md": [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], "acum": [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334], "smi": 17094};
function r2(x) { return Math.round(x * 100 + 1e-7) / 100; }
// d: bruto anual, extras 2|3|4, contrato indef|temp, ret (%), situacion todo|baja, mes y dia del último día trabajado (solo baja)
function calcular(d) {
  var B = +d.bruto || 0, n = Math.floor(+d.extras) || 2, t = (+d.ret || 0) / 100, cot = (d.contrato === "temp" ? P.cot[1] : P.cot[0]) / 100;
  var baja = d.situacion === "baja", m = Math.floor(+d.mes || 0), dd = Math.floor(+d.dia || 0);
  var fechaOk = m >= 1 && m <= 12 && dd >= 1 && dd <= P.md[m - 1];
  if (!(B > 0) || (n !== 2 && n !== 3 && n !== 4) || (baja && !fechaOk)) return { bloqueado: 1, escenario: 0 };
  var pe = B / (12 + n), m14 = pe, m12 = B / 12;
  var base = Math.min(B / 12, P.bmax), cotMes = base * cot;
  var o = { bloqueado: 0, escenario: baja ? 2 : 1, pagaExtra: r2(pe), mensual14: r2(m14), mensual12: r2(m12), baseCot: r2(base), cotMes: r2(cotMes), baseDiaria: r2(base / P.diasBR),
    retMes14: r2(m14 * t), retMesPaga14: r2(2 * m14 * t), retMes12: r2(m12 * t),
    netoMes14: r2(m14 * (1 - t) - cotMes), netoMesPaga14: r2(2 * m14 * (1 - t) - cotMes), netoMes12: r2(m12 * (1 - t) - cotMes) };
  o.difMensual = r2((m12 * (1 - t) - cotMes) - (m14 * (1 - t) - cotMes));
  o.bajoSmi = B < P.smi ? 1 : 0;
  if (!baja) {
    var net14 = 0, ret14 = 0, k, mm, g;
    for (mm = 1; mm <= 12; mm++) {
      g = m14;
      for (k = 1; k <= n; k++) if (Math.floor(12 * k / n) === mm) g += pe;
      ret14 += g * t; net14 += g * (1 - t) - cotMes;
    }
    var net12 = 12 * (m12 * (1 - t) - cotMes);
    o.netoAnual14 = r2(net14); o.netoAnual12 = r2(net12); o.difAnual = r2(net14 - net12);
    o.retAnual14 = r2(ret14); o.retAnual12 = r2(B * t); o.cotAnual = r2(12 * cotMes);
    return o;
  }
  var meses = (m - 1) + dd / P.md[m - 1], f = P.acum[m - 1] + dd, pend = 0, paid = 0, sm, em, ini, fin, acc;
  for (var j = 0; j < n; j++) {
    sm = Math.floor(12 * j / n) + 1; em = Math.floor(12 * (j + 1) / n);
    ini = P.acum[sm - 1] + 1; fin = P.acum[em - 1] + P.md[em - 1];
    acc = Math.max(0, Math.min(f - ini + 1, fin - ini + 1)) / (fin - ini + 1) * pe;
    if (em < m) paid += acc; else pend += acc;
  }
  var g14 = m14 * meses + paid + pend, g12 = m12 * meses, cotTot = cotMes * meses;
  o.devengado14 = r2(g14); o.devengado12 = r2(g12); o.difDevengado = r2(g14 - g12);
  o.pendiente14 = r2(pend); o.pendienteNeto14 = r2(pend * (1 - t)); o.nomina14 = r2(g14 - pend); o.nomina12 = r2(g12);
  o.neto14 = r2(g14 * (1 - t) - cotTot); o.neto12 = r2(g12 * (1 - t) - cotTot); o.difNeto = r2((g14 - g12) * (1 - t));
  return o;
}
function eur(x) { return EM.eur(x); }
function pct(x) { return EM.num(x, 2) + " %"; }
function leer() {
  var d = {}; ["bruto", "extras", "ret", "mes", "dia"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["contrato", "situacion"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.ret < 0 || d.ret > 100) return;
  var r = calcular(d);
  if (r.bloqueado) {
    EM.renderResult({ winner: "bloqueado", tone: "warn", verdict: d.bruto > 0 ? "Esa fecha no existe en 2026: revisa el día y el mes del último día trabajado." : "Escribe tu salario bruto anual (el total de las pagas, extras incluidas).", note: "<p>La calculadora compara el mismo bruto anual cobrado en pagas extra separadas o prorrateadas, con el calendario de 2026.</p>" });
    return;
  }
  var N = 12 + (+d.extras), v, rows, note = "", big, bigL, bars;
  if (r.escenario === 1) {
    v = "Con " + eur(d.bruto) + " brutos al año, cobrar en " + N + " pagas o prorrateado en 12 te deja el mismo neto al año (" + eur(r.netoAnual14) + ", diferencia " + eur(Math.abs(r.difAnual)) + "), con la misma retención y la misma cotización; lo que cambia es cuándo lo cobras: " + eur(r.netoMes12) + " netos cada mes prorrateado frente a " + eur(r.netoMes14) + " en los meses sin paga extra, " + eur(r.difMensual) + " menos al mes (y " + eur(r.netoMesPaga14) + " en los meses con paga).";
    big = r.difMensual; bigL = "más al mes sin paga extra con el prorrateo (el neto anual es el mismo)";
    bars = [{ label: "Neto de un mes sin paga extra, " + N + " pagas", value: r.netoMes14, color: "a" }, { label: "Neto de un mes con prorrateo (12 pagas)", value: r.netoMes12, color: "b" }];
    rows = [["Bruto de cada paga", eur(r.mensual14), eur(r.mensual12)], ["Retención de ese mes (" + pct(d.ret) + ")", eur(r.retMes14), eur(r.retMes12)], ["Cotización del mes (idéntica)", eur(r.cotMes), eur(r.cotMes)], ["Neto de un mes sin paga extra", eur(r.netoMes14), eur(r.netoMes12)], ["Neto de un mes con paga extra", eur(r.netoMesPaga14), eur(r.netoMes12)], ["Retención del año", eur(r.retAnual14), eur(r.retAnual12)], ["Cotización del año", eur(r.cotAnual), eur(r.cotAnual)], { label: "Neto del año", values: [eur(r.netoAnual14), eur(r.netoAnual12)], strong: true }, ["Base diaria del paro (la de la baja es igual en las dos formas)", eur(r.baseDiaria), eur(r.baseDiaria)]];
  } else {
    var mayor = r.difDevengado >= 0 ? N + " pagas" : "el prorrateo";
    v = "Si dejas la empresa el " + dd2(d) + ", con " + N + " pagas se te devengan " + eur(r.devengado14) + " brutos y con el prorrateo " + eur(r.devengado12) + " (" + (Math.abs(r.difDevengado) < 0.005 ? "sin diferencia" : "diferencia de " + eur(Math.abs(r.difDevengado)) + " a favor de " + mayor + ", por contar la paga por días y el sueldo por meses") + "); lo que cambia es cuánto llega en el finiquito: " + eur(r.pendiente14) + " brutos de pagas pendientes con " + N + " pagas y 0 € con el prorrateo, que ya cobraste mes a mes.";
    big = r.pendiente14; bigL = "brutos de pagas extra que te pagan en el finiquito con " + N + " pagas (0 € con prorrateo)";
    bars = [{ label: N + " pagas: neto devengado hasta la baja", value: r.neto14, color: "a" }, { label: "Prorrateo: neto devengado hasta la baja", value: r.neto12, color: "b" }];
    rows = [["Devengado bruto hasta la baja", eur(r.devengado14), eur(r.devengado12)], ["Cobrado ya en nómina (bruto)", eur(r.nomina14), eur(r.nomina12)], ["Pendiente en el finiquito (bruto)", eur(r.pendiente14), eur(0)], ["Pendiente en el finiquito (neto, mismo tipo)", eur(r.pendienteNeto14), eur(0)], { label: "Neto devengado hasta la baja", values: [eur(r.neto14), eur(r.neto12)], strong: true }, ["Base diaria del paro (la de la baja es igual en las dos formas)", eur(r.baseDiaria), eur(r.baseDiaria)]];
  }
  if (r.bajoSmi) note += "<p><strong>Ojo con el mínimo:</strong> por debajo de " + eur(P.smi) + " brutos al año (salario mínimo de 2026 en 14 pagas) rigen bases mínimas de cotización por grupo que esta calculadora no modela.</p>";
  if (d.bruto / 12 > P.bmax) note += "<p>Tu sueldo supera la base máxima de cotización (" + eur(P.bmax) + " al mes): la cotización se calcula sobre la base máxima, igual en las dos formas.</p>";
  note += "<p><strong>Esto no lo eliges tú solo:</strong> la ley prevé el prorrateo cuando lo acuerda el convenio colectivo (art. 31 del Estatuto): mira el tuyo antes de pedirlo; y cuándo se cobran las pagas y si se devengan por días o por meses también lo fija el convenio (aquí: devengo por días y cobro al cierre de cada periodo).</p>";
  EM.renderResult({ winner: "e" + r.escenario, verdict: v, tone: "ok", bigNumber: big, bigLabel: bigL, format: EM.eur, barsLabel: "Neto", bars: bars, cols: [N + " pagas", "12 pagas (prorrateo)"], rows: rows, note: note });
}
function dd2(d) { return d.dia + "/" + d.mes + "/2026"; }
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
