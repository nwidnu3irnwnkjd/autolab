// Marca blanca o marca de fabricante: ahorro anual segun gasto, % cambiable y diferencia media de precio (hipotesis del usuario).
// base = gasto del periodo x % cambiable x (1 - % que descartas); ahorro = base x diferencia; equilibrio = diferencia minima para llegar a tu ahorro minimo.
// ganador: 0 cambiar, 1 mantener, 2 empate, 3 sin base de cambio.
function calcular(d) {
  var gasto = d.gasto * d.meses * 52 / 12;
  var base = gasto * d.pct / 100 * (1 - d.excl / 100);
  var ahorro = base * d.dif / 100, g;
  if (base <= 0) g = 3;
  else g = ahorro > d.minimo + 0.005 ? 0 : (ahorro < d.minimo - 0.005 ? 1 : 2);
  return { gastoAnual: gasto, baseCambio: base, ahorroAnual: ahorro, ahorroMes: ahorro / d.meses,
    pctGasto: gasto > 0 ? ahorro / gasto * 100 : 0, porPersona: ahorro / d.personas,
    difEquilibrio: base > 0 ? d.minimo / base * 100 : -1, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["gasto", "pct", "dif", "excl", "personas", "meses", "minimo"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.meses < 1 || d.meses > 12) {
    EM.renderResult({ winner: "invalido", verdict: "Indica de 1 a 12 meses de compra en el periodo.", tone: "warn", note: "<p>Para un ahorro anual usa 12; con menos meses el resultado es del periodo indicado.</p>" });
    return;
  }
  if (d.pct > 100 || d.excl > 100 || d.dif > 100) {
    EM.renderResult({ winner: "invalido", verdict: "Los porcentajes no pueden pasar de 100.", tone: "warn", note: "<p>Revisa el porcentaje de la cesta, el que descartas y la diferencia de precio.</p>" });
    return;
  }
  if (d.personas < 1) {
    EM.renderResult({ winner: "invalido", verdict: "El hogar debe tener al menos 1 persona.", tone: "warn", note: "<p>Indica cuántas personas comen de esa compra.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, w, verdict, tone = "ok", per = d.meses === 12 ? "al año" : "en " + EM.num(d.meses, 0) + (d.meses === 1 ? " mes" : " meses");
  if (g === 3) {
    w = "sin-base"; tone = "warn";
    verdict = "Con estos datos no queda ninguna parte de la cesta que cambiarías, así que no hay ahorro que calcular: sube el porcentaje cambiable o reduce los productos donde no cambiarías.";
  } else if (g === 0) {
    w = "cambiar";
    verdict = "Con estos datos cambiar compensa: ahorrarías " + eur(r.ahorroAnual) + " " + per + " (" + eur(r.ahorroMes) + " al mes, " + EM.num(r.pctGasto, 1) + " % de tu gasto), por encima de tus " + eur(d.minimo) + " mínimos. Compensaría mientras la diferencia media de precio no baje de " + EM.num(r.difEquilibrio, 1) + " %.";
  } else if (g === 1) {
    w = "mantener";
    verdict = "Con estos datos cambiar no llega a tu mínimo: ahorrarías " + eur(r.ahorroAnual) + " " + per + ", menos de los " + eur(d.minimo) + " que pedías. Compensaría si la diferencia media de precio fuera de al menos " + EM.num(r.difEquilibrio, 1) + " %.";
  } else {
    w = "empate"; tone = "warn";
    verdict = "Con estos datos el ahorro (" + eur(r.ahorroAnual) + " " + per + ") coincide con tu mínimo de " + eur(d.minimo) + ": cambiar o no es indiferente en dinero.";
  }
  var note = "<p><strong>Lectura:</strong> la diferencia de precio es una <strong>hipótesis tuya</strong>, no un dato de mercado: compruébala comparando unos pocos productos en tu supermercado habitual antes de decidir. ";
  if (g !== 3) note += "El ahorro por persona sería de " + eur(r.porPersona) + " " + per + ". Sobre " + eur(r.baseCambio) + " de compra que cambiarías, tu mínimo de " + eur(d.minimo) + " exige una diferencia de al menos <strong>" + EM.num(r.difEquilibrio, 1) + " %</strong>. ";
  note += "</p><p><strong>No incluye:</strong> diferencias de calidad, sabor o preferencias, ofertas y promociones, desplazamientos a otro establecimiento, ni cambios de precio durante el año. Se supone que el gasto semanal es constante.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: g !== 3 ? r.ahorroAnual : undefined, bigLabel: "ahorro estimado " + per, format: function (x) { return EM.eur(x); },
    barsLabel: "Gasto en el periodo",
    bars: [{ label: "Sin cambiar nada", value: r.gastoAnual, color: "a" }, { label: "Cambiando lo que indicas", value: Math.max(r.gastoAnual - r.ahorroAnual, 0), color: "b" }],
    cols: ["Valor"],
    rows: [
      ["Gasto en supermercado " + per, eur(r.gastoAnual)],
      ["Parte de la compra que cambiarías", eur(r.baseCambio)],
      { label: "Ahorro estimado " + per, values: [eur(r.ahorroAnual)], strong: true },
      ["Ahorro por mes", eur(r.ahorroMes)],
      ["Ahorro sobre el gasto total", EM.num(r.pctGasto, 1) + " %"],
      ["Diferencia de precio de equilibrio", r.difEquilibrio >= 0 ? EM.num(r.difEquilibrio, 1) + " %" : "—"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
