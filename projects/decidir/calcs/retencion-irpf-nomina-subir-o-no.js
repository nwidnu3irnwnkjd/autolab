// Retencion del IRPF en nomina vs impuesto 2026. Parametros generados desde data/params.json -> irpf_2026 y retencion_irpf_nomina_2026 (fuentes y fechas alli).
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "min": [5550, [2400, 2700, 4000, 4500], 2800], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": [5790, [2510, 2820, 4170, 4700], 2920], "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": [6105, [2640, 2970, 4400, 4950], 3080], "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": [5550, [2400, 2970, 4400, 4950], 2800], "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": [5606, [2424, 2727, 4040, 4545], 2828], "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": [5789, [2503, 2816, 4172, 4694], 2920], "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": [5956.65, [2575.85, 2897.83, 4400, 4950], 3005.16], "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": [6105, [2640, 2970, 4400, 4950], 3080], "orient": false}}, "ret": [[0, 19], [12450, 24], [20200, 30], [35200, 37], [60000, 45], [300000, 47]], "ss": 0.065, "ssTope": 61214.4, "lim81": [15876, 16342, 16867], "umbral": 100, "meses": 12, "oblGen": 22000, "oblMulti": 15876, "oblResto": 1500};
function scale(x, esc) {
  var t = 0, i, hi;
  for (i = 0; i < esc.length; i++) { hi = i + 1 < esc.length ? esc[i + 1][0] : Infinity; if (x > esc[i][0]) t += (Math.min(x, hi) - esc[i][0]) * esc[i][1] / 100; }
  return t;
}
function minimo(m, n, m3, mitad) {
  var s = 0, i; for (i = 0; i < n; i++) s += m[1][Math.min(i, 3)];
  return m[0] + (s + m3 * m[2]) * (mitad ? 0.5 : 1);
}
function art20(rn) { return rn <= 14852 ? 7302 : rn <= 17673.52 ? 7302 - 1.75 * (rn - 14852) : rn < 19747.5 ? 2364.34 - 1.14 * (rn - 17673.52) : 0; }
function retencion(R, n, m3, mitad) {
  if (!(R > 0)) return 0;
  var lim = P.lim81[Math.min(n, 2)];
  if (R <= lim) return 0;
  var rnAb = R - P.ss * Math.min(R, P.ssTope), g = Math.min(2000, rnAb), red = Math.min(art20(rnAb), rnAb);
  var base = Math.max(0, rnAb - g - red - (n >= 3 ? 600 : 0)), mn = minimo(P.min, n, m3, mitad);
  if (base - mn <= 0) return 0;
  var cuota = Math.max(0, scale(base, P.ret) - scale(mn, P.ret));
  if (R <= 35200) cuota = Math.min(cuota, 0.43 * Math.max(0, R - lim));
  return Math.round(cuota / R * 10000 + 1e-7) / 100;
}
function calcular(d) {
  var R1 = +d.bruto || 0, n = Math.floor(+d.hijos || 0), m3 = Math.floor(+d.menores3 || 0), mitad = d.reparto === "mitad", R2 = Math.max(0, +d.pagador2 || 0), ret = Math.max(0, +d.ret || 0), eu = +d.euribor || 0;
  var c = P.ccaa[d.ccaa];
  if (!c || m3 > n || n > 10 || R1 <= 0) return { bloqueado: 1, escenario: 0, cuota: 0, cuotaIntegra: 0, ded: 0, ret1: 0, ret2: 0, retenido: 0, resultado: 0, tipo0: 0, tipo0p2: 0, tipoLegal: 0, tipo2: 0, obligado: 0, limiteObl: 0, coste: 0 };
  var R = R1 + R2, rnAb = R - P.ss * Math.min(R, P.ssTope), g = Math.min(2000, rnAb), blg = Math.max(0, rnAb - g - art20(rnAb));
  var mnE = minimo(P.min, n, m3, mitad), mnA = minimo(c.min || P.min, n, m3, mitad);
  var ci = Math.max(0, scale(blg, P.est) - scale(mnE, P.est)) + Math.max(0, scale(blg, c.esc) - scale(mnA, c.esc));
  var ded = 0;
  if (R < 20048.45) ded = Math.max(0, Math.min(R <= 17094 ? 590.89 : 590.89 - 0.2 * (R - 17094), ci));
  var cuota = ci - ded, t1 = retencion(R1, n, m3, mitad), t2 = R2 > 0 ? retencion(R2, 0, 0, false) : 0;
  var ret1 = R1 * ret / 100, ret2 = R2 * t2 / 100, res = cuota - ret1 - ret2, lim = (R2 > 0 ? Math.min(R1, R2) : 0) <= P.oblResto ? P.oblGen : P.oblMulti, obl = R > lim ? 1 : 0;
  var esc = res > P.umbral ? (obl ? 1 : 4) : res < -P.umbral ? 2 : 3;
  return { bloqueado: 0, escenario: esc, cuota: cuota, cuotaIntegra: ci, ded: ded, ret1: ret1, ret2: ret2, retenido: ret1 + ret2, resultado: res,
    tipo0: Math.min(100, Math.max(0, (cuota - ret2) / R1 * 100)), tipo0p2: R2 > 0 ? Math.min(100, Math.max(0, (cuota - ret1) / R2 * 100)) : 0, alcanza1: (cuota - ret2) / R1 * 100 <= 47 ? 1 : 0, alcanza2: R2 > 0 && (cuota - ret1) / R2 * 100 <= 47 ? 1 : 0, tipoLegal: t1, tipo2: t2, obligado: obl, limiteObl: lim, coste: Math.abs(res) * eu / 100 * P.meses / 12, orientativo: c.orient ? 1 : 0 };
}
function eur(x) { return EM.eur(x); }
function pct(x) { return EM.num(x, 2) + " %"; }
function leer() {
  var d = {}; ["bruto", "ret", "hijos", "menores3", "pagador2", "euribor"].forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.reparto = document.getElementById("reparto").value; d.ccaa = document.getElementById("ccaa").value;
  return d;
}
function pintar() {
  var d = leer();
  if (d.bruto <= 0 || d.ret < 0 || d.ret > 100 || d.hijos < 0 || d.menores3 < 0 || d.pagador2 < 0) return;
  var r = calcular(d);
  if (r.bloqueado) {
    var foral = !P.ccaa[d.ccaa];
    EM.renderResult({ winner: "bloqueado-" + (foral ? "f" : "h"), verdict: foral ? "Esta calculadora no cubre el País Vasco ni Navarra: tienen su propio IRPF y sus propias retenciones." : "Los hijos menores de 3 años no pueden ser más que el total de hijos.", tone: "warn",
      note: foral ? "<p>Consulta la Hacienda Foral de tu territorio. Las escalas y los tipos de retención de esta página son los del régimen común.</p>" : "<p>Corrige el número de hijos o el de menores de 3 años.</p>" });
    return;
  }
  var ex = r.resultado, a = Math.abs(ex), t0 = Math.ceil(r.tipo0 * 100 - 1e-9) / 100, ver, tone, big, bigL, extra = "";
  if (r.escenario === 1) {
    ver = "Con estos datos te saldría a pagar unos " + eur(a) + " en la Renta 2026: tu retención se queda corta. " + (r.alcanza1 ? "Si pides a tu pagador un tipo voluntario del " + pct(t0) + " (art. 88.5 del Reglamento del IRPF) el resultado quedaría en torno a 0." : "Con tu primer pagador no se puede cubrir todo el pago con un tipo razonable: tendrías que pedir también un tipo mayor al segundo pagador.");
    tone = "warn"; big = a; bigL = "a pagar en la Renta 2026 (estimado)";
    extra = "<p><strong>Qué cambia y qué no:</strong> subir el tipo no reduce tu impuesto, solo adelanta el pago a lo largo del año. Si lo pides ahora y ya has cobrado parte del año, el tipo se aplica solo a las nóminas que queden, así que tendría que ser más alto que " + pct(t0) + " para llegar al mismo importe (aproximadamente, lo que falta por retener dividido entre lo que te queda por cobrar). El tipo voluntario se mantiene hasta final de año y en los años siguientes mientras no lo renuncies por escrito. Adelantar esos " + eur(a) + " unos 12 meses (se retienen de media a mitad de 2026 y los pagarías con la campaña de la Renta de 2027) te cuesta unos " + eur(r.coste) + " de intereses que no cobrarías si tu ahorro rinde el " + EM.num(d.euribor, 2) + " % que indicas.</p>";
  } else if (r.escenario === 4) {
    ver = "Con estos datos saldría un pago de unos " + eur(a) + ", pero no estás obligado a declarar (cobras " + eur(d.bruto + d.pagador2) + " y tu límite es " + eur(r.limiteObl) + "), así que no tendrías que pagar esa diferencia salvo que presentes la declaración por otro motivo. Subir la retención solo tendría sentido si prefieres ir cubierto.";
    tone = "info"; big = a; bigL = "de diferencia estimada (no obligado a declarar)";
    extra = "<p>Si presentas la declaración (por ejemplo, para aplicar una deducción que sí te corresponda), la diferencia se liquidaría y saldría a pagar. " + (r.alcanza1 ? "Para dejarla en 0 bastaría un tipo del " + pct(t0) + "." : "Con tu primer pagador no basta: habría que pedir también un tipo mayor al segundo.") + "</p>";
  } else if (r.escenario === 2) {
    ver = "Con estos datos te saldría a devolver unos " + eur(a) + " en la Renta 2026: retienes de más y no necesitas subir el tipo. Subirlo sería prestar dinero a Hacienda sin intereses (a un " + EM.num(d.euribor, 2) + " % de ahorro dejarías de ganar unos " + eur(r.coste) + " al año).";
    tone = "ok"; big = a; bigL = "a devolver en la Renta 2026 (estimado)";
    extra = "<p>El Reglamento solo permite pedir un tipo superior, no uno inferior (art. 88.5); lo que sí puedes es comunicar a tu pagador los cambios de tu situación personal y familiar que bajen el tipo (art. 88.4). Hacienda tiene seis meses desde el fin del plazo de presentación para devolverte la diferencia y, pasado ese plazo, te abona intereses de demora si el retraso es imputable a la Administración (art. 103.4 de la Ley del IRPF). Si no estás obligado a declarar y te sale devolución, tienes que presentar la declaración para recuperarla.</p>";
  } else {
    ver = "Con estos datos tu retención es casi justa: la diferencia con el impuesto estimado es de unos " + eur(a) + ", dentro del margen del modelo (" + eur(P.umbral) + "), así que no hace falta subirla ni bajarla.";
    tone = "ok"; big = a; bigL = ex >= 0 ? "a pagar (estimado)" : "a devolver (estimado)";
  }
  var avisos = "";
  if (r.tipoLegal - d.ret > 0.5) avisos += "<p><strong>Tu nómina retiene menos que el Reglamento:</strong> con los datos que has puesto, el tipo del Reglamento sería el " + pct(r.tipoLegal) + " y tu nómina aplica el " + pct(d.ret) + ". Revisa que tu pagador tenga tu situación familiar actualizada (modelo 145) o si tienes un cambio de retribución pendiente de regularizar.</p>";
  else if (d.ret - r.tipoLegal > 0.5) avisos += "<p><strong>Tu nómina retiene más que el Reglamento:</strong> con los datos que has puesto, el tipo del Reglamento sería el " + pct(r.tipoLegal) + " y tu nómina aplica el " + pct(d.ret) + ", por ejemplo porque pediste un tipo voluntario o porque tu pagador cuenta con menos circunstancias personales de las que has puesto aquí.</p>";
  if (d.pagador2 > 0) avisos += "<p><strong>Segundo pagador:</strong> cada pagador calcula su retención sin conocer lo que cobras del otro (el Reglamento no prevé ningún mecanismo para repartir el exceso). Se estima que el segundo retiene un " + pct(r.tipo2) + (r.tipo2 === 0 ? " (por debajo de " + eur(P.lim81[0]) + " no retiene)" : "") + ", y por eso suele quedarse corto el total. " + (r.alcanza2 ? "También puedes pedirle a él un tipo voluntario: bastaría un " + pct(Math.ceil(r.tipo0p2 * 100 - 1e-9) / 100) + " sobre sus " + eur(d.pagador2) + "." : "Pedirle solo a él no basta, porque su importe es demasiado pequeño para cubrir la diferencia; hay que pedirlo al primer pagador.") + " Si su contrato dura menos de un año, retiene al menos el 2 % (art. 86.2 del Reglamento).</p>";
  if (r.orientativo) avisos += "<p><strong>Escala autonómica orientativa:</strong> alguna cifra de tu comunidad no se ha podido confirmar del todo en el BOE (ver «Fuentes»); revisa la AEAT antes de decidir.</p>";
  var nota = extra + avisos + "<p><strong>Límites del cálculo:</strong> estima el impuesto del trabajo en declaración individual con la escala estatal y la de tu comunidad. No incluye planes de pensiones, deducciones autonómicas o estatales, alquileres, ahorro, discapacidad, ascendientes, Ceuta y Melilla ni Canarias. La retención no es el impuesto: es un adelanto, y la diferencia se liquida en la Renta.</p>";
  EM.renderResult({
    winner: "e" + r.escenario, verdict: ver, tone: tone, bigNumber: big, bigLabel: bigL, format: EM.eur,
    barsLabel: "IRPF 2026 estimado frente a lo retenido",
    bars: [{ label: "Cuota del IRPF estimada", value: r.cuota, color: "a" }, { label: "Retenido en el año", value: r.retenido, color: "b" }],
    cols: ["Importe"],
    rows: [
      ["Cuota estimada del IRPF 2026", eur(r.cuota)],
      ["Retenido en el año (nómina" + (d.pagador2 > 0 ? " y segundo pagador" : "") + ")", eur(r.retenido)],
      { label: "Resultado (positivo = a pagar, negativo = a devolver)", values: [eur(ex)], strong: true },
      ["Tipo de retención que lo deja en 0", pct(t0)],
      ["Tipo que da el Reglamento para tus datos", pct(r.tipoLegal)],
      ["¿Obligado a declarar? (límite " + eur(r.limiteObl) + ")", r.obligado ? "Sí" : "No"]
    ],
    note: nota
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
