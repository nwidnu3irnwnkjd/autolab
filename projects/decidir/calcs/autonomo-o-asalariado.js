// Autonomo o asalariado (2026). Parametros generados desde data/params.json (irpf_2026 y autonomo_2026; fuentes y fechas alli).
// est: escala estatal general; minE: minimo del contribuyente y de descendientes estatales; ccaa: escala general y minimos de cada comunidad (min null = estatales).
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": {"c": 5790, "d": [2510, 2820, 4170, 4700]}, "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": {"c": 6105, "d": [2640, 2970, 4400, 4950]}, "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": {"c": 5550, "d": [2400, 2970, 4400, 4950]}, "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": {"c": 5606, "d": [2424, 2727, 4040, 4545]}, "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": {"c": 5789, "d": [2503, 2816, 4172, 4694]}, "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": {"c": 5956.65, "d": [2575.85, 2897.83, 4400, 4950]}, "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": {"c": 6105, "d": [2640, 2970, 4400, 4950]}, "orient": false}}, "reta": [["reducida", 670, 653.59, 718.94], ["reducida", 900, 718.95, 900.0], ["reducida", 1166.7, 849.67, 1166.7], ["general", 1300, 950.98, 1300], ["general", 1500, 960.78, 1500], ["general", 1700, 960.78, 1700], ["general", 1850, 1143.79, 1850], ["general", 2030, 1209.15, 2030], ["general", 2330, 1274.51, 2330], ["general", 2760, 1356.21, 2760], ["general", 3190, 1437.91, 3190], ["general", 3620, 1519.61, 3620], ["general", 4050, 1601.31, 4050], ["general", 6000, 1732.03, 5101.2], ["general", null, 1928.1, 5101.2]], "sol": [[5101.2, 5611.32, 0.96, 0.19], [5611.32, 7651.8, 1.04, 0.21], [7651.8, null, 1.22, 0.24]], "wInd": 6.5, "wTemp": 6.55, "eInd": 30.65, "eTemp": 31.85, "tipoReta": 0.315, "genericos": 0.07, "djPct": 0.05, "djMax": 2000};
var SMI = 17094, BMAX = 5101.20, DESC_E = [2400, 2700, 4000, 4500];
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function minimo(n, m) {
  var t = m ? m.c : 5550, d = m ? m.d : DESC_E, i;
  for (i = 0; i < n; i++) t += d[Math.min(i, 3)];
  return t;
}
function cuotaBase(bg, n, cc) {
  return Math.max(0, escala(bg, P.est) - escala(minimo(n, null), P.est)) + Math.max(0, escala(bg, cc.esc) - escala(minimo(n, cc.min), cc.esc));
}
function red20(n) {
  if (n >= 19747.5) return 0;
  if (n <= 14852) return 7302;
  if (n <= 17673.52) return 7302 - 1.75 * (n - 14852);
  return Math.max(0, 2364.34 - 1.14 * (n - 17673.52));
}
function da61(rit) {
  if (rit >= 20048.45) return 0;
  return rit <= 17094 ? 590.89 : 590.89 - 0.2 * (rit - 17094);
}
// Cotizacion adicional de solidaridad mensual (empresa, trabajador).
function solidaridad(r) {
  var s = [0, 0], i, t, x;
  for (i = 0; i < P.sol.length; i++) {
    t = P.sol[i]; x = Math.max(0, Math.min(r, t[1] === null ? Infinity : t[1]) - t[0]);
    s[0] += x * t[2] / 100; s[1] += x * t[3] / 100;
  }
  return s;
}
function ssAsalariado(bruto, indef) {
  var r = bruto / 12, base = Math.min(r, BMAX), s = solidaridad(r);
  var wt = (indef ? P.wInd : P.wTemp) / 100, et = (indef ? P.eInd : P.eTemp) / 100;
  return { trab: 12 * (base * wt + s[1]), emp: 12 * (base * et + s[0]) };
}
function irpfAsalariado(bruto, ssw, n, cc) {
  var neto = bruto - ssw, otros = Math.min(2000, Math.max(neto, 0)), rn = Math.max(0, neto - otros - red20(neto));
  var ci = cuotaBase(rn, n, cc);
  return Math.max(0, ci - Math.min(da61(bruto), ci));
}
// RETA: base minima mensual del tramo que corresponde al rendimiento computable mensual R (tabla reducida si R < 1.166,70).
function tramoReta(R) {
  var i, t;
  for (i = 0; i < P.reta.length; i++) {
    t = P.reta[i];
    if (t[1] === null || (i === 2 ? R < t[1] : R <= t[1])) return { n: i, base: t[2], max: t[3], tabla: t[0] };
  }
}
function cuotaReta(C) { return 12 * tramoReta(C > 0 ? (1 - P.genericos) * C / 12 : 0).base * P.tipoReta; }
function dj(N) { return Math.min(P.djMax, P.djPct * Math.max(N, 0)); }
// Punto fijo: la cuota depende del rendimiento computable, que depende de la deduccion de dificil justificacion, que depende de la cuota.
function ssAutonomo(I, G) {
  var s = 0, k, c;
  for (k = 0; k < 60; k++) { c = cuotaReta(I - G - dj(I - G - s)); if (Math.abs(c - s) < 1e-9) break; s = c; }
  return s;
}
function autonomo(I, G, n, cc) {
  var s = ssAutonomo(I, G), N = I - G - s, rn = N - dj(N), r3 = Math.max(rn, 0), red = 0;
  if (r3 > 0 && r3 < 12000) red = Math.min(r3 <= 8000 ? 1620 : 1620 - 0.405 * (r3 - 8000), r3);
  var irpf = cuotaBase(Math.max(rn - red, 0), n, cc);
  return { ss: s, irpf: irpf, neto: I - G - s - irpf, N: N };
}
function calcular(d) {
  var cc = P.ccaa[d.ccaa], n = Math.round(+d.hijos || 0), indef = d.contrato !== "temp", G = Math.max(+d.gastos || 0, 0);
  var sa = ssAsalariado(d.bruto, indef), ir = irpfAsalariado(d.bruto, sa.trab, n, cc), na = d.bruto - sa.trab - ir;
  var a = autonomo(d.factura, G, n, cc), coste = d.bruto + sa.emp;
  // Facturacion a partir de la cual el neto del autonomo alcanza el del asalariado y ya no baja de el: el neto cae en cada salto de tramo de la cuota y vuelve a subir,
  // asi que se barre de 10 en 10 EUR hasta 10.000 EUR despues del primer cruce, se toma el ultimo punto por debajo y se afina por biseccion.
  var I = Math.floor(Math.max(0, na + G + 2400) / 10) * 10, lastBelow = null, first = null, fe = null, m, lo, hi, j;
  while (I <= 2000000) {
    if (autonomo(I, G, n, cc).neto >= na) { if (first === null) first = I; }
    else { lastBelow = I; if (first !== null && I > first + 10000) break; }
    if (first !== null && I > first + 10000) break;
    I += 10;
  }
  if (first !== null) {
    lo = lastBelow === null ? Math.max(0, first - 10) : lastBelow; hi = lo + 10;
    if (autonomo(hi, G, n, cc).neto < na) hi = first;
    for (j = 0; j < 60; j++) { m = (lo + hi) / 2; if (autonomo(m, G, n, cc).neto >= na) hi = m; else lo = m; }
    fe = hi;
  }
  var ac = autonomo(coste, G, n, cc), dif = a.neto - na, tr = tramoReta(a.N > 0 ? (1 - P.genericos) * (d.factura - G - dj(a.N)) / 12 : 0);
  return {
    netoAsalariado: na, ssTrabajador: sa.trab, irpfAsalariado: ir, costeEmpresa: coste, ssEmpresa: sa.emp,
    netoAutonomo: a.neto, cuotaReta: a.ss, irpfAutonomo: a.irpf, facturaIgual: fe, netoAutonomoAlCoste: ac.neto,
    diferencia: dif, ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "autonomo" : "asalariado"),
    baseMensual: a.ss / 12 / P.tipoReta, cuotaMensual: a.ss / 12, tabla: tr.tabla, tramo: tr.n, baseMax: d.bruto / 12 > BMAX ? 1 : 0,
    solidaridad: d.bruto / 12 > BMAX ? 1 : 0, orientativo: cc.orient ? 1 : 0, ccaaNombre: cc.n
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["bruto", "factura", "gastos", "hijos"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; d.contrato = document.getElementById("contrato").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.bruto < SMI) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Introduce un salario bruto anual de al menos " + eur(SMI) + " (salario mínimo de 2026 en 14 pagas): por debajo, las bases mínimas de cotización y las reducciones cambian y esta calculadora no las modela.",
      note: "<p>Esta herramienta compara tu sueldo como asalariado a jornada completa con lo que quedaría como autónomo.</p>" });
    return;
  }
  var r = calcular(d), nm = function (x) { return eur(x / 12); };
  var verdict;
  if (r.facturaIgual === null) verdict = "Con estos datos no se alcanza el neto de asalariado con ninguna facturación razonable.";
  else {
    var cmp;
    if (r.ganador === "empate") cmp = "Con " + eur(d.factura) + " quedarías igual.";
    else if (r.ganador === "autonomo") cmp = "Con " + eur(d.factura) + " ganarías " + eur(r.diferencia) + " más al año" + (d.factura < r.facturaIgual ? ", aunque estás justo antes de un cambio de tramo de la cuota: si facturas algo más, la cuota sube y podrías quedar por debajo del asalariado hasta llegar a esa cifra." : ".");
    else cmp = "Con " + eur(d.factura) + " ganarías " + eur(-r.diferencia) + " menos al año.";
    verdict = "Para quedarte con lo mismo que como asalariado (" + eur(r.netoAsalariado) + " netos al año con " + eur(d.bruto) + " brutos), como autónomo, a partir de " + eur(r.facturaIgual) + " al año sin IVA, con " + eur(d.gastos) + " de gastos, cobras siempre lo mismo o más (en algunas franjas estrechas justo antes de esa cifra ya puedes ganar más). " + cmp;
  }
  var note = "";
  if (r.orientativo) note += "<p><strong>Cifras autonómicas orientativas:</strong> para " + r.ccaaNombre + " alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»).</p>";
  if (d.factura - d.gastos <= 0) note += "<p><strong>Atención:</strong> con estos gastos y facturación el autónomo no tiene beneficio y aun así paga la cuota mínima de la Seguridad Social.</p>";
  note += "<p><strong>Lectura:</strong> tu empresa gasta " + eur(r.costeEmpresa) + " al año en ti (bruto más Seguridad Social a cargo de la empresa, sin accidentes de trabajo). Un autónomo que facture esa misma cifra se quedaría con " + eur(r.netoAutonomoAlCoste) + " netos frente a tus " + eur(r.netoAsalariado) + " como asalariado. Facturar " + eur(r.facturaIgual === null ? 0 : r.facturaIgual) + " equivale a " + eur(r.facturaIgual === null ? 0 : r.facturaIgual / 12) + " al mes y a " + (r.facturaIgual === null ? "–" : EM.num(100 * r.facturaIgual / d.bruto, 0) + " %") + " de tu bruto.</p>";
  note += "<p>Como autónomo, con tu facturación y gastos, cotizarías por la base mínima de tu tramo (" + eur(r.baseMensual) + " al mes, tabla " + r.tabla + "): " + eur(r.cuotaMensual) + " al mes de cuota. Puedes elegir una base mayor dentro del tramo, que sube la cuota y la pensión futura; aquí no se modela.</p>";
  if (r.baseMax) note += "<p>Tu sueldo supera la base máxima de cotización (" + eur(5101.2) + " al mes): el exceso solo paga la cotización adicional de solidaridad, ya incluida.</p>";
  note += "<p><strong>No incluye:</strong> IVA, sociedad, tarifa plana (Ley 20/2007, art. 38 ter) ni bonificaciones de nuevos autónomos, reducción del 20 % del IRPF del primer año con beneficios y del siguiente (art. 32.3), deducciones autonómicas, ni lo que cambia en prestaciones (paro, baja, jubilación: cotizar distinto da derechos distintos). Supone estimación directa simplificada y que el sueldo y la facturación son de todo el año. Si trabajas para un único cliente no vinculado y cumples los requisitos del art. 32.2 de la Ley del IRPF (gastos ≤ 30 %, ≥ 70 % de ingresos con retención…), tienes una reducción mayor que el 5 % (2.000 € y hasta 6.498 € más con rendimientos bajos) y la facturación necesaria sería unos 250-500 € menor.</p>";
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: r.ganador === "asalariado" || r.ganador === "empate" ? "warn" : "ok",
    bigNumber: r.facturaIgual === null ? undefined : r.facturaIgual, bigLabel: "al año sin IVA para cobrar lo mismo que como asalariado", format: eur,
    barsLabel: "Neto anual después de Seguridad Social e IRPF",
    bars: [{ label: "Asalariado" + (r.ganador === "asalariado" ? " (gana)" : ""), value: Math.max(r.netoAsalariado, 0), color: "a" },
           { label: "Autónomo" + (r.ganador === "autonomo" ? " (gana)" : ""), value: Math.max(r.netoAutonomo, 0), color: "b" }],
    cols: ["Asalariado", "Autónomo"],
    rows: [
      ["Ingresos", eur(d.bruto), eur(d.factura)],
      ["Gastos del negocio", "–", eur(d.gastos)],
      ["Seguridad Social a tu cargo", eur(r.ssTrabajador), eur(r.cuotaReta)],
      ["IRPF", eur(r.irpfAsalariado), eur(r.irpfAutonomo)],
      { label: "Neto al año", values: [eur(r.netoAsalariado), eur(r.netoAutonomo)], strong: true },
      ["Neto al mes (÷ 12)", nm(r.netoAsalariado), nm(r.netoAutonomo)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
