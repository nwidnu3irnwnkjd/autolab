// Rescate del plan de pensiones: capital, renta o mixto (IRPF 2026). Parametros generados desde data/params.json -> irpf_2026 (fuentes y fechas alli).
// est: escala estatal general; minE/descE: minimo del contribuyente y por descendientes (arts. 57-58); ccaa: escala general y minimos propios (null = los estatales).
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "minE": 5550, "descE": [2400, 2700, 4000, 4500], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": [5790, [2510, 2820, 4170, 4700]], "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": [6105, [2640, 2970, 4400, 4950]], "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": [5550, [2400, 2970, 4400, 4950]], "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": [5606, [2424, 2727, 4040, 4545]], "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": [5789, [2503, 2816, 4172, 4694]], "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": [5956.65, [2575.85, 2897.83, 4400, 4950]], "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": [6105, [2640, 2970, 4400, 4950]], "orient": false}}}
var TR = {"gastos": 2000, "t1": 14852, "max": 7302, "p1": 1.75, "t2": 17673.52, "b2": 2364.34, "p2": 1.14, "lim": 19747.5};
var NMAX = 40;
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function tasa(base, tr) { var t = 0, i; for (i = 0; i < tr.length; i++) if (base > tr[i][0]) t = tr[i][1]; return t; }
// Minimo personal y familiar (art. 56.3): contribuyente + descendientes (el cuarto y siguientes cuentan igual).
function minimo(pers, desc, h) { var m = pers, i; for (i = 0; i < h; i++) m += desc[Math.min(i, 3)]; return m; }
function minimos(cc, h) {
  var c = cc.min;
  return [minimo(P.minE, P.descE, h), c ? minimo(c[0], c[1], h) : minimo(P.minE, P.descE, h)];
}
// Rendimiento del trabajo (art. 17.2.a.3.a: tambien las prestaciones del plan): base = I - gastos 2.000 (art. 19.2.f) - reduccion del art. 20 (RDL 4/2024).
function red20(I) {
  if (I <= TR.t1) return TR.max;
  if (I <= TR.t2) return TR.max - TR.p1 * (I - TR.t1);
  if (I < TR.lim) return TR.b2 - TR.p2 * (I - TR.t2);
  return 0;
}
function baseTrab(I) { return Math.max(0, I - Math.min(TR.gastos, I) - red20(I)); }
// Cuota estatal + autonomica sobre la base general de un rendimiento del trabajo I (art. 63.1: escala menos la escala del minimo).
function cuota(I, cc, h) {
  var b = baseTrab(I);
  var m = minimos(cc, h);
  return escala(b, P.est) - escala(Math.min(b, m[0]), P.est) + escala(b, cc.esc) - escala(Math.min(b, m[1]), cc.esc);
}
function marginal(I, cc, h) { var b = baseTrab(I), m = minimos(cc, h); return (b > m[0] ? tasa(b, P.est) : 0) + (b > m[1] ? tasa(b, cc.esc) : 0); }
// Factor de valor actual de n pagos al inicio de cada ano, descontados a g.
function factor(n, g) { var s = 0, k; for (k = 0; k < n; k++) s += Math.pow(1 + g, -k); return s; }
// Renta de n pagos iguales: {pago, impuesto de cada ano, impuesto en valor de hoy}.
function renta(S, O, n, g, cc, h) {
  var a = factor(n, g), A = S / a, t = cuota(O + A, cc, h) - cuota(O, cc, h);
  return { a: a, pago: A, t: t, van: t * a };
}
function calcular(d) {
  var cc = P.ccaa[d.ccaa], h = Math.round(d.hijos), n = Math.max(Math.round(d.anos), 1), g = d.rentab / 100, S = d.saldo, O = d.otras, x = d.pctCapital / 100;
  var base = cuota(O, cc, h), impCap = cuota(O + S, cc, h) - base;
  var r = renta(S, O, n, g, cc, h);
  var C = S * x, Am = (S - C) / r.a, t0 = cuota(O + C + Am, cc, h) - base, t1 = cuota(O + Am, cc, h) - base;
  var impMix = t0 + (n - 1) * t1, vanMix = t0 + t1 * (r.a - 1);
  var serie = [], k, mn = Infinity, nopt = 1, v;
  for (k = 1; k <= NMAX; k++) { v = renta(S, O, k, g, cc, h).van; serie.push({ n: k, imp: v }); if (v < mn) mn = v; }
  for (k = 1; k <= NMAX; k++) if (serie[k - 1].imp <= mn + 1) { nopt = k; break; }
  var ahorro = impCap - r.van, ahorroOpt = impCap - serie[nopt - 1].imp;
  var pOpt = 0, vOpt = Infinity, p, Cp, Ap, vp;
  for (p = 0; p <= 100; p++) { Cp = S * p / 100; Ap = (S - Cp) / r.a; vp = (cuota(O + Cp + Ap, cc, h) - base) + (cuota(O + Ap, cc, h) - base) * (r.a - 1); if (vp < vOpt - 1e-9) { vOpt = vp; pOpt = p; } }
  return {
    pagoRenta: r.pago, impCapital: impCap, impRenta: n * r.t, impMixto: impMix,
    vanImpCapital: impCap, vanImpRenta: r.van, vanImpMixto: vanMix,
    netoCapital: S - impCap, netoRenta: n * (r.pago - r.t), netoMixto: C + n * Am - impMix,
    vanNetoCapital: S - impCap, vanNetoRenta: S - r.van, vanNetoMixto: S - vanMix,
    ahorroRenta: ahorro, ahorroMixto: impCap - vanMix, costeLiquidez: vanMix - r.van,
    nOptimo: nopt, ahorroOptimo: ahorroOpt, pagoOptimo: renta(S, O, nopt, g, cc, h).pago,
    tipoMedioCapital: S > 0 ? 100 * impCap / S : 0, tipoMedioRenta: r.pago > 0 ? 100 * r.t / r.pago : 0,
    tipoMarginalBase: marginal(O, cc, h), tipoMarginalCapital: marginal(O + S, cc, h), tipoMarginalRenta: marginal(O + r.pago, cc, h),
    serieMin: mn, ganador: ahorro >= 1 ? "renta" : (ahorro <= -1 ? "capital" : "empate"), pctMixtoOpt: pOpt, vanImpMixtoOpt: vOpt, orientativo: cc.orient ? 1 : 0, ccaaNombre: cc.n, capitalMixto: C, serieN: serie
  };
}
function eur(x) { return EM.eur(x); }
function txtAnos(n) { return n + (n === 1 ? " año" : " años"); }
function pct(x, dec) { return EM.num(x, dec === undefined ? 1 : dec) + " %"; }
var IDS = ["saldo", "otras", "hijos", "anos", "rentab", "pctCapital"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.saldo <= 0 || d.otras < 0 || d.hijos < 0 || d.hijos > 6 || d.anos < 1 || d.anos > NMAX || d.rentab < -5 || d.rentab > 15 || d.pctCapital < 0 || d.pctCapital > 100) {
    EM.renderResult({ winner: "revisar", tone: "warn", verdict: "Revisa los datos: el saldo debe ser mayor que 0, los años de cobro de 1 a " + NMAX + ", la rentabilidad entre -5 % y 15 %, el capital entre 0 % y 100 % y los hijos de 0 a 6." });
    return;
  }
  var r = calcular(d), n = Math.round(d.anos), ahorro = r.ahorroRenta, g = r.ganador;
  var mixMejor = n > 1 && r.pctMixtoOpt > 0 && r.pctMixtoOpt < 100 && r.vanImpMixtoOpt < Math.min(r.vanImpRenta, r.vanImpCapital) - 1;
  var verdict;
  if (n === 1) verdict = "Cobrar en 1 año es lo mismo que cobrar de una vez" + (r.ahorroOptimo >= 1 ? ": repartiendo el cobro en " + txtAnos(r.nOptimo) + " pagarías " + EM.eur(r.ahorroOptimo) + " menos de IRPF (en valor de hoy)." : ": con estos datos repartirlo no reduce el IRPF.");
  else {
    if (g === "empate") verdict = "Con estos supuestos, cobrar el plan de una vez o en renta de " + txtAnos(n) + " paga prácticamente el mismo IRPF (menos de 1 € de diferencia).";
    else if (g === "renta") verdict = "Con estos supuestos, cobrar el plan en renta durante " + txtAnos(n) + " paga " + EM.eur(ahorro) + " menos de IRPF (en valor de hoy) que rescatarlo de una vez.";
    else verdict = "Con estos supuestos, rescatar el plan de una vez paga " + EM.eur(-ahorro) + " menos de IRPF (en valor de hoy) que cobrarlo en renta durante " + txtAnos(n) + ": cada pago anual vuelve a perder la reducción por rendimientos del trabajo (art. 20), que el capital pierde una sola vez.";
    if (r.nOptimo === 1) verdict += " Ningún plazo de renta hasta " + NMAX + " años paga menos que el capital.";
    else if (r.nOptimo !== n && r.ahorroOptimo > Math.max(ahorro, 0) + 1) verdict += " El plazo de renta más barato sería de " + txtAnos(r.nOptimo) + ", con " + EM.eur(r.ahorroOptimo) + " menos de IRPF que el capital.";
    if (mixMejor) verdict += r.vanImpMixtoOpt < r.serieMin - 1 ? " Un mixto con el " + r.pctMixtoOpt + " % en capital pagaría aún menos (" + EM.eur(r.vanImpMixtoOpt) + " en valor de hoy)." : " Con tu plazo de " + txtAnos(n) + ", un mixto con el " + r.pctMixtoOpt + " % en capital pagaría " + EM.eur(r.vanImpMixtoOpt) + " (en valor de hoy), menos que la renta y el capital de ese plazo.";
  }
  var note = "";
  if (r.orientativo) note += "<p><strong>Cifras autonómicas orientativas:</strong> para " + r.ccaaNombre + " alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»).</p>";
  note += "<p><strong>Lectura:</strong> el rescate en capital se suma de golpe a tus otras rentas (" + eur(d.otras) + " al año) y paga un tipo medio del " + pct(r.tipoMedioCapital) + " (el tipo de la escala sobre tu último euro pasa del " + pct(r.tipoMarginalBase) + " al " + pct(r.tipoMarginalCapital) + "). ";
  note += "En renta cobras " + eur(r.pagoRenta) + " al año y el tipo medio sobre cada pago es del " + pct(r.tipoMedioRenta) + ". ";
  note += "A cada año se le aplican los gastos de 2.000 € y la reducción por rendimientos del trabajo (arts. 19 y 20): esa reducción se pierde del todo a partir de 19.747,50 € de rendimiento, así que si tus otras rentas más el pago anual quedan entre 14.852 y 19.747,50 € repartir no siempre ahorra (por debajo de 14.852 € la renta gana más). ";
  if (d.pctCapital > 0 && d.pctCapital < 100 && n > 1) note += "Cobrar el " + EM.num(d.pctCapital, 0) + " % de golpe (" + eur(r.capitalMixto) + ") y el resto en renta " + (r.costeLiquidez >= 1 ? "cuesta " + eur(r.costeLiquidez) + " más de IRPF que" : (r.costeLiquidez <= -1 ? "ahorra " + eur(-r.costeLiquidez) + " de IRPF frente a" : "paga lo mismo de IRPF que")) + " la renta pura de " + txtAnos(n) + "; el mixto puede ganar a la renta pura por la reducción del art. 20 o, con aportaciones hasta 2006, cobrando esa parte en capital con el 40 %. ";
  note += "«Valor de hoy» descuenta cada año a la rentabilidad que has indicado, de modo que la renta y el capital valen lo mismo antes de impuestos y la diferencia es solo IRPF.</p>";
  note += "<p><strong>Lo que no entra en el cálculo y puede cambiar la decisión:</strong> si tienes aportaciones hasta 2006, la reducción del 40 % de la disposición transitoria 12.ª solo se aplica al cobro en capital dentro del año de la contingencia o los dos siguientes y se pierde si cobras después o en renta; si estás en plazo, el capital (o un mixto que cobre en capital esa parte) puede salir mejor que lo que muestra esta herramienta. Tampoco se modelan la deducción por rendimientos del trabajo del RDL 5/2026 (que se pierde si lo que cobras del plan más tus otras rentas no laborales supera 6.500 € al año), la liquidez, que el plan siga con comisiones y riesgo mientras cobras la renta, ni los supuestos de liquidez excepcionales (enfermedad grave, desempleo de larga duración).</p>";
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: r.orientativo ? "warn" : (g === "empate" ? "info" : "ok"),
    bigNumber: Math.abs(ahorro), bigLabel: g === "renta" ? "menos de IRPF en renta que en capital (valor de hoy)" : (g === "capital" ? "menos de IRPF en capital que en renta (valor de hoy)" : "de diferencia de IRPF"), format: EM.eur,
    line: { caption: "IRPF total (valor de hoy) según los años en que cobres el plan", xLabel: "Años de cobro", xFormat: function (a) { return a + (a === 1 ? " año" : " años"); }, yFormat: EM.eur,
      series: [{ label: "Renta en N años", color: "a", points: r.serieN.map(function (v) { return [v.n, v.imp]; }) },
               { label: "Capital de una vez", color: "b", points: r.serieN.map(function (v) { return [v.n, r.impCapital]; }) }] },
    barsLabel: "IRPF total en valor de hoy (menos es mejor)",
    bars: [{ label: "Capital de una vez", value: r.vanImpCapital, color: "b" }, { label: "Renta en " + txtAnos(n), value: r.vanImpRenta, color: "a" },
           { label: "Mixto (" + EM.num(d.pctCapital, 0) + " % capital)", value: r.vanImpMixto, color: "c" }],
    cols: ["Capital", "Renta " + txtAnos(n), "Mixto"],
    rows: [
      ["Cobrado el 1.er año", eur(d.saldo), eur(r.pagoRenta), eur(r.capitalMixto + (d.saldo - r.capitalMixto) / factor(n, d.rentab / 100))],
      ["IRPF total (suma de años)", eur(r.impCapital), eur(r.impRenta), eur(r.impMixto)],
      { label: "IRPF en valor de hoy", values: [eur(r.vanImpCapital), eur(r.vanImpRenta), eur(r.vanImpMixto)], strong: true },
      ["Neto cobrado (suma de años)", eur(r.netoCapital), eur(r.netoRenta), eur(r.netoMixto)],
      ["Neto en valor de hoy", eur(r.vanNetoCapital), eur(r.vanNetoRenta), eur(r.vanNetoMixto)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
