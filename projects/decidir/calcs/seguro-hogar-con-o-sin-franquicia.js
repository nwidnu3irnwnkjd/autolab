// Seguro de hogar con o sin franquicia: prima ahorrada vs coste esperado de siniestros pequenos.
// Modelo: frecuencia f de siniestros pequenos al ano (hipotesis del usuario) con coste medio c. Con franquicia F pagas min(c, F) por siniestro; sin franquicia, 0.
// Ahorro de prima = primaSin - primaCon (constante). El capital asegurado es solo informativo (tasa por mil sobre la prima sin franquicia).
function calcular(d) {
  var H = Math.max(Math.round(d.horizonte), 1);
  var ahorro = d.primaSin - d.primaCon, paga = Math.min(d.coste, d.franq);
  var perdida = d.frec * paga, neto = ahorro - perdida;
  return {
    ahorroAnual: ahorro, ahorroTotal: ahorro * H, pagaSiniestro: paga,
    perdidaAnual: perdida, perdidaTotal: perdida * H,
    netoAnual: neto, netoTotal: neto * H,
    frecEquilibrio: paga > 0 ? ahorro / paga : -1,
    aniosEntreSiniestros: paga > 0 && ahorro > 0 ? paga / ahorro : -1,
    siniestrosEquilibrio: paga > 0 ? ahorro * H / paga : -1,
    peorAno1: d.franq - ahorro,
    fondoCubre: d.fondo >= d.franq ? 1 : 0,
    tasaSin: d.capital > 0 ? d.primaSin / d.capital * 1000 : -1,
    mejor: neto > 1 ? 0 : (neto < -1 ? 1 : 2)
  };
}
function eur(x) { return EM.eur(x); }
var IDS = ["primaSin", "primaCon", "franq", "frec", "coste", "capital", "horizonte", "fondo"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  return d;
}
function pintar() {
  var d = leer(), k;
  for (k in d) if (d[k] < 0) return;
  if (d.primaSin <= 0 || d.primaCon <= 0 || d.horizonte < 1) {
    EM.renderResult({ winner: "invalido", verdict: "Escribe las dos primas anuales (mayores que 0) y al menos 1 año de horizonte.", tone: "warn",
      note: "<p>Sin las dos primas no hay nada que comparar.</p>" });
    return;
  }
  if (d.frec > 10 || d.horizonte > 30) {
    EM.renderResult({ winner: "invalido", verdict: "Revisa los límites: hasta 10 siniestros pequeños al año y un horizonte de como máximo 30 años.", tone: "warn",
      note: "<p>Fuera de esos valores el resultado no tendría sentido práctico.</p>" });
    return;
  }
  var r = calcular(d), H = Math.round(d.horizonte), w, verdict;
  var anos = EM.num(H, 0) + (H === 1 ? " año" : " años");
  if (r.ahorroAnual <= 0) {
    w = "sin-franquicia";
    verdict = "Con estos datos la póliza con franquicia no es más barata (" + eur(d.primaCon) + " frente a " + eur(d.primaSin) + " al año): pagarías la franquicia en cada siniestro sin ahorrar prima, así que la póliza sin franquicia sale mejor.";
  } else if (r.mejor === 0) {
    w = "con-franquicia";
    verdict = "Con tus datos compensa la póliza con franquicia: ahorras " + eur(r.ahorroAnual) + " de prima al año y esperas pagar " + eur(r.perdidaAnual) + " en franquicias, " + eur(r.netoAnual) + " a favor al año (" + eur(r.netoTotal) + " en " + anos + ")";
    verdict += r.frecEquilibrio >= 0 ? ", mientras tengas menos de " + EM.num(r.frecEquilibrio, 2) + " siniestros pequeños al año." : ".";
  } else if (r.mejor === 1) {
    w = "sin-franquicia";
    verdict = "Con tus datos compensa la póliza sin franquicia: la franquicia te costaría " + eur(r.perdidaAnual) + " al año esperados frente a " + eur(r.ahorroAnual) + " de prima ahorrada, " + eur(-r.netoAnual) + " más al año (" + eur(-r.netoTotal) + " en " + anos + "); la franquicia solo compensa por debajo de " + EM.num(r.frecEquilibrio, 2) + " siniestros pequeños al año.";
  } else {
    w = "empate";
    verdict = "Con tus datos ambas pólizas cuestan lo mismo de media: la frecuencia de equilibrio es " + EM.num(r.frecEquilibrio, 2) + " siniestros pequeños al año, igual que tu estimación.";
  }
  if (r.fondoCubre === 0) verdict += " Ojo: tu fondo (" + eur(d.fondo) + ") no cubre la franquicia (" + eur(d.franq) + "); en ese caso la póliza sin franquicia reduce el riesgo aunque cueste más de media.";
  var note = "<p><strong>Lectura:</strong> un seguro se paga para reducir la varianza, no para esperar ganar; la frecuencia y el coste de los siniestros son hipótesis tuyas. ";
  note += "Cada siniestro pequeño te cuesta " + eur(r.pagaSiniestro) + " con franquicia (el menor entre el coste medio y la franquicia) y 0 sin ella. ";
  if (r.frecEquilibrio >= 0) note += "La frecuencia de equilibrio es " + EM.num(r.frecEquilibrio, 2) + " siniestros al año" + (r.aniosEntreSiniestros >= 0 ? " (uno cada " + EM.num(r.aniosEntreSiniestros, 1) + " años)" : "") + ": por debajo compensa la franquicia, por encima la póliza sin franquicia. En " + anos + " la prima ahorrada paga " + EM.num(r.siniestrosEquilibrio, 1) + " siniestros pequeños. ";
  else note += "Con un coste medio de 0 o una franquicia de 0 no hay franquicia que pagar. ";
  note += "</p><p><strong>Peor escenario:</strong> en un siniestro grande la franquicia pesa poco frente al coste total y la póliza paga el resto en ambos casos; en el año 1 la diferencia es que con franquicia pagas " + eur(d.franq) + " y has ahorrado " + eur(r.ahorroAnual) + " de prima, es decir " + (r.peorAno1 >= 0 ? eur(r.peorAno1) + " más" : eur(-r.peorAno1) + " menos") + " que sin franquicia. ";
  note += r.fondoCubre === 1 ? "Tu fondo de " + eur(d.fondo) + " cubre la franquicia." : "Tu fondo de " + eur(d.fondo) + " no cubre la franquicia de " + eur(d.franq) + ".";
  if (r.tasaSin >= 0) note += " Como referencia informativa, tu prima sin franquicia equivale a " + EM.num(r.tasaSin, 2) + " por mil de un capital asegurado de " + eur(d.capital) + ".";
  note += "</p><p><strong>Límites:</strong> no incluye coberturas concretas, exclusiones, infraseguro ni regla proporcional (un capital insuficiente reduce lo que paga la póliza), ni la responsabilidad civil. Si tienes hipoteca, el banco puede exigir cobertura y bonificar el tipo si contratas con él: consúltalo antes de cambiar de póliza. Las primas son tuyas o ejemplos, no de aseguradoras concretas; la prima se supone constante.</p>";
  EM.renderResult({
    winner: w, verdict: verdict, tone: r.mejor === 2 || r.fondoCubre === 0 ? "warn" : "ok",
    bigNumber: r.netoTotal, bigLabel: "ventaja de la póliza con franquicia en " + anos + " (negativa: sale mejor la póliza sin franquicia)", format: EM.eur,
    barsLabel: "En " + anos,
    bars: [{ label: "Prima ahorrada con franquicia", value: Math.max(r.ahorroTotal, 0), color: "a" }, { label: "Franquicias esperadas", value: Math.max(r.perdidaTotal, 0), color: "b" }],
    cols: ["Con franquicia", "Sin franquicia"],
    rows: [
      ["Prima al año", eur(d.primaCon), eur(d.primaSin)],
      ["Franquicias esperadas al año", eur(r.perdidaAnual, 2), eur(0)],
      ["Coste esperado al año", eur(d.primaCon + r.perdidaAnual, 2), eur(d.primaSin, 2)],
      ["Coste esperado en " + anos, eur((d.primaCon + r.perdidaAnual) * H), eur(d.primaSin * H)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
