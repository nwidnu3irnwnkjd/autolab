// Jubilacion activa o dejar de trabajar (2026). Norma: LGSS (RDL 8/2015, consolidado a 31/07/2026) arts. 153, 205.1, 210, 214 (redaccion del RDL 11/2024, en vigor desde el 1-4-2025) y 310; DT 7.ª y 9.ª; RD 241/2026 (pension maxima). Parametros y fuentes en data/params.json (jubilacion_activa_2026).
var P = {
  maxMes: 3359.60, topeAnual: 61214.40, baseMax: 5101.20, minAnual: 13106.80,
  ordM: 780, carenciaM: 180, mesRef: 6,   // 65 anos; 15 anos de carencia (205.1.b); el mes del hecho causante se toma como julio para fijar el anio en que se cumple la edad ordinaria
  // DT 7.ª: [anio, meses cotizados para jubilarse a los 65, edad exigida en meses si no se llega]; desde 2027: 462 y 804
  dt7: [[2013, 423, 781], [2014, 426, 782], [2015, 429, 783], [2016, 432, 784], [2017, 435, 785], [2018, 438, 786], [2019, 441, 788], [2020, 444, 790], [2021, 447, 792], [2022, 450, 794], [2023, 453, 796], [2024, 456, 798], [2025, 459, 800], [2026, 459, 802]],
  dt7Futuro: [462, 804],
  escala: [45, 55, 65, 80, 100], conContrato: 75, sumaAnual: 5,   // art. 214.2 y 214.3: % de la pension segun anos completos de demora; +5 puntos cada 12 meses en activa
  solTrab: 0.02, solAut: 0.09, itTrab: 0.0025, itAut: 0.0156, cpAut: 0.013, genericos: 0.07,   // art. 153 (2 % del trabajador) y 310 (9 % del autonomo); desde la edad ordinaria solo IT (arts. 152 y 311, Orden PJC/297/2026 art. 32: 0,25 % del trabajador; autonomo 1,56 % IT + 1,30 % CP)
  reta: [[670, 653.59], [900, 718.95], [1166.7, 849.67], [1300, 950.98], [1500, 960.78], [1700, 960.78], [1850, 1143.79], [2030, 1209.15], [2330, 1274.51], [2760, 1356.21], [3190, 1437.91], [3620, 1519.61], [4050, 1601.31], [6000, 1732.03], [null, 1928.10]]
};
// Porcentaje de la base reguladora por meses cotizados (art. 210.1 y DT 9.ª): 2027 en adelante 248 meses al 0,19 y el resto al 0,18; 2023-2026, 49 al 0,21 y el resto al 0,19.
function porcentaje(c, y) {
  var x = c - 180, n1 = y >= 2027 ? 248 : 49, t1 = y >= 2027 ? 0.19 : 0.21, t2 = y >= 2027 ? 0.18 : 0.19;
  return Math.min(100, 50 + Math.min(x, n1) * t1 + Math.max(0, x - n1) * t2);
}
// Pension mensual (paga de 14) con `dm` meses de demora: 4 puntos por ano completo (+2 desde dos anos si sobran mas de 6 meses), tope art. 57 y exceso como cantidad anual (art. 210.2.a).
function pensionDemora(br, cotM, dm, y) {
  var pc = porcentaje(cotM, y), yy = Math.floor(dm / 12), rem = dm - 12 * yy, extra = 4 * yy + (yy >= 2 && rem >= 7 ? 2 : 0), pb = br * pc / 100, reg, sin, raw;
  if (pb >= P.maxMes) { reg = P.maxMes; sin = extra; }
  else { raw = br * (pc + extra) / 100; if (raw <= P.maxMes) { reg = raw; sin = 0; } else { reg = P.maxMes; sin = pc + extra - P.maxMes / br * 100; } }
  return reg + Math.max(0, Math.min(sin / 100 * P.maxMes, P.topeAnual / 14 - reg));
}
// Base de cotizacion mensual minima del tramo del RETA para un rendimiento neto mensual (rendimiento computable = rendimiento menos el 7 %; el tramo 3 reducido es exclusivo).
function baseReta(rend) {
  var r = rend > 0 ? (1 - P.genericos) * rend : 0, i;
  for (i = 0; i < P.reta.length; i++) if (P.reta[i][0] === null || (i === 2 ? r < P.reta[i][0] : r <= P.reta[i][0])) return P.reta[i][1];
}
// Ingreso mensual neto de cotizaciones, antes de IRPF: [en jubilacion activa, trabajando sin pension]. Desde la edad ordinaria solo se cotiza por IT (y CP el autonomo): arts. 152 y 311; la activa anade el 9 % de solidaridad.
function netos(s, propia) {
  if (propia) { var b = baseReta(s); return [s - (P.solAut + P.itAut + P.cpAut) * b, s - (P.itAut + P.cpAut) * b]; }
  var bc = Math.min(s, P.baseMax);
  return [s - (P.solTrab + P.itTrab) * bc, s - P.itTrab * bc];
}
// Edad ordinaria en meses (art. 205.1.a, DT 7.ª segun el anio en que se cumple): 65 anos si a esa edad se acreditan los meses exigidos; si no, el mes en que se completan con cotizacion continuada, hasta la edad del cuadro.
function edadOrdinaria(cot65M, anioHc, hc) {
  var m, y, um, ed, i, c;
  for (m = P.ordM; m <= 804; m++) {
    y = anioHc + Math.floor((P.mesRef + m - hc) / 12); c = cot65M + m - P.ordM;
    if (y >= 2027) { um = P.dt7Futuro[0]; ed = P.dt7Futuro[1]; }
    else if (y < 2013) { um = 0; ed = P.ordM; }
    else { for (i = 0; i < P.dt7.length; i++) if (P.dt7[i][0] === y) { um = P.dt7[i][1]; ed = P.dt7[i][2]; } }
    if (m >= (c >= um ? P.ordM : ed)) return m;
  }
  return 804;
}
function calcular(d) {
  var hc = Math.round(d.edad_a) * 12 + Math.round(d.edad_m), cotM = Math.floor(d.cot * 12 + 1e-9), n = Math.round(d.n), propia = d.tipo !== "ajena";
  var y = Math.round(d.anio), eo = edadOrdinaria(cotM - (hc - P.ordM), y, hc), res = { estado: 0, ordM: eo };
  if (hc < eo) { res.estado = 1; return res; }
  if (cotM - (hc - P.ordM) + eo - P.ordM < P.carenciaM) { res.estado = cotM >= P.carenciaM ? 3 : 2; return res; }
  var D = hc - eo, dY = Math.floor(D / 12), activa = D >= 12 ? 1 : 0, pin = Math.min(d.pension, P.maxMes), br = pin * 100 / porcentaje(cotM, y);
  var p = pensionDemora(br, cotM, D, y), p2 = pensionDemora(br, cotM + 12 * n, D + 12 * n, y + n), nt = netos(d.salario, propia), base = 0, t, pt, ta = 0, tb = 0, tc = 0, perd = 0, last = 0;
  if (activa) base = (d.tipo === "propia_contrata" && dY >= 1 && dY <= 3) ? P.conContrato : P.escala[Math.min(dY, 5) - 1];
  for (t = 0; t < 12 * n; t++) {
    pt = Math.min(100, base + P.sumaAnual * Math.floor(t / 12)); last = pt;
    if (activa) ta += p * pt / 100 * 14 / 12 + nt[0];
    perd += (1 - pt / 100) * p * 14 / 12;
    tb += p * 14 / 12; tc += nt[1];
  }
  res.demora = D; res.demoraAnios = dY; res.activa = activa; res.pension = p; res.pensionDemora = p2; res.ganancia = p2 - p;
  res.netoActiva = nt[0]; res.netoDemora = nt[1]; res.TB = tb; res.TC = tc; res.eq = null; res.umbral = null; res.hcM = hc;
  var best = activa ? Math.max(ta, tb) : tb, s;
  if (p2 - p > 1e-9) res.eq = (hc + 12 * n) / 12 + Math.max(0, best - tc) / ((p2 - p) * 14 / 12) / 12;
  if (activa) {
    res.pctInicial = base; res.pctFinal = last; res.TA = ta; res.dif = ta - tb; res.mensualA = ta / (12 * n);
    for (s = 0; s <= 40000; s++) if (netos(s, propia)[0] >= perd / (12 * n) - 1e-9) { res.umbral = s; break; }
  }
  return res;
}
function eur(x) { return EM.eur(x); }
function edadTxt(m) {
  var a = Math.floor(m / 12), r = m - 12 * a;
  return a + " años" + (r ? " y " + r + (r === 1 ? " mes" : " meses") : "");
}
var IDS = ["pension", "cot", "edad_a", "edad_m", "anio", "salario", "n"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.tipo = document.getElementById("tipo").value;
  return d;
}
function aviso(msg) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: msg, note: "<p>Esta herramienta compara la jubilación activa, dejar de trabajar y demorar la pensión solo en el Régimen General o el RETA, a partir de la edad ordinaria y sin jubilación anticipada ni parcial. Para tu pensión exacta usa el simulador de la Seguridad Social.</p>" }); }
var NO_MODELA = "<p><strong>No incluye:</strong> el IRPF (pensión y sueldo se suman en la misma escala, así que la ventaja de la activa baja), la elección de otra base de cotización, el complemento por mínimos (en la activa se pierde), la revalorización (euros de hoy), regímenes especiales y forales, funcionarios y Clases Pasivas (la activa es incompatible con un puesto en el sector público), jubilación anticipada, parcial o flexible y un cambio de tu base reguladora por seguir cotizando.</p>";
function pintar() {
  var d = leer(), r, ord, n, nm = eur;
  if (d.pension <= 0 || d.salario <= 0 || d.cot <= 0 || d.n < 1) { aviso("Revisa los datos: la pensión, el sueldo, los años cotizados y los años a trabajar deben ser mayores que 0."); return; }
  r = calcular(d); n = Math.round(d.n); ord = edadTxt(r.ordM);
  if (r.estado === 1) { aviso("Con " + EM.num(d.cot, 1) + " años cotizados al pedir la pensión, tu edad ordinaria de jubilación es " + ord + " y la edad que has puesto es anterior: sería una jubilación anticipada, que no es compatible con el trabajo (art. 214.1). Pon una edad igual o posterior a la ordinaria."); return; }
  if (r.estado === 2) { aviso("Con esos años cotizados no llegas a los 15 años de cotización que exige la pensión de jubilación (art. 205.1.b), ni a tu edad ordinaria (" + ord + ") ni al pedirla: sin esos 15 años no hay pensión contributiva de jubilación ni jubilación activa."); return; }
  if (r.estado === 3) { aviso("Con esos años cotizados reúnes los 15 años después de tu edad ordinaria (" + ord + "). La jubilación activa sigue siendo posible: el año mínimo de espera se cuenta desde que reúnes los 15 años (art. 214.1, última frase). Lo que no hay es complemento por demora (art. 210.2, que exige los 15 años a la edad ordinaria). La herramienta no calcula este caso."); return; }
  var note = "", pin = Math.min(d.pension, P.maxMes), verdict, winner, gan = 0, rel, mA, mB = r.TB / (12 * n), mC = r.TC / (12 * n), propia = d.tipo !== "ajena";
  var eqTxt = r.eq === null ? null : edadTxt(Math.round(r.eq * 12));
  var dem = "Demorar la pensión " + n + (n === 1 ? " año" : " años") + " más (sin cobrarla y cotizando) la sube de " + nm(r.pension) + " a " + nm(r.pensionDemora) + " al mes en 14 pagas y " + (eqTxt === null ? "no llega a recuperar lo que dejas de cobrar" : "recupera lo no cobrado a partir de los " + eqTxt) + ".";
  if (!r.activa) {
    winner = "sin_activa";
    verdict = "Con tus datos todavía no puedes acogerte a la jubilación activa: pides la pensión " + edadTxt(r.demora) + " después de tu edad ordinaria (" + ord + ") y la ley exige al menos un año (art. 214.1); la primera edad posible es " + edadTxt(r.ordM + 12) + ". Mientras tanto, jubilarte del todo da " + nm(mB) + " al mes y seguir trabajando " + n + (n === 1 ? " año" : " años") + " sin cobrar la pensión, " + nm(mC) + " al mes de sueldo neto; " + dem;
  } else {
    mA = r.mensualA; rel = Math.abs(r.dif) / Math.max(r.TA, r.TB);
    gan = rel < 0.05 ? 0 : (r.dif > 0 ? 1 : -1);
    winner = gan === 0 ? "empate" : (gan > 0 ? "activa" : "jubilarse");
    var base = "cobrarías de media " + nm(mA) + " al mes con la activa (" + r.pctInicial + " % de la pensión de " + nm(r.pension) + " más " + nm(r.netoActiva) + " de sueldo neto de cotizaciones) frente a " + nm(mB) + " si dejas de trabajar y cobras la pensión íntegra";
    if (gan === 0) verdict = "Con tus datos, empate práctico entre la jubilación activa y jubilarte del todo (" + nm(Math.abs(r.dif)) + " de diferencia en " + n + (n === 1 ? " año" : " años") + ", menos del 5 %): " + base + ". " + dem;
    else if (gan > 0) verdict = "Con tus datos, gana la jubilación activa por " + nm(r.dif) + " en " + n + (n === 1 ? " año" : " años") + ": " + base + ". La activa gana a partir de un sueldo neto de cotizaciones de " + nm(r.umbral === null ? 0 : r.umbral) + " al mes. " + dem;
    else verdict = "Con tus datos, gana dejar de trabajar y cobrar la pensión íntegra por " + nm(-r.dif) + " en " + n + (n === 1 ? " año" : " años") + ": " + base + ". Tu sueldo no compensa la parte de pensión que dejas de cobrar; la activa empezaría a ganar con un sueldo de " + nm(r.umbral === null ? 0 : r.umbral) + " al mes. " + dem;
  }
  if (d.pension > P.maxMes) note += "<p>La pensión que has puesto supera la máxima de " + eur(P.maxMes) + " al mes (2026): se ha limitado a esa cifra; el incentivo por demora por encima del límite se cobra aparte como cantidad anual.</p>";
  note += "<p><strong>Cómo sale:</strong> tu edad ordinaria con estos años cotizados es " + ord + " (art. 205.1.a y disposición transitoria 7.ª, según el año en que la cumples: en 2026, 65 años con 38 años y 3 meses cotizados y 66 años y 10 meses si no; desde 2027, 65 con 38 años y 6 meses y 67 si no) y pides la pensión " + edadTxt(r.demora) + " más tarde (" + r.demoraAnios + (r.demoraAnios === 1 ? " año completo" : " años completos") + " de demora). La pensión de " + nm(r.pension) + " ya incluye el complemento por demora (4 puntos por año completo, art. 210.2.a)" + (r.activa ? "; la activa paga " + (d.tipo === "propia_contrata" && r.demoraAnios >= 1 && r.demoraAnios <= 3 ? "el 75 % porque contratas a un trabajador indefinido (art. 214.3)" : "el " + P.escala[Math.min(r.demoraAnios, 5) - 1] + " % por esos años de demora (art. 214.2)") + ", y sube 5 puntos por cada 12 meses seguidos en activa hasta el 100 %: " + r.pctFinal + " % en el último año de los " + n + "." : ".") + "</p>";
  note += "<p><strong>Cotización:</strong> desde la edad ordinaria, sin pensión, solo cotizas por incapacidad temporal" + (propia ? " y contingencias profesionales (arts. 311 y Orden PJC/297/2026: " + EM.num(P.itAut * 100, 2) + " % de IT más " + EM.num(P.cpAut * 100, 2) + " % de contingencias profesionales sobre la base mínima de tu tramo del RETA)" : " (art. 152: " + EM.num(P.itTrab * 100, 2) + " % a cargo del trabajador)") + ". En la activa se añade la cotización de solidaridad del 9 %, que no genera prestaciones" + (propia ? " (art. 310: la pagas entera tú)" : " (art. 153: 7 % la empresa y 2 % tú)") + ". Tu sueldo neto pasa de " + nm(r.netoDemora) + " sin pensión a " + nm(r.netoActiva) + " al mes en la activa.</p>";
  if (pin * 14 < P.minAnual) note += "<p><strong>Complemento por mínimos:</strong> tu pensión (" + eur(pin * 14) + " al año) está por debajo de la mínima de " + eur(P.minAnual) + " al año. Si cumples los límites de ingresos, dejando de trabajar podrías cobrar el complemento; en la activa se pierde (art. 214.6). No se suma aquí, así que jubilarte del todo puede salir mejor de lo que indica el resultado.</p>";
  note += NO_MODELA;
  EM.renderResult({
    winner: winner, verdict: verdict, tone: winner === "sin_activa" ? "info" : "ok",
    bigNumber: r.activa ? r.dif : undefined, bigLabel: "diferencia en " + n + (n === 1 ? " año" : " años") + " (activa menos jubilarte del todo, antes de IRPF)", format: eur,
    barsLabel: "Ingresos acumulados netos de cotizaciones en " + n + (n === 1 ? " año" : " años") + " (antes de IRPF)",
    bars: (r.activa ? [{ label: "Jubilación activa", value: Math.max(r.TA, 0), color: "a" }] : []).concat([{ label: "Jubilarte del todo", value: Math.max(r.TB, 0), color: "b" }, { label: "Demorar la pensión", value: Math.max(r.TC, 0), color: "c" }]),
    cols: ["Activa", "Jubilarte del todo", "Demorar"],
    rows: [
      ["Pensión al mes (14 pagas)", r.activa ? eur(r.pension * r.pctInicial / 100) + " (" + r.pctInicial + " %)" : "no disponible", eur(r.pension), "0 € (hasta cobrarla)"],
      ["Sueldo neto de cotizaciones al mes", eur(r.netoActiva), "0 €", eur(r.netoDemora)],
      ["Ingreso mensual medio en " + n + (n === 1 ? " año" : " años"), r.activa ? eur(r.mensualA) : "no disponible", eur(mB), eur(mC)],
      { label: "Acumulado en " + n + (n === 1 ? " año" : " años"), values: [r.activa ? eur(r.TA) : "no disponible", eur(r.TB), eur(r.TC)], strong: true },
      ["Pensión íntegra al dejar de trabajar", eur(r.pension), eur(r.pension), eur(r.pensionDemora)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
