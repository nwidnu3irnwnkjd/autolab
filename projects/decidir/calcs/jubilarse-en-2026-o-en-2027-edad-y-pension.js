// Jubilarse en 2026 o en 2027. Parámetros y fuentes: data/params.json -> jubilarse_2026_2027 (LGSS 205.1, 209.1, 210.1-2, DT 4.ª.7, 7.ª, 9.ª, 40.ª) y jubilacion_2026 (pensión máxima, RD 241/2026).
var P = {"refAnio": 2026, "refMes": 10, "ordM": 780, "carencia": 180, "ed26": [459, 802], "ed27": [462, 804], "basePct": 50, "topePct": 100, "pc26": [49, 0.21, 0.19], "pc27": [248, 0.19, 0.18], "demAnio": 12, "dt40": {"2026": [302, 304, 352.33], "2027": [304, 308, 354.67], "2028": [306, 312, 357.00], "2029": [308, 316, 359.33], "2030": [310, 320, 361.67], "2031": [312, 324, 364.00], "2032": [314, 328, 366.33], "2033": [316, 332, 368.67], "2034": [318, 336, 371.00], "2035": [320, 340, 373.33], "2036": [322, 344, 375.67]}, "dt40f": [324, 348, 378], "old": [300, 350], "rec": 60, "maxMes": 3359.6, "bmax": 5101.2, "nacMin": 1955, "nacMax": 1966, "hasta": 2036, "cotMax": 60, "ed25": [459, 800], "ed24": [456, 798], "reval": 2.7, "altDesde": 2024};
var REF = P.refAnio * 12 + P.refMes - 1;
// Mes absoluto = año * 12 + (mes - 1). Hecho causante = mes t; la cotización sigue sin interrupción desde la fecha de referencia.
function cotEn(t, cot0) { return cot0 + t - REF; }
// Edad exigida en meses (art. 205.1.a + DT 7.ª, según el año del hecho causante).
function edadExigida(t, c) {
  var y = Math.floor(t / 12), e = y === P.altDesde ? P.ed24 : (y === P.altDesde + 1 ? P.ed25 : (y === P.refAnio ? P.ed26 : P.ed27));
  return c >= e[0] ? P.ordM : e[1];
}
// Porcentaje de la base reguladora por meses cotizados (art. 210.1 y DT 9.ª), sin demora.
function pctBase(t, c) {
  var q = Math.floor(t / 12) === P.refAnio ? P.pc26 : P.pc27, x = c - P.carencia;
  return Math.min(P.topePct, P.basePct + q[1] * Math.min(x, q[0]) + q[2] * Math.max(0, x - q[0]));
}
// Suma de las n mejores bases de una ventana de N meses en la que los P.rec más recientes valen a y el resto b.
function mejores(n, N, a, b) {
  var hi = Math.max(a, b), lo = Math.min(a, b), nh = a >= b ? P.rec : N - P.rec, k = Math.min(n, nh);
  return k * hi + (n - k) * lo;
}
// Base reguladora (DT 40.ª y DT 4.ª.7): la más favorable. null si la ventana tendría meses sin cotizar.
function baseReguladora(t, c, a, b) {
  var y = Math.floor(t / 12), q = P.dt40[String(y)] || P.dt40f, nuevo, viejo;
  if (c < q[1] + 1) return null;
  nuevo = mejores(q[0], q[1], a, b) / q[2];
  viejo = (P.rec * a + (P.old[0] - P.rec) * b) / P.old[1];
  return { br: Math.max(nuevo, viejo), nuevo: nuevo, viejo: viejo };
}
// Cota S1: meses desde el primer mes de un año anterior (desde 2024) en que ya se cumplía la edad exigida de ese año con la cotización de entonces (art. 210.2.a: «fecha en que cumplió dicha edad»).
function demoraAlt(t, B, cot0) {
  var y, m, c, best = 0;
  for (y = P.altDesde; y < Math.min(Math.floor(t / 12), P.refAnio + 1); y++) {
    for (m = y * 12; m < y * 12 + 12 && m <= t; m++) {
      c = cotEn(m, cot0);
      if (m - B >= edadExigida(m, c) && c >= P.carencia) { best = Math.max(best, t - m); break; }
    }
  }
  return best;
}
function pensionEn(t, B, cot0, a, b) {
  var c = cotEn(t, cot0), R = edadExigida(t, c), d = t - B - R;
  var o = { t: t, cot: c, req: R, demora: d, pct: pctBase(t, c) }, r = baseReguladora(t, c, a, b);
  if (r) { o.br = r.br; o.brNew = r.nuevo; o.brOld = r.viejo; o.pension = Math.min(r.br * o.pct / 100, Math.floor(t / 12) === P.refAnio ? P.maxMes : P.maxMes * (1 + P.reval / 100)); }
  o.demoraAlt = demoraAlt(t, B, cot0);
  return o;
}
// Primer mes posible entre lo y hi: edad exigida cumplida y 15 años cotizados. estado 1 = no llegas a la edad, 2 = edad sí pero sin 15 años.
function primero(B, cot0, lo, hi) {
  var t, c, edadOk = false;
  for (t = lo; t <= hi; t++) {
    c = cotEn(t, cot0);
    if (t - B >= edadExigida(t, c)) { edadOk = true; if (c >= P.carencia) return { t: t, estado: 0 }; }
  }
  return { t: null, estado: edadOk ? 2 : 1 };
}
function calcular(d) {
  var na = Math.round(+d.nac_a), nm = Math.round(+d.nac_m), ca = Math.round(+d.cot_a), cm = Math.round(+d.cot_m), a = +d.b_rec, b = +d.b_ant;
  REF = (d.ref !== undefined && isFinite(+d.ref)) ? Math.round(+d.ref) : P.refAnio * 12 + P.refMes - 1;
  if (REF >= (P.refAnio + 1) * 12) return { bloqueado: 2 };
  if (!(na >= P.nacMin && na <= P.nacMax && nm >= 1 && nm <= 12 && ca >= 0 && ca <= P.cotMax && cm >= 0 && cm <= 11 && a > 0 && a <= P.bmax && b > 0 && b <= P.bmax)) return { bloqueado: 1 };
  var B = na * 12 + nm - 1, cot0 = ca * 12 + cm, out = { bloqueado: 0 }, Y, ys = [P.refAnio, P.refAnio + 1], i, lo, hi, f, p, k, tf;
  for (i = 0; i < 2; i++) {
    Y = ys[i]; lo = Math.max(REF, Y * 12); hi = Y * 12 + 11;
    f = primero(B, cot0, lo, hi); k = "a" + (Y % 100) + "_"; out[k + "estado"] = f.estado;
    if (f.t === null) continue;
    p = pensionEn(f.t, B, cot0, a, b);
    out[k + "t"] = p.t; out[k + "req"] = p.req; out[k + "cot"] = p.cot; out[k + "pct"] = p.pct; out[k + "demora"] = p.demora; out[k + "demoraAlt"] = p.demoraAlt;
    if (p.pension === undefined) out[k + "estado"] = 3;
    else { out[k + "br"] = p.br; out[k + "brNew"] = p.brNew; out[k + "brOld"] = p.brOld; out[k + "pension"] = p.pension; }
  }
  tf = primero(B, cot0, REF, P.hasta * 12 + 11);
  out.pf_t = tf.t === null ? -1 : tf.t;
  if (tf.t !== null) {
    p = pensionEn(tf.t, B, cot0, a, b);
    out.pf_req = p.req; out.pf_cot = p.cot; out.pf_pct = p.pct;
    if (p.pension !== undefined) out.pf_pension = p.pension;
  }
  out.demoraPosible = Math.max(out.a26_demora || 0, out.a26_demoraAlt || 0, out.a27_demora || 0, out.a27_demoraAlt || 0) >= P.demAnio ? 1 : 0;
  if (out.a26_pension !== undefined && out.a27_pension !== undefined) {
    out.a26_pension_ene27 = out.a26_pension * (1 + P.reval / 100);
    out.dif = out.a27_pension - out.a26_pension_ene27;
    if (out.dif > 1e-9) out.equilibrio = out.a26_pension * (out.a27_t - out.a26_t) / out.dif;
  }
  return out;
}
function eur(x) { return EM.eur(x); }
var MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
function fechaTxt(t) { return MESES[t % 12] + " de " + Math.floor(t / 12); }
function edadTxt(m) {
  var a = Math.floor(m / 12), r = m - 12 * a;
  return a + " años" + (r ? " y " + r + (r === 1 ? " mes" : " meses") : "");
}
function mesesTxt(m) {
  m = Math.round(m); var a = Math.floor(m / 12), r = m - 12 * a, s = [];
  if (a) s.push(a + (a === 1 ? " año" : " años"));
  if (r || !a) s.push(r + (r === 1 ? " mes" : " meses"));
  return s.join(" y ");
}
var IDS = ["nac_a", "nac_m", "cot_a", "cot_m", "b_rec", "b_ant"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); });
  return d;
}
function aviso(msg) { EM.renderResult({ winner: "invalido", tone: "warn", verdict: msg, note: "<p>Esta herramienta calcula con el calendario de la Ley General de la Seguridad Social para el Régimen General. Para tu caso exacto usa el simulador de la Seguridad Social.</p>" }); }
function celda(r, k, f) { return r[k + "estado"] === 0 || r[k + "estado"] === 3 ? f(r) : "—"; }
function pintar() {
  var d = leer(), r, ok26, ok27, v, winner, tone = "ok", big, bigL, bars, rows, note = "", hoy = new Date(), ref = Math.max(P.refAnio * 12 + P.refMes - 1, hoy.getFullYear() * 12 + hoy.getMonth());
  d.ref = ref; r = calcular(d);
  if (r.bloqueado === 2) return aviso("Esta comparación caducó: el calendario de 2026 ya ha pasado y la pensión de 2027 se calcula con los parámetros de ese año, que aún no están publicados. Para 2027 usa el simulador de la Seguridad Social.");
  if (r.bloqueado) return aviso("Revisa los datos: el año de nacimiento va de " + P.nacMin + " a " + P.nacMax + ", los meses de cotización de 0 a 11, y las dos bases deben ser mayores que 0 y no superar la base máxima de cotización de 2026 (" + eur(P.bmax) + " al mes).");
  ok26 = r.a26_estado === 0 || r.a26_estado === 3; ok27 = r.a27_estado === 0 || r.a27_estado === 3;
  if (r.pf_t < 0) return aviso("Con estos datos no llegas a 15 años cotizados a tu edad exigida antes de " + P.hasta + ": no se genera pensión de jubilación contributiva y esta herramienta no la calcula.");
  var f26 = ok26 ? fechaTxt(r.a26_t) : null, f27 = ok27 ? fechaTxt(r.a27_t) : null, ff = fechaTxt(r.pf_t), pe = function (x) { return eur(x); };
  var e26 = edadTxt(P.ed26[1]) + ", o " + edadTxt(P.ordM) + " con " + edadTxt(P.ed26[0]) + " cotizados", e27 = edadTxt(P.ed27[1]) + ", o " + edadTxt(P.ordM) + " con " + edadTxt(P.ed27[0]) + " cotizados";
  if (ok26 && ok27) {
    v = "Puedes jubilarte con pensión ordinaria desde " + f26 + " (con " + edadTxt(r.a26_req) + ") o desde " + f27 + " (con " + edadTxt(r.a27_req) + ").";
    if (r.a26_pension !== undefined && r.a27_pension !== undefined) {
      if (r.demoraPosible) {
        winner = "fechas"; tone = "info";
        v += " Las pensiones de la tabla (" + pe(r.a26_pension) + " en 2026 y " + pe(r.a27_pension) + " en 2027 al mes, 14 pagas) no incluyen el complemento por demora que puede corresponderte, así que con estos datos no se compara cuál conviene.";
      } else if (r.dif > 0) {
        winner = "depende"; tone = "info";
        v += " La herramienta estima que, desde enero de 2027, la pensión de 2027 (" + pe(r.a27_pension) + " al mes, 14 pagas) supera a la de 2026 ya revalorizada un " + EM.num(P.reval, 1) + " % por hipótesis (" + pe(r.a26_pension_ene27) + "), pero la de 2026 se cobra " + mesesTxt(r.a27_t - r.a26_t) + " antes: la de 2027 acumula más a partir de " + mesesTxt(r.equilibrio) + " después de " + f27 + ", sin contar el sueldo.";
        big = r.equilibrio; bigL = "meses después de " + f27 + " a partir de los cuales esperar acumula más pensión";
      } else {
        winner = "2026";
        v += " La herramienta estima que esperar a 2027 no sube la pensión: " + pe(r.a26_pension) + " al mes en 2026, que en enero de 2027 pasan a " + pe(r.a26_pension_ene27) + " con la revalorización supuesta del " + EM.num(P.reval, 1) + " %, frente a " + pe(r.a27_pension) + " en 2027 (14 pagas); además retrasa el cobro " + mesesTxt(r.a27_t - r.a26_t) + ".";
        big = r.a26_pension; bigL = "pensión mensual (14 pagas) jubilándote en " + f26;
      }
      if (!r.demoraPosible) bars = [{ label: "En 2026 (" + f26 + ")", value: r.a26_pension, color: "a" }, { label: "En 2027 (" + f27 + ")", value: r.a27_pension, color: "b" }];
    } else { winner = "fechas"; tone = "info"; v += " No se calcula la pensión con estos datos (ver más abajo)."; }
  } else if (ok27) {
    winner = "solo2027"; tone = "info";
    v = "En 2026 no llegas a la edad exigida (" + e26 + "): tu primer mes posible es " + f27 + ", con " + edadTxt(r.a27_req) + ".";
    if (r.a27_pension !== undefined) { v += " Pensión estimada: " + pe(r.a27_pension) + " al mes en 14 pagas."; big = r.a27_pension; bigL = "pensión mensual (14 pagas) jubilándote en " + f27; }
  } else if (ok26) {
    winner = "fechas"; tone = "info";
    v = "Puedes jubilarte con pensión ordinaria desde " + f26 + " (con " + edadTxt(r.a26_req) + "); en 2027 no hay un mes posible con estos datos.";
  } else {
    winner = "mas_tarde"; tone = "info";
    v = (r.a26_estado === 2 || r.a27_estado === 2 ? "Llegas a la edad exigida pero sin 15 años cotizados. " : "Ni en 2026 ni en 2027 llegas a la edad exigida. ") + "Tu primer mes posible con pensión ordinaria es " + ff + " (con " + edadTxt(r.pf_req) + ", con las reglas de ese año).";
    if (r.pf_pension !== undefined) { v += " Pensión estimada: " + pe(r.pf_pension) + " al mes en 14 pagas, con las bases que has puesto."; big = r.pf_pension; bigL = "pensión mensual (14 pagas) en " + ff; }
  }
  if (r.demoraPosible && winner !== "fechas") v += " Las pensiones no incluyen el complemento por demora que puede corresponderte.";
  rows = [
    ["Primer mes posible", ok26 ? f26 : "no hay", ok27 ? f27 : "no hay"],
    ["Edad exigida ese año (DT 7.ª)", celda(r, "a26_", function (x) { return edadTxt(x.a26_req); }), celda(r, "a27_", function (x) { return edadTxt(x.a27_req); })],
    ["Cotizado ese mes (cotizando hasta entonces)", celda(r, "a26_", function (x) { return edadTxt(x.a26_cot); }), celda(r, "a27_", function (x) { return edadTxt(x.a27_cot); })],
    ["% de la base reguladora (arts. 210.1 y DT 9.ª)", celda(r, "a26_", function (x) { return EM.num(x.a26_pct, 2) + " %"; }), celda(r, "a27_", function (x) { return EM.num(x.a27_pct, 2) + " %"; })],
    ["Meses por encima de la edad exigida", celda(r, "a26_", function (x) { return mesesTxt(Math.max(0, x.a26_demora)); }), celda(r, "a27_", function (x) { return mesesTxt(Math.max(0, x.a27_demora)); })],
    ["Base reguladora (€/mes, 14 pagas)", r.a26_br !== undefined ? eur(r.a26_br) : "—", r.a27_br !== undefined ? eur(r.a27_br) : "—"],
    ["Regla de la base reguladora", r.a26_br !== undefined ? (r.a26_brNew >= r.a26_brOld ? "DT 40.ª (302 de 304 meses)" : "Art. 209.1 de 2023 (300 meses)") : "—", r.a27_br !== undefined ? (r.a27_brNew >= r.a27_brOld ? "DT 40.ª (304 de 308 meses)" : "Art. 209.1 de 2023 (300 meses)") : "—"],
    ["Pensión desde enero de 2027, con revalorización supuesta del " + EM.num(P.reval, 1) + " %", r.a26_pension_ene27 !== undefined ? pe(r.a26_pension_ene27) : "—", r.a27_pension !== undefined ? pe(r.a27_pension) : "—"],
    { label: "Pensión mensual estimada al empezar (14 pagas, bruta)", values: [r.a26_pension !== undefined ? pe(r.a26_pension) : "—", r.a27_pension !== undefined ? pe(r.a27_pension) : "—"], strong: true }
  ];
  if ((ok26 && r.a26_estado === 3) || (ok27 && r.a27_estado === 3)) note += "<p><strong>Sin importe de pensión:</strong> con tus años cotizados la ventana de cálculo de la base reguladora incluiría meses sin cotizar (lagunas), que se integran con reglas propias (art. 209.1.b y DT 41.ª) y esta herramienta no modela. Sí se calculan la edad, la fecha y el porcentaje.</p>";
  if (r.a26_br !== undefined && r.a27_br !== undefined && r.a26_brOld > r.a26_brNew && r.a27_brOld > r.a27_brNew) note += "<p><strong>La base reguladora no cambia con el salto a 2027:</strong> con tus bases (más altas en los últimos años) se aplica la regla de 300 meses entre 350 de la disposición transitoria 4.ª.7, que es más favorable que la de 302 o 304 meses de la disposición transitoria 40.ª.</p>";
  if (r.demoraPosible) note += "<p><strong>Complemento por demora no calculado:</strong> llevas un año o más por encima de la edad exigida, así que puede corresponderte (según la edad que se tome como cumplida, art. 210.2.a: la de la fecha en que la cumpliste) un complemento (4 % por año completo, art. 210.2.a) que sube la pensión de los dos años y puede cambiar cuál conviene; las pensiones de la tabla no lo incluyen. Mira la <a href=\"/jubilacion-anticipada-o-demorada/\">calculadora de jubilación anticipada o demorada</a>.</p>";
  note += "<p><strong>Cómo se ha calculado:</strong> edad exigida y porcentaje según el año en que se causa la pensión (tablas de las disposiciones transitorias 7.ª y 9.ª); se supone que sigues cotizando mes a mes hasta jubilarte, con tus cotizados contados a 1 de " + MESES[ref % 12] + " de " + Math.floor(ref / 12) + ", y que ya reúnes los 2 años dentro de los últimos 15 (art. 205.1.b). Las dos bases son tus bases mensuales en euros de hoy: la reciente (últimos 5 años) y la anterior; la oficial actualiza con el IPC solo hasta el mes 25 anterior y deja los 24 últimos meses sin actualizar (art. 209.1.c y d), así que la base oficial suele salir algo menor que la de este cálculo, del orden de lo que han subido los precios en los dos últimos años (entre un 3 % y un 5 %): si tus bases son de hace años, súbelas con el IPC antes de escribirlas. La pensión causada en 2026 se revaloriza en enero de 2027 (art. 58.2): se supone el " + EM.num(P.reval, 1) + " % de 2026, y la máxima de 2027 se supone la de 2026 con esa misma subida. En 2027 la base reguladora gana además algo por la actualización de las bases por tres meses más de IPC, menos de lo que revaloriza la pensión.</p>";
  note += "<p><strong>Otra lectura de la DT 7.ª:</strong> la herramienta aplica la edad del año en que se causa la pensión; quien ya cumplió en 2026 la edad exigida (66 años y 10 meses, o 65 con 38 años y 3 meses) podría defender que la conserva en 2027, y su mes de 2027 saldría 1 a 3 meses antes. La ley no lo aclara.</p>"; note += "<p><strong>No incluye:</strong> lagunas de cotización ni su integración (art. 209.1.b y DT 41.ª), jubilación anticipada (mira la <a href=\"/jubilacion-anticipada-o-demorada/\">calculadora de jubilación anticipada o demorada</a>), el tope máximo de 2027 (no publicado: se usa el de 2026, " + eur(P.maxMes) + " al mes, subido un " + EM.num(P.reval, 1) + " % desde 2027, y la pensión se limita a él), el complemento a mínimos, el complemento por demora que excede la pensión máxima, la revalorización anual, el IRPF, otros regímenes (autónomos, funcionarios) ni jubilaciones especiales. Para tu caso exacto, usa el simulador de la Seguridad Social.</p>";
  EM.renderResult({ winner: winner, verdict: v, tone: tone, bigNumber: big, bigLabel: bigL, format: winner === "depende" ? function (x) { return mesesTxt(x); } : EM.eur, bars: bars, barsLabel: "Pensión mensual estimada (14 pagas, bruta)", cols: ["Jubilarte en 2026", "Jubilarte en 2027"], rows: rows, note: note });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
