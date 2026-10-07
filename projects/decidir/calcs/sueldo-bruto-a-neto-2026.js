// Sueldo bruto a neto 2026. Parametros generados desde data/params.json -> irpf_2026, retencion_irpf_nomina_2026, autonomo_2026.general y sueldo_bruto_neto_2026 (fuentes y fechas alli).
// Reutiliza escalas, minimos, art. 20, DA 61.ª, retencion (RIRPF 80-86) y cotizacion de comparar-ofertas-de-trabajo-neto-real y retencion-irpf-nomina-subir-o-no (ya verificadas); anade el tipo minimo del 2 % (RIRPF 86.2), la cotizacion temporal y el neto por mes en 12 y 14 pagas.
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "min": [5550, [2400, 2700, 4000, 4500], 2800], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": [5790, [2510, 2820, 4170, 4700], 2920], "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": [6105, [2640, 2970, 4400, 4950], 3080], "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": [5550, [2400, 2970, 4400, 4950], 2800], "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": [5606, [2424, 2727, 4040, 4545], 2828], "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": [5789, [2503, 2816, 4172, 4694], 2920], "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": [5956.65, [2575.85, 2897.83, 4400, 4950], 3005.16], "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": [6105, [2640, 2970, 4400, 4950], 3080], "orient": false}}, "ret": [[0, 19], [12450, 24], [20200, 30], [35200, 37], [60000, 45], [300000, 47]], "lim81": [15876, 16342, 16867], "cap": [35200, 43], "r600": 600, "g": 2000, "a20": [14852, 17673.52, 19747.5, 7302, 1.75, 2364.34, 1.14], "da": [590.89, 17094, 20048.45, 0.2], "bmax": 5101.2, "w": [6.5, 6.55], "sol": [[5101.2, 5611.32, 0.96, 0.19], [5611.32, 7651.8, 1.04, 0.21], [7651.8, null, 1.22, 0.24]], "min2": 2, "smi": 17094, "obl": 22000, "pasos": [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2800, 3000, 3200, 3400, 3500, 3600, 3800, 4000]};
function escala(x, esc) {
  var t = 0, i, hi;
  for (i = 0; i < esc.length; i++) { hi = i + 1 < esc.length ? esc[i + 1][0] : Infinity; if (x > esc[i][0]) t += (Math.min(x, hi) - esc[i][0]) * esc[i][1] / 100; }
  return t;
}
function art20(rn) {
  var a = P.a20;
  return rn <= a[0] ? a[3] : rn <= a[1] ? a[3] - a[4] * (rn - a[0]) : rn < a[2] ? a[5] - a[6] * (rn - a[1]) : 0;
}
function minimo(m, n, m3) {
  var s = 0, i; for (i = 0; i < n; i++) s += m[1][Math.min(i, 3)];
  return m[0] + s + m3 * m[2];
}
// Cotizacion anual del trabajador: tipo (6,50 % indefinido, 6,55 % temporal) sobre la base mensual topada, mas solidaridad sobre el exceso (Orden PJC/297/2026).
function ssTrab(R, temp) {
  var m = R / 12, base = Math.min(m, P.bmax), s = 0, i, t, x;
  for (i = 0; i < P.sol.length; i++) { t = P.sol[i]; x = Math.max(0, Math.min(m, t[1] === null ? Infinity : t[1]) - t[0]); s += x * t[3] / 100; }
  return 12 * (base * P.w[temp ? 1 : 0] / 100 + s);
}
// Tipo de retencion de la nomina (RIRPF 80-86), situacion «otras situaciones» del art. 81; menos1: contrato temporal de menos de un ano (tipo minimo 2 %, sin limite del art. 81).
function tipoRet(R, S, n, m3, menos1) {
  var lim = P.lim81[Math.min(n, 2)], rn = R - S, g = Math.min(P.g, rn), base = Math.max(0, rn - g - art20(rn) - (n >= 3 ? P.r600 : 0)), mn = minimo(P.min, n, m3), t = 0, c;
  if (menos1 || R > lim) {
    if (base - mn > 0) {
      c = Math.max(0, escala(base, P.ret) - escala(mn, P.ret));
      if (R <= P.cap[0]) c = Math.min(c, P.cap[1] / 100 * Math.max(0, R - lim));
      t = Math.round(c / R * 10000 + 1e-7) / 100;
    }
  }
  return menos1 ? Math.max(t, P.min2) : t;
}
function calcular(d) {
  var Req = +d.bruto || 0, meses = Math.floor(+d.meses || 0), menos = d.contrato === "temp1", R = menos ? Req * meses / 12 : Req, n = Math.floor(+d.hijos || 0), m3 = Math.floor(+d.menores3 || 0), con = d.contrato, cc = P.ccaa[d.ccaa], temp = con === "temp1" || con === "temp2";
  if (!(Req > 0) || !cc || m3 > n || n > 10 || (menos && (meses < 1 || meses > 11))) return { bloqueado: 1, motivo: !(Req > 0) ? 1 : (!cc ? 2 : (menos && (meses < 1 || meses > 11) && !(m3 > n || n > 10) ? 4 : 3)), ss: 0, tipo: 0, ret: 0, neto: 0, netoMes12: 0, netoMesNormal14: 0, netoMesExtra14: 0, irpfFinal: 0, netoFinal: 0, difRenta: 0 };
  var S = ssTrab(Req, temp) * (menos ? meses / 12 : 1), rn = R - S, tipo = tipoRet(R, S, n, m3, con === "temp1"), ret = R * tipo / 100, neto = R - S - ret, p = R / 14;
  var g = Math.min(P.g, rn), bf = Math.max(0, rn - g - art20(rn)), mnE = minimo(P.min, n, m3), mnA = minimo(cc.min || P.min, n, m3);
  var ci = Math.max(0, escala(bf, P.est) - escala(mnE, P.est)) + Math.max(0, escala(bf, cc.esc) - escala(mnA, cc.esc)), da = 0, irpf;
  if (R < P.da[2]) da = R <= P.da[1] ? P.da[0] : P.da[0] - P.da[3] * (R - P.da[1]);
  irpf = ci - Math.min(da, ci);
  return { bloqueado: 0, motivo: 0, ss: S, tipo: tipo, ret: ret, neto: neto, netoMes12: neto / (menos ? meses : 12), netoMesNormal14: menos ? neto / meses : p * (1 - tipo / 100) - S / 12, netoMesExtra14: menos ? neto / meses : 2 * p * (1 - tipo / 100) - S / 12,
    irpfFinal: irpf, netoFinal: R - S - irpf, difRenta: ret - irpf, cuotaPorPaga: p, bajoSmi: Req < P.smi ? 1 : 0, sobreBase: Req / 12 > P.bmax ? 1 : 0, brutoAnio: R, meses: menos ? meses : 12, noObligado: R <= P.obl ? 1 : 0, orientativo: cc.orient ? 1 : 0,
    temporal: temp ? 1 : 0, menos1: con === "temp1" ? 1 : 0, limite81: P.lim81[Math.min(n, 2)], ccaaNombre: cc.n, pagas: +d.pagas === 12 ? 12 : 14 };
}
// Tabla fija: bruto por paga (P.pasos) en 12 y en 14 pagas, con el contrato, la comunidad y los hijos de d.
function tablaSueldo(d) {
  var c = d.contrato === "temp1" ? "temp2" : d.contrato; // la tabla es anual: un temporal de menos de un año se muestra como de año completo
  return P.pasos.map(function (m) {
    var a = calcular({ bruto: 12 * m, pagas: 12, contrato: c, ccaa: d.ccaa, hijos: d.hijos, menores3: d.menores3 }), b = calcular({ bruto: 14 * m, pagas: 14, contrato: c, ccaa: d.ccaa, hijos: d.hijos, menores3: d.menores3 });
    return { m: m, bruto12: 12 * m, tipo12: a.tipo, neto12: a.netoMes12, bruto14: 14 * m, tipo14: b.tipo, normal14: b.netoMesNormal14, extra14: b.netoMesExtra14 };
  });
}
// Filas HTML de la tabla (la misma cadena que ops/gen_tabla_sueldo.py escribe en el HTML estatico; EM.num formatea).
function htmlTabla(d) {
  return tablaSueldo(d).map(function (r) {
    var c = function (v) { return '<td class="n">' + v + '</td>'; };
    return '<tr id="bruto-' + r.m + '"><th scope="row">' + EM.num(r.m, 0) + '</th>' + c(EM.num(r.neto12, 0)) + c(EM.num(r.normal14, 0)) + c(EM.num(r.extra14, 0)) + c(EM.num(r.tipo12, 2) + ' %') + c(EM.num(r.tipo14, 2) + ' %') + c(EM.num(r.bruto12, 0)) + c(EM.num(r.bruto14, 0)) + '</tr>';
  }).join("");
}
function eur(x) { return EM.eur(x); }
function pct(x) { return EM.num(x, 2) + " %"; }
var IDS = ["bruto", "pagas", "meses", "hijos", "menores3"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; d.contrato = document.getElementById("contrato").value; return d;
}
function pintarTabla(d) {
  var tb = document.getElementById("tabla-sueldo-cuerpo"), cap = document.getElementById("tabla-sueldo-datos");
  if (!tb) return;
  var cc = P.ccaa[d.ccaa], n = Math.floor(d.hijos), m3 = Math.floor(d.menores3);
  if (!cc || m3 > n || n > 10) return;
  tb.innerHTML = htmlTabla(d);
  if (cap) cap.textContent = "Calculada para " + cc.n + ", " + (d.contrato === "indef" ? "contrato indefinido" : d.contrato === "temp1" ? "contrato temporal (la tabla es de año completo)" : "contrato temporal de un año o más") + " y " + n + (n === 1 ? " hijo" : " hijos") + " (la de arriba se recalcula con tus datos).";
}
function pintar() {
  var d = leer(), r = calcular(d), nota = "";
  pintarTabla(d);
  if (r.bloqueado) {
    var foral = r.motivo === 2;
    EM.renderResult({ winner: "bloqueado-" + r.motivo, tone: "warn",
      verdict: r.motivo === 1 ? "Escribe tu sueldo bruto anual (el total de las pagas)." : r.motivo === 4 ? "Con un contrato temporal de menos de un año, escribe los meses de contrato en 2026 (de 1 a 11)." : foral ? "Esta calculadora no cubre el País Vasco ni Navarra: tienen su propio IRPF y sus propias retenciones." : "Los hijos menores de 3 años no pueden ser más que el total de hijos (y el máximo es 10).",
      note: foral ? "<p>Consulta la Hacienda Foral de tu territorio. Las escalas y los tipos de retención de esta página son los del régimen común.</p>" : "<p>Calcula el sueldo neto de 2026 a partir del bruto anual: Seguridad Social, retención del IRPF y neto al mes en 12 o 14 pagas.</p>" });
    return;
  }
  var R = r.brutoAnio, menos = r.menos1, p14 = r.pagas === 14 && !menos, ver, dr = r.difRenta, adr = Math.abs(dr);
  if (menos) ver = "Con " + eur(d.bruto) + " brutos al año de sueldo y " + r.meses + (r.meses === 1 ? " mes" : " meses") + " de contrato en 2026 cobras " + eur(R) + " brutos en el año y te quedan unos " + eur(r.neto) + " netos (" + eur(r.netoMes12) + " al mes de contrato), tras " + eur(r.ss) + " de Seguridad Social y " + eur(r.ret) + " de retención del IRPF (tipo del " + pct(r.tipo) + ") en " + r.ccaaNombre + (d.hijos > 0 ? " con " + Math.floor(d.hijos) + (d.hijos === 1 ? " hijo" : " hijos") : "") + ", con contrato temporal de menos de un año.";
  else ver = "Con " + eur(R) + " brutos al año (" + eur(R / r.pagas) + " por paga en " + r.pagas + " pagas) te quedan unos " + eur(r.neto) + " netos al año: " + (p14 ? eur(r.netoMesNormal14) + " al mes y " + eur(r.netoMesExtra14) + " en los dos meses con paga extra" : eur(r.netoMes12) + " al mes") +
    ", tras " + eur(r.ss) + " de Seguridad Social y " + eur(r.ret) + " de retención del IRPF (tipo del " + pct(r.tipo) + ") en " + r.ccaaNombre + (d.hijos > 0 ? " con " + Math.floor(d.hijos) + (d.hijos === 1 ? " hijo" : " hijos") : "") + ", " + (r.temporal ? "con contrato temporal" : "con contrato indefinido") + ".";
  if (adr < 50) nota += "<p>En la Renta 2026, con estos datos, lo retenido y el IRPF final salen casi iguales (diferencia de " + eur(adr) + "): no esperes devolución ni pago relevante.</p>";
  else if (dr > 0) nota += "<p>En la Renta 2026 el IRPF final estimado es " + eur(r.irpfFinal) + ", " + eur(adr) + " menos de lo que te retienen: con estos datos te saldría a devolver, y tu neto del año sería " + eur(r.netoFinal) + ".</p>";
  else if (r.noObligado) nota += "<p>En la Renta 2026 el IRPF final estimado es " + eur(r.irpfFinal) + ", " + eur(adr) + " más de lo que te retienen, pero con un solo pagador y hasta " + eur(P.obl) + " brutos no estás obligado a declarar (art. 96.2.a de la Ley del IRPF): si no presentas la Renta, no pagas esa diferencia y tu neto es el de la nómina (" + eur(r.neto) + "). Si la presentas por otro motivo, se liquidaría.</p>";
  else nota += "<p>En la Renta 2026 el IRPF final estimado es " + eur(r.irpfFinal) + ", " + eur(adr) + " más de lo que te retienen: con estos datos te saldría a pagar, y tu neto del año sería " + eur(r.netoFinal) + ". La calculadora de <a href=\"/decidir/retencion-irpf-nomina-subir-o-no/\">retención del IRPF en la nómina</a> te dice si te conviene subirla.</p>";
  if (r.orientativo) nota += "<p><strong>Escala autonómica orientativa:</strong> para " + r.ccaaNombre + " alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Supuestos y fuentes»); solo afecta al IRPF final de la Renta, no a la retención de la nómina.</p>";
  if (r.bajoSmi) nota += "<p><strong>Atención:</strong> por debajo de " + eur(P.smi) + " brutos al año (salario mínimo de 2026 a jornada completa) rigen bases mínimas de cotización por grupo que no se modelan, salvo que trabajes a tiempo parcial: el resultado es orientativo.</p>";
  if (r.sobreBase) nota += "<p>Tu sueldo supera la base máxima de cotización (" + eur(P.bmax) + " al mes): el exceso solo paga la cotización adicional de solidaridad, ya incluida.</p>";
  if (r.tipo === 0 && !r.menos1) nota += "<p>Con estos datos tu pagador no te retiene nada (por debajo de " + eur(r.limite81) + " al año, art. 81 del Reglamento del IRPF, en la situación «otras situaciones»); si eres soltero, viudo, divorciado o separado con hijos y no convives con el otro progenitor (monoparental), o tu cónyuge no gana más de 1.500 € al año, el límite es mayor y no te retendrían en más casos.</p>";
  if (r.menos1) nota += "<p>En un contrato temporal de menos de un año la retención mínima es del " + pct(P.min2) + " (art. 86.2 del Reglamento del IRPF); la retención y el IRPF final se calculan sobre lo que cobras en el año natural (art. 83.2 del Reglamento: sueldo equivalente por los meses de contrato entre 12), y no se reparte en pagas.</p>";
  nota += "<p><strong>Límites del cálculo:</strong> los hijos los cuentas tú enteros (si los compartes con el otro progenitor, tu retención sube); no incluye ascendientes, discapacidad, pensión compensatoria, deducciones, planes de pensiones, retribución en especie ni flexible, ni cambios de sueldo durante el año (regularización del art. 87 del Reglamento); supone todas las pagas iguales, un año completo (salvo el contrato temporal de menos de un año, que usa los meses indicados) y sin otras rentas; no cubre Ceuta ni Melilla, y algunos temporales (sustitución, formativos, relevo o discapacidad de al menos el 33 %) cotizan el 1,55 % de desempleo como los indefinidos. Tampoco la base mínima de cotización por grupo ni los pluses y horas extra, que cotizan distinto. Tu nómina real puede variar unos euros por redondeos de la empresa.</p>";
  var rows = [[menos ? "Bruto cobrado en 2026" : "Bruto anual", eur(R)], ["Seguridad Social a tu cargo (" + pct(P.w[r.temporal]) + " hasta la base máxima)", eur(r.ss)], ["Retención del IRPF en la nómina (" + pct(r.tipo) + ")", eur(r.ret)], { label: "Neto anual", values: [eur(r.neto)], strong: true }];
  if (p14) { rows.push(["Neto al mes (meses sin paga extra)", eur(r.netoMesNormal14)]); rows.push(["Neto en los 2 meses con paga extra", eur(r.netoMesExtra14)]); rows.push(["Neto al mes si te prorratean las pagas (12)", eur(r.netoMes12)]); }
  else rows.push([menos ? "Neto al mes de contrato" : "Neto al mes (12 pagas)", eur(r.netoMes12)]);
  rows.push(["IRPF final de la Renta 2026 (estimado)", eur(r.irpfFinal)]); rows.push([dr >= 0 ? "A devolver en la Renta (estimado)" : r.noObligado ? "Diferencia (no obligado a declarar)" : "A pagar en la Renta (estimado)", eur(adr)]);
  EM.renderResult({
    winner: p14 ? "p14" : "p12", verdict: ver, tone: "info", bigNumber: p14 ? r.netoMesNormal14 : r.netoMes12, bigLabel: p14 ? "netos al mes (meses sin paga extra, 14 pagas)" : menos ? "netos al mes de contrato" : "netos al mes (12 pagas)", format: eur,
    barsLabel: "De tu bruto anual: lo que cobras y lo que se queda en cotización y retención",
    bars: [{ label: "Neto anual", value: Math.max(r.neto, 0), color: "a" }, { label: "Retención del IRPF", value: r.ret, color: "b" }, { label: "Seguridad Social", value: r.ss, color: "c" }],
    cols: ["Importe"], rows: rows, note: nota
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
