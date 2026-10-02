// Comprar o alquilar un trastero (o guardamuebles): coste a N años, año de equilibrio y valor residual.
// Compra = precio x (1 + gastos de compra %) + costes anuales (comunidad, IBI, seguro) - valor residual al final (precio x (1 + revalorizacion)^N).
// Alquiler = 12 x cuota mensual, con subida anual. Flujos anuales a final de año; con coste de oportunidad > 0 se descuentan (euros de hoy).
// Todo son supuestos del usuario: no incluye impuestos de compra (el usuario mete el % total), plusvalia, hipoteca ni gastos de venta.
function calcular(d) {
  var r = d.tasa / 100, v = 1 / (1 + r), g = d.subida / 100, rv = d.reval / 100, N = d.anios, MAXT = 40;
  function pvCompra(T) {
    var A = r === 0 ? T : (1 - Math.pow(v, T)) / r;
    return d.precio * (1 + d.gastosPct / 100) + d.costes * A - d.precio * Math.pow(1 + rv, T) * Math.pow(v, T);
  }
  function factorAlq(T) { var s = 0, t; for (t = 1; t <= T; t++) s += Math.pow(1 + g, t - 1) * Math.pow(v, t); return s; }
  function pvAlq(T) { return 12 * d.alq * factorAlq(T); }
  var pvc = pvCompra(N), pva = pvAlq(N), dif = pva - pvc, eq = -1, T;
  for (T = MAXT; T >= 1; T--) { if (pvAlq(T) - pvCompra(T) < 0) { eq = T < MAXT ? T + 1 : -1; break; } }
  if (T < 1) eq = 1;
  return {
    pvCompra: pvc, pvAlquiler: pva, diferencia: dif, valorResidual: d.precio * Math.pow(1 + rv, N),
    desembolso: d.precio * (1 + d.gastosPct / 100), anioEq: eq, alqEq: pvc / (12 * factorAlq(N)),
    ganador: dif > 1 ? 0 : (dif < -1 ? 1 : 2)
  };
}
function eur(x, n) { return EM.eur(x, n); }
var IDS = ["precio", "gastosPct", "costes", "alq", "subida", "anios", "reval", "tasa"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0 && k !== "reval") return;
  if (d.precio <= 0 || d.anios < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe un precio de compra mayor que 0 y al menos 1 año de horizonte.", tone: "warn", note: "<p>Sin precio de compra o sin años no hay nada que comparar.</p>" });
    return;
  }
  if (d.anios > 40 || d.tasa > 30 || d.subida > 30 || d.gastosPct > 30 || d.reval > 15 || d.reval < -10) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: máximo 40 años, 30 % de gastos, de subida del alquiler y de coste de oportunidad, y una revalorización entre -10 % y 15 % al año.", tone: "warn", note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), N = d.anios, g = r.ganador, abs = Math.abs(r.diferencia);
  var anos = EM.num(N, N % 1 ? 1 : 0) + (N === 1 ? " año" : " años"), w, verdict;
  if (g === 2) {
    w = "empate";
    verdict = "Con estos datos comprar y alquilar el trastero cuestan lo mismo en " + anos + " (unos " + eur(r.pvCompra) + "): estás justo en el punto de equilibrio.";
  } else if (g === 0) {
    w = "comprar";
    verdict = "Con estos datos compensa comprar: te sale " + eur(abs) + " más barato que alquilar en " + anos + (r.anioEq > 0 && r.anioEq <= N ? ", y desde el año " + r.anioEq + " comprar cuesta menos que alquilar" : "") + (r.alqEq <= 0 ? ". Compensa incluso con un alquiler gratis, porque el valor residual supera todos los costes de comprar." : ". Compensa si el alquiler equivalente supera " + eur(r.alqEq) + " al mes y el tuyo es de " + eur(d.alq) + ".");
  } else {
    w = "alquilar";
    verdict = "Con estos datos compensa alquilar: te sale " + eur(abs) + " más barato que comprar en " + anos + ". Comprar compensaría si el alquiler equivalente superara " + eur(Math.max(r.alqEq, 0)) + " al mes y el tuyo es de " + eur(d.alq) + (r.anioEq > N ? ", o si lo mantienes al menos " + r.anioEq + " años" : "") + ".";
  }
  var note = "<p><strong>Lectura:</strong> ";
  if (d.alq > 0) {
    if (r.anioEq > 0) note += "con tus datos, comprar empieza a costar menos que alquilar a partir del año " + r.anioEq + " (y se mantiene así hasta los 40 años del modelo). ";
    else note += "con tus datos, comprar no llega a costar menos que alquilar en 40 años. ";
    note += "El alquiler mensual que iguala ambas opciones a " + anos + " es " + eur(Math.max(r.alqEq, 0)) + ". ";
  }
  note += "Al comprar desembolsas " + eur(r.desembolso) + " el primer día (precio más gastos) y esperas un valor residual de " + eur(r.valorResidual) + " a " + anos + " con una revalorización del " + EM.num(d.reval, 1) + " % anual";
  note += d.tasa > 0 ? "; con un coste de oportunidad del " + EM.num(d.tasa, 1) + " % los importes se expresan en euros de hoy.</p>" : ".</p>";
  note += "<p>Es una estimación con supuestos tuyos: el porcentaje de gastos de compra lo pones tú con el total de tu comunidad (consulta los gastos de tu comunidad). No incluye impuestos de compra por separado, plusvalía ni gastos de venta, hipoteca, disponibilidad de oferta de trasteros ni cambios de tamaño o de necesidad; supone costes anuales constantes y que el alquiler sube cada año lo que indiques.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: g === 2 ? "warn" : "ok",
    bigNumber: Math.max(r.alqEq, 0), bigLabel: "€ al mes de alquiler con los que comprar y alquilar cuestan lo mismo", format: function (x) { return EM.eur(x); },
    barsLabel: "Coste total en " + anos + (d.tasa > 0 ? " (euros de hoy)" : ""),
    bars: [{ label: "Comprar" + (w === "comprar" ? " (gana)" : ""), value: Math.max(r.pvCompra, 0), color: "a" }, { label: "Alquilar" + (w === "alquilar" ? " (gana)" : ""), value: Math.max(r.pvAlquiler, 0), color: "b" }],
    cols: ["Comprar", "Alquilar"],
    rows: [
      ["Coste total en " + anos, eur(r.pvCompra), eur(r.pvAlquiler)],
      ["Desembolso el primer día", eur(r.desembolso), "—"],
      ["Valor residual al final", eur(r.valorResidual), "—"],
      ["Alquiler mensual de equilibrio", eur(Math.max(r.alqEq, 0)), eur(d.alq)],
      { label: "Año desde el que comprar cuesta menos", values: [r.anioEq > 0 ? EM.num(r.anioEq, 0) : "no llega", ""], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
