// Impresora de tinta (cartuchos), de deposito recargable o laser: coste total y por pagina a N anios.
// Coste = precio de la impresora + paginas totales x coste de consumible por pagina (precio del consumible / paginas que rinde, media de tu mezcla).
// Punto de equilibrio entre dos tipos: paginas al mes con las que cuestan lo mismo en el horizonte. Todo son supuestos del usuario.
function calcular(d) {
  var pag = d.pagMes * 12 * d.anios;
  var tot = [d.pT + pag * d.cT, d.pD + pag * d.cD, d.pL + pag * d.cL];
  var best = 0, i;
  for (i = 1; i < 3; i++) if (tot[i] < tot[best] - 1e-9) best = i;
  function eq(pa, ca, pb, cb) {
    var dp = pa - pb, dc = ca - cb;
    if (dp * dc < 0) return Math.abs(dp) / (12 * d.anios * Math.abs(dc));
    return -1;
  }
  return {
    paginas: pag, totTinta: tot[0], totDeposito: tot[1], totLaser: tot[2],
    pagTinta: pag > 0 ? tot[0] / pag : -1, pagDeposito: pag > 0 ? tot[1] / pag : -1, pagLaser: pag > 0 ? tot[2] / pag : -1,
    eqTintaLaser: eq(d.pT, d.cT, d.pL, d.cL), eqTintaDeposito: eq(d.pT, d.cT, d.pD, d.cD), eqDepositoLaser: eq(d.pD, d.cD, d.pL, d.cL),
    ganador: best
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["pagMes", "anios", "pT", "cT", "pD", "cD", "pL", "cL"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function cp(x) { return EM.eur(x, 3); }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.pagMes <= 0 || d.anios < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe cuántas páginas imprimes al mes (más de 0) y al menos 1 año de horizonte.", tone: "warn", note: "<p>Sin páginas no hay coste por página que comparar.</p>" });
    return;
  }
  if (d.anios > 15 || d.pagMes > 5000 || d.cT > 2 || d.cD > 2 || d.cL > 2) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 15 años, 5.000 páginas al mes y 2 € de consumible por página.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), N = d.anios, anos = EM.num(N, N % 1 ? 1 : 0) + (N === 1 ? " año" : " años");
  var nombres = ["tinta con cartuchos", "tinta de depósito recargable", "láser"], tots = [r.totTinta, r.totDeposito, r.totLaser];
  var g = r.ganador, w = ["tinta", "deposito", "laser"][g], otros = [], i, ahorro;
  for (i = 0; i < 3; i++) if (i !== g) otros.push(tots[i]);
  ahorro = Math.min(otros[0], otros[1]) - tots[g];
  var verdict;
  if (ahorro <= 1) {
    w = "empate";
    verdict = "Con estos datos hay empate: al menos dos tipos de impresora cuestan lo mismo en " + anos + " (unos " + eur(Math.min.apply(null, tots)) + ").";
  } else {
    verdict = "Con estos datos compensa la " + nombres[g] + ": " + eur(tots[g]) + " en " + anos + " (" + cp([r.pagTinta, r.pagDeposito, r.pagLaser][g]) + " por página), " + eur(ahorro) + " menos que la siguiente opción, con " + EM.num(d.pagMes, 0) + " páginas al mes.";
  }
  var note = "<p><strong>Lectura:</strong> ";
  note += r.eqTintaLaser > 0 ? "la tinta con cartuchos y el láser cuestan lo mismo con unas " + EM.num(r.eqTintaLaser, 0) + " páginas al mes (el que cuesta más de equipo pero menos por página gana por encima de esa cifra). " : "no hay un número de páginas al mes que iguale tinta con cartuchos y láser: uno es más barato a la vez en equipo y en consumible. ";
  note += r.eqTintaDeposito > 0 ? "Tinta con cartuchos y depósito se igualan con unas " + EM.num(r.eqTintaDeposito, 0) + " páginas al mes. " : "No hay punto de equilibrio entre cartuchos y depósito con tus datos. ";
  note += r.eqDepositoLaser > 0 ? "Depósito y láser se igualan con unas " + EM.num(r.eqDepositoLaser, 0) + " páginas al mes." : "No hay punto de equilibrio entre depósito y láser con tus datos.";
  note += "</p><p>Es una estimación con supuestos tuyos: el coste de consumible por página es la media de tu mezcla de blanco y negro y color (precio del consumible dividido entre las páginas que rinde). No incluye papel, electricidad, tinta que se seca por no usarla, averías, cabezales ni el valor de reventa, y supone un uso constante.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: w === "empate" ? "warn" : "ok",
    bigNumber: tots[g], bigLabel: "€ en " + anos + " con la opción más barata", format: function (x) { return EM.eur(x); },
    barsLabel: "Coste total en " + anos,
    bars: [{ label: "Tinta con cartuchos" + (w === "tinta" ? " (gana)" : ""), value: r.totTinta, color: "a" }, { label: "Tinta de depósito" + (w === "deposito" ? " (gana)" : ""), value: r.totDeposito, color: "b" }, { label: "Láser" + (w === "laser" ? " (gana)" : ""), value: r.totLaser, color: "c" }],
    cols: ["Cartuchos", "Depósito", "Láser"],
    rows: [
      ["Coste total en " + anos, eur(r.totTinta), eur(r.totDeposito), eur(r.totLaser)],
      ["Coste por página (todo incluido)", cp(r.pagTinta), cp(r.pagDeposito), cp(r.pagLaser)],
      ["Páginas en " + anos, EM.num(r.paginas, 0), EM.num(r.paginas, 0), EM.num(r.paginas, 0)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
