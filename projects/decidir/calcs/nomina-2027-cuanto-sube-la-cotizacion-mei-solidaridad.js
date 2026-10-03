// Nómina 2026 frente a 2027: cuánto sube lo que cotizas por el MEI y la cotización adicional de solidaridad. Parámetros: data/params.json -> cotizacion_mei_solidaridad_2027 (fuentes y fechas allí; base máxima de 2027 = supuesto editable).
// LGSS 127 bis y DT 43.ª (MEI), 19 bis y DT 42.ª (solidaridad), DT 38.ª (base máxima), Orden PJC/297/2026 arts. 2, 4, 16, 17 y 33.
var P = {"b26": 5101.2, "cc": 4.7, "mei": {"26": 0.15, "27": 0.17}, "ind": 1.55, "tem": 1.6, "fp": 0.1, "tr": [0.1, 0.5], "sol": {"26": [0.19, 0.21, 0.24], "27": [0.23, 0.25, 0.29]}};
function r2(x) { return Math.round(x * 100 + 1e-7) / 100; }
function cuota(y, B, m, temporal) {
  var base = Math.min(m, B), des = temporal ? P.tem : P.ind;
  var cc = r2(base * P.cc / 100), mei = r2(base * P.mei[y] / 100), de = r2(base * des / 100), fp = r2(base * P.fp / 100);
  var ex = Math.max(0, m - B), s = P.sol[y];
  var t1 = Math.min(ex, P.tr[0] * B), t2 = Math.min(Math.max(ex - P.tr[0] * B, 0), (P.tr[1] - P.tr[0]) * B), t3 = Math.max(ex - P.tr[1] * B, 0);
  var sol = r2(r2(t1 * s[0] / 100) + r2(t2 * s[1] / 100) + r2(t3 * s[2] / 100));
  return { mei: mei, sol: sol, total: r2(cc + mei + de + fp + sol) };
}
// d: bruto (anual, €), contrato indefinido|temporal, base27 (€/mes, base máxima supuesta de 2027)
function calcular(d) {
  var anual = +d.bruto || 0, B27 = +d.base27 || 0, temp = d.contrato === "temporal";
  if (!(anual > 0) || !(B27 > 0)) return { bloqueado: 1, escenario: 0 };
  var m = anual / 12, c26 = cuota("26", P.b26, m, temp), c27 = cuota("27", B27, m, temp), c26b = cuota("26", B27, m, temp);
  return { bloqueado: 0, escenario: m > B27 ? 2 : 1, mes26: c26.total, mes27: c27.total, anual26: 12 * c26.total, anual27: 12 * c27.total,
    sube: 12 * (c27.total - c26.total), dMei: 12 * (c27.mei - c26b.mei), dSol: 12 * (c27.sol - c26b.sol), dBase: 12 * (c26b.total - c26.total),
    mei27: 12 * c27.mei, sol26: 12 * c26.sol, sol27: 12 * c27.sol, solMes27: c27.sol, umbral27: B27 * 12, umbral26: P.b26 * 12, pctBruto: 12 * (c27.total - c26.total) / anual * 100 };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["bruto", "base27"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.contrato = document.getElementById("contrato").value;
  return d;
}
function pintar() {
  var d = leer(), r = calcular(d);
  if (r.bloqueado) {
    EM.renderResult({ winner: "bloqueado", tone: "warn", verdict: d.bruto > 0 ? "La base máxima de 2027 tiene que ser mayor que 0: pon la de 2026 (5.101,20 €) si no sabes otra." : "Escribe tu salario bruto anual.", note: "<p>La calculadora compara 2026 con 2027 para el mismo sueldo.</p>" });
    return;
  }
  var v, tone = "ok", pos = function (x, a, b) { return eur(Math.abs(x)) + (x >= 0 ? a : b); };
  var cab = "Con " + eur(d.bruto) + " brutos al año, " + (r.escenario === 1 ? "por debajo" : "por encima") + " de la base máxima de 2027 que supones (" + eur(d.base27) + " al mes), en 2027 cotizarás " + pos(r.sube, " más", " menos") + " al año que en 2026";
  var par = [pos(r.dMei, " más", " menos") + " por el MEI (0,17 % en vez de 0,15 %)"];
  if (r.escenario === 2) par.push(pos(r.dSol, " más", " menos") + " por la cotización de solidaridad" + (r.dBase === 0 ? ", que pasa de " + eur(r.sol26) + " a " + eur(r.sol27) + " al año" : ""));
  if (r.dBase !== 0) par.push(pos(r.dBase, " más", " menos") + " por la base máxima que supones frente a la de 2026 (cotizas sobre una base " + (r.dBase > 0 ? "más alta" : "más baja") + ")");
  v = cab + (r.escenario === 1 && r.dBase === 0 ? " (" + EM.num(r.pctBruto, 2) + " % de tu bruto): el MEI pasa de 0,15 % a 0,17 % (" + pos(r.dMei, " más", " menos") + ") y en 2027 no pagas solidaridad." : ": " + (par.length > 2 ? par.slice(0, -1).join(", ") + " y " + par[par.length - 1] : par.join(" y ")) + (r.escenario === 1 ? "; en 2027 no pagas solidaridad." : "."));
  var rows = [["Cotización del trabajador al mes en 2026", eur(r.mes26)], ["Cotización del trabajador al mes en 2027", eur(r.mes27)], ["Total al año en 2026", eur(r.anual26)], ["Total al año en 2027", eur(r.anual27)],
    { label: "Diferencia al año", values: [eur(r.sube)], strong: true }, ["De ella, por el MEI", eur(r.dMei)], ["De ella, por la solidaridad", eur(r.dSol)]];
  if (r.dBase !== 0) rows.push(["De ella, por la base máxima que supones", eur(r.dBase)]);
  var note = d.base27 < P.b26 ? "<p><strong>Aviso:</strong> has puesto una base máxima de 2027 menor que la de 2026 (" + eur(P.b26) + "); la ley prevé subirla cada año (disposición transitoria 38.ª), no bajarla. El cálculo sigue con tu cifra.</p>" : "";
  note += "<p><strong>Dato que falta:</strong> la base máxima de 2027 no está publicada (no hay orden de cotización ni Presupuestos de 2027). Usa 5.101,20 € al mes, la de 2026, por defecto: cámbiala cuando se publique. La ley la sube cada año (disposición transitoria 38.ª: revalorización más 1,2 puntos), así que la cifra con la de 2026 es la subida mínima. Si sube, también suben el tope del MEI y el punto desde el que empieza la solidaridad (hoy " + eur(r.umbral26) + " brutos al año con esa base).</p>";
  EM.renderResult({ winner: "e" + r.escenario, verdict: v, tone: tone, bigNumber: Math.abs(r.sube), bigLabel: r.sube >= 0 ? "más al año en 2027" : "menos al año en 2027", format: EM.eur, cols: ["Importe"], rows: rows, note: note });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
