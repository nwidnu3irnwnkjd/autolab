// Mover consumos (lavadora, lavavajillas, termo) a horas valle de la 2.0TD: ahorro anual de energia frente a llano o punta.
// kWh desplazados = (kWh por uso x usos/semana + kWh de termo/semana) x 365/7 x % desplazable. Precio efectivo = (energia + IEE con minimo por kWh) x IVA.
// franja: 0 llano, 1 punta, 2 mitad punta y mitad llano (franja a la que lo usas hoy). El ahorro es la diferencia de precio efectivo entre esa franja y el valle.
// estado: 0 compensa, 1 casi igual (precios planos), 2 el valle es mas caro, 3 nada que mover. ganador: 0 mover, 1 no mover, 2 empate.
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21 };
function pe(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var kwhAnio = (d.kwhUso * d.usosSem + d.kwhTermo) * 365 / 7, kwhDesp = kwhAnio * d.pctDesp / 100;
  var origen = d.franja === 1 ? pe(d.precioPunta) : (d.franja === 2 ? (pe(d.precioPunta) + pe(d.precioLlano)) / 2 : pe(d.precioLlano));
  var valle = pe(d.precioValle), dif = origen - valle, ahorro = kwhDesp * dif;
  var estado, ganador;
  if (kwhDesp <= 0) { estado = 3; ganador = 1; }
  else if (Math.abs(ahorro) < 1) { estado = 1; ganador = 2; }
  else if (ahorro < 0) { estado = 2; ganador = 1; }
  else { estado = 0; ganador = 0; }
  return { kwhAnio: kwhAnio, kwhDesp: kwhDesp, precioOrigen: origen, precioValle: valle, ahorroKwh: dif, ahorroAnual: ahorro, ahorroMes: ahorro / 12,
    ahorroMax: kwhAnio * dif, costeHoy: kwhDesp * origen, costeValle: kwhDesp * valle, estado: estado, ganador: ganador };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["kwhUso", "usosSem", "kwhTermo", "pctDesp", "precioPunta", "precioLlano", "precioValle", "franja"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.pctDesp > 100) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa el porcentaje desplazable: no puede pasar del 100 %.", tone: "warn", note: "<p>Es la parte de esos consumos que puedes mover a las horas valle.</p>" });
    return;
  }
  if (d.usosSem > 70) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los usos por semana: más de 70 son más de 10 al día.", tone: "warn", note: "<p>Cuenta lavadoras y lavavajillas juntas.</p>" });
    return;
  }
  var r = calcular(d), w, v, tone = "ok", fr = d.franja === 1 ? "la punta" : (d.franja === 2 ? "la punta y el llano a partes iguales" : "el llano");
  if (r.estado === 3) {
    w = "nada"; tone = "warn";
    v = "Con estos datos no hay consumo que mover: pon los kWh de tus aparatos y un porcentaje desplazable mayor que 0.";
  } else if (r.estado === 1) {
    w = "empate"; tone = "warn";
    v = "Con estos datos mover " + EM.num(r.kwhDesp, 0) + " kWh al valle apenas cambia nada (" + EM.eur(r.ahorroAnual) + " al año): el valle cuesta casi lo mismo que " + fr + ". Con una tarifa de precio único no hay ahorro por horas.";
  } else if (r.estado === 2) {
    w = "no";  tone = "warn";
    v = "Con estos precios no compensa mover consumos al valle: cuesta " + EM.eur(-r.ahorroAnual) + " más al año que hacerlo en " + fr + ". Revisa los precios por periodo de tu tarifa.";
  } else {
    w = "mover";
    v = "Con estos datos compensa mover " + EM.num(r.kwhDesp, 0) + " kWh al año a las horas valle: ahorras " + EM.eur(r.ahorroAnual) + " al año con impuestos (" + EM.eur(r.ahorroMes) + " al mes) frente a hacerlo en " + fr + ".";
  }
  var note = "<p><strong>Lectura:</strong> tus aparatos gastan " + EM.num(r.kwhAnio, 0) + " kWh al año y mueves el " + EM.num(d.pctDesp, 0) + " % (" + EM.num(r.kwhDesp, 0) + " kWh). Cada kWh movido ahorra " + EM.num(r.ahorroKwh, 3) + " € con impuestos (de " + EM.num(r.precioOrigen, 3) + " a " + EM.num(r.precioValle, 3) + " €/kWh). ";
  if (r.estado === 0 && d.pctDesp < 100) note += "Si movieras todo, el ahorro llegaría a " + EM.eur(r.ahorroMax) + " al año. ";
  note += "El ahorro sale de la diferencia de precio, no de gastar menos: mueves la hora, no el consumo.</p>" +
    "<p><strong>Cuándo es valle:</strong> en la tarifa 2.0TD el valle va de 0 a 8 h todos los días y todo el día en sábados, domingos y festivos nacionales; ahí tu consumo ya es valle sin hacer nada. Si ya pones la lavadora de noche o en fin de semana, baja el porcentaje desplazable.</p>" +
    "<p><strong>No incluye:</strong> el ruido y la comodidad de poner aparatos de noche, el consumo de espera ni que un termo caliente pierda calor entre medias. Los precios por periodo por defecto son la media de los últimos 12 meses del PVPC (energía sin impuestos) y no valen para una tarifa de precio fijo o con tus propios periodos: pon los de tu contrato. Península y Baleares.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: tone,
    bigNumber: r.ahorroAnual, bigLabel: "al año con impuestos moviendo " + EM.num(r.kwhDesp, 0) + " kWh a valle", format: EM.eur,
    barsLabel: "Coste anual de esos " + EM.num(r.kwhDesp, 0) + " kWh (con impuestos)",
    bars: [{ label: "En " + fr, value: r.costeHoy, color: "a" }, { label: "En valle", value: r.costeValle, color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Consumo de los aparatos (kWh al año)", EM.num(r.kwhAnio, 0)],
      ["kWh movidos al valle", EM.num(r.kwhDesp, 0)],
      ["Ahorro por kWh movido", EM.num(r.ahorroKwh, 3) + " €"],
      { label: "Ahorro al año", values: [EM.eur(r.ahorroAnual)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
