#!/usr/bin/env python3
"""Casos propios del Verificador fiscal (2026-10-03) para sueldo-bruto-a-neto-2026.
Reutiliza model() del oraculo del Constructor y comprueba: (a) los casos del lead/FAQ recalculados a mano;
(b) los casos que exigen los cambios obligatorios C1 (art. 83.2 RIRPF, temporal < 1 año sobre lo cobrado en el año)
y C2 (art. 96.2.a LIRPF, sin obligacion de declarar hasta 22.000 € de un pagador). Uso: python3 ops/verif/sueldo-bruto-a-neto-2026.py"""
import importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sp = importlib.util.spec_from_file_location("o", os.path.join(ROOT, "ops/verif/sueldo-bruto-a-neto-2026_oraculo.py"))
o = importlib.util.module_from_spec(sp); sp.loader.exec_module(o)
def M(**k):
    d = dict(bruto=25200, pagas=14, contrato="indef", ccaa="madrid", hijos=0, menores3=0); d.update(k); return o.model(d)
fail = 0
def eq(nombre, got, exp, tol=0.011):
    global fail
    ok = abs(got - exp) <= tol; fail += not ok
    print(("OK  " if ok else "MAL ") + nombre, round(got, 2), "esperado", exp)
# (a) lead y FAQ (recalculo a mano: SS 6,50 %, art. 20 = 0, base 21.562, cuota 3.579,60 < tope 43 % 4.009,32)
r = M(); eq("25.200 tipo", r["tipo"], 14.20); eq("25.200 mes normal", r["netoMesNormal14"], 1407.90); eq("25.200 mes extra", r["netoMesExtra14"], 2952.30)
eq("25.200 IRPF final Madrid", r["irpfFinal"], 3350.35); eq("25.200 a devolver", r["difRenta"], 228.05)
r = M(bruto=21600); eq("21.600 tipo (tope 43 % art. 85.3 activo: 2.461,32)", r["tipo"], 11.40); eq("21.600 neto/12", r["netoMes12"], 1477.80)
eq("25.200 con 2 hijos tipo", M(hijos=2)["tipo"], 10.36); eq("18.000 tipo", M(bruto=18000)["tipo"], 5.07)
# (b) C2: con un solo pagador y <= 22.000 € no hay obligacion de declarar (art. 96.2.a LIRPF): si difRenta < 0 la pagina NO debe decir «a pagar»
for R, cc, exp in [(21000, "madrid", -132.35), (22000, "andalucia", -109.85), (22250, "andalucia", -58.15)]:
    r = M(bruto=R, ccaa=cc); eq("%d %s difRenta" % (R, cc), r["difRenta"], exp)
    print("    -> obligado a declarar:", R > 22000, "| la pagina debe decir:", "a pagar estimado" if R > 22000 else "no obligado a declarar: el neto real es el de la nomina (%.2f)" % r["neto"])
# C1: temporal < 1 año, 6 meses a 1.800 x 14 equivalente -> cobrado en el año natural 12.600 (art. 83.2 regla 1.ª)
r = M(bruto=25200, contrato="temp1", meses=6); eq("temp1 6 meses tipo (minimo 2 %)", r["tipo"], 2.00); eq("temp1 6 meses SS (6,55 % de 12.600)", r["ss"], 825.30); eq("temp1 6 meses retencion", r["ret"], 252.00)
eq("temp1 6 meses neto", r["neto"], 11522.70); eq("temp1 6 meses neto por mes de contrato", r["netoMes12"], 1920.45); eq("temp1 IRPF final", r["irpfFinal"], 0.0); eq("temp1 a devolver", r["difRenta"], 252.00)
sys.exit(1 if fail else 0)
