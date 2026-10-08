// Cuota de autonomos por rendimientos reales y regularizacion (2026). Parametros generados desde data/params.json (autonomo_2026.reta y autonomo_regularizacion_2026; fuentes y fechas alli).
// reta: [tabla, limite superior de rendimientos netos mensuales (null = sin limite), base minima, base maxima]; el limite 1.166,70 es exclusivo en el tramo 3 reducido.
var P = {"reta": [["reducida", 670, 653.59, 718.94], ["reducida", 900, 718.95, 900.0], ["reducida", 1166.7, 849.67, 1166.7], ["general", 1300, 950.98, 1300], ["general", 1500, 960.78, 1500], ["general", 1700, 960.78, 1700], ["general", 1850, 1143.79, 1850], ["general", 2030, 1209.15, 2030], ["general", 2330, 1274.51, 2330], ["general", 2760, 1356.21, 2760], ["general", 3190, 1437.91, 3190], ["general", 3620, 1519.61, 3620], ["general", 4050, 1601.31, 4050], ["general", 6000, 1732.03, 5101.2], ["general", null, 1928.1, 5101.2]], "tipo": 0.315, "gen": 0.07, "bmax": 5101.2, "plurRed": 0.055, "cc": 0.283, "bmin": 653.59};
function tramoDe(R) {
  var i, t;
  for (i = 0; i < P.reta.length; i++) {
    t = P.reta[i];
    if (t[1] === null || (i === 2 ? R < t[1] : R <= t[1])) return i;
  }
}
function calcular(d) {
  var prev = Math.max(+d.prev || 0, 0), real = Math.max(+d.real || 0, 0), base = Math.max(+d.base || 0, 0), cambio = Math.max(+d.cambio || 0, 0);
  var N = Math.min(Math.max(Math.round(+d.meses || 12), 1), 12), mc = Math.max(Math.round(+d.mcambio || 0), 0), plur = +d.plur ? 1 : 0;
  var cp = prev * (1 - P.gen), ip = tramoDe(cp), minP = P.reta[ip][2], maxP = P.reta[ip][3];
  var out = { compPrev: cp, tramoPrev: ip + 1, minPrev: minP, maxPrev: maxP, bloqueo: 0, tipo: P.tipo, meses: N };
  if (real <= 0) { out.bloqueo = 3; return out; }
  if (base < minP) { out.bloqueo = 1; return out; }
  if (base > P.bmax) { out.bloqueo = 2; return out; }
  if (cambio > 0 && (cambio < P.bmin || cambio > P.bmax || mc < 1 || mc >= N)) { out.bloqueo = 4; return out; }
  var media = cambio > 0 ? (base * (N - mc) + cambio * mc) / N : base;
  var cr = real * (1 - P.gen), ir = tramoDe(cr), minR = P.reta[ir][2], maxR = P.reta[ir][3];
  function regul(b) { return b < minR ? N * (minR - b) * P.tipo : (b > maxR ? -N * (b - maxR) * P.tipo : 0); }
  var reg = regul(media), lo = Math.max(minP, minR), rec = lo <= maxR ? Math.min(Math.max(cr, lo), maxR) : minP, defin = Math.min(Math.max(media, minR), maxR);
  out.compReal = cr; out.tramoReal = ir + 1; out.minReal = minR; out.maxReal = maxR; out.baseMedia = media; out.cuotaProv = base * P.tipo; out.pagado = media * N * P.tipo;
  out.regul = reg; out.baseDefinitiva = defin; out.definitiva = defin * N * P.tipo; out.recomendada = rec; out.regulRec = regul(rec);
  out.plurRed = plur ? P.plurRed * P.cc * media : 0; out.escenario = reg > 0 ? 1 : (reg < 0 ? 2 : 0); out.cuotaMinReal = minR * P.tipo; out.cuotaMaxReal = maxR * P.tipo;
  out.cuotaMinPrev = minP * P.tipo; out.cuotaMaxPrev = maxP * P.tipo; out.cuotaDef = defin * P.tipo; out.cuotaRec = rec * P.tipo; out.plur = plur;
  return out;
}
function nombreTramo(i) { return i <= 3 ? "Reducida " + i : "General " + (i - 3); }
function decidir(r, d) {
  var eurS = EM.eur, m = r.meses;
  if (r.bloqueo === 1) return { winner: "invalido", tone: "warn", verdict: "No puedes cotizar por una base menor que la base mínima de tu tramo previsto: con " + eurS(d.prev) + " al mes de rendimiento previsto estás en el tramo " + nombreTramo(r.tramoPrev) + " y la base mínima es " + eurS(r.minPrev, 2) + " (disposición transitoria 1.ª del Real decreto-ley 13/2022). Sube la base elegida o corrige tu previsión." };
  if (r.bloqueo === 2) return { winner: "invalido", tone: "warn", verdict: "La base máxima de cotización de 2026 es " + eurS(P.bmax, 2) + " al mes (Orden PJC/297/2026, art. 18): no puedes elegir una base mayor." };
  if (r.bloqueo === 3) return { winner: "invalido", tone: "warn", verdict: "Si no presentas la Renta, o la presentas sin declarar ingresos en estimación directa, la base definitiva es la mínima del grupo de cotización 7 (1.424,40 € al mes, art. 308.1.c.5.ª de la Ley General de la Seguridad Social). Si tuviste ingresos y tu rendimiento neto fue 0 o negativo, tu tramo real es Reducida 1 (hasta 670 €): indica 1 € para calcularlo." };
  if (r.bloqueo === 4) return { winner: "invalido", tone: "warn", verdict: "El cambio de base no es válido: la nueva base tiene que estar entre la mínima del tramo de la nueva previsión que declaras con el cambio (art. 45.2 del Reglamento General de Cotización; desde " + eurS(P.bmin, 2) + ") y " + eurS(P.bmax, 2) + " al mes y los meses con la nueva base, entre 1 y " + (m - 1) + " (menos que tus meses de alta). Pon 0 en la nueva base si no la cambias." };
  var v = "Con tus datos, tu rendimiento previsto te sitúa en el tramo " + nombreTramo(r.tramoPrev) + " y el real, en el tramo " + nombreTramo(r.tramoReal) + ". ";
  if (r.escenario === 1) {
    v += "Cotizas por una base media de " + eurS(r.baseMedia, 2) + " frente a la mínima de tu tramo real (" + eurS(r.minReal, 2) + "): la Seguridad Social te reclamaría unos " + eurS(r.regul) + " al regularizar, a ingresar hasta el último día del mes siguiente a la notificación, sin recargo ni intereses si pagas en ese plazo.";
  } else if (r.escenario === 2) {
    v += "Cotizas por una base media de " + eurS(r.baseMedia, 2) + ", por encima de la máxima de tu tramo real (" + eurS(r.maxReal, 2) + "): te devolverían de oficio unos " + eurS(-r.regul) + ", sin intereses.";
  } else {
    v += "Tu base media de " + eurS(r.baseMedia, 2) + " está entre la mínima (" + eurS(r.minReal, 2) + ") y la máxima (" + eurS(r.maxReal, 2) + ") de tu tramo real: no habría regularización y tus cuotas provisionales pasarían a ser definitivas.";
  }
  if (r.escenario !== 0 && Math.abs(r.regulRec) < 1) v += " Con una base de " + eurS(r.recomendada, 2) + " al mes (cuota de " + eurS(r.cuotaRec, 2) + ") no habría regularización si tu rendimiento real fuera ese.";
  return { winner: r.escenario === 1 ? "pagar" : (r.escenario === 2 ? "devolver" : "sin"), tone: r.escenario === 0 ? "ok" : "info", verdict: v };
}
function eur(x) { return EM.eur(x); }
var IDS = ["prev", "real", "base", "cambio", "mcambio", "meses"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.plur = document.getElementById("plur").value;
  return d;
}
function pintar() {
  var d = leer(), r = calcular(d), dec = decidir(r, d), e2 = function (x) { return EM.eur(x, 2); }, note = "";
  if (r.bloqueo) { EM.renderResult({ winner: dec.winner, tone: dec.tone, verdict: dec.verdict, note: "<p>La calculadora usa la tabla de cotización de 2026 de los autónomos (Orden PJC/297/2026, art. 18) y el procedimiento de regularización de la Ley General de la Seguridad Social (art. 308.1.c).</p>" }); return; }
  note += "<p><strong>Cómo se regulariza:</strong> la Seguridad Social compara tu base provisional media del año con la mínima y la máxima del tramo de tu rendimiento real: dentro de ese intervalo no hay regularización; por debajo pagas la diferencia (con el tipo del " + EM.num(P.tipo * 100, 1) + " %) y por encima te la devuelven (art. 308.1.c de la Ley General de la Seguridad Social y art. 46 del Reglamento General de Cotización). Se hace en el año siguiente, cuando la Agencia Tributaria le comunica tus rendimientos.</p>";
  if (r.recomendada !== d.base) note += "<p><strong>Base recomendada:</strong> " + e2(r.recomendada) + " al mes (cuota de " + e2(r.cuotaRec) + "). Si tu rendimiento real fuera el que has indicado, con esa base " + (Math.abs(r.regulRec) < 1 ? "no habría regularización" : (r.regulRec > 0 ? "aún tendrías que pagar " + eur(r.regulRec) + " (no puedes elegir una base menor que la mínima de tu tramo previsto)" : "te devolverían " + eur(-r.regulRec) + " (no puedes elegir una base menor que la mínima de tu tramo previsto)")) + ". Una devolución no es un ahorro: es dinero que adelantas sin intereses; una reclamación no es una multa si la pagas a tiempo.</p>";
  else note += "<p><strong>Base recomendada:</strong> la que has elegido (" + e2(d.base) + ") ya es la más cercana a tu rendimiento real dentro de los límites que permite la norma.</p>";
  note += "<p><strong>Si tu rendimiento cambia durante el año</strong> puedes cambiar la base hasta seis veces al año: la solicitud surte efecto el 1 de marzo, mayo, julio, septiembre, noviembre o enero según el bimestre en que la presentes (art. 45.1 del Reglamento General de Cotización). Cambiarla a tiempo evita la regularización.</p>";
  if (r.plur) note += "<p><strong>Pluriactividad:</strong> si no cubres la baja por enfermedad como autónomo, la cuota por contingencias comunes baja un 5,5 % (unos " + e2(r.plurRed) + " al mes con tu base media; Orden PJC/297/2026, art. 18.2.a); no cubrirla es voluntario si ya la tienes por tu trabajo por cuenta ajena (art. 315 de la Ley General de la Seguridad Social) y esa rebaja no está restada en el cálculo. Si tus cotizaciones por contingencias comunes suman más de " + e2(17323.68) + " al año, tienes derecho al reintegro del 50 % del exceso (Real decreto-ley 3/2026, art. 3.5): depende de tu nómina y no se calcula.</p>";
  note += "<p><strong>No incluye:</strong> autónomos societarios, familiares colaboradores, tarifa plana y otras bonificaciones (con tarifa plana, los primeros 12 meses no se regularizan, art. 46.1 del Reglamento General de Cotización), venta ambulante, RETA agrario, País Vasco y Navarra, recargos por impago, el cómputo por días de alta (aquí, meses completos) ni la tabla de 2027, que todavía no existe. El cese de actividad es obligatorio (art. 327.1 de la Ley General de la Seguridad Social) y va incluido en el 31,5 %. Tu rendimiento en la Renta puede diferir de tu previsión.</p>";
  EM.renderResult({
    winner: dec.winner, verdict: dec.verdict, tone: dec.tone,
    bigNumber: Math.abs(r.regul), bigLabel: r.escenario === 0 ? "de regularización" : (r.escenario === 1 ? "a pagar al regularizar" : "a devolver al regularizar"), format: eur,
    barsLabel: "Cuotas del año (" + r.meses + " " + (r.meses === 1 ? "mes" : "meses") + "): pagadas frente a definitivas",
    bars: [{ label: "Pagadas con tu base", value: r.pagado, color: "a" }, { label: "Definitivas con tu rendimiento real", value: r.definitiva, color: "b" }],
    cols: ["Con tu previsión", "Con tu rendimiento real"],
    rows: [
      ["Rendimiento neto mensual (tras el 7 % de gastos genéricos)", e2(r.compPrev), e2(r.compReal)],
      ["Tramo de la tabla de 2026", nombreTramo(r.tramoPrev), nombreTramo(r.tramoReal)],
      ["Base mínima – máxima del tramo", e2(r.minPrev) + " – " + e2(r.maxPrev), e2(r.minReal) + " – " + e2(r.maxReal)],
      ["Cuota mensual con la base mínima – máxima del tramo", e2(r.cuotaMinPrev) + " – " + e2(r.cuotaMaxPrev), e2(r.cuotaMinReal) + " – " + e2(r.cuotaMaxReal)],
      ["Base de cotización media del año (provisional → definitiva)", e2(r.baseMedia), e2(r.baseDefinitiva)],
      ["Cuota mensual (provisional → definitiva)", e2(r.baseMedia * P.tipo), e2(r.cuotaDef)],
      ["Cuotas del año (pagadas → definitivas)", eur(r.pagado), eur(r.definitiva)],
      { label: "Regularización estimada (+ pagas, − te devuelven)", values: ["", (r.regul > 0 ? "+" : "") + eur(r.regul)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
