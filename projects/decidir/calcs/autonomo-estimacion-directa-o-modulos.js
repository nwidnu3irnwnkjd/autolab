// Autonomo: estimacion directa simplificada o modulos (2026). Parametros generados desde data/params.json (irpf_2026, autonomo_2026 y autonomo_modulos_2026; fuentes y fechas alli).
// est: escala estatal general; ccaa: escala general y minimo del contribuyente de cada comunidad (min null = estatal); reta: tabla de bases 2026.
var P = {"est": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5], [300000, 24.5]], "ccaa": {"andalucia": {"n": "Andalucía", "esc": [[0, 9.5], [13000, 12], [21100, 15], [35200, 18.5], [60000, 22.5]], "min": {"c": 5790}, "orient": false}, "aragon": {"n": "Aragón", "esc": [[0, 9.5], [13072.5, 12], [21210, 15], [36960, 18.5], [52500, 20.5], [60000, 23], [80000, 24], [90000, 25], [130000, 25.5]], "min": null, "orient": false}, "asturias": {"n": "Asturias", "esc": [[0, 9], [12450, 12], [17707.2, 14], [33007.2, 19.2], [53407.2, 21.5], [70000, 22.5], [90000, 25], [175000, 26]], "min": {"c": 6105}, "orient": false}, "baleares": {"n": "Illes Balears", "esc": [[0, 9], [10000, 11.25], [18000, 14.25], [30000, 17.5], [48000, 19], [70000, 21.75], [90000, 22.75], [120000, 23.75], [175000, 24.75]], "min": {"c": 5550}, "orient": false}, "canarias": {"n": "Canarias", "esc": [[0, 9], [13748, 11.5], [19422, 14], [35924, 18.5], [57566, 23.5], [93268, 25], [123745, 26]], "min": {"c": 5606}, "orient": false}, "cantabria": {"n": "Cantabria", "esc": [[0, 8.5], [13000, 11], [21000, 14.5], [35200, 18], [60000, 22.5], [90000, 24.5]], "min": null, "orient": false}, "clm": {"n": "Castilla-La Mancha", "esc": [[0, 9.5], [12450, 12], [20200, 15], [35200, 18.5], [60000, 22.5]], "min": null, "orient": false}, "cyl": {"n": "Castilla y León", "esc": [[0, 9], [12450, 12], [20200, 14], [35200, 18.5], [53407.2, 21.5]], "min": null, "orient": true}, "cataluna": {"n": "Cataluña", "esc": [[0, 9.5], [12500, 12.5], [22000, 16], [33000, 19], [53000, 21.5], [90000, 23.5], [120000, 24.5], [175000, 25.5]], "min": null, "orient": false}, "extremadura": {"n": "Extremadura", "esc": [[0, 7.75], [12450, 9.75], [20200, 16], [24200, 17.5], [35200, 21], [60000, 23.5], [80200, 24], [99200, 24.5], [120200, 25]], "min": null, "orient": false}, "galicia": {"n": "Galicia", "esc": [[0, 9], [12985.35, 11.65], [21068.6, 14.9], [35200, 18.4], [60000, 22.5]], "min": {"c": 5789}, "orient": false}, "madrid": {"n": "Comunidad de Madrid", "esc": [[0, 8.5], [13362.22, 10.7], [19004.63, 12.8], [35425.68, 17.4], [57320.4, 20.5]], "min": {"c": 5956.65}, "orient": false}, "murcia": {"n": "Región de Murcia", "esc": [[0, 9.5], [12450, 11.2], [20200, 13.3], [34000, 17.9], [60000, 22.5]], "min": null, "orient": true}, "rioja": {"n": "La Rioja", "esc": [[0, 8], [12450, 10.6], [20200, 13.6], [35200, 17.8], [40000, 18.3], [50000, 19], [60000, 24.5], [120000, 27]], "min": null, "orient": true}, "valencia": {"n": "Comunitat Valenciana", "esc": [[0, 8.8], [12000, 11.7], [22000, 14.6], [32000, 17], [42000, 19.4], [52000, 21.9], [62000, 24.4], [72000, 26.1], [100000, 27.35], [150000, 28.35], [200000, 29.35]], "min": {"c": 6105}, "orient": false}}, "minE": 5550, "reta": [["reducida", 670, 653.59, 718.94], ["reducida", 900, 718.95, 900.0], ["reducida", 1166.7, 849.67, 1166.7], ["general", 1300, 950.98, 1300], ["general", 1500, 960.78, 1500], ["general", 1700, 960.78, 1700], ["general", 1850, 1143.79, 1850], ["general", 2030, 1209.15, 2030], ["general", 2330, 1274.51, 2330], ["general", 2760, 1356.21, 2760], ["general", 3190, 1437.91, 3190], ["general", 3620, 1519.61, 3620], ["general", 4050, 1601.31, 4050], ["general", 6000, 1732.03, 5101.2], ["general", null, 1928.1, 5101.2]], "tipoReta": 0.315, "genericos": 0.07, "djPct": 0.05, "djMax": 2000};
var LIM = 250000, PD = 0.20, PM = 0.02;
function escala(base, tr) {
  var s = 0, i, hi;
  for (i = 0; i < tr.length; i++) {
    hi = i + 1 < tr.length ? tr[i + 1][0] : Infinity;
    if (base > tr[i][0]) s += (Math.min(base, hi) - tr[i][0]) * tr[i][1] / 100;
  }
  return s;
}
function cuotaBase(bg, cc) {
  var m = cc.min ? cc.min.c : P.minE;
  return Math.max(0, escala(bg, P.est) - escala(P.minE, P.est)) + Math.max(0, escala(bg, cc.esc) - escala(m, cc.esc));
}
function tramoReta(R) {
  var i, t;
  for (i = 0; i < P.reta.length; i++) {
    t = P.reta[i];
    if (t[1] === null || (i === 2 ? R < t[1] : R <= t[1])) return { n: i, base: t[2], tabla: t[0] };
  }
}
function cuotaReta(C) { return 12 * tramoReta(C > 0 ? (1 - P.genericos) * C / 12 : 0).base * P.tipoReta; }
function dj(N) { return Math.min(P.djMax, P.djPct * Math.max(N, 0)); }
// Punto fijo: la cuota depende del rendimiento computable (neto + cuota), que depende de la deduccion de dificil justificacion, que depende de la cuota.
function ssDirecta(I, G) {
  var s = 0, k, c;
  for (k = 0; k < 60; k++) { c = cuotaReta(I - G - dj(I - G - s)); if (Math.abs(c - s) < 1e-9) break; s = c; }
  return s;
}
// Reduccion del art. 32.2.3.o LIRPF: rentas totales (actividad + otras) por debajo de 12.000 EUR.
function reduccion(rn, otras) {
  var t = rn + otras;
  if (rn <= 0 || t >= 12000) return 0;
  return Math.min(t <= 8000 ? 1620 : 1620 - 0.405 * (t - 8000), rn);
}
function irpfAtribuible(rn, otras, cc) { return cuotaBase(Math.max(otras + rn - reduccion(rn, otras), 0), cc) - cuotaBase(Math.max(otras, 0), cc); }
function directa(I, G, otras, cc) {
  var s = ssDirecta(I, G), N = I - G - s, rn = N - dj(N), ir = irpfAtribuible(rn, otras, cc);
  return { ss: s, rn: rn, irpf: ir, neto: I - G - s - ir };
}
function modulos(I, G, previo, mod, otras, cc) {
  var s = cuotaReta(previo), rn = 0.95 * mod, ir = irpfAtribuible(rn, otras, cc);
  return { ss: s, rn: rn, irpf: ir, neto: I - G - s - ir };
}
function calcular(d) {
  var cc = P.ccaa[d.ccaa], I = Math.max(+d.ingresos || 0, 0), G = Math.max(+d.gastos || 0, 0), o = Math.max(+d.otras || 0, 0);
  var a = directa(I, G, o, cc), m = modulos(I, G, Math.max(+d.previo || 0, 0), Math.max(+d.modulos || 0, 0), o, cc), cargaM = m.ss + m.irpf, ge, lo, hi, mid, j, bloq = 0;
  function ok(g) { var x = directa(I, g, o, cc); return x.ss + x.irpf <= cargaM + 1e-9; }
  if (ok(0)) ge = 0;
  else if (!ok(I)) ge = null;
  else { lo = 0; hi = I; for (j = 0; j < 80; j++) { mid = (lo + hi) / 2; if (ok(mid)) hi = mid; else lo = mid; } ge = hi; }
  if (d.situacion === "directa_bloqueo") bloq = 1; else if (d.situacion === "sin_modulos") bloq = 2; else if (I > LIM) bloq = 3;
  var dif = m.neto - a.neto;
  return {
    ssDirecta: a.ss, rnDirecta: a.rn, irpfDirecta: a.irpf, netoDirecta: a.neto, ssModulos: m.ss, rnModulos: m.rn, irpfModulos: m.irpf, netoModulos: m.neto,
    diferencia: dif, ganador: Math.abs(dif) < 1 ? "empate" : (dif > 0 ? "modulos" : "directa"), pagoDirectaAnual: PD * Math.max(a.rn, 0), pagoModulosAnual: 4 * PM * Math.max(m.rn, 0),
    gastosEquilibrio: ge, exento130: (+d.retencion || 0) >= 70 ? 1 : 0, bloqueo: bloq, aviso150: I > 125000 && I <= LIM ? 1 : 0, orientativo: cc.orient ? 1 : 0, ccaaNombre: cc.n
  };
}
function plazo(sit) {
  if (sit === "inicio") return "Si empiezas la actividad, la renuncia a módulos se hace al presentar la declaración censal de inicio, o presentando el primer pago fraccionado en la forma de la estimación directa (art. 33.1 del Reglamento del IRPF).";
  if (sit === "directa_libre") return "Tu renuncia se prorroga sola cada año; para volver a módulos tienes que revocarla durante el mes de diciembre anterior al año en que quieras volver (art. 33.3 y 33.1.a del Reglamento del IRPF), si sigues cumpliendo los límites.";
  return "Para estar en directa en 2027 tendrías que renunciar a módulos en diciembre de 2026 (art. 33.1.a del Reglamento del IRPF) o presentando el pago fraccionado del primer trimestre de 2027 en la forma de la directa (art. 33.1.b). La Orden de 2027 todavía no está publicada y fija el plazo de cada año: la de 2026 lo cerró el 31/12/2025. La renuncia dura mínimo 3 años (art. 33.3).";
}
function decidir(r, d) {
  var eurS = EM.eur;
  if (r.bloqueo === 1) return { winner: "invalido", tone: "warn", verdict: "Ahora mismo no puedes elegir módulos: si renunciaste a ellos o te excluyeron hace menos de 3 años, tienes que tributar en estimación directa los tres años siguientes (art. 31.1.3.ª.5.ª de la Ley del IRPF y arts. 33.3 y 34.3 del Reglamento). La comparación solo tiene sentido cuando se cumpla ese plazo." };
  if (r.bloqueo === 2) return { winner: "invalido", tone: "warn", verdict: "Esta comparación solo vale si tu actividad figura en los anexos de la Orden de módulos y no determinas otra actividad en estimación directa (art. 31.1.3.ª.a de la Ley del IRPF). Si no figura, tu método es la estimación directa y no hay nada que elegir." };
  if (r.bloqueo === 3) return { winner: "invalido", tone: "warn", verdict: "Si en el año anterior tus ingresos superaron " + eurS(LIM) + ", no puedes aplicar módulos con ninguna de las lecturas del límite vigente (150.000 € en la ley consolidada, 250.000 € según el criterio de la Agencia Tributaria para 2026): tributarías en estimación directa." };
  var dif = r.diferencia, ge = r.gastosEquilibrio, v;
  if (r.ganador === "empate") return { winner: "empate", tone: "info", verdict: "Con estos datos, módulos y estimación directa simplificada te dejan prácticamente lo mismo al año (diferencia menor de 1 €): decide por la tranquilidad de cada régimen y por si tus ingresos o gastos van a cambiar." };
  if (r.ganador === "modulos") {
    v = "Con tus datos, módulos te deja " + eurS(dif) + " más al año que la estimación directa simplificada (" + eurS(r.netoModulos) + " frente a " + eurS(r.netoDirecta) + " netos después de gastos, Seguridad Social e IRPF), si tu rendimiento neto por módulos es el que has indicado. ";
    v += ge === null ? "La directa no llegaría a compensar ni con gastos iguales a tus ingresos." : (ge <= 0 ? "" : "La directa empezaría a salirte mejor a partir de unos " + eurS(ge) + " de gastos deducibles al año.");
    if (d.situacion === "directa_libre") v += " Para volver a módulos tendrías que revocar tu renuncia en diciembre.";
    return { winner: "modulos", tone: "ok", verdict: v };
  }
  v = "Con tus datos, la estimación directa simplificada te deja " + eurS(-dif) + " más al año que módulos (" + eurS(r.netoDirecta) + " frente a " + eurS(r.netoModulos) + " netos). ";
  if (d.situacion === "inicio") v += "Al darte de alta tendrías que renunciar a módulos y mantener la renuncia 3 años: compruébalo con tu gestor antes, porque tus gastos pueden cambiar.";
  else if (d.situacion === "directa_libre") v += "Ya estás en directa y tienes la renuncia en vigor: mantenerla es lo que te sale mejor con estos datos.";
  else v += "Para estar en directa en 2027 tendrías que renunciar a módulos en diciembre de 2026 y mantener la renuncia 3 años: compruébalo con tu gestor antes, porque tus gastos pueden cambiar.";
  return { winner: "directa", tone: "ok", verdict: v };
}
function eur(x) { return EM.eur(x); }
var IDS = ["ingresos", "gastos", "previo", "modulos", "otras", "retencion"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value) || 0; });
  d.ccaa = document.getElementById("ccaa").value; d.situacion = document.getElementById("situacion").value;
  return d;
}
function pintar() {
  var d = leer(), r = calcular(d), dec = decidir(r, d);
  if (r.bloqueo) { EM.renderResult({ winner: dec.winner, tone: dec.tone, verdict: dec.verdict, note: "<p>Esta herramienta compara el régimen de módulos con la estimación directa simplificada de una persona física sin sociedad. Las cifras de referencia son las de 2026 (Orden HAC/1425/2025).</p>" }); return; }
  var tq = function (x) { return eur(x / 4); }, note = "";
  if (r.orientativo) note += "<p><strong>Cifras autonómicas orientativas:</strong> para " + r.ccaaNombre + " alguna cifra del IRPF autonómico no se ha podido confirmar del todo en el BOE (ver «Fuentes»).</p>";
  if (r.aviso150) note += "<p><strong>Atención al límite:</strong> con " + eur(d.ingresos) + " de ingresos puedes quedar fuera de módulos. Para 2026, la Agencia Tributaria (criterio de la DGT, nota de 1/4/2026) aplica 250.000 € al año y 125.000 € si facturas a empresas o profesionales; la ley consolidada fija 150.000 € y 75.000 €. Para 2027 rige la ley (150.000 € y 75.000 €) mientras no haya prórroga ni Orden de 2027: si en 2026 facturas más de 150.000 € (o más de 75.000 € a empresas), puede que en 2027 no puedas estar en módulos, así que no decidas apoyándote en 250.000 €.</p>";
  note += "<p><strong>Plazo de renuncia:</strong> " + plazo(d.situacion) + "</p>";
  note += "<p><strong>Pagos trimestrales (media, antes de restar retenciones):</strong> en directa, el modelo 130 suma el 20 % de tu rendimiento neto del año (" + tq(r.pagoDirectaAnual) + " por trimestre); en módulos, el modelo 131 es el 2 % del rendimiento neto de módulos reducido en cada trimestre, sin asalariados (" + tq(r.pagoModulosAnual) + " de media). Son anticipos del IRPF, no un coste adicional.";
  if (r.exento130) note += " La exención del modelo 130 por tener al menos el 70 % de ingresos con retención (art. 109.2) es solo para actividades profesionales; las actividades de módulos son empresariales y no se aplica.";
  note += "</p>";
  note += "<p>La cuota de autónomos pasa de " + eur(r.ssDirecta) + " en directa a " + eur(r.ssModulos) + " en módulos porque en módulos cotizas por el rendimiento neto previo que has indicado, no por tus ingresos menos gastos reales.</p>";
  note += "<p><strong>No incluye:</strong> IVA (renunciar a módulos supone renunciar también al régimen simplificado del IVA, y al revés: art. 33.2 del Reglamento del IVA y art. 36 del Reglamento del IRPF; en directa pasas al IVA general y su efecto no se calcula), agricultura, ganadería y pesca, recargo de equivalencia, País Vasco y Navarra, Ceuta y Melilla (la disposición adicional 64.ª de la Ley del IRPF mejora en 2026 la difícil justificación y la reducción de módulos en Ceuta), Canarias (IGIC: la renuncia también arrastra, art. 36 del Reglamento del IRPF), hijos y deducciones, la reducción del 20 % del IRPF del primer año con beneficios y del siguiente (art. 32.3 de la Ley del IRPF, solo en directa: baja el IRPF de la directa), la reducción por cliente único (art. 32.2.1.º, también solo en directa), la tarifa plana, el personal asalariado y los gastos extraordinarios por circunstancias excepcionales. El rendimiento neto por módulos no se calcula: es el dato que tú introduces.</p>";
  EM.renderResult({
    winner: dec.winner, verdict: dec.verdict, tone: dec.tone,
    bigNumber: Math.abs(r.diferencia), bigLabel: r.ganador === "empate" ? "de diferencia al año" : (r.ganador === "modulos" ? "más al año con módulos" : "más al año con estimación directa"), format: eur,
    barsLabel: "Neto anual después de gastos, Seguridad Social e IRPF",
    bars: [{ label: "Directa simplificada" + (r.ganador === "directa" ? " (gana)" : ""), value: Math.max(r.netoDirecta, 0), color: "a" },
           { label: "Módulos" + (r.ganador === "modulos" ? " (gana)" : ""), value: Math.max(r.netoModulos, 0), color: "b" }],
    cols: ["Directa simplificada", "Módulos"],
    rows: [
      ["Ingresos", eur(d.ingresos), eur(d.ingresos)],
      ["Gastos reales (se pagan igual)", eur(d.gastos), eur(d.gastos)],
      ["Rendimiento neto fiscal", eur(r.rnDirecta), eur(r.rnModulos)],
      ["Seguridad Social (cuota de autónomos)", eur(r.ssDirecta), eur(r.ssModulos)],
      ["IRPF atribuible a la actividad", eur(r.irpfDirecta), eur(r.irpfModulos)],
      { label: "Neto al año", values: [eur(r.netoDirecta), eur(r.netoModulos)], strong: true },
      ["Pago fraccionado por trimestre (medio)", tq(r.pagoDirectaAnual), tq(r.pagoModulosAnual)]
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
