// Idiomas: coste total, por hora y meses hasta el objetivo en academia presencial, curso online e inmersion.
// Modelo: H horas de aprendizaje necesarias (hipotesis del usuario). Academia = referencia (eficacia 100 %). Online: se necesitan H / eficacia horas.
// Inmersion: HINM horas lectivas por semana (supuesto del modelo) y coste semanal todo incluido (viaje, curso, alojamiento) puesto por el usuario.
var HINM = 20, SEM_MES = 52 / 12;
function calcular(d) {
  var acadHora = d.acad * (1 - d.desc / 100) + d.desp;
  var horasOnl = d.horas / (d.ef / 100), semInm = d.horas / HINM;
  var cAcad = d.horas * acadHora, cOnl = horasOnl * d.onl, cInm = semInm * d.inm;
  var mejor = 0, min = cAcad;
  if (cOnl < min) { mejor = 1; min = cOnl; }
  if (cInm < min) { mejor = 2; min = cInm; }
  var otros = [cAcad, cOnl, cInm]; otros.splice(mejor, 1);
  var segundo = Math.min(otros[0], otros[1]);
  return {
    acadHora: acadHora, costeAcad: cAcad, costeOnl: cOnl, costeInm: cInm,
    horasOnl: horasOnl, semanasInm: semInm,
    mesesAcad: d.horas / d.hs / SEM_MES, mesesOnl: horasOnl / d.hs / SEM_MES, mesesInm: semInm / SEM_MES,
    horaAprOnl: d.onl / (d.ef / 100), horaInm: d.inm / HINM,
    efEquilibrio: acadHora > 0 ? d.onl / acadHora * 100 : -1,
    inmEquilibrio: semInm > 0 ? Math.min(cAcad, cOnl) / semInm : -1,
    mejor: mejor, ahorro: segundo - min, minimo: min
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["horas", "hs", "acad", "desp", "desc", "onl", "inm", "ef"];
var NOM = ["academia presencial", "curso online", "inmersión"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function mes(m) { return EM.num(m, 1) + " meses"; }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.horas < 1 || d.hs <= 0 || d.ef <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe al menos 1 hora necesaria, más de 0 horas de estudio por semana y una eficacia del online mayor que 0 %.", tone: "warn",
      note: "<p>Sin horas necesarias, tiempo disponible o eficacia no se puede estimar el coste ni el plazo.</p>" });
    return;
  }
  if (d.horas > 3000 || d.hs > 60 || d.desc > 100 || d.ef > 300) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: hasta 3.000 horas, 60 horas por semana, un descuento de como máximo 100 % y una eficacia del online de como máximo 300 %.", tone: "warn",
      note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), w = ["academia", "online", "inmersion"][r.mejor];
  var verdict = "Con estos datos, lo más barato es " + NOM[r.mejor] + ": " + eur(r.minimo) + " para llegar al objetivo, " + eur(r.ahorro) + " menos que la siguiente opción. ";
  if (r.mejor === 1) verdict += "Compensa mientras el online rinda al menos el " + (r.efEquilibrio >= 0 ? EM.num(r.efEquilibrio, 0) + " % de la academia" : "0 % de la academia") + " (tú supones el " + EM.num(d.ef, 0) + " %); depende de tu disciplina.";
  else if (r.mejor === 0) verdict += "Con tu eficacia estimada del " + EM.num(d.ef, 0) + " % el online costaría " + eur(r.costeOnl) + "; la academia gana mientras el online rinda menos de lo que marca el punto de equilibrio. Depende de tu disciplina y de tu objetivo.";
  else verdict += "La inmersión es la más barata solo con estos datos: si su coste semanal superase " + eur(r.inmEquilibrio) + ", dejaría de serlo. Depende de que puedas dedicarle semanas enteras.";
  var note = "<p><strong>Lectura:</strong> las horas necesarias y la eficacia relativa son hipótesis tuyas, no datos científicos; la página no promete resultados. ";
  note += "Academia: " + eur(r.acadHora, 2) + " por hora con descuento y desplazamiento, " + eur(r.costeAcad) + " en total y " + mes(r.mesesAcad) + " con " + EM.num(d.hs, 1) + " horas por semana. ";
  note += "Online: " + eur(d.onl, 2) + " por hora lectiva, que con una eficacia del " + EM.num(d.ef, 0) + " % equivale a " + eur(r.horaAprOnl, 2) + " por hora de aprendizaje; necesitas " + EM.num(r.horasOnl, 0) + " horas, " + eur(r.costeOnl) + " y " + mes(r.mesesOnl) + ". ";
  note += "Inmersión: " + EM.num(r.semanasInm, 1) + " semanas a " + eur(d.inm) + " (con " + HINM + " horas lectivas por semana, supuesto del modelo), " + eur(r.costeInm) + " y " + mes(r.mesesInm) + ", sin contar el tiempo libre ni el trabajo que dejes de hacer.</p>";
  note += "<p><strong>Punto de equilibrio:</strong> ";
  note += r.efEquilibrio >= 0 ? "el online cuesta lo mismo que la academia si rinde el " + EM.num(r.efEquilibrio, 0) + " % de ella; por encima, sale más barato. " : "la academia te cuesta 0 por hora, así que el online no la mejora en coste. ";
  note += "La inmersión pasa a ser la más cara cuando su coste semanal supera " + eur(r.inmEquilibrio) + " con tus datos.</p>";
  note += "<p><strong>Límites:</strong> no incluye precios de academias concretas, material, exámenes oficiales, el coste de oportunidad ni el tiempo de desplazamiento; todo son tus datos o ejemplos. El número de horas depende del nivel de partida y del objetivo, y no garantiza un resultado. Es información orientativa.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: "ok",
    bigNumber: r.minimo, bigLabel: "coste de la opción más barata hasta el objetivo", format: EM.eur,
    barsLabel: "Coste total hasta el objetivo",
    bars: [{ label: "Academia presencial" + (r.mejor === 0 ? " (más barata)" : ""), value: Math.max(r.costeAcad, 0), color: "a" },
      { label: "Curso online" + (r.mejor === 1 ? " (más barato)" : ""), value: Math.max(r.costeOnl, 0), color: "b" },
      { label: "Inmersión" + (r.mejor === 2 ? " (más barata)" : ""), value: Math.max(r.costeInm, 0), color: "c" }],
    cols: ["Academia", "Online", "Inmersión"],
    rows: [
      ["Coste total", eur(r.costeAcad), eur(r.costeOnl), eur(r.costeInm)],
      ["Coste por hora de aprendizaje", eur(r.acadHora, 2), eur(r.horaAprOnl, 2), eur(r.horaInm, 2)],
      ["Meses hasta el objetivo", mes(r.mesesAcad), mes(r.mesesOnl), mes(r.mesesInm)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
