// Compensar perdidas y ganancias del ahorro antes del 31-dic (arts. 33.5.f-g, 49 y 66/76 LIRPF; ejercicio 2026). Parametros: data/params.json -> compensar_perdidas_2026 e irpf_2026.escala_ahorro_mitad.
// Escala de UNA mitad (art. 66.1 estatal; la autonomica del art. 76 es igual): [desde, cuota integra acumulada, tipo %]; el total es el doble.
var P = { tab: [[0, 0, 9.5], [6000, 570, 10.5], [50000, 5190, 11.5], [200000, 22440, 13.5], [300000, 35940, 15]], limite: 0.25, ejercicio: 2026, anios: 4 };
function escala(x) {
  if (x <= 0) return 0;
  for (var i = P.tab.length - 1; i >= 0; i--) if (x > P.tab[i][0]) return 2 * (P.tab[i][1] + (x - P.tab[i][0]) * P.tab[i][2] / 100);
  return 0;
}
// Integra y compensa (orden AEAT): fase 1 = ejercicio (a = capital mobiliario, b = ganancias y perdidas, 25 % entre cajones, art. 49.1); fase 2 = saldo negativo de anos anteriores (primero b restante, luego el 25 % restante de a).
function liquidar(gp, perd, rcm, otras, prev, anio, perdida) {
  var a = rcm + otras, b = gp - perd - perdida, ant = (anio >= P.ejercicio - P.anios && anio < P.ejercicio) ? prev : 0, aNeg = 0, nuevo = 0, topeA, topeB, y, z, t, x;
  if (b < 0) { nuevo = -b; b = 0; }
  if (a < 0) { aNeg = -a; a = 0; }
  topeA = P.limite * a; topeB = P.limite * b;
  y = Math.min(nuevo, topeA); nuevo -= y; a -= y; topeA -= y;
  z = Math.min(aNeg, topeB); aNeg -= z; b -= z;
  t = Math.min(ant, b); ant -= t; b -= t;
  x = Math.min(ant, topeA); ant -= x; a -= x;
  var ult = anio === P.ejercicio - P.anios;
  return { base: a + b, arrastre: nuevo + aNeg + (ult ? 0 : ant), caduca: ult ? ant : 0 };
}
function calcular(d) {
  var cero = { invalido: 1, baseSin: 0, baseCon: 0, cuotaSin: 0, cuotaCon: 0, ahorro: 0, ahorroSinRecompra: 0, arrastreSin: 0, arrastreCon: 0, caducaSin: 0, caducaCon: 0, capacidad: 0, aplicada: 0 };
  if (d.gp < 0 || d.perd < 0 || d.prev < 0 || d.perdida < 0) return cero;
  var anio = parseInt(d.anio, 10) || 0, rec = d.recompra === "si", ef = rec ? 0 : d.perdida;
  var s = liquidar(d.gp, d.perd, d.rcm, d.otras, d.prev, anio, 0), c = liquidar(d.gp, d.perd, d.rcm, d.otras, d.prev, anio, ef);
  var x = liquidar(d.gp, d.perd, d.rcm, d.otras, d.prev, anio, d.perdida), inf = liquidar(d.gp, d.perd, d.rcm, d.otras, d.prev, anio, 1e12);
  return { invalido: 0, baseSin: s.base, baseCon: c.base, cuotaSin: escala(s.base), cuotaCon: escala(c.base), ahorro: escala(s.base) - escala(c.base),
    ahorroSinRecompra: escala(s.base) - escala(x.base), arrastreSin: s.arrastre, arrastreCon: c.arrastre, caducaSin: s.caduca, caducaCon: c.caduca, capacidad: s.base - inf.base, aplicada: ef };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["gp", "perd", "rcm", "prev", "perdida", "otras"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.anio = document.getElementById("anio").value; d.recompra = document.getElementById("recompra").value; return d;
}
function pintar() {
  var d = leer(), r = calcular(d);
  if (r.invalido) {
    EM.renderResult({ winner: "inv", tone: "warn", verdict: "Estos datos no encajan: las ganancias, las pérdidas, el saldo pendiente y la pérdida que venderías no pueden ser negativos (el capital mobiliario y las otras rentas del ahorro sí pueden llevar signo menos).",
      note: "<p><strong>Qué hacer:</strong> pon cada importe en positivo en su casilla.</p>" });
    return;
  }
  var winner, tone = "ok", verdict, extra = r.arrastreCon - r.arrastreSin, perdido = r.caducaCon - r.caducaSin;
  if (d.perdida <= 0) {
    winner = "sin_efecto"; tone = "warn"; verdict = "Con tus datos todavía no has indicado ninguna pérdida latente que vender: la base del ahorro de 2026 queda en " + eur(r.baseSin) + " y la cuota estimada en " + eur(r.cuotaSin) + ". Pon el importe de la pérdida para ver cuánto ahorrarías.";
  } else if (d.recompra === "si") {
    winner = "recompra"; tone = "warn"; verdict = "Con tus datos, si recompras los mismos valores (u otros homogéneos) en los 2 meses anteriores o posteriores a la venta (1 año si no cotizan), la pérdida de " + eur(d.perdida) + " no computa en 2026 y el ahorro este año es de 0 €: se integrará cuando transmitas los valores recomprados. Sin esa recompra el ahorro estimado sería de " + eur(r.ahorroSinRecompra) + ".";
  } else if (r.ahorro < 1) {
    winner = "sin_efecto"; tone = "warn"; verdict = "Con tus datos, vender la pérdida de " + eur(d.perdida) + " antes del 31 de diciembre no baja tu IRPF de 2026 (ahorro de 0 €): tus pérdidas y saldos pendientes ya cubren lo que la ley deja compensar este año (las ganancias y hasta el 25 % del capital mobiliario) o no tienes rentas positivas que compensar." + (extra > 0.5 ? " La pérdida se arrastra a 2027-2030 (" + eur(r.arrastreCon) + " pendientes en total)." : "");
  } else if (extra > 0.5) {
    winner = "parcial"; verdict = "Con tus datos, vender la pérdida de " + eur(d.perdida) + " antes del 31 de diciembre reduce tu IRPF de 2026 en " + eur(r.ahorro) + " (de " + eur(r.cuotaSin) + " a " + eur(r.cuotaCon) + "), pero este año solo se aprovechan " + eur(r.capacidad) + " de pérdida; los otros " + eur(extra) + " se arrastran a 2027-2030.";
  } else {
    winner = "total"; verdict = "Con tus datos, vender la pérdida de " + eur(d.perdida) + " antes del 31 de diciembre reduce tu IRPF de 2026 en " + eur(r.ahorro) + " (de " + eur(r.cuotaSin) + " a " + eur(r.cuotaCon) + "): se compensa entera este año.";
  }
  if (perdido > 0.5 && winner !== "recompra") verdict += " Ojo: vender consume antes las rentas del año y " + eur(perdido) + " de tu saldo pendiente de " + d.anio + " caducarían sin usar tras 2026.";
  var rows = [
    { label: "Sin vender la pérdida", values: [eur(r.baseSin), eur(r.cuotaSin), eur(r.arrastreSin)] },
    { label: "Vendiéndola antes del 31/12" + (d.recompra === "si" ? " (con recompra: no computa)" : ""), values: [eur(r.baseCon), eur(r.cuotaCon), eur(r.arrastreCon)], strong: true }
  ];
  var note = '<p><strong>Ojo, es un aplazamiento:</strong> si recompras el mismo valor más barato, tu ganancia futura será mayor en lo mismo que ahorras hoy; el ahorro real es pagar el impuesto más tarde, salvo que esa ganancia caiga en un tramo más bajo o no llegue a producirse.</p>';
  if (d.recompra === "no" && d.perdida > 0) note += '<p><strong>Capacidad este año:</strong> con tus datos solo reduce la base de 2026 una pérdida de hasta ' + eur(r.capacidad) + '; lo que supere esa cifra se arrastra 4 años en vez de ahorrar ya.</p>';
  if (perdido > 0.5) note += '<p><strong>Saldo que caduca:</strong> tu saldo negativo de ' + d.anio + ' vence con este ejercicio y, al vender la pérdida, ' + eur(perdido) + ' de ese saldo se quedan sin usar (se pierden), porque la pérdida nueva consume antes las ganancias del año.</p>';
  if (r.caducaSin > 0.5) note += '<p><strong>Saldo de 2022:</strong> aun sin vender, ' + eur(r.caducaSin) + ' de tu saldo negativo de 2022 caduca tras 2026 por falta de ganancias o dividendos que compensar.</p>';
  note += '<p><strong>Límites:</strong> la cuota usa la escala del ahorro (19 % a 30 %, estatal más autonómica) y supone que tu base general absorbe el mínimo personal y familiar; no incluye retenciones. La compensación entre capital mobiliario y ganancias tiene un límite del 25 % del saldo positivo. No se modelan criptomonedas, derivados, FIFO por lotes (la pérdida que pones se supone ya calculada con el lote más antiguo), forales, pérdidas de no cotizados, saldos antiguos de capital mobiliario ni declaración conjunta. Con recompra, la pérdida no se pierde: se integra cuando vendas lo recomprado.</p>';
  EM.renderResult({
    winner: winner, verdict: verdict, tone: tone,
    bigNumber: r.ahorro, bigLabel: "de IRPF que ahorrarías en 2026", format: EM.eur,
    barsLabel: "Cuota del ahorro 2026", bars: [{ label: "Sin vender la pérdida", value: r.cuotaSin, color: "a" }, { label: "Vendiéndola", value: r.cuotaCon, color: "b" }],
    cols: ["Base del ahorro", "Cuota estimada", "Pendiente para 2027-2030"], rows: rows, note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
