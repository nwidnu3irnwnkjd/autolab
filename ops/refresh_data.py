#!/usr/bin/env python3
"""Datos vivos de entremuchos.com -> projects/decidir/data/live.json (dueño: Estratega SEO/GEO). Solo stdlib.

Fuentes públicas SIN clave (probadas 2026-10-02):
  luz_pvpc    REE apidatos (PVPC por hora, EUR/MWh -> EUR/kWh)
  diesel / gasolina95   Geoportal MITECO (media simple de estaciones, Península y Baleares)
  euribor12m  BCE Data Portal (Euríbor 12 m, media mensual)
  madrid_tiempo  Open-Meteo (CC BY 4.0)
Tolerante a fallos: si una fuente falla se conserva el dato anterior con ok:false y motivo.
Uso: python3 ops/refresh_data.py [--out ruta] [--dry]
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse, statistics, calendar

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "projects/decidir/data/live.json")
UA = "entremuchos-refresh/1.0 (+https://entremuchos.com)"
SCHEMA = 1


def http_json(url, timeout=60, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last = e; time.sleep(2 + 3 * i)
    raise RuntimeError(f"{type(last).__name__}: {last}")


def http_text(url, timeout=60, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            last = e; time.sleep(2 + 3 * i)
    raise RuntimeError(f"{type(last).__name__}: {last}")


def num_es(s):
    return float(s.replace(",", ".")) if s and s.strip() else None


# ---------- fuentes ----------
def fetch_luz(today):
    base = "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real?start_date=%s&end_date=%s&time_trunc=hour"
    first = today.replace(day=1)
    prev_first = (first - datetime.timedelta(days=1)).replace(day=1)
    tomorrow = today + datetime.timedelta(days=1)
    rows = {}
    spans = [(prev_first, first - datetime.timedelta(days=1)), (first, tomorrow)]
    for a, b in spans:
        d = http_json(base % (a.isoformat() + "T00:00", b.isoformat() + "T23:59"))
        pv = [i for i in d.get("included", []) if i.get("type") == "PVPC"]
        if not pv: raise RuntimeError("respuesta sin serie PVPC")
        for v in pv[0]["attributes"]["values"]:
            rows[v["datetime"]] = v["value"] / 1000.0  # EUR/MWh -> EUR/kWh
    days = {}
    for k, v in rows.items():
        days.setdefault(k[:10], []).append((k[11:13], v))
    full = sorted(d for d, l in days.items() if len(l) >= 23)
    if not full: raise RuntimeError("sin ningún día completo")
    day = full[-1]
    avg = lambda l: sum(v for _, v in l) / len(l)
    cur = days[day]
    cheapest = min(cur, key=lambda x: x[1]); dearest = max(cur, key=lambda x: x[1])
    ym = day[:7]
    mes = [v for d in full if d[:7] == ym for _, v in days[d]]
    prevs = [d for d in full if d < day]
    ayer = round(avg(days[prevs[-1]]), 5) if prevs else None
    if not (0.0 < avg(cur) < 1.5): raise RuntimeError(f"valor implausible {avg(cur)}")
    return {
        "valor": round(avg(cur), 5), "unidad": "€/kWh", "fecha_dato": day,
        "anterior": ayer, "anterior_fecha": prevs[-1] if prevs else None,
        "extra": {"media_mes": round(sum(mes) / len(mes), 5), "mes": ym, "dias_mes": len([d for d in full if d[:7] == ym]),
                  "hora_barata": int(cheapest[0]), "precio_hora_barata": round(cheapest[1], 5),
                  "hora_cara": int(dearest[0]), "precio_hora_cara": round(dearest[1], 5),
                  "detalle": "PVPC (precio de la energía por hora), media de las 24 horas del día"},
        "fuente": {"nombre": "Red Eléctrica de España (REData)", "url": "https://www.ree.es/es/datos/mercados/precios-mercados-tiempo-real"},
    }


_carb_cache = {}
def _carburantes():
    if _carb_cache: return _carb_cache
    d = http_json("https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/", timeout=120)
    fecha = datetime.datetime.strptime(d["Fecha"].split()[0], "%d/%m/%Y").date().isoformat()
    L = [x for x in d["ListaEESSPrecio"] if x.get("IDCCAA") not in ("05", "18", "19")]  # sin Canarias, Ceuta y Melilla (otra fiscalidad)
    if len(L) < 5000: raise RuntimeError(f"solo {len(L)} estaciones")
    out = {"fecha": fecha, "n": len(L)}
    for k, campo in (("diesel", "Precio Gasoleo A"), ("gasolina95", "Precio Gasolina 95 E5")):
        vals = [p for p in (num_es(x.get(campo, "")) for x in L) if p and 0.5 < p < 4]
        if len(vals) < 3000: raise RuntimeError(f"{campo}: solo {len(vals)} precios")
        out[k] = (round(statistics.mean(vals), 4), len(vals))
    _carb_cache.update(out); return out

def fetch_carb(clave):
    c = _carburantes(); v, n = c[clave]
    nombre = "Gasóleo A (diésel)" if clave == "diesel" else "Gasolina 95 E5"
    return {"valor": v, "unidad": "€/l", "fecha_dato": c["fecha"],
            "extra": {"detalle": f"Media simple de {n} estaciones de servicio de la Península y Baleares (excluye Canarias, Ceuta y Melilla), {nombre}"},
            "fuente": {"nombre": "Geoportal de gasolineras, Ministerio para la Transición Ecológica (MITECO)", "url": "https://geoportalgasolineras.es/"}}


def fetch_euribor(today):
    url = "https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA?lastNObservations=3&format=csvdata"
    lines = http_text(url).strip().splitlines()
    head = lines[0].split(","); it, iv = head.index("TIME_PERIOD"), head.index("OBS_VALUE")
    obs = sorted((r.split(",")[it], float(r.split(",")[iv])) for r in lines[1:] if r.strip())
    if len(obs) < 2: raise RuntimeError("menos de 2 observaciones")
    (pm, pv), (m, v) = obs[-2], obs[-1]
    y, mo = map(int, m.split("-"))
    fin = datetime.date(y, mo, calendar.monthrange(y, mo)[1]).isoformat()
    if not (-1 < v < 10): raise RuntimeError(f"valor implausible {v}")
    return {"valor": round(v, 3), "unidad": "%", "fecha_dato": fin, "max_edad_dias": 45,
            "anterior": round(pv, 3), "anterior_fecha": pm,
            "extra": {"periodo": m, "periodo_anterior": pm, "detalle": "Euríbor a 12 meses, media mensual"},
            "fuente": {"nombre": "Banco Central Europeo (Data Portal, serie Euribor 1 año, vía Refinitiv)", "url": "https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA"}}


def fetch_tiempo():
    q = urllib.parse.urlencode({"latitude": 40.4168, "longitude": -3.7038, "current": "temperature_2m",
                                "daily": "temperature_2m_min,temperature_2m_max", "timezone": "Europe/Madrid", "forecast_days": 7})
    d = http_json("https://api.open-meteo.com/v1/forecast?" + q)
    t = d["current"]["temperature_2m"]; dd = d["daily"]
    mins, maxs = dd["temperature_2m_min"], dd["temperature_2m_max"]
    if not (-30 < t < 55): raise RuntimeError(f"temperatura implausible {t}")
    return {"valor": t, "unidad": "°C", "fecha_dato": d["current"]["time"][:10],
            "extra": {"min_hoy": mins[0], "max_hoy": maxs[0], "min_semana": min(mins), "max_semana": max(maxs),
                      "dias_prevision": len(mins), "ciudad": "Madrid",
                      "detalle": "Temperatura actual en Madrid y previsión de los próximos 7 días"},
            "fuente": {"nombre": "Open-Meteo (CC BY 4.0)", "url": "https://open-meteo.com/"}}


# ---------- orquestación ----------
def build_fetchers(today):
    return {
        "luz_pvpc": lambda: fetch_luz(today),
        "diesel": lambda: fetch_carb("diesel"),
        "gasolina95": lambda: fetch_carb("gasolina95"),
        "euribor12m": lambda: fetch_euribor(today),
        "madrid_tiempo": fetch_tiempo,
    }


def merge(old, new, today_iso):
    """Combina un dato nuevo con el guardado: calcula la variación frente al valor anterior."""
    e = dict(new)
    prev_v, prev_f = new.get("anterior"), new.get("anterior_fecha")
    if prev_v is None and old and old.get("valor") is not None:
        if old.get("fecha_dato") != new["fecha_dato"]:  # dato distinto: el guardado pasa a ser el anterior
            prev_v, prev_f = old["valor"], old.get("fecha_dato")
        else:  # mismo dato (re-ejecución): conserva el anterior que ya había
            prev_v, prev_f = old.get("anterior"), old.get("anterior_fecha")
    if prev_v is not None:
        e["anterior"], e["anterior_fecha"] = prev_v, prev_f
        e["variacion_abs"] = round(new["valor"] - prev_v, 5)
        e["variacion_pct"] = round((new["valor"] / prev_v - 1) * 100, 2) if prev_v else None
    else:
        for k in ("anterior", "anterior_fecha", "variacion_abs", "variacion_pct"): e.pop(k, None)
    e.update(ok=True, fecha_consulta=today_iso); e.pop("motivo", None)
    return e


def run(path=OUT, fetchers=None, today=None):
    today = today or datetime.date.today()
    old = {}
    if os.path.exists(path):
        try: old = json.load(open(path)).get("datos", {})
        except Exception: old = {}
    fetchers = fetchers or build_fetchers(today)
    datos, fallos = {}, []
    for k, fn in fetchers.items():
        try:
            datos[k] = merge(old.get(k), fn(), today.isoformat())
        except Exception as ex:
            fallos.append(k)
            prev = dict(old.get(k) or {"valor": None})
            prev.update(ok=False, motivo=str(ex)[:300], fecha_consulta=today.isoformat())
            datos[k] = prev
            print(f"AVISO {k}: {ex}", file=sys.stderr)
    return {"esquema": SCHEMA, "generado": today.isoformat(),
            "nota": "Datos públicos sin clave; cada dato lleva su fecha y fuente. Generado por ops/refresh_data.py", "datos": datos}, fallos


if __name__ == "__main__":
    out = OUT
    if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]
    res, fallos = run(out)
    txt = json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if "--dry" in sys.argv: print(txt)
    else:
        os.makedirs(os.path.dirname(out), exist_ok=True); open(out, "w").write(txt)
        print(f"live.json escrito ({len(res['datos']) - len(fallos)} ok, {len(fallos)} con fallo: {', '.join(fallos) or '-'})")
    sys.exit(0 if len(fallos) < len(res["datos"]) else 1)  # solo falla si no se obtuvo NADA
