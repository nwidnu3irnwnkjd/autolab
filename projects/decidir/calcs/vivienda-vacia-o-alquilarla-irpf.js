// Piso vacio o alquilado: IRPF por imputacion de rentas (art. 85) frente a rendimiento del alquiler. Parametros: data/params.json -> alquiler_irpf_2026 (fuentes y fechas alli).
var P = {"imp": {"g": 2, "r": 1.1, "r12": 1.1}, "dias": 365};
function calcular(d) {
  var D = P.dias, t = d.tipo / 100, p = Number(d.contrato) / 100, dv = Math.min(Math.max(Math.round(d.dv), 0), D - 1), da = D - dv, fam = d.fam === "si";
  var impA = d.cat * P.imp[d.rev] / 100, cuotaA = impA * t, resA = -d.gastos - cuotaA;
  var ing = 12 * d.renta * da / D, gded = d.gastos * da / D, prev = ing - gded, red = prev > 0 ? prev * (1 - p) : prev;
  var minimo = impA * da / D, redf = fam ? Math.max(red, minimo) : red, impdv = impA * dv / D;
  var cuotaB = (Math.max(redf, 0) + impdv) * t, resB = ing - d.gastos - cuotaB;
  var rstar = (gded + minimo / (1 - p)) * D / (12 * da);
  return { noModelado: 0, impA: impA, cuotaA: cuotaA, resA: resA, ing: ing, prev: prev, red: red, minimo: minimo, redf: redf, impdv: impdv, cuotaB: cuotaB, resB: resB,
    dif: resB - resA, rstar: rstar, famAplica: fam && red < minimo ? 1 : 0, dobleCuota: cuotaB - cuotaA };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["cat", "dv", "renta", "gastos", "tipo"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  ["rev", "contrato", "fam"].forEach(function (k) { d[k] = document.getElementById(k).value; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.cat < 0 || d.renta < 0 || d.gastos < 0 || d.tipo < 0 || d.tipo > 54 || d.dv < 0 || d.dv > 364) return;
  var r = calcular(d), pc = EM.num(P.imp[d.rev], 1) + " %", fam = d.fam === "si", verdict;
  verdict = 'Con tus datos, tenerlo vacío todo el año te cuesta ' + EM.eur(-r.resA) + ' (gastos más ' + EM.eur(r.cuotaA) + ' de IRPF por la imputación del ' + pc + ' del valor catastral); alquilado pagas ' + EM.eur(r.cuotaB) + ' de IRPF y te quedan ' + EM.eur(r.resB) + ' al año después de gastos e impuestos.';
  if (r.famAplica) verdict += ' Como se lo alquilas a un familiar y el alquiler rinde menos que la imputación, Hacienda te cobra la imputación (' + EM.eur(r.minimo) + ' de base) como si no lo hubieras reducido.';
  var rows = [
    { label: "Vacío todo el año", values: [EM.eur(0), EM.eur(r.impA), EM.eur(r.cuotaA), EM.eur(r.resA)] },
    { label: "Alquilado" + (d.dv > 0 ? " (" + (365 - d.dv) + " días)" : ""), values: [EM.eur(r.ing), EM.eur(Math.max(r.redf, 0) + r.impdv), EM.eur(r.cuotaB), EM.eur(r.resB)], strong: true }
  ];
  var note = fam ? '<p><strong>Alquiler a un familiar:</strong> con un cónyuge o pariente hasta el tercer grado (incluidos los afines) el rendimiento neto no puede ser inferior a la imputación de los días alquilados (' + EM.eur(r.minimo) + '). Para que el alquiler te cueste más IRPF que dejarlo vacío, el rendimiento neto reducido tiene que superar esa cifra: con tus gastos y la reducción del ' + EM.num(Number(d.contrato)) + ' %, hace falta cobrar más de <strong>' + EM.eur(r.rstar) + ' al mes</strong>; por debajo, tributas lo mismo que vacío.</p>'
    : '<p><strong>Umbral:</strong> con tus gastos y la reducción del ' + EM.num(Number(d.contrato)) + ' %, alquilar te cuesta más IRPF que tenerlo vacío a partir de <strong>' + EM.eur(r.rstar) + ' al mes</strong> (' + (d.renta >= r.rstar ? 'tu renta lo supera' : 'tu renta no llega') + '). Por debajo, pagas menos impuestos que vacío, pero esa cifra no es la renta que te compensa: cobras ' + EM.eur(r.ing) + ' al año.</p>';
  note += '<p><strong>Cómo se calcula:</strong> vacío, tributas el ' + pc + ' del valor catastral (' + EM.eur(r.impA) + ') al tipo marginal que indicas; los gastos no son deducibles. Alquilado, tributas por el rendimiento neto (renta menos gastos de los días alquilados) con la reducción del art. 23.2' + (d.dv > 0 ? ', más la imputación de los ' + d.dv + ' días vacíos (' + EM.eur(r.impdv) + ')' : '') + '. Los gastos incluyen la amortización, que no sale de tu cuenta pero es coste real del inmueble.</p>';
  note += '<p><strong>Límites:</strong> el tipo marginal es una aproximación; la calculadora no resta las pérdidas del alquiler de tus otras rentas, aunque la ley sí lo permite (art. 48), salvo el exceso de intereses y reparaciones sobre los ingresos, que se arrastra 4 años (art. 23.1): con pérdidas, el IRPF real del alquilado es menor que el que ves; se supone que los gastos se deducen por días alquilados; no incluye el recargo del IBI a viviendas vacías, que fijan algunos ayuntamientos, ni Ceuta, Melilla, País Vasco y Navarra, ni inmuebles sin valor catastral, vivienda habitual, IVA o alquiler turístico.</p>';
  note += '<p><strong>Vigencia (7/10/2026):</strong> el Real Decreto-ley 26/2026 estuvo en vigor del 1 al 2 de octubre y fue derogado (BOE-A-2026-20526). El RDL 29/2026 (en vigor desde el 8-10-2026, pendiente de convalidación) recupera la DA 55.ª con efectos desde el 1-1-2026: el 1,1 % también para revisiones catastrales de 2012 a 2015 (opción propia del desplegable); sus cambios en el art. 23.2 solo afectan a contratos firmados desde el 1-12-2026 y los de los arts. 24 y 85 empiezan en 2027, y no se aplican aquí.</p>';
  EM.renderResult({
    winner: "alquilar", verdict: verdict, tone: "ok",
    bigNumber: r.resB, bigLabel: "te quedan al año alquilado, después de gastos e IRPF", format: EM.eur,
    barsLabel: "IRPF al año", bars: [{ label: "Vacío", value: r.cuotaA, color: "a" }, { label: "Alquilado", value: r.cuotaB, color: "b" }],
    cols: ["Ingresos", "Base de IRPF", "IRPF", "Te queda al año"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
