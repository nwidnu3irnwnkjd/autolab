// Portatil o movil: contado, financiar o renting. Coste NETO a la vida util (sin valor temporal del dinero: ver contado-o-financiar).
// Contado: precio x (1 - descuento) - reventa. Financiar: se financia el precio de lista (sin entrada): cuotas + comision - reventa.
// Renting: cuota x 12 x anos de uso, sin reventa (se devuelve el equipo). Reparaciones y garantia: fuera del modelo.
// Empates: gana el primero en el orden contado, financiar, renting.
var NOMBRES = ["contado", "financiar", "renting"];
function cuotaFrancesa(P, i, n) { return i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)); }
// Tipo anual efectivo por biseccion: valor actual de las cuotas = importe recibido (neto).
function taeBis(cuota, n, neto) {
  if (neto <= 0 || cuota <= 0) return null;
  var lo = -0.05, hi = 1;
  for (var k = 0; k < 200; k++) {
    var mid = (lo + hi) / 2, pv = 0;
    for (var m = 1; m <= n; m++) pv += cuota / Math.pow(1 + mid, m);
    if (pv > neto) lo = mid; else hi = mid;
  }
  return (Math.pow(1 + (lo + hi) / 2, 12) - 1) * 100;
}
function calcular(d) {
  var H = d.vida, n = Math.max(Math.round(d.meses), 1);
  var pagoContado = d.precio * (1 - d.descuento / 100), reventa = d.precio * d.reventa / 100, com = d.precio * d.comision / 100;
  var cuota = cuotaFrancesa(d.precio, d.tin / 1200, n), pagoFin = cuota * n + com, totRenting = d.renting * 12 * H;
  var costes = [pagoContado - reventa, pagoFin - reventa, totRenting];
  var best = 0, i; for (i = 1; i < 3; i++) if (costes[i] < costes[best]) best = i;
  var minOtro = Math.min(costes[0], costes[1]);
  var segundo = Infinity; for (i = 0; i < 3; i++) if (i !== best && costes[i] < segundo) segundo = costes[i];
  return {
    costeContado: costes[0], costeFinanciar: costes[1], costeRenting: costes[2],
    anoContado: costes[0] / H, anoFinanciar: costes[1] / H, anoRenting: costes[2] / H,
    cuota: cuota, comision: com, sobrecosteFinanciar: pagoFin - pagoContado, interesesYComision: pagoFin - d.precio,
    tae: taeBis(cuota, n, d.precio - com), taeConDescuento: taeBis(cuota, n, pagoContado - com),
    cuotaRentingEquilibrio: minOtro / (12 * H), mejor: best, diferenciaSegundo: segundo - costes[best]
  };
}
function eur(x) { return EM.eur(x); }
function pct(x) { return x === null ? "—" : EM.num(x, 2) + " %"; }
var IDS = ["precio", "descuento", "tin", "comision", "meses", "renting", "reventa", "vida"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer();
  if (d.precio < 0 || d.descuento < 0 || d.tin < 0 || d.comision < 0 || d.renting < 0 || d.reventa < 0) return;
  if (d.precio <= 0 || d.vida < 1 || d.meses < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un precio mayor que 0, al menos 1 año de uso y al menos 1 mes de financiación.", tone: "warn",
      note: "<p>Sin precio, vida útil o plazo no hay compra que comparar.</p>" });
    return;
  }
  if (d.descuento >= 100 || d.reventa > 100) {
    EM.renderResult({ winner: "invalido", verdict: "El descuento debe ser menor que el 100 % y la reventa no puede superar el 100 % del precio.", tone: "warn",
      note: "<p>Revisa esos dos porcentajes: con ellos el equipo saldría gratis o se revendería por más de lo que cuesta.</p>" });
    return;
  }
  if (d.meses > d.vida * 12) {
    EM.renderResult({ winner: "invalido", verdict: "Financiar a " + EM.num(d.meses, 0) + " meses supera los " + EM.num(d.vida * 12, 0) + " meses de uso: seguirías pagando un equipo que ya no usas.", tone: "warn",
      note: "<p>Reduce el plazo de financiación o alarga los años de uso para que la comparación tenga sentido.</p>" });
    return;
  }
  var r = calcular(d), cs = [r.costeContado, r.costeFinanciar, r.costeRenting], b = r.mejor, otras = [0, 1, 2].filter(function (k) { return k !== b; });
  var nom = ["comprar al contado", "financiar", "el renting"], sg = otras[0]; if (cs[otras[1]] < cs[sg]) sg = otras[1];
  var verdict = r.diferenciaSegundo < 1 ? "Con estos datos, " + nom[b] + " y " + nom[sg] + " cuestan lo mismo: " + EM.eur(cs[b]) + " netos en " + EM.num(d.vida, 0) + (d.vida === 1 ? " año" : " años") + " (" + EM.eur(cs[b] / d.vida) + " al año)."
    : "Con estos datos, " + nom[b] + " es lo más barato: " + EM.eur(cs[b]) + " netos en " + EM.num(d.vida, 0) + (d.vida === 1 ? " año" : " años") + " (" + EM.eur(cs[b] / d.vida) + " al año); la siguiente opción, " + nom[sg] + ", cuesta " + EM.eur(r.diferenciaSegundo) + " más.";
  var note = "<p><strong>Lectura:</strong> ";
  if (r.sobrecosteFinanciar < 1) note += "financiar te cuesta lo mismo que pagar al contado, porque no pagas intereses ni comisión y no pierdes ningún descuento: sirve para repartir el pago, no para ahorrar. ";
  else note += "financiar cuesta " + EM.eur(r.sobrecosteFinanciar) + " más que pagar al contado (intereses y comisión " + EM.eur(r.interesesYComision) + (d.descuento > 0 ? ", más el descuento que pierdes" : "") + "), con una cuota de " + EM.eur(r.cuota, 2) + " al mes durante " + EM.num(d.meses, 0) + " meses; la TAE con comisión es del <strong>" + pct(r.tae) + "</strong> y, contando el descuento perdido respecto al precio al contado, el coste efectivo sube al <strong>" + pct(r.taeConDescuento) + "</strong>. ";
  if (d.tin === 0 && d.descuento > 0) note += "Un «0 % de interés» no es gratis aquí: financias el precio sin descuento, y esa diferencia es el coste. Compara siempre con el precio al contado. ";
  note += "Con estos datos el renting compensa solo si su cuota baja de <strong>" + EM.eur(r.cuotaRentingEquilibrio, 2) + " al mes</strong>; la tuya es " + EM.eur(d.renting, 2) + ". ";
  note += "El renting no deja valor de reventa, pero suele incluir servicios que aquí no valoramos; si tu cuota los incluye, compara con ellos en mente.</p>";
  note += "<p><strong>Límites:</strong> los porcentajes y las cuotas son tuyos o ejemplos, no ofertas de ningún comercio. El valor de reventa es una estimación. No se descuenta lo que rendiría tu dinero (para eso, <a href=\"/decidir/contado-o-financiar/\">contado o financiar</a>), ni se incluyen reparaciones, garantía, seguro ni impuestos o deducciones de autónomos.</p>";
  EM.renderResult({
    winner: NOMBRES[b], verdict: verdict, tone: r.diferenciaSegundo < 1 ? "warn" : "ok",
    bigNumber: cs[b] / d.vida, bigLabel: "al año con la opción más barata (" + NOMBRES[b] + ")", format: EM.eur,
    barsLabel: "Coste neto durante la vida útil",
    bars: [{ label: "Contado" + (b === 0 ? " (más barato)" : ""), value: Math.max(cs[0], 0), color: "a" }, { label: "Financiar" + (b === 1 ? " (más barato)" : ""), value: Math.max(cs[1], 0), color: "b" }, { label: "Renting" + (b === 2 ? " (más barato)" : ""), value: Math.max(cs[2], 0), color: "a" }],
    cols: ["Contado", "Financiar", "Renting"],
    rows: [
      ["Coste neto total", EM.eur(cs[0]), EM.eur(cs[1]), EM.eur(cs[2])],
      ["Coste por año de uso", EM.eur(cs[0] / d.vida), EM.eur(cs[1] / d.vida), EM.eur(cs[2] / d.vida)],
      ["Pago al empezar", EM.eur(d.precio * (1 - d.descuento / 100)), EM.eur(0), EM.eur(0)],
      ["Pago mensual", "—", EM.eur(r.cuota, 2), EM.eur(d.renting, 2)],
      ["Valor de reventa que recuperas", EM.eur(d.precio * d.reventa / 100), EM.eur(d.precio * d.reventa / 100), EM.eur(0)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
