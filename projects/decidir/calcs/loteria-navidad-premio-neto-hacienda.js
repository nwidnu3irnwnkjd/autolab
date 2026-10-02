// Lotería de Navidad: neto de un premio tras el gravamen especial. Parámetros: data/params.json -> loteria_navidad_2026 (fuentes y fechas allí).
// DA 33.ª LIRPF: exentos los premios de hasta 40.000 € por décimo; el exceso tributa al 20 % con retención del 20 % en el cobro; en titularidad compartida la exención se prorratea.
var P = {"exento": 40000, "tipo": 20, "ret": 20};
function calcular(d) {
  var r = { bloqueo: 0, esc: 0 };
  var x = d.premio, nd = Math.round(d.decimos), np = Math.round(d.personas);
  if (!(x > 0)) { r.bloqueo = 1; return r; }
  if (nd < 1) { r.bloqueo = 2; return r; }
  if (np < 1) { r.bloqueo = 3; return r; }
  var tipo = P.tipo / 100, ret = P.ret / 100;
  var exDec = Math.min(x, P.exento), baseDec = Math.max(0, x - P.exento), retDec = baseDec * ret;
  r.netoDecimo = x - retDec; r.exentoDecimo = exDec; r.sujetoDecimo = baseDec; r.retDecimo = retDec;
  r.bruto = x * nd; r.exento = exDec * nd; r.sujeto = baseDec * nd; r.retencion = retDec * nd;
  r.cuota = baseDec * tipo * nd;
  r.netoTotal = r.bruto - r.retencion;
  r.brutoPersona = r.bruto / np; r.exentoPersona = r.exento / np; r.sujetoPersona = r.sujeto / np; r.retPersona = r.retencion / np;
  r.netoPersona = r.netoTotal / np;
  r.pctNeto = r.netoTotal / r.bruto * 100;
  r.esc = x <= P.exento ? 1 : (np === 1 ? 2 : (d.cobro === "uno" ? 4 : 3));
  return r;
}
function eur(x) { return EM.eur(x); }
var IDS = ["premio", "decimos", "personas"];
function leer() {
  var d = {}; IDS.forEach(function (k) { d[k] = parseFloat(document.getElementById(k).value); if (isNaN(d[k])) d[k] = 0; });
  d.cobro = document.getElementById("cobro").value;
  return d;
}
function aviso(txt) { EM.renderResult({ winner: "revisar", tone: "warn", verdict: txt }); }
var NO_MODELA = "<p><strong>No incluye:</strong> el Impuesto sobre Sucesiones y Donaciones si repartes el premio con quien no figura como cotitular del décimo (cada comunidad autónoma lo regula distinto); los premios de loterías públicas o sin ánimo de lucro de otros Estados de la UE o del EEE (también tributan por este gravamen, pero sin retención española: se autoliquidan con el modelo 136); los premios obtenidos por no residentes (tributan por el Impuesto sobre la Renta de no Residentes); los regímenes forales de País Vasco y Navarra, con normas propias; los premios de empresa o de organizadores privados o de fuera de la UE y el EEE (tributan en el IRPF general); el Impuesto sobre el Patrimonio si guardas el dinero; los rendimientos que genere el premio después de cobrarlo; los premios en especie; y los repartos por partes distintas de las iguales.</p>";
function pintar() {
  var d = leer();
  if (d.premio < 0 || d.decimos < 0 || d.personas < 0) { aviso("Revisa los datos: el premio, los décimos y las personas no pueden ser negativos."); return; }
  var r = calcular(d);
  if (r.bloqueo === 1) { aviso("Indica el premio íntegro de un décimo (mayor que 0 €). Es el importe bruto que figura en la lista oficial, antes de cualquier retención."); return; }
  if (r.bloqueo === 2) { aviso("Indica al menos 1 décimo premiado."); return; }
  if (r.bloqueo === 3) { aviso("Indica al menos 1 persona (tú cuentas)."); return; }
  var nd = Math.round(d.decimos), np = Math.round(d.personas), verdict;
  var ref = "Con tus datos (" + EM.num(nd, 0) + (nd === 1 ? " décimo" : " décimos") + " de " + eur(d.premio) + (np > 1 ? ", entre " + EM.num(np, 0) + " personas" : "") + "), ";
  if (r.esc === 1) verdict = ref + "cobras " + eur(r.netoTotal) + " sin retención: el premio de cada décimo no pasa de " + eur(P.exento) + " y está exento del gravamen especial.";
  else if (r.esc === 2) verdict = ref + "te quedan " + eur(r.netoTotal) + " netos: la retención es de " + eur(r.retencion) + " (el " + EM.num(P.ret, 0) + " % de los " + eur(r.sujeto) + " que superan los " + eur(P.exento) + " exentos por décimo). Esa retención es el impuesto definitivo y no vuelve a tributar en tu renta.";
  else if (r.esc === 3) verdict = ref + "la retención total es de " + eur(r.retencion) + " y el neto total, " + eur(r.netoTotal) + ": " + eur(r.netoPersona) + " por persona. Compartir no multiplica la exención: los " + eur(P.exento) + " exentos se reparten entre los cotitulares y el impuesto total es el mismo que si cobrara una sola persona.";
  else verdict = ref + "si una sola persona cobra y luego reparte, según el criterio de la Agencia Tributaria, si no se acredita la cotitularidad al cobrar el gravamen recae sobre ella: retención de " + eur(r.retencion) + " y neto de " + eur(r.netoTotal) + ", es decir, " + eur(r.netoPersona) + " por persona si se reparte a partes iguales. El impuesto total es el mismo que con cotitulares identificados, pero lo que entregues a los demás puede ser una donación sujeta al Impuesto sobre Sucesiones y Donaciones de tu comunidad.";
  var note = "<p><strong>Cómo sale:</strong> el gravamen especial se aplica a cada décimo por separado. Los primeros " + eur(P.exento) + " de cada premio están exentos; lo que pasa de ahí tributa al " + EM.num(P.tipo, 0) + " %, y Loterías y Apuestas del Estado ya retiene ese " + EM.num(P.ret, 0) + " % al pagarte. Por cada décimo de " + eur(d.premio) + ": exento " + eur(r.exentoDecimo) + ", sujeto " + eur(r.sujetoDecimo) + ", retención " + eur(r.retDecimo) + " y neto " + eur(r.netoDecimo) + ".</p>";
  note += "<p>El premio no se declara en la renta ni suma a tu base imponible del IRPF (disposición adicional 33.ª, apartado 8), y la retención no se devuelve ni se descuenta de tu cuota.</p>";
  if (np > 1) note += "<p><strong>Cada persona:</strong> premio íntegro " + eur(r.brutoPersona) + ", exento " + eur(r.exentoPersona) + ", sujeto " + eur(r.sujetoPersona) + ", retención " + eur(r.retPersona) + " y neto " + eur(r.netoPersona) + " (a partes iguales). Para que la exención se prorratee, los cotitulares deben figurar como tales al cobrar; si cobra uno solo y reparte, el reparto puede ser una donación sujeta al Impuesto sobre Sucesiones y Donaciones de tu comunidad.</p>";
  note += NO_MODELA;
  var rows = [
    ["Premio íntegro", eur(r.bruto), np > 1 ? eur(r.brutoPersona) : ""],
    ["Exento (hasta " + eur(P.exento) + " por décimo)", eur(r.exento), np > 1 ? eur(r.exentoPersona) : ""],
    ["Sujeto al gravamen especial", eur(r.sujeto), np > 1 ? eur(r.sujetoPersona) : ""],
    ["Retención del " + EM.num(P.ret, 0) + " %", eur(r.retencion), np > 1 ? eur(r.retPersona) : ""],
    ["Neto que cobras", eur(r.netoTotal), np > 1 ? eur(r.netoPersona) : ""]
  ];
  EM.renderResult({
    winner: "esc" + r.esc, verdict: verdict, tone: r.esc === 1 ? "ok" : "info",
    bigNumber: r.netoTotal, bigLabel: "netos que te quedan tras la retención", format: eur,
    barsLabel: "Dónde va el premio",
    bars: [{ label: "Para ti", value: r.netoTotal, color: "a" }, { label: "Retención (Hacienda)", value: r.retencion, color: "b" }],
    cols: np > 1 ? ["Concepto", "Total", "Por persona"] : ["Concepto", "Total"],
    rows: np > 1 ? rows : rows.map(function (x) { return [x[0], x[1]]; }),
    note: note
  });
}
document.getElementById("go").addEventListener("click", pintar);
document.getElementById("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); pintar(); } });
EM.live(document.getElementById("f"), pintar);
