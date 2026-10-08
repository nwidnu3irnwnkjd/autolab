#!/usr/bin/env python3
"""Regenera journal/paquete-datos/csv/*.csv SOLO desde projects/decidir/data/live.json y params.json (stdlib).
Uso: python3 ops/gen_paquete_datos.py   (y luego zip del contenido de journal/paquete-datos/)"""
import csv, json, os, zipfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, "projects/decidir/data"); O = os.path.join(R, "journal/paquete-datos")
live = json.load(open(f"{D}/live.json"))["datos"]; par = json.load(open(f"{D}/params.json"))
os.makedirs(f"{O}/csv", exist_ok=True)
def w(name, rows):
    with open(f"{O}/csv/{name}", "w", newline="", encoding="utf-8") as f:
        c = csv.writer(f); c.writerow(["fecha", "valor", "unidad", "fuente", "url_fuente"]); c.writerows(rows)
    print(name, len(rows), "filas")
def serie(key, name, pts):
    d = live[key]; w(name, [[f, v, d["unidad"], d["fuente"]["nombre"], d["fuente"]["url"]] for f, v in pts])
serie("euribor12m", "euribor_12m_mensual.csv", live["euribor12m"]["extra"]["serie_mensual"])
serie("tipo_hipoteca_fija", "tipo_hipoteca_vivienda_nuevas_operaciones_mensual.csv", live["tipo_hipoteca_fija"]["extra"]["serie_mensual"])
serie("gasolina95", "gasolina95_media_diaria.csv", live["gasolina95"]["historial"])
serie("diesel", "diesel_media_diaria.csv", live["diesel"]["historial"])
serie("luz_pvpc", "pvpc_media_diaria.csv", live["luz_pvpc"]["historial"])
r = par["renta_alquiler_2026"]
w("irav_ipc_alquiler.csv", [
    [r["irav_periodo"], r["irav_pct"], "%", "INE, IRAV (publicado " + r["irav_publicado"] + ")", r["url_irav"]],
    [r["irav_periodo"], r["ipc_pct"], "%", "INE, IPC tasa anual, índice definitivo", r["url_ipc"]]])
