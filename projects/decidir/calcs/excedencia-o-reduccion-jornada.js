// Excedencia o reducción de jornada: coste neto mensual y total de cada opción frente a seguir igual.
// Coste neto = ingreso neto que pierdes - ayudas - ahorro en cuidados evitados. Reducción: pierdes el % neto indicado (por defecto, el mismo % que la reducción) y evitas ese % de los cuidados; excedencia: pierdes el 100 % del neto y evitas el 100 % de los cuidados.
// La cotización se mide en meses equivalentes de base completa no cotizada (hipótesis del usuario), no en euros de pensión.
function calcular(d) {
  var hay = d.red > 0, pr = d.perdida > 0 ? d.perdida : d.red, M = d.dur;
  var perdRed = hay ? d.neto * pr / 100 : 0, ahRed = hay ? d.cuidados * d.red / 100 : 0, ayRed = hay ? d.ayudas : 0;
  var cRed = hay ? perdRed - ayRed - ahRed : 0, cExc = d.neto - d.ayudas - d.cuidados;
  var cotRed = d.cotRed > 0 ? d.cotRed : d.red;
  var g = 0, mn = 0;
  if (hay && cRed < mn) { g = 1; mn = cRed; }
  if (cExc < mn) { g = 2; mn = cExc; }
  return {
    perdidaMesRed: perdRed, ahorroCuidadosRed: ahRed, costeMesRed: cRed, costeMesExc: cExc,
    costeTotalRed: cRed * M, costeTotalExc: cExc * M,
    equilibrioCuidadosRed: hay ? (perdRed - ayRed) / (d.red / 100) : -1, equilibrioCuidadosExc: d.neto - d.ayudas,
    costePor10Red: hay ? cRed / (d.red / 10) : 0, costePor10Exc: cExc / 10,
    mesesCotRed: hay ? M * cotRed / 100 : 0, mesesCotExc: M * d.cotExc / 100,
    cobertura: d.neto > 0 ? d.cuidados / d.neto * 100 : 0, pctPerdidaRed: pr, ganador: g
  };
}
function eur(x, n) { return EM.eur(x, n); }
function pos(x) { return x > 0 ? EM.eur(x) : "0 € (ya sale a favor)"; }
var IDS = ["neto", "red", "perdida", "dur", "ayudas", "cuidados", "cotRed", "cotExc"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.neto <= 0 || d.dur < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un sueldo neto mayor que 0 y al menos 1 mes de duración.", tone: "warn", note: "<p>Sin sueldo o sin duración no hay nada que comparar.</p>" });
    return;
  }
  if (d.red > 100 || d.perdida > 100 || d.cotRed > 100 || d.cotExc > 100 || d.dur > 120) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: los porcentajes no pueden pasar del 100 % ni la duración de 120 meses.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), M = d.dur, hay = d.red > 0, g = r.ganador;
  var meses = EM.num(M, 0) + (M === 1 ? " mes" : " meses");
  var verdict, w = ["seguir", "reduccion", "excedencia"][g];
  var txtExc = "la excedencia " + eur(r.costeMesExc) + " al mes (" + eur(r.costeTotalExc) + " en " + meses + ")";
  if (hay) {
    var txtRed = "reducir tu jornada un " + EM.num(d.red, 1) + " % te cuesta " + eur(r.costeMesRed) + " al mes (" + eur(r.costeTotalRed) + " en " + meses + ")";
    if (g === 0) verdict = "Con estos datos, seguir igual es lo que menos cuesta en euros: " + txtRed + " y " + txtExc + ", ya descontadas ayudas y cuidados evitados. Es solo la parte económica.";
    else verdict = "Con estos datos, " + (g === 1 ? "reducir tu jornada un " + EM.num(d.red, 1) + " %" : "la excedencia") + " te deja " + eur(-(g === 1 ? r.costeMesRed : r.costeMesExc)) + " al mes a favor en neto, porque las ayudas y los cuidados evitados superan lo que dejas de cobrar.";
  } else {
    if (g === 0) verdict = "Con una reducción del 0 % no hay reducción que calcular; la excedencia te cuesta " + eur(r.costeMesExc) + " al mes (" + eur(r.costeTotalExc) + " en " + meses + ") tras ayudas y cuidados evitados, y seguir igual es lo que menos cuesta en euros.";
    else verdict = "Con una reducción del 0 % no hay reducción que calcular; la excedencia te deja " + eur(-r.costeMesExc) + " al mes a favor en neto, porque las ayudas y los cuidados evitados superan lo que dejas de cobrar.";
  }
  var note = "<p><strong>Lectura:</strong> ";
  if (hay) note += "para que la reducción no te cueste nada en neto, los cuidados que evitas tendrían que valer " + pos(r.equilibrioCuidadosRed) + " al mes; para la excedencia, " + pos(r.equilibrioCuidadosExc) + " al mes (con tus ayudas). Tus cuidados evitados de " + eur(d.cuidados) + " al mes son el " + EM.num(r.cobertura, 0) + " % de tu sueldo neto. ";
  else note += "para que la excedencia no te cueste nada en neto, los cuidados que evitas tendrían que valer " + pos(r.equilibrioCuidadosExc) + " al mes (con tus ayudas); los tuyos son " + eur(d.cuidados) + " al mes. ";
  if (hay) note += d.perdida > 0 ? "Has indicado que la reducción te hace perder el " + EM.num(d.perdida, 1) + " % del neto. " : "Se supone que pierdes en neto el mismo % que reduces; el IRPF y la cotización pueden suavizar esa pérdida: si tienes una nómina simulada, indica tu % real de pérdida neta. ";
  note += "</p>";
  if (hay && (d.red < 12.5 || d.red > 50)) note += "<p><strong>Ojo:</strong> el artículo 37.6 del Estatuto de los Trabajadores prevé una reducción de entre un octavo (12,5 %) y la mitad (50 %) de la jornada; fuera de ese tramo habría que pactarla con la empresa o en tu convenio.</p>";
  if (d.dur > 36) note += "<p><strong>Ojo:</strong> la excedencia por cuidado de cada hijo del artículo 46.3 tiene un máximo de tres años; comprueba qué tipo de excedencia te corresponde, porque las voluntarias del 46.2 tienen otro régimen.</p>";
  note += "<p><strong>Cotización (hipótesis tuya):</strong> ";
  note += hay ? "la reducción equivale a " + EM.num(r.mesesCotRed, 1) + " meses de base completa sin cotizar y la excedencia, a " + EM.num(r.mesesCotExc, 1) + ". " : "la excedencia equivale a " + EM.num(r.mesesCotExc, 1) + " meses de base completa sin cotizar. ";
  note += "No es una cifra de pensión: el sistema prevé reconocimientos de cotización por cuidado de hijos que no se modelan aquí; consulta la Seguridad Social.</p>";
  note += "<p><strong>Qué no incluye:</strong> la promoción y la carrera, el derecho a prestaciones (paro, incapacidad) durante la medida, el efecto de la medida en tu IRPF salvo el % de pérdida neta que indiques, el bienestar o el tiempo con la familia, y las condiciones de tu convenio o tu empresa. Las ayudas se aplican a las dos opciones: si solo cubren una, pon 0 y suma la ayuda a mano. El Estatuto de los Trabajadores fija derechos y reserva de puesto distintos en cada caso: consulta el texto y tu convenio. Información orientativa, no asesoramiento laboral.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 0 ? "warn" : "ok",
    bigNumber: hay ? r.costeMesRed : r.costeMesExc, bigLabel: hay ? "coste neto al mes de reducir la jornada" : "coste neto al mes de la excedencia", format: EM.eur,
    barsLabel: "Coste neto en " + meses,
    bars: (hay ? [{ label: "Reducir jornada", value: Math.max(r.costeTotalRed, 0), color: "a" }] : []).concat([{ label: "Excedencia", value: Math.max(r.costeTotalExc, 0), color: "b" }, { label: "Seguir igual", value: 0, color: "c" }]),
    cols: ["Reducir jornada", "Excedencia", "Seguir igual"],
    rows: [
      ["Ingreso neto que dejas de cobrar al mes", hay ? eur(r.perdidaMesRed) : "—", eur(d.neto), eur(0)],
      ["Ayudas al mes", hay ? eur(d.ayudas) : "—", eur(d.ayudas), eur(0)],
      ["Cuidados evitados al mes", hay ? eur(r.ahorroCuidadosRed) : "—", eur(d.cuidados), eur(0)],
      ["Coste neto al mes", hay ? eur(r.costeMesRed) : "—", eur(r.costeMesExc), eur(0)],
      ["Coste neto en " + meses, hay ? eur(r.costeTotalRed) : "—", eur(r.costeTotalExc), eur(0)],
      ["Coste neto al mes por cada 10 % de jornada que recuperas", hay ? eur(r.costePor10Red) : "—", eur(r.costePor10Exc), "—"],
      { label: "Cuidados evitados al mes para que no cueste nada", values: [hay ? pos(r.equilibrioCuidadosRed) : "—", pos(r.equilibrioCuidadosExc), "—"], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
