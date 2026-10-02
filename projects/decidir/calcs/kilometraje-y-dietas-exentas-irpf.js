// Kilometraje y dietas exentas de IRPF (2026): ¿te compensa usar tu coche para la empresa? Cifras legales generadas desde data/params.json (kilometraje_dietas_2026; fuentes y fechas allí).
// km: EUR/km exento (Orden HFP/792/2023 sobre RIRPF art. 9.A.2.b); sin/con: manutención diaria exenta sin y con pernocta en España (art. 9.A.3.a); w: cotización del trabajador (LGSS 147.2.b: el exceso cotiza); umbral: empate práctico.
var P = {"km": 0.26, "sin": 26.67, "con": 53.34, "w": 0.065, "umbral": 0.05};
var MAXD = 365, MAXT = 47;
function pos(x) { return Math.max(+x || 0, 0); }
function calcular(d) {
  var r = { bloqueado: 0, escenario: 0, cobradoKm: 0, exentoKm: 0, tribKm: 0, exentoPeajes: 0, exentoSin: 0, tribSin: 0, exentoCon: 0, tribCon: 0, exentoTotal: 0, tribTotal: 0, ssExtra: 0, irpfExtra: 0, cargaExtra: 0, costeCoche: 0, netoCoche: 0, netoDietas: 0, cobradoDietas: 0, pagoEq: 0, ahorroIRPF: 0, ahorroSS: 0, ganNum: 0 };
  var km = pos(d.km), p = pos(d.pagokm), c = pos(d.costekm), pe = pos(d.peajes), ds = pos(d.diasSin), dc = pos(d.diasCon), di = pos(d.dieta);
  var t = Math.min(pos(d.tipo), MAXT) / 100, f, T, n, g;
  if (km <= 0 && ds + dc <= 0) { r.bloqueado = 1; return r; }
  if (ds + dc > MAXD) { r.bloqueado = 2; return r; }
  r.cobradoKm = km * p;
  r.exentoKm = km * Math.min(p, P.km); r.tribKm = km * Math.max(0, p - P.km);
  r.exentoPeajes = pe;
  r.exentoSin = ds * Math.min(di, P.sin); r.tribSin = ds * Math.max(0, di - P.sin);
  r.exentoCon = dc * Math.min(di, P.con); r.tribCon = dc * Math.max(0, di - P.con);
  r.cobradoDietas = (ds + dc) * di;
  r.exentoTotal = r.exentoKm + pe + r.exentoSin + r.exentoCon;
  T = r.tribKm + r.tribSin + r.tribCon; r.tribTotal = T;
  r.ssExtra = P.w * T; r.irpfExtra = (T - r.ssExtra) * t; r.cargaExtra = r.ssExtra + r.irpfExtra;
  f = P.w + (1 - P.w) * t;
  r.costeCoche = km * c;
  r.netoCoche = km * p - r.tribKm * f - km * c;
  r.netoDietas = r.cobradoDietas - (r.tribSin + r.tribCon) * f;
  r.pagoEq = c <= P.km ? c : P.km + (c - P.km) / ((1 - P.w) * (1 - t));
  r.ahorroIRPF = r.exentoTotal * (1 - P.w) * t; r.ahorroSS = r.exentoTotal * P.w;
  n = r.netoCoche;
  g = n >= P.umbral * r.costeCoche && n > 0 ? 1 : (n <= -P.umbral * r.costeCoche && n < 0 ? 2 : 0);
  r.ganNum = g;
  r.escenario = km <= 0 ? 5 : (g === 1 ? (r.tribKm <= 0 ? 1 : 2) : (g === 2 ? 4 : 3));
  return r;
}
// F = formateadores {eur, num} (en la página son EM.eur y EM.num; en los tests, simples)
function veredicto(d, r, F) {
  var e = F.eur, km = F.num(Math.round(pos(d.km)), 0), p = F.num(pos(d.pagokm), 2), q = F.num(P.km, 2), f = P.w + (1 - P.w) * Math.min(pos(d.tipo), MAXT) / 100;
  if (r.escenario === 1) return "Con tus datos, usar tu coche te compensa: la empresa te paga " + e(r.cobradoKm) + " al año por " + km + " km (" + p + " € por km, dentro de los " + q + " € por km exentos de IRPF y de cotización), tu coche te cuesta " + e(r.costeCoche) + " y te quedan " + e(r.netoCoche) + " al año.";
  if (r.escenario === 2) return "Con tus datos, usar tu coche te compensa por " + e(r.netoCoche) + " al año, pero no todo lo que cobras está exento: de los " + p + " € por km, lo que pasa de " + q + " € (" + e(r.tribKm) + " al año) tributa como sueldo y se queda en " + e(r.tribKm * (1 - f)) + " tras IRPF y cotización.";
  if (r.escenario === 3) return "Con tus datos, es un empate práctico (diferencia de " + e(Math.abs(r.netoCoche)) + " al año): lo que cobras por km queda casi igual que lo que te cuesta el coche, así que usarlo para la empresa ni te da ni te quita dinero.";
  if (r.escenario === 4) return "Con tus datos, usar tu coche no te compensa: pierdes " + e(-r.netoCoche) + " al año (cobras " + e(r.cobradoKm) + " y el coche te cuesta " + e(r.costeCoche) + "). Para no perder tendrías que cobrar al menos " + F.num(r.pagoEq, 3) + " € por km.";
  if (r.escenario === 5) return "Sin kilómetros, la calculadora solo evalúa las dietas: de " + e(r.cobradoDietas) + " al año, " + e(r.exentoSin + r.exentoCon) + " están exentos y " + e(r.tribSin + r.tribCon) + " tributan como sueldo.";
  return "";
}
function eur(x) { return EM.eur(x); }
function num(x, n) { return EM.num(x, n); }
var IDS = ["km", "pagokm", "costekm", "peajes", "diasSin", "diasCon", "dieta", "tipo"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; }); return d;
}
function pintar() {
  var d = leer(), r = calcular(d), F = { eur: eur, num: num }, tone = "ok", note = "", verdict, hayDietas = d.diasSin + d.diasCon > 0 && d.dieta > 0, f = P.w + (1 - P.w) * Math.min(d.tipo, MAXT) / 100;
  if (r.bloqueado === 1) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Escribe los kilómetros que haces al año con tu coche para el trabajo o los días de dieta que cobras.", note: "<p>La calculadora compara lo que te paga la empresa con lo que te cuesta tu coche y separa lo que tributa de lo que está exento de IRPF y de cotización.</p>" });
    return;
  }
  if (r.bloqueado === 2) {
    EM.renderResult({ winner: "invalido", tone: "warn", verdict: "Los días de dieta con y sin pernocta suman más de " + num(MAXD, 0) + ": un año tiene como máximo " + num(MAXD, 0) + " días.", note: "<p>Revisa los días con dieta sin pernocta y con pernocta.</p>" });
    return;
  }
  verdict = veredicto(d, r, F);
  if (r.escenario === 4 || r.escenario === 3) tone = "warn";
  if (d.km > 0) {
    note += "<p><strong>Kilometraje:</strong> están exentos " + eur(r.exentoKm) + " (hasta " + num(P.km, 2) + " € por km, si se justifica el desplazamiento)" + (r.tribKm > 0 ? " y tributan " + eur(r.tribKm) + " (IRPF y cotización)." : ".") + " Solo cuentan los viajes de trabajo fuera de tu centro habitual: ir de casa a tu centro de trabajo no es kilometraje exento.</p>";
    if (d.pagokm > 0 && d.pagokm < d.costekm) note += "<p>La empresa te paga menos por km (" + num(d.pagokm, 3) + " €) de lo que te cuesta el coche (" + num(d.costekm, 3) + " €): la diferencia la pones tú y no se descuenta en tu IRPF.</p>";
    note += "<p><strong>Punto de equilibrio:</strong> para no perder dinero con tu coche necesitas cobrar al menos " + num(r.pagoEq, 3) + " € por km" + (d.costekm > P.km ? " (por encima de " + num(P.km, 2) + " € una parte se va en impuestos y cotización)" : "") + ". Tu coche te cuesta " + eur(r.costeCoche) + " al año por esos km.</p>";
    if (d.peajes > 0) note += "<p><strong>Peajes y aparcamiento:</strong> " + eur(d.peajes) + " exentos si los justificas y la empresa te los reembolsa; si no te los reembolsa, son un coste tuyo más y hay que sumarlos al coste por km.</p>";
  }
  if (hayDietas) note += "<p><strong>Dietas de manutención en España:</strong> cobras " + eur(r.cobradoDietas) + " al año; " + eur(r.exentoSin + r.exentoCon) + " están exentos (hasta " + num(P.sin, 2) + " € al día sin pernocta y " + num(P.con, 2) + " € con pernocta) y " + eur(r.tribSin + r.tribCon) + " tributan; después de impuestos te quedan " + eur(r.netoDietas) + ". Esa dieta compensa tu comida fuera de casa: el cálculo no resta lo que gastas en comer.</p>";
  if (r.tribTotal > 0) note += "<p><strong>Impuestos extra por lo que supera los límites:</strong> " + eur(r.tribTotal) + " tributables suponen " + eur(r.irpfExtra) + " de IRPF (al " + num(Math.min(d.tipo, MAXT), 1) + " % de tipo marginal, tras restar la cotización) y " + eur(r.ssExtra) + " de cotización tuya a la Seguridad Social, " + eur(r.cargaExtra) + " en total.</p>";
  else note += "<p>Con estos importes todo lo que cobras está dentro de los límites exentos: sin IRPF ni cotización extra.</p>";
  note += "<p><strong>Lo que te ahorra la exención:</strong> si esos " + eur(r.exentoTotal) + " exentos te los pagaran como sueldo, pagarías unos " + eur(r.ahorroIRPF) + " de IRPF y " + eur(r.ahorroSS) + " de cotización más.</p>";
  note += "<p><strong>No incluye:</strong> vehículo de empresa, autónomos, transporte público (se justifica con factura y está exento entero), teletrabajo, País Vasco y Navarra, transporte de mercancías por carretera y personal de vuelo (reglas propias), desplazamientos de más de nueve meses continuados, dietas en el extranjero ni la estancia en hotel (exenta si la justificas). El importe por km depende de tu convenio o contrato, y el tipo marginal lo pones tú. Se supone que cotizas por debajo de la base máxima.</p>";
  EM.renderResult({
    winner: r.escenario, verdict: verdict, tone: tone,
    bigNumber: d.km > 0 ? r.netoCoche : undefined, bigLabel: d.km > 0 ? "al año " + (r.netoCoche >= 0 ? "a tu favor" : "en tu contra") + " usando tu coche" : "", format: eur,
    barsLabel: "Kilometraje: lo que cobras neto de impuestos y lo que te cuesta el coche",
    bars: d.km > 0 ? [{ label: "Cobras neto de impuestos", value: Math.max(r.cobradoKm - r.tribKm * f, 0), color: "a" }, { label: "Te cuesta el coche", value: Math.max(r.costeCoche, 0), color: "b" }] : [],
    cols: ["Exento", "Tributa"],
    rows: [
      ["Kilometraje (" + num(d.km, 0) + " km)", eur(r.exentoKm), eur(r.tribKm)],
      ["Peajes y aparcamiento justificados", eur(r.exentoPeajes), eur(0)],
      ["Dietas sin pernocta (" + num(d.diasSin, 0) + " días)", eur(r.exentoSin), eur(r.tribSin)],
      ["Dietas con pernocta (" + num(d.diasCon, 0) + " días)", eur(r.exentoCon), eur(r.tribCon)],
      { label: "Total", values: [eur(r.exentoTotal), eur(r.tribTotal)], strong: true },
      ["IRPF y cotización extra por lo que tributa", "–", eur(r.cargaExtra)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
