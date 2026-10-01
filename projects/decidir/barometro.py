"""Barómetro Entre Muchos (dueño: Estratega SEO/GEO). Solo stdlib.
Datos propios, fechados y reproducibles: se calculan en cada build con data/params.json y con un port
a Python de las funciones puras de las calculadoras (calcs/<slug>.js). ops/check_barometro.py ejecuta
el JS real de cada calculadora con las mismas entradas y exige que coincida con /barometro/datos.json.
Genera /barometro/ (respuesta primero, tablas, Dataset + Article) y /barometro/datos.json.
Revertir: quitar la llamada a barometro.build(...) en build.py main() y los enlaces (footer, calc_link, home)."""
import json, os, html
import calcs_loader

ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = "/barometro/"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
CALCS = ["hipoteca-fija-o-variable", "diesel-gasolina-hibrido-electrico", "amortizar-o-invertir"]
FILES = ["barometro.py", "data/params.json"] + [f"calcs/{s}.{e}" for s in CALCS for e in ("js", "json")]


# ---------- port 1:1 de las funciones puras (mismo orden de operaciones que el JS) ----------
def cuota_francesa(P, i, n):
    return P / n if i == 0 else P * i / (1 - (1 + i) ** (-n))

def simular_variable(P, n, tipo1, tipo2):
    i1, i2 = max(tipo1, 0) / 1200, max(tipo2, 0) / 1200
    c1 = cuota_francesa(P, i1, n); saldo = P; inter = 0.0; m = min(12, n)
    for _ in range(m):
        im = saldo * i1; inter += im; saldo -= c1 - im
    if n <= 12: return {"cuota1": c1, "cuota2": c1, "intereses": inter}
    c2 = cuota_francesa(saldo, i2, n - 12)
    return {"cuota1": c1, "cuota2": c2, "intereses": inter + c2 * (n - 12) - saldo}

def euribor_equilibrio(P, n, euribor, dif, int_fija):
    lo, hi = -5.0, 30.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if simular_variable(P, n, euribor + dif, mid + dif)["intereses"] > int_fija: hi = mid
        else: lo = mid
    return (lo + hi) / 2

def hipoteca(d):
    """= calcular() de calcs/hipoteca-fija-o-variable.js"""
    P, n, iF = d["capital"], round(d["anos"] * 12), d["fijo"] / 1200
    cuota_fija = cuota_francesa(P, iF, n); int_fija = cuota_fija * n - P
    v = simular_variable(P, n, d["euribor"] + d["dif"], d["euribor"] + d["escenario"] + d["dif"])
    return {"cuotaFija": cuota_fija, "intFija": int_fija, "cuotaVar1": v["cuota1"], "cuotaVar2": v["cuota2"],
            "intVar": v["intereses"], "diferencia": v["intereses"] - int_fija,
            "euriborEquilibrio": euribor_equilibrio(P, n, d["euribor"], d["dif"], int_fija)}

MOTORES = [("Diesel", "Diésel"), ("Gasolina", "Gasolina"), ("Hibrido", "Híbrido"), ("Electrico", "Eléctrico")]
def coche(d):
    """= calcular() de calcs/diesel-gasolina-hibrido-electrico.js (solo las salidas que usamos)"""
    kwh = d["pctCasa"] / 100 * d["kwhCasa"] + (1 - d["pctCasa"] / 100) * d["kwhPublico"]
    out = {"precioKwh": kwh}; tot = []
    for k, _ in MOTORES:
        precio = kwh if k == "Electrico" else (d["precioDiesel"] if k == "Diesel" else d["precioGasolina"])
        e_km = d["cons" + k] / 100 * precio
        fijo = d["compra" + k] * (1 - d["res" + k] / 100) + (d["seguro" + k] + d["mant" + k] + d["imp" + k]) * d["anos"]
        tot.append((fijo, e_km, fijo + e_km * d["km"] * d["anos"]))
        out["coste" + k] = tot[-1][2]; out["costeKm" + k] = tot[-1][2] / (d["km"] * d["anos"]); out["mes" + k] = tot[-1][2] / (d["anos"] * 12)
    orden = sorted(range(4), key=lambda a: tot[a][2]); g, s = orden[0], orden[1]
    den = (tot[g][1] - tot[s][1]) * d["anos"]; km_eq = 0
    if den != 0:
        k = (tot[s][0] - tot[g][0]) / den
        if k > 0: km_eq = k
    out.update({"ganador": g, "segundo": s, "kmEquilibrio": km_eq, "diferencia": tot[s][2] - tot[g][2],
                "energiaKm": [t[1] for t in tot]})
    return out

def _simular_amort(d, rentab):
    n, i, j = round(d["anos"] * 12), d["tipo"] / 1200, (1 + rentab / 100) ** (1 / 12) - 1
    imp = min(d["importe"], d["capital"]); E = imp / (1 + d["comision"] / 100)
    cuota0 = cuota_francesa(d["capital"], i, n); Pn = d["capital"] - E
    cuotaA = cuota_francesa(Pn, i, n) if d["modo"] == 2 else cuota0
    saldo, carA, aporA, carB, aporB = Pn, 0.0, 0.0, imp, imp
    for _ in range(n):
        pago = 0
        if saldo > 0.005:
            im = saldo * i; pago = min(cuotaA, saldo + im); saldo -= pago - im
        libre = cuota0 - pago + d["aporte"]
        carA = carA * (1 + j) + libre; aporA += libre
        carB = carB * (1 + j) + d["aporte"]; aporB += d["aporte"]
    t = d["impuesto"] / 100
    return carA - max(carA - aporA, 0) * t, carB - max(carB - aporB, 0) * t

def amortizar(d):
    """= calcular() de calcs/amortizar-o-invertir.js (patrimonios y rentabilidad de equilibrio)"""
    A, B = _simular_amort(d, d["rentab"])
    lo, hi = -20.0, 60.0; eq = None
    flo, fhi = _simular_amort(d, lo), _simular_amort(d, hi)
    if (flo[1] - flo[0]) * (fhi[1] - fhi[0]) <= 0:
        for _ in range(80):
            mid = (lo + hi) / 2; sm = _simular_amort(d, mid); fm = sm[1] - sm[0]
            if (flo[1] - flo[0]) * fm <= 0: hi = mid
            else: lo, flo = mid, sm
        eq = (lo + hi) / 2
    return {"patrimonioAmortizar": A, "patrimonioInvertir": B, "diferencia": B - A, "rentabilidadDeEquilibrio": eq}


# ---------- formato es-ES ----------
def num(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
def pct(x, dec=2): return num(x, dec) + " %"
def eur(x, dec=0): return num(x, dec) + " €"
def mes_es(iso):
    y, m, _ = iso.split("-"); return f"{MESES[int(m) - 1]} de {y}"
def fecha_es(iso):
    y, m, d = iso.split("-"); return f"{int(d)} de {MESES[int(m) - 1]} de {y}"
def el(motor): return "el de gasolina" if motor == "Gasolina" else "el " + motor.lower()
def r(x, d=4): return None if x is None else round(x, d)


# ---------- datos ----------
def defaults(slug, params=None, live=None):
    """Valores por defecto de la calculadora, resueltos igual que el build (default_from live/params)."""
    c = json.load(open(os.path.join(ROOT, "calcs", slug + ".json")))
    return {i["id"]: (float(i["options"][0]["v"]) if i.get("type") == "select" else calcs_loader.resolve_default(i, params or {}, live)) for i in c["inputs"]}

def compute(params, base, live=None):
    """params de data/params.json; el mercado (Euríbor, combustibles) sale de data/live.json si está fresco (calcs_loader.merge_market)."""
    live = calcs_loader.load_live() if live is None else live
    params = calcs_loader.merge_market(params, live)
    fecha_datos = max([params["fecha"]] + [params[k] for k in ("fecha_euribor", "fecha_combustibles") if params.get("mercado_vivo") and k in params])
    eurib, fija_ref = params["euribor_12m"], params["tipo_hipoteca_fija_medio"]
    checks = []  # (calc, func, args, salida) -> ops/check_barometro.py
    # 1) Hipoteca fija o variable
    hb = dict(defaults("hipoteca-fija-o-variable", params, live), capital=150000, anos=25, euribor=eurib, escenario=0, dif=0.8)
    fijos, difs = [2.2, 2.4, 2.6, 2.8, 3.0], [0.6, 0.8, 1.0]
    if fija_ref not in fijos: fijos = sorted(fijos + [fija_ref])
    tabla_h = []
    for f in fijos:
        fila = {"tipo_fijo": f, "euribor_equilibrio": {}}
        for df in difs:
            d = dict(hb, fijo=f, dif=df); o = hipoteca(d)
            fila["euribor_equilibrio"][f"{df:.1f}"] = r(o["euriborEquilibrio"], 3)
            checks.append({"calc": "hipoteca-fija-o-variable", "func": "calcular", "args": [d], "salida": {"euriborEquilibrio": r(o["euriborEquilibrio"], 3)}})
        tabla_h.append(fila)
    hd = dict(hb, fijo=fija_ref); ho = hipoteca(hd)
    esc = {}
    for e in [-1, 0, 1, 2]:
        dd = dict(hd, escenario=float(e)); oo = hipoteca(dd); esc[str(e)] = r(oo["diferencia"], 2)
        checks.append({"calc": "hipoteca-fija-o-variable", "func": "calcular", "args": [dd], "salida": {"diferencia": r(oo["diferencia"], 2), "cuotaVar2": r(oo["cuotaVar2"], 2)}})
    checks.append({"calc": "hipoteca-fija-o-variable", "func": "calcular", "args": [hd], "salida": {k: r(ho[k], 3) for k in ("cuotaFija", "cuotaVar1", "intFija", "intVar", "euriborEquilibrio")}})
    hip = {"pregunta": "¿A partir de qué Euríbor medio futuro compensa una hipoteca fija frente a una variable?",
           "supuestos": {"capital_eur": 150000, "plazo_anos": 25, "euribor_12m_actual": eurib, "euribor_fecha_dato": params.get("fecha_euribor"), "euribor_periodo": params.get("periodo_euribor", ""), "diferencial_variable_referencia": 0.8,
                         "tipo_fijo_referencia": fija_ref, "nota": "La variable aplica el Euríbor actual el primer año y el Euríbor medio indicado del año 2 en adelante. Sistema francés, sin comisiones ni bonificaciones."},
           "referencia": {"cuota_fija": r(ho["cuotaFija"], 2), "cuota_variable_ano1": r(ho["cuotaVar1"], 2), "intereses_fija": r(ho["intFija"], 2),
                          "intereses_variable_si_euribor_se_mantiene": r(ho["intVar"], 2), "euribor_equilibrio": r(ho["euriborEquilibrio"], 3),
                          "diferencia_intereses_variable_menos_fija_por_escenario": esc},
           "tabla": tabla_h, "calculadora": base + "/decidir/hipoteca-fija-o-variable/"}
    # 2) Coche: coste por motor
    cb = dict(defaults("diesel-gasolina-hibrido-electrico", params, live), precioDiesel=params["diesel_eur_l"], precioGasolina=params["gasolina_eur_l"],
              kwhCasa=params["kwh_casa_eur"], kwhPublico=params["kwh_publico_eur"], anos=5)
    tabla_c = []
    for km in [5000, 10000, 15000, 20000, 25000, 30000]:
        d = dict(cb, km=km); o = coche(d)
        fila = {"km_ano": km, "ganador": MOTORES[o["ganador"]][1], "segundo": MOTORES[o["segundo"]][1], "diferencia_5_anos": r(o["diferencia"], 2)}
        fila.update({f"eur_km_{k.lower()}": r(o["costeKm" + k], 4) for k, _ in MOTORES})
        tabla_c.append(fila)
        checks.append({"calc": "diesel-gasolina-hibrido-electrico", "func": "calcular", "args": [d],
                       "salida": dict({"costeKm" + k: r(o["costeKm" + k], 4) for k, _ in MOTORES}, ganador=o["ganador"], segundo=o["segundo"], diferencia=r(o["diferencia"], 2))})
    d15 = dict(cb, km=15000); o15 = coche(d15)
    checks.append({"calc": "diesel-gasolina-hibrido-electrico", "func": "calcular", "args": [d15],
                   "salida": dict({"coste" + k: r(o15["coste" + k], 2) for k, _ in MOTORES}, **{"mes" + k: r(o15["mes" + k], 2) for k, _ in MOTORES},
                                  precioKwh=r(o15["precioKwh"], 4), kmEquilibrio=r(o15["kmEquilibrio"], 3))})
    energia = []
    for idx, (k, nombre) in enumerate(MOTORES):
        t = {"compra": d15["compra" + k], "consumo": d15["cons" + k], "precioEnergia": o15["precioKwh"] if k == "Electrico" else (d15["precioDiesel"] if k == "Diesel" else d15["precioGasolina"]),
             "seguro": d15["seguro" + k], "mant": d15["mant" + k], "imp": d15["imp" + k], "residual": d15["res" + k]}
        ekm = o15["energiaKm"][idx]
        energia.append({"motor": nombre, "consumo": d15["cons" + k], "unidad": "kWh/100 km" if k == "Electrico" else "l/100 km",
                        "precio_energia": r(t["precioEnergia"], 4), "eur_100km": r(ekm * 100, 2), "energia_15000km": r(ekm * 15000, 2),
                        "coste_total_5_anos": r(o15["coste" + k], 2), "coste_mes": r(o15["mes" + k], 2), "eur_km_total": r(o15["costeKm" + k], 4)})
        checks.append({"calc": "diesel-gasolina-hibrido-electrico", "func": "costeTipo", "args": [d15, t], "salida": {"energiaKm": r(ekm, 6), "total": r(o15["coste" + k], 2)}})
    car = {"pregunta": "¿Cuánto cuesta recorrer 15.000 km al año según el tipo de motor y cuál sale más barato?",
           "supuestos": {"anos_uso": 5, "precio_diesel_eur_l": params["diesel_eur_l"], "precio_gasolina_eur_l": params["gasolina_eur_l"],
                         "kwh_casa_eur": params["kwh_casa_eur"], "kwh_publico_eur": params["kwh_publico_eur"], "pct_carga_en_casa": cb["pctCasa"],
                         "precio_kwh_mixto": r(o15["precioKwh"], 4), "fecha_precios": params.get("fecha_combustibles", params["fecha"]),
                         "vehiculos": {nombre: {"compra_eur": cb["compra" + k], "consumo": cb["cons" + k], "valor_residual_pct": cb["res" + k],
                                                "seguro_eur_ano": cb["seguro" + k], "mantenimiento_eur_ano": cb["mant" + k], "impuesto_eur_ano": cb["imp" + k]} for k, nombre in MOTORES},
                         "nota": "Coste total = compra menos valor residual + seguro, mantenimiento e impuesto + energía. Vehículos tipo del segmento compacto con los valores por defecto de la calculadora."},
           "a_15000_km": {"ganador": MOTORES[o15["ganador"]][1], "segundo": MOTORES[o15["segundo"]][1], "diferencia_5_anos": r(o15["diferencia"], 2),
                          "km_ano_equilibrio_entre_ambos": r(o15["kmEquilibrio"], 3), "por_motor": energia},
           "tabla_por_km": tabla_c, "calculadora": base + "/decidir/diesel-gasolina-hibrido-electrico/"}
    # 3) Amortizar o invertir
    ab = dict(defaults("amortizar-o-invertir", params, live), capital=150000, anos=20, importe=30000, aporte=0, rentab=4, impuesto=19, comision=0)
    tipos = sorted({1.5, 2.0, 2.5, 3.0, 3.5, 4.0, fija_ref, round(eurib + 0.8, 2)})
    tabla_a = []
    for tp in tipos:
        fila = {"tipo_hipoteca": tp}
        for modo, key in [(1, "reduciendo_plazo"), (2, "reduciendo_cuota")]:
            d = dict(ab, tipo=tp, modo=modo); o = amortizar(d)
            fila[key] = r(o["rentabilidadDeEquilibrio"], 3)
            checks.append({"calc": "amortizar-o-invertir", "func": "calcular", "args": [d],
                           "salida": {"rentabilidadDeEquilibrio": r(o["rentabilidadDeEquilibrio"], 3), "patrimonioAmortizar": r(o["patrimonioAmortizar"], 2), "patrimonioInvertir": r(o["patrimonioInvertir"], 2)}})
        tabla_a.append(fila)
    amo = {"pregunta": "¿Qué rentabilidad necesita una inversión para que compense más que amortizar la hipoteca?",
           "supuestos": {"capital_pendiente_eur": 150000, "anos_restantes": 20, "importe_disponible_eur": 30000, "tributacion_ganancias_pct": 19,
                         "comision_amortizacion_pct": 0, "nota": "Rentabilidad anual neta de comisiones, antes de impuestos; el 19 % se aplica a la ganancia al final. Al amortizar, el ahorro mensual de cuota (o el dinero liberado al acabar antes) se invierte a la misma rentabilidad."},
           "tabla": tabla_a, "calculadora": base + "/decidir/amortizar-o-invertir/"}
    return {"nombre": "Barómetro Entre Muchos", "version": 1, "fecha_datos": fecha_datos, "url": base + PATH,
            "url_datos": base + PATH + "datos.json", "editor": "Entre Muchos (entremuchos.com)",
            "metodo": "Cálculo propio con las calculadoras de entremuchos.com (código abierto en la propia página) y los parámetros de mercado de la fecha. Cada cifra es reproducible introduciendo los supuestos en la calculadora enlazada.",
            "fuentes": {"euribor": params.get("euribor_fuente", ""), "combustibles": params.get("combustibles_fuente", "")},
            "datos_vivos": params.get("mercado_vivo", []),
            "hipoteca_fija_o_variable": hip, "coche_coste_por_motor": car, "amortizar_o_invertir": amo, "comprobaciones": checks}


# ---------- página ----------
def _answers(D):
    h, c, a = D["hipoteca_fija_o_variable"], D["coche_coste_por_motor"], D["amortizar_o_invertir"]
    s = h["supuestos"]; ref = h["referencia"]; c15 = c["a_15000_km"]
    a3 = next(f for f in a["tabla"] if f["tipo_hipoteca"] == 3.0)
    ganador = next(m for m in c15["por_motor"] if m["motor"] == c15["ganador"])
    return [
        f"Con el Euríbor a {pct(s['euribor_12m_actual'], 3)} y una hipoteca fija al {pct(s['tipo_fijo_referencia'])}, la fija de 150.000 € a 25 años sale más barata que una variable con diferencial del {pct(s['diferencial_variable_referencia'], 1)} si el Euríbor medio a partir del segundo año supera el <strong>{pct(ref['euribor_equilibrio'])}</strong>.",
        f"Recorriendo 15.000 km al año durante 5 años, el coche más barato en coste total es <strong>{el(c15['ganador'])}</strong>: {num(ganador['eur_km_total'], 2)} € por km ({eur(ganador['coste_mes'])} al mes), {eur(c15['diferencia_5_anos'])} menos que {el(c15['segundo'])} en 5 años.",
        f"Amortizar una hipoteca al 3 % reduciendo plazo equivale a una inversión que rinda un <strong>{pct(a3['reduciendo_plazo'])}</strong> anual antes de impuestos (con un 19 % de tributación sobre la ganancia): por debajo de eso, amortizar gana.",
    ]

def answers_text(D):
    import re
    return [re.sub(r"<[^>]+>", "", x) for x in _answers(D)]

def page(D, modified):
    h, c, a = D["hipoteca_fija_o_variable"], D["coche_coste_por_motor"], D["amortizar_o_invertir"]
    fd = D["fecha_datos"]; mes = mes_es(fd); hs = h["supuestos"]; difs = list(h["tabla"][0]["euribor_equilibrio"].keys())
    ans = "".join(f"<li>{x}</li>" for x in _answers(D))
    th = "".join(f'<th scope="col">Diferencial {pct(float(k), 1)}</th>' for k in difs)
    rows_h = "".join(f'<tr><th scope="row">{pct(f["tipo_fijo"])}{" (ref.)" if f["tipo_fijo"] == hs["tipo_fijo_referencia"] else ""}</th>' +
                     "".join(f"<td>{pct(f['euribor_equilibrio'][k])}</td>" for k in difs) + "</tr>" for f in h["tabla"])
    ref = h["referencia"]; esc = ref["diferencia_intereses_variable_menos_fija_por_escenario"]
    def esc_txt(k):
        v = esc[k]; return f"la variable paga {eur(abs(v))} {'más' if v > 0 else 'menos'} de intereses que la fija"
    c15 = c["a_15000_km"]; cs = c["supuestos"]
    rows_e = "".join(f'<tr><th scope="row">{m["motor"]}</th><td>{num(m["consumo"], 1)}&nbsp;{m["unidad"].replace(" ", "&nbsp;")}</td><td>{num(m["precio_energia"], 3)} €/{"kWh" if m["motor"] == "Eléctrico" else "l"}</td><td>{eur(m["energia_15000km"])}</td><td>{eur(m["coste_total_5_anos"])}</td><td>{eur(m["coste_mes"])}</td><td>{num(m["eur_km_total"], 2)} €</td></tr>' for m in c15["por_motor"])
    rows_k = "".join(f'<tr><th scope="row">{num(f["km_ano"])}&nbsp;km</th>' + "".join(f'<td>{num(f["eur_km_" + k.lower()], 2)} €</td>' for k, _ in MOTORES) + f'<td><strong>{f["ganador"]}</strong></td></tr>' for f in c["tabla_por_km"])
    rows_a = "".join(f'<tr><th scope="row">{pct(f["tipo_hipoteca"])}</th><td>{pct(f["reduciendo_plazo"])}</td><td>{pct(f["reduciendo_cuota"])}</td></tr>' for f in a["tabla"])
    euro_per = f", media de {mes_es(hs['euribor_periodo'] + '-01')}, dato del {fecha_es(hs['euribor_fecha_dato'])}" if hs.get("euribor_periodo") else ""
    eq_txt = f" (por encima de unos {num(c15['km_ano_equilibrio_entre_ambos'])} km al año el orden entre ambos cambia)" if c15["km_ano_equilibrio_entre_ambos"] else ""
    return f"""<article class="guide barometro">
<p class="kicker">Datos propios · {mes}</p>
<h1>Barómetro Entre Muchos: hipoteca, coche y ahorro ({mes})</h1>
<p class="byline note">Por Equipo de Entre Muchos · Datos del <time datetime="{fd}">{fecha_es(fd)}</time> · Página actualizada el <time datetime="{modified}">{fecha_es(modified)}</time> · <a href="{PATH}datos.json">Descargar datos (JSON)</a></p>
<div class="box"><p><strong>Respuesta corta ({mes}):</strong></p><ul>{ans}</ul></div>
<p>Cada mes calculamos estas cifras con nuestras propias calculadoras y los parámetros de mercado de la fecha. No son opiniones: puedes reproducir cualquier número poniendo los mismos supuestos en la calculadora enlazada.</p>

<h2 id="hipoteca">Hipoteca fija o variable: el Euríbor de equilibrio</h2>
<p>Si el Euríbor medio de los próximos años (del segundo en adelante) queda <strong>por encima</strong> de la cifra de la tabla, la hipoteca fija te sale más barata; si queda por debajo, gana la variable. Hipoteca de 150.000 € a 25 años, Euríbor actual {pct(hs["euribor_12m_actual"], 3)} aplicado el primer año.</p>
<div class="em-tw"><table>
<thead><tr><th scope="col">Tipo fijo</th>{th}</tr></thead>
<tbody>{rows_h}</tbody>
</table></div>
<p>Con la fija de referencia al {pct(hs["tipo_fijo_referencia"])} pagarías {eur(ref["cuota_fija"], 2)} al mes; la variable con diferencial {pct(hs["diferencial_variable_referencia"], 1)} empieza en {eur(ref["cuota_variable_ano1"], 2)}. Si el Euríbor se mantiene, {esc_txt("0")}; si sube 1 punto, {esc_txt("1")}; si baja 1 punto, {esc_txt("-1")}.</p>
<p><a class="btn2" href="/decidir/hipoteca-fija-o-variable/">Calcúlalo con tu oferta</a></p>

<h2 id="coche">Diésel, gasolina, híbrido o eléctrico: coste de 15.000 km al año</h2>
<p>A 15.000 km al año durante 5 años gana <strong>{el(c15["ganador"])}</strong>, seguido d{el(c15["segundo"])}{eq_txt}. La energía es solo una parte: el precio de compra y el valor residual pesan más cuantos menos kilómetros haces.</p>
<div class="em-tw"><table>
<thead><tr><th scope="col">Motor</th><th scope="col">Consumo</th><th scope="col">Precio energía</th><th scope="col">Energía 15.000 km</th><th scope="col">Coste total 5 años</th><th scope="col">Al mes</th><th scope="col">Por km</th></tr></thead>
<tbody>{rows_e}</tbody>
</table></div>
<p>Coste total por km según los kilómetros al año (5 años de uso):</p>
<div class="em-tw"><table>
<thead><tr><th scope="col">Km al año</th>{"".join(f'<th scope="col">{n}</th>' for _, n in MOTORES)}<th scope="col">Más barato</th></tr></thead>
<tbody>{rows_k}</tbody>
</table></div>
<p class="note">Precios de la energía del {fecha_es(cs["fecha_precios"])}: diésel {num(cs["precio_diesel_eur_l"], 3)} €/l, gasolina {num(cs["precio_gasolina_eur_l"], 3)} €/l (también para el híbrido), electricidad {num(cs["kwh_casa_eur"], 2)} €/kWh en casa y {num(cs["kwh_publico_eur"], 2)} €/kWh en carga pública, con un {num(cs["pct_carga_en_casa"])} % de la carga en casa ({num(cs["precio_kwh_mixto"], 3)} €/kWh de media). Precios de compra: diésel {eur(cs["vehiculos"]["Diésel"]["compra_eur"])}, gasolina {eur(cs["vehiculos"]["Gasolina"]["compra_eur"])}, híbrido {eur(cs["vehiculos"]["Híbrido"]["compra_eur"])}, eléctrico {eur(cs["vehiculos"]["Eléctrico"]["compra_eur"])}; seguro, mantenimiento, impuesto y valor residual: los valores por defecto de la calculadora.</p>
<p><a class="btn2" href="/decidir/diesel-gasolina-hibrido-electrico/">Calcúlalo con tu coche</a></p>

<h2 id="amortizar">Amortizar la hipoteca o invertir: la rentabilidad que hay que batir</h2>
<p>Amortizar es una inversión sin riesgo al tipo de tu hipoteca. La tabla muestra la rentabilidad anual (neta de comisiones, antes de impuestos) que necesitaría una inversión para igualarla, con 30.000 € disponibles, 150.000 € pendientes a 20 años y un 19 % de impuestos sobre la ganancia. Por encima de esa cifra gana invertir, <strong>si se cumple</strong>: la rentabilidad no está garantizada.</p>
<div class="em-tw"><table>
<thead><tr><th scope="col">Tipo de la hipoteca</th><th scope="col">Amortizando plazo</th><th scope="col">Amortizando cuota</th></tr></thead>
<tbody>{rows_a}</tbody>
</table></div>
<p><a class="btn2" href="/decidir/amortizar-o-invertir/">Calcúlalo con tu hipoteca</a></p>

<h2>Metodología y fuentes</h2>
<ul>
<li><strong>Cálculo propio</strong> con las mismas fórmulas que nuestras calculadoras (sistema francés de amortización; coste total de propiedad del coche; simulación mensual de amortizar frente a invertir). Una comprobación automática verifica en cada actualización que cada cifra de esta página coincide con la calculadora.</li>
<li><strong>Euríbor a 12 meses:</strong> {pct(hs["euribor_12m_actual"], 3)}{euro_per} ({html.escape(D["fuentes"]["euribor"])}). Consulta el dato oficial en el <a href="https://www.bde.es/wbe/es/estadisticas/temas/tipos-interes.html" rel="noopener">Banco de España</a>.</li>
<li><strong>Combustibles y electricidad:</strong> diésel y gasolina, media del {fecha_es(cs["fecha_precios"])} ({html.escape(D["fuentes"]["combustibles"])}); electricidad, precio orientativo de la calculadora; consulta el precio en tu zona en el <a href="https://geoportalgasolineras.es/" rel="noopener">Geoportal de gasolineras del Ministerio</a>.</li>
<li><strong>Datos en formato máquina:</strong> <a href="{PATH}datos.json">{PATH}datos.json</a> (supuestos, tablas y fecha). Si citas estas cifras, enlaza a esta página e indica la fecha de los datos ({fecha_es(fd)}).</li>
<li>Más contexto: <a href="/guias/euribor-hipoteca/">qué es el Euríbor y cómo afecta a tu hipoteca</a> y <a href="/guias/amortizacion-anticipada-comisiones/">comisiones por amortizar</a>.</li>
</ul>
<p class="disclaimer">Cifras orientativas calculadas con supuestos tipo; no constituyen asesoramiento financiero. Tu caso depende de tu oferta, tu contrato y tu coche: usa las calculadoras con tus números y, si la decisión es importante, consulta con un profesional. Lee <a href="/como-funciona/">cómo trabajamos</a> y nuestra <a href="/politica-ia/">política de uso de IA</a>.</p>
</article>"""

def jsonld(D, base, modified, published, desc, org, article, breadcrumbs):
    url = base + PATH
    ds = {"@context": "https://schema.org", "@type": "Dataset", "name": f"Barómetro Entre Muchos ({mes_es(D['fecha_datos'])})",
          "description": "Cifras propias calculadas cada mes: Euríbor de equilibrio entre hipoteca fija y variable, coste por kilómetro de coches diésel, gasolina, híbrido y eléctrico, y rentabilidad necesaria para que invertir compense frente a amortizar la hipoteca. Supuestos y metodología en la página.",
          "url": url, "inLanguage": "es-ES", "isAccessibleForFree": True, "creator": org, "publisher": {"@id": base + "/#org"},
          "dateModified": modified, "datePublished": published, "temporalCoverage": D["fecha_datos"], "spatialCoverage": {"@type": "Place", "name": "España"},
          "keywords": ["Euríbor", "hipoteca fija o variable", "coste por kilómetro", "coche eléctrico", "amortizar hipoteca", "invertir"],
          "variableMeasured": ["Euríbor de equilibrio fija/variable (%)", "Coste total por km por tipo de motor (€/km)", "Rentabilidad de equilibrio amortizar/invertir (%)"],
          "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": url + "datos.json"}]}
    return [ds, article(f"Barómetro Entre Muchos: hipoteca, coche y ahorro ({mes_es(D['fecha_datos'])})", desc, url, published, modified, base),
            breadcrumbs(base, [("Inicio", "/"), ("Barómetro", None)])]

def calc_link(slug, D):
    """Bloque para las calculadoras afines (render_calc)."""
    if not D or slug not in CALCS: return ""
    i = CALCS.index(slug); t = answers_text(D)[i]
    anchor = ["hipoteca", "coche", "amortizar"][i]
    return f'<p class="box"><strong>Dato del mes ({mes_es(D["fecha_datos"])}):</strong> {html.escape(t)} <a href="{PATH}#{anchor}">Ver el Barómetro</a></p>'

def home_teaser(D):
    t = answers_text(D)
    return (f'<h2>Barómetro de {mes_es(D["fecha_datos"])}</h2><p>{html.escape(t[0])}</p>'
            f'<p><a class="btn2" href="{PATH}">Ver el Barómetro: hipoteca, coche y ahorro</a></p>\n')

def llms_md(D, base):
    return (f"\n---\n\n## Barómetro Entre Muchos ({mes_es(D['fecha_datos'])})\n\nURL: {base}{PATH}\nDatos (JSON): {base}{PATH}datos.json\nFecha de los datos: {D['fecha_datos']}\n\n"
            + "\n".join(f"- {x}" for x in answers_text(D)) + "\n")

def build(dist, params, base):
    D = compute(params, base)
    d = os.path.join(dist, PATH.strip("/")); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "datos.json"), "w") as f: json.dump(D, f, ensure_ascii=False, indent=1)
    return D
