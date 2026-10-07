// IRPF por alquilar una vivienda (ejercicio 2026). Parametros: data/params.json -> alquiler_irpf_2026 (fuentes y fechas alli).
var P = {"amort": 3, "pct": {"a60": 60, "b50": 50, "b60": 60, "b70": 70, "b70s": 70, "b90": 90, "n0": 0}};
// Neto en mano con renta mensual R y reduccion p (%): ingresos - gastos pagados - cuota. Devuelve tambien las piezas del rendimiento.
function liquidar(d, R, p) {
  var m = d.meses, ing = R * m, fin = Math.min(d.interep, ing);
  var am = P.amort / 100 * Math.max(d.adq, d.cat) * m / 12;
  var prev = ing - d.otros - fin - am;
  var red = prev > 0 ? prev * (1 - p / 100) : prev;
  var cuota = Math.max(red, 0) * d.tipo / 100;
  return { ing: ing, fin: fin, am: am, prev: prev, red: red, cuota: cuota, neto: ing - d.otros - d.interep - cuota };
}
// Renta mensual con la que, con la reduccion q, el neto en mano iguala a T (despeje exacto por tramos).
function rentaEquivalente(d, q, T) {
  var m = d.meses, S = d.otros + d.interep, am = P.amort / 100 * Math.max(d.adq, d.cat) * m / 12, k = d.tipo / 100 * (1 - q / 100), Rm;
  if (T >= am && k < 1) Rm = S + (T - k * am) / (1 - k); else Rm = T + S;
  return Math.max(0, Rm / m);
}
function calcular(d) {
  var p = P.pct[d.contrato], R = d.renta, m = d.meses, a = liquidar(d, R, p);
  var o = { noModelado: 0, ingresos: a.ing, amort: a.am, finDeducido: a.fin, previo: a.prev, pct: p, reduccion: Math.max(a.prev, 0) * p / 100, reducido: a.red, cuota: a.cuota, neto: a.neto,
    rentaCubre: (d.otros + d.interep) / m, rentaIrpf: (d.otros + d.interep + a.am) / m };
  [50, 60, 70, 90].forEach(function (q) { o["n" + q] = liquidar(d, R, q).neto; });
  [60, 70, 90].forEach(function (q) { o["r" + q] = q <= p ? R : rentaEquivalente(d, q, a.neto); });
  return o;
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["renta", "meses", "otros", "interep", "adq", "cat", "tipo"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.contrato = document.getElementById("contrato").value; return d;
}
function pintar() {
  var d = leer();
  if (d.renta < 0 || d.otros < 0 || d.interep < 0 || d.adq < 0 || d.cat < 0 || d.tipo < 0 || d.tipo > 54 || d.meses < 1 || d.meses > 12) return;
  var r = calcular(d);
  var perdida = r.previo <= 0;
  var verdict = perdida
    ? 'Con estos datos, los gastos deducibles (' + EM.eur(d.otros + r.finDeducido + r.amort) + ') igualan o superan los ingresos (' + EM.eur(r.ingresos) + '): el rendimiento neto es ' + EM.eur(r.previo) + ' y no pagas IRPF por este alquiler (esta herramienta no calcula el ahorro que daría compensar la pérdida con otras rentas).'
    : 'Con estos datos, tu rendimiento neto de ' + EM.eur(r.previo) + ' baja a ' + EM.eur(r.reducido) + ' con la reducción del ' + EM.num(r.pct) + ' %, pagas unos ' + EM.eur(r.cuota) + ' de IRPF y te quedan ' + EM.eur(r.neto) + ' netos en el año.';
  var rows = [], lv = [[50, "n50"], [60, "n60"], [70, "n70"], [90, "n90"]];
  lv.forEach(function (x) {
    var q = x[0], sel = q === r.pct;
    rows.push({ label: "Reducción del " + q + " %" + (sel ? " (la tuya)" : ""), values: [EM.eur(r[x[1]]), q > r.pct ? EM.eur(Math.round(r["r" + q] * 100) / 100) + " al mes (" + EM.num(Math.max(0, (1 - r["r" + q] / d.renta) * 100), 1) + " % menos)" : "—"], strong: sel });
  });
  var note = '<p><strong>Umbrales:</strong> con estos gastos, necesitas unos <strong>' + EM.eur(r.rentaCubre) + ' al mes</strong> para cubrir lo que pagas (gastos, intereses y reparaciones) y empiezas a tributar a partir de unos <strong>' + EM.eur(r.rentaIrpf) + ' al mes</strong> (incluida la amortización).</p>';
  note += '<p><strong>Rebaja de renta que compensa:</strong> la última columna es la renta mensual mínima con la que, con esa reducción mayor, te quedaría lo mismo que ahora. Si rebajas más, pierdes; solo sirve si de verdad cumples los requisitos de ese porcentaje (para el 90 %: zona tensionada declarada, contrato nuevo y renta inicial rebajada más del 5 % respecto al contrato anterior).</p>';
  note += '<p><strong>Límites:</strong> la reducción solo se aplica a rendimientos netos positivos declarados en una autoliquidación presentada antes de que Hacienda inicie un procedimiento, y no a ingresos no declarados o gastos indebidos que se regularicen (art. 23.2). Si cumples varios supuestos, se aplica el mayor porcentaje. Presentar fuera de plazo mantiene la reducción pero añade recargo (art. 27 de la Ley General Tributaria). Si tus otras rentas no del trabajo superan 6.500 €, pierdes la reducción del art. 20 y la deducción de la DA 61.ª, lo que sube tu IRPF. El tipo marginal es una aproximación: si el alquiler te cambia de tramo, la cuota real difiere. No incluye el mobiliario y enseres cedidos (se amortizan aparte, art. 14.2.b del Reglamento), los gastos pendientes de años anteriores, la renta imputada de los meses sin alquilar, IVA, alquiler turístico, local, pérdidas, ITP/AJD, no residentes ni País Vasco y Navarra.</p>';
  note += '<p><strong>Vigencia (2/10/2026):</strong> El Real Decreto-ley 26/2026 estuvo en vigor del 1 al 2 de octubre de 2026 y fue derogado (BOE-A-2026-20526); esta calculadora aplica el régimen vigente de la Ley 12/2023. <strong>Desde el 7/10/2026:</strong> el RDL 29/2026 (en vigor desde el 8-10-2026, pendiente de convalidación) reescribe el art. 23.2 solo para contratos firmados después del 1-12-2026 (DT 38.ª) y añade un 80 % para la prórroga tácita; para el IRPF 2026 de contratos anteriores casi nada cambia (el 80 % de la prórroga tácita vale si el plazo de 5 años del contrato vence después del 1-12-2026). Su nueva deducción estatal del 10 % del alquiler de vivienda habitual (base imponible inferior a 33.007,20 €, máximo 1.163 €) no está incluida.</p>';
  EM.renderResult({
    winner: "p" + r.pct, verdict: verdict, tone: "ok",
    bigNumber: r.neto, bigLabel: "netos al año después de IRPF", format: EM.eur,
    barsLabel: "Del ingreso al neto en mano", bars: [{ label: "Ingresos por alquiler", value: r.ingresos, color: "a" }, { label: "Neto después de gastos e IRPF", value: Math.max(r.neto, 0), color: "b" }],
    cols: ["Neto en mano al año", "Renta mensual mínima que compensa (rebaja)"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
