#!/usr/bin/env python3
"""Oraculo independiente del Verificador (2026-10-02) para calcs/luz-fija-o-indexada.js.
Norma: peajes 2.0TD (BOE-A-2025-26348) + cargos (BOE-A-2025-26705) potencia; IEE Ley 38/1992 art. 99 (5,11269632 %, minimo 1 EUR/MWh);
IVA 21 % (octubre 2026; RDL 25/2026 arts. 18-21 solo nov/dic condicionados). Factores por periodo recalculados de REData (8.760 h).
Uso: python3 ops/verif/luz-fija-o-indexada.py   (compara con el JS via osascript, tol 1 EUR)"""
import json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POT = 23.324952 + 0.443770 + 4.379461 + 0.281653      # EUR/kW y ano, P1 + P2 con la misma potencia
CCF = 3.113                                             # margen comercializacion fijo PVPC (Orden ETU/1948/2016 anexo II) -- NO en el JS actual
IEE, IEEMIN, IVA = 0.0511269632, 0.001, 0.21
F = {"P": 1.4366052, "L": 0.9336461, "V": 0.8374197}   # REData oct-2025..sep-2026, Circular 3/2020
M12 = 0.14252844
def factura(base, kwh):                                 # IEE sobre potencia+energia, con cuota minima; IVA sobre base+IEE
    return (base + max(IEE * base, IEEMIN * kwh)) * (1 + IVA)
def pvpc(d, media, ccf=0.0):
    v = 100 - d["pctPunta"] - d["pctLlano"]
    e = d["consumo"] * media * (d["pctPunta"] * F["P"] + d["pctLlano"] * F["L"] + v * F["V"]) / 100
    return factura(d["potencia"] * (POT + ccf) + e, d["consumo"])
def fija(d, pf=None):
    pf = d["precioFijo"] if pf is None else pf
    return factura(d["potencia"] * d["potFija"] * 365 + d["consumo"] * pf, d["consumo"])
def ref(d, ccf=0.0):
    media = d["pvpc"] * (1 + d["hip"] / 100); cf, cp = fija(d), pvpc(d, media, ccf)
    eq = -1
    if d["consumo"] > 0:   # forma cerrada con el IEE porcentual (el minimo no rige si el precio > ~0,0196 EUR/kWh)
        x = (cp / ((1 + IEE) * (1 + IVA)) - d["potencia"] * d["potFija"] * 365) / d["consumo"]
        if x >= 0: eq = x * 1000
    return {"costeFija": cf, "costePvpc": cp, "diferencia": cf - cp, "difMedia12": cf - pvpc(d, M12, ccf),
            "difMas10": cf - pvpc(d, d["pvpc"] * 1.1, ccf), "equilibrioMwh": eq}
B = dict(consumo=3000, potencia=4.6, pctPunta=30, pctLlano=30, precioFijo=0.15, potFija=0.0779, pvpc=0.184, hip=0)
S = [("1 defecto", {}), ("2 consumo 0", dict(consumo=0)),
     ("3 3,45 kW 2.000 kWh", dict(potencia=3.45, consumo=2000, pctPunta=25, pctLlano=35, precioFijo=0.13, potFija=0.09)),
     ("4 5,75 kW muy punta 50/30/20", dict(potencia=5.75, consumo=4500, pctPunta=50, pctLlano=30, precioFijo=0.16)),
     ("5 muy valle 10/10/80, -10 %", dict(pctPunta=10, pctLlano=10, hip=-10)),
     ("6 PVPC gana (media 12m)", dict(pvpc=0.1425, pctPunta=15, pctLlano=25, precioFijo=0.16)),
     ("7 fija gana (0,11, +10 %)", dict(precioFijo=0.11, hip=10)),
     ("8 fija = equilibrio", dict(precioFijo=0.192458)),
     ("9 minimo IEE (base 0)", dict(precioFijo=0, potFija=0))]
if __name__ == "__main__":
    js = open(os.path.join(ROOT, "projects/decidir/calcs/luz-fija-o-indexada.js")).read().split("function eur(")[0]
    ins = [dict(B, **o) for _, o in S]
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", js + "\nJSON.stringify(%s.map(calcular));" % json.dumps(ins)],
                         capture_output=True, text=True)
    R = json.loads(out.stdout)
    usa = CCF if 'ccf' in js else 0.0   # cuando el Constructor anada el CCF, el oraculo compara con el
    bad = 0
    print("escenario | JS fija | JS PVPC | Py fija | Py PVPC | dif JS | dif Py | eq JS | eq Py | PVPC+CCF | dif+CCF | difMedia12 +CCF")
    for (n, _), d, r in zip(S, ins, R):
        p, q = ref(d, usa), ref(d, CCF)
        ok = all(abs(r[k] - p[k]) <= 1 for k in ("costeFija", "costePvpc", "diferencia", "difMedia12", "difMas10", "equilibrioMwh"))
        bad += not ok
        print(f"{n} | {r['costeFija']:.2f} | {r['costePvpc']:.2f} | {p['costeFija']:.2f} | {p['costePvpc']:.2f} | {r['diferencia']:.2f} | {p['diferencia']:.2f} | "
              f"{r['equilibrioMwh']:.2f} | {p['equilibrioMwh']:.2f} | {q['costePvpc']:.2f} | {q['diferencia']:.2f} | {q['difMedia12']:.2f} | {'OK' if ok else 'FALLO'}")
    print("discrepancias JS vs Python (CCF=%s):" % usa, bad)
