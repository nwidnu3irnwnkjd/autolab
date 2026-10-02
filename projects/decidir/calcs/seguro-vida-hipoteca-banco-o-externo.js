// Seguro de vida de la hipoteca: seguro del banco (con bonificacion del tipo) o poliza externa (sin bonificacion).
// Prestamo en amortizacion francesa a n = plazo x 12 cuotas. Banco: tipo = TIN con bonificacion. Externa: TIN + bonificacion.
// Coste a H anos = intereses efectivos (cuotas pagadas + capital pendiente - capital inicial) + primas. La prima del ano y se calcula sobre
// el capital pendiente a principio de ano (evol = 1, capital cubierto decreciente) o es fija (evol = 0). Primas anuales, sin reembolso.
function saldo(P, i, n, m) {
  if (P <= 0) return 0;
  if (i === 0) return P - P / n * m;
  var c = P * i / (1 - Math.pow(1 + i, -n)), g = Math.pow(1 + i, m);
  return P * g - c * (g - 1) / i;
}
function opcion(P, plazo, H, tinPct, prima, evol) {
  var n = plazo * 12, m = H * 12, i = tinPct / 1200, c = P <= 0 ? 0 : (i === 0 ? P / n : P * i / (1 - Math.pow(1 + i, -n)));
  var inter = P <= 0 ? 0 : c * m + saldo(P, i, n, m) - P, primas = 0, y;
  for (y = 0; y < H; y++) primas += prima * (evol === 1 && P > 0 ? saldo(P, i, n, 12 * y) / P : 1);
  return { cuota: c, intereses: inter, primas: primas, coste: inter + primas };
}
function calcular(d) {
  var plazo = Math.max(Math.round(d.plazo), 1), H = Math.min(Math.max(Math.round(d.horizonte), 1), plazo), evol = d.evol === 1 ? 1 : 0;
  var b = opcion(d.capital, plazo, H, d.tin, d.primaBanco, evol), e = opcion(d.capital, plazo, H, d.tin + d.bonif, d.primaExt, evol);
  function f(x) { return opcion(d.capital, plazo, H, d.tin + x, d.primaExt, evol).coste - b.coste; }
  var bm, lo = 0, hi = 10, k;
  if (f(0) >= 0) bm = 0; else if (f(hi) < 0) bm = -1;
  else { for (k = 0; k < 100; k++) { var mid = (lo + hi) / 2; if (f(mid) < 0) lo = mid; else hi = mid; } bm = (lo + hi) / 2; }
  var dif = e.coste - b.coste;
  return {
    H: H, cuotaBanco: b.cuota, cuotaExt: e.cuota, interesesBanco: b.intereses, interesesExt: e.intereses, primasBanco: b.primas, primasExt: e.primas,
    costeBanco: b.coste, costeExt: e.coste, diferencia: dif, extraIntereses: e.intereses - b.intereses, extraPrimas: b.primas - e.primas,
    ahorroCuotaMes: e.cuota - b.cuota, bonifMin: bm, mejor: dif > 1 ? 0 : (dif < -1 ? 1 : 2)
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["capital", "plazo", "tin", "bonif", "primaBanco", "primaExt", "horizonte", "evol"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function pts(x) { return EM.num(x, 2) + " puntos"; }
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.capital <= 0 || d.plazo < 1 || d.horizonte < 1) { aviso("Escribe un capital pendiente mayor que 0, al menos 1 año de plazo restante y 1 de horizonte.", "Sin capital, plazo u horizonte no hay préstamo ni seguro que comparar."); return; }
  if (d.plazo > 40 || d.tin > 15 || d.bonif > 5) { aviso("Revisa los límites: plazo de hasta 40 años, TIN de hasta el 15 % y bonificación de hasta 5 puntos.", "Fuera de esos valores el resultado no sería realista."); return; }
  var r = calcular(d), H = r.H, anos = EM.num(H, 0) + (H === 1 ? " año" : " años"), w, v, bm = r.bonifMin;
  var umbral = bm < 0 ? "más de 10 puntos (ninguna bonificación realista lo cubre)" : (bm === 0 ? "0 puntos (su prima ya no es más cara que la externa)" : pts(bm));
  if (r.mejor === 0) {
    w = "banco";
    v = "Con estos datos, el seguro del banco sale más barato: " + eur(r.diferencia) + " menos en " + anos + " que la póliza externa, " + (d.bonif > 0 ? "porque la bonificación de " + pts(d.bonif) + " ahorra " + eur(r.extraIntereses) + " de intereses" + (r.extraPrimas > 0 ? " y su prima extra suma " + eur(r.extraPrimas) : " y su prima no es más cara") : "porque su prima es más barata que la externa (sin bonificación que perder)") + ". Compensa a partir de una bonificación de " + umbral + ".";
  } else if (r.mejor === 1) {
    w = "externa";
    v = "Con estos datos, la póliza externa sale más barata: " + eur(-r.diferencia) + " menos en " + anos + (d.bonif > 0 ? ", aunque pierdas la bonificación de " + pts(d.bonif) + " (" + eur(r.extraIntereses) + " más de intereses)" : ", porque su prima es más barata y no hay bonificación que perder") + ". El seguro del banco solo compensaría con una bonificación de " + umbral + ", siempre que la póliza externa tenga coberturas equivalentes.";
  } else {
    w = "empate";
    v = "Con estos datos, las dos opciones cuestan lo mismo en " + anos + " (unos " + eur(r.costeBanco) + "): " + (d.bonif > 0 ? "la bonificación de " + pts(d.bonif) + " compensa justo la diferencia de primas." : "las primas son iguales y no hay bonificación.");
  }
  var note = "<p><strong>Lectura:</strong> pagar el préstamo al tipo bonificado cuesta " + eur(r.cuotaBanco, 2) + " al mes y sin bonificación " + eur(r.cuotaExt, 2) + " (" + eur(r.ahorroCuotaMes, 2) + " de diferencia). ";
  note += "En " + anos + " las primas son " + eur(r.primasBanco) + " con el banco y " + eur(r.primasExt) + " con la póliza externa. ";
  note += "La bonificación mínima que iguala los costes es " + umbral + "; tú tienes " + pts(d.bonif) + ".</p>";
  if (d.horizonte > d.plazo) note += "<p>El horizonte se ha limitado al plazo restante (" + anos + ").</p>";
  note += "<p><strong>Condiciones y límites:</strong> la comparación solo vale si la póliza externa ofrece coberturas y prestaciones equivalentes y si perder la bonificación es lo que ocurre en tu contrato: según el art. 17.3 de la Ley 5/2019, el prestamista que exige un seguro de vida debe aceptar pólizas alternativas equivalentes, no puede cobrar por analizarlas y aceptarlas no puede empeorar las condiciones del préstamo; cómo se aplica a tu bonificación, consulta tu escritura y la FEIN. No incluye exclusiones ni salud o edad (que cambian la prima), la subida de la prima con la edad, el reembolso de la parte no consumida de una prima única al amortizar, comisiones ni el efecto fiscal. Las primas son anuales y el capital pendiente sigue el calendario francés sin amortizaciones anticipadas. Información orientativa, no asesoramiento.</p>";
  EM.renderResult({
    winner: w, verdict: v, tone: r.mejor === 2 ? "warn" : "ok",
    bigNumber: Math.abs(r.diferencia), bigLabel: r.mejor === 0 ? "menos con el seguro del banco en " + anos : (r.mejor === 1 ? "menos con la póliza externa en " + anos : "de diferencia en " + anos), format: EM.eur,
    barsLabel: "Coste total en " + anos + " (intereses + primas)",
    bars: [{ label: "Seguro del banco" + (r.mejor === 0 ? " (más barato)" : ""), value: r.costeBanco, color: "a" }, { label: "Póliza externa" + (r.mejor === 1 ? " (más barata)" : ""), value: r.costeExt, color: "b" }],
    cols: ["Seguro del banco", "Póliza externa"],
    rows: [
      ["Tipo del préstamo", EM.num(d.tin, 2) + " %", EM.num(d.tin + d.bonif, 2) + " %"],
      ["Cuota mensual del préstamo", eur(r.cuotaBanco, 2), eur(r.cuotaExt, 2)],
      ["Intereses en " + anos, eur(r.interesesBanco), eur(r.interesesExt)],
      ["Primas del seguro en " + anos, eur(r.primasBanco), eur(r.primasExt)],
      { label: "Coste total en " + anos, values: [eur(r.costeBanco), eur(r.costeExt)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
