// Hotel o apartamento turístico en grupo: coste total y por persona y noche, noches y personas de equilibrio.
// Hotel = habitaciones x precio x noches + comer fuera x personas x noches. Apartamento = precio x noches + limpieza + cocinar x personas x noches.
// Todo son supuestos del usuario; tasas, parking y tarifa flexible van dentro del precio de la noche. La fianza se devuelve y no se cuenta. Días de comida = noches.
function calcular(d) {
  var P = d.personas, N = d.noches;
  var hotel = d.habs * d.precioHab * N + d.comerFuera * P * N;
  var apto = d.precioApto * N + d.limpieza + d.cocinar * P * N;
  var dif = hotel - apto, e = d.comerFuera - d.cocinar, d0 = d.habs * d.precioHab - d.precioApto;
  var den = d0 + P * e, nEq = den > 0 ? d.limpieza / den : -1, pEq = -1, p;
  if (e !== 0) { p = (d.limpieza / N - d0) / e; if (p > 0) pEq = p; }
  return {
    totalHotel: hotel, totalApto: apto, ppnHotel: hotel / (P * N), ppnApto: apto / (P * N), diferencia: dif,
    nochesEq: nEq, personasEq: pEq, ganador: dif < -1 ? 0 : (dif > 1 ? 1 : 2)
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["personas", "noches", "habs", "precioHab", "precioApto", "limpieza", "comerFuera", "cocinar"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.personas < 1 || d.noches < 1 || d.habs < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe al menos 1 persona, 1 noche y 1 habitación.", tone: "warn", note: "<p>Sin esos datos no hay nada que comparar.</p>" });
    return;
  }
  if (d.personas > 30 || d.noches > 60 || d.habs > 15 || d.habs > d.personas) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 30 personas, 60 noches y 15 habitaciones, y no más habitaciones que personas.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, abs = Math.abs(r.diferencia), P = d.personas, N = d.noches;
  var noches = EM.num(N, 0) + (N === 1 ? " noche" : " noches"), pers = EM.num(P, 0) + (P === 1 ? " persona" : " personas"), w, verdict;
  var ppn = Math.abs(r.ppnHotel - r.ppnApto);
  if (g === 2) {
    w = "empate";
    verdict = "Con estos datos el hotel y el apartamento cuestan lo mismo para " + pers + " y " + noches + " (unos " + eur(r.totalHotel) + "): estás en el punto de equilibrio.";
  } else if (g === 0) {
    w = "hotel";
    verdict = "Con estos datos compensa el hotel: te sale " + eur(abs) + " más barato que el apartamento para " + pers + " y " + noches + " (" + eur(ppn, 2) + " menos por persona y noche)" +
      (r.nochesEq > 1 ? ", pero a partir de " + EM.num(r.nochesEq, 1) + " noches el apartamento pasaría a salir más barato" : "") + ".";
  } else {
    w = "apartamento";
    verdict = "Con estos datos compensa el apartamento: te sale " + eur(abs) + " más barato que el hotel para " + pers + " y " + noches + " (" + eur(ppn, 2) + " menos por persona y noche)" +
      (r.nochesEq > 1 ? ", y desde " + EM.num(r.nochesEq, 1) + " noches sale más barato que el hotel" : ", y sale más barato desde la primera noche") + ".";
  }
  var note = "<p><strong>Lectura:</strong> ";
  if (r.nochesEq > 1) note += "con tus datos, a partir de " + EM.num(r.nochesEq, 1) + " noches el apartamento sale más barato que el hotel (antes de eso, la limpieza lo encarece). ";
  else if (r.nochesEq >= 0) note += "con tus datos el apartamento sale más barato desde la primera noche (la limpieza no basta para encarecerlo). ";
  else note += "con tus datos el hotel sale más barato o igual a cualquier número de noches. ";
  if (r.personasEq > 0 && d.comerFuera !== d.cocinar) note += "Con " + d.habs + " habitación(es) fija(s), el punto de equilibrio está en " + EM.num(r.personasEq, 1) + " personas: " + (d.comerFuera > d.cocinar ? "con más personas sale más barato el apartamento." : "con menos personas sale más barato el apartamento.") + " ";
  note += "El hotel cuesta " + eur(r.ppnHotel, 2) + " por persona y noche y el apartamento, " + eur(r.ppnApto, 2) + ".</p>";
  note += "<p>Todos los precios son ejemplos editables, no cotizaciones: pon los de tu reserva. Tasa turística (consulta tu destino), parking y tarifa flexible no tienen casilla: si los pagas, súmalos al precio por noche. La fianza del apartamento se devuelve y no se cuenta. No incluye comisiones de plataformas ni la comodidad de cada opción.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 2 ? "warn" : "ok",
    bigNumber: Math.min(r.ppnHotel, r.ppnApto), bigLabel: "€ por persona y noche en la opción más barata", format: function (x) { return EM.eur(x, 2); },
    barsLabel: "Coste total para " + pers + " y " + noches,
    bars: [{ label: "Hotel" + (w === "hotel" ? " (gana)" : ""), value: Math.max(r.totalHotel, 0), color: "a" }, { label: "Apartamento" + (w === "apartamento" ? " (gana)" : ""), value: Math.max(r.totalApto, 0), color: "b" }],
    cols: ["Hotel", "Apartamento"],
    rows: [
      ["Coste total", eur(r.totalHotel), eur(r.totalApto)],
      ["Alojamiento", eur(d.habs * d.precioHab * N), eur(d.precioApto * N + d.limpieza)],
      ["Comida", eur(d.comerFuera * P * N), eur(d.cocinar * P * N)],
      ["Por persona y noche", eur(r.ppnHotel, 2), eur(r.ppnApto, 2)],
      { label: "Noches desde las que el apartamento es más barato", values: [r.nochesEq > 1 ? EM.num(r.nochesEq, 1) : (r.nochesEq >= 0 ? "desde la 1.ª" : "no hay"), ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
