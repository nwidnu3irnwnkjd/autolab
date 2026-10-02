// Traspasar un fondo (art. 94.1.a LIRPF, sin tributar) o reembolsar hoy (escala del ahorro, arts. 66.1 y 76); ejercicio 2026. Parametros: data/params.json -> traspasar_fondo_2026 e irpf_2026.escala_ahorro_mitad.
// Escala de UNA mitad (estatal art. 66.1; la autonomica del art. 76 es igual): [desde, cuota integra acumulada, tipo %]; el total es el doble.
var P = { tab: [[0, 0, 9.5], [6000, 570, 10.5], [50000, 5190, 11.5], [200000, 22440, 13.5], [300000, 35940, 15]], limite: 0.25, maxAnios: 40 };
function escala(x) {
  if (x <= 0) return 0;
  for (var i = P.tab.length - 1; i >= 0; i--) if (x > P.tab[i][0]) return 2 * (P.tab[i][1] + (x - P.tab[i][0]) * P.tab[i][2] / 100);
  return 0;
}
// Impuesto de una ganancia g (negativo = ahorro si es perdida) sobre otras rentas del ahorro o >= 0; la perdida solo compensa el 25 % de o (art. 49.1).
function impuesto(g, o) {
  if (g >= 0) return escala(o + g) - escala(o);
  var comp = Math.min(-g, P.limite * o);
  return -(escala(o) - escala(o - comp));
}
// Resultado a n anos: reembolsar hoy y reinvertir frente a traspasar y reembolsar al final.
function escenario(v, c, r, n, cT, cR, o) {
  var g = v - cR - c, t0 = impuesto(g, o), reinv = v - cR - t0, fR = reinv * Math.pow(1 + r, n), tR = impuesto(fR - reinv, o);
  var fT = (v - cT) * Math.pow(1 + r, n), tT = impuesto(fT - c, o);
  return { g: g, t0: t0, reinv: reinv, fR: fR, tR: tR, nR: fR - tR, fT: fT, tT: tT, nT: fT - tT };
}
function calcular(d) {
  var cero = { invalido: 1, traspasable: 0, ganancia: 0, impuestoHoy: 0, reinvertido: 0, valorReem: 0, impuestoFinalReem: 0, netoReem: 0, valorTras: 0, impuestoFinalTras: 0, netoTras: 0, ventaja: 0, nEq: 0 };
  var n = Math.round(d.anios), r = d.rent / 100;
  if (!(d.valor > 0) || d.coste < 0 || d.otras < 0 || d.comT < 0 || d.comR < 0 || d.comT >= d.valor || d.comR >= d.valor || r <= -1 || n < 1) return cero;
  var e = escenario(d.valor, d.coste, r, n, d.comT, d.comR, d.otras), ok = d.vehiculo === "fondo" || d.vehiculo === "sicav", nEq = 0;
  if (ok) for (var k = 1; k <= P.maxAnios; k++) { var f = escenario(d.valor, d.coste, r, k, d.comT, d.comR, d.otras); if (f.nT - f.nR >= 0) { nEq = k; break; } }
  return { invalido: 0, traspasable: ok ? 1 : 0, ganancia: e.g, impuestoHoy: e.t0, reinvertido: e.reinv, valorReem: e.fR, impuestoFinalReem: e.tR, netoReem: e.nR,
    valorTras: ok ? e.fT : 0, impuestoFinalTras: ok ? e.tT : 0, netoTras: ok ? e.nT : 0, ventaja: ok ? e.nT - e.nR : 0, nEq: nEq };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["valor", "coste", "rent", "anios", "otras", "comT", "comR"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.vehiculo = document.getElementById("vehiculo").value; return d;
}
function pintar() {
  var d = leer(), r = calcular(d);
  if (r.invalido) {
    EM.renderResult({ winner: "inv", tone: "warn", verdict: "Estos datos no encajan: el valor debe ser mayor que 0, el coste, las otras rentas y las comisiones no pueden ser negativos, las comisiones deben ser menores que el valor y los años, al menos 1.",
      note: "<p><strong>Qué hacer:</strong> corrige la casilla que no cuadre; la rentabilidad puede ser negativa, pero no del -100 % o peor.</p>" });
    return;
  }
  var n = Math.round(d.anios), anos = n + (n === 1 ? " año" : " años"), perdida = r.ganancia < -0.5, sinGan = Math.abs(r.ganancia) <= 0.5, ahorroPerdida = -r.impuestoHoy;
  var winner, tone = "ok", verdict, mejor = Math.max(r.netoTras, r.netoReem), adv = r.ventaja, bigNumber, bigLabel;
  if (!r.traspasable) {
    winner = "no_existe"; tone = "warn"; bigNumber = Math.max(r.impuestoHoy, 0); bigLabel = "de IRPF si reembolsas o vendes hoy";
    verdict = "Con tus datos, traspasar no es una opción: " + (d.vehiculo === "etf" ? "un ETF (fondo cotizado) o una acción no se puede traspasar sin tributar (salvo ETF extranjeros comprados antes de 2022 y no cotizados en bolsa española, DT 36.ª, que no se modela)" : "una SICAV solo se traspasa sin tributar si tiene más de 500 socios y no has superado el 5 % de su capital en ningún momento de los 12 meses anteriores") + ", así que vender tributa. " +
      (perdida ? "Venderlo hoy computaría una pérdida de " + eur(-r.ganancia) + " y te ahorraría " + eur(ahorroPerdida) + " de IRPF." : sinGan ? "Hoy no tienes ganancia, así que venderlo no costaría IRPF." : "Venderlo hoy tendría una ganancia de " + eur(r.ganancia) + " y costaría " + eur(r.impuestoHoy) + " de IRPF.") +
      " Vendiendo hoy y reinvirtiendo, tendrías " + eur(r.netoReem) + " netos a " + anos + " (al " + EM.num(d.rent, 1) + " % anual).";
  } else {
    var rel = mejor > 0 ? Math.abs(adv) / mejor : 0;
    if (rel < 0.05) { winner = "empate"; tone = "info"; }
    else if (adv > 0) winner = "traspasar"; else { winner = "reembolsar"; tone = "warn"; }
    bigNumber = Math.abs(adv); bigLabel = adv >= 0 ? "de ventaja neta de traspasar a " + anos : "de ventaja neta de reembolsar a " + anos;
    if (sinGan) verdict = "Con tus datos, no hay ganancia latente que diferir (el fondo vale lo que pagaste): reembolsar hoy no cuesta IRPF y la diferencia a " + anos + " es de " + eur(Math.abs(adv)) + ", sin ventaja práctica para traspasar.";
    else if (winner === "empate") verdict = "Con tus datos, es un empate práctico" + (adv > 0 ? ", con ligera ventaja para traspasar" : adv < 0 ? ", con ligera ventaja para reembolsar" : "") + ": traspasar y reembolsar al final deja " + eur(r.netoTras) + " netos a " + anos + " frente a " + eur(r.netoReem) + " si reembolsas hoy y reinviertes (diferencia de " + eur(Math.abs(adv)) + ", " + EM.num(rel * 100, 1) + " % del valor final)." + (perdida ? "" : " Reembolsar hoy te costaría " + eur(r.impuestoHoy) + " de IRPF por una ganancia de " + eur(r.ganancia) + ".");
    else if (winner === "traspasar") verdict = "Con tus datos, gana traspasar por " + eur(adv) + " a " + anos + ": terminas con " + eur(r.netoTras) + " netos frente a " + eur(r.netoReem) + " si reembolsas hoy y reinviertes. Reembolsar hoy te costaría " + eur(r.impuestoHoy) + " de IRPF por una ganancia de " + eur(r.ganancia) + ", que traspasando no tributa hasta el reembolso final.";
    else verdict = "Con tus datos, gana reembolsar hoy por " + eur(-adv) + " a " + anos + ": terminas con " + eur(r.netoReem) + " netos frente a " + eur(r.netoTras) + " si traspasas." + (perdida ? " Tienes una pérdida latente de " + eur(-r.ganancia) + ": reembolsar la computa (te ahorra " + eur(ahorroPerdida) + " de IRPF) y traspasar no." : " Las comisiones del traspaso pesan más que lo que gana diferir el impuesto.");
    if (perdida && winner !== "reembolsar") verdict += " Ojo: tienes una pérdida latente de " + eur(-r.ganancia) + ". Traspasando no se computa, pero se conserva en el coste y reduce la ganancia futura; reembolsar la computa hoy (ahorro de " + eur(ahorroPerdida) + " de IRPF, con tope del 25 % de tus dividendos e intereses) y aquí no se valora lo que se arrastra a los 4 años siguientes.";
  }
  var rows = [], note = "";
  if (r.traspasable) rows.push({ label: "Traspasar y reembolsar al final", values: ["0 €", eur(r.impuestoFinalTras), eur(r.netoTras)], strong: winner === "traspasar" });
  rows.push({ label: "Reembolsar hoy y reinvertir", values: [eur(r.impuestoHoy), eur(r.impuestoFinalReem), eur(r.netoReem)], strong: winner === "reembolsar" || winner === "no_existe" });
  if (r.traspasable) {
    if (r.nEq > 1) note += '<p><strong>Punto de equilibrio:</strong> con tus comisiones, traspasar solo iguala a reembolsar a partir del año ' + r.nEq + '.</p>';
    else if (r.nEq === 0) note += '<p><strong>Punto de equilibrio:</strong> con tus comisiones y tu rentabilidad, traspasar no llega a igualar a reembolsar en 40 años.</p>';
    else note += '<p><strong>Punto de equilibrio:</strong> con tus datos, traspasar iguala o supera a reembolsar desde el primer año.</p>';
    note += '<p><strong>Qué estás difiriendo:</strong> al traspasar no tributas la ganancia de hoy (' + eur(r.ganancia) + '), pero no la perdonas: se paga al reembolsar de verdad, con la ganancia acumulada de ' + anos + ' (' + eur(r.valorTras - d.coste) + ' en total). La ventaja viene de seguir invirtiendo ese impuesto, no de pagar menos por la misma ganancia, y depende de la rentabilidad que supongas.</p>';
  }
  note += '<p><strong>Requisitos del traspaso (art. 94.1.a):</strong> solo fondos de inversión (y SICAV con más de 500 socios y tú con 5 % o menos); el dinero debe ir íntegro a otro fondo o SICAV, sin pasar por tu cuenta, y ni el origen ni el destino pueden ser un ETF (fondo cotizado). Si recibes el dinero en tu cuenta, tributa.</p>';
  note += '<p><strong>Límites:</strong> misma escala del ahorro (19 % a 30 %, estatal más autonómica) en hoy y en el reembolso final, con tus otras rentas del ahorro iguales en ambos años; rentabilidad constante y sin comisiones de gestión (el valor ya es neto); la comisión de traspaso se descuenta del importe invertido y la de reembolso es gasto de la transmisión. No se modelan retenciones (son pago a cuenta), otras ganancias patrimoniales del año (una pérdida las compensa sin límite, art. 49.1.b, y reembolsar con pérdida te ahorraría más), la compensación de pérdidas entre años (solo se aprovecha hasta el 25 % de tus dividendos e intereses; el resto se arrastra 4 años sin valorarlo), el aplazamiento de la pérdida si compras homogéneos en el año anterior o posterior (art. 33.5.g; 2 meses si es un ETF), el reparto FIFO si traspasas solo una parte (art. 94.1.a y 37.2), forales, criptoactivos, planes de pensiones, seguros unit linked, cuentas en el extranjero, derivados ni no residentes. La Cuenta de Ahorro e Inversión Financia Europa (art. 95 ter, RDL 26/2026, en vigor y sin convalidar) no se modela.</p>';
  EM.renderResult({
    winner: winner, verdict: verdict, tone: tone,
    bigNumber: bigNumber, bigLabel: bigLabel, format: EM.eur,
    barsLabel: "Valor neto a " + anos, bars: r.traspasable ? [{ label: "Traspasar", value: r.netoTras, color: "a" }, { label: "Reembolsar hoy", value: r.netoReem, color: "b" }] : [{ label: "Reembolsar hoy y reinvertir", value: r.netoReem, color: "b" }],
    cols: ["Impuesto hoy", "Impuesto al final", "Valor neto a " + anos], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
