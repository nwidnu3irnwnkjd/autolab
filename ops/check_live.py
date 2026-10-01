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
ok(h.startswith('<aside class="pulso') and "<time datetime=" in h and h.count("<li>") == 3, "home: 3 datos con <time>")
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
print("FALLOS:\n- " + "\n- ".join(fails) if fails else "OK check_live: Pulso + live.json")
sys.exit(1 if fails else 0)
