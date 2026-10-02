// Capitalizar el paro o cobrarlo mensualmente (2026). Parametros generados desde data/params.json -> capitalizar_paro_2026 (fuentes y fechas alli).
// tope/minimo: cuantia maxima y minima mensual por hijos a cargo (0, 1, 2 o mas) = IPREM 600 + 1/6, x 175/200/225 % y 80/107 %; int: interes legal del dinero.
var P = {"tope": [1225, 1400, 1575], "minimo": [560, 749, 749], "pctAlto": 70, "pctBajo": 60, "mesesAlto": 6, "int": 3.25, "maxMeses": 24, "minPend": 3, "mesesCompat": 9, "cuotaMin": 205.88};
function calcular(d) {
  var n = Math.round(d.meses), ya = Math.round(d.cobrados), h = Math.min(Math.max(Math.round(d.hijos), 0), 2), M = Math.max(Math.round(d.arranque), 0);
  var br = d.br, inv = Math.max(d.inversion, 0), cuota = Math.max(d.cuota, 0);
  if (d.actividad !== "si") return { bloqueo: 1 };
  if (n < P.minPend) return { bloqueo: 2 };
  if (ya + n > P.maxMeses) return { bloqueo: 3 };
  var c = [], k, T = 0, V = 0, raw, i = P.int / 100;
  for (k = 1; k <= n; k++) {
    raw = br * ((ya + k) <= P.mesesAlto ? P.pctAlto : P.pctBajo) / 100;
    c.push(Math.min(Math.max(raw, P.minimo[h]), P.tope[h]));
    T += c[k - 1];
    V += c[k - 1] * (1 - i * k / 12);
  }
  // Ley 20/2007 art. 34.1 regla 1.a y 2.a + SEPE: lo no capitalizado (R = T - X*T/V, en euros de prestacion) se abona como subvencion de cuota hasta agotarlo mientras sigas de alta.
  var X = Math.min(inv, V), R = T - X * T / V;
  var sm = Math.max(cuota, P.cuotaMin), msub = R / sm, capT = X + R, coste = T - capT;
  // Cobrar mes a mes siendo autonomo: compatibilidad como maximo 270 dias = 9 mensualidades (Ley 20/2007 art. 33).
  var mc = Math.min(n, P.mesesCompat), Tc = 0, kk;
  for (kk = 0; kk < mc; kk++) Tc += c[kk];
  var recCap = X + Math.min(M, msub) * sm, recCob = 0;
  for (k = 0; k < Math.min(M, mc); k++) recCob += c[k];
  var sCap = recCap - inv - M * cuota, sCob = recCob - inv - M * cuota;
  return {
    bloqueo: 0, primera: c[0], total: T, totalCob: Tc, mesesCob: mc, valorActual: V, pagoUnico: X, mesesSub: msub, subMes: sm, subTotal: R,
    capTotal: capT, coste: coste, dif: capT - Tc, propioCap: Math.max(0, inv - X), propioCob: inv,
    saldoCap: sCap, saldoCob: sCob, colchonCap: cuota > 0 ? sCap / cuota : 0, colchonCob: cuota > 0 ? sCob / cuota : 0,
    recCap: recCap, recCob: recCob, reintegro: X, costeTodo: T - V, n: n, tope: P.tope[h], inversion: inv
  };
}
function eur(x) { return EM.eur(x); }
function txtMeses(n) { var r = Math.round(n * 10) / 10; return EM.num(r, Number.isInteger(r) ? 0 : 1) + (r === 1 ? " mes" : " meses"); }
var IDS = ["meses", "br", "hijos", "cobrados", "inversion", "cuota", "arranque"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.actividad = document.getElementById("actividad").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
function pintar() {
  var d = leer();
  if (d.meses < 0 || d.br <= 0 || d.hijos < 0 || d.cobrados < 0 || d.inversion < 0 || d.cuota < 0 || d.arranque < 0 || d.arranque > 60) { aviso("Revisa los datos: la base reguladora debe ser mayor que 0 y ningún importe ni número de meses puede ser negativo (el arranque, hasta 60 meses)."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("Sin una actividad nueva no se puede capitalizar: el pago único de la prestación se concede para constituirte como autónomo (o aportar capital a una sociedad que controles, que esta herramienta no calcula). Si no vas a iniciar una actividad, lo que te corresponde es cobrar la prestación mes a mes."); return; }
  if (r.bloqueo === 2) { aviso("Con " + txtMeses(Math.round(d.meses)) + " pendientes no puedes capitalizar: el Real Decreto 1044/1985 (art. 2) exige tener al menos 3 mensualidades por cobrar. Lo que queda se cobra mes a mes."); return; }
  if (r.bloqueo === 3) { aviso("La suma de meses cobrados y pendientes supera los 24 meses (720 días) que es la duración máxima de la prestación contributiva (art. 269.1 de la LGSS). Revisa los datos."); return; }
  var n = r.n, verdict, dif = r.dif, ad = Math.abs(dif), sub = r.subTotal >= 1;
  var comp = "Capitalizar " + (r.pagoUnico >= 1 ? "te da " + eur(r.pagoUnico) + " de golpe" : "no te da pago único") + (sub ? (r.pagoUnico >= 1 ? " y otros " : " pero sí ") + eur(r.subTotal) + " como subvención de tu cuota de autónomo, que se cobra mientras sigas de alta durante unos " + txtMeses(r.mesesSub) : "") + ": " + eur(r.capTotal) + " en total. Cobrar la prestación mes a mes siendo autónomo solo es posible " + txtMeses(r.mesesCob) + " (270 días como máximo, art. 33 de la Ley 20/2007)" + (n > r.mesesCob ? ", " + eur(r.totalCob) + " en total" : ": " + eur(r.totalCob)) + ".";
  if (ad < 1) verdict = comp + " Con estos datos recibes prácticamente lo mismo en total, así que decide por la liquidez que necesites al empezar.";
  else if (dif >= 1) verdict = comp + " Capitalizar te da " + eur(dif) + " más en total, porque la compatibilidad con tu actividad cubre menos meses que la prestación pendiente y lo que no capitalizas se sigue cobrando como cuota. Frente a cobrar los " + txtMeses(n) + " enteros sin darte de alta, " + (r.coste >= 1 ? "lo que pierdes es el interés legal descontado (" + eur(r.coste) + ")" : "no pierdes nada con estos datos, porque no hay pago único al que descontar el interés") + "." + (sub ? " La subvención solo la cobras mientras sigas de alta: si cesas antes de agotarla, pierdes lo que quede sin cobrar." : "");
  else verdict = comp + " Cobrar mes a mes te deja " + eur(ad) + " más en total, que es el interés legal que se descuenta al capitalizar" + (sub ? " (la subvención se cobra mientras sigas de alta y, si cesas antes de agotarla, pierdes lo que quede)" : "") + ". Capitalizar compensa si necesitas ese dinero ya para la inversión o si te rinde en el negocio más que esa diferencia.";
  var note = "<p><strong>Lectura:</strong> pendiente de cobrar tienes " + txtMeses(n) + " de prestación, " + eur(r.total) + " en total (" + eur(r.primera) + " el primer mes pendiente" + (d.hijos >= 0 ? ", con tope de " + eur(r.tope) + " al mes según tus hijos a cargo" : "") + "). El valor actual que paga el SEPE al capitalizar, descontando el interés legal del dinero, es de " + eur(r.valorActual) + "; solo se abona hasta el importe de la inversión que justifiques (incluidos tributos de inicio y hasta un 15 % en asesoramiento y formación): " + eur(r.pagoUnico) + ". ";
  if (sub) note += "La parte de prestación que no capitalizas (" + eur(r.subTotal) + ") se abona cada mes como subvención de tu cuota de autónomo, por un importe fijo (" + eur(r.subMes) + " al mes, no menor que la aportación de la base mínima, " + eur(P.cuotaMin) + "), durante unos " + txtMeses(r.mesesSub) + " mientras sigas de alta como autónomo hasta agotarla. ";
  note += "Al arrancar necesitas " + eur(r.propioCap) + " de dinero propio si capitalizas, o " + eur(r.propioCob) + " si cobras mes a mes (la prestación mensual llega después de gastar la inversión).</p>";
  note += "<p><strong>Los " + (d.arranque === 0 ? "0" : EM.num(d.arranque, 0)) + " meses hasta tener ingresos regulares:</strong> recibes " + eur(r.recCap) + " capitalizando o " + eur(r.recCob) + " cobrando mes a mes; tras pagar la inversión y " + eur(d.cuota * d.arranque) + " de cuotas, te quedan " + eur(r.saldoCap) + " capitalizando o " + eur(r.saldoCob) + " cobrando mes a mes (" + EM.num(r.colchonCap, 1) + " y " + EM.num(r.colchonCob, 1) + " meses de cuota; saldo negativo = tendrías que ponerlo tú).</p>";
  note += "<p><strong>Si no sale bien:</strong> el pago único debe destinarse a la actividad para la que se concede, y hay que iniciarla y darse de alta como autónomo en el plazo máximo de un mes desde que lo cobras (RD 1044/1985, arts. 4.1 y 7): si no, es un pago indebido y tendrías que devolver " + eur(r.reintegro) + ". Para la exención del IRPF (art. 7.n de la Ley 35/2006) hay que mantener la actividad durante cinco años. Solicítalo antes de darte de alta, y recuerda que no puedes pedirlo si en los 24 meses anteriores compatibilizaste la prestación con un trabajo por cuenta propia ni si usaste el pago único en los últimos cuatro años.</p>";
  if (n > P.mesesCompat) note += "<p><strong>Cobrar mes a mes siendo autónomo:</strong> compatibilizar la prestación con tu alta por cuenta propia solo es posible hasta 270 días (9 meses) y hay que pedirlo en los 15 días siguientes al inicio (art. 33 de la Ley 20/2007); por eso la columna «Cobrar mes a mes» suma " + txtMeses(r.mesesCob) + " (" + eur(r.totalCob) + "). Las otras " + txtMeses(n - r.mesesCob) + " (" + eur(r.total - r.totalCob) + ") solo se cobrarían si no te das de alta o si cesas la actividad y reanudas la prestación, que no modelamos; según los casos el alta puede suspenderla o extinguirla, así que consúltalo con el SEPE.</p>";
  note += "<p><strong>Supuesto sobre el interés:</strong> el interés legal se descuenta solo del pago único; sobre la parte que se cobra como subvención no lo descontamos, porque la norma no lo fija con claridad y el SEPE indica que «en cualquier caso se descontará el interés legal». Si lo aplicara también ahí, el total capitalizando quedaría entre " + eur(Math.min(r.valorActual, r.capTotal)) + " y " + eur(r.capTotal) + ".</p>";
  note += "<p><strong>No incluye:</strong> el riesgo del negocio y su rentabilidad real, la protección por cese de actividad, trabajar por cuenta ajena a la vez, la reanudación de la prestación, subsidios, comunidades forales, trabajo a tiempo parcial, discapacidad del 33 % o más, bonificaciones por edad o sexo, la tarifa plana (su cuantía de 2026 no está verificada en una fuente oficial), la cotización por desempleo que el SEPE descuenta de la prestación mensual (no sabemos si se aplica al pago único) ni el IRPF: el pago único está exento si se cumplen los requisitos, mientras que la prestación mensual tributa como rendimiento del trabajo y suele tener retención, lo que, si tuvieras otras rentas ese año, favorecería a capitalizar. Las cifras son estimaciones: el SEPE calcula el importe exacto.</p>";
  EM.renderResult({
    winner: ad < 1 ? "empate" : (dif > 0 ? "capitalizar" : "cobrar"), verdict: verdict, tone: "info",
    bigNumber: ad, bigLabel: ad < 1 ? "de diferencia en total entre capitalizar y cobrar mes a mes" : (dif > 0 ? "más en total capitalizando que cobrando mes a mes siendo autónomo" : "menos en total capitalizando que cobrando mes a mes"), format: eur,
    barsLabel: "Dinero total que recibes de la prestación pendiente siendo autónomo",
    bars: [{ label: "Cobrar mes a mes (" + txtMeses(r.mesesCob) + ")", value: r.totalCob, color: "a" }, { label: "Capitalizar", value: r.capTotal, color: "b" }],
    cols: ["Cobrar mes a mes", "Capitalizar"],
    rows: [
      ["Pago único al empezar", eur(0), eur(r.pagoUnico)],
      ["Prestación / subvención de cuotas", eur(r.totalCob), eur(r.subTotal)],
      ["Meses durante los que se cobra", txtMeses(r.mesesCob), sub ? txtMeses(r.mesesSub) : "0 meses"],
      { label: "Total recibido", values: [eur(r.totalCob), eur(r.capTotal)], strong: true },
      ["Dinero propio necesario al empezar", eur(r.propioCob), eur(r.propioCap)],
      ["Recibido en tus " + EM.num(d.arranque, 0) + " meses de arranque", eur(r.recCob), eur(r.recCap)],
      ["Saldo tras inversión y cuotas en el arranque", eur(r.saldoCob), eur(r.saldoCap)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
