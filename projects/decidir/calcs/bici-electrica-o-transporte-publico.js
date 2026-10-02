// Bici electrica, transporte publico o coche: coste anual de cada modo, ahorro, amortizacion de la bici y umbrales.
// Coche = km/anio x coste por km (combustible + desgaste; sin costes fijos). Abono = cuota mensual x 12 (el usuario la pone; 0 = no usa transporte publico).
// Bici = precio / vida util + seguro y robo + km/anio x (mantenimiento + carga). Reventa 0 (el usuario la resta del precio). Empate: coche, abono, bici.
function calcular(d) {
  var km = d.kmdia * d.dias, coche = km * d.kmcoche, abono = d.abono * 12, fijo = d.bici / d.vida + d.seguro;
  var corriente = km * d.mant + d.seguro, bici = fijo + km * d.mant, sc = coche - corriente, sa = abono - corriente, den = d.kmcoche - d.mant;
  var costes = [coche, abono, bici], b = 0, k;
  for (k = 1; k < 3; k++) if ((k !== 1 || d.abono > 0) && costes[k] < costes[b]) b = k;
  return {
    km: km, cocheAnual: coche, abonoAnual: abono, biciAnual: bici, ahorroVsCoche: coche - bici, ahorroVsAbono: d.abono > 0 ? abono - bici : 0,
    paybackCoche: sc > 0 ? d.bici / sc : -1, paybackAbono: (d.abono > 0 && sa > 0) ? d.bici / sa : -1,
    kmMinCoche: den > 0 ? fijo / den : -1, abonoMinMes: bici / 12, barato: b
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["kmdia", "dias", "abono", "kmcoche", "bici", "vida", "mant", "seguro"];
function leer() { var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; }); return d; }
function aviso(v, n) { EM.renderResult({ winner: "invalido", verdict: v, tone: "warn", note: "<p>" + n + "</p>" }); }
function anos(x) { return (Math.round(x * 10) / 10).toLocaleString("es-ES") + " años"; }
function pintar() {
  var d = leer(), r, b, nombres = ["el coche", "el abono de transporte público", "la bici eléctrica"], v, note, cs, hay = d.abono > 0, pc, pa, vu;
  if (d.kmdia < 0 || d.dias < 0 || d.abono < 0 || d.kmcoche < 0 || d.bici < 0 || d.vida < 0 || d.mant < 0 || d.seguro < 0) return;
  if (d.vida < 1) { aviso("La vida útil de la bici debe ser de al menos 1 año.", "Sin vida útil no se puede repartir el precio de la bici por años."); return; }
  if (d.kmdia > 60 || d.dias > 366) { aviso("Revisa el trayecto: hasta 60 km al día en bici (ida y vuelta) y 366 días al año.", "Por encima de eso la comparación deja de ser un desplazamiento diario realista en bici eléctrica."); return; }
  r = calcular(d); b = r.barato; cs = [r.cocheAnual, r.abonoAnual, r.biciAnual]; pc = r.paybackCoche; pa = r.paybackAbono; vu = d.vida + (d.vida === 1 ? " año" : " años");
  if (r.km === 0) v = "Con 0 km al año no hay desplazamiento que comparar: la bici solo suma su coste fijo de " + EM.eur(r.biciAnual) + " al año.";
  else v = "Con estos datos, lo más barato al año es " + nombres[b] + " (" + EM.eur(cs[b]) + " al año)" + (b === 2 ? ": " + (hay ? "ahorras " + EM.eur(r.ahorroVsAbono) + " frente al abono y " : "ahorras ") + EM.eur(r.ahorroVsCoche) + " frente al coche." : ".");
  note = "<p><strong>Lectura:</strong> ";
  note += pc >= 0 ? "la bici se amortiza frente al coche en <strong>" + anos(pc) + "</strong>" + (pc <= d.vida ? ", dentro de su vida útil de " + vu : ", más que su vida útil de " + vu + " (no compensa)") : "con estos datos la bici no llega a amortizarse frente al coche (sus costes corrientes superan lo que te ahorra)";
  if (hay) note += "; frente al abono, " + (pa >= 0 ? "en <strong>" + anos(pa) + "</strong>" + (pa <= d.vida ? "" : " (más que su vida útil)") : "no se amortiza");
  note += ". ";
  note += r.kmMinCoche >= 0 ? "Frente al coche, el coste anual de la bici queda por debajo a partir de unos <strong>" + Math.round(r.kmMinCoche).toLocaleString("es-ES") + " km al año</strong> (tú haces " + Math.round(r.km).toLocaleString("es-ES") + "). " : "Con ese coste por km del coche, igual o menor que el de mantenimiento de la bici, la bici no gana al coche por coste a ningún kilometraje. ";
  if (hay) note += "Frente al transporte público, la bici sale más barata si tu abono cuesta más de <strong>" + EM.eur(r.abonoMinMes, 2) + " al mes</strong> (pagas " + EM.eur(d.abono, 2) + "). ";
  note += "</p><p><strong>No incluido:</strong> el tiempo, la comodidad, el clima, el aparcamiento ni los costes fijos del coche (seguro, impuesto, ITV: si dejarías de tener coche, el ahorro sería mayor). Supone que la bici sustituye todos esos desplazamientos y que cancelas el abono. Las ayudas a la compra de bicis eléctricas y los abonos dependen de tu municipio: consulta tu ayuntamiento. Reventa de la bici: 0 €; si la revenderás, réstalo del precio. Mira también <a href=\"/decidir/tren-avion-o-coche/\">tren, avión o coche</a>.</p>";
  EM.renderResult({
    winner: ["coche", "abono", "bici"][b], verdict: v, tone: r.km === 0 ? "warn" : "ok",
    bigNumber: cs[b], bigLabel: "al año con " + nombres[b], format: EM.eur,
    barsLabel: "Coste anual de cada modo",
    bars: [{ label: "Coche" + (b === 0 ? " (más barato)" : ""), value: r.cocheAnual, color: "a" }].concat(hay ? [{ label: "Abono" + (b === 1 ? " (más barato)" : ""), value: r.abonoAnual, color: "b" }] : [], [{ label: "Bici eléctrica" + (b === 2 ? " (más barato)" : ""), value: r.biciAnual, color: "a" }]),
    cols: ["Coche", "Abono", "Bici eléctrica"],
    rows: [
      { label: "Coste al año", values: [EM.eur(r.cocheAnual), hay ? EM.eur(r.abonoAnual) : "—", EM.eur(r.biciAnual)], strong: true },
      ["Coste al mes", EM.eur(r.cocheAnual / 12), hay ? EM.eur(r.abonoAnual / 12) : "—", EM.eur(r.biciAnual / 12)],
      ["Ahorro anual de la bici frente a cada modo", EM.eur(r.ahorroVsCoche), hay ? EM.eur(r.ahorroVsAbono) : "—", "—"],
      ["Años para amortizar la bici", pc >= 0 ? anos(pc) : "no se amortiza", pa >= 0 ? anos(pa) : "no se amortiza", "—"]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
