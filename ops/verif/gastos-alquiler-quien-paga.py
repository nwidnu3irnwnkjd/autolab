#!/usr/bin/env python3
"""Verificador fiscal c58 · gastos-alquiler-quien-paga. Casos propios sobre el JS (re-verificacion Sonnet: solo ejecutar).
Lectura del Verificador (LAU consolidada 2/10/2026):
- 20.2: dentro de los 5/7 primeros anos de VIGENCIA (art. 9.1: desde la fecha del contrato o la entrega, prorrogas incluidas) la SUMA no tributaria
  (comunidad + seguro u otros gastos generales no tributarios) solo sube POR ACUERDO (clausula de revision en el pacto = acuerdo anticipado) y nunca > 2 x s.
  Sin acuerdo ni clausula -> no sube (pctLegal 0). Clausula automatica por encima del tope: nula en el exceso (art. 6).
- s = % en que PUEDE subir la renta por art. 18.1 + DA 11.a (IRAV) segun la clausula del contrato; sin clausula de actualizacion s = 0.
- Fuera de 5/7 anos: manda el pacto (se admite lo pedido). Honorarios: pago unico, del arrendador.
Requiere input nuevo d.acuerdo in {"si","no"} (default "si"). Mientras el JS no lo tenga, los casos A* fallan (esperado)."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/gastos-alquiler-quien-paga.js")
def model(d):
    ok = d["pacto"] == "ok"; lim = ok and d["tramo"] == "dentro"; tope = max(0.0, 2 * d["subidaRenta"])
    pct = (0.0 if d.get("acuerdo", "si") == "no" else min(d["subidaPedida"], tope)) if lim else d["subidaPedida"]
    comLey = d["comunidad"] * (1 + pct / 100) if ok else 0.0
    ped = d["comunidad"] * (1 + d["subidaPedida"] / 100) + d["ibi"] + d["basuras"] + d["honorarios"]
    ley = comLey + ((d["ibi"] + d["basuras"]) if ok else 0.0)
    return dict(topePct=tope, pctLegal=pct if ok else 0.0, comunidadLegal=comLey, pedido=ped, tuCargo=ley, rechazable=ped - ley)
B = dict(pacto="ok", comunidad=600, ibi=400, basuras=100, subidaPedida=10, subidaRenta=2.47, tramo="dentro", honorarios=500, acuerdo="si")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("E ejemplo con acuerdo/clausula", V()), ("A1 sin acuerdo dentro: no sube", V(acuerdo="no")),
 ("A2 sin acuerdo, pedida 3 % < tope: tampoco", V(acuerdo="no", subidaPedida=3)), ("A3 sin acuerdo fuera de 5/7: manda el pacto", V(acuerdo="no", tramo="fuera")),
 ("A4 sin acuerdo y pacto invalido: 0", V(acuerdo="no", pacto="sinimp")), ("B1 borde 2s exacto", V(subidaPedida=4.94)), ("B2 s=0", V(subidaRenta=0)),
 ("S1 seguro sumado a comunidad 600+150: tope sobre la suma", V(comunidad=750))]
if __name__ == "__main__":
    src = open(JS).read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", src + "\nJSON.stringify(" + json.dumps([c for _, c in CASES]) + ".map(calcular));"], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    jr = json.loads(o.stdout); bad = 0
    for (n, c), j in zip(CASES, jr):
        m = model(c); d = [(k, round(j.get(k, float("nan")), 2), round(v, 2)) for k, v in m.items() if j.get(k) is None or abs(j[k] - v) > 0.005]
        bad += bool(d); print(n, "OK" if not d else d)
    print("casos:", len(CASES), "discrepancias:", bad); sys.exit(1 if bad else 0)
