// IRPF 2026: conjunta o individual. Parametros (generados desde data/params.json -> irpf_2026; fuentes y fechas alli).
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "aho": [[0, 9.5], [6000, 10.5], [50000, 11.5], [200000, 13.5], [300000, 15]], "conj": [3400, 2150], "min": [5550, [2400, 2700, 4000, 4500], 2800], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": [5790, [2510, 2820, 4170, 4700], 2920], "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": [6105, [2640, 2970, 4400, 4950], 3080], "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": [5550, [2400, 2970, 4400, 4950], 2800], "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": [5606, [2424, 2727, 4040, 4545], 2828], "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": [5789, [2503, 2816, 4172, 4694], 2920], "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": [5956.65, [2575.85, 2897.83, 4400, 4950], 3005.16], "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": [6105, [2640, 2970, 4400, 4950], 3080], "orient": false}}};

function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function red20(n) {
  if (n >= 19747.5) return 0;
  if (n <= 14852) return 7302;
  if (n <= 17673.52) return 7302 - 1.75 * (n - 14852);
  return Math.max(0, 2364.34 - 1.14 * (n - 17673.52));
}
function da61(rit) {
  if (rit <= 0 || rit >= 20048.45) return 0;
  return rit <= 17094 ? 590.89 : 590.89 - 0.2 * (rit - 17094);
}
// Minimo por descendientes: los de 3 a 24 anos ocupan los primeros lugares (nacieron antes); los menores de 3 anos, los ultimos.
function minHijos(may, men, cfg) {
  may = +may || 0; men = +men || 0;
  var t = 0, n = may + men, i;
  for (i = 0; i < n; i++) t += cfg[1][Math.min(i, 3)];
  return t + men * cfg[2];
}
function cuotaIntegra(big, bia, m, esc) {
  var mg = Math.min(m, big), ma = Math.min(m - mg, bia);
  return Math.max(0, escala(big, esc) - escala(mg, esc)) + Math.max(0, escala(bia, P.aho) - escala(ma, P.aho));
}
// Liquida un declarante (o la unidad familiar entera): rit y ss = rendimientos integros y cotizacion; s = ahorro; red = reduccion por tributacion conjunta.
function liquidar(rit, ss, s, mEst, mAut, cc, red) {
  var neto = Math.max(rit - ss, 0), otros = Math.min(2000, neto);
  var r = s <= 6500 ? red20(neto) : 0;
  var rn = Math.max(0, neto - otros - r), big = rn, bia = s;
  var g = Math.min(red, big); big -= g; bia = Math.max(0, bia - (red - g));
  var ci = cuotaIntegra(big, bia, mEst, P.est) + cuotaIntegra(big, bia, mAut, cc.esc);
  var ded = s <= 6500 ? da61(rit) : 0, lim = big + bia > 0 ? ci * big / (big + bia) : 0;
  return Math.max(0, ci - Math.min(ded, lim));
}
function comparar(d) {
  var cc = P.ccaa[d.ccaa], ce = P.min, ca = cc.min || P.min;
  var may = (+d.hijosMayores || 0) + (+d.hijosAdultos || 0), he = minHijos(may, d.hijosMenores, ce), ha = minHijos(may, d.hijosMenores, ca);
  var ind, con;
  if (d.tipo === "mono") {
    ind = liquidar(d.b1, d.ss, d.ahorro, ce[0] + he, ca[0] + ha, cc, 0);
    con = liquidar(d.b1, d.ss, d.ahorro, ce[0] + he, ca[0] + ha, cc, P.conj[1]);
    return { ind: ind, con: con };
  }
  var tot = d.b1 + d.b2, s1 = tot > 0 ? d.ss * d.b1 / tot : 0, s2 = d.ss - s1;
  ind = liquidar(d.b1, s1, d.ahorro / 2, ce[0] + he / 2, ca[0] + ha / 2, cc, 0) + liquidar(d.b2, s2, d.ahorro / 2, ce[0] + he / 2, ca[0] + ha / 2, cc, 0);
  con = liquidar(tot, d.ss, d.ahorro, ce[0] + he, ca[0] + ha, cc, P.conj[0]);
  return { ind: ind, con: con };
}
function difConSegundo(d, b2) {
  var tot = d.b1 + d.b2, tasa = tot > 0 ? d.ss / tot : 0;
  var x = { tipo: d.tipo, b1: d.b1, b2: b2, ss: tasa * (d.b1 + b2), ahorro: d.ahorro, hijosMenores: d.hijosMenores, hijosMayores: d.hijosMayores, hijosAdultos: d.hijosAdultos, ccaa: d.ccaa };
  var c = comparar(x); return c.ind - c.con;
}
function calcular(d) {
  if (d.tipo === "mono" && (+d.hijosMenores || 0) + (+d.hijosMayores || 0) < 1) {
    return { invalido: 1, cuotaIndividual: 0, cuotaConjunta: 0, diferencia: 0, ahorroConjunta: 0, ahorroIndividual: 0, ganador: "invalido", umbralSegundoSueldo: null, conjuntaSiempre: false, orientativo: P.ccaa[d.ccaa].orient ? 1 : 0, ccaaNombre: P.ccaa[d.ccaa].n };
  }
  var c = comparar(d), dif = c.ind - c.con, umbral = null, siempre = false;
  if (d.tipo !== "mono") {
    var tope = Math.max(150000, 3 * d.b1), paso = 250, b;
    if (difConSegundo(d, 0) > 0.5) {
      siempre = true;
      for (b = paso; b <= tope; b += paso) {
        if (difConSegundo(d, b) <= 0.5) {
          var lo = b - paso, hi = b, j;
          for (j = 0; j < 30; j++) { var m = (lo + hi) / 2; if (difConSegundo(d, m) > 0.5) lo = m; else hi = m; }
          umbral = (lo + hi) / 2; siempre = false; break;
        }
      }
    }
  }
  return {
    cuotaIndividual: c.ind, cuotaConjunta: c.con, diferencia: dif,
    ahorroConjunta: Math.max(dif, 0), ahorroIndividual: Math.max(-dif, 0),
    ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "conjunta" : "individual"),
    umbralSegundoSueldo: umbral, conjuntaSiempre: siempre,
    orientativo: P.ccaa[d.ccaa].orient ? 1 : 0, ccaaNombre: P.ccaa[d.ccaa].n
  };
}
function eur(x) { return EM.eur(x); }
function leer() {
  var d = {}; ["b1", "b2", "ss", "ahorro", "hijosMenores", "hijosMayores", "hijosAdultos"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.tipo = document.getElementById("tipo").value; d.ccaa = document.getElementById("ccaa").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.b1 < 0 || d.b2 < 0 || d.ss < 0 || d.ahorro < 0 || (d.b1 + (d.tipo === "mono" ? 0 : d.b2)) <= 0 || d.ss > d.b1 + d.b2) return;
  if (d.tipo === "mono") d.b2 = 0;
  var r = calcular(d), mono = d.tipo === "mono", abs = Math.abs(r.diferencia);
  if (r.invalido) {
    EM.renderResult({ winner: "empate", verdict: "La declaración conjunta monoparental no es posible sin al menos un hijo menor de 18 años.", tone: "warn",
      note: '<p><strong>No hay unidad familiar monoparental:</strong> la modalidad 2 exige convivir con al menos un hijo menor de edad (o mayor incapacitado judicialmente), según el art. 82.1.2.ª de la Ley del IRPF. Los hijos de 18 a 24 años cuentan para el mínimo familiar en la declaración individual, pero por sí solos no permiten la conjunta. Añade un hijo menor de 18 años o elige «Matrimonio».</p>' });
    return;
  }
  var nom = r.ganador === "conjunta" ? "la declaración conjunta" : "la declaración individual";
  var verdict = r.ganador === "empate" ? 'Con estos datos, declarar en conjunta o por separado te cuesta lo mismo de IRPF.'
    : 'Con estos datos, ' + nom + ' te sale ' + EM.eur(abs) + ' más barata de cuota del IRPF 2026.';
  var note = '';
  if (r.orientativo) note += '<p><strong>Cifras autonómicas orientativas:</strong> para ' + r.ccaaNombre + ' alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»). El orden de magnitud es fiable, pero revisa tu comunidad en la AEAT antes de decidir.</p>';
  note += '<p><strong>Lectura:</strong> ';
  if (mono) note += 'en una familia monoparental la conjunta aplica una reducción de ' + EM.eur(P.conj[1]) + ' a la base y no pierde ningún mínimo, así que casi nunca sale peor; solo no sale mejor si no pagas IRPF. Si convives con el otro progenitor, esta reducción no se aplica. ';
  else if (r.umbralSegundoSueldo !== null) note += 'con tu primer sueldo, la conjunta compensa mientras el segundo sueldo bruto sea inferior a unos <strong>' + EM.eur(Math.round(r.umbralSegundoSueldo / 100) * 100) + '</strong> al año; por encima, suele salir mejor declarar por separado. ';
  else if (r.conjuntaSiempre) note += 'con tu primer sueldo, la conjunta sale mejor en todo el rango de segundo sueldo que probamos. ';
  else note += 'con estos datos la conjunta no mejora a la individual ni aunque el segundo sueldo fuera cero. ';
  note += 'La diferencia es de cuota; lo que pagues o te devuelvan dependerá además de tus retenciones. ' + (mono ? '' : 'En la conjunta firman los dos y responden solidariamente de la deuda (art. 84.6 de la Ley del IRPF). ') + 'Esta calculadora no incluye deducciones autonómicas, hijos con discapacidad, ascendientes, ni rentas inmobiliarias o de autónomos.</p><p><strong>Supuestos:</strong> la deducción por rendimientos del trabajo de la disposición adicional 61.ª se aplica a la suma de los dos sueldos en la conjunta (criterio coherente con la ley, pero que la AEAT no confirma expresamente); la cotización a la Seguridad Social se reparte entre los dos en proporción al sueldo' + (mono ? '' : '; y los intereses y dividendos se reparten a partes iguales, lo que solo es correcto si las cuentas o acciones son de los dos (gananciales)') + '.</p>';
  EM.renderResult({
    winner: r.ganador, verdict: verdict, tone: r.orientativo ? "warn" : (r.ganador === "empate" ? "info" : "ok"),
    bigNumber: abs, bigLabel: r.ganador === "empate" ? "de diferencia" : "menos de cuota con " + (r.ganador === "conjunta" ? "conjunta" : "individual"), format: EM.eur,
    barsLabel: "Cuota del IRPF 2026 según la modalidad",
    bars: [{ label: mono ? "Individual" : "Individual (suma de los dos)", value: r.cuotaIndividual, color: "a" }, { label: "Conjunta", value: r.cuotaConjunta, color: "b" }],
    cols: ["Cuota"],
    rows: [
      [mono ? "Declaración individual" : "Declaración individual (suma de los dos)", EM.eur(r.cuotaIndividual)],
      ["Declaración conjunta", EM.eur(r.cuotaConjunta)],
      { label: "Diferencia (positivo = conviene la conjunta)", values: [EM.eur(r.diferencia)], strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
