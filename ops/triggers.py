#!/usr/bin/env python3
"""Disparadores de actualidad (dueño: Estratega SEO/GEO). Solo stdlib.
Lee projects/decidir/data/live.json (+ historial) y data/events.json; evalúa reglas OBJETIVAS y, solo si una se activa,
escribe una nota breve y determinista (plantilla de texto + cifras) en projects/decidir/content/actualidad/<fecha>-<slug>.html.
Sin disparador no se publica nada. Las cifras del efecto salen de las mismas funciones que el Barómetro
(barometro.hipoteca / barometro.coche = port de las calculadoras, verificado por ops/check_barometro.py).
Reglas (umbrales en RULES):
  euribor    variación mensual >= 0,15 puntos (media mensual BCE, vs mes anterior)
  carburante diésel o gasolina 95 varían >= 3 % frente al dato de hace ~7 días (historial de live.json)
  pvpc       PVPC diario >= 15 % sobre la media del mes (con >= 7 días del mes)
  frio/calor mínima prevista de la semana en Madrid <= 3 °C / máxima >= 36 °C (Open-Meteo, previsión; no observación)
Uso: python3 ops/triggers.py [--dry] [--hoy YYYY-MM-DD]"""
import json, os, sys, re, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(ROOT, "projects/decidir")
sys.path.insert(0, PROJ)
import seo, barometro, calcs_loader  # noqa: E402

OUT = os.path.join(PROJ, "content/actualidad")
RULES = {
    "euribor": {"umbral_pts": 0.15, "cooldown": 20},
    "carburante": {"umbral_pct": 3.0, "dias": 7, "cooldown": 7},
    "pvpc": {"umbral_pct": 15.0, "min_dias_mes": 7, "cooldown": 7},
    "frio": {"min_c": 3.0, "cooldown": 7},
    "calor": {"max_c": 36.0, "cooldown": 7},
}
E, N, MES = seo._eur, seo._num, seo._mes


def _fresh(d, today): return seo._fresh(d, today)
def _time(iso, txt=None): return f'<time datetime="{iso}">{txt or seo._fmt_fecha(iso)}</time>'
def _fuente(d): return f'<a href="{d["fuente"]["url"]}" rel="noopener">{html.escape(d["fuente"]["nombre"])}</a>'
def _eventos(calc, today):
    ev = [r["evento"] for r in seo.eventos_activos(today) if r["evento"]["calc"] == calc]
    return "".join(f'<p class="note">En el calendario: <a href="/calendario/">{html.escape(e["titulo"])}</a>.</p>' for e in ev[:1])
def _trim(s, n): return s if len(s) <= n else s[:n - 1].rstrip() + "…"

def _mercado(params, live):
    p = calcs_loader.merge_market(params, live)
    return p

def _wrap(dato_html, efecto_html, calc, extra_fuentes, today):
    return (f'<p class="lead"><strong>Dato:</strong> {dato_html}</p>\n<h2>Qué cambia en tu decisión</h2>\n{efecto_html}\n'
            f'<p><a class="btn" href="/decidir/{calc}/">Calcula tu caso con tus números</a></p>\n<h2>Datos y fuente</h2>\n{extra_fuentes}\n{_eventos(calc, today)}')


# ---------- reglas ----------
def r_euribor(live, params, today):
    eu = live.get("datos", {}).get("euribor12m")
    cfg = RULES["euribor"]
    if not _fresh(eu, today) or eu.get("variacion_abs") is None or abs(eu["variacion_abs"]) < cfg["umbral_pts"] - 1e-9: return []
    v, prev, dif = eu["valor"], eu["anterior"], eu["variacion_abs"]
    sube = dif > 0; per = eu["extra"]["periodo"]; perp = eu["extra"].get("periodo_anterior") or eu["anterior_fecha"]
    p = _mercado(params, live)
    hb = dict(barometro.defaults("hipoteca-fija-o-variable", p, live), capital=150000, anos=25, dif=0.8, escenario=0, fijo=p["tipo_hipoteca_fija_medio"])
    o1 = barometro.hipoteca(dict(hb, euribor=v)); o0 = barometro.hipoteca(dict(hb, euribor=prev))
    c1, c0 = o1["cuotaVar1"], o0["cuotaVar1"]
    mes = MES(per)
    dato = (f'el Euríbor a 12 meses fue del {E(v, 3)} % de media en {mes}, {E(abs(dif), 2)} puntos {"más" if sube else "menos"} '
            f'que en {MES(perp).split(" de ")[0]} ({E(prev, 3)} %).')
    efecto = (f'<p>En una hipoteca variable de 150.000 € a 25 años con un diferencial del 0,8 %, la primera cuota sería de <strong>{E(c1)} €/mes</strong> '
              f'con el Euríbor de {mes}, frente a {E(c0)} € con el del mes anterior: <strong>{E(abs(c1 - c0))} € al mes {"más" if c1 > c0 else "menos"}</strong>.</p>\n'
              f'<p>Con una hipoteca fija al {E(p["tipo_hipoteca_fija_medio"], 1)} % del mismo importe, la variable sale más barata mientras el Euríbor se mantenga por debajo del <strong>{E(o1["euriborEquilibrio"], 2)} %</strong> (Euríbor de equilibrio de la calculadora).</p>')
    src = (f'<p class="note">Dato de {_time(eu["fecha_dato"], mes)}. Fuente: {_fuente(eu)}. Cálculo con la calculadora <a href="/decidir/hipoteca-fija-o-variable/">Hipoteca fija o variable</a> '
           f'(150.000 €, 25 años, diferencial 0,8 %); el diferencial de tu contrato puede ser otro.</p>')
    slug = f"euribor-{'sube' if sube else 'baja'}-{per}"
    return [dict(regla="euribor", clave=f"euribor-{per}", slug=slug, fecha=eu["fecha_dato"], calc="hipoteca-fija-o-variable",
                 title=f'El Euríbor {"sube" if sube else "baja"} {E(abs(dif), 2)} puntos en {mes.split(" de ")[0]}',
                 description=_trim(f'Euríbor a 12 meses: {E(v, 3)} % en {mes}. En una hipoteca variable de 150.000 € la cuota cambia {E(abs(c1 - c0))} € al mes.', 155),
                 body=_wrap(dato, efecto, "hipoteca-fija-o-variable", src, today))]

def _hace(hist, today, dias):
    """Entrada del historial más cercana a `dias` atrás (entre dias-1 y dias+2)."""
    best = None
    for f, v in hist or []:
        try: age = (today - datetime.date.fromisoformat(f)).days
        except ValueError: continue
        if dias - 1 <= age <= dias + 2 and (best is None or abs(age - dias) < best[0]): best = (abs(age - dias), f, v)
    return best and (best[1], best[2])

def r_carburante(live, params, today):
    D = live.get("datos", {}); cfg = RULES["carburante"]; out = []
    p = _mercado(params, live)
    for k, nombre, tkey in (("diesel", "Diésel", "Diesel"), ("gasolina95", "Gasolina 95", "Gasolina")):
        d = D.get(k)
        if not _fresh(d, today): continue
        ref = _hace(d.get("historial"), datetime.date.fromisoformat(d["fecha_dato"]), cfg["dias"])
        if not ref or not ref[1]: continue
        pct = (d["valor"] / ref[1] - 1) * 100
        if abs(pct) < cfg["umbral_pct"] - 1e-9: continue
        sube = pct > 0
        cb = dict(barometro.defaults("diesel-gasolina-hibrido-electrico", p, live), kwhCasa=p["kwh_casa_eur"], kwhPublico=p["kwh_publico_eur"], anos=5, km=15000)
        pk = "precioDiesel" if k == "diesel" else "precioGasolina"
        cb["precioDiesel"], cb["precioGasolina"] = D["diesel"]["valor"], D["gasolina95"]["valor"]
        o1 = barometro.coche(cb); o0 = barometro.coche(dict(cb, **{pk: ref[1]}))
        idx = 0 if k == "diesel" else 1
        g1, g0 = o1["energiaKm"][idx] * 15000, o0["energiaKm"][idx] * 15000
        win = barometro.MOTORES[o1["ganador"]][1]
        dato = (f'el {nombre.lower()} está a {E(d["valor"], 3)} €/l de media en España el {seo._fmt_fecha(d["fecha_dato"])}, un {N(abs(pct))} % {"más" if sube else "menos"} '
                f'que el {seo._fmt_fecha(ref[0])} ({E(ref[1], 3)} €/l).')
        efecto = (f'<p>Para un coche de {nombre.lower()} que haga 15.000 km al año, el gasto anual solo en combustible pasa de <strong>{E(g0, 0)} €</strong> a <strong>{E(g1, 0)} €</strong> '
                  f'({E(abs(g1 - g0), 0)} € {"más" if sube else "menos"} al año) con el consumo por defecto de la calculadora.</p>\n'
                  f'<p>Con los precios actuales, la calculadora da como opción más barata a 5 años y 15.000 km al año: <strong>{win}</strong>.</p>')
        src = (f'<p class="note">Dato de {_time(d["fecha_dato"])}. Fuente: {_fuente(d)}. {html.escape(d.get("extra", {}).get("detalle", ""))}. '
               f'Variación frente al dato guardado de hace unos 7 días. Cálculo con <a href="/decidir/diesel-gasolina-hibrido-electrico/">Diésel, gasolina, híbrido o eléctrico</a>.</p>')
        out.append(dict(regla=f"carburante-{k}", clave=f"{k}-{today.isocalendar()[0]}w{today.isocalendar()[1]}", slug=f"{k.replace('95', '')}-{'sube' if sube else 'baja'}-semana",
                        fecha=d["fecha_dato"], calc="diesel-gasolina-hibrido-electrico",
                        title=f'{nombre}: {"sube" if sube else "baja"} un {N(abs(pct))} % en una semana',
                        description=_trim(f'{nombre} a {E(d["valor"], 3)} €/l, un {N(abs(pct))} % {"más" if sube else "menos"} que hace una semana: {E(abs(g1 - g0), 0)} € al año con 15.000 km.', 155),
                        body=_wrap(dato, efecto, "diesel-gasolina-hibrido-electrico", src, today)))
    return out

def r_pvpc(live, params, today):
    l = live.get("datos", {}).get("luz_pvpc"); cfg = RULES["pvpc"]
    if not _fresh(l, today): return []
    x = l.get("extra", {}); m = x.get("media_mes")
    if not m or x.get("dias_mes", 0) < cfg["min_dias_mes"]: return []
    pct = (l["valor"] / m - 1) * 100
    if pct < cfg["umbral_pct"] - 1e-9: return []
    c1, c0 = 10 * l["valor"], 10 * m
    dato = (f'el PVPC medio del {seo._fmt_fecha(l["fecha_dato"])} es de {E(l["valor"], 3)} €/kWh, un {N(pct)} % por encima de la media de lo que va de mes ({E(m, 3)} €/kWh, {x["dias_mes"]} días).')
    efecto = (f'<p>Con 10 kWh de calefacción eléctrica directa, el término de energía de ese día cuesta <strong>{E(c1)} €</strong> frente a {E(c0)} € con el precio medio del mes '
              f'({E(c1 - c0)} € más). Ese día, la hora más barata fue la de las {x["hora_barata"]} h ({E(x["precio_hora_barata"], 3)} €/kWh) y la más cara la de las {x["hora_cara"]} h ({E(x["precio_hora_cara"], 3)} €/kWh).</p>\n'
              f'<p>Una aerotermia necesita unas 3 veces menos electricidad para dar el mismo calor, de ahí que la calculadora compare los tres sistemas.</p>')
    src = (f'<p class="note">Dato de {_time(l["fecha_dato"])}. Fuente: {_fuente(l)}. Solo término de energía del PVPC, sin peajes, cargos ni impuestos. La media del mes incluye el propio día.</p>')
    return [dict(regla="pvpc", clave=f"pvpc-{l['fecha_dato']}", slug="luz-pvpc-por-encima-media", fecha=l["fecha_dato"], calc="calefaccion-gas-aerotermia-electrica",
                 title=f'Luz: el PVPC supera un {N(pct, 0)} % la media del mes',
                 description=_trim(f'PVPC de {E(l["valor"], 3)} €/kWh, un {N(pct)} % sobre la media del mes: 10 kWh de calefacción eléctrica cuestan {E(c1)} € ese día.', 155),
                 body=_wrap(dato, efecto, "calefaccion-gas-aerotermia-electrica", src, today))]

def _clima(live, params, today):
    tm = live.get("datos", {}).get("madrid_tiempo")
    return tm if _fresh(tm, today) else None

def r_frio(live, params, today):
    tm = _clima(live, params, today); cfg = RULES["frio"]
    if not tm or tm["extra"].get("min_semana") is None or tm["extra"]["min_semana"] > cfg["min_c"]: return []
    x = tm["extra"]; p = _mercado(params, live)
    kwh = 10.0; gas = kwh / p["rendimiento_caldera_condensacion"] * p["gas_eur_kwh"]; aero = kwh / p["scop_aerotermia"] * p["electricidad_eur_kwh"]; elec = kwh * p["electricidad_eur_kwh"]
    dato = f'la previsión para Madrid da una mínima de {N(x["min_semana"])} °C en los próximos {x["dias_prevision"]} días (hoy, {N(tm["valor"])} °C).'
    efecto = (f'<p>Para 10 kWh de calor, con los precios de la calculadora (gas {E(p["gas_eur_kwh"], 3)} €/kWh, electricidad {E(p["electricidad_eur_kwh"], 3)} €/kWh), el coste de energía es de '
              f'<strong>{E(gas)} €</strong> con caldera de gas de condensación, <strong>{E(aero)} €</strong> con aerotermia (SCOP {E(p["scop_aerotermia"], 1)}) y <strong>{E(elec)} €</strong> con calefacción eléctrica directa. '
              f'Cuanto más frío, más kWh de calefacción: la diferencia entre sistemas se multiplica.</p>')
    src = f'<p class="note">Dato de {_time(tm["fecha_dato"])}. Fuente: {_fuente(tm)}. Es una previsión, no una observación. Costes: supuestos por defecto de <a href="/decidir/calefaccion-gas-aerotermia-electrica/">la calculadora de calefacción</a>.</p>'
    wk = today.isocalendar()
    return [dict(regla="frio", clave=f"frio-{wk[0]}w{wk[1]}", slug="frio-madrid-prevision", fecha=tm["fecha_dato"], calc="calefaccion-gas-aerotermia-electrica",
                 title=f'Frío en Madrid: mínima prevista de {N(x["min_semana"])} °C',
                 description=_trim(f'Previsión de {N(x["min_semana"])} °C de mínima en Madrid. 10 kWh de calor cuestan {E(gas)} € con gas, {E(aero)} € con aerotermia y {E(elec)} € con electricidad directa.', 155),
                 body=_wrap(dato, efecto, "calefaccion-gas-aerotermia-electrica", src, today))]

def r_calor(live, params, today):
    tm = _clima(live, params, today); cfg = RULES["calor"]
    if not tm or tm["extra"].get("max_semana") is None or tm["extra"]["max_semana"] < cfg["max_c"]: return []
    x = tm["extra"]; p = _mercado(params, live); l = live.get("datos", {}).get("luz_pvpc")
    dato = f'la previsión para Madrid da una máxima de {N(x["max_semana"])} °C en los próximos {x["dias_prevision"]} días (hoy, {N(tm["valor"])} °C).'
    efecto = f'<p>Una hora de aire acondicionado de 1 kW consume 1 kWh: con la electricidad a {E(p["electricidad_eur_kwh"], 3)} €/kWh (supuesto de la calculadora de calefacción, con impuestos) son <strong>{E(p["electricidad_eur_kwh"])} €</strong> por hora de uso a plena potencia.</p>'
    if _fresh(l, today):
        efecto += (f'\n<p>Con tarifa PVPC, el término de energía del {seo._fmt_fecha(l["fecha_dato"])} osciló entre {E(l["extra"]["precio_hora_barata"], 3)} €/kWh ({l["extra"]["hora_barata"]} h) y '
                   f'{E(l["extra"]["precio_hora_cara"], 3)} €/kWh ({l["extra"]["hora_cara"]} h): mover el uso a la hora barata reduce el coste de la misma hora de aire a un {N((1 - l["extra"]["precio_hora_barata"] / l["extra"]["precio_hora_cara"]) * 100, 0)} % menos.</p>')
    efecto += '\n<p>Una aerotermia también enfría: si estás valorando cambiar de sistema, la calculadora compara su coste anual con el del gas y la electricidad directa.</p>'
    src = f'<p class="note">Dato de {_time(tm["fecha_dato"])}. Fuente: {_fuente(tm)}. Es una previsión, no una observación.' + (f' Precios PVPC: {_fuente(l)}.' if _fresh(l, today) else "") + '</p>'
    wk = today.isocalendar()
    return [dict(regla="calor", clave=f"calor-{wk[0]}w{wk[1]}", slug="calor-madrid-prevision", fecha=tm["fecha_dato"], calc="calefaccion-gas-aerotermia-electrica",
                 title=f'Calor en Madrid: máxima prevista de {N(x["max_semana"])} °C',
                 description=_trim(f'Previsión de {N(x["max_semana"])} °C de máxima en Madrid. Una hora de aire acondicionado de 1 kW cuesta {E(p["electricidad_eur_kwh"])} € con la electricidad a {E(p["electricidad_eur_kwh"], 3)} €/kWh.', 155),
                 body=_wrap(dato, efecto, "calefaccion-gas-aerotermia-electrica", src, today))]

REGLAS = [r_euribor, r_carburante, r_pvpc, r_frio, r_calor]

def evaluar(live, params, today):
    out = []
    for fn in REGLAS: out += fn(live, params, today)
    return out


# ---------- escritura idempotente ----------
def existentes(path=OUT):
    res = []
    if os.path.isdir(path):
        for f in os.listdir(path):
            m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", open(os.path.join(path, f)).read(), re.S) if f.endswith(".html") else None
            if m: res.append(json.loads(m.group(1)))
    return res

def escribir(notas, today, path=OUT, dry=False):
    """Escribe las notas nuevas (misma clave => no se repite; cooldown por regla). Devuelve lista de rutas/ids escritos."""
    ex = existentes(path); hechas = []
    for n in notas:
        if any(e.get("clave") == n["clave"] for e in ex): continue
        cd = RULES[n["regla"].split("-")[0]]["cooldown"]
        if any(e.get("regla") == n["regla"] and (today - datetime.date.fromisoformat(e["published"])).days < cd for e in ex): continue
        meta = {"title": n["title"], "h1": n["title"], "description": n["description"], "published": n["fecha"], "calc": n["calc"],
                "regla": n["regla"], "clave": n["clave"]}
        fn = os.path.join(path, f'{n["fecha"]}-{n["slug"]}.html')
        hechas.append(fn)
        if not dry:
            os.makedirs(path, exist_ok=True)
            open(fn, "w").write("<!--meta " + json.dumps(meta, ensure_ascii=False) + " -->\n" + n["body"])
        ex.append(meta)
    return hechas

def main(argv):
    today = datetime.date.today()
    if "--hoy" in argv: today = datetime.date.fromisoformat(argv[argv.index("--hoy") + 1])
    live = seo.load_live(); params = json.load(open(os.path.join(PROJ, "data/params.json")))
    notas = evaluar(live, params, today)
    hechas = escribir(notas, today, dry="--dry" in argv)
    print(f"disparadores activos: {len(notas)}; notas {'(simuladas) ' if '--dry' in argv else ''}nuevas: {len(hechas)}")
    for h in hechas: print(" +", os.path.relpath(h, ROOT))

if __name__ == "__main__":
    main(sys.argv[1:])
