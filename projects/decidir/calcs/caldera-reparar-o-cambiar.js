// Reparar o cambiar la caldera de gas. Coste anualizado de cada opcion, sin descuento ni inflacion.
// Supuestos del modelo (data/params.json -> caldera_2026.modelo): caldera nueva de 15 anos; reserva anual para averias de la reparada = 10 % del presupuesto de la reparacion.
var S = { vidaNueva: 15, riesgo: 0.10 };
function calcular(d) {
  var neta = Math.max(d.nueva - d.ayuda, 0);
  var gasAct = d.consumo * d.pgas;
  var gasNue = d.consumo * d.rendAct / d.rendNueva * d.pgas;
  var ahorro = gasAct - gasNue, reserva = S.riesgo * d.repar;
  var rep = d.repar / d.vida + reserva + gasAct;
  var cam = neta / S.vidaNueva + gasNue;
  var flujo = ahorro + reserva, extra = neta - d.repar, vs;
  if (extra <= 0 && flujo >= 0) vs = 0; else if (flujo <= 0) vs = -1; else vs = extra / flujo;
  var amGas = ahorro > 0 ? neta / ahorro : (neta <= 0 ? 0 : -1);
  var diff = rep - cam;
  return {
    neta: neta, gasActual: gasAct, gasNuevo: gasNue, ahorroGas: ahorro, reserva: reserva,
    anualReparar: rep, anualCambiar: cam, diferencia: diff, ganador: Math.abs(diff) < 1 ? 2 : (diff > 0 ? 1 : 0),
    amortVsRep: vs, amortGas: amGas, equilibrio: (neta / S.vidaNueva - ahorro) / (1 / d.vida + S.riesgo)
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["repar", "nueva", "ayuda", "consumo", "rendAct", "rendNueva", "pgas", "vida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function anos(x) { return EM.num(x, 1) + " años"; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: n }); }
function pintar() {
  var d = leer();
  if (d.repar < 0 || d.nueva < 0 || d.ayuda < 0 || d.consumo < 0 || d.pgas < 0 || d.vida <= 0 || d.rendAct <= 0 || d.rendNueva <= 0) return;
  if (d.rendAct > 1.1 || d.rendNueva > 1.1) {
    aviso("Un rendimiento superior a 1,10 no es realista para una caldera.", "<p>Escribe el rendimiento como número entre 0 y 1 (0,81 = 81 %). Si tu caldera tiene la prueba de combustión de la revisión, ahí figura el rendimiento medido.</p>");
    return;
  }
  var r = calcular(d), g = r.ganador, N = S.vidaNueva;
  var cerca = Math.abs(r.diferencia) < Math.max(Math.min(r.anualReparar, r.anualCambiar), 1) * 0.03;
  var verdict;
  if (g === 2) verdict = "Con estos números, reparar y cambiar cuestan lo mismo al año.";
  else if (g === 0) verdict = "Con estos números, sale más barato reparar la caldera: " + EM.eur(Math.abs(r.diferencia)) + " menos al año que cambiarla.";
  else verdict = "Con estos números, sale más barato cambiar la caldera: " + EM.eur(Math.abs(r.diferencia)) + " menos al año que repararla.";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.equilibrio <= 0) note += "con tu gas, tu rendimiento y el precio de la caldera nueva, cambiar sale más barato aunque la reparación fuera gratis. ";
  else note += "cambiar empieza a salir más barato si la reparación cuesta más de <strong>" + EM.eur(r.equilibrio) + "</strong>; la tuya cuesta " + EM.eur(d.repar) + ". ";
  if (r.ahorroGas > 0) note += "La caldera nueva te ahorraría " + EM.eur(r.ahorroGas) + " de gas al año" + (r.amortGas > 0 ? " y esa diferencia, sola, tardaría " + anos(r.amortGas) + " en pagar sus " + EM.eur(r.neta) + " netos" : "") + (r.amortVsRep > 0 ? "; frente a reparar (contando también la reserva de averías que te ahorras) el cambio se amortiza en " + anos(r.amortVsRep) : (r.amortVsRep === 0 ? "; frente a reparar, el cambio ya sale a cuenta desde el primer año" : "")) + ". ";
  else note += "Con estos rendimientos la caldera nueva no ahorra gas, así que el cambio no se amortiza por consumo. ";
  note += "Dura " + N + " años en el modelo; si la reparada aguanta " + d.vida + (d.vida === 1 ? " año" : " años") + ", repartes la reparación entre esos años.</p>";
  if (d.ayuda > d.nueva) note += "<p><strong>Ojo:</strong> la ayuda que has puesto supera el precio de la caldera; se toma un coste neto de 0 €.</p>";
  note += "<p><strong>Seguridad:</strong> una revisión por técnico autorizado es obligatoria y esta calculadora no sustituye el diagnóstico: si hay olor a gas o sospecha de monóxido de carbono, corta el gas y llama al servicio técnico o a emergencias. <strong>Qué incluye:</strong> reparación, caldera nueva (neta de ayudas), gas y una reserva de averías de " + EM.num(S.riesgo * 100) + " % del presupuesto de la reparación al año; sin descuento ni inflación. <strong>No incluye:</strong> el mantenimiento y la revisión periódica (se suponen iguales en las dos), la normativa de calderas ni posibles prohibiciones futuras, el término fijo del gas, ni las ayudas autonómicas o municipales (consulta tu comunidad).</p>";
  EM.renderResult({
    winner: g === 2 ? "empate" : (g === 0 ? "reparar" : "cambiar"), verdict: verdict, tone: g === 2 || cerca ? "warn" : "ok",
    bigNumber: Math.abs(r.diferencia), bigLabel: g === 2 ? "de diferencia al año" : "menos al año con " + (g === 0 ? "reparar" : "cambiar") + " (coste anualizado)",
    barsLabel: "Coste anual (inversión repartida + reserva de averías + gas)",
    bars: [{ label: "Reparar" + (g === 0 ? " (gana)" : ""), value: r.anualReparar, color: "a" }, { label: "Cambiar" + (g === 1 ? " (gana)" : ""), value: r.anualCambiar, color: "b" }],
    cols: ["Reparar", "Cambiar"],
    rows: [
      ["Inversión repartida por año", EM.eur(d.repar / d.vida), EM.eur(r.neta / N)],
      ["Reserva de averías al año", EM.eur(r.reserva), EM.eur(0)],
      ["Gas al año", EM.eur(r.gasActual), EM.eur(r.gasNuevo)],
      { label: "Total al año", values: [EM.eur(r.anualReparar), EM.eur(r.anualCambiar)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
