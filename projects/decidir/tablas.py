"""Tablas 2026 (dueño: Estratega SEO/GEO, c36, T24 «páginas de dato propio»). Solo stdlib.
Páginas de referencia citables por buscadores e IAs, generadas SOLO desde data/params.json con cifras ya
verificadas (bloques con `confianza` A o A− y su fuente/URL oficial). Cada página: tabla oficial + un cálculo
propio reproducible (cuota íntegra del IRPF por comunidad, cuota anual de autónomos, impuestos de compra de
vivienda por comunidad), fecha de revisión, fuente enlazada, enlaces a las calculadoras, JSON-LD Dataset +
Table + Article + BreadcrumbList y CSV descargable (/tablas-2026/<slug>/datos.csv; todo en /tablas-2026/datos.json).
Revertir: quitar las llamadas a tablas.* en build.py (y la clave `datos` de hubs.HUBS)."""
import csv, io, json, os, html
from barometro import num, pct, eur, fecha_es

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = "/tablas-2026/"
LIC = "https://creativecommons.org/licenses/by/4.0/deed.es"
BOE_IRPF = "https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764"
e = html.escape


def _ok(b):
    return isinstance(b, dict) and str(b.get("confianza", "")).startswith(("A", "B"))

def _f(x):  # 2 decimales solo si hacen falta
    return num(x, 0 if float(x).is_integer() else 2)

def _ef(x): return _f(x) + " €"

def escala(v, tr):
    """Tarifa progresiva [[desde, %], ...]: cada tramo sobre su parte (art. 63.1 LIRPF)."""
    s = 0.0
    for i, (d, t) in enumerate(tr):
        hi = tr[i + 1][0] if i + 1 < len(tr) else float("inf")
        if v > d: s += (min(v, hi) - d) * t / 100
    return s

def marginal(v, tr):
    t = tr[0][1]
    for d, p in tr:
        if v > d: t = p
    return t

def impuesto(v, t):  # mismo algoritmo que calcs/cuanto-ahorrar-para-comprar-casa.js
    if t["tipo"] == "plano": return v * t["pct"] / 100
    if t["tipo"] == "escala": return escala(v, t["tramos"])
    return v * marginal(v, t["tramos"]) / 100

def tipo_txt(t):
    if t["tipo"] == "plano": return _pc(t["pct"])
    sep = " · "
    if t["tipo"] == "escala":
        return "progresivo: " + sep.join(f"{_pc(p)} desde {_ef(d)}" if d else f"{_pc(p)}" for d, p in t["tramos"])
    return "según valor (todo el valor al tipo del tramo): " + sep.join(f"{_pc(p)} si supera {_ef(d)}" if d else f"{_pc(p)}" for d, p in t["tramos"])

def _pc(p): return pct(p, 2 if round(p * 100) % 10 else (1 if p % 1 else 0))

def _src(url, label): return f'<a href="{e(url)}" rel="noopener">{e(label)}</a>'

def _csv(rows):
    b = io.StringIO(); w = csv.writer(b, lineterminator="\n")
    w.writerow(["tabla", "clave", "campo", "valor", "unidad", "fuente", "url_fuente"])
    for r in rows: w.writerow(r)
    return b.getvalue()


# ---------- 1. IRPF ----------
BASES_CUOTA = [20000, 30000, 50000]
BASES_MARG = [25000, 45000, 75000, 160000]

def irpf(P):
    I = P["irpf_2026"]; est = I["escala_estatal_general"]; ah = I["escala_ahorro_mitad"]; me = I["minimo_estatal"]
    assert _ok(est) and _ok(ah) and _ok(me)
    ccaa = [(k, c) for k, c in I["ccaa"].items() if _ok(c)]
    rows, csvr = [], []
    m_est = me["contribuyente"]
    for k, c in ccaa:
        tr = c["escala_general"]; m_aut = (c.get("minimo") or {}).get("contribuyente", m_est)
        cuotas = {}
        for B in BASES_CUOTA:
            ce = escala(B, est["tramos"]) - escala(m_est, est["tramos"])
            ca = escala(B, tr) - escala(m_aut, tr)
            cuotas[B] = round(ce + ca, 2)
        margs = {B: round(marginal(B, est["tramos"]) + marginal(B, tr), 2) for B in BASES_MARG}
        top = round(est["tramos"][-1][1] + tr[-1][1], 2)
        rows.append(dict(k=k, n=c["nombre"], tr=tr, m_aut=m_aut, propio=bool(c.get("minimo")), cuotas=cuotas, margs=margs, top=top,
                         fuente=c["fuente"], url=c["url"], orient=bool(c.get("orientativo"))))
        for d, p in tr: csvr.append(["irpf_escala_autonomica", k, f"tipo_desde_{_raw(d)}", p, "%", c["fuente"], c["url"]])
        csvr.append(["irpf_minimo_personal_autonomico", k, "contribuyente", m_aut, "EUR", c["fuente"] if c.get("minimo") else me["fuente"], c["url"]])
        for B, v in cuotas.items(): csvr.append(["irpf_cuota_integra_calculo_propio", k, f"base_{B}", v, "EUR", "Cálculo Entre Muchos (CC BY 4.0)", ""])
        for B, v in margs.items(): csvr.append(["irpf_tipo_marginal_combinado", k, f"base_{B}", v, "%", "Cálculo Entre Muchos (CC BY 4.0)", ""])
        csvr.append(["irpf_tipo_maximo_combinado", k, "maximo", top, "%", "Cálculo Entre Muchos (CC BY 4.0)", ""])
    for d, p in est["tramos"]: csvr.append(["irpf_escala_estatal", "estado", f"tipo_desde_{_raw(d)}", p, "%", est["fuente"], est["url"]])
    for d, p in ah["tramos"]: csvr.append(["irpf_escala_ahorro_total", "estado+ccaa", f"tipo_desde_{_raw(d)}", round(p * 2, 2), "%", ah["fuente"], ah["url"]])
    rows.sort(key=lambda r: r["cuotas"][30000])
    return dict(est=est, ah=ah, me=me, rows=rows, excl=I.get("excluidas", []), fecha=I["consultado"], csv=csvr)

def _raw(d): return int(d) if float(d).is_integer() else d

def _escala_table(tr, nxt_label="Hasta"):
    out = []
    for i, (d, p) in enumerate(tr):
        hi = tr[i + 1][0] if i + 1 < len(tr) else None
        rng = f"De {_ef(d)} a {_ef(hi)}" if hi is not None and d else (f"Hasta {_ef(hi)}" if hi is not None else f"Más de {_ef(d)}")
        out.append(f"<tr><th scope=\"row\">{rng}</th><td>{_pc(p)}</td></tr>")
    return "".join(out)

def irpf_body(D):
    rows = D["rows"]; lo, hi = rows[0], rows[-1]
    estado = D["est"]
    ah = _escala_table([[d, round(p * 2, 2)] for d, p in D["ah"]["tramos"]])
    star = lambda r: " *" if r["orient"] else ""
    cuota_rows = "".join(f'<tr><th scope="row">{e(r["n"])}{star(r)}</th>' + "".join(f"<td>{eur(r['cuotas'][B])}</td>" for B in BASES_CUOTA) + "</tr>" for r in rows)
    marg_rows = "".join(f'<tr><th scope="row">{e(r["n"])}{star(r)}</th>' + "".join(f"<td>{_pc(r['margs'][B])}</td>" for B in BASES_MARG) + f"<td>{_pc(r['top'])}</td></tr>" for r in sorted(rows, key=lambda r: r["n"]))
    det = "".join(f'<details><summary><strong>{e(r["n"])}</strong>{star(r)}: {len(r["tr"])} tramos, del {_pc(r["tr"][0][1])} al {_pc(r["tr"][-1][1])}; mínimo personal {_ef(r["m_aut"])}{" (propio)" if r["propio"] else " (estatal)"}</summary>'
                  f'<div class="em-tw"><table><thead><tr><th scope="col">Base liquidable general</th><th scope="col">Tipo autonómico</th></tr></thead><tbody>{_escala_table(r["tr"])}</tbody></table></div>'
                  f'<p class="note">Fuente: {_src(r["url"], r["fuente"])}, {e(fecha_es(D["fecha"]))}.</p></details>' for r in sorted(rows, key=lambda r: r["n"]))
    mid = rows[len(rows) // 2]
    return f"""<div class="box"><p><strong>Respuesta corta:</strong> en 2026 la escala estatal del IRPF va del {_pc(estado["tramos"][0][1])} al {_pc(estado["tramos"][-1][1])} y cada comunidad suma la suya. Con 30.000 € de base liquidable general (contribuyente sin hijos, menor de 65 años), la cuota íntegra total va de <strong>{eur(lo["cuotas"][30000])} en {e(lo["n"])}</strong> a <strong>{eur(hi["cuotas"][30000])} en {e(hi["n"])}</strong>: {eur(hi["cuotas"][30000] - lo["cuotas"][30000])} de diferencia al año por vivir en una u otra comunidad.</p></div>

<h2 id="estatal">Escala estatal del IRPF 2026 (base general)</h2>
<p>Es la mitad estatal del impuesto, igual en todas las comunidades de régimen común. Se aplica a la base liquidable general y, aparte, al mínimo personal y familiar (la diferencia es la cuota). Fuente: {_src(estado["url"], estado["fuente"])}, {e(estado["consulta"])}.</p>
<div class="em-tw"><table><thead><tr><th scope="col">Base liquidable general</th><th scope="col">Tipo estatal</th></tr></thead><tbody>{_escala_table(estado["tramos"])}</tbody></table></div>

<h2 id="cuota">Cuánto IRPF se paga en cada comunidad: cuota íntegra 2026 (cálculo propio)</h2>
<p>Cuota íntegra estatal más autonómica de un contribuyente menor de 65 años, sin descendientes ni discapacidad, aplicando cada escala a la base y restando la misma escala aplicada al mínimo personal ({_ef(D["me"]["contribuyente"])} estatal; el de la comunidad si tiene uno propio). Redondeada al euro y antes de deducciones (vivienda, autonómicas, DA 61.ª) y de retenciones. Ordenado de menor a mayor a 30.000 €; la comunidad del medio es {e(mid["n"])} ({eur(mid["cuotas"][30000])}). Fuentes: escalas de esta página ({_src(BOE_IRPF, "Ley 35/2006, arts. 56, 57, 63 y 74")}).</p>
<div class="em-tw"><table><thead><tr><th scope="col">Comunidad</th>{"".join(f'<th scope="col">Base {_ef(B)}</th>' for B in BASES_CUOTA)}</tr></thead><tbody>{cuota_rows}</tbody></table></div>

<h2 id="marginal">Tipo marginal combinado por comunidad (estatal + autonómico)</h2>
<p>Lo que se paga por cada euro más de base liquidable general a esa altura de la escala, sumando el tipo estatal y el autonómico; la última columna es el tipo máximo. Sirve para saber cuánto se queda Hacienda de una subida de sueldo o de un ingreso extra. Fuente: escalas de la {_src(BOE_IRPF, "Ley 35/2006, art. 63")} y de cada comunidad (enlaces abajo).</p>
<div class="em-tw"><table><thead><tr><th scope="col">Comunidad</th>{"".join(f'<th scope="col">A {_ef(B)}</th>' for B in BASES_MARG)}<th scope="col">Máximo</th></tr></thead><tbody>{marg_rows}</tbody></table></div>

<h2 id="autonomicas">Escalas autonómicas del IRPF 2026, una a una</h2>
<p>Tramos de la parte autonómica de cada comunidad de régimen común, leídos en el texto consolidado del BOE. No incluye {e(" ni ".join(D["excl"]))}, que tienen impuesto propio.</p>
{det}
<p class="note">* Confianza A−: la escala coincide con el texto consolidado y con el Manual de Renta 2025 de la AEAT, pero el BOE consolidado no está actualizado a 2026 o no hay norma de 2026 que lo confirme; tómala como orientativa y confírmala en el boletín de la comunidad.</p>

<h2 id="ahorro">Escala del ahorro 2026 (intereses, dividendos y ganancias)</h2>
<p>Tipo total (estatal + autonómico, la mitad cada uno, igual en todas las comunidades). Fuente: {_src(D["ah"]["url"], D["ah"]["fuente"])}, {e(D["ah"]["consulta"])}.</p>
<div class="em-tw"><table><thead><tr><th scope="col">Base liquidable del ahorro</th><th scope="col">Tipo total</th></tr></thead><tbody>{ah}</tbody></table></div>"""

def irpf_md(D):
    r = D["rows"]
    return ("Cuota íntegra IRPF 2026 (estatal + autonómica, contribuyente sin hijos < 65 años, antes de deducciones), base liquidable general 20.000 / 30.000 / 50.000 €:\n"
            + "\n".join(f"- {x['n']}: {eur(x['cuotas'][20000])} / {eur(x['cuotas'][30000])} / {eur(x['cuotas'][50000])} · tipo máximo {_pc(x['top'])}" for x in r))


# ---------- 2. Autónomos ----------
def autonomos(P):
    A = P["autonomo_2026"]; assert _ok(A)
    reta = A["reta"]; tipo = reta["tipo_total"]; rows = []; prev = None; csvr = []
    for i, (tabla, lim, bmin, bmax) in enumerate(reta["tramos"]):
        if prev is None: rng = f"Hasta {_ef(lim)}"
        elif lim is None: rng = f"Más de {_ef(prev)}"
        elif lim == 1166.7: rng = f"Más de {_ef(prev)} y menos de {_ef(lim)}"
        elif prev == 1166.7: rng = f"De {_ef(prev)} a {_ef(lim)}"
        else: rng = f"Más de {_ef(prev)} hasta {_ef(lim)}"
        cmin, cmax = round(bmin * tipo / 100, 2), round(bmax * tipo / 100, 2)
        n = sum(1 for t in reta["tramos"][:i + 1] if t[0] == tabla)
        rows.append(dict(t=f"{'Reducida' if tabla == 'reducida' else 'General'} {n}", rng=rng, bmin=bmin, bmax=bmax, cmin=cmin, cmax=cmax, anual=round(cmin * 12, 2)))
        k = f"{tabla}_{n}"
        for campo, v, u in [("limite_rendimiento_mes", lim, "EUR"), ("base_minima_mes", bmin, "EUR"), ("base_maxima_mes", bmax, "EUR"),
                            ("cuota_minima_mes_calculo", cmin, "EUR"), ("cuota_maxima_mes_calculo", cmax, "EUR"), ("cuota_minima_anual_calculo", round(cmin * 12, 2), "EUR")]:
            csvr.append(["autonomos_tramos_2026", k, campo, "" if v is None else v, u, A["fuente"].split(";")[0], A["url"]])
        prev = lim
    return dict(A=A, tipo=tipo, rows=rows, csv=csvr, fecha="2026-10-02")

def autonomos_body(D):
    A, rows = D["A"], D["rows"]
    tr = "".join(f'<tr><th scope="row">{r["t"]}</th><td>{r["rng"]}</td><td>{_ef(r["bmin"])}</td><td>{_ef(r["bmax"])}</td><td><strong>{_ef(r["cmin"])}</strong></td><td>{_ef(r["cmax"])}</td><td>{_ef(r["anual"])}</td></tr>' for r in rows)
    return f"""<div class="box"><p><strong>Respuesta corta:</strong> en 2026 la cuota mínima de autónomos va de <strong>{_ef(rows[0]["cmin"])} al mes</strong> (rendimientos netos de hasta {_ef(A["reta"]["tramos"][0][1])} al mes) a <strong>{_ef(rows[-1]["cmin"])}</strong> (más de {_ef(A["reta"]["tramos"][-2][1])}), es decir, de {_ef(rows[0]["anual"])} a {_ef(rows[-1]["anual"])} al año, con un tipo del {_pc(D["tipo"])} sobre la base que elijas dentro de tu tramo. No incluye la tarifa plana ni bonificaciones.</p></div>

<h2 id="tramos">Tabla de tramos, bases y cuotas de autónomos 2026</h2>
<p>Bases mínima y máxima por tramo de rendimientos netos mensuales, de la {_src(A["url"], "Orden PJC/297/2026, de cotización 2026")} ({e(A["consulta"])}). Las cuotas son cálculo propio: base × {_pc(D["tipo"])} ({e(A["reta"]["desglose"])}), redondeadas al céntimo.</p>
<div class="em-tw"><table><thead><tr><th scope="col">Tramo</th><th scope="col">Rendimiento neto al mes</th><th scope="col">Base mínima</th><th scope="col">Base máxima</th><th scope="col">Cuota mínima al mes</th><th scope="col">Cuota máxima al mes</th><th scope="col">Cuota mínima al año</th></tr></thead><tbody>{tr}</tbody></table></div>

<h2 id="rendimiento">Qué rendimiento neto cuenta para elegir tramo</h2>
<p>El rendimiento computable es el de tu actividad (ingresos menos gastos deducibles, más tu propia cuota si la deduces) menos un {_pc(A["reta"]["deduccion_gastos_genericos_pct"])} por gastos genéricos ({_src(A["url_lgss"], "LGSS, art. 308.1.c")}). Se calcula como media mensual del año: si a final de año tus rendimientos caen en otro tramo, la Seguridad Social regulariza la diferencia (te devuelve o te pide). Esa deducción del {_pc(A["reta"]["deduccion_gastos_genericos_pct"])} es solo para la cotización; en el IRPF se aplica la de gastos de difícil justificación ({_pc(A["irpf_autonomo"]["dificil_justificacion_pct"])} con máximo {_ef(A["irpf_autonomo"]["dificil_justificacion_max"])}, {_src(A["url_rirpf"], "RIRPF, art. 30.2.ª")}).</p>"""

def autonomos_md(D):
    return "Cuota de autónomos 2026 (base mínima × " + _pc(D["tipo"]) + "), por tramo de rendimiento neto mensual:\n" + "\n".join(
        f"- {r['t']} ({r['rng'].replace('&nbsp;', ' ')}): base mínima {_ef(r['bmin'])}, cuota mínima {_ef(r['cmin'])}/mes ({_ef(r['anual'])}/año)" for r in D["rows"])


# ---------- 3. ITP / AJD ----------
PRECIOS = [200000, 300000]

def vivienda(P):
    V = P["vivienda_2026"]; assert _ok(V)
    rows, csvr = [], []
    for k, c in V["ccaa"].items():
        r = dict(k=k, n=c["nombre"], itp=c["itp"], ajd=c["ajd"], norma=c["norma"], url=c["url"], red=c.get("red", ""), orient=bool(c.get("orient")))
        r["usada"] = {p: round(impuesto(p, c["itp"]), 2) for p in PRECIOS}
        r["nueva"] = {p: round(p * V["iva_vivienda_pct"] / 100 + impuesto(p, c["ajd"]), 2) for p in PRECIOS}
        rows.append(r)
        for p in PRECIOS:
            csvr.append(["vivienda_impuestos_compra_calculo", k, f"usada_itp_{p}", r["usada"][p], "EUR", "Cálculo Entre Muchos (CC BY 4.0) con " + c["norma"], c["url"]])
            csvr.append(["vivienda_impuestos_compra_calculo", k, f"nueva_iva_ajd_{p}", r["nueva"][p], "EUR", "Cálculo Entre Muchos (CC BY 4.0) con " + c["norma"], c["url"]])
        for nm in ("itp", "ajd"):
            t = c[nm]
            if t["tipo"] == "plano": csvr.append(["vivienda_tipos_generales", k, f"{nm}_pct", t["pct"], "%", c["norma"], c["url"]])
            else:
                for d, p in t["tramos"]: csvr.append(["vivienda_tipos_generales", k, f"{nm}_{t['tipo']}_desde_{_raw(d)}", p, "%", c["norma"], c["url"]])
    rows.sort(key=lambda r: r["usada"][200000])
    return dict(V=V, rows=rows, csv=csvr, fecha="2026-10-02")

def vivienda_body(D):
    V, rows = D["V"], D["rows"]; lo, hi = rows[0], rows[-1]
    star = lambda r: " *" if r["orient"] else ""
    t1 = "".join(f'<tr><th scope="row">{e(r["n"])}{star(r)}</th><td>{e(tipo_txt(r["itp"]))}</td><td>{e(tipo_txt(r["ajd"]))}</td><td>{_src(r["url"], r["norma"])}</td></tr>' for r in sorted(rows, key=lambda r: r["n"]))
    t2 = "".join(f'<tr><th scope="row">{e(r["n"])}{star(r)}</th>' + "".join(f"<td>{_ef(r['usada'][p])}</td>" for p in PRECIOS) + "".join(f"<td>{_ef(r['nueva'][p])}</td>" for p in PRECIOS) + "</tr>" for r in rows)
    red = "".join(f"<li><strong>{e(r['n'])}:</strong> {e(r['red'])}</li>" for r in sorted(rows, key=lambda r: r["n"]) if r["red"] and not r["red"].startswith("Esta comunidad tiene tipos reducidos"))
    gen = [r["n"] for r in sorted(rows, key=lambda r: r["n"]) if r["red"].startswith("Esta comunidad tiene tipos reducidos")]
    return f"""<div class="box"><p><strong>Respuesta corta:</strong> comprar una vivienda usada de 200.000 € paga de ITP desde <strong>{_ef(lo["usada"][200000])} en {e(lo["n"])}</strong> hasta <strong>{_ef(hi["usada"][200000])} en {e(hi["n"])}</strong> con el tipo general de 2026. Si es nueva, se paga IVA del {_pc(V["iva_vivienda_pct"])} más AJD, de {_ef(min(r["nueva"][200000] for r in rows))} a {_ef(max(r["nueva"][200000] for r in rows))}. Los tipos reducidos (vivienda habitual, jóvenes, familia numerosa) pueden bajarlo mucho: abajo, los de cada comunidad.</p></div>

<h2 id="tipos">Tipos generales de ITP y AJD por comunidad (2026)</h2>
<p>ITP: impuesto de transmisiones patrimoniales, en la compra de vivienda usada. AJD: actos jurídicos documentados, en la escritura de vivienda nueva (que además paga IVA, {_src(V["url"], "Ley 37/1992, art. 91")}). Tipos leídos en la norma autonómica consolidada del BOE, {e(V["consulta"])}.</p>
<div class="em-tw"><table><thead><tr><th scope="col">Comunidad</th><th scope="col">ITP (usada)</th><th scope="col">AJD (nueva)</th><th scope="col">Norma</th></tr></thead><tbody>{t1}</tbody></table></div>

<h2 id="coste">Impuestos de compra de una vivienda en cada comunidad (cálculo propio)</h2>
<p>Lo que se paga solo en impuestos al comprar, con el tipo general y sin reducciones: ITP en la usada; IVA del {_pc(V["iva_vivienda_pct"])} + AJD en la nueva. Sin notaría, registro ni gestoría. Ordenado de menor a mayor ITP a 200.000 €. Normas enlazadas en la tabla anterior.</p>
<div class="em-tw"><table><thead><tr><th scope="col">Comunidad</th>{"".join(f'<th scope="col">Usada {_ef(p)}</th>' for p in PRECIOS)}{"".join(f'<th scope="col">Nueva {_ef(p)}</th>' for p in PRECIOS)}</tr></thead><tbody>{t2}</tbody></table></div>

<h2 id="reducidos">Tipos reducidos que pueden cambiar la cifra</h2>
<p>Resumen de los tipos reducidos que recoge cada norma (detalle y requisitos en el artículo citado, enlazado en la tabla de tipos):</p>
<ul>{red}</ul>
<p class="note">{e(", ".join(gen))}: tienen tipos reducidos para determinados casos (vivienda habitual, edad, familia numerosa, discapacidad o vivienda protegida) que no se resumen aquí. No incluye {e(", ".join(V["excluidas"]))}. * Castilla y León: tipo orientativo, confírmalo en el boletín autonómico.</p>"""

def vivienda_md(D):
    return "Impuestos de compra de vivienda 2026, tipo general sin reducciones (usada: ITP; nueva: IVA 10 % + AJD), 200.000 € / 300.000 €:\n" + "\n".join(
        f"- {r['n']}: usada {_ef(r['usada'][200000])} / {_ef(r['usada'][300000])}; nueva {_ef(r['nueva'][200000])} / {_ef(r['nueva'][300000])}" for r in D["rows"])


# ---------- 4. SMI, IPREM, paro y pensiones ----------
def cuantias(P):
    S, J, Pa, Vi, A, Cp = P["smi_2026"], P["jubilacion_2026"], P["cuanto_cobro_paro_2026"], P["viudedad_2026"], P["autonomo_2026"], P["capitalizar_paro_2026"]
    for b in (S, J, Pa, Vi, A, Cp): assert _ok(b)
    rd241 = J["url_rd"]; sepe = Pa["url_sepe_cuantias"]; orden = A["url"]
    G = [
        ("Salario y referencias", [
            ("smi_mes", "Salario mínimo interprofesional (SMI), al mes en 14 pagas", S["mensual_14_pagas"], "€", S["fuente"], S["url"]),
            ("smi_anual", "SMI anual", S["anual"], "€", S["fuente"], S["url"]),
            ("iprem_mes", "IPREM mensual (prorrogado, sin Presupuestos 2026)", Pa["iprem_mensual"], "€", "SEPE, cuantías 2026", sepe),
            ("iprem_mas_sexta", "IPREM mensual + 1/6 (referencia del paro)", Pa["iprem_mas_sexta"], "€", "LGSS art. 270.3 y SEPE", sepe),
            ("interes_legal", "Interés legal del dinero", Cp["interes_legal_pct"], "%", "SEPE, cuantías 2026", Cp["url_sepe_cuantias"]),
        ]),
        ("Prestación por desempleo (paro)", [
            ("paro_max_0", "Paro máximo al mes, sin hijos", Pa["tope_mensual"][0], "€", "LGSS art. 270.3 y SEPE", sepe),
            ("paro_max_1", "Paro máximo al mes, 1 hijo", Pa["tope_mensual"][1], "€", "LGSS art. 270.3 y SEPE", sepe),
            ("paro_max_2", "Paro máximo al mes, 2 o más hijos", Pa["tope_mensual"][2], "€", "LGSS art. 270.3 y SEPE", sepe),
            ("paro_min_0", "Paro mínimo al mes, sin hijos", Pa["minimo_mensual"][0], "€", "LGSS art. 270.3 y SEPE", sepe),
            ("paro_min_1", "Paro mínimo al mes, con hijos", Pa["minimo_mensual"][1], "€", "LGSS art. 270.3 y SEPE", sepe),
        ]),
        ("Pensiones", [
            ("pension_max_mes", "Pensión máxima de jubilación al mes (14 pagas)", J["max_mes"], "€", "Real Decreto 241/2026", rd241),
            ("pension_max_anual", "Pensión máxima anual", J["max_anual"], "€", "Real Decreto 241/2026", rd241),
            ("min_jub_65_sin_conyuge", "Mínima de jubilación con 65 años, sin cónyuge, al año", J["minima_jubilacion_65_sin_conyuge_unipersonal"], "€", "Real Decreto 241/2026", rd241),
            ("min_jub_65_conyuge_cargo", "Mínima de jubilación con 65 años, con cónyuge a cargo, al año", J["minima_jubilacion_65_conyuge_a_cargo"], "€", "Real Decreto 241/2026", rd241),
            ("min_jub_65_conyuge_no_cargo", "Mínima de jubilación con 65 años, cónyuge no a cargo, al año", J["minima_jubilacion_65_conyuge_no_a_cargo"], "€", "Real Decreto 241/2026", rd241),
            ("min_viud_cargas", "Mínima de viudedad con cargas familiares, al año", Vi["minimo_cargas_anual"], "€", "Real Decreto 241/2026", rd241),
            ("min_viud_65", "Mínima de viudedad con 65 años o más, al año", Vi["minimo_65_anual"], "€", "Real Decreto 241/2026", rd241),
            ("min_viud_60_64", "Mínima de viudedad de 60 a 64 años, al año", Vi["minimo_60_64_anual"], "€", "Real Decreto 241/2026", rd241),
            ("min_viud_menor_60", "Mínima de viudedad menor de 60 años, al año", Vi["minimo_menor_60_anual"], "€", "Real Decreto 241/2026", rd241),
            ("limite_ingresos_minimos", "Límite de ingresos para cobrar complementos a mínimos, al año", Vi["limite_ingresos"], "€", "Real Decreto 241/2026", rd241),
            ("revalorizacion", "Revalorización general de las pensiones en 2026", J["revalorizacion_2026_pct"], "%", "Real Decreto 241/2026", rd241),
        ]),
        ("Cotización", [
            ("base_max_mes", "Base máxima de cotización al mes", A["general"]["base_max_mes"], "€", "Orden PJC/297/2026", orden),
            ("tipo_trabajador", "Cotización del trabajador, contrato indefinido", A["general"]["trabajador_indefinido_pct"], "%", "Orden PJC/297/2026", orden),
            ("tipo_empresa", "Cotización de la empresa, contrato indefinido (sin AT/EP)", A["general"]["empresa_indefinido_pct"], "%", "Orden PJC/297/2026", orden),
            ("cuota_min_autonomo", "Cuota mínima de autónomos al mes (tramo 1, sin tarifa plana)", Cp["cuota_minima_mensual"], "€", "Orden PJC/297/2026 (cálculo: base mínima × 31,5 %)", orden),
        ]),
    ]
    csvr = [["cuantias_2026", k, "valor", v, "EUR" if u == "€" else "%", f, url] for _, items in G for k, _, v, u, f, url in items]
    return dict(G=G, csv=csvr, fecha="2026-10-02")

def cuantias_body(D):
    G = D["G"]; v = {k: x for _, it in G for k, _, x, _, _, _ in it}
    secs = []
    for name, items in G:
        def mes14(k, val): return f' <span class="note">({_ef(round(val / 14, 2))} al mes en 14 pagas)</span>' if k.startswith("min_") else ""
        tr = "".join(f'<tr><th scope="row">{e(lab)}</th><td><strong>{_ef(val) if u == "€" else _pc(val)}</strong>{mes14(k, val)}</td><td>{_src(url, f)}</td></tr>'
                     for k, lab, val, u, f, url in items)
        secs.append(f'<h2 id="{name.split()[0].lower()}">{e(name)} 2026</h2>\n<div class="em-tw"><table><thead><tr><th scope="col">Concepto</th><th scope="col">Cuantía 2026</th><th scope="col">Fuente</th></tr></thead><tbody>{tr}</tbody></table></div>')
    return f"""<div class="box"><p><strong>Respuesta corta:</strong> en 2026 el SMI es de <strong>{_ef(v["smi_mes"])} al mes en 14 pagas</strong> ({_ef(v["smi_anual"])} al año), el IPREM sigue en {_ef(v["iprem_mes"])} al mes, el paro va de {_ef(v["paro_min_0"])} a {_ef(v["paro_max_2"])} al mes y la pensión máxima es de {_ef(v["pension_max_mes"])} al mes ({_ef(v["pension_max_anual"])} al año), con una revalorización general del {_pc(v["revalorizacion"])}.</p></div>
{chr(10).join(secs)}
<p class="note">Las cuantías mensuales de las pensiones mínimas son la anual dividida entre 14 pagas. El paro mínimo «con hijos» es el mismo con 1 o con 2 o más hijos.</p>"""

def cuantias_md(D):
    return "Cuantías oficiales 2026:\n" + "\n".join(f"- {lab}: {_ef(val) if u == '€' else _pc(val)} ({f})" for _, it in D["G"] for _, lab, val, u, f, _ in it)


# ---------- 5. Trabajo y prestaciones (c42) ----------
def trabajo(P):
    Pa, Pn, Ja, Di, Kd, Rf, Fi = (P.get(k) for k in ("cuanto_cobro_paro_2026", "permiso_nacimiento_2026", "jubilacion_activa_2026",
        "indemnizacion_despido_2026", "kilometraje_dietas_2026", "retribucion_flexible_2026", "finiquito_baja_voluntaria_2026"))
    for b in (Pa, Pn, Ja, Di, Kd, Rf, Fi): assert _ok(b) and b.get("confianza") in ("A", "A−"), "clave sin confianza A/A−"
    sepe = Pa["url_sepe_cuantias"]; ET = Di["url"]
    # item: (clave, rótulo, valor, tipo, fuente, url)  tipo: eur, pct, dias, sem, mens, eurkm
    G = []
    def add(name, items): G.append((name, [i for i in items if i[2] is not None and i[5]]))
    add("Prestación por desempleo (paro)", [
        ("paro_max_0", "Paro máximo al mes, sin hijos", Pa.get("tope_mensual", [None])[0], "eur", "LGSS art. 270.3 y SEPE", sepe),
        ("paro_max_1", "Paro máximo al mes, 1 hijo", Pa.get("tope_mensual", [None] * 2)[1], "eur", "LGSS art. 270.3 y SEPE", sepe),
        ("paro_max_2", "Paro máximo al mes, 2 o más hijos", Pa.get("tope_mensual", [None] * 3)[2], "eur", "LGSS art. 270.3 y SEPE", sepe),
        ("paro_min_0", "Paro mínimo al mes, sin hijos", Pa.get("minimo_mensual", [None])[0], "eur", "LGSS art. 270.3 y SEPE", sepe),
        ("paro_min_1", "Paro mínimo al mes, con hijos", Pa.get("minimo_mensual", [None] * 2)[1], "eur", "LGSS art. 270.3 y SEPE", sepe),
        ("paro_pct_180", "Porcentaje de la base reguladora, primeros 180 días", Pa.get("pct_primeros_180_dias"), "pct", "LGSS art. 270.2", Pa["url"]),
        ("paro_pct_despues", "Porcentaje de la base reguladora, desde el día 181", Pa.get("pct_despues"), "pct", "LGSS art. 270.2", Pa["url"]),
        ("paro_dias_minimos", "Días cotizados mínimos en los 6 años anteriores", Pa.get("dias_minimos_cotizados"), "dias", "LGSS art. 269.1", Pa["url"]),
    ])
    esc = [("duracion_%d" % d, f"Duración de la prestación con {num(d, 0)} días cotizados o más", v, "dias", "LGSS art. 269.1", Pa["url"]) for d, v in Pa.get("escala_duracion", [])]
    add("Duración del paro según días cotizados", esc)
    add("Permiso de nacimiento", [
        ("nac_semanas", "Semanas de permiso por progenitor", Pn.get("semanas_total"), "sem", "ET art. 48.4 (RDL 9/2025)", Pn["url_et"]),
        ("nac_obligatorias", "Semanas obligatorias e ininterrumpidas tras el parto", Pn.get("semanas_obligatorias"), "sem", "ET art. 48.4", Pn["url_et"]),
        ("nac_12_meses", "Semanas voluntarias hasta los 12 meses del hijo", Pn.get("semanas_12_meses"), "sem", "ET art. 48.4", Pn["url_et"]),
        ("nac_8_anos", "Semanas voluntarias hasta los 8 años del hijo", Pn.get("semanas_8_anos"), "sem", "ET art. 48.4", Pn["url_et"]),
        ("nac_monoparental", "Semanas en familia monoparental", Pn.get("semanas_monoparental"), "sem", "ET art. 48.4", Pn["url_et"]),
        ("nac_base_max", "Base máxima de cotización al mes (tope de la prestación)", Pn.get("base_maxima_mes"), "eur", "Orden PJC/297/2026, art. 2.1", Pn["url_orden_cotizacion"]),
    ])
    esc_ja = Ja.get("escala_pct", [])
    add("Jubilación activa", [("ja_escala_%d" % (i + 1), f"Porcentaje de la pensión que se cobra con {i + 1} {'año' if i == 0 else 'años'} de demora" + (" o más" if i == len(esc_ja) - 1 else ""),
                                p, "pct", "LGSS art. 214", Ja["url"]) for i, p in enumerate(esc_ja)] + [
        ("ja_autonomo_contrata", "Porcentaje si el autónomo contrata a un trabajador", Ja.get("pct_autonomo_contrata"), "pct", "LGSS art. 214", Ja["url"]),
        ("ja_suma", "Puntos que se suman cada 12 meses en activa", Ja.get("suma_pp_cada_12_meses"), "pp", "LGSS art. 214", Ja["url"]),
        ("ja_solidaridad", "Cotización de solidaridad (empresa 7 % + trabajador 2 %)", Ja.get("solidaridad_pct"), "pct", "LGSS arts. 153 y 310", Ja["url"]),
    ])
    add("Indemnización por despido", [
        ("desp_dias_obj", "Despido objetivo: días de salario por año de servicio", Di.get("dias_objetivo"), "dias", "ET art. 53.1.b", ET),
        ("desp_tope_obj", "Despido objetivo: máximo", Di.get("tope_objetivo_mensualidades"), "mens", "ET art. 53.1.b", ET),
        ("desp_dias_imp", "Despido improcedente: días de salario por año de servicio", Di.get("dias_improcedente"), "dias", "ET art. 56.1", ET),
        ("desp_tope_imp", "Despido improcedente: máximo", Di.get("tope_improcedente_mensualidades"), "mens", "ET art. 56.1", ET),
        ("desp_dias_pre", "Contratos anteriores al 12-2-2012: días por año hasta esa fecha", Di.get("dias_previo_2012"), "dias", "ET DT 11.ª", ET),
        ("desp_tope_pre", "Contratos anteriores al 12-2-2012: máximo", Di.get("tope_previo_mensualidades"), "mens", "ET DT 11.ª", ET),
        ("desp_exenta", "Indemnización obligatoria exenta de IRPF, hasta", Di.get("exencion_tope"), "eur", "Ley 35/2006, art. 7.e", Di["url_irpf"]),
    ])
    add("Kilometraje y dietas exentas", [
        ("km", "Kilometraje exento (más peajes y aparcamiento justificados)", Kd.get("km_eur"), "eurkm", "Orden HFP/792/2023", Kd["url_orden"]),
        ("dieta_sin_es", "Manutención sin pernocta, en España", Kd.get("manutencion_sin_pernocta_espana"), "eur", "RIRPF art. 9.A.3", Kd["url"]),
        ("dieta_con_es", "Manutención con pernocta, en España", Kd.get("manutencion_con_pernocta_espana"), "eur", "RIRPF art. 9.A.3", Kd["url"]),
        ("dieta_sin_ext", "Manutención sin pernocta, en el extranjero", Kd.get("manutencion_sin_pernocta_extranjero"), "eur", "RIRPF art. 9.A.3", Kd["url"]),
        ("dieta_con_ext", "Manutención con pernocta, en el extranjero", Kd.get("manutencion_con_pernocta_extranjero"), "eur", "RIRPF art. 9.A.3", Kd["url"]),
    ])
    add("Retribución flexible: topes exentos", [
        ("rf_seguro", "Seguro de salud, por persona y año", Rf.get("seguro_persona"), "eur", "Ley 35/2006, art. 42.3.c", Rf["url"]),
        ("rf_seguro_disc", "Seguro de salud, por persona con discapacidad y año", Rf.get("seguro_persona_discapacidad"), "eur", "Ley 35/2006, art. 42.3.c", Rf["url"]),
        ("rf_comida", "Comida en fórmulas indirectas (vales, tarjeta), por día", Rf.get("comida_dia"), "eur", "RIRPF art. 45.2", Rf["url_rirpf"]),
        ("rf_transporte", "Transporte colectivo, por año", Rf.get("transporte_anual"), "eur", "Ley 35/2006, art. 42.3.e", Rf["url"]),
        ("rf_transporte_mes", "Tarjeta de transporte, por mes", Rf.get("transporte_mes_tarjeta"), "eur", "RIRPF arts. 46 y 46 bis", Rf["url_rirpf"]),
        ("rf_especie", "Máximo del salario en especie sobre las percepciones salariales", Rf.get("especie_max_pct"), "pct", "ET art. 26.1", Rf["url_et"]),
    ])
    add("Finiquito", [
        ("fin_vacaciones", "Vacaciones mínimas anuales (compensables al extinguirse el contrato si no se disfrutaron)", Fi.get("vacaciones_minimas_dias"), "diasnat", "ET art. 38.1 y Convenio 132 OIT", Fi["url"]),
        ("fin_base_max", "Tope de base de cotización al mes", Fi.get("base_maxima_cotizacion_mes"), "eur", "Orden PJC/297/2026", Fi["url_orden_cotizacion"]),
    ])
    UN = {"eur": "EUR", "pct": "%", "dias": "dias", "sem": "semanas", "mens": "mensualidades", "eurkm": "EUR/km", "pp": "puntos", "diasnat": "dias_naturales"}
    csvr = [["trabajo_prestaciones_2026", k, "valor", v, UN[t], f, u] for _, it in G for k, _, v, t, f, u in it]
    return dict(G=G, csv=csvr, fecha="2026-10-02", v={k: v for _, it in G for k, _, v, _, _, _ in it})

def _tv(v, t):
    if t == "eur": return _ef(v)
    if t == "eurkm": return _f(v) + " €/km"
    if t == "pct": return _pc(v)
    if t == "pp": return f"{_f(v)} puntos"
    if t == "sem": return f"{_f(v)} semanas"
    if t == "mens": return f"{_f(v)} mensualidades"
    if t == "diasnat": return f"{_f(v)} días naturales"
    return f"{_f(v)} días"

def trabajo_body(D):
    G, v = D["G"], D["v"]
    secs = []
    for name, items in G:
        if not items: continue
        tr = "".join(f'<tr><th scope="row">{e(lab)}</th><td><strong>{e(_tv(val, t))}</strong></td><td>{_src(url, f)}</td></tr>' for k, lab, val, t, f, url in items)
        sid = "t-" + "".join(c for c in name.lower().split(":")[0].replace(" ", "-") if c.isalnum() or c == "-")
        secs.append(f'<h2 id="{sid}">{e(name)} 2026</h2>\n<div class="em-tw"><table><thead><tr><th scope="col">Concepto</th><th scope="col">Cuantía 2026</th><th scope="col">Fuente</th></tr></thead><tbody>{tr}</tbody></table></div>')
    g = lambda k, d="": _tv(v[k], "eur") if k in v else d
    return f"""<div class="box"><p><strong>Respuesta corta:</strong> en 2026 el paro va de <strong>{g("paro_min_0")} a {g("paro_max_2")} al mes</strong> según hijos; el permiso de nacimiento es de <strong>{_f(v["nac_semanas"])} semanas por progenitor</strong> con tope de base de {g("nac_base_max")} al mes; la indemnización por despido es de {_f(v["desp_dias_obj"])} días por año en el objetivo ({_f(v["desp_tope_obj"])} mensualidades máximo) y de {_f(v["desp_dias_imp"])} en el improcedente ({_f(v["desp_tope_imp"])} máximo); el kilometraje exento es de {_tv(v["km"], "eurkm")}; y las vacaciones mínimas son de {_f(v["fin_vacaciones"])} días naturales al año.</p></div>
{chr(10).join(secs)}
<p class="note">Cada fila enlaza la norma o la página oficial de la que sale; son las mismas cifras que usan nuestras calculadoras. El importe exacto de tu caso depende de tu base de cotización, tus años de servicio y tu convenio: usa la calculadora enlazada abajo. La escala de la jubilación activa se aplica según los años completos de demora del acceso a la pensión.</p>"""

def trabajo_md(D):
    return "Trabajo y prestaciones 2026:\n" + "\n".join(f"- {lab}: {_tv(val, t)} ({f})" for _, it in D["G"] for _, lab, val, t, f, _ in it)


# ---------- páginas ----------
PAGES = [
    dict(slug="tramos-irpf-comunidades", compute=irpf, body=irpf_body, md=irpf_md,
         title="Tramos del IRPF 2026 por comunidad autónoma: tablas",
         h1="Tramos del IRPF 2026: escala estatal y de cada comunidad",
         description="Escala estatal y autonómica del IRPF 2026 con fuente del BOE, tipo marginal por comunidad y cuánto se paga con 20.000, 30.000 o 50.000 € de base.",
         nav="IRPF por comunidad", hubs=["impuestos"],
         calcs=["retencion-irpf-nomina-subir-o-no", "declaracion-conjunta-o-individual", "comparar-ofertas-de-trabajo-neto-real", "autonomo-o-asalariado"],
         variables=["Escala estatal del IRPF (%)", "Escala autonómica por comunidad (%)", "Cuota íntegra por comunidad y base liquidable (€)", "Tipo marginal combinado (%)", "Escala del ahorro (%)"],
         keywords=["tramos IRPF 2026", "escala autonómica IRPF", "IRPF por comunidad autónoma", "tipo marginal IRPF"]),
    dict(slug="cuota-autonomos-tramos", compute=autonomos, body=autonomos_body, md=autonomos_md,
         title="Cuota de autónomos 2026 por tramos: tabla oficial",
         h1="Cuota de autónomos 2026: tabla de tramos, bases y cuotas",
         description="Los 15 tramos de cotización de autónomos en 2026 (Orden PJC/297/2026) con base mínima y máxima y la cuota mensual y anual que sale de cada una.",
         nav="Cuota de autónomos", hubs=["impuestos"],
         calcs=["autonomo-o-asalariado", "autonomo-o-sociedad-limitada", "autonomo-estimacion-directa-o-modulos", "cuota-autonomos-ingresos-reales-regularizacion", "capitalizar-paro-o-cobrarlo"],
         variables=["Rendimiento neto mensual por tramo (€)", "Base mínima y máxima de cotización (€/mes)", "Cuota mínima y máxima (€/mes)", "Cuota mínima anual (€)"],
         keywords=["cuota autónomos 2026", "tramos autónomos 2026", "tabla cotización autónomos", "base mínima autónomos"]),
    dict(slug="itp-ajd-comunidades", compute=vivienda, body=vivienda_body, md=vivienda_md,
         title="ITP y AJD 2026 por comunidad: tipos y coste de compra",
         h1="ITP y AJD 2026 por comunidad: tipos y lo que pagas al comprar casa",
         description="Tipos de ITP (vivienda usada) y AJD (nueva) de cada comunidad en 2026, con su norma, y cuánto se paga en impuestos por una casa de 200.000 o 300.000 €.",
         nav="ITP y AJD por comunidad", hubs=["hipoteca"],
         calcs=["cuanto-ahorrar-para-comprar-casa", "alquilar-o-comprar", "hipoteca-mas-entrada-o-conservar-ahorros"],
         variables=["Tipo de ITP por comunidad (%)", "Tipo de AJD por comunidad (%)", "Impuestos de compra de vivienda usada y nueva (€)"],
         keywords=["ITP por comunidades 2026", "impuesto transmisiones patrimoniales vivienda", "AJD vivienda nueva", "impuestos comprar casa"]),
    dict(slug="smi-iprem-paro-pensiones", compute=cuantias, body=cuantias_body, md=cuantias_md,
         title="SMI, IPREM, paro y pensiones 2026: cuantías oficiales",
         h1="SMI, IPREM, paro y pensiones 2026: todas las cuantías oficiales",
         description="SMI, IPREM, paro máximo y mínimo, pensión máxima y mínimas, base máxima de cotización e interés legal de 2026, cada cifra con su fuente oficial enlazada.",
         nav="SMI, IPREM y pensiones", hubs=["impuestos", "ahorro"],
         calcs=["cuanto-cobro-de-paro-prestacion-desempleo", "jubilacion-anticipada-o-demorada", "pension-viudedad-cuanto-cobro", "capitalizar-paro-o-cobrarlo"],
         variables=["SMI (€)", "IPREM (€)", "Paro máximo y mínimo (€/mes)", "Pensión máxima y mínimas (€)", "Base máxima de cotización (€/mes)", "Interés legal del dinero (%)"],
         keywords=["SMI 2026", "IPREM 2026", "pensión máxima 2026", "paro máximo 2026", "pensión mínima 2026"]),
    dict(slug="trabajo-prestaciones", compute=trabajo, body=trabajo_body, md=trabajo_md,
         title="Trabajo y prestaciones 2026: paro, despido, permisos",
         h1="Trabajo y prestaciones 2026: paro, permiso de nacimiento, despido y dietas",
         description="Paro máximo y mínimo y su duración, permiso de nacimiento, jubilación activa, despido, kilometraje, dietas y finiquito en 2026, con fuente.",
         nav="Trabajo y prestaciones", hubs=["impuestos", "ahorro"],
         calcs=["cuanto-cobro-de-paro-prestacion-desempleo", "permiso-nacimiento-cuanto-cobro-y-como-repartir", "jubilacion-activa-o-dejar-de-trabajar", "indemnizacion-despido-objetivo-o-improcedente-neto", "kilometraje-y-dietas-exentas-irpf", "retribucion-flexible-me-conviene", "finiquito-baja-voluntaria-vacaciones-preaviso"],
         variables=["Paro máximo y mínimo (€/mes)", "Duración del paro (días)", "Permiso de nacimiento (semanas)", "Jubilación activa (% de la pensión)", "Indemnización por despido (días por año y mensualidades máximas)", "Kilometraje y dietas exentas (€)", "Retribución flexible exenta (€)", "Vacaciones del finiquito (días)"],
         keywords=["paro 2026 cuantía máxima", "permiso nacimiento 19 semanas", "indemnización despido 33 días", "kilometraje exento 0,26", "dietas exentas 2026", "jubilación activa porcentaje"]),
]
BY = {p["slug"]: p for p in PAGES}
FILES = ["tablas.py", "data/params.json"]

def path(slug): return f"{INDEX}{slug}/"

def build(dist, params, base):
    """Calcula todo y escribe los CSV y /tablas-2026/datos.json. -> dict con los datos por página."""
    T = {}
    out = {"nombre": "Tablas 2026 Entre Muchos", "url": base + INDEX, "fecha_revision": params.get("irpf_2026", {}).get("consultado", params.get("fecha")),
           "licencia_calculos_propios": "CC BY 4.0", "licencia_url": LIC, "tablas": {}}
    for p in PAGES:
        D = p["compute"](params); T[p["slug"]] = D
        d = os.path.join(dist, path(p["slug"]).strip("/")); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "datos.csv"), "w").write(_csv(D["csv"]))
        out["tablas"][p["slug"]] = {"url": base + path(p["slug"]), "csv": base + path(p["slug"]) + "datos.csv", "filas": [dict(zip(["tabla", "clave", "campo", "valor", "unidad", "fuente", "url_fuente"], r)) for r in D["csv"]]}
    os.makedirs(os.path.join(dist, INDEX.strip("/")), exist_ok=True)
    json.dump(out, open(os.path.join(dist, INDEX.strip("/"), "datos.json"), "w"), ensure_ascii=False, indent=1)
    return T

def _byline(D, modified, author):
    return (f'<p class="byline note">Por {author} · Cifras revisadas el <time datetime="{D["fecha"]}">{fecha_es(D["fecha"])}</time> en la fuente oficial · '
            f'Página actualizada el <time datetime="{modified}">{fecha_es(modified)}</time> · <a href="#descargas">Descargar CSV · CC BY 4.0</a></p>')

def page(slug, T, calcs, card, modified, author):
    p = BY[slug]; D = T[slug]; by = {c["slug"]: c for c in calcs}
    rel = [by[s] for s in p["calcs"] if s in by]
    others = "".join(f'<li><a href="{path(q["slug"])}">{e(q["h1"])}</a></li>' for q in PAGES if q["slug"] != slug)
    return f"""<article class="guide barometro tablas">
<p class="kicker"><a href="{INDEX}">Tablas 2026</a> · Datos oficiales verificados</p>
<h1>{e(p["h1"])}</h1>
{_byline(D, modified, author)}
{p["body"](D)}

<h2>Calcúlalo con tus números</h2>
<ul class="cards">{"".join(card(c) for c in rel)}</ul>

<h2 id="descargas">Descargas, metodología y cómo citar</h2>
<ul>
<li><strong>CSV:</strong> <a href="{path(slug)}datos.csv">{path(slug)}datos.csv</a> (tabla, clave, campo, valor, unidad, fuente y URL de la fuente en cada fila). Todas las tablas en JSON: <a href="{INDEX}datos.json">{INDEX}datos.json</a>.</li>
<li><strong>De dónde salen las cifras:</strong> cada cifra oficial se ha leído en el texto consolidado del BOE o en la página oficial enlazada en su fila, y es la misma que usan nuestras calculadoras (un cambio en la norma cambia a la vez la tabla y la calculadora). Las filas marcadas como cálculo propio aplican esas cifras con la fórmula descrita encima de cada tabla.</li>
<li><strong>Cómo citar:</strong> «Tablas 2026 Entre Muchos» con el enlace a esta página y la fecha de revisión ({fecha_es(D["fecha"])}). Los cálculos propios se publican con licencia <a href="{LIC}" rel="noopener">CC BY 4.0</a>; las cifras oficiales son de la fuente citada.</li>
<li>Si ves una cifra que no coincide con el BOE, escríbenos desde <a href="/contacto/">contacto</a>: la corregimos y anotamos la fecha.</li>
</ul>
<p>Más tablas 2026:</p>
<ul>{others}</ul>
<p class="disclaimer">Información orientativa, no constituye asesoramiento fiscal, laboral ni financiero. Tu caso depende de tu situación personal y de los requisitos de cada norma: usa las calculadoras con tus números y, si la decisión es importante, consulta con un profesional. Lee <a href="/como-funciona/">cómo trabajamos</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""

def index_page(T, modified, author):
    items = "".join(f'<li><a href="{path(p["slug"])}"><strong>{e(p["h1"])}</strong></a><br><span class="note">{e(p["description"])}</span></li>' for p in PAGES)
    fecha = T[PAGES[0]["slug"]]["fecha"]
    return f"""<article class="guide tablas">
<p class="kicker">Datos oficiales verificados</p>
<h1>Tablas 2026: IRPF, autónomos, ITP, pensiones y trabajo</h1>
<p class="byline note">Por {author} · Cifras revisadas el <time datetime="{fecha}">{fecha_es(fecha)}</time> · Página actualizada el <time datetime="{modified}">{fecha_es(modified)}</time></p>
<p class="lead">Las cifras oficiales de 2026 que usan nuestras calculadoras, en tablas limpias, con la norma enlazada en cada fila y un cálculo propio que no encontrarás junto en otro sitio: cuánto IRPF se paga en cada comunidad, la cuota de autónomos de cada tramo, los impuestos de compra de una vivienda por comunidad y las cuantías de trabajo y prestaciones (paro, permiso de nacimiento, despido y dietas).</p>
<ul class="guides">{items}</ul>
<p>Todas las tablas en un archivo: <a href="{INDEX}datos.json">{INDEX}datos.json</a> (y un CSV en cada página). Para cifras de mercado que cambian cada mes (Euríbor, carburantes, coste por km), consulta el <a href="/barometro/">Barómetro Entre Muchos</a>.</p>
<p class="disclaimer">Información orientativa, no constituye asesoramiento fiscal, laboral ni financiero. Lee <a href="/como-funciona/">cómo trabajamos</a>.</p>
</article>"""

def jsonld(slug, T, base, modified, published, org, article, breadcrumbs):
    p = BY[slug]; url = base + path(slug)
    ds = {"@context": "https://schema.org", "@type": "Dataset", "name": p["h1"], "description": p["description"], "url": url,
          "inLanguage": "es-ES", "isAccessibleForFree": True, "creator": org, "publisher": {"@id": base + "/#org"},
          "dateModified": modified, "datePublished": published, "temporalCoverage": "2026", "spatialCoverage": {"@type": "Place", "name": "España"},
          "keywords": p["keywords"], "variableMeasured": p["variables"], "license": LIC,
          "isBasedOn": sorted({r[6] for r in T[slug]["csv"] if r[6]}),
          "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": url + "datos.csv"},
                           {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": base + INDEX + "datos.json"}]}
    tb = {"@context": "https://schema.org", "@type": "Table", "about": p["h1"], "url": url, "inLanguage": "es-ES", "dateModified": modified}
    return [ds, tb, article(p["h1"], p["description"], url, published, modified, base),
            breadcrumbs(base, [("Inicio", "/"), ("Tablas 2026", INDEX), (p["h1"], None)])]

def index_jsonld(base, modified, published, org, breadcrumbs, desc):
    return [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Tablas 2026", "description": desc, "url": base + INDEX,
             "inLanguage": "es-ES", "datePublished": published, "dateModified": modified, "publisher": org,
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(PAGES), "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": p["h1"], "url": base + path(p["slug"])} for i, p in enumerate(PAGES)]}},
            breadcrumbs(base, [("Inicio", "/"), ("Tablas 2026", None)])]

# ---------- enlaces desde otras páginas ----------
def calc_link(slug):
    ps = [p for p in PAGES if slug in p["calcs"]]
    if not ps: return ""
    return '<p class="note hub-link"><strong>Tabla oficial 2026:</strong> ' + " · ".join(f'<a href="{path(p["slug"])}">{e(p["h1"])}</a>' for p in ps[:2]) + " (con fuente y CSV).</p>"

def hub_items(hub_key):
    return [(path(p["slug"]), p["h1"], p["description"]) for p in PAGES if hub_key in p["hubs"]]

def llms_lines(base):
    return [f"- [{p['h1']}]({base}{path(p['slug'])}): {p['description']} CSV: {base}{path(p['slug'])}datos.csv" for p in PAGES]

def llms_md(T, base):
    out = [f"\n---\n\n## Tablas 2026 Entre Muchos\n\nURL: {base}{INDEX}\nDatos (JSON): {base}{INDEX}datos.json\nCifras revisadas en la fuente oficial: {T[PAGES[0]['slug']]['fecha']}. Cálculos propios: CC BY 4.0.\n"]
    for p in PAGES:
        out.append(f"\n### {p['h1']}\n\nURL: {base}{path(p['slug'])}\n\n{p['md'](T[p['slug']])}\n")
    return "".join(out)

def feed_items(base, modified, published):
    return [dict(id=f"tag:entremuchos.com,2026:tablas-2026/{p['slug']}", title=p["h1"], url=base + path(p["slug"]), published=published,
                 updated=modified, summary=p["description"], cat="Tablas 2026") for p in PAGES]
