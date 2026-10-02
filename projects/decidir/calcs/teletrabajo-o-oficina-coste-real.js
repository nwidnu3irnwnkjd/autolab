// Teletrabajo u oficina: ahorro o coste neto con tus gastos. Semanas de teletrabajo al ano = SEM (supuesto: 52 menos vacaciones, festivos y bajas aproximados).
// Equipamiento: se reparte en AMORT anos. Con 0 dias no hay teletrabajo: compensacion y equipamiento no aplican y el neto es 0.
// Equilibrio de dias: neto(d) = d x unidad + fijo, con unidad = SEM x (desplazamiento + comida - casa) y fijo = compensacion anual - equipamiento anual.
var SEM = 46, AMORT = 4;
function calcular(d) {
  var act = d.dias > 0, dd = d.dias * SEM;
  var ahorroDesp = dd * d.desp, ahorroComida = dd * d.comida, costeCasa = dd * d.casa;
  var comp = act ? d.comp * 12 : 0, equip = act ? d.equip / AMORT : 0;
  var neto = ahorroDesp + ahorroComida + comp - costeCasa - equip;
  var horas = dd * d.min / 60, valorTiempo = horas * d.valorHora;
  var unidad = SEM * (d.desp + d.comida - d.casa), fijo = d.comp * 12 - d.equip / AMORT, tipo, diasEq = 0;
  if ((unidad > 0 && fijo >= 0) || (unidad === 0 && fijo > 0)) tipo = 0;
  else if (unidad > 0) { tipo = 1; diasEq = -fijo / unidad; }
  else if (unidad < 0 && fijo > 0) { tipo = 2; diasEq = fijo / -unidad; }
  else tipo = 3;
  var compEq = Math.max(0, equip - (ahorroDesp + ahorroComida - costeCasa)) / 12;
  return {
    ahorroDesplazamiento: ahorroDesp, ahorroComida: ahorroComida, costeCasa: costeCasa, compensacionAnual: comp, equipamientoAnual: equip,
    netoAnual: neto, netoMensual: neto / 12, horasAhorradas: horas, valorTiempo: valorTiempo, netoConTiempo: neto + valorTiempo,
    tipoDias: tipo, diasEquilibrio: diasEq, compensacionEquilibrio: compEq, ganador: Math.abs(neto) < 1 ? "empate" : (neto > 0 ? "teletrabajo" : "oficina")
  };
}
function dia(x) { return EM.num(x, x % 1 ? 1 : 0); }
function eur(x) { return EM.eur(x); }
var IDS = ["dias", "desp", "min", "valorHora", "casa", "comida", "comp", "equip"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.dias < 0 || d.desp < 0 || d.min < 0 || d.valorHora < 0 || d.casa < 0 || d.comida < 0 || d.comp < 0 || d.equip < 0) return;
  if (d.dias > 5) {
    EM.renderResult({ winner: "invalido", verdict: "Los días de teletrabajo por semana van de 0 a 5.", tone: "warn", note: "<p>Una semana laboral tiene 5 días como máximo; para teletrabajo total, pon 5.</p>" });
    return;
  }
  if (d.dias === 0) {
    EM.renderResult({ winner: "invalido", verdict: "Con 0 días de teletrabajo no hay nada que comparar: escribe al menos medio día por semana.", tone: "warn", note: "<p>Sin teletrabajo no hay ahorro ni coste; por eso la compensación y el equipamiento no se cuentan.</p>" });
    return;
  }
  var r = calcular(d), n = r.netoAnual, ab = Math.abs(n), t = r.ganador;
  var verdict = t === "empate" ? "Con estos datos, teletrabajar " + dia(d.dias) + " días a la semana ni te ahorra ni te cuesta dinero."
    : "Con estos datos, teletrabajar " + dia(d.dias) + " días a la semana " + (n > 0 ? "te ahorra " : "te cuesta ") + EM.eur(ab) + " al año (" + EM.eur(ab / 12) + " al mes)" + (r.horasAhorradas > 0 ? " y " + EM.num(r.horasAhorradas, 0) + " horas de desplazamiento" : "") + ".";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.tipoDias === 0) note += "con tus gastos, cada día de teletrabajo ahorra dinero y no necesitas un mínimo de días. ";
  else if (r.tipoDias === 1) note += "cada día de teletrabajo ahorra dinero, pero la inversión en equipamiento supera la compensación: empiezas a ahorrar a partir de <strong>" + EM.num(r.diasEquilibrio, 1) + " días</strong> a la semana" + (r.diasEquilibrio > 5 ? " (más de los 5 que tiene la semana: no compensa con este equipamiento)" : "") + ". ";
  else if (r.tipoDias === 2) note += "cada día de teletrabajo te cuesta más de lo que evitas; la compensación de la empresa, neta del equipamiento, lo cubre hasta <strong>" + EM.num(r.diasEquilibrio, 1) + " días</strong> a la semana. ";
  else note += "cada día de teletrabajo te cuesta más de lo que evitas y la compensación no lo cubre: no hay un número de días con el que ahorres. ";
  if (r.compensacionEquilibrio > 0) note += "Para que no pierdas dinero, la empresa debería compensarte al menos <strong>" + EM.eur(r.compensacionEquilibrio, 2) + " al mes</strong>. ";
  else note += "No necesitas compensación de la empresa para no perder dinero. ";
  if (d.valorHora > 0) note += "Valorando tu hora a " + EM.eur(d.valorHora, 2) + ", el tiempo que ahorras equivale a " + EM.eur(r.valorTiempo) + " al año y el balance con tiempo es de " + EM.eur(r.netoConTiempo) + ". ";
  note += "</p><p><strong>Límites:</strong> el coste del desplazamiento solo ahorra lo que realmente evitas (gasolina, peajes, billete suelto): un abono mensual se ahorra solo si lo das de baja. Se cuentan " + SEM + " semanas al año, supuesto que descuenta vacaciones y festivos, y el equipamiento se reparte en " + AMORT + " años. No se modelan la deducibilidad fiscal de gastos de teletrabajo (consulta con tu empresa o asesor), la productividad ni el bienestar, ni posibles cambios de salario o plus.</p>";
  EM.renderResult({
    winner: t, verdict: verdict, tone: t === "empate" ? "warn" : "ok",
    bigNumber: ab, bigLabel: t === "empate" ? "de diferencia al año" : (n > 0 ? "de ahorro neto al año teletrabajando" : "de coste neto al año teletrabajando"), format: EM.eur,
    barsLabel: "Lo que evitas y lo que gastas, al año",
    bars: [{ label: "Desplazamiento y comida que evitas", value: r.ahorroDesplazamiento + r.ahorroComida, color: "a" }, { label: "Gasto extra en casa y equipamiento", value: r.costeCasa + r.equipamientoAnual, color: "b" }, { label: "Compensación de la empresa", value: r.compensacionAnual, color: "a" }],
    cols: ["Al año", "Al mes"],
    rows: [
      ["Desplazamiento que evitas", EM.eur(r.ahorroDesplazamiento), EM.eur(r.ahorroDesplazamiento / 12)],
      ["Comida fuera que evitas", EM.eur(r.ahorroComida), EM.eur(r.ahorroComida / 12)],
      ["Gasto extra en casa", EM.eur(-r.costeCasa), EM.eur(-r.costeCasa / 12)],
      ["Equipamiento (repartido)", EM.eur(-r.equipamientoAnual), EM.eur(-r.equipamientoAnual / 12)],
      ["Compensación de la empresa", EM.eur(r.compensacionAnual), EM.eur(r.compensacionAnual / 12)],
      { label: "Balance neto (negativo = te cuesta)", values: [EM.eur(n), EM.eur(n / 12)], strong: true },
      ["Horas de desplazamiento que ahorras", EM.num(r.horasAhorradas, 0) + " h", EM.num(r.horasAhorradas / 12, 1) + " h"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
