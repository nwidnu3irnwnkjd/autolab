// Coste del primer anio de un bebe como presupuesto personal (sin cifras legales). Todo son entradas tuyas.
// bruto = equipamiento + 12 x (panales y alimentacion) + ropa + 12 x salud + cuidado x meses de cuidado + ingreso perdido.
// total = bruto - ayudas (las ayudas no superan el bruto). Ahorro previo = equipamiento + 3 meses de gasto corriente (panales, alimentacion, salud, ropa).
// flexibles = equipamiento + ropa + salud privada. mayor = indice de la partida mayor (0 equip, 1 panales/alim, 2 ropa, 3 salud, 4 cuidado, 5 ingreso perdido; empate: la primera).
function calcular(d) {
  var p = [d.equip, 12 * d.panalim, d.ropa, 12 * d.salud, d.cuidado * d.mesesC, d.perdida];
  var bruto = 0, i, mayor = 0;
  for (i = 0; i < 6; i++) { bruto += p[i]; if (p[i] > p[mayor]) mayor = i; }
  var ayu = Math.min(d.ayudas, bruto), total = bruto - ayu, flex = p[0] + p[2] + p[3];
  return {
    bruto: bruto, ayudasAplicadas: ayu, total: total, mensualMedio: total / 12,
    ahorroPrevio: d.equip + 3 * (d.panalim + d.salud) + d.ropa / 4,
    mayor: bruto > 0 ? mayor : -1, pesoMayor: bruto > 0 ? p[mayor] / bruto * 100 : 0,
    flexibles: flex, pesoFlex: bruto > 0 ? flex / bruto * 100 : 0, ahorro10: flex * 0.1,
    cuidadoTotal: p[4], panalimTotal: p[1], saludTotal: p[3]
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["equip", "panalim", "ropa", "salud", "cuidado", "mesesC", "perdida", "ayudas"];
var NOM = ["el equipamiento inicial", "los pañales y la alimentación", "la ropa", "la salud privada", "la guardería o cuidadora", "el ingreso que dejas de cobrar"];
var ETQ = ["Equipamiento inicial (una vez)", "Pañales y alimentación (12 meses)", "Ropa", "Salud privada opcional (12 meses)", "Guardería o cuidadora", "Ingreso que dejas de cobrar"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.mesesC > 12) {
    EM.renderResult({ winner: "invalido", verdict: "Indica entre 0 y 12 meses de guardería o cuidadora dentro del primer año.", tone: "warn", note: "<p>Solo se cuenta el primer año del bebé.</p>" });
    return;
  }
  var r = calcular(d);
  if (r.bruto <= 0) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe al menos una partida mayor que 0 para calcular el coste del primer año.", tone: "warn", note: "<p>Sin ninguna partida no hay presupuesto que calcular.</p>" });
    return;
  }
  var v = [d.equip, r.panalimTotal, d.ropa, r.saludTotal, r.cuidadoTotal, d.perdida];
  var verdict = "Con tus datos, el primer año cuesta " + eur(r.total) + " (unos " + eur(r.mensualMedio) + " al mes); la partida mayor es " + NOM[r.mayor] + " (" + EM.num(r.pesoMayor, 0) + " % del total antes de ayudas).";
  if (r.flexibles > 0) verdict += " Las partidas más flexibles (equipamiento, ropa y salud privada) suman " + eur(r.flexibles) + " (" + EM.num(r.pesoFlex, 0) + " %): recortar un 10 % de ellas ahorraría " + eur(r.ahorro10) + ".";
  else verdict += " No has puesto partidas flexibles (equipamiento, ropa ni salud privada): el margen para reducir está en la guardería, la cuidadora o el ingreso que dejas de cobrar.";
  if (r.ayudasAplicadas > 0) verdict += " Ya descuentas " + eur(r.ayudasAplicadas) + " de ayudas que has escrito tú.";
  var rows = [], i;
  for (i = 0; i < 6; i++) rows.push([ETQ[i], eur(v[i]), EM.num(v[i] / r.bruto * 100, 0) + " %"]);
  rows.push(["Ayudas y deducciones que escribes (resta)", "−" + eur(r.ayudasAplicadas), ""]);
  rows.push({ label: "Coste total del primer año", values: [eur(r.total), ""], strong: true });
  var note = "<p><strong>Lectura:</strong> para llegar al nacimiento con colchón, el ahorro necesario antes del parto es de <strong>" + eur(r.ahorroPrevio) + "</strong>: el equipamiento más tres meses de pañales, alimentación, salud privada y ropa (los tres meses son un supuesto de esta página, no una norma). La media mensual es " + eur(r.mensualMedio) + ", pero el gasto no es uniforme: el equipamiento se concentra antes del parto y el ingreso perdido, durante el permiso o la reducción. ";
  note += "Para la guardería usa <a href=\"/decidir/guarderia-cuidadora-o-reducir-jornada/\">guardería, cuidadora o reducir jornada</a> y para el ingreso que dejas de cobrar, <a href=\"/decidir/permiso-nacimiento-cuanto-cobro-y-como-repartir/\">permiso de nacimiento: cuánto cobro</a>.</p>";
  note += "<p><strong>Límites:</strong> los importes son hipótesis tuyas o de ejemplo, no precios de mercado. Las ayudas y deducciones dependen de tu situación y comunidad: consulta las tuyas y escribe solo lo que te corresponda. Si cuentas guardería y pérdida de ingresos en los mismos meses, revisa que no sea la misma necesidad de cuidado contada dos veces. No incluye imprevistos, ni inflación, ni el coste de oportunidad en tu carrera, y no da consejo sanitario.</p>";
  EM.renderResult({
    winner: "mayor" + r.mayor, verdict: verdict, tone: r.ayudasAplicadas >= r.bruto ? "warn" : "ok",
    bigNumber: r.total, bigLabel: "de coste total del primer año", format: EM.eur,
    barsLabel: "Coste del primer año por partida",
    bars: [0, 1, 2, 3, 4, 5].map(function (j) { return { label: ETQ[j], value: v[j], color: ["a", "b", "c", "a", "b", "c"][j] }; }),
    cols: ["Importe", "% del total"],
    rows: rows,
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
