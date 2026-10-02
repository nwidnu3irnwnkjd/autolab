// Cocinar en casa o comer fuera: ahorro anual de sustituir X comidas por semana, con y sin valor del tiempo.
// Comida fuera = precio + minutos de desplazamiento x valor de la hora; en casa = coste por racion + minutos de cocinar x valor de la hora.
// Equilibrio = valor de la hora a partir del cual deja de compensar cocinar (-1 si no hay: cocinar gana siempre o nunca).
// ganador: 0 cocinar, 1 comer fuera, 2 empate.
function calcular(d) {
  var k = d.dias / 5, vh = d.vh / 60;
  var cOut = d.precio + d.minDesp * vh, cHome = d.racion + d.minCook * vh, dif = cOut - cHome;
  var sust = d.sust * k, fuera = d.fuera * k;
  var ahorroDin = sust * (d.precio - d.racion), ahorro = sust * dif;
  var horas = sust * (d.minCook - d.minDesp) / 60;
  var vhEq = -1, dm = d.precio - d.racion, dt = d.minCook - d.minDesp;
  if (dt > 0 && dm > 0) vhEq = dm / (dt / 60);
  return { comidasAnio: fuera, sustAnio: sust, gastoFuera: fuera * d.precio, gastoCasaMismas: fuera * d.racion,
    costeFueraT: fuera * cOut, costeCasaT: fuera * cHome,
    ahorroDinero: ahorroDin, ahorroTiempo: ahorro, horasExtra: horas, vhEq: vhEq,
    difComida: dif, ganador: ahorro > 1 ? 0 : (ahorro < -1 ? 1 : 2) };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["fuera", "precio", "racion", "minCook", "minDesp", "vh", "sust", "dias"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.dias < 1 || d.dias > 366) {
    EM.renderResult({ winner: "invalido", verdict: "Indica entre 1 y 366 días laborables al año.", tone: "warn", note: "<p>Con otro valor el cálculo anual no tendría sentido.</p>" });
    return;
  }
  if (d.fuera > 7 || d.sust > d.fuera) {
    EM.renderResult({ winner: "invalido", verdict: "Las comidas fuera son como mucho 7 a la semana y no puedes sustituir más de las que haces fuera.", tone: "warn", note: "<p>Revisa «comidas fuera» y «comidas que sustituirías».</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, w, verdict, tone = "ok";
  var tiempo = d.vh > 0, ah = Math.abs(r.ahorroTiempo), s = EM.num(d.sust, d.sust % 1 ? 1 : 0);
  if (d.sust <= 0) {
    w = "sin-cambio"; tone = "warn";
    verdict = "Sin sustituir ninguna comida no hay ahorro que calcular: hoy gastas " + eur(r.gastoFuera) + " al año en comer fuera.";
  } else if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con estos datos cocinar en casa y comer fuera cuestan lo mismo" + (tiempo ? ", contando tu tiempo a " + eur(d.vh, 2) + " la hora" : "") + ".";
  } else if (g === 0) {
    w = "cocinar";
    verdict = "Con estos datos sustituir " + s + " comidas por semana por cocinar en casa te ahorra " + eur(ah) + " al año" + (tiempo ? " contando tu tiempo a " + eur(d.vh, 2) + " la hora" : " (sin contar tu tiempo)") + "." +
      (r.vhEq > 0 ? " Compensa mientras tu hora valga menos de " + eur(r.vhEq, 2) + "." : "");
  } else {
    w = "fuera";
    verdict = "Con estos datos comer fuera te sale " + eur(ah) + " al año mejor que sustituir " + s + " comidas por semana por cocinar" + (tiempo ? ", contando tu tiempo a " + eur(d.vh, 2) + " la hora" : "") + ": cocinar no compensa" + (r.vhEq > 0 ? " si tu hora vale más de " + eur(r.vhEq, 2) + "" : "") + ".";
  }
  var note = "<p><strong>Lectura:</strong> cada comida que sustituyes ahorra " + eur(d.precio - d.racion, 2) + " en dinero";
  note += d.minCook !== d.minDesp ? " y " + (d.minCook > d.minDesp ? "te cuesta " + EM.num(d.minCook - d.minDesp, 0) + " minutos más de tu tiempo" : "te ahorra " + EM.num(d.minDesp - d.minCook, 0) + " minutos de tu tiempo") + ". " : ". ";
  if (r.vhEq > 0) note += "El valor de la hora de equilibrio es <strong>" + eur(r.vhEq, 2) + "</strong>: por debajo cocinar sale mejor y por encima, comer fuera. ";
  else if (d.sust > 0) note += "Con estos datos no hay un valor de la hora que invierta el resultado. ";
  note += "Como el coste es lineal por comida, el número de comidas por semana no cambia cuál sale mejor, solo cuánto ahorras: cada comida sustituida suma " + eur(r.difComida * d.dias / 5, 2) + " al año.</p>";
  note += "<p><strong>No incluye:</strong> la calidad de lo que comes (no es consejo nutricional), el ocio o lo social de comer con otros, ni el ticket restaurante o la retribución en especie de tu empresa: su fiscalidad no está modelada, consúltalo con tu empresa. Los importes son tuyos o ejemplos, no precios de mercado; la compra se supone igual toda la temporada y que cocinas lo mismo que comerías fuera.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: g === 0 && d.sust > 0 ? r.ahorroTiempo : undefined, bigLabel: "de ahorro al año por cocinar" + (tiempo ? " (con tu tiempo valorado)" : " (sin valorar tu tiempo)"), format: eur,
    barsLabel: "Coste anual de las " + EM.num(r.comidasAnio, 0) + " comidas que haces fuera hoy",
    bars: [{ label: "Seguir fuera", value: r.costeFueraT, color: "a" }, { label: "Cocinar en casa", value: r.costeCasaT, color: "b" }],
    cols: ["Comer fuera", "Cocinar en casa"],
    rows: [
      ["Coste por comida (dinero)", eur(d.precio, 2), eur(d.racion, 2)],
      ["Coste por comida con tu tiempo", eur(d.precio + d.minDesp * d.vh / 60, 2), eur(d.racion + d.minCook * d.vh / 60, 2)],
      ["Dinero al año (todas las comidas fuera)", eur(r.gastoFuera), eur(r.gastoCasaMismas)],
      { label: "Ahorro anual de sustituir " + s + " por semana", values: [eur(r.ahorroDinero) + " en dinero", eur(r.ahorroTiempo) + " con tu tiempo"], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
