"""Carga de calculadoras (dueño: Constructor).
`default_from` en inputs:
  "params.clave.con.puntos"  -> data/params.json (ya con los datos vivos aplicados por merge_market)
  "live.<id>[.sub.ruta]"     -> data/live.json: datos[<id>].valor, o la subruta (p. ej. live.luz_pvpc.extra.media_mes)
Opciones del input para "live.*": "default_factor" (multiplicador), "default_round" (decimales),
"default_add" (se suma tras el factor, p. ej. Euríbor + diferencial; también al fallback), "default_min_extra" ({campo: mínimo} sobre datos[<id>].extra, p. ej. {"dias_mes": 7}), "default_fallback" ("params.x").
Si falta el dato vivo, no es ok, es viejo (45 días Euríbor, 7 el resto; o `max_edad_dias`) o no cumple el mínimo,
se usa default_fallback (params) y si no, el `default` literal. Nunca rompe el build."""
import json, os, datetime
import ui

LIVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/live.json")
MAX_EDAD = 7
MAX_EDAD_ID = {"euribor12m": 45}
# datos vivos que sustituyen a params (clave de params -> id en live.json, decimales)
LIVE_PARAMS = {"euribor_12m": ("euribor12m", 3), "diesel_eur_l": ("diesel", 3), "gasolina_eur_l": ("gasolina95", 3)}

def _dig(params, path):
    v = params
    for k in path.split("."):
        v = v[k]
    return v

def load_live(path=LIVE_PATH):
    try:
        with open(path) as f: d = json.load(f)
        return d if isinstance(d.get("datos"), dict) else {}
    except Exception:
        return {}

def _fresh(d, today, did=None):
    # ok=false (el último refresco falló) no descarta el dato mientras siga dentro de su edad máxima (igual que datos.py `_live`)
    if not isinstance(d, dict) or not isinstance(d.get("valor"), (int, float)) or not d.get("fecha_dato"):
        return False
    try: f = datetime.date.fromisoformat(d["fecha_dato"])
    except ValueError: return False
    return -1 <= (today - f).days <= d.get("max_edad_dias", MAX_EDAD_ID.get(did, MAX_EDAD))

def live_value(live, ref, i=None, today=None):
    """(valor, fecha_dato, fuente) del dato vivo `live.<id>[.sub]` si es utilizable; None si no."""
    today = today or datetime.date.today()
    try:
        parts = ref[len("live."):].split(".")
        d = (live or {}).get("datos", {}).get(parts[0])
        if not _fresh(d, today, parts[0]): return None
        i = i or {}
        for k, mn in (i.get("default_min_extra") or {}).items():
            if (d.get("extra") or {}).get(k, 0) < mn: return None
        v = d["valor"] if len(parts) == 1 else _dig(d, ".".join(parts[1:]))
        if not isinstance(v, (int, float)): return None
        v = v * i.get("default_factor", 1) + i.get("default_add", 0)
        if "default_round" in i: v = round(v, i["default_round"])
        return v, d["fecha_dato"], d.get("fuente") or {}
    except Exception:
        return None

def merge_market(params, live=None, today=None):
    """Copia de params con euribor_12m, diesel_eur_l y gasolina_eur_l del dato vivo si está fresco (si no, el de params).
    Añade fecha_euribor, fecha_combustibles, euribor_fuente, combustibles_fuente y mercado_vivo (qué claves son vivas)."""
    live = load_live() if live is None else live
    p = dict(params); vivo = []
    for k, (did, dec) in LIVE_PARAMS.items():
        r = live_value(live, "live." + did, today=today)
        if r:
            p[k] = round(r[0], dec); vivo.append(k)
            if k == "euribor_12m":
                p["fecha_euribor"] = r[1]; p["euribor_fuente"] = r[2].get("nombre", "")
                p["periodo_euribor"] = (live["datos"]["euribor12m"].get("extra") or {}).get("periodo", "")
            elif k == "diesel_eur_l":
                p["fecha_combustibles"] = r[1]; p["combustibles_fuente"] = r[2].get("nombre", "")
    p.setdefault("fecha_euribor", params.get("fecha", ""))
    p["mercado_vivo"] = vivo
    return p

def resolve_default(i, params, live=None, today=None):
    """Valor por defecto de un input (aplica default_from)."""
    ref = i.get("default_from")
    if not ref: return i.get("default")
    if ref.startswith("live."):
        r = live_value(live, ref, i, today)
        if r: return r[0]
        fb = i.get("default_fallback")
        if fb:
            try:
                v = _dig(params, fb[len("params."):] if fb.startswith("params.") else fb)
                if "default_add" in i and isinstance(v, (int, float)): v = v + i["default_add"]
                if "default_round" in i and isinstance(v, (int, float)): v = round(v, i["default_round"])
                return v
            except Exception: pass
        return i.get("default")
    try:
        return _dig(params, ref[len("params."):] if ref.startswith("params.") else ref)
    except Exception:
        return i.get("default")

MAX_EDAD_RESPALDO = 45  # días: un valor de respaldo de params más antiguo lleva aviso visible

def _fecha_respaldo(fb, params):
    """Fecha (date) del valor de respaldo `fb` de params, o None si no se puede saber."""
    k = fb[len("params."):] if fb.startswith("params.") else fb
    cand = {"euribor_12m": ["fecha_euribor"], "tipo_hipoteca_fija_medio": ["tipo_hipoteca_fija_periodo"],
            "diesel_eur_l": ["fecha_combustibles"], "gasolina_eur_l": ["fecha_combustibles"]}.get(k, []) + ["fecha"]
    for c in cand:
        v = params.get(c)
        if not v: continue
        try:
            if len(v) == 7:  # AAAA-MM -> último día del mes
                y, m = int(v[:4]), int(v[5:])
                return (datetime.date(y + m // 12, m % 12 + 1, 1) - datetime.timedelta(days=1))
            return datetime.date.fromisoformat(v)
        except ValueError: continue
    return None

def aviso_respaldo(i, params, live=None, today=None):
    """Texto de aviso si el default de `i` sale del respaldo de params y ese valor es antiguo (o no tiene fecha); '' si no."""
    ref, fb = i.get("default_from") or "", i.get("default_fallback")
    if not fb or not ref.startswith("live.") or live_value(live, ref, i, today): return ""
    today = today or datetime.date.today()
    f = _fecha_respaldo(fb, params)
    nom = i.get("label", i.get("id", "")).split(" (")[0]
    if f is None: return f"«{nom}»: el valor por defecto es de respaldo y no tiene fecha; compruébalo y cámbialo por el de tu oferta."
    if (today - f).days > MAX_EDAD_RESPALDO:
        return f"«{nom}»: el dato actualizado no está disponible y el valor por defecto es de respaldo, fechado el {f.strftime('%d/%m/%Y')}; puede estar desfasado, cámbialo por el de tu oferta."
    return ""

def load_calcs(root, params):
    calcs = []
    cdir = os.path.join(root, "calcs")
    live = load_live(os.path.join(root, "data/live.json"))
    params = merge_market(params, live)
    for f in sorted(os.listdir(cdir)):
        if f.endswith(".json") and not f.endswith(".test.json"):
            c = json.load(open(os.path.join(cdir, f)))
            c["js"] = open(os.path.join(cdir, c["slug"] + ".js")).read()
            c["content"] = open(os.path.join(root, "content", c["slug"] + ".html")).read()
            c.setdefault("tema", ui.tema(c))
            for i in c["inputs"]:
                if i.get("default_from"):
                    i["default"] = resolve_default(i, params, live)
                    av = aviso_respaldo(i, params, live)
                    if av: c["sources"] = c.get("sources", "") + " Aviso: " + av
            calcs.append(c)
    return calcs
