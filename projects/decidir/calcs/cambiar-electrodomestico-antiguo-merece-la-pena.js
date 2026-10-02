// Cambiar un electrodomestico que funciona por uno de clase A: solo cuenta el ahorro de luz frente al precio neto del nuevo.
// ahorro anual = (kWh actual - kWh nuevo) x precio de la luz; neto = precio nuevo - reventa/ayuda (>= 0).
// Compensa si el ahorro de los N años de horizonte cubre el neto (equivale a: ahorro anual >= neto / N, el precio del nuevo repartido en su vida).
// vida restante del actual: años que el viejo aun duraria; ventaja de cambiar ahora frente a esperar = restante x (ahorro anual - neto / N).
function calcular(d) {
  var dk = d.act - d.nue, ahorro = dk * d.luz, neto = Math.max(d.coste - d.reventa, 0);
  var pb = neto === 0 ? 0 : (ahorro > 0 ? neto / ahorro : -1);
  var ahorroN = ahorro * d.anos, saldo = ahorroN - neto, anual = neto / d.anos;
  return {
    ahorroKwh: dk, ahorroAnual: ahorro, neto: neto, anosAmort: pb, kwhEvitados: dk * d.anos,
    ahorroAcum: ahorroN, saldo: saldo, costeAnualizado: anual, ventajaAnual: ahorro - anual,
    ventajaAdelantar: d.resta * (ahorro - anual), minKwh: d.luz > 0 ? neto / (d.anos * d.luz) : -1,
    compensa: saldo >= 0 && dk > 0 ? 1 : 0
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["act", "nue", "coste", "reventa", "luz", "anos", "resta"];
var EJ = {
  nevera: { act: 300, nue: 170, coste: 650 }, lavadora: { act: 150, nue: 90, coste: 500 },
  lavavajillas: { act: 280, nue: 200, coste: 550 }, secadora: { act: 450, nue: 200, coste: 700 }, horno: { act: 160, nue: 110, coste: 500 }
};
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function an(x) { return x < 0 ? "nunca" : EM.num(x, 1) + " años"; }
function pintar() {
  var d = leer();
  if (d.act < 0 || d.nue < 0 || d.coste <= 0 || d.reventa < 0 || d.luz < 0 || d.anos < 1 || d.anos > 30 || d.resta < 0) return;
  if (d.reventa > d.coste) {
    EM.renderResult({ winner: "invalido", verdict: "La reventa o ayuda no puede superar el precio del aparato nuevo.", tone: "warn",
      note: "<p>Escribe solo el importe que recuperarás (venta del viejo o ayuda confirmada), que no puede ser mayor que lo que pagas.</p>" });
    return;
  }
  var r = calcular(d), n = Math.round(d.anos), c = r.compensa === 1, abs = Math.abs(r.saldo);
  var verdict = r.ahorroKwh <= 0 ? "El aparato nuevo no gasta menos que el actual: no hay ahorro de luz que justifique el cambio."
    : c ? "Con estos supuestos, el ahorro de luz cubre el precio neto del nuevo en " + an(r.anosAmort) + " y deja " + EM.eur(r.saldo) + " de ahorro neto en " + n + " años."
    : "Con estos supuestos, el ahorro de luz no cubre el precio neto del nuevo en " + n + " años (se amortizaría en " + an(r.anosAmort) + ").";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.ahorroKwh > 0) {
    note += "ahorras " + EM.num(r.ahorroKwh, 0) + " kWh al año (" + EM.eur(r.ahorroAnual) + ") y evitas " + EM.num(r.kwhEvitados, 0) + " kWh en " + n + " años. ";
    note += "Para que el cambio compense en " + n + " años necesitarías ahorrar al menos <strong>" + EM.num(r.minKwh, 0) + " kWh al año</strong> con tu precio de la luz y tu precio neto. ";
    note += d.resta > 0 ? "Si tu aparato aún aguantara " + EM.num(d.resta, 0) + " años, cambiarlo ahora en vez de esperar a que falle " + (r.ventajaAdelantar >= 0 ? "te daría" : "te costaría") + " unos " + EM.eur(Math.abs(r.ventajaAdelantar)) + " en ese tiempo, contando el precio del nuevo repartido en su vida." : "Si el actual ya no funciona, la comparación útil es entre modelos nuevos: pesa el precio y el consumo de cada uno.";
  } else note += "con el mismo consumo o más, el cambio solo se justificaría por averías, ruido o funciones, no por energía. ";
  note += "</p><p><strong>Ojo:</strong> el consumo real depende del uso (carga, programa, temperatura, ubicación) y el de la etiqueta es de laboratorio. No incluye agua o detergente (en lavadora y lavavajillas pueden sumar), el transporte e instalación, ni el impacto ambiental de fabricar un aparato nuevo y reciclar el viejo. Si el actual se ha estropeado, compara también con <a href=\"/decidir/reparar-o-comprar-electrodomestico/\">reparar o comprar un electrodoméstico</a>.</p>";
  EM.renderResult({
    winner: c ? "cambiar" : "mantener", verdict: verdict, tone: c ? "ok" : "warn",
    bigNumber: r.saldo, bigLabel: r.saldo >= 0 ? "de ahorro neto en " + n + " años (ahorro de luz menos precio neto)" : "de pérdida en " + n + " años (precio neto menos ahorro de luz)",
    format: function (x) { return EM.eur(Math.abs(x)); },
    barsLabel: "Precio neto frente al ahorro de luz en " + n + " años",
    bars: [{ label: "Precio neto del nuevo", value: r.neto, color: "a" }, { label: "Ahorro de luz acumulado", value: Math.max(r.ahorroAcum, 0), color: "b" }],
    cols: ["Resultado"],
    rows: [
      ["Ahorro de energía por año", EM.num(r.ahorroKwh, 0) + " kWh"],
      ["Ahorro en euros por año", EM.eur(r.ahorroAnual)],
      ["Precio neto (nuevo menos reventa o ayuda)", EM.eur(r.neto)],
      ["Años de amortización simple", an(r.anosAmort)],
      ["Ahorro de luz en " + n + " años", EM.eur(r.ahorroAcum)],
      ["kWh evitados en " + n + " años", EM.num(r.kwhEvitados, 0)],
      ["Ahorro mínimo para compensar", r.minKwh < 0 ? "—" : EM.num(r.minKwh, 0) + " kWh al año"]
    ],
    note: note
  });
}
(function () {
  var s = document.getElementById("tipoSel");
  s.value = "nevera";
  s.addEventListener("change", function () {
    var e = EJ[s.value]; if (!e) return;
    ["act", "nue", "coste"].forEach(function (k) { document.getElementById(k).value = e[k]; });
    pintar();
  });
})();
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
