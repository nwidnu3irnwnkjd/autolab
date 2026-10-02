// Navidad y Black Friday: presupuesto maximo sin endeudarte, ahorro mensual necesario y coste de financiar el gasto.
// Margen mensual = ingresos - gastos fijos (con cuotas de deudas) - ahorro objetivo. Presupuesto sin credito = margen x meses restantes (no toca el fondo).
// Financiar: cuota francesa con TIN/12 en 3, 6 y 12 cuotas (sin comisiones). Herramienta de planificacion con supuestos del usuario.
function calcular(d) {
  var margen = d.ingresos - d.gastos - d.ahorro, mpos = Math.max(0, margen);
  var presup = mpos * d.meses, colchon = d.mesesFondo * d.gastos;
  var exceso = Math.max(0, d.fondo - colchon), faltaFondo = Math.max(0, colchon - d.fondo);
  var falta = Math.max(0, d.gasto - presup), i = d.tin / 1200;
  function cuota(P, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
  function inter(P, n) { return P > 0 ? cuota(P, n) * n - P : 0; }
  var g = d.gasto <= presup + 0.005 ? 0 : (d.gasto <= presup + exceso + 0.005 ? 1 : 2);
  return {
    margen: margen, presupuesto: presup, colchon: colchon, exceso: exceso, faltaFondo: faltaFondo,
    ahorroNecesario: d.gasto / d.meses, falta: falta, sobra: Math.max(0, presup - d.gasto),
    int3: inter(d.gasto, 3), int6: inter(d.gasto, 6), int12: inter(d.gasto, 12),
    cuota12: d.gasto > 0 ? cuota(d.gasto, 12) : 0, intFalta12: inter(falta, 12), ganador: g
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["ingresos", "gastos", "ahorro", "fondo", "mesesFondo", "gasto", "meses", "tin"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.ingresos <= 0 || d.meses < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe tus ingresos netos mensuales y al menos 1 mes hasta diciembre.", tone: "warn", note: "<p>Sin ingresos ni meses por delante no hay presupuesto que calcular.</p>" });
    return;
  }
  if (d.meses > 12 || d.tin > 60 || d.mesesFondo > 36) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 12 meses de antelación, 36 meses de fondo y un TIN del 60 %.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, m = EM.num(d.meses, 0) + (d.meses === 1 ? " mes" : " meses"), w, verdict;
  var neg = r.margen < 0;
  if (d.gasto <= 0) {
    w = "ahorrar";
    verdict = "Con un gasto previsto de 0 € no hay nada que ahorrar ni financiar. Sin tocar tu fondo ni endeudarte, tu presupuesto máximo para Navidad es " + eur(r.presupuesto) + " en " + m + ".";
  } else if (g === 0) {
    w = "ahorrar";
    verdict = "Puedes pagar " + eur(d.gasto) + " sin crédito y sin tocar tu fondo: necesitas ahorrar " + eur(r.ahorroNecesario) + " al mes durante " + m + " y tu margen es " + eur(r.margen) + " al mes. El presupuesto que no necesita crédito es " + eur(r.presupuesto) + ".";
  } else if (g === 1) {
    w = "fondo";
    verdict = "Con tu margen solo ahorras " + eur(r.presupuesto) + " en " + m + " y tu gasto previsto es " + eur(d.gasto) + ": el resto solo lo cubrirías con el " + "exceso de tu fondo sobre el objetivo (" + eur(r.exceso) + "), que es una decisión tuya. El presupuesto que no necesita crédito ni fondo es " + eur(r.presupuesto) + ".";
  } else {
    w = "recortar";
    verdict = "Con tus datos tu gasto previsto de " + eur(d.gasto) + " no cabe sin crédito: el presupuesto máximo sin endeudarte ni tocar el fondo es " + eur(r.presupuesto) + " y te faltan " + eur(r.falta) + ". Financiar esa parte a 12 cuotas costaría " + eur(r.intFalta12) + " de intereses con el TIN que has puesto.";
  }
  var note = "<p><strong>Lectura:</strong> ";
  note += neg ? "tus gastos fijos y tu ahorro objetivo superan tus ingresos en " + eur(-r.margen) + " al mes, así que ahora mismo no queda margen para Navidad sin recortar o sin crédito. " : "te quedan " + eur(r.margen) + " libres al mes tras gastos fijos y ahorro objetivo. ";
  if (d.gasto > 0) note += "Para llegar con " + eur(d.gasto) + " tendrías que apartar " + eur(r.ahorroNecesario) + " al mes durante " + m + ". ";
  if (r.faltaFondo > 0) note += "Tu fondo está " + eur(r.faltaFondo) + " por debajo de tu objetivo de " + EM.num(d.mesesFondo, 1) + " meses de gastos (" + eur(r.colchon) + "): el presupuesto calculado no lo toca. ";
  else if (r.exceso > 0) note += "Tu fondo supera tu objetivo de " + EM.num(d.mesesFondo, 1) + " meses de gastos en " + eur(r.exceso) + ". ";
  note += "</p><p>Financiar todo el gasto con un TIN del " + EM.num(d.tin, 1) + " % costaría " + eur(r.int3) + " de intereses a 3 cuotas, " + eur(r.int6) + " a 6 y " + eur(r.int12) + " a 12 (el TIN es un ejemplo editable: pon el de tu tarjeta o crédito).</p>";
  note += "<p>Es una herramienta de planificación, no asesoramiento financiero. No incluye comisiones de aplazamiento ni descuentos o ofertas de Black Friday, pagas extra o ingresos variables, ni juegos de azar: no cuentes con premios para pagar la Navidad. Los gastos fijos deben incluir las cuotas de tus préstamos y tarjetas.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 0 ? "ok" : "warn",
    bigNumber: r.presupuesto, bigLabel: "presupuesto máximo sin crédito ni tocar el fondo", format: function (x) { return EM.eur(x); },
    barsLabel: "Presupuesto frente a gasto previsto",
    bars: [{ label: "Presupuesto sin crédito", value: Math.max(r.presupuesto, 0), color: "a" }, { label: "Gasto previsto", value: Math.max(d.gasto, 0), color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Margen libre al mes", eur(r.margen)],
      ["Presupuesto sin crédito en " + m, eur(r.presupuesto)],
      ["Ahorro mensual necesario para el gasto previsto", eur(r.ahorroNecesario)],
      ["Falta por cubrir con tu margen", eur(r.falta)],
      ["Intereses si financias todo a 3 cuotas", eur(r.int3)],
      ["Intereses si financias todo a 6 cuotas", eur(r.int6)],
      ["Intereses si financias todo a 12 cuotas", eur(r.int12)],
      { label: "Cuota mensual a 12 cuotas", values: [eur(r.cuota12)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
