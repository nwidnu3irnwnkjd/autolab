// Movil nuevo o reacondicionado/usado: coste total de propiedad por anio de vida esperada.
// Coste = precio x (1 - reventa) + riesgo esperado de reparacion fuera de garantia (prob x coste x anios sin garantia).
// Garantia legal del nuevo: 3 anios (TRLGDCU art. 120.1, BOE consolidado). Reacondicionado: garantia que indique el usuario.
// Reventa: mismo % del precio pagado en ambos (hipotesis editable). Sin coste de oportunidad del dinero.
var GAR_NUEVO = 3, VMAX = 30;
function costeAno(precio, rv, prob, rep, vida, gar) {
  var riesgo = prob / 100 * rep * Math.max(0, vida - gar);
  return { riesgo: riesgo, tco: precio * (1 - rv / 100) + riesgo };
}
function calcular(d) {
  var n = costeAno(d.pnuevo, d.reventa, d.prob, d.rep, d.vidaN, GAR_NUEVO);
  var r = costeAno(d.prec, d.reventa, d.prob, d.rep, d.vidaR, d.garR);
  var anoN = n.tco / d.vidaN, anoR = r.tco / d.vidaR, dif = anoN - anoR;
  var best = Math.abs(dif) < 0.5 ? 2 : (dif > 0 ? 1 : 0);
  var pe = d.reventa < 100 ? Math.max(0, (anoN * d.vidaR - r.riesgo) / (1 - d.reventa / 100)) : 0;
  var desde = -1, v;
  for (v = VMAX; v >= 1; v--) { if (costeAno(d.pnuevo, d.reventa, d.prob, d.rep, v, GAR_NUEVO).tco / v <= anoR) desde = v; else break; }
  return { tcoNuevo: n.tco, tcoReac: r.tco, anoNuevo: anoN, anoReac: anoR, riesgoNuevo: n.riesgo, riesgoReac: r.riesgo,
    residualNuevo: d.pnuevo * d.reventa / 100, residualReac: d.prec * d.reventa / 100, diferenciaAno: dif, mejor: best,
    precioEquilibrio: pe, desdeAnos: desde };
}
function eur(x) { return EM.eur(x); }
var IDS = ["pnuevo", "prec", "vidaN", "vidaR", "garR", "prob", "rep", "reventa"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function anos(x) { return EM.num(x, x % 1 ? 1 : 0) + (x === 1 ? " año" : " años"); }
function pintar() {
  var d = leer();
  if (d.pnuevo <= 0 || d.prec <= 0 || d.vidaN < 1 || d.vidaR < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe los dos precios (mayores que 0) y al menos 1 año de vida esperada para cada móvil.", tone: "warn",
      note: "<p>Sin precios ni vida esperada no hay coste por año que comparar.</p>" });
    return;
  }
  if (d.garR < 0 || d.prob < 0 || d.prob > 100 || d.rep < 0 || d.reventa < 0 || d.reventa >= 100) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los porcentajes: la probabilidad va de 0 a 100 %, la reventa debe ser menor que 100 % y ningún valor puede ser negativo.", tone: "warn",
      note: "<p>Con una reventa del 100 % o más el móvil no costaría nada.</p>" });
    return;
  }
  var r = calcular(d), b = r.mejor, rv = d.reventa;
  var verdict;
  if (b === 2) verdict = "Con estos datos, el nuevo y el reacondicionado cuestan lo mismo: unos " + EM.eur(r.anoNuevo, 2) + " al año.";
  else {
    var gana = b === 0 ? "el nuevo" : "el reacondicionado", pierde = b === 0 ? "del reacondicionado" : "del nuevo";
    verdict = "Con estos datos, " + gana + " sale más barato: " + EM.eur(b === 0 ? r.anoNuevo : r.anoReac, 2) + " al año frente a " + EM.eur(b === 0 ? r.anoReac : r.anoNuevo, 2) + " " + pierde + " (" + EM.eur(Math.abs(r.diferenciaAno), 2) + " al año de diferencia). ";
    verdict += r.precioEquilibrio > 0 ? "El reacondicionado compensa mientras cueste menos de " + EM.eur(r.precioEquilibrio) + "; el tuyo cuesta " + EM.eur(d.prec) + "." : "Con estos datos el reacondicionado no compensa a ningún precio.";
  }
  var note = "<p><strong>Lectura:</strong> el nuevo tiene " + GAR_NUEVO + " años de garantía legal y el reacondicionado, la que has indicado (" + anos(d.garR) + "). El riesgo esperado de reparación fuera de garantía es de " + EM.eur(r.riesgoNuevo) + " en el nuevo y " + EM.eur(r.riesgoReac) + " en el reacondicionado (probabilidad por coste por años sin garantía). ";
  if (r.desdeAnos > 0) note += "Con tus demás datos, el nuevo sale más barato por año si dura " + anos(r.desdeAnos) + " o más; has puesto " + anos(d.vidaN) + ". ";
  else note += "Con tus demás datos, el nuevo no llega a salir más barato por año aunque dure hasta " + VMAX + " años. ";
  note += "</p><p><strong>Garantía:</strong> el texto consolidado del TRLGDCU (art. 120.1, redacción del Real Decreto-ley 7/2021) fija tres años desde la entrega para los bienes vendidos por un empresario; en los de segunda mano se puede pactar un plazo menor, nunca inferior a un año. Entre particulares no rige esa garantía. Comprueba qué garantía figura en tu factura.</p>";
  note += "<p><strong>Límites:</strong> los precios, años de vida, probabilidades y reventa son hipótesis tuyas o ejemplos. No se valora la calidad del reacondicionado, el estado de la batería, las actualizaciones de seguridad que reciba cada modelo, el impacto ambiental ni el coste de oportunidad del dinero.</p>";
  EM.renderResult({
    winner: ["nuevo", "reacondicionado", "empate"][b], verdict: verdict, tone: b === 2 ? "warn" : "ok",
    bigNumber: Math.min(r.anoNuevo, r.anoReac), bigLabel: "al año con la opción más barata", format: function (x) { return EM.eur(x, 2); },
    barsLabel: "Coste por año de vida esperada",
    bars: [{ label: "Nuevo" + (b === 0 ? " (más barato)" : ""), value: Math.max(r.anoNuevo, 0), color: "a" }, { label: "Reacondicionado/usado" + (b === 1 ? " (más barato)" : ""), value: Math.max(r.anoReac, 0), color: "b" }],
    cols: ["Nuevo", "Reacondicionado/usado"],
    rows: [
      ["Coste total de propiedad", EM.eur(r.tcoNuevo), EM.eur(r.tcoReac)],
      ["Coste por año", EM.eur(r.anoNuevo, 2), EM.eur(r.anoReac, 2)],
      ["Riesgo esperado de reparación", EM.eur(r.riesgoNuevo), EM.eur(r.riesgoReac)],
      ["Valor de reventa al final", EM.eur(r.residualNuevo), EM.eur(r.residualReac)],
      ["Garantía (años)", EM.num(GAR_NUEVO, 0), EM.num(d.garR, d.garR % 1 ? 1 : 0)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
