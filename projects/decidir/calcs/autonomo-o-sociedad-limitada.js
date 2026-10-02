// Autonomo o SL (2026). Parametros generados desde data/params.json (autonomo_sl_2026, irpf_2026, autonomo_2026; fuentes y fechas alli).
// est/ccaa: escalas generales y minimos; reta: [limite mensual, base minima] de la tabla 2026; ah: escala del ahorro (cada mitad, estatal y autonomica); is: tipos IS 2026; socDed: % deduccion del autonomo societario; baseG7: base minima del grupo 7.
var P = {"est":[[0,9.5],[12450,12],[20200,15],[35200,18.5],[60000,22.5],[300000,24.5]],"ccaa":{"andalucia":{"esc":[[0,9.5],[13000,12],[21100,15],[35200,18.5],[60000,22.5]],"min":{"c":5790,"d":[2510,2820,4170,4700]}},"aragon":{"esc":[[0,9.5],[13072.5,12],[21210,15],[36960,18.5],[52500,20.5],[60000,23],[80000,24],[90000,25],[130000,25.5]],"min":null},"asturias":{"esc":[[0,9],[12450,12],[17707.2,14],[33007.2,19.2],[53407.2,21.5],[70000,22.5],[90000,25],[175000,26]],"min":{"c":6105,"d":[2640,2970,4400,4950]}},"baleares":{"esc":[[0,9],[10000,11.25],[18000,14.25],[30000,17.5],[48000,19],[70000,21.75],[90000,22.75],[120000,23.75],[175000,24.75]],"min":{"c":5550,"d":[2400,2970,4400,4950]}},"canarias":{"esc":[[0,9],[13748,11.5],[19422,14],[35924,18.5],[57566,23.5],[93268,25],[123745,26]],"min":{"c":5606,"d":[2424,2727,4040,4545]}},"cantabria":{"esc":[[0,8.5],[13000,11],[21000,14.5],[35200,18],[60000,22.5],[90000,24.5]],"min":null},"clm":{"esc":[[0,9.5],[12450,12],[20200,15],[35200,18.5],[60000,22.5]],"min":null},"cyl":{"esc":[[0,9],[12450,12],[20200,14],[35200,18.5],[53407.2,21.5]],"min":null,"orient":true},"cataluna":{"esc":[[0,9.5],[12500,12.5],[22000,16],[33000,19],[53000,21.5],[90000,23.5],[120000,24.5],[175000,25.5]],"min":null},"extremadura":{"esc":[[0,7.75],[12450,9.75],[20200,16],[24200,17.5],[35200,21],[60000,23.5],[80200,24],[99200,24.5],[120200,25]],"min":null},"galicia":{"esc":[[0,9],[12985.35,11.65],[21068.6,14.9],[35200,18.4],[60000,22.5]],"min":{"c":5789,"d":[2503,2816,4172,4694]}},"madrid":{"esc":[[0,8.5],[13362.22,10.7],[19004.63,12.8],[35425.68,17.4],[57320.4,20.5]],"min":{"c":5956.65,"d":[2575.85,2897.83,4400,4950]}},"murcia":{"esc":[[0,9.5],[12450,11.2],[20200,13.3],[34000,17.9],[60000,22.5]],"min":null,"orient":true},"rioja":{"esc":[[0,8],[12450,10.6],[20200,13.6],[35200,17.8],[40000,18.3],[50000,19],[60000,24.5],[120000,27]],"min":null,"orient":true},"valencia":{"esc":[[0,8.8],[12000,11.7],[22000,14.6],[32000,17],[42000,19.4],[52000,21.9],[62000,24.4],[72000,26.1],[100000,27.35],[150000,28.35],[200000,29.35]],"min":{"c":6105,"d":[2640,2970,4400,4950]}}},"reta":[[670,653.59],[900,718.95],[1166.7,849.67],[1300,950.98],[1500,960.78],[1700,960.78],[1850,1143.79],[2030,1209.15],[2330,1274.51],[2760,1356.21],[3190,1437.91],[3620,1519.61],[4050,1601.31],[6000,1732.03],[null,1928.1]],"tipoReta":0.315,"genericos":0.07,"djPct":0.05,"djMax":2000,"ah":[[0,9.5],[6000,10.5],[50000,11.5],[200000,13.5],[300000,15]],"is":{"nueva":15,"micro":[50000,19,21],"reducida":23},"socDed":3,"baseG7":1424.4,"otras":6500};
var BE_PASO = 100, BE_TOPE = 400000;
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
// Cuota integra (estatal + autonomica): base general con el minimo personal; el minimo que la general no absorbe pasa a la base del ahorro (arts. 56.2, 63, 66, 76).
function irpfTotal(blg, bla, cc) {
  var mE = 5550, mC = cc.min ? cc.min.c : 5550, tot = 0, i, sc = [P.est, cc.esc], m = [mE, mC], resto;
  for (i = 0; i < 2; i++) {
    resto = Math.max(0, m[i] - blg);
    tot += Math.max(0, escala(blg, sc[i]) - escala(Math.min(blg, m[i]), sc[i])) + Math.max(0, escala(bla, P.ah) - escala(Math.min(bla, resto), P.ah));
  }
  return tot;
}
function red20(n) {
  if (n >= 19747.5) return 0;
  if (n <= 14852) return 7302;
  if (n <= 17673.52) return 7302 - 1.75 * (n - 14852);
  return Math.max(0, 2364.34 - 1.14 * (n - 17673.52));
}
function baseMin(R) {
  var i, t;
  for (i = 0; i < P.reta.length; i++) {
    t = P.reta[i];
    if (t[0] === null || (i === 2 ? R < t[0] : R <= t[0])) return t[1];
  }
}
function dj(N) { return Math.min(P.djMax, P.djPct * Math.max(N, 0)); }
function cuotaRetaAut(C) { return 12 * baseMin(C > 0 ? (1 - P.genericos) * C / 12 : 0) * P.tipoReta; }
function ssAut(I) {
  var s = 0, k, c;
  for (k = 0; k < 60; k++) { c = cuotaRetaAut(I - dj(I - s)); if (Math.abs(c - s) < 1e-9) break; s = c; }
  return s;
}
// Autonomo individual: rendimiento = beneficio; cuota RETA por tramo, 5 % de dificil justificacion y reduccion del art. 32.2.3.o.
function autonomo(I, cc) {
  var s = ssAut(I), N = I - s, rn = N - dj(N), r3 = Math.max(rn, 0), red = 0;
  if (r3 > 0 && r3 < 12000) red = Math.min(r3 <= 8000 ? 1620 : 1620 - 0.405 * (r3 - 8000), r3);
  var irpf = irpfTotal(Math.max(rn - red, 0), 0, cc);
  return { ss: s, irpf: irpf, neto: I - s - irpf };
}
function sociedades(base, tipo) {
  if (base <= 0) return 0;
  if (tipo === "nueva") return base * P.is.nueva / 100;
  if (tipo === "reducida") return base * P.is.reducida / 100;
  return Math.min(base, P.is.micro[0]) * P.is.micro[1] / 100 + Math.max(base - P.is.micro[0], 0) * P.is.micro[2] / 100;
}
// SL con un socio-administrador con control efectivo: IS sobre el resultado tras retribucion y costes; dividendos (base del ahorro); cuota RETA societaria.
function sl(R, S, p, cc, tipo, C) {
  var Sx = Math.min(S, Math.max(R - C, 0)), base = R - Sx - C, is = sociedades(base, tipo), U = base - is, D = p * Math.max(U, 0), ret = Math.max(U, 0) - D;
  var comp = (Sx + D) * (1 - P.socDed / 100), rm = comp > 0 ? comp / 12 : 0, cuota = 12 * Math.max(baseMin(rm), P.baseG7) * P.tipoReta;
  var nt = Math.max(0, Sx - cuota), otros = Math.min(2000, nt), red = D <= P.otras ? red20(nt) : 0, blg = Math.max(0, nt - otros - red);
  var irpf = irpfTotal(blg, D, cc);
  return { Sx: Sx, base: base, is: is, U: U, D: D, ret: ret, cuota: cuota, irpf: irpf, neto: Sx + D - cuota - irpf };
}
// Beneficio a partir del cual el neto de la SL alcanza el del autonomo y ya no baja de el (barrido de 100 EUR y biseccion).
function equilibrio(S, p, cc, tipo, C) {
  var R, lastBelow = null, lo, hi, m, j;
  for (R = 0; R <= BE_TOPE; R += BE_PASO) if (sl(R, S, p, cc, tipo, C).neto - autonomo(R, cc).neto < 0) lastBelow = R;
  if (lastBelow === null) return 0;
  lo = lastBelow; hi = lo + BE_PASO;
  if (sl(hi, S, p, cc, tipo, C).neto - autonomo(hi, cc).neto < 0) return null;
  for (j = 0; j < 60; j++) { m = (lo + hi) / 2; if (sl(m, S, p, cc, tipo, C).neto - autonomo(m, cc).neto >= 0) hi = m; else lo = m; }
  return hi;
}
function calcular(d) {
  var cc = P.ccaa[d.ccaa], p = Math.min(Math.max(+d.pct || 0, 0), 100) / 100, R = Math.max(+d.benef || 0, 0), S = Math.max(+d.retrib || 0, 0), C = Math.max(+d.costes || 0, 0);
  var a = autonomo(R, cc), s = sl(R, S, p, cc, d.tipo, C), dif = s.neto - a.neto;
  return {
    netoAut: a.neto, ssAut: a.ss, irpfAut: a.irpf, netoSL: s.neto, isoc: s.is, dividendos: s.D, retenido: s.ret, cuotaSL: s.cuota, irpfSL: s.irpf, retribEf: s.Sx,
    baseSL: s.base, equilibrio: equilibrio(S, p, cc, d.tipo, C), equilibrio100: p < 1 ? equilibrio(S, 1, cc, d.tipo, C) : equilibrio(S, p, cc, d.tipo, C), diferencia: dif, ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "sl" : "autonomo"),
    tope: S > Math.max(R - C, 0) ? 1 : 0, art20: s.D > P.otras ? 1 : 0, orientativo: cc.orient ? 1 : 0, ccaaNombre: ''
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["benef", "retrib", "pct", "costes"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; d.tipo = document.getElementById("tipo").value;
  return d;
}
var TIPO_TXT = { nueva: "15 % (nueva creación)", micro: "19 % hasta 50.000 € y 21 % el resto", reducida: "23 % (entidad de reducida dimensión)" };
function pintar() {
  var d = leer(), r = calcular(d), nm = function (x) { return eur(x / 12); }, verdict, note = "", rows;
  var cond = "con " + eur(d.benef) + " de beneficio, " + eur(r.retribEf) + " de retribución, " + EM.num(d.pct, 0) + " % de dividendos y " + eur(d.costes) + " de costes de la SL";
  if (d.benef <= 0) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Introduce un beneficio anual mayor que 0: sin beneficio no hay nada que comparar (el autónomo paga su cuota mínima y la SL sus costes y su cuota).",
      note: "<p>Esta herramienta compara el neto en mano de un titular que factura como autónomo con el de una SL unipersonal con un socio-administrador.</p>" });
    return;
  }
  if (r.ganador === "sl") verdict = "Con estos datos, " + cond + ", la SL te deja " + eur(r.diferencia) + " más al año en mano que ser autónomo (" + eur(r.netoSL) + " frente a " + eur(r.netoAut) + ").";
  else if (r.ganador === "autonomo") verdict = "Con estos datos, " + cond + ", ser autónomo te deja " + eur(-r.diferencia) + " más al año en mano que la SL (" + eur(r.netoAut) + " frente a " + eur(r.netoSL) + ").";
  else verdict = "Con estos datos, " + cond + ", quedas igual en mano con la SL que como autónomo (" + eur(r.netoAut) + ").";
  if (r.equilibrio === null) verdict += " Con estas condiciones la SL no alcanza al autónomo con beneficios de hasta " + eur(400000) + ".";
  else if (r.equilibrio === 0) verdict += " Con estas condiciones la SL deja al menos lo mismo desde el primer euro.";
  else verdict += " Con esas mismas condiciones, la SL deja más neto en mano que el autónomo a partir de unos " + eur(r.equilibrio) + " de beneficio al año.";
  if (d.pct < 100) verdict += r.equilibrio100 === null ? " Aunque repartieras el 100 % de los dividendos, la SL no alcanzaría al autónomo con beneficios de hasta " + eur(400000) + "." : " Si repartieras el 100 % de los dividendos, ese umbral sería de unos " + eur(r.equilibrio100) + ".";
  if (r.retenido > 0) verdict += " Además, quedan " + eur(r.retenido) + " en la SL tras el Impuesto sobre Sociedades, sin repartir (no cuentan como neto en mano y tributarán al repartirlos).";
  if (r.tope) note += "<p><strong>Retribución ajustada:</strong> la retribución que has indicado supera el resultado menos los costes de la SL; se ha limitado a " + eur(r.retribEf) + " para que la SL no tenga pérdidas.</p>";
  if (r.baseSL <= 0) note += "<p><strong>Atención:</strong> tras la retribución y los costes la SL no tiene base imponible positiva: no paga Impuesto sobre Sociedades, no hay dividendos y aun así cotizas la base mínima del autónomo societario.</p>";
  if (r.art20) note += "<p><strong>Dividendos sobre 6.500 €:</strong> con otras rentas distintas del trabajo por encima de 6.500 € no se aplica la reducción del art. 20 de la Ley del IRPF al sueldo (ya descontada en el cálculo).</p>";
  if (r.orientativo) note += "<p><strong>Cifras autonómicas orientativas:</strong> para tu comunidad alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»).</p>";
  if (d.tipo === "nueva") note += "<p><strong>El 15 % es temporal:</strong> solo se aplica en el primer periodo con base imponible positiva y en el siguiente; después rige la escala de microempresa y el umbral sube (calcúlalo con esa opción). Tampoco vale si ya ejercías la actividad como autónomo el año anterior y tienes más del 50 % de la SL.</p>";
  note += "<p><strong>Lectura:</strong> el neto en mano es lo que recibes tras impuestos y cuotas; lo no repartido queda en la SL y no cuenta. Tipo del Impuesto sobre Sociedades: " + TIPO_TXT[d.tipo] + ". La cuota de la SL (" + eur(r.cuotaSL / 12) + " al mes) parte de la base mínima del autónomo societario y sube con retribución y dividendos.</p>";
  note += "<p><strong>No incluye:</strong> la responsabilidad limitada (no se puede valorar en euros), IVA, retenciones, deducciones, reserva legal, tarifa plana y bonificaciones, gastos distintos en cada forma, venta o liquidación de la SL, patrimonio, sociedades patrimoniales o profesionales (en una SL profesional lo que cobras es rendimiento de actividad, art. 27.1 LIRPF, y debe ir a valor de mercado), varios socios ni hijos. Supone retribución deducible (prevista en los estatutos), control efectivo de la SL y la cifra de negocios del tipo elegido. Consulta con un asesor fiscal y mercantil.</p>";
  rows = [
    ["Beneficio de la actividad", eur(d.benef), eur(d.benef)],
    ["Retribución como administrador (bruta)", "–", eur(r.retribEf)],
    ["Costes extra de la SL", "–", eur(d.costes)],
    ["Impuesto sobre Sociedades", "–", eur(r.isoc)],
    ["Dividendos (brutos)", "–", eur(r.dividendos)],
    ["Cuota de la Seguridad Social (RETA)", eur(r.ssAut), eur(r.cuotaSL)],
    ["IRPF (sueldo y dividendos)", eur(r.irpfAut), eur(r.irpfSL)],
    { label: "Neto en mano al año", values: [eur(r.netoAut), eur(r.netoSL)], strong: true },
    ["Neto en mano al mes (÷ 12)", nm(r.netoAut), nm(r.netoSL)],
    ["Se queda en la SL sin repartir", "–", eur(r.retenido)]
  ];
  var xs = [], ya = [], ys = [], x, step = Math.max(1000, Math.round(Math.max(d.benef * 2.5, 60000) / 30 / 1000) * 1000);
  var cc = P.ccaa[d.ccaa], p = Math.min(Math.max(d.pct, 0), 100) / 100;
  for (x = 0; x <= Math.max(d.benef * 2.5, 60000); x += step) { ya.push([x, autonomo(x, cc).neto]); ys.push([x, sl(x, d.retrib, p, cc, d.tipo, d.costes).neto]); }
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: r.ganador === "sl" ? "ok" : "warn",
    bigNumber: r.equilibrio === null ? undefined : r.equilibrio, bigLabel: "de beneficio al año a partir del cual la SL deja más neto en mano que ser autónomo, con tus datos de sueldo, dividendos, costes, tipo del IS y comunidad", format: eur,
    barsLabel: "Neto en mano al año tras impuestos y cuotas",
    bars: [{ label: "Autónomo" + (r.ganador === "autonomo" ? " (gana)" : ""), value: Math.max(r.netoAut, 0), color: "a" },
           { label: "SL" + (r.ganador === "sl" ? " (gana)" : ""), value: Math.max(r.netoSL, 0), color: "b" }],
    line: { caption: "Neto en mano según el beneficio anual (con tus demás datos)", xLabel: "Beneficio anual", xFormat: eur, yFormat: eur,
      series: [{ label: "Autónomo", color: "a", points: ya }, { label: "SL", color: "b", points: ys }] },
    cols: ["Autónomo", "SL"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
