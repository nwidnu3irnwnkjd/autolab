// Coste esperado de cada opcion: precio + gastos de compra + reparaciones previstas + averia esperada (probabilidad x coste), con garantia solo en el concesionario.
function calcular(d) {
  var riesgo = d.prob / 100 * d.averia;                         // averia esperada sin garantia
  var cubierto = riesgo * d.cobertura / 100;                    // parte que cubre la garantia del concesionario
  var part = d.precioPart + d.trasp + d.revision + d.reparPrev + riesgo;
  var conc = d.precioConc + d.reparPrev + riesgo - cubierto;
  var prima = d.precioConc - d.precioPart;                      // sobreprecio del concesionario
  var eqPrima = d.trasp + d.revision + cubierto;                // sobreprecio de equilibrio
  var base = prima - d.trasp - d.revision, den = d.averia * d.cobertura / 100;
  var probEq = den > 0 ? base / den * 100 : -1;                 // probabilidad (%) a la que ambas cuestan lo mismo
  return { costePart: part, costeConc: conc, diferencia: part - conc, prima: prima, primaEquilibrio: eqPrima, riesgo: riesgo, cubierto: cubierto, probEquilibrio: probEq, ganador: part < conc ? 0 : 1 };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
var IDS = ["precioPart", "precioConc", "reparPrev", "averia", "prob", "cobertura", "trasp", "revision"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pintar() {
  var d = leer(), r, v, note, g, dif, tone;
  if (IDS.some(function (k) { return d[k] < 0; })) return;
  if (d.precioPart <= 0 || d.precioConc <= 0) { aviso("Pon el precio de los dos coches.", "Sin precio de compra no se puede comparar."); return; }
  if (d.prob > 100 || d.cobertura > 100) { aviso("La probabilidad de avería y la parte cubierta por la garantía van de 0 a 100 %.", "Revisa esos dos porcentajes."); return; }
  r = calcular(d); g = r.ganador; dif = Math.abs(r.diferencia);
  if (dif < 0.02 * Math.min(r.costePart, r.costeConc)) { v = "Con estos datos las dos opciones salen casi igual (" + EM.eur(dif) + " de diferencia): decide por la confianza en el vendedor y no por el precio."; tone = "warn"; }
  else if (g === 0) { v = "Con estos datos sale mejor comprar a particular: te cuesta " + EM.eur(r.costePart) + " frente a " + EM.eur(r.costeConc) + " en el concesionario (" + EM.eur(dif) + " menos), contando la avería esperada."; tone = "ok"; }
  else { v = "Con estos datos sale mejor el concesionario: " + EM.eur(r.costeConc) + " frente a " + EM.eur(r.costePart) + " a particular (" + EM.eur(dif) + " menos), porque la garantía cubre parte del riesgo de avería."; tone = "ok"; }
  note = "<p><strong>Lectura:</strong> el concesionario pide " + (r.prima >= 0 ? EM.eur(r.prima) + " más" : EM.eur(-r.prima) + " menos") + " que el particular y la diferencia de equilibrio es de <strong>" + EM.eur(r.primaEquilibrio) + "</strong>: si la prima real supera esa cifra, a particular sale más barato; si es menor, compensa el concesionario. ";
  if (r.probEquilibrio >= 0 && r.probEquilibrio <= 100) note += "Con tu coste de avería y tu cobertura, ambas opciones cuestan lo mismo si la probabilidad de avería es de <strong>" + EM.num(r.probEquilibrio, 0) + " %</strong> (tú has puesto " + EM.num(d.prob, 0) + " %). ";
  else if (r.probEquilibrio > 100) note += "Ni con probabilidad de avería del 100 % compensaría el concesionario con estos precios. ";
  else if (r.probEquilibrio < 0 && d.averia * d.cobertura > 0) note += "El concesionario sale más barato aunque no hubiera ninguna avería, porque cuesta menos que el particular más sus gastos de compra. ";
  note += "</p><p><strong>Ojo:</strong> la probabilidad y el coste de avería son hipótesis tuyas, no estadísticas; la tasa y el impuesto de transferencia los pones tú (consulta la tarifa de tu comunidad y la DGT); la garantía no cubre desgaste ni todo tipo de averías. Mira también <a href=\"/decidir/coche-nuevo-o-seminuevo/\">coche nuevo o seminuevo</a>.</p>";
  EM.renderResult({
    winner: g === 0 ? "particular" : "concesionario", verdict: v, tone: tone,
    bigNumber: g === 0 ? r.costePart : r.costeConc, bigLabel: "de coste esperado " + (g === 0 ? "a particular" : "en el concesionario") + " (la opción más barata)", format: EM.eur,
    barsLabel: "Coste esperado de cada opción",
    bars: [{ label: "Particular" + (g === 0 ? " (más barato)" : ""), value: r.costePart, color: "a" }, { label: "Concesionario" + (g === 1 ? " (más barato)" : ""), value: r.costeConc, color: "b" }],
    cols: ["Particular", "Concesionario"],
    rows: [
      { label: "Coste esperado total", values: [EM.eur(r.costePart), EM.eur(r.costeConc)], strong: true },
      ["Precio del coche", EM.eur(d.precioPart), EM.eur(d.precioConc)],
      ["Impuesto, tasa y revisión previa", EM.eur(d.trasp + d.revision), "—"],
      ["Reparaciones previstas", EM.eur(d.reparPrev), EM.eur(d.reparPrev)],
      ["Avería esperada (tras garantía)", EM.eur(r.riesgo), EM.eur(r.riesgo - r.cubierto)],
      ["Diferencia de precio de equilibrio", EM.eur(r.primaEquilibrio), "—"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
