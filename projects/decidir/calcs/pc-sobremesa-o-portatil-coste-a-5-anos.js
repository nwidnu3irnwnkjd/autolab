// Ordenador: sobremesa o portatil, coste total a N anios con extras, consumo electrico y valor residual opcional.
// Total = precio x (1 - residual) + extras + consumo (kW medio x horas/dia x 365 x anios x precio con impuestos).
// Extras del sobremesa = perifericos adicionales + ampliaciones + reparaciones previstas; del portatil = reparaciones previstas.
// Potencias medias en uso: hipotesis propias (no son de ningun fabricante). Coste anual = total / anios. Empate si la diferencia < 5 %.
// ganador: 0 sobremesa, 1 portatil, 2 empate. precioPortEq: precio maximo del portatil para igualar; extraSobEq: extras maximos del sobremesa.
var L = { iee: 0.0511269632, ieeMin: 0.001, iva: 0.21, kwSob: 0.15, kwPort: 0.04, dias: 365 };
function precioEfectivo(p) { return Math.max(p * (1 + L.iee), p + L.ieeMin) * (1 + L.iva); }
function calcular(d) {
  var pe = precioEfectivo(d.precioKwh), res = d.resid / 100, h = d.horas * L.dias * d.anios;
  var kwhS = L.kwSob * h, kwhP = L.kwPort * h, enS = kwhS * pe, enP = kwhP * pe;
  var netoS = d.precioSob * (1 - res), netoP = d.precioPort * (1 - res);
  var totS = netoS + d.extraSob + enS, totP = netoP + d.repPort + enP, dif = totS - totP;
  var m = Math.min(totS, totP), g = Math.abs(dif) < 0.05 * m || Math.abs(dif) < 1e-9 ? 2 : (dif > 0 ? 1 : 0);
  var ppEq = (res < 1) ? (totS - d.repPort - enP) / (1 - res) : -1;
  var esEq = totP - netoS - enS;
  return { kwhSob: kwhS, kwhPort: kwhP, energiaSob: enS, energiaPort: enP, totalSob: totS, totalPort: totP,
    anualSob: totS / d.anios, anualPort: totP / d.anios, diferencia: dif,
    precioPortEq: ppEq > 0 ? ppEq : -1, extraSobEq: esEq > 0 ? esEq : -1, precioEf: pe, ganador: g };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["precioSob", "precioPort", "extraSob", "repPort", "anios", "horas", "precioKwh", "resid"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.precioSob <= 0 || d.precioPort <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Indica el precio de compra del sobremesa y el del portátil (mayores que 0 €).", tone: "warn", note: "<p>Sin precios no hay coste que comparar.</p>" });
    return;
  }
  if (d.anios < 1 || d.anios > 15) {
    EM.renderResult({ winner: "invalido", verdict: "Indica una vida útil de entre 1 y 15 años.", tone: "warn", note: "<p>Es el periodo en que repartes el coste; no es una garantía del fabricante.</p>" });
    return;
  }
  if (d.horas > 24) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa las horas de uso: no puede haber más de 24 al día.", tone: "warn", note: "<p>Cuenta solo las horas con el equipo encendido y en uso.</p>" });
    return;
  }
  if (d.resid > 90) {
    EM.renderResult({ winner: "invalido", verdict: "El valor residual no puede superar el 90 % del precio de compra.", tone: "warn", note: "<p>Pon 0 si no esperas venderlo o reutilizarlo.</p>" });
    return;
  }
  var r = calcular(d), g = r.ganador, A = d.anios, per = EM.num(A, A % 1 ? 1 : 0) + (A === 1 ? " año" : " años"), ab = Math.abs(r.diferencia);
  var w, verdict, tone = "ok", an = Math.abs(r.anualSob - r.anualPort);
  if (g === 2) {
    w = "empate"; tone = "warn";
    verdict = "Con tus datos hay empate práctico: el sobremesa (" + eur(r.totalSob) + ") y el portátil (" + eur(r.totalPort) + ") cuestan casi lo mismo en " + per + ", con menos de un 5 % de diferencia.";
  } else if (g === 0) {
    w = "sobremesa";
    verdict = "Con tus datos, gana el sobremesa por " + eur(ab) + " en " + per + " (" + eur(an) + " al año): " + eur(r.totalSob) + " frente a " + eur(r.totalPort) + " del portátil." + (r.precioPortEq > 0 ? " El portátil igualaría si costara " + eur(r.precioPortEq) + " o menos." : "");
  } else {
    w = "portatil";
    verdict = "Con tus datos, gana el portátil por " + eur(ab) + " en " + per + " (" + eur(an) + " al año): " + eur(r.totalPort) + " frente a " + eur(r.totalSob) + " del sobremesa." + (r.extraSobEq > 0 ? " El sobremesa igualaría si sus periféricos, ampliaciones y reparaciones sumaran " + eur(r.extraSobEq) + " o menos." : " El sobremesa no igualaría ni sin extras.");
  }
  var note = "<p><strong>Lectura:</strong> la electricidad en " + per + " cuesta " + eur(r.energiaSob) + " con el sobremesa (" + EM.num(r.kwhSob, 0) + " kWh) y " + eur(r.energiaPort) + " con el portátil (" + EM.num(r.kwhPort, 0) + " kWh), con el precio de " + EM.num(r.precioEf, 3) + " €/kWh con impuestos. ";
  note += "El coste anual es " + eur(r.anualSob) + " con el sobremesa y " + eur(r.anualPort) + " con el portátil. ";
  if (r.precioPortEq > 0) note += "El punto de equilibrio del portátil, con el resto igual, es un precio de <strong>" + eur(r.precioPortEq) + "</strong>. ";
  note += "</p><p><strong>No incluye:</strong> la movilidad (un portátil te lo llevas y un sobremesa no), la potencia de cálculo que necesites, la pantalla integrada (en el sobremesa se paga aparte, dentro de los periféricos), el SAI, la obsolescencia anticipada ni descuentos financieros. Las potencias medias en uso (0,15 kW el sobremesa, 0,04 kW el portátil) son hipótesis del modelo, no datos de ningún fabricante, y se supone el mismo uso todos los días del año.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: ab, bigLabel: g === 2 ? "de diferencia en " + per : (g === 0 ? "menos con el sobremesa en " + per : "menos con el portátil en " + per), format: EM.eur,
    barsLabel: "Coste total en " + per,
    bars: [{ label: "Sobremesa" + (w === "sobremesa" ? " (gana)" : ""), value: r.totalSob, color: "a" }, { label: "Portátil" + (w === "portatil" ? " (gana)" : ""), value: r.totalPort, color: "b" }],
    cols: ["Sobremesa", "Portátil"],
    rows: [
      ["Compra (menos valor residual)", eur(d.precioSob * (1 - d.resid / 100)), eur(d.precioPort * (1 - d.resid / 100))],
      ["Periféricos, ampliaciones y reparaciones", eur(d.extraSob), eur(d.repPort)],
      ["Electricidad en el periodo", eur(r.energiaSob), eur(r.energiaPort)],
      { label: "Total en " + per, values: [eur(r.totalSob), eur(r.totalPort)], strong: true },
      ["Coste anual", eur(r.anualSob), eur(r.anualPort)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
