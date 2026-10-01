#!/usr/bin/env python3
"""Pruebas ligeras del Pulso y de live.json. Sin red. Uso: python3 ops/check_live.py
Valida: esquema de data/live.json (si existe), y el comportamiento de seo.pulso_html con datos de ejemplo
(fresco / viejo / ausente / fallo conservado)."""
import json, os, sys, datetime, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "projects/decidir")); sys.path.insert(0, os.path.join(ROOT, "ops"))
import seo, refresh_data

fails = []
def ok(c, m):
    if not c: fails.append(m)

REQ = ("valor", "unidad", "fecha_dato", "fecha_consulta", "fuente", "ok")
def schema(live, name):
    ok(live.get("esquema") == 1 and isinstance(live.get("datos"), dict), f"{name}: esquema")
    for k, d in live.get("datos", {}).items():
        for f in REQ: ok(f in d, f"{name}.{k}: falta {f}")
        ok(isinstance(d.get("fuente"), dict) and d["fuente"].get("url", "").startswith("https://") and d["fuente"].get("nombre"), f"{name}.{k}: fuente")
        if d.get("ok") is False: ok(d.get("motivo"), f"{name}.{k}: ok:false sin motivo")
        if d.get("valor") is not None: ok(isinstance(d["valor"], (int, float)), f"{name}.{k}: valor no numérico")
        if d.get("fecha_dato"): datetime.date.fromisoformat(d["fecha_dato"])

TODAY = datetime.date(2026, 10, 2)
def mk(valor, fecha, unidad, **kw):
    d = dict(valor=valor, unidad=unidad, fecha_dato=fecha, fecha_consulta="2026-10-02", ok=True,
             fuente={"nombre": "Fuente", "url": "https://example.org/"}); d.update(kw); return d
SAMPLE = {"esquema": 1, "datos": {
    "luz_pvpc": mk(0.2, "2026-10-02", "€/kWh", variacion_pct=-5.0, extra=dict(hora_barata=14, hora_cara=20, precio_hora_barata=0.1, precio_hora_cara=0.3)),
    "diesel": mk(1.9, "2026-10-02", "€/l"), "gasolina95": mk(1.8, "2026-10-02", "€/l"),
    "euribor12m": mk(3.2, "2026-09-30", "%", max_edad_dias=45, variacion_abs=-0.1, anterior_fecha="2026-08", extra=dict(periodo="2026-09")),
    "madrid_tiempo": mk(15.0, "2026-10-02", "°C", extra=dict(min_semana=8.0, dias_prevision=7))}}
schema(SAMPLE, "muestra")

h = seo.pulso_html(SAMPLE, None, TODAY)
ok(h.startswith('<aside class="pulso') and "<time datetime=" in h and h.count("<li ") == 3, "home: 3 datos con <time>")
ok("5,0 % menos que ayer" in h and "0,10 puntos menos" in h, "textos calculados")
ok("Open-Meteo" not in h, "home sin tiempo")
ok("<time" in seo.pulso_html(SAMPLE, "calefaccion-gas-aerotermia-electrica", TODAY) and "Open-Meteo" in seo.pulso_html(SAMPLE, "calefaccion-gas-aerotermia-electrica", TODAY), "calefacción: luz + tiempo")
ok(seo.pulso_html(SAMPLE, "alquilar-o-comprar", TODAY) == "", "calculadora no afín: vacío")
# datos viejos: nunca se muestran
old = json.loads(json.dumps(SAMPLE)); old["datos"]["luz_pvpc"]["fecha_dato"] = "2026-09-20"
ok("La luz" not in seo.pulso_html(old, None, TODAY), "luz > 7 días oculta")
ok("A 12 meses" in seo.pulso_html(old, None, TODAY), "euríbor mensual aún vigente")
ok(seo.pulso_html({}, None, TODAY) == "", "sin live.json: vacío")
ok(seo.live_date("/", SAMPLE, TODAY) == "2026-10-02", "live_date")
# fallo conservado: ok:false con valor anterior
with tempfile.TemporaryDirectory() as t:
    p = os.path.join(t, "live.json"); json.dump(SAMPLE, open(p, "w"))
    def boom(): raise RuntimeError("caída simulada")
    res, fallos = refresh_data.run(p, {"diesel": boom, "luz_pvpc": lambda: {"valor": 0.25, "unidad": "€/kWh", "fecha_dato": "2026-10-03", "fuente": {"nombre": "x", "url": "https://x.org"}}}, today=datetime.date(2026, 10, 3))
    ok(fallos == ["diesel"], "fallo detectado")
    d = res["datos"]["diesel"]; ok(d["ok"] is False and d["valor"] == 1.9 and "caída" in d["motivo"], "diesel conserva valor + motivo")
    l = res["datos"]["luz_pvpc"]; ok(l["anterior"] == 0.2 and abs(l["variacion_pct"] - 25.0) < 0.01, "variación frente al guardado")
    schema(res, "run")
if os.path.exists(os.path.join(ROOT, "projects/decidir/data/live.json")):
    schema(json.load(open(os.path.join(ROOT, "projects/decidir/data/live.json"))), "live.json")

# ---- Disparadores (ops/triggers.py): casos que activan y que no activan cada regla, sin red ----
import triggers
PARAMS = json.load(open(os.path.join(ROOT, "projects/decidir/data/params.json")))
def ev(live, today=TODAY): return {n["regla"]: n for n in triggers.evaluar(live, PARAMS, today)}
def mod(**cambios):
    l = json.loads(json.dumps(SAMPLE))
    for ruta, val in cambios.items():
        k, campo = ruta.split("__"); d = l["datos"][k]
        if campo.startswith("extra_"): d["extra"][campo[6:]] = val
        else: d[campo] = val
    return l
W = [["2026-09-25", 1.8], ["2026-09-30", 1.85]]
ok(ev(mod(euribor12m__variacion_abs=0.15, euribor12m__anterior=3.05)).get("euribor"), "euribor: +0,15 activa")
ok(ev(mod(euribor12m__variacion_abs=-0.2, euribor12m__anterior=3.4)).get("euribor"), "euribor: -0,20 activa")
ok("euribor" not in ev(mod(euribor12m__variacion_abs=0.14, euribor12m__anterior=3.06)), "euribor: 0,14 no activa")
ok("euribor" not in ev(SAMPLE), "euribor: muestra (-0,1) no activa")
ok("euribor" in ev(mod(euribor12m__variacion_abs=0.3, euribor12m__anterior=2.9)) and "euribor" not in ev(mod(euribor12m__variacion_abs=0.3, euribor12m__anterior=2.9, euribor12m__fecha_dato="2026-06-30")), "euribor: dato viejo no activa")
hist = lambda v: [["2026-09-25", v], ["2026-10-02", 1.9]]
ok(ev(mod(diesel__historial=hist(1.8))).get("carburante-diesel"), "diésel: +5,6 % semanal activa")
ok("carburante-diesel" not in ev(mod(diesel__historial=hist(1.87))), "diésel: +1,6 % no activa")
ok("carburante-diesel" not in ev(SAMPLE), "diésel: sin historial no activa")
ok(ev(mod(gasolina95__historial=[["2026-09-25", 1.9], ["2026-10-02", 1.8]])).get("carburante-gasolina95"), "gasolina: -5,3 % activa")
ok("-" in (ev(mod(diesel__historial=hist(1.8)))["carburante-diesel"]["body"]) and "15.000 km" in ev(mod(diesel__historial=hist(1.8)))["carburante-diesel"]["body"], "diésel: el efecto usa el cálculo de la calculadora")
ok(ev(mod(luz_pvpc__valor=0.23, luz_pvpc__extra_media_mes=0.2, luz_pvpc__extra_dias_mes=10)).get("pvpc"), "pvpc: +15 % activa")
ok("pvpc" not in ev(mod(luz_pvpc__valor=0.22, luz_pvpc__extra_media_mes=0.2, luz_pvpc__extra_dias_mes=10)), "pvpc: +10 % no activa")
ok("pvpc" not in ev(mod(luz_pvpc__valor=0.3, luz_pvpc__extra_media_mes=0.2, luz_pvpc__extra_dias_mes=3)), "pvpc: < 7 días del mes no activa")
ok(ev(mod(madrid_tiempo__extra_min_semana=3.0)).get("frio"), "frío: 3 °C activa")
ok("frio" not in ev(mod(madrid_tiempo__extra_min_semana=3.5)), "frío: 3,5 °C no activa")
ok(ev(mod(madrid_tiempo__extra_max_semana=36.0)).get("calor"), "calor: 36 °C activa")
ok("calor" not in ev(mod(madrid_tiempo__extra_max_semana=35.0)), "calor: 35 °C no activa")
ok(not triggers.evaluar({}, PARAMS, TODAY), "sin live.json no hay notas")
# escritura idempotente + cooldown
with tempfile.TemporaryDirectory() as t:
    n = triggers.evaluar(mod(euribor12m__variacion_abs=0.3, euribor12m__anterior=2.9), PARAMS, TODAY)
    ok(len(triggers.escribir(n, TODAY, t)) == 1 and len(os.listdir(t)) == 1, "escribe la nota una vez")
    ok(len(triggers.escribir(n, TODAY, t)) == 0, "no repite la misma clave")
    nota = open(os.path.join(t, os.listdir(t)[0])).read()
    ok("<time datetime=" in nota and "Fuente:" in nota and "/decidir/hipoteca-fija-o-variable/" in nota, "nota: time + fuente + enlace a la calculadora")
# ---- Calendario (seo.eventos_activos) ----
D = datetime.date
act = lambda f: {r["evento"]["id"] for r in seo.eventos_activos(f)}
ok("tur-gas-trimestral" in act(D(2026, 10, 2)) and "euribor-mensual" in act(D(2026, 10, 2)), "oct-2026: TUR y Euríbor activos")
ok("cambio-hora-octubre" in act(D(2026, 10, 15)) and "cambio-hora-octubre" not in act(D(2026, 10, 5)), "cambio de hora: ventana 14 días antes")
ok("black-friday" in act(D(2026, 11, 20)) and "black-friday" not in act(D(2026, 12, 5)), "Black Friday 27-nov-2026")
ok("campana-renta" in act(D(2027, 5, 10)) and "campana-renta" not in act(D(2026, 10, 2)), "Renta: abril-junio")
ok("tur-gas-trimestral" in act(D(2026, 12, 28)), "TUR enero 2027: ventana previa")
ok(seo.eventos_activos(D(2026, 8, 15), []) == [], "sin eventos no hay banner")
ok(not seo.ahora_html("alquilar-o-comprar", D(2026, 10, 2)), "banner solo en calculadora afín")
ok(seo.ahora_html(None, D(2026, 10, 2)).count("<p ") == 1 and "Ahora:" in seo.ahora_html(None, D(2026, 10, 2)), "home: 1 banner Ahora")
evs = json.load(open(os.path.join(ROOT, "projects/decidir/data/events.json")))["eventos"]
ok(0 < len(evs) <= 10 and all(e.get("fuente", {}).get("url", "").startswith("https://") and e.get("aviso") for e in evs), "events.json: <= 10, todos con fuente y aviso")
print("FALLOS:\n- " + "\n- ".join(fails) if fails else "OK check_live: Pulso + live.json")
sys.exit(1 if fails else 0)
