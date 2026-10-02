#!/usr/bin/env python3
"""Casos del Verificador fiscal (Opus, 2026-10-02) para retencion-irpf-nomina-subir-o-no. Ejecuta el JS con osascript y comprueba:
V1 LIRPF 96.3.a.1.º: el «segundo pagador» es el de menor cuantía -> bruto 1.000 + pagador2 20.000 => limite 22.000, no obligado.
V2 bruto 20.000 + pagador2 1.000 => limite 22.000, no obligado (ya correcto).
V3 tipo voluntario mostrado nunca > 100 % (bruto 20.000, pagador2 1.000 da tipo0p2 = 233 %): el JS debe acotarlo o marcarlo como inalcanzable.
Sale 1 si alguno falla."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(ROOT, "projects/decidir/calcs/retencion-irpf-nomina-subir-o-no.js"), encoding="utf-8").read()
src = src[:src.index("function eur(")]
B = dict(ret=0, hijos=0, menores3=0, reparto="mitad", ccaa="madrid", euribor=2.5)
casos = [dict(B, bruto=1000, pagador2=20000), dict(B, bruto=20000, pagador2=1000)]
js = src + "\nJSON.stringify(%s.map(calcular));" % json.dumps(casos)
r = json.loads(subprocess.run(["osascript", "-l", "JavaScript", "-e", js], capture_output=True, text=True).stdout)
fallos = []
if r[0]["limiteObl"] != 22000 or r[0]["obligado"] != 0: fallos.append("V1 limite 96.3.a.1.º (orden de cuantia): %s / %s" % (r[0]["limiteObl"], r[0]["obligado"]))
if r[1]["limiteObl"] != 22000 or r[1]["obligado"] != 0: fallos.append("V2")
if max(x["tipo0"] for x in r) > 100 or max(x["tipo0p2"] for x in r) > 100: fallos.append("V3 tipo voluntario > 100 %% (tipo0p2=%.2f)" % r[1]["tipo0p2"])
print("\n".join(fallos) or "OK"); sys.exit(1 if fallos else 0)
