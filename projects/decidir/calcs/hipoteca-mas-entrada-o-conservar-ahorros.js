// Hipoteca: aportar mas entrada o conservar ese dinero como ahorro. Amortizacion francesa a tipo fijo.
// A (aportar): capital C-E a TIN-bajada (min 0); la cuota que te ahorras respecto a B se ahorra cada mes a la misma rentabilidad. B (conservar): capital C a TIN y E queda ahorrado a la rentabilidad neta anual (efectiva), capitalizacion mensual.
// Patrimonio neto a N anos (m meses) = ahorro acumulado - deuda pendiente. dif = patrimonio A - patrimonio B (> 0: aportar gana). Empate practico: |dif| < 5 % de E.
// Rentabilidad de equilibrio: biseccion en [-20, 20] % (+-999 si no hay cruce). Mes de equilibrio: ultimo mes con signo distinto al del horizonte, + 1 (0 = ventaja desde el principio).
function cuotaF(P, i, n) { return P <= 0 ? 0 : (i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n))); }
function saldoF(P, i, c, m) { return i === 0 ? P - c * m : P * Math.pow(1 + i, m) - c * (Math.pow(1 + i, m) - 1) / i; }
function acumF(c, j, m) { return j === 0 ? c * m : c * (Math.pow(1 + j, m) - 1) / j; }
function sg(x) { return x > 0.005 ? 1 : (x < -0.005 ? -1 : 0); }
function calcular(d) {
  var n = Math.round(d.plazo * 12), m = Math.round(d.anos * 12);
  var iB = d.tin / 1200, iA = Math.max(d.tin - d.baja, 0) / 1200;
  var CA = d.capital - d.extra, cA = cuotaF(CA, iA, n), cB = cuotaF(d.capital, iB, n), lib = cB - cA;
  function dif(k, rent) {
    var j = Math.pow(1 + rent / 100, 1 / 12) - 1;
    var sA = Math.max(saldoF(CA, iA, cA, k), 0), sB = Math.max(saldoF(d.capital, iB, cB, k), 0);
    return (acumF(lib, j, k) - sA) - (d.extra * Math.pow(1 + j, k) - sB);
  }
  var j0 = Math.pow(1 + d.rent / 100, 1 / 12) - 1;
  var sA = Math.max(saldoF(CA, iA, cA, m), 0), sB = Math.max(saldoF(d.capital, iB, cB, m), 0);
  var ahorroA = acumF(lib, j0, m), valor = d.extra * Math.pow(1 + j0, m), patA = ahorroA - sA, patB = valor - sB, df = patA - patB;
  var intA = cA * m - (CA - sA), intB = cB * m - (d.capital - sB);
  var tipo = Math.abs(df) < 0.05 * d.extra ? 2 : (df > 0 ? 0 : 1);
  var rentEq, lo = -20, hi = 20, it;
  if (dif(m, lo) <= 0) rentEq = -999; else if (dif(m, hi) >= 0) rentEq = 999;
  else { for (it = 0; it < 80; it++) { var mid = (lo + hi) / 2; if (dif(m, mid) > 0) lo = mid; else hi = mid; } rentEq = (lo + hi) / 2; }
  var sN = sg(df), mesEq = 0, k;
  if (sN !== 0) for (k = 1; k <= m; k++) if (sg(dif(k, d.rent)) !== sN) mesEq = k + 1;
  return { capitalA: CA, cuotaA: cA, cuotaB: cB, ahorroCuota: lib, saldoA: sA, saldoB: sB, ahorroA: ahorroA, valorAhorro: valor, patrimonioA: patA, patrimonioB: patB, dif: df,
    interesesA: intA, interesesB: intB, rentEq: rentEq, mesEq: mesEq, tipo: tipo, cubreCuotas: cB > 0 ? d.extra / cB : 0 };
}
function eur(x, d) { return EM.eur(x, d); }
var IDS = ["capital", "extra", "tin", "baja", "plazo", "anos", "rent"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pct(x) { return EM.num(x, 2) + " %"; }
function anosTxt(m) { var a = Math.floor(m / 12), r = m % 12; return (a > 0 ? a + (a === 1 ? " año" : " años") : "") + (a > 0 && r > 0 ? " y " : "") + (r > 0 ? r + (r === 1 ? " mes" : " meses") : ""); }
function pintar() {
  var d = leer(), k;
  for (k in d) if (k !== "rent" && d[k] < 0) return;
  if (d.capital <= 0 || d.extra <= 0 || d.plazo < 1 || d.anos < 1) { aviso("Escribe un capital, una entrada extra, un plazo y un horizonte mayores que 0.", "Sin capital, sin dinero para aportar o sin plazo no hay nada que comparar."); return; }
  if (d.extra >= d.capital) { aviso("La entrada extra debe ser menor que el capital de la hipoteca.", "Si aportas todo el capital, ya no hay hipoteca que comparar con conservar el dinero."); return; }
  if (d.anos > d.plazo || d.plazo > 40 || d.tin > 15 || d.rent > 20 || d.rent < -20) { aviso("Revisa los límites: el horizonte no puede superar el plazo, el plazo llega a 40 años, el TIN a 15 % y la rentabilidad va de -20 % a 20 %.", "Fuera de esos valores el resultado no sería realista."); return; }
  var r = calcular(d), t = r.tipo, w, v, a = Math.abs(r.dif), m = Math.round(d.anos * 12), N = anosTxt(m);
  if (t === 2) {
    w = "empate";
    v = "Con tus datos, es un empate práctico a " + N + ": la diferencia es de " + eur(a) + ", menos del 5 % de la entrada que valoras aportar. Decide por la liquidez: el dinero conservado puedes usarlo; el aportado ya no.";
  } else if (t === 0) {
    w = "aportar";
    v = "Con tus datos, aportar " + eur(d.extra) + " más de entrada gana por " + eur(a) + " de patrimonio en " + N + ": el interés que dejas de pagar supera lo que rendiría ese dinero al " + pct(d.rent) + " neto anual. A condición de que ese dinero no sea tu colchón de emergencia.";
  } else {
    w = "conservar";
    v = "Con tus datos, conservar " + eur(d.extra) + " gana por " + eur(a) + " de patrimonio en " + N + ": al " + pct(d.rent) + " neto anual rinde más de lo que te ahorrarías en intereses aportándolo, y además sigue disponible.";
  }
  var eq = r.rentEq <= -999 ? "A " + N + " conservar el ahorro gana con cualquier rentabilidad entre -20 % y 20 %." : (r.rentEq >= 999 ? "A " + N + " aportar gana con cualquier rentabilidad entre -20 % y 20 %." : "Aportar gana mientras tu ahorro rinda menos de " + pct(r.rentEq) + " neto anual a " + N + "; por encima, conservarlo sale mejor.");
  var mes = t === 2 ? "" : (r.mesEq > 1 ? " " + (t === 0 ? "Aportar" : "Conservar") + " va por delante de forma estable desde el mes " + r.mesEq + "." : " " + (t === 0 ? "Aportar" : "Conservar") + " va por delante desde el primer mes.");
  var note = "<p><strong>Lectura:</strong> " + eq + mes + " Con la entrada extra, la cuota baja de " + eur(r.cuotaB, 2) + " a " + eur(r.cuotaA, 2) + " al mes (" + eur(r.ahorroCuota, 2) + " menos). El dinero conservado cubriría unas " + EM.num(r.cubreCuotas, 0) + " cuotas de la hipoteca sin aportar.</p>";
  note += "<p><strong>Liquidez:</strong> el dinero que aportas a la entrada no lo recuperas salvo que vendas o refinancies; el que conservas lo tienes para imprevistos. Aunque aportar gane en euros, conviene mantener un colchón de emergencia aparte antes de aportar de más.</p>";
  note += "<p><strong>Condiciones y límites:</strong> la rentabilidad del ahorro es una hipótesis editable (neta de impuestos y comisiones), no una previsión ni un dato de ninguna entidad. Se supone tipo fijo todo el plazo y amortización francesa. Se supone que la cuota que te ahorras al aportar la ahorras cada mes a la misma rentabilidad; si la gastas, aportar sale peor de lo que muestra la tabla. El tipo no baja con más entrada salvo que lo indiques en «Bajada del TIN»; tu oferta manda. No incluye seguros, comisiones, gastos de compraventa ni impuestos sobre los intereses del ahorro. Información orientativa, no asesoramiento.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: "ok",
    bigNumber: a, format: EM.eur,
    bigLabel: t === 2 ? "de diferencia a " + N + " (empate práctico)" : (t === 0 ? "a favor de aportar más entrada a " + N : "a favor de conservar el ahorro a " + N),
    barsLabel: "Intereses de la hipoteca pagados a " + N,
    bars: [{ label: "Aportar" + (t === 0 ? " (gana)" : ""), value: r.interesesA, color: "a", fmt: EM.eur }, { label: "Conservar" + (t === 1 ? " (gana)" : ""), value: r.interesesB, color: "b", fmt: EM.eur }],
    cols: ["Aportar más entrada", "Conservar el ahorro"],
    rows: [
      ["Capital de la hipoteca", eur(r.capitalA), eur(d.capital)],
      ["Cuota mensual", eur(r.cuotaA, 2), eur(r.cuotaB, 2)],
      ["Intereses pagados a " + N, eur(r.interesesA), eur(r.interesesB)],
      ["Deuda pendiente", eur(r.saldoA), eur(r.saldoB)],
      ["Ahorro acumulado", eur(r.ahorroA), eur(r.valorAhorro)],
      { label: "Patrimonio neto a " + N, values: [eur(r.patrimonioA), eur(r.patrimonioB)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
