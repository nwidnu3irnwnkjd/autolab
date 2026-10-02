// Deposito, Letras del Tesoro o fondo monetario (IRPF 2026). Parametros: data/params.json -> deposito_letras_2026 (escala del ahorro, retencion, base 360; fuentes y fechas alli).
var P = {"aho": [[0, 19], [6000, 21], [50000, 23], [200000, 27], [300000, 30]], "ret": 19, "base360": 360, "anio": 365, "fgd": 100000};
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function tasa(base, tr) { var t = tr[0][1], i; for (i = 0; i < tr.length; i++) if (base > tr[i][0]) t = tr[i][1]; return t; }
// Impuesto adicional de un rendimiento g sumado a otras rentas del ahorro (solo si g > 0).
function impuesto(otras, g) { return g > 0 ? escala(otras + g, P.aho) - escala(otras, P.aho) : 0; }
function calcular(d) {
  var imp = Math.max(+d.importe || 0, 0), m = Math.min(Math.max(Math.round(+d.plazo || 0), 1), 12), otras = Math.max(+d.otras || 0, 0);
  var dl = +d.diasLetra > 0 ? Math.min(Math.max(+d.diasLetra, 1), 400) : P.anio * m / 12;
  var tin = +d.tin || 0, lt = +d.letras || 0, rent = +d.rentFondo || 0, com = Math.max(+d.comFondo || 0, 0);
  var z = { invalido: 0, plazo: m, diasLetra: 0, gDep: 0, gLet: 0, gFon: 0, taxDep: 0, taxLet: 0, taxFon: 0, netoDep: 0, netoLet: 0, netoFon: 0, retDep: 0, retLet: 0, retFon: 0,
    taeDep: 0, taeLet: 0, taeFon: 0, ganador: "empate", rentFondoEquilibrio: 0, tinEquilibrioLetras: 0, marginal: tasa(otras, P.aho), excedeFgd: 0, hayDatos: 0 };
  if (d.ambito !== "comun" && d.ambito !== "ceutamelilla") { z.invalido = 1; return z; }
  if (imp <= 0) return z;
  var f = 1 + (rent - com) / 100;
  if (f <= 0) { z.invalido = 2; return z; }
  var g = { Dep: imp * tin / 100 * m / 12, Let: imp * lt / 100 * dl / P.base360, Fon: imp * (Math.pow(f, m / 12) - 1) };
  var k, t, mejor;
  z.hayDatos = 1; z.diasLetra = dl;
  for (k in g) {
    t = impuesto(otras, g[k]);
    z["g" + k] = g[k]; z["tax" + k] = t; z["neto" + k] = g[k] - t;
    z["ret" + k] = k === "Let" ? 0 : (g[k] > 0 ? g[k] * P.ret / 100 : 0);
    z["tae" + k] = 100 * (Math.pow((imp + g[k] - t) / imp, k === "Let" ? P.anio / dl : 12 / m) - 1);
  }
  mejor = Math.max(g.Dep, g.Let);
  z.rentFondoEquilibrio = 100 * (Math.pow(1 + mejor / imp, 12 / m) - 1) + com;
  z.tinEquilibrioLetras = 100 * g.Let / (imp * m / 12);
  var arr = [["dep", z.netoDep], ["letras", z.netoLet], ["fondo", z.netoFon]].sort(function (a, b) { return b[1] - a[1]; });
  z.ganador = arr[0][1] - arr[1][1] < 1 ? "empate" : arr[0][0];
  z.segundo = arr[1][0]; z.tercero = arr[2][0]; z.diferencia = arr[0][1] - arr[1][1];
  z.marginal = tasa(otras + Math.max(g.Dep, g.Let, g.Fon, 0), P.aho);
  z.excedeFgd = imp > P.fgd ? 1 : 0;
  return z;
}
function eur(x) { return EM.eur(x); }
function pct(x, dec) { return EM.num(x, dec === undefined ? 2 : dec) + " %"; }
var NOM = { dep: "el depósito", letras: "las Letras del Tesoro", fondo: "el fondo monetario" };
var NOMC = { dep: "El depósito", letras: "Las Letras del Tesoro", fondo: "El fondo monetario" };
var IDS = ["importe", "plazo", "tin", "letras", "diasLetra", "rentFondo", "comFondo", "otras"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ambito = document.getElementById("ambito").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.importe < 0 || d.plazo < 1 || d.plazo > 12 || d.diasLetra < 0 || d.otras < 0 || d.comFondo < 0) return;
  var r = calcular(d), m = r.plazo;
  if (r.invalido === 1) {
    EM.renderResult({ winner: "invalido", verdict: "Esta calculadora no cubre tu territorio: haciendas forales.", tone: "warn",
      note: "<p>El País Vasco y Navarra tienen su propia escala del ahorro, distinta de la estatal y autonómica que usa esta calculadora. Consulta la normativa de tu administración tributaria.</p>" });
    return;
  }
  if (r.invalido === 2) {
    EM.renderResult({ winner: "invalido2", verdict: "Con esa rentabilidad y esa comisión el fondo perdería todo su valor: revisa los datos.", tone: "warn" });
    return;
  }
  if (!r.hayDatos) {
    EM.renderResult({ winner: "nada", verdict: "Escribe el importe que quieres colocar para ver cuánto te queda neto con cada opción.", tone: "info" });
    return;
  }
  var w = r.ganador, tone = "ok", verdict;
  if (w === "empate") verdict = "Con estos datos las mejores opciones te dejan lo mismo neto (diferencia de menos de 1 €) en " + m + (m === 1 ? " mes" : " meses") + " tras el IRPF.";
  else verdict = NOMC[w] + (w === "letras" ? " te dejan " : " te deja ") + eur(r.diferencia) + " más netos que " + NOM[r.segundo] + " en " + m + (m === 1 ? " mes" : " meses") + ", tras el IRPF del ahorro. No es una recomendación: depende de los tipos que te ofrezcan.";
  if (w === "fondo" || (r.gFon > 0 && r.netoFon >= Math.max(r.netoDep, r.netoLet) - 1)) { verdict += " Ojo: la rentabilidad del fondo es una hipótesis tuya y no está garantizada."; tone = "warn"; }
  var note = "";
  if (r.gFon < 0) note += "<p><strong>Con esa rentabilidad el fondo pierde dinero:</strong> pierdes " + eur(-r.gFon) + " y no pagas IRPF, pero tampoco lo recuperas en impuestos; la calculadora no compensa la pérdida con otras rentas.</p>";
  note += "<p><strong>Lectura del impuesto:</strong> intereses del depósito, rendimiento de las Letras y ganancia del fondo tributan en la base del ahorro con la misma escala (19 %, 21 %, 23 %, 27 % y 30 %), así que el IRPF baja a las tres y, con estos supuestos, no cambia cuál sale mejor: lo que cambia es cuánto te queda. Excepción no modelada: si tienes pérdidas patrimoniales (del año o pendientes de los 4 anteriores), compensan al 100 % la ganancia del fondo y solo hasta el 25 % los intereses del depósito y de las Letras (art. 49), lo que favorece al fondo y puede cambiar el orden. Con tus otras rentas del ahorro, tu siguiente euro de interés tributa al " + pct(r.marginal, 0) + ".</p>";
  note += "<p><strong>Retención y renta:</strong> el depósito te retiene " + eur(r.retDep) + " (19 %) al cobrar los intereses y el fondo " + eur(r.retFon) + " al reembolsar; las Letras no llevan retención (art. 75.3.b del Reglamento, salvo cuentas basadas en operaciones sobre Letras), así que el impuesto (" + eur(r.taxLet) + ") lo pagas en la declaración. La retención es un pago a cuenta: se regulariza en la renta con el impuesto final que ves en la tabla.</p>";
  note += "<p><strong>Punto de equilibrio:</strong> el fondo monetario iguala al mejor de depósito y Letras si rinde un " + pct(r.rentFondoEquilibrio) + " anual bruto antes de comisión (tu comisión de gestión ya está restada); un depósito iguala a las Letras con un TIN de " + pct(r.tinEquilibrioLetras) + ". Las Letras se calculan con " + EM.num(r.diasLetra, 0) + " días reales de vida y base 360 (tipo simple del Tesoro); el depósito, con " + m + (m === 1 ? " mes" : " meses") + " de 365 días al año.</p>";
  if (r.excedeFgd) note += "<p><strong>Más de 100.000 €:</strong> el Fondo de Garantía de Depósitos cubre hasta 100.000 € por depositante y entidad; reparte el depósito entre entidades o ten en cuenta que lo que exceda no está cubierto.</p>";
  note += "<p><strong>Límites:</strong> no incluye la compensación de pérdidas del art. 49, la liquidez (el depósito y las Letras a vencimiento no se pueden retirar sin penalización o sin vender), comisiones de custodia o suscripción ni el riesgo del fondo; en Ceuta y Melilla la deducción del 60 % de la cuota (art. 68.4 de la Ley del IRPF) solo afecta a las rentas obtenidas allí (en general no a las Letras ni a los fondos) y no se calcula; si te aplica, puede cambiar el orden entre las opciones.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: tone,
    bigNumber: Math.max(r.netoDep, r.netoLet, r.netoFon), bigLabel: "de ganancia neta la mejor opción en " + m + (m === 1 ? " mes" : " meses"), format: EM.eur,
    barsLabel: "Ganancia neta tras IRPF en " + m + (m === 1 ? " mes" : " meses"),
    bars: [{ label: "Depósito" + (w === "dep" ? " (gana)" : ""), value: Math.max(r.netoDep, 0), color: "a" },
           { label: "Letras" + (w === "letras" ? " (gana)" : ""), value: Math.max(r.netoLet, 0), color: "b" },
           { label: "Fondo" + (w === "fondo" ? " (gana)" : ""), value: Math.max(r.netoFon, 0), color: "a" }],
    cols: ["Depósito", "Letras", "Fondo"],
    rows: [
      ["Rendimiento bruto", eur(r.gDep), eur(r.gLet), eur(r.gFon)],
      ["IRPF final (base del ahorro)", eur(r.taxDep), eur(r.taxLet), eur(r.taxFon)],
      ["Retención al cobrar (pago a cuenta)", eur(r.retDep), eur(r.retLet), eur(r.retFon)],
      { label: "Ganancia neta", values: [eur(r.netoDep), eur(r.netoLet), eur(r.netoFon)], strong: true },
      ["TAE neta equivalente", pct(r.taeDep), pct(r.taeLet), pct(r.taeFon)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
