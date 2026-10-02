// Reparar o comprar: coste anualizado. Reparar = (reparacion + coste esperado de otra averia) / años de vida restante + sobreconsumo del viejo.
// Comprar = precio nuevo / vida util. Vida util, probabilidad de averia y consumos son supuestos del usuario (ejemplos declarados en la pagina).
// Coste esperado de otra averia = prob * reparacion * (1 - cobertura de la garantia de la reparacion sobre una ventana de 24 meses); supuesto: la avería futura cuesta lo mismo que esta.
function calcular(d) {
  var vidaRest = Math.max(d.vida - d.edad, 0), h = Math.max(vidaRest, 1);
  var cob = Math.min(d.garantia, 24) / 24, p = d.prob / 100;
  var esperado = p * d.reparacion * (1 - cob), energia = d.dkwh * d.precio;
  var anualRep = (d.reparacion + esperado) / h + energia, anualNuevo = d.nuevo / d.vida, dif = anualRep - anualNuevo;
  var eq = Math.max((anualNuevo - energia) * h / (1 + p * (1 - cob)), 0);
  return {
    vidaRestante: vidaRest, horizonteRep: h, costeEsperadoAveria: esperado, energiaExtraAnual: energia,
    anualReparar: anualRep, anualNuevo: anualNuevo, diferenciaAnual: dif,
    ganador: Math.abs(dif) < 1 ? "empate" : (dif < 0 ? "reparar" : "comprar"),
    equilibrioReparacion: eq, equilibrioPctNuevo: d.nuevo > 0 ? eq / d.nuevo * 100 : 0,
    regla50: d.reparacion <= 0.5 * d.nuevo ? 1 : 0, ratioReparacion: d.nuevo > 0 ? d.reparacion / d.nuevo : 0
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["vida", "edad", "reparacion", "nuevo", "garantia", "prob", "dkwh", "precio"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.vida < 1 || d.edad < 0 || d.reparacion < 0 || d.nuevo <= 0 || d.garantia < 0 || d.dkwh < 0 || d.precio < 0 || d.prob < 0) return;
  if (d.prob > 100) {
    EM.renderResult({ winner: "invalido", verdict: "La probabilidad de otra avería no puede superar el 100 %.", tone: "warn", note: "<p>Escribe un porcentaje entre 0 y 100.</p>" });
    return;
  }
  var r = calcular(d), abs = Math.abs(r.diferenciaAnual), g = r.ganador;
  var verdict = g === "empate" ? "Con estos supuestos, reparar y comprar cuestan lo mismo por año de uso."
    : "Con estos supuestos, " + (g === "reparar" ? "reparar" : "comprar uno nuevo") + " te sale " + EM.eur(abs) + " más barato por año de uso.";
  var note = "<p><strong>Lectura:</strong> ";
  note += r.equilibrioReparacion > 0 ? "reparar compensa si el presupuesto no pasa de unos <strong>" + EM.eur(r.equilibrioReparacion) + "</strong> (" + EM.num(r.equilibrioPctNuevo, 0) + " % del precio del nuevo) con tus datos. " : "con tus datos, reparar no compensa ni siquiera gratis, porque el sobreconsumo del aparato viejo ya supera el coste anual del nuevo. ";
  note += "Tu presupuesto es el " + EM.num(r.ratioReparacion * 100, 0) + " % del precio nuevo: la regla del 50 % " + (r.regla50 ? "diría reparar" : "diría comprar") + (r.regla50 === (g === "reparar") || g === "empate" ? ", y coincide con este cálculo." : ", pero este cálculo, que además cuenta la edad, el riesgo de otra avería y la energía, apunta a lo contrario.") + "</p>";
  if (d.edad >= d.vida) note += "<p><strong>Ojo:</strong> el aparato ya supera la vida útil que has indicado; se supone que la reparación te da al menos un año más de uso.</p>";
  if (d.reparacion > d.nuevo) note += "<p><strong>Ojo:</strong> la reparación cuesta más que un aparato nuevo.</p>";
  note += "<p>Es una estimación con supuestos tuyos: la vida útil y la probabilidad de avería son orientativas, se supone que una nueva avería costaría lo mismo que esta y que el nuevo dura " + EM.num(d.vida, 1) + " años. No incluye valor de venta, transporte e instalación, el reciclado del viejo ni lo que cuesta no tener el aparato unos días. Antes de decidir, comprueba si el aparato aún tiene garantía legal: en ese caso la reparación debería ser gratis.</p>";
  EM.renderResult({
    winner: g, verdict: verdict, tone: abs < Math.max(r.anualReparar, r.anualNuevo, 1) * 0.05 ? "warn" : "ok",
    bigNumber: abs, bigLabel: g === "empate" ? "de diferencia por año" : "menos por año de uso si " + (g === "reparar" ? "reparas" : "compras uno nuevo"), format: EM.eur,
    barsLabel: "Coste anualizado",
    bars: [{ label: "Reparar" + (g === "reparar" ? " (gana)" : ""), value: r.anualReparar, color: "a" }, { label: "Comprar nuevo" + (g === "comprar" ? " (gana)" : ""), value: r.anualNuevo, color: "b" }],
    cols: ["Reparar", "Comprar"],
    rows: [
      ["Coste anual", EM.eur(r.anualReparar), EM.eur(r.anualNuevo)],
      ["Años de uso que se espera", EM.num(r.horizonteRep, 1), EM.num(d.vida, 1)],
      ["Coste esperado de otra avería", EM.eur(r.costeEsperadoAveria), "—"],
      ["Sobreconsumo eléctrico del viejo por año", EM.eur(r.energiaExtraAnual), "—"],
      { label: "Presupuesto máximo para que reparar compense", values: [EM.eur(r.equilibrioReparacion), ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
