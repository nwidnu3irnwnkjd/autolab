// Plazo inicial de la hipoteca: 20, 25 o 30 anos. Amortizacion francesa, tipo fijo durante todo el plazo.
// Esfuerzo = (cuota + otras cuotas de deuda al mes) / ingresos netos mensuales. Tope orientativo editable (no legal).
function cuota(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
function plazo(P, i, anos, otras, ing) {
  var n = anos * 12, c = cuota(P, i, n), t = c * n - P;
  return { cuota: c, intereses: t, esfuerzo: ing > 0 ? (c + otras) / ing * 100 : 0 };
}
function calcular(d) {
  var P = d.capital, i = d.tin / 1200, a = plazo(P, i, 20, d.otras, d.ingresos), b = plazo(P, i, 25, d.otras, d.ingresos), c = plazo(P, i, 30, d.otras, d.ingresos);
  var cmax = d.tope / 100 * d.ingresos - d.otras, nmin;
  // meses minimos para que la cuota no pase de cmax (amortizacion francesa); -1 si ningun plazo lo consigue
  if (cmax <= 0) nmin = -1;
  else if (i === 0) nmin = P / cmax;
  else if (cmax <= P * i) nmin = -1;
  else nmin = -Math.log(1 - P * i / cmax) / Math.log(1 + i);
  var ok = [a.esfuerzo <= d.tope, b.esfuerzo <= d.tope, c.esfuerzo <= d.tope];
  var elegido = ok[0] ? 20 : (ok[1] ? 25 : (ok[2] ? 30 : 0));
  var ref = elegido === 20 ? a : (elegido === 25 ? b : c);
  return {
    cuota20: a.cuota, cuota25: b.cuota, cuota30: c.cuota, int20: a.intereses, int25: b.intereses, int30: c.intereses,
    esf20: a.esfuerzo, esf25: b.esfuerzo, esf30: c.esfuerzo, cuotaMax: cmax, plazoMinAnos: nmin < 0 ? -1 : nmin / 12,
    elegido: elegido, extra30: c.intereses - ref.intereses, alivio30: ref.cuota - c.cuota, extra25: b.intereses - a.intereses, alivio25: a.cuota - b.cuota,
    extra30vs25: c.intereses - b.intereses
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["capital", "tin", "ingresos", "otras", "tope"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pctx(x) { return EM.num(x, 1) + " %"; }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.capital <= 0 || d.ingresos <= 0 || d.tope <= 0) { aviso("Escribe un capital, unos ingresos netos y un tope de esfuerzo mayores que 0.", "Sin capital ni ingresos no se puede calcular el esfuerzo."); return; }
  if (d.tin > 15 || d.tope > 100) { aviso("Revisa los límites: TIN de hasta el 15 % y tope de esfuerzo de hasta el 100 %.", "Fuera de esos valores el resultado no sería realista."); return; }
  var r = calcular(d), w, v, e = r.elegido, mejorTxt;
  if (e === 20) {
    w = "20";
    v = "Con estos datos, 20 años es el plazo más corto de los tres y ya queda dentro del " + pctx(d.tope) + " de esfuerzo (" + pctx(r.esf20) + " de tus ingresos): es el que menos intereses paga. Alargar a 30 años bajaría la cuota " + eur(r.alivio30, 2) + " al mes, pero añadiría " + eur(r.extra30) + " de intereses.";
  } else if (e === 25) {
    w = "25";
    v = "Con estos datos, 20 años se pasa del " + pctx(d.tope) + " de esfuerzo (" + pctx(r.esf20) + "), y 25 años es el plazo más corto de los tres que queda dentro (" + pctx(r.esf25) + "): es el que menos intereses paga entre los viables. Alargar a 30 años bajaría la cuota " + eur(r.alivio30, 2) + " al mes, pero añadiría " + eur(r.extra30) + " de intereses.";
  } else if (e === 30) {
    w = "30";
    v = "Con estos datos, solo 30 años queda dentro del " + pctx(d.tope) + " de esfuerzo (" + pctx(r.esf30) + "); a 25 años llegarías al " + pctx(r.esf25) + " y a 20 años al " + pctx(r.esf20) + ". Es el plazo más caro en intereses (" + eur(r.int30) + "), pero el único de los tres que cumple tu tope.";
  } else {
    w = "ninguno";
    v = "Con estos datos, ni 30 años queda dentro del " + pctx(d.tope) + " de esfuerzo (" + pctx(r.esf30) + "): con ese tope necesitarías pedir menos capital, aportar más entrada o contar con más ingresos.";
  }
  var minTxt = r.plazoMinAnos < 0 ? "no existe un plazo que baje la cuota al tope con este capital y estos ingresos" : "el plazo mínimo para quedar en el tope es de " + EM.num(Math.ceil(r.plazoMinAnos * 12 - 1e-9) / 12, 1) + " años";
  var note = "<p><strong>Lectura:</strong> la cuota máxima que cabe en tu tope es " + eur(Math.max(r.cuotaMax, 0), 2) + " al mes; " + minTxt + ". ";
  note += "Pasar de 20 a 25 años baja la cuota " + eur(r.alivio25, 2) + " al mes y suma " + eur(r.extra25) + " de intereses; pasar de 25 a 30 suma " + eur(r.extra30vs25) + " más.</p>";
  note += "<p><strong>Condiciones y límites:</strong> el tope de esfuerzo es una regla orientativa de prudencia que puedes cambiar, no un límite legal ni el criterio de ningún banco; cada entidad evalúa tu solvencia con sus propios criterios. Se supone tipo fijo todo el plazo y amortización francesa; en una variable la cuota cambiaría con el Euríbor. No incluye seguros, comisiones, gastos de la compraventa ni la edad (algunas entidades limitan el plazo para que termine antes de cierta edad). Si ya tienes la hipoteca y quieres acortarla o reducir cuota, usa la calculadora de amortizar plazo o cuota. Información orientativa, no asesoramiento.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: e === 0 ? "warn" : "ok",
    bigNumber: e === 0 ? r.esf30 : (e === 30 ? r.int30 : r.extra30), format: e === 0 ? function (x) { return pctx(x); } : EM.eur,
    bigLabel: e === 0 ? "de esfuerzo incluso a 30 años" : (e === 30 ? "de intereses a 30 años, el único plazo que cumple" : "más de intereses a 30 años que con " + e + " años"),
    barsLabel: "Intereses totales por plazo",
    bars: [{ label: "20 años", value: r.int20, color: "a", fmt: EM.eur }, { label: "25 años", value: r.int25, color: "b", fmt: EM.eur }, { label: "30 años", value: r.int30, color: "c", fmt: EM.eur }],
    cols: ["20 años", "25 años", "30 años"],
    rows: [
      ["Cuota mensual", eur(r.cuota20, 2), eur(r.cuota25, 2), eur(r.cuota30, 2)],
      ["Intereses totales", eur(r.int20), eur(r.int25), eur(r.int30)],
      { label: "Esfuerzo sobre ingresos", values: [pctx(r.esf20), pctx(r.esf25), pctx(r.esf30)], strong: true },
      ["Dentro de tu tope", r.esf20 <= d.tope ? "Sí" : "No", r.esf25 <= d.tope ? "Sí" : "No", r.esf30 <= d.tope ? "Sí" : "No"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
