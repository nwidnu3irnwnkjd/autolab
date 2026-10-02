// Placas solares (autoconsumo): amortizacion. Parametros fijos de data/params.json -> placas_2026 (fuentes y fechas alli).
// Euros constantes (sin subida de precio en el caso base), degradacion compuesta, vida util de N anos.
// IEE e IVA: (a) tope de la compensacion (energia de la factura sin impuestos = precio con impuestos / ((1+iee)(1+iva)));
// (b) la compensacion se descuenta antes de impuestos (RD 244/2019 art. 14.6.ii-iv) y la energia compensada esta exenta del IEE (Ley 38/1992 art. 94.9): cada euro compensado ahorra tambien IEE e IVA.
var S = { N: 25, deg: 0.005, g0: 0, gSens: 0.03, dto: 0.03, autoSens: 10, iee: 0.0511269632, iva: 0.21 };
// Flujos anuales (ahorro por autoconsumo + compensacion de excedentes con su tope), ano 1..N.
function flujos(d, g, pct) {
  var out = [], t, p, a, e, compra, pr, comp;
  for (t = 1; t <= S.N; t++) {
    p = d.potencia * d.prod * Math.pow(1 - S.deg, t - 1);
    a = Math.min(pct / 100 * p, d.consumo); e = p - a; compra = d.consumo - a;
    pr = d.precio * Math.pow(1 + g, t - 1);
    comp = Math.min(e * d.comp, compra * pr / ((1 + S.iee) * (1 + S.iva))) * (1 + S.iee) * (1 + S.iva);
    out.push({ auto: a, exc: e, ahorro: a * pr, comp: comp, compSinTope: e * d.comp * (1 + S.iee) * (1 + S.iva), flujo: a * pr + comp });
  }
  return out;
}
// Ano (interpolado) en que el acumulado iguala el coste neto; -1 si no llega en N anos.
function amort(net, fl) {
  if (net <= 0) return 0;
  var acc = 0, i;
  for (i = 0; i < fl.length; i++) {
    if (fl[i] > 0 && acc + fl[i] >= net) return i + (net - acc) / fl[i];
    acc += fl[i];
  }
  return -1;
}
function van(r, net, fl) { var s = -net, i; for (i = 0; i < fl.length; i++) s += fl[i] / Math.pow(1 + r, i + 1); return s; }
// TIR (%) por biseccion; null si no existe (coste neto 0 o flujos sin valor).
function tirPct(net, fl) {
  var tot = 0, i; for (i = 0; i < fl.length; i++) tot += fl[i];
  if (net <= 0 || tot <= 0) return null;
  var lo = -0.99, hi = 20, m, j;
  if (van(lo, net, fl) < 0 || van(hi, net, fl) > 0) return null;
  for (j = 0; j < 200; j++) { m = (lo + hi) / 2; if (van(m, net, fl) > 0) lo = m; else hi = m; }
  return (lo + hi) / 2 * 100;
}
function suma(a, n) { var s = 0, i; for (i = 0; i < n && i < a.length; i++) s += a[i]; return s; }
function calcular(d) {
  var net = Math.max(d.coste - d.subv, 0), F = flujos(d, S.g0, d.pctAuto), fl = F.map(function (x) { return x.flujo; });
  var fd = fl.map(function (x, i) { return x / Math.pow(1 + S.dto, i + 1); });
  var tot = suma(fl, S.N), t = tirPct(net, fl), acc = -net;
  var serie = [{ anio: 0, saldo: -net }];
  fl.forEach(function (x, i) { acc += x; serie.push({ anio: i + 1, saldo: acc }); });
  return {
    neto: net, ahorro1: fl[0], ahorroAuto1: F[0].ahorro, comp1: F[0].comp, compSinTope1: F[0].compSinTope, autoKwh1: F[0].auto, excKwh1: F[0].exc,
    topeAplicado: F[0].compSinTope > F[0].comp + 1e-9 ? 1 : 0, anosAmort: amort(net, fl), anosAmortDto: amort(net, fd),
    ahorroNeto: tot - net, tir: t === null ? -999 : t, hayTir: t === null ? 0 : 1,
    anosSubida: amort(net, flujos(d, S.gSens, d.pctAuto).map(function (x) { return x.flujo; })),
    anosAutoMenos: amort(net, flujos(d, S.g0, Math.max(d.pctAuto - S.autoSens, 0)).map(function (x) { return x.flujo; })),
    costeMaxVida: tot + d.subv, costeMax10: suma(fl, 10) + d.subv, costeKwp: d.potencia > 0 ? d.coste / d.potencia : -1, serie: serie
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["potencia", "coste", "subv", "consumo", "pctAuto", "prod", "precio", "comp"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function anos(x) { return EM.num(x, 1) + " años"; }
function pintar() {
  var d = leer();
  if (d.potencia <= 0 || d.coste < 0 || d.subv < 0 || d.consumo < 0 || d.pctAuto < 0 || d.prod < 0 || d.precio < 0 || d.comp < 0) return;
  if (d.pctAuto > 100) {
    EM.renderResult({ winner: "invalido", verdict: "El autoconsumo directo no puede pasar del 100 % de lo que producen las placas.", tone: "warn",
      note: "<p>Escribe un porcentaje entre 0 y 100. Sin batería suele quedar muy por debajo del 100 %, porque las placas producen de día y en casa se consume más de noche.</p>" });
    return;
  }
  if (d.potencia > 100) {
    EM.renderResult({ winner: "invalido", verdict: "Esta calculadora es para instalaciones de hasta 100 kWp.", tone: "warn",
      note: "<p>La compensación simplificada del RD 244/2019 (art. 4.2) solo existe hasta 100 kW; por encima, los excedentes se venden de otra forma y no se modelan aquí.</p>" });
    return;
  }
  var r = calcular(d), ok = r.anosAmort >= 0, N = S.N, kw = EM.num(d.potencia, 1) + " kWp";
  var verdict;
  if (r.neto <= 0) verdict = "Con estos supuestos la subvención cubre todo el coste: la instalación no te cuesta dinero y ahorra " + EM.eur(r.ahorro1) + " el primer año.";
  else if (r.ahorro1 <= 0) verdict = "Con estos supuestos la instalación no ahorra nada, así que no se amortiza.";
  else if (ok) verdict = "Con estos supuestos, las placas se amortizan en unos " + EM.num(r.anosAmort, 1) + " años y, a " + N + " años, habrás ahorrado " + EM.eur(r.ahorroNeto) + " netos.";
  else verdict = "Con estos supuestos, las placas no llegan a amortizarse en " + N + " años: al final habrías perdido " + EM.eur(-r.ahorroNeto) + ".";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.neto > 0 && r.ahorro1 > 0) {
    note += "la instalación compensa en los " + N + " años si cuesta menos de <strong>" + EM.eur(r.costeMaxVida) + "</strong> (" + EM.eur(r.costeMaxVida / d.potencia) + " por kWp) con tu subvención; para amortizarla en 10 años, menos de <strong>" + EM.eur(r.costeMax10) + "</strong>. La tuya cuesta " + EM.eur(d.coste) + " (" + EM.eur(r.costeKwp) + " por kWp). ";
    note += "Si el precio de la luz subiera un " + EM.num(S.gSens * 100) + " % al año, se amortizaría " + (r.anosSubida >= 0 ? "en unos " + EM.num(r.anosSubida, 1) + " años" : "ni así en " + N + " años") + "; con " + S.autoSens + " puntos menos de autoconsumo, " + (r.anosAutoMenos >= 0 ? "en unos " + EM.num(r.anosAutoMenos, 1) + " años" : "no se amortizaría en " + N + " años") + ".</p>";
  } else note += "revisa los datos de potencia, producción y precio.</p>";
  if (d.subv > d.coste) note += "<p><strong>Ojo:</strong> la subvención que has puesto supera el coste; se toma un coste neto de 0 €.</p>";
  if (r.autoKwh1 < d.pctAuto / 100 * d.potencia * d.prod - 1e-6) note += "<p><strong>Ojo:</strong> con tu consumo no puedes autoconsumir tanto: el autoconsumo directo se limita a tu consumo anual (" + EM.num(d.consumo) + " kWh).</p>";
  if (r.topeAplicado) note += "<p><strong>Tope de la compensación:</strong> los excedentes valdrían " + EM.eur(r.compSinTope1) + " el primer año, pero la compensación no puede superar el valor de la energía que consumes de la red (RD 244/2019, art. 14.3), así que se cuentan " + EM.eur(r.comp1) + ". Aquí se aplica sobre el año completo y con el precio con impuestos de la energía; la norma lo exige hora a hora y por periodo de facturación (máximo un mes) y, con PVPC, valora esa energía solo con su coste (sin peajes ni cargos, art. 14.3.ii.a), así que el tope real puede ser bastante menor (con los datos del ejemplo, alrededor de un tercio menos).</p>";
  note += "<p><strong>Qué incluye:</strong> ahorro por la energía que consumes de tus placas al precio que escribes (con impuestos, porque evitas pagar también el impuesto eléctrico y el IVA) y compensación de excedentes al precio sin impuestos que escribes (se descuenta antes de impuestos, así que ahorras también impuesto eléctrico e IVA sobre ella: ×1,2718). Degradación de " + EM.num(S.deg * 100, 1) + " % al año, vida de " + N + " años y euros constantes (sin subida del precio de la luz en el caso base). <strong>No incluye:</strong> batería ni «batería virtual» (oferta comercial no regulada), autoconsumo colectivo, mantenimiento ni cambio de inversor, el ICIO como coste (hasta el 4 % del presupuesto si no está incluido) ni las bonificaciones municipales de IBI e ICIO, deducción del IRPF salvo que la metas como subvención, cambios regulatorios, sombras ni cambios de potencia contratada. En Canarias, Ceuta y Melilla no hay IVA del 21 % (IGIC/IPSI): escribe tu precio con tus impuestos y ten en cuenta que el ×1,2718 de la compensación es el de península y Baleares. Es una estimación con tus hipótesis, no una previsión.</p>";
  EM.renderResult({
    winner: ok ? "amortiza" : "noamortiza", verdict: verdict, tone: ok && r.ahorroNeto > 0 ? "ok" : "warn",
    bigNumber: ok ? r.anosAmort : Math.abs(r.ahorroNeto), bigLabel: ok ? "años para amortizar la instalación" : "de pérdida neta a " + N + " años", format: ok ? anos : EM.eur,
    line: { caption: "Saldo acumulado año a año (ahorro acumulado menos coste neto)", xLabel: "Años", xFormat: function (a) { return "año " + a; }, yFormat: EM.eur,
      series: [{ label: "Saldo", color: "a", points: r.serie.map(function (v) { return [v.anio, v.saldo]; }) }] },
    barsLabel: "Coste y ahorro acumulado a " + N + " años",
    bars: [{ label: "Coste neto de la instalación", value: r.neto, color: "a", fmt: EM.eur }, { label: "Ahorro acumulado a " + N + " años", value: r.ahorroNeto + r.neto, color: "b", fmt: EM.eur }],
    cols: ["Resultado"],
    rows: [
      ["Coste neto (tras subvención)", EM.eur(r.neto)],
      ["Ahorro el primer año por autoconsumo (" + EM.num(r.autoKwh1) + " kWh)", EM.eur(r.ahorroAuto1)],
      ["Compensación de excedentes el primer año (" + EM.num(r.excKwh1) + " kWh vertidos)", EM.eur(r.comp1)],
      ["Amortización simple", r.anosAmort >= 0 ? anos(r.anosAmort) : "No en " + N + " años"],
      ["Amortización con descuento del " + EM.num(S.dto * 100) + " %", r.anosAmortDto >= 0 ? anos(r.anosAmortDto) : "No en " + N + " años"],
      ["TIR (rentabilidad anual de la inversión)", r.hayTir ? EM.num(r.tir, 1) + " %" : "No calculable"],
      { label: "Ahorro neto a " + N + " años (sin descuento)", values: [EM.eur(r.ahorroNeto)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
