// Punto de carga en casa: con o sin placas. Euros constantes, sin descuento.
// Hipotesis (data/params.json -> punto_carga_2026): 10 anos de horizonte; la energia de las placas se valora a la compensacion de excedentes que dejas de ingresar
// (0,07 EUR/kWh sin impuestos x 1,2718, igual que la calculadora de placas); coche de gasolina equivalente de 6,5 l/100 km (params.viaje_coche).
var S = { anos: 10, comp: 0.07 * 1.2718, cGas: 6.5 };
function pay(coste, ahorro) { return ahorro > 0 ? coste / ahorro : (coste <= 0 ? 0 : -1); }
function calcular(d) {
  var kwh = d.km * d.cons / 100, casa = kwh * d.pctCasa / 100, pub = kwh - casa, pp = d.pctPlacas / 100;
  var pCon = (1 - pp) * d.pelec + pp * S.comp;
  var cPub = kwh * d.ppub, cSin = casa * d.pelec + pub * d.ppub, cCon = casa * pCon + pub * d.ppub;
  var cGas = d.km * S.cGas / 100 * d.pgas, aSin = cPub - cSin, aCon = cPub - cCon;
  var den = S.anos * d.cons / 100 * d.pctCasa / 100 * (d.ppub - pCon);
  var pc = pay(d.coste, aCon);
  return {
    kwhAnual: kwh, kwhCasa: casa, precioCasaCon: pCon, costePublica: cPub, costeSin: cSin, costeCon: cCon, costeGasolina: cGas,
    ahorroSin: aSin, ahorroCon: aCon, paybackSin: pay(d.coste, aSin), paybackCon: pc,
    kmMin: den > 0 ? d.coste / den : (d.coste <= 0 ? 0 : -1), ahorroVsGasolina: cGas - cCon, instalar: pc >= 0 && pc <= S.anos ? 1 : 0
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["km", "cons", "pctCasa", "coste", "pelec", "ppub", "pctPlacas", "pgas"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function anos(x) { return EM.num(x, 1) + " años"; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: n }); }
function pintar() {
  var d = leer();
  if (d.km < 0 || d.cons < 0 || d.coste < 0 || d.pelec < 0 || d.ppub < 0 || d.pgas < 0 || d.pctCasa < 0 || d.pctPlacas < 0) return;
  if (d.pctCasa > 100 || d.pctPlacas > 100) {
    aviso("Los porcentajes de carga en casa y de placas no pueden pasar del 100 %.", "<p>Escribe un valor entre 0 y 100. Las placas solo producen de día: si cargas de noche, la parte cubierta por tus placas suele ser menor.</p>");
    return;
  }
  var r = calcular(d), N = S.anos, ok = r.instalar === 1, mejoraPlacas = r.ahorroCon > r.ahorroSin + 0.5;
  var verdict;
  if (r.ahorroCon <= 0) verdict = "Con estos números, el punto de carga no ahorra frente a cargar todo en pública: la electricidad de casa no te sale más barata.";
  else if (r.paybackCon === 0) verdict = "Con estos números, el punto de carga no te cuesta nada y ahorras " + EM.eur(r.ahorroCon) + " al año frente a la carga pública.";
  else if (ok) verdict = "Con estos números, el punto de carga se amortiza en unos " + EM.num(r.paybackCon, 1) + " años y ahorra " + EM.eur(r.ahorroCon) + " al año frente a la carga pública.";
  else verdict = "Con estos números, el punto de carga tarda unos " + EM.num(r.paybackCon, 1) + " años en amortizarse, más que los " + N + " años del modelo.";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.kmMin > 0) note += "con tus precios y tu % de carga en casa, el punto se amortiza en " + N + " años a partir de unos <strong>" + EM.num(r.kmMin) + " km al año</strong>; haces " + EM.num(d.km) + ". ";
  else if (r.kmMin < 0) note += "con tus precios no existe un número de km que amortice el punto, porque cada kWh en casa no sale más barato que en pública. ";
  note += "Cargar en casa cuesta " + EM.num(r.kwhAnual > 0 ? r.costeCon / r.kwhAnual * d.cons : 0, 2) + " € cada 100 km de media (con tus placas si las tienes), frente a " + EM.num(d.ppub * d.cons, 2) + " € en pública y " + EM.num(S.cGas * d.pgas, 2) + " € con el coche de gasolina equivalente (" + EM.num(S.cGas, 1) + " l/100 km). ";
  if (d.pctPlacas > 0 && d.pctCasa > 0) note += "Tus placas " + (mejoraPlacas ? "añaden " + EM.eur(r.ahorroCon - r.ahorroSin) + " de ahorro al año" : "no mejoran el ahorro") + " frente a cargar solo de la red (" + EM.eur(r.ahorroSin) + " sin placas). ";
  note += "</p>";
  note += "<p><strong>Qué incluye:</strong> energía de cada tipo de carga y el coste neto del punto que escribes (réstale tus ayudas). La energía de tus placas se valora a lo que dejarías de ingresar por verterla a la red (0,07 €/kWh sin impuestos por 1,2718 con impuestos, como en la calculadora de placas), no a coste cero. Euros constantes, sin descuento. <strong>No incluye:</strong> el coste de las placas, las bonificaciones fiscales de puntos de recarga (autonómicas o municipales: consulta tu ayuntamiento y tu comunidad), las tarifas nocturnas o con discriminación horaria (pueden bajar el precio de cargar en casa de noche, pero no se modelan), la obra en un garaje comunitario, la comisión por cargar en pública ni el valor de comprar el coche.</p>";
  EM.renderResult({
    winner: r.ahorroCon <= 0 ? "noahorra" : (ok ? "instalar" : "noinstalar"), verdict: verdict, tone: ok || r.paybackCon === 0 ? "ok" : "warn",
    bigNumber: r.ahorroCon > 0 && r.paybackCon > 0 ? r.paybackCon : r.ahorroCon, bigLabel: r.ahorroCon > 0 && r.paybackCon > 0 ? "años para amortizar el punto de carga" : "de ahorro al año frente a la carga pública",
    format: r.ahorroCon > 0 && r.paybackCon > 0 ? anos : EM.eur,
    barsLabel: "Coste anual de recargar los " + EM.num(r.kwhAnual) + " kWh de tus " + EM.num(d.km) + " km",
    bars: [{ label: "Gasolina (equivalente)", value: r.costeGasolina, color: "c", fmt: EM.eur }, { label: "Solo carga pública", value: r.costePublica, color: "b", fmt: EM.eur },
      { label: "Casa sin placas", value: r.costeSin, color: "a", fmt: EM.eur }, { label: "Casa con tus placas", value: r.costeCon, color: "ok", fmt: EM.eur }],
    cols: ["Sin placas", "Con tus placas"],
    rows: [
      ["Ahorro al año frente a pública", EM.eur(r.ahorroSin), EM.eur(r.ahorroCon)],
      ["Años para amortizar el punto", r.paybackSin >= 0 ? anos(r.paybackSin) : "No se amortiza", r.paybackCon >= 0 ? anos(r.paybackCon) : "No se amortiza"],
      { label: "Ahorro al año frente a gasolina", values: [EM.eur(r.costeGasolina - r.costeSin), EM.eur(r.ahorroVsGasolina)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
