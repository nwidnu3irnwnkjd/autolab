// Jubilacion anticipada o demorada (2026). Norma: LGSS (RDL 8/2015, consolidado a 31/07/2026) arts. 205.1, 208, 210 y DT 7.ª y 9.ª; RD 241/2026 (limites de pension). Parametros y fuentes en data/params.json (pensiones_2026.jubilacion).
var P = {
  maxMes: 3359.60, topeAnual: 61214.40, minBaja: 12441.80, minAlta: 17592.40, refAnio: 2026, refMes: 9,
  // DT 7.ª: [anio, meses cotizados para jubilarse a los 65, edad exigida en meses si no se llega]
  dt7: [[2013, 423, 781], [2014, 426, 782], [2015, 429, 783], [2016, 432, 784], [2017, 435, 785], [2018, 438, 786], [2019, 441, 788], [2020, 444, 790], [2021, 447, 792], [2022, 450, 794], [2023, 453, 796], [2024, 456, 798], [2025, 459, 800], [2026, 459, 802]],
  dt7Futuro: [462, 804],
  // DT 9.ª: [anio desde, meses al tipo alto, tipo alto %, tipo bajo %]
  dt9: [[2027, 248, 0.19, 0.18], [2023, 49, 0.21, 0.19], [2020, 106, 0.21, 0.19], [0, 163, 0.21, 0.19]],
  // art. 208.2: porcentaje de reduccion por meses de anticipo (indice 0 = 1 mes) y columna de cotizacion
  coef: [[3.26, 3.11, 2.96, 2.81], [3.38, 3.23, 3.08, 2.92], [3.52, 3.36, 3.20, 3.04], [3.67, 3.50, 3.33, 3.17], [3.83, 3.65, 3.48, 3.30], [4.00, 3.82, 3.64, 3.45],
    [4.19, 4.00, 3.81, 3.62], [4.40, 4.20, 4.00, 3.80], [4.63, 4.42, 4.21, 4.00], [4.89, 4.67, 4.44, 4.22], [5.18, 4.94, 4.71, 4.47], [5.50, 5.25, 5.00, 4.75],
    [5.87, 5.60, 5.33, 5.07], [6.29, 6.00, 5.71, 5.43], [6.77, 6.46, 6.15, 5.85], [7.33, 7.00, 6.67, 6.33], [8.00, 7.64, 7.27, 6.91], [8.80, 8.40, 8.00, 7.60],
    [9.78, 9.33, 8.89, 8.40], [11.00, 10.50, 10.00, 9.20], [12.57, 12.00, 11.43, 10.00], [14.67, 14.00, 13.33, 11.00], [17.60, 16.50, 15.00, 12.00], [21.00, 19.00, 17.00, 13.00]],
  // DT 34.ª: aplicacion gradual 2024-2033 del 2.º parrafo del art. 210.3 (pension por encima del limite): dt34[meses de anticipo - 1][anio - 2024][columna de cotizacion] (%)
  dt34s: [
    [0.776,0.762,0.746,0.732],
    [0.788,0.774,0.758,0.742],
    [0.802,0.786,0.77,0.754],
    [1.268,1.25,1.234,1.218],
    [1.284,1.27,1.248,1.23],
    [1.3,1.282,1.264,1.25],
    [1.77,1.75,1.732,1.712],
    [1.79,1.77,1.75,1.73],
    [1.814,1.792,1.772,1.75],
    [2.29,2.268,2.244,2.222],
    [2.318,2.294,2.272,2.248],
    [2.35,2.33,2.3,2.28],
    [2.838,2.81,2.784,2.758],
    [2.88,2.85,2.822,2.794],
    [2.928,2.896,2.87,2.84],
    [3.434,3.4,3.368,3.334],
    [3.5,3.464,3.428,3.392],
    [3.58,3.54,3.5,3.46],
    [4.128,4.084,4.04,3.99],
    [4.25,4.2,4.15,4.07],
    [4.408,4.35,4.294,4.15],
    [5.068,5.0,4.935,4.7],
    [5.36,5.25,5.1,4.8],
    [5.7,5.5,5.3,4.9]]
};
// dt34[meses-1][anio-2024][col]: interpolacion lineal entre el valor de 2024 (dt34s, 3 decimales) y el coeficiente pleno de 2033 (coef), redondeada a 2 decimales; reproduce la tabla del BOE celda a celda (verificado)
P.dt34 = P.coef.map(function (r, a) { return r.map(function (e, c) { var s = P.dt34s[a][c], o = []; for (var k = 0; k < 10; k++) o.push(Math.round((s + k * (e - s) / 9) * 100) / 100); return o; }); });
// transpone a [meses-1][anio][col]
P.dt34 = P.dt34.map(function (cols) { return cols[0].map(function (_, k) { return cols.map(function (col) { return col[k]; }); }); });

// Anio natural en el que cae el mes m (la edad actual se fija en la fecha de referencia: octubre de 2026).
function anioDe(m, ageM) { return P.refAnio + Math.floor((P.refMes + m - ageM) / 12); }
// Edad ordinaria en meses (art. 205.1.a y DT 7.ª): 65 si, con cotizacion continuada, se llega al periodo exigido; si no, la edad del cuadro.
function edadOrdinaria(ageM, cotM) {
  var m, y, c, um, ed, i;
  for (m = 780; m <= 804; m++) {
    y = anioDe(m, ageM); c = cotM + m - ageM;
    if (y >= 2027) { um = P.dt7Futuro[0]; ed = P.dt7Futuro[1]; }
    else if (y < 2013) { um = 0; ed = 780; }
    else { for (i = 0; i < P.dt7.length; i++) if (P.dt7[i][0] === y) { um = P.dt7[i][1]; ed = P.dt7[i][2]; } }
    if (m >= (c >= um ? 780 : ed)) return m;
  }
  return 804;
}
// Porcentaje de la base reguladora por meses cotizados (art. 210.1 y DT 9.ª); null si no llega a 15 anos.
function porcentaje(c, y) {
  var i, t, x, p;
  if (c < 180) return null;
  for (i = 0; i < P.dt9.length; i++) if (y >= P.dt9[i][0]) { t = P.dt9[i]; break; }
  x = c - 180; p = 50 + Math.min(x, t[1]) * t[2] + Math.max(0, x - t[1]) * t[3];
  return Math.min(p, 100);
}
// Pension mensual (14 pagas) al causarla en el mes m, o el motivo por el que no se puede.
function pensionAl(m, ord, ageM, cotM, br, g) {
  var c = cotM + m - ageM, y = anioDe(m, ageM), pc = porcentaje(c, y);
  if (pc === null) return { estado: "carencia" };
  var f = Math.pow(1 + g, (m - ageM) / 12), brn = br * f, mx = P.maxMes * f, tope = P.topeAnual * f, pb = brn * pc / 100, ant, col, p, d, yy, rem, extra, reg, sin, raw, comp, cf;
  if (m < ord) {
    ant = ord - m;
    if (ant > 24) return { estado: "antic24" };
    if (c < 420) return { estado: "antic35" };
    col = c < 462 ? 0 : (c < 498 ? 1 : (c < 534 ? 2 : 3));
    // Si la pension (BR x %) supera la maxima, el coeficiente se aplica sobre la maxima y de forma gradual segun el anio del hecho causante (DT 34.ª LGSS: 2024-2033); si no, el cuadro del art. 208.2.
    cf = pb > mx ? P.dt34[ant - 1][Math.min(Math.max(y, 2024), 2033) - 2024][col] : P.coef[ant - 1][col];
    p = Math.min(pb, mx) * (1 - cf / 100);
    if (p / f * 14 <= P.minBaja) return { estado: "minima" };
    return { estado: "ok", p: p, coefPct: cf, pctBase: pc, dt34: pb > mx && y < 2033 ? 1 : 0 };
  }
  if (m === ord) return { estado: "ok", p: Math.min(pb, mx), coefPct: 0, pctBase: pc };
  d = m - ord; extra = 0;
  if (cotM + ord - ageM >= 180) { yy = Math.floor(d / 12); rem = d - 12 * yy; extra = 4 * yy + (yy >= 2 && rem >= 7 ? 2 : 0); }
  if (pb >= mx) { reg = mx; sin = extra; }
  else { raw = brn * (pc + extra) / 100; if (raw <= mx) { reg = raw; sin = 0; } else { reg = mx; sin = pc + extra - mx / brn * 100; } }
  comp = Math.max(0, Math.min(sin / 100 * mx, tope / 14 - reg));
  return { estado: "ok", p: reg + comp, coefPct: 0, pctBase: pc, extraPct: extra, complemento: comp };
}
// Acumulado neto mes a mes desde `ini` hasta `hasta` (exclusive): 14 pagas = 14/12 por mes, revalorizacion cada enero.
function serieAcum(ini, p0, hasta, ageM, g, net) {
  var out = [], acc = 0, fac = 1, mm;
  for (mm = ini; mm < hasta; mm++) {
    if (mm > ini && (P.refMes + mm - ageM) % 12 === 0) fac *= 1 + g;
    acc += p0 * fac * 14 / 12 * net; out.push(acc);
  }
  return out;
}
// Edad ordinaria con la cotizacion REAL a la fecha elegida (sin seguir cotizando despues): art. 208.1.a puede medirse con ella, frente a la hipotetica del 208.2.
function ordinariaReal(m, ageM, cotM) {
  var y = anioDe(m, ageM), c = cotM + m - ageM, um, ed, i;
  if (y >= 2027) { um = P.dt7Futuro[0]; ed = P.dt7Futuro[1]; }
  else if (y < 2013) { um = 0; ed = 780; }
  else { for (i = 0; i < P.dt7.length; i++) if (P.dt7[i][0] === y) { um = P.dt7[i][1]; ed = P.dt7[i][2]; } }
  return c >= um ? 780 : ed;
}
function calcular(d) {
  var ageM = Math.round(d.edad * 12), cotM = Math.floor(d.cot * 12 + 1e-9), m = Math.round(d.eleg_a) * 12 + Math.round(d.eleg_m), endM = Math.round(d.fin * 12);
  var g = d.ipc / 100, net = 1 - d.irpf / 100, o = edadOrdinaria(ageM, cotM), res = { ordM: o, edadOrdinaria: o / 12, cotAlCausar: (cotM + m - ageM) / 12 };
  if (m < ageM) { res.estado = "pasado"; return res; }
  if (o < ageM) { res.estado = "ord_pasada"; return res; }
  var po = pensionAl(o, o, ageM, cotM, d.br, g);
  if (po.estado !== "ok") { res.estado = "carencia_ord"; return res; }
  var pe = pensionAl(m, o, ageM, cotM, d.br, g);
  res.estado = pe.estado; res.pensionOrdinaria = po.p;
  if (pe.estado !== "ok") return res;
  res.pensionElegida = pe.p; res.coefPct = pe.coefPct; res.extraPct = pe.extraPct || 0; res.complemento = pe.complemento || 0;
  res.dt34 = pe.dt34 || 0; res.ordRealM = m < o ? ordinariaReal(m, ageM, cotM) : o;
  res.mesesDiff = m - o; res.pctBase = pe.pctBase; res.pctBaseOrd = po.pctBase;
  res.avisoMinima = (m < o && pe.p / Math.pow(1 + g, (m - ageM) / 12) * 14 <= P.minAlta) ? 1 : 0;
  var A = serieAcum(m, pe.p, endM, ageM, g, net), B = serieAcum(o, po.p, endM, ageM, g, net);
  res.acumElegida = A.length ? A[A.length - 1] : 0; res.acumOrdinaria = B.length ? B[B.length - 1] : 0; res.diferencia = res.acumElegida - res.acumOrdinaria;
  res.equilibrioEdad = null;
  if (m !== o) {
    var tope = 1320, ear = m < o ? [m, pe.p] : [o, po.p], lat = m < o ? [o, po.p] : [m, pe.p];
    var E = serieAcum(ear[0], ear[1], tope, ageM, g, net), L = serieAcum(lat[0], lat[1], tope, ageM, g, net), k;
    for (k = lat[0]; k < tope; k++) if (L[k - lat[0]] >= E[k - ear[0]]) { res.equilibrioEdad = (k + 1) / 12; break; }
  }
  // Serie anual para el grafico: acumulado neto a cada edad entera desde el primer cobro hasta la edad final
  var s = [], a = Math.ceil(Math.min(m, o) / 12), eM;
  for (; a * 12 <= endM; a++) {
    eM = a * 12;
    s.push([a, (eM - 1 - m >= 0 && eM - 1 - m < A.length) ? A[eM - 1 - m] : 0, (eM - 1 - o >= 0 && eM - 1 - o < B.length) ? B[eM - 1 - o] : 0]);
  }
  res.serie = s;
  return res;
}
function eur(x) { return EM.eur(x); }
function edadTxt(y) {
  var m = Math.round(y * 12), a = Math.floor(m / 12), r = m - 12 * a;
  return a + " años" + (r ? " y " + r + (r === 1 ? " mes" : " meses") : "");
}
var IDS = ["edad", "cot", "br", "eleg_a", "eleg_m", "fin", "irpf", "ipc"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function aviso(msg) { EM.renderResult({ winner: "invalido", tone: "warn", verdict: msg, note: "<p>Esta herramienta compara tu pensión de jubilación a la edad que elijas con la de la edad ordinaria, solo para el Régimen General con carrera de cotización continuada. Para tu caso exacto usa el simulador de la Seguridad Social.</p>" }); }
function pintar() {
  var d = leer(), r;
  if (d.fin <= 0 || d.edad <= 0) return;
  r = calcular(d);
  var ordTxt = edadTxt(r.edadOrdinaria), elegTxt = edadTxt((Math.round(d.eleg_a) * 12 + Math.round(d.eleg_m)) / 12);
  if (r.estado === "pasado") return aviso("La edad de jubilación que eliges (" + elegTxt + ") es anterior a tu edad actual: elige una edad igual o mayor que la actual.");
  if (r.estado === "ord_pasada") return aviso("Con estos datos tu edad ordinaria de jubilación (" + ordTxt + ") ya ha pasado: la opción «ordinaria» sumaría pensiones de meses que ya no puedes cobrar y la comparación no sería válida. Esta herramienta es para quien aún no ha llegado a su edad ordinaria; si ya la has cumplido, consulta el simulador de la Seguridad Social.");
  if (r.estado === "carencia_ord") return aviso("Con estos datos no llegas a 15 años cotizados a la edad ordinaria (" + ordTxt + "), así que no se genera pensión de jubilación contributiva ordinaria. La herramienta no calcula este caso.");
  if (r.estado === "carencia") return aviso("A los " + elegTxt + " tendrías " + edadTxt(r.cotAlCausar) + " cotizados, menos de los 15 años que exige la pensión de jubilación (art. 205.1.b de la Ley General de la Seguridad Social). Elige una edad posterior.");
  if (r.estado === "antic24") return aviso("La jubilación anticipada por voluntad del interesado solo permite adelantarse hasta 24 meses respecto a tu edad ordinaria (" + ordTxt + ", art. 208.1.a): como pronto a los " + edadTxt(r.edadOrdinaria - 2) + ". Elige una edad posterior.");
  if (r.estado === "antic35") return aviso("La jubilación anticipada voluntaria exige 35 años de cotización efectiva (art. 208.1.b); a los " + elegTxt + " tendrías " + edadTxt(r.cotAlCausar) + " cotizados. Con menos, esta vía no está disponible.");
  if (r.estado === "minima") return aviso("La pensión resultante de anticipar a los " + elegTxt + " no superaría la pensión mínima de jubilación (art. 208.1.c): en ese caso la ley no permite esta modalidad. Elige una edad posterior o revisa la base reguladora.");
  var m = Math.round(d.eleg_a) * 12 + Math.round(d.eleg_m);
  if (d.fin * 12 <= Math.max(m, r.ordM)) return aviso("Pon una edad final posterior tanto a la edad de jubilación que eliges como a tu edad ordinaria (" + ordTxt + "): la comparación acumula pensiones hasta esa edad.");
  var ant = m < r.ordM, dem = m > r.ordM, nm = function (x) { return eur(x); };
  var eqTxt = r.equilibrioEdad === null ? null : edadTxt(r.equilibrioEdad), verdict, winner, big;
  if (!ant && !dem) {
    verdict = "A los " + ordTxt + " es tu edad ordinaria: no hay reducción ni incentivo. Tu pensión sería de " + nm(r.pensionOrdinaria) + " al mes en 14 pagas (bruta, en euros de ese año). Elige una edad anterior o posterior para compararla.";
    winner = "ordinaria";
  } else {
    var gana = Math.abs(r.diferencia) < 1 ? "empate" : (r.diferencia > 0 ? "elegida" : "ordinaria"), tail;
    winner = gana === "empate" ? "empate" : (gana === "ordinaria" ? "ordinaria" : (ant ? "anticipada" : "demorada"));
    if (ant) {
      tail = eqTxt === null ? "con estos datos la opción de cobrar más tarde no llega a igualar a la otra antes de los 110 años" : "a partir de los " + eqTxt + " la pensión a la edad ordinaria acumula más";
      verdict = "Anticipar a los " + elegTxt + " baja tu pensión de " + nm(r.pensionOrdinaria) + " a " + nm(r.pensionElegida) + " al mes (reducción del " + EM.num(r.coefPct, 2) + " % y menos meses cotizados): " + tail + ". ";
    } else {
      tail = eqTxt === null ? "con estos datos la opción de cobrar más tarde no llega a igualar a la otra antes de los 110 años" : "a partir de los " + eqTxt + " la pensión retrasada acumula más";
      verdict = "Retrasar a los " + elegTxt + " sube tu pensión de " + nm(r.pensionOrdinaria) + " a " + nm(r.pensionElegida) + " al mes (incentivo del " + EM.num(r.extraPct, 0) + " % y más meses cotizados): " + tail + ". ";
    }
    if (gana === "empate") verdict += "Si cobras hasta los " + d.fin + " años, ambas opciones acumulan lo mismo.";
    else verdict += "Si cobras hasta los " + d.fin + " años, con estos supuestos " + (gana === "elegida" ? (ant ? "anticipar" : "retrasar") : "jubilarte a la edad ordinaria") + " acumula " + nm(Math.abs(r.diferencia)) + " más; la cuenta solo compara pensiones, sin descontar el dinero en el tiempo ni el sueldo.";
  }
  var note = "";
  if (ant && r.ordRealM > r.ordM) note += "<p><strong>Atención:</strong> si dejas de cotizar al jubilarte a los " + elegTxt + ", con " + edadTxt(r.cotAlCausar) + " cotizados tu edad ordinaria sería " + edadTxt(r.ordRealM / 12) + " y no " + ordTxt + ". El art. 208.2 usa la cotización continuada hasta la edad ordinaria solo para calcular los coeficientes; para poder acceder (art. 208.1.a, hasta 24 meses antes de tu edad ordinaria) puede contar tu cotización real, y entonces quizá no puedas anticipar tanto o nada. Compruébalo en el simulador de la Seguridad Social.</p>";
  if (r.dt34) note += "<p>Tu pensión teórica supera la pensión máxima: el coeficiente de anticipación (" + EM.num(r.coefPct, 2) + " %) es el que la disposición transitoria 34.ª aplica de forma gradual entre 2024 y 2033 según el año de jubilación, no el del cuadro completo del art. 208.2, que rige desde 2033.</p>";
  if (r.avisoMinima) note += "<p><strong>Atención:</strong> tu pensión anticipada queda por debajo de la mínima de jubilación con cónyuge a cargo (" + eur(17592.4) + " al año en 2026). La ley exige que supere la mínima que te corresponde según tu situación familiar (art. 208.1.c); si no, no puedes anticipar. Compruébalo en la Seguridad Social.</p>";
  if (dem && r.extraPct === 0) note += "<p><strong>Sin incentivo:</strong> con estos datos no se genera el complemento por demora (hace falta haber reunido 15 años de cotización a la edad ordinaria, art. 210.2) o el retraso es menor de un año completo.</p>";
  if (dem && r.complemento > 0) note += "<p>Parte del incentivo supera el límite de la pensión máxima y se cobra como cantidad anual aparte (" + eur(r.complemento) + " al mes en 14 pagas, art. 210.2.a).</p>";
  if (m !== r.ordM) note += "<p><strong>Cómo se ha calculado:</strong> base reguladora de " + eur(d.br) + " (en euros de hoy, la misma para todas las edades) por el " + EM.num(r.pctBase, 2) + " % que dan " + edadTxt(r.cotAlCausar) + " cotizados" + (ant ? ", reducida por el coeficiente del art. 208.2 (columna de tu período cotizado)" : (r.extraPct ? ", más " + EM.num(r.extraPct, 0) + " puntos del incentivo de demora" : "")) + ". Las 14 pagas se reparten en 12 meses para el acumulado y la pensión se revaloriza cada enero un " + EM.num(d.ipc, 1) + " %.</p>";
  note += "<p><strong>Edad ordinaria con tus datos:</strong> " + ordTxt + " (calendario de la disposición transitoria 7.ª, suponiendo que sigues cotizando hasta jubilarte). La edad de equilibrio no es esperanza de vida: nadie sabe cuánto cobrará.</p>";
  note += "<p><strong>No incluye:</strong> otras vías de jubilación, trabajo compatible, complementos, regímenes especiales, la cantidad a tanto alzado del art. 210.2, descuento financiero ni tablas de mortalidad; IRPF solo como tipo medio. Para tu caso exacto, usa el simulador de la Seguridad Social.</p>";
  EM.renderResult({
    winner: winner, verdict: verdict, tone: !ant && !dem ? "info" : "ok",
    bigNumber: m === r.ordM || r.equilibrioEdad === null ? undefined : r.equilibrioEdad, bigLabel: "edad de equilibrio: a partir de ahí la opción que cobra más tarde acumula más", format: function (x) { return edadTxt(x); },
    line: m === r.ordM ? undefined : { caption: "Pensión acumulada neta por edad (euros nominales)", xLabel: "Edad", xFormat: function (a) { return a + " años"; }, yFormat: EM.eur,
      series: [{ label: "Elegida (" + elegTxt + ")", color: "a", points: r.serie.map(function (v) { return [v[0], v[1]]; }) }, { label: "Ordinaria (" + ordTxt + ")", color: "b", points: r.serie.map(function (v) { return [v[0], v[2]]; }) }] },
    barsLabel: "Pensión acumulada neta hasta los " + d.fin + " años",
    bars: [{ label: "Elegida (" + elegTxt + ")", value: Math.max(r.acumElegida, 0), color: "a" }, { label: "Ordinaria (" + ordTxt + ")", value: Math.max(r.acumOrdinaria, 0), color: "b" }],
    cols: ["Elegida", "Ordinaria"],
    rows: [
      ["Edad de jubilación", elegTxt, ordTxt],
      ["Pensión mensual al empezar (14 pagas, bruta)", eur(r.pensionElegida), eur(r.pensionOrdinaria)],
      ["Años cotizados al jubilarte", edadTxt(r.cotAlCausar), edadTxt(r.cotAlCausar - (m - r.ordM) / 12)],
      { label: "Acumulado neto hasta los " + d.fin + " años", values: [eur(r.acumElegida), eur(r.acumOrdinaria)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
