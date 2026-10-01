// Coste de una opción de calefacción a N años. energia = demanda útil / rendimiento * precio.
function opcion(demanda, rend, precio, inst, ayuda, mant, fijo, anos) {
  var energia = demanda / rend * precio, anual = energia + mant + fijo;
  return { energia: energia, anual: anual, total: inst - ayuda + anual * anos };
}
function calcular(d) {
  var demanda = d.sup * d.demanda * d.aisl;
  var g = opcion(demanda, d.rendGas, d.pgas, d.instGas, 0, d.mantGas, d.fijoGas, d.anos);
  var a = opcion(demanda, d.scop, d.pelec, d.instAero, d.ayuda, d.mantAero, d.fijoAero, d.anos);
  var e = opcion(demanda, d.rendElec, d.pelec, d.instElec, 0, d.mantElec, d.fijoElec, d.anos);
  var tot = [g.total, a.total, e.total], orden = [0, 1, 2].sort(function (x, y) { return tot[x] - tot[y]; });
  var extra = d.instAero - d.ayuda - d.instGas, ahorro = g.anual - a.anual, amort = -1;
  if (ahorro > 0) amort = extra <= 0 ? 0 : extra / ahorro;
  return {
    demandaKwh: demanda,
    costeGas: g.total, costeAero: a.total, costeElec: e.total,
    anualGas: g.anual, anualAero: a.anual, anualElec: e.anual,
    energiaGas: g.energia, energiaAero: a.energia, energiaElec: e.energia,
    m2Gas: g.anual / d.sup, m2Aero: a.anual / d.sup, m2Elec: e.anual / d.sup,
    ganador: orden[0], segundo: orden[1], orden: orden, diferencia: tot[orden[1]] - tot[orden[0]],
    ahorroAnualAeroVsGas: ahorro, extraInstalacionAero: extra, anosAmortizacionAero: amort
  };
}
function eur(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }); }
function eur2(x) { return x.toLocaleString("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
var IDS = ["sup", "demanda", "aisl", "anos", "instGas", "instAero", "instElec", "pgas", "pelec", "rendGas", "scop", "rendElec",
  "mantGas", "mantAero", "mantElec", "ayuda", "fijoGas", "fijoAero", "fijoElec"];
var NOM = ["Gas", "Aerotermia", "Eléctrica"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  return d;
}
function pintar() {
  var d = leer(); if (d.sup <= 0 || d.anos <= 0 || d.demanda <= 0 || d.aisl <= 0 || d.rendGas <= 0 || d.scop <= 0 || d.rendElec <= 0) return;
  var r = calcular(d), tot = [r.costeGas, r.costeAero, r.costeElec], anual = [r.anualGas, r.anualAero, r.anualElec], m2 = [r.m2Gas, r.m2Aero, r.m2Elec];
  var g = NOM[r.ganador], s = NOM[r.segundo], abs = r.diferencia, ref = Math.max(tot[r.ganador], 1);
  var note = '<p><strong>Lectura:</strong> con tu vivienda necesitas unos ' + EM.num(r.demandaKwh) + ' kWh útiles al año. ';
  if (r.anosAmortizacionAero < 0) note += 'Con estos precios la aerotermia no ahorra frente al gas cada año, así que su sobrecoste de instalación no se recupera. ';
  else if (r.anosAmortizacionAero === 0) note += 'La aerotermia cuesta menos de instalar y menos al año que el gas. ';
  else note += 'La aerotermia cuesta ' + EM.eur(r.extraInstalacionAero) + ' más de instalar que el gas y ahorra ' + EM.eur(r.ahorroAnualAeroVsGas) + ' al año: se amortiza en ' + (Math.round(r.anosAmortizacionAero * 10) / 10).toString().replace(".", ",") + ' años' + (r.anosAmortizacionAero > d.anos ? ', más que tu horizonte de ' + d.anos + ' años' : '') + '. ';
  note += 'Es una estimación con demanda orientativa: depende de tus tarifas reales, del aislamiento y de que la aerotermia alcance el SCOP indicado. Pide presupuestos antes de decidir.</p>';
  var colores = ["a", "b", "c"];
  EM.renderResult({
    winner: abs < 1 ? "empate" : ["gas", "aerotermia", "electrica"][r.ganador],
    verdict: abs < 1 ? 'Con estos números, las opciones cuestan lo mismo en ' + d.anos + ' años.' : 'Con estos números, la opción más barata en ' + d.anos + ' años es ' + g.toLowerCase() + ': ' + EM.eur(abs) + ' menos que ' + s.toLowerCase() + ' (segunda).',
    tone: abs < ref * 0.03 ? "warn" : "ok",
    bigNumber: tot[r.ganador], bigLabel: "de coste total en " + d.anos + " años con la opción " + g.toLowerCase() + " (la más barata)",
    barsLabel: "Coste total en " + d.anos + " años (instalación + energía + mantenimiento)",
    bars: NOM.map(function (n, i) { return { label: n + (i === r.ganador ? " (gana)" : ""), value: tot[i], color: colores[i] }; }),
    cols: ["Coste total", "€/año", "€/m²·año"],
    rows: r.orden.map(function (i, pos) {
      var vals = [EM.eur(tot[i]), EM.eur(anual[i]), EM.eur(m2[i], 2)];
      return pos === 0 ? { label: "1. " + NOM[i], values: vals, strong: true } : [(pos + 1) + ". " + NOM[i]].concat(vals);
    }),
    note: note
  });
}
(function () {
  var z = document.getElementById("zona"), dem = document.getElementById("demanda");
  z.value = "75"; dem.value = "75"; document.getElementById("aisl").value = "1";
  z.addEventListener("change", function () { dem.value = z.value; pintar(); });
})();
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
