// Subsidio por desempleo: derecho, cuantía y duración (2026). Parámetros desde data/params.json -> subsidio_desempleo_2026 (fuentes y fechas allí).
// Cuantía = % del IPREM mensual (95 % días 1-180, 90 % días 181-360, 80 % desde el 361). Duración por art. 277 (agotado: 6, 24 o 30 meses; cotización insuficiente: 3, 4, 5, 6 o 21). Mayores de 52: 80 % del IPREM hasta la edad ordinaria de jubilación (cotas 65 y 67).
var P = {"iprem": 600, "pct": [95, 90, 80], "tramos": [180, 360], "pct52": 80, "smi": 1221, "pctSmi": 75, "edadSin": 45, "prestSin": 360, "prestMin": 120, "prestLargo": 180, "mesesSin": 6, "mesesCon120": 24, "mesesCon180": 30, "cotMin": 90, "cotPrest": 360, "tablaInsuf": [[90, 3], [120, 4], [150, 5]], "insufSin": 180, "mesesInsufSin": 6, "mesesInsufCon": 21, "edad52": 52, "ordMin": 65, "ordMax": 67, "diasMes": 30};
function calcular(d) {
  var dias = Math.round(d.dias), h = Math.max(Math.round(d.hijos), 0), edad = Math.floor(d.edad), i;
  if (d.situ === "agotado" && dias < P.prestMin) return { bloqueo: 1 };
  if (d.situ !== "agotado" && dias < P.cotMin) return { bloqueo: 2 };
  if (d.situ !== "agotado" && dias >= P.cotPrest) return { bloqueo: 3 };
  var umbralC = P.smi * P.pctSmi, miembros = 1 + (d.conyuge === "si" ? 1 : 0) + h;
  var propiaC = Math.round(d.renta * 100), famC = Math.round((d.renta + d.rentaOtros) * 100);
  var propiaOk = propiaC <= umbralC, cargas = miembros > 1 && famC <= umbralC * miembros, rentaOk = propiaOk || cargas;
  var r = { bloqueo: 0, umbral: umbralC / 100, miembros: miembros, propiaOk: propiaOk ? 1 : 0, cargas: cargas ? 1 : 0, rentaOk: rentaOk ? 1 : 0, perCapita: famC / 100 / miembros, gen: 0, motivo: 0, meses: 0, d52: 0 };
  if (!rentaOk) r.motivo = 1;
  else if (d.situ === "agotado") {
    if (edad < P.edadSin && !cargas && dias < P.prestSin) r.motivo = 2;
    else { r.gen = 1; r.meses = cargas ? (dias >= P.prestLargo ? P.mesesCon180 : P.mesesCon120) : P.mesesSin; }
  } else {
    r.gen = 1; r.meses = cargas ? P.mesesInsufCon : P.mesesInsufSin;
    if (dias < P.insufSin) { r.meses = 0; for (i = 0; i < P.tablaInsuf.length; i++) if (dias >= P.tablaInsuf[i][0]) r.meses = P.tablaInsuf[i][1]; }
  }
  if (r.gen) {
    var D = r.meses * P.diasMes, t1 = Math.min(D, P.tramos[0]), t2 = Math.max(Math.min(D, P.tramos[1]) - P.tramos[0], 0), t3 = Math.max(D - P.tramos[1], 0);
    r.dur = D; r.dias1 = t1; r.dias2 = t2; r.dias3 = t3;
    r.m1 = P.iprem * P.pct[0] / 100; r.m2 = P.iprem * P.pct[1] / 100; r.m3 = P.iprem * P.pct[2] / 100;
    r.tot1 = r.m1 * t1 / P.diasMes; r.tot2 = r.m2 * t2 / P.diasMes; r.tot3 = r.m3 * t3 / P.diasMes;
    r.total = r.tot1 + r.tot2 + r.tot3;
  }
  if (edad >= P.edad52 && edad < P.ordMax && d.jub === "si" && propiaOk) {
    r.d52 = 1; r.m52 = P.iprem * P.pct52 / 100;
    r.meses52min = Math.max(P.ordMin - edad, 0) * 12; r.meses52max = (P.ordMax - edad) * 12;
    r.total52min = r.m52 * r.meses52min; r.total52max = r.m52 * r.meses52max;
  }
  return r;
}
function eur(x) { return EM.eur(x, Math.abs(x - Math.round(x)) > 0.004 ? 2 : 0); }
function txtMeses(n) { return EM.num(n, 0) + (n === 1 ? " mes" : " meses"); }
var IDS = ["dias", "edad", "hijos", "renta", "rentaOtros"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.situ = document.getElementById("situ").value; d.conyuge = document.getElementById("conyuge").value; d.jub = document.getElementById("jub").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
function pintar() {
  var d = leer();
  if (d.dias < 0 || d.hijos < 0 || d.renta < 0 || d.rentaOtros < 0) { aviso("Revisa los datos: los días, los hijos y las rentas no pueden ser negativos."); return; }
  if (d.edad <= 0 || d.edad > 100) { aviso("Revisa la edad: indica tu edad en años cumplidos."); return; }
  var r = calcular(d), um = EM.eur(P.smi * P.pctSmi / 100, 2);
  if (r.bloqueo === 1) { aviso("La prestación contributiva dura como mínimo " + P.prestMin + " días; con menos no encaja ninguna situación de la ley. Revisa los días de prestación que cobraste."); return; }
  if (r.bloqueo === 2) { aviso("Con menos de " + P.cotMin + " días cotizados no hay subsidio por cotización insuficiente (art. 274.1.b de la LGSS). Si agotaste una prestación, elige «He agotado el paro»."); return; }
  if (r.bloqueo === 3) { aviso("Con " + P.cotPrest + " días cotizados o más tienes derecho a la prestación contributiva (paro), no al subsidio por cotización insuficiente. Calcula primero <a href=\"/decidir/cuanto-cobro-de-paro-prestacion-desempleo/\">cuánto cobrarías de paro</a>."); return; }
  var rentaTxt = "Rentas del mes natural anterior: tuyas " + eur(d.renta) + (r.miembros > 1 ? "; por persona de tu unidad familiar (" + r.miembros + " miembros) " + eur(r.perCapita) : "") + "; límite " + um + " al mes (75 % del SMI sin pagas extra).";
  if (r.motivo === 1) {
    aviso("Con tus datos no tendrías derecho al subsidio: tus rentas propias superan " + um + " al mes" + (r.miembros > 1 ? " y la renta por persona de tu unidad familiar (" + eur(r.perCapita) + ") también supera ese límite" : "") + ". La opción no existe si superas la renta; se mira el mes natural anterior a la solicitud, así que puede cambiar si tus ingresos bajan (art. 275 de la LGSS). " + rentaTxt);
    return;
  }
  if (r.motivo === 2) {
    aviso("Con tus datos no tendrías derecho al subsidio por haber agotado el paro: con menos de " + P.edadSin + " años y sin responsabilidades familiares se exige que la prestación agotada haya durado " + P.prestSin + " días o más, y la tuya duró " + EM.num(d.dias, 0) + " (art. 274.1.a de la LGSS). Con hijos o cónyuge a tu cargo y rentas bajas por persona sí tendrías derecho.");
    return;
  }
  if (r.d52) {
    var v52 = "Con tus datos tendrías derecho al subsidio para mayores de 52 años: " + eur(r.m52) + " al mes hasta tu edad ordinaria de jubilación (entre " + txtMeses(r.meses52min) + " y " + txtMeses(r.meses52max) + ", de " + eur(r.total52min) + " a " + eur(r.total52max) + " brutos, antes del IRPF). Es el subsidio que te corresponde si cumples el art. 280 (art. 274.3 de la LGSS): no se cobra a la vez que el subsidio general.";
    var n52 = "<p><strong>Cómo sale:</strong> " + rentaTxt + " En este subsidio solo cuentan tus rentas propias (art. 280.2) y no se computan el sueldo ni las prestaciones que ya no cobras el día de la solicitud (art. 275.5.e). La cuantía es el " + P.pct52 + " % del IPREM de " + eur(P.iprem) + " (art. 280.4) y dura hasta tu edad ordinaria de jubilación (entre " + P.ordMin + " y " + P.ordMax + " años según tu carrera, art. 205.1.a; el calendario transitorio no se modela). La entidad gestora cotiza por jubilación a tu favor (art. 280.9). Solicítalo en los 15 días hábiles siguientes al agotamiento del paro o de la situación legal de desempleo (art. 280.3).</p><p><strong>No incluye:</strong> la retención del IRPF, el patrimonio como renta, la compatibilidad con un trabajo, la Renta Activa de Inserción, el Ingreso Mínimo Vital, los fijos discontinuos y los trabajadores agrarios.</p>";
    EM.renderResult({ winner: "derecho52", verdict: v52, tone: "ok", bigNumber: r.m52, bigLabel: "al mes hasta la edad ordinaria de jubilación (bruto)", format: eur, barsLabel: "Subsidio mensual bruto", bars: [{ label: "Mayores de 52 años", value: r.m52, color: "a" }], cols: ["Mayores de 52 años"],
      rows: [["Porcentaje del IPREM", EM.num(P.pct52, 0) + " %"], ["Cuantía mensual", eur(r.m52)], ["Meses hasta la edad ordinaria", EM.num(r.meses52min, 0) + " a " + EM.num(r.meses52max, 0)], { label: "Total estimado (bruto)", values: [eur(r.total52min) + " a " + eur(r.total52max)], strong: true }], note: n52 });
    return;
  }
  var partes = [eur(r.m1) + " al mes los primeros " + r.dias1 + " días"];
  if (r.dias2 > 0) partes.push(eur(r.m2) + " desde el día " + (P.tramos[0] + 1) + (r.dias3 > 0 ? " hasta el " + P.tramos[1] : ""));
  if (r.dias3 > 0) partes.push(eur(r.m3) + " desde el día " + (P.tramos[1] + 1));
  var verdict = "Con tus datos tendrías derecho al subsidio" + (r.cargas ? " por responsabilidades familiares" : "") + ": " + partes.join(", ") + ", durante " + txtMeses(r.meses) + " (" + EM.num(r.dur, 0) + " días): unos " + eur(r.total) + " brutos en total, antes del IRPF.";
  var note = "<p><strong>Cómo sale:</strong> " + rentaTxt + (r.cargas && !r.propiaOk ? " Superas el límite con tus rentas propias, pero accedes por responsabilidades familiares (art. 274.2 de la LGSS)." : "") + " No cuentan como renta el sueldo ni las prestaciones que ya no cobras el día de la solicitud (art. 275.5.e). La cuantía es el " + P.pct[0] + " % del IPREM de " + eur(P.iprem) + " los primeros " + P.tramos[0] + " días, el " + P.pct[1] + " % hasta el día " + P.tramos[1] + " y el " + P.pct[2] + " % después (art. 278). La duración (art. 277) sale de " + (d.situ === "agotado" ? "los " + EM.num(d.dias, 0) + " días de paro que agotaste y de que " + (r.cargas ? "acreditas" : "no acreditas") + " responsabilidades familiares" : "los " + EM.num(d.dias, 0) + " días cotizados y de que " + (r.cargas ? "acreditas" : "no acreditas") + " responsabilidades familiares") + ".</p>";
  note += "<p><strong>Plazos:</strong> solicítalo en los 15 días hábiles siguientes al agotamiento del paro (o de la situación legal de desempleo); fuera de ese plazo, y dentro de los 6 meses, el derecho nace el día de la solicitud y pierdes los días intermedios (art. 276.1). Se reconoce por trimestres y hay que pedir cada prórroga acreditando de nuevo las rentas.</p>";
  note += "<p><strong>No incluye:</strong> la retención del IRPF, el patrimonio (el 100 % del interés legal del dinero de tu patrimonio, salvo la vivienda habitual, cuenta como renta), la compatibilidad con un trabajo y el complemento de apoyo al empleo (que consume días del subsidio, art. 282.3), la Renta Activa de Inserción, el subsidio de emigrantes retornados y de víctimas de violencia, los liberados de prisión, el Ingreso Mínimo Vital, los fijos discontinuos, los trabajadores agrarios, las ayudas autonómicas y los territorios forales en lo que no es la prestación estatal.</p>";
  var bars = [{ label: "Primeros " + r.dias1 + " días", value: r.m1, color: "a" }];
  var cols = ["Primeros " + P.tramos[0] + " días"];
  if (r.dias2 > 0) { bars.push({ label: "Días " + (P.tramos[0] + 1) + "-" + P.tramos[1], value: r.m2, color: "b" }); cols.push("Días " + (P.tramos[0] + 1) + "-" + P.tramos[1]); }
  if (r.dias3 > 0) { bars.push({ label: "Desde el día " + (P.tramos[1] + 1), value: r.m3, color: "c" }); cols.push("Desde el día " + (P.tramos[1] + 1)); }
  var ms = [r.m1, r.m2, r.m3].slice(0, cols.length), ds = [r.dias1, r.dias2, r.dias3].slice(0, cols.length), ts = [r.tot1, r.tot2, r.tot3].slice(0, cols.length);
  EM.renderResult({
    winner: (r.cargas ? "derechocargas" : "derecho"), verdict: verdict, tone: "ok",
    bigNumber: r.m1, bigLabel: "al mes los primeros " + P.tramos[0] + " días (bruto)", format: eur,
    barsLabel: "Subsidio mensual bruto", bars: bars, cols: cols,
    rows: [
      ["Porcentaje del IPREM"].concat(P.pct.slice(0, cols.length).map(function (p) { return EM.num(p, 0) + " %"; })),
      ["Cuantía mensual"].concat(ms.map(function (x) { return eur(x); })),
      ["Días de subsidio"].concat(ds.map(function (x) { return EM.num(x, 0); })),
      { label: "Total estimado (bruto): " + eur(r.total), values: ts.map(function (x) { return eur(x); }), strong: true }
    ],
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
