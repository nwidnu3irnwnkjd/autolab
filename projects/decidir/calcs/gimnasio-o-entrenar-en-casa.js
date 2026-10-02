// Gimnasio o entrenar en casa: coste total, coste por sesion real y sesiones/semana de equilibrio a N meses.
// Gimnasio = matricula + cuota x meses + desplazamiento x sesiones; casa = equipo - reventa al final (sin coste por sesion).
// Se compara el coste por sesion que de verdad haces en cada sitio; con 0 sesiones no hay coste por sesion (-1).
// ganador: 0 gimnasio, 1 casa, 2 empate, 3 sin sesiones.
function calcular(d) {
  var W = d.meses * 52 / 12, sg = d.sg * W, sc = d.sc * W;
  var fijoG = d.matricula + d.cuota * d.meses, cg = fijoG + d.desp * sg, cc = d.equipo - d.reventa;
  var cpsG = sg > 0 ? cg / sg : -1, cpsC = sc > 0 ? cc / sc : -1, g;
  if (sg <= 0 && sc <= 0) g = 3;
  else if (sg <= 0) g = 1;
  else if (sc <= 0) g = 0;
  else g = cpsG < cpsC - 0.005 ? 0 : (cpsG > cpsC + 0.005 ? 1 : 2);
  var eqG = (cpsC > d.desp) ? fijoG / (W * (cpsC - d.desp)) : -1;
  var eqC = cpsG > 0 ? cc / (W * cpsG) : -1;
  return { semanas: W, costeGim: cg, costeCasa: cc, sesGim: sg, sesCasa: sc, cpsGim: cpsG, cpsCasa: cpsC,
    eqGim: eqG, eqCasa: eqC, diferencia: cg - cc, ganador: g };
}
function n1(x) { return EM.num(x, x % 1 ? 1 : 0); }
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["cuota", "matricula", "desp", "sg", "sc", "equipo", "reventa", "meses"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.meses < 1 || d.meses > 120) {
    EM.renderResult({ winner: "invalido", verdict: "Indica un horizonte de entre 1 y 120 meses.", tone: "warn", note: "<p>Con otro horizonte el resultado no tendría sentido práctico.</p>" });
    return;
  }
  if (d.reventa > d.equipo) {
    EM.renderResult({ winner: "invalido", verdict: "Lo que recuperarías al final no puede superar lo que pagaste por el equipo.", tone: "warn", note: "<p>Pon la reventa en 0 si no esperas recuperar nada.</p>" });
    return;
  }
  if (d.sg > 21 || d.sc > 21) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa las sesiones por semana: más de 21 no es un dato realista.", tone: "warn", note: "<p>Cuenta solo las sesiones completas que de verdad haces.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, m = d.meses, per = EM.num(m, m % 1 ? 1 : 0) + (m === 1 ? " mes" : " meses");
  var w, verdict, tone = "ok";
  if (g === 3) {
    w = "sin-sesiones"; tone = "warn";
    verdict = "Con 0 sesiones en los dos sitios no hay coste por sesión que comparar: el gimnasio te cuesta " + eur(r.costeGim) + " y el equipo en casa " + eur(r.costeCasa) + " en " + per + " igualmente.";
  } else if (g === 1 && r.sesGim <= 0) {
    w = "casa";
    verdict = "Si no vas al gimnasio, pagarlo (" + eur(r.costeGim) + " en " + per + ") es dinero sin sesiones; entrenar en casa te sale a " + eur(r.cpsCasa, 2) + " por sesión.";
  } else if (g === 0 && r.sesCasa <= 0) {
    w = "gimnasio";
    verdict = "Si en casa no entrenas, el equipo (" + eur(r.costeCasa) + " netos en " + per + ") no sirve de nada; el gimnasio te sale a " + eur(r.cpsGim, 2) + " por sesión.";
  } else if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con estos datos el gimnasio y entrenar en casa cuestan lo mismo por sesión (" + eur(r.cpsGim, 2) + ") en " + per + ".";
  } else if (g === 0) {
    w = "gimnasio";
    verdict = "Con estos datos el gimnasio sale más barato por sesión: " + eur(r.cpsGim, 2) + " frente a " + eur(r.cpsCasa, 2) + " en casa, con " + n1(d.sg) + " sesiones a la semana en el gimnasio y " + n1(d.sc) + " en casa durante " + per + ". Entrenar en casa compensaría si hicieras más de " + EM.num(r.eqCasa, 1) + " sesiones por semana en casa (con tus sesiones actuales en el gimnasio).";
  } else {
    w = "casa";
    verdict = "Con estos datos entrenar en casa sale más barato por sesión: " + eur(r.cpsCasa, 2) + " frente a " + eur(r.cpsGim, 2) + " en el gimnasio, con " + n1(d.sc) + " sesiones a la semana en casa y " + n1(d.sg) + " en el gimnasio durante " + per + ". " +
      (r.eqGim > 0 ? "El gimnasio solo compensaría si fueras más de " + EM.num(r.eqGim, 1) + " veces por semana (con tus sesiones actuales en casa)." : "Con ese coste de desplazamiento, el gimnasio no llegaría a igualar a casa por mucho que fueras.");
  }
  var note = "<p><strong>Lectura:</strong> la comparación es por sesión que de verdad haces, no por lo que pagas: una cuota que no usas no sale en la cuenta del uso, pero sí en el total. ";
  if (r.eqGim > 0 && r.sesCasa > 0) note += "Con " + n1(d.sc) + " sesiones a la semana en casa, el gimnasio iguala su coste por sesión a partir de <strong>" + EM.num(r.eqGim, 1) + " sesiones por semana</strong>. ";
  if (r.eqCasa > 0 && r.sesGim > 0) note += "Con " + n1(d.sg) + " sesiones a la semana en el gimnasio, entrenar en casa iguala su coste por sesión a partir de <strong>" + EM.num(r.eqCasa, 1) + " sesiones por semana en casa</strong>. ";
  note += "El valor que pongas en «sesiones» debe ser lo que hiciste el último trimestre, no lo que te propones hacer.</p>";
  note += "<p><strong>No incluye:</strong> clases dirigidas, la motivación de ir a un sitio concreto, el espacio que ocupa el equipo, el valor de tu tiempo (suma al desplazamiento el valor de esos minutos si quieres contarlo), ni la salud o el rendimiento: esto no es consejo médico ni de entrenamiento. Se supone que el equipo no se renueva ni cuesta mantenimiento y que la cuota no cambia. Si tu horizonte es menor que la permanencia del gimnasio, usa la permanencia como horizonte.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: r.eqGim > 0 && g !== 3 ? r.eqGim : undefined, bigLabel: "sesiones por semana en el gimnasio para igualar el coste por sesión de casa", format: function (x) { return EM.num(x, 1); },
    barsLabel: "Coste total en " + per,
    bars: [{ label: "Gimnasio" + (w === "gimnasio" ? " (gana)" : ""), value: r.costeGim, color: "a" }, { label: "En casa" + (w === "casa" ? " (gana)" : ""), value: Math.max(r.costeCasa, 0), color: "b" }],
    cols: ["Gimnasio", "En casa"],
    rows: [
      ["Coste total en " + per, eur(r.costeGim), eur(r.costeCasa)],
      ["Sesiones en el periodo", EM.num(r.sesGim, 0), EM.num(r.sesCasa, 0)],
      { label: "Coste por sesión efectiva", values: [r.cpsGim < 0 ? "sin sesiones" : eur(r.cpsGim, 2), r.cpsCasa < 0 ? "sin sesiones" : eur(r.cpsCasa, 2)], strong: true },
      ["Sesiones por semana de equilibrio", r.eqGim > 0 ? EM.num(r.eqGim, 1) : "—", r.eqCasa > 0 ? EM.num(r.eqCasa, 1) : "—"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
