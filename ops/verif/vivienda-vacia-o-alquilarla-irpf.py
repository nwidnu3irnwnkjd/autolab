#!/usr/bin/env python3
"""Casos del Verificador fiscal (2026-10-02): JS vs oraculo del Constructor en 4 bordes nuevos + asserts de valor."""
import importlib.util as u, os, sys
H = os.path.dirname(os.path.abspath(__file__))
s = u.spec_from_file_location("o", os.path.join(H, "vivienda-vacia-o-alquilarla-irpf_oraculo.py")); o = u.module_from_spec(s); s.loader.exec_module(o)
C = [("familiar con perdida: minimo 660", o.V(fam="si", gastos=12000), dict(redf=660, cuotaB=198, resB=-2598)),
     ("familiar 90 dias vacio renta 600", o.V(fam="si", dv=90, renta=600), dict(minimo=497.26, impdv=162.74, cuotaB=198)),
     ("perdida con 60 dias vacio (limite: no compensa)", o.V(gastos=12000, dv=60), dict(redf=-2005.48, cuotaB=32.55)),
     ("2 % familiar 800: reducido 1300 > minimo 1200", o.V(rev="g", fam="si"), dict(redf=1300, cuotaA=360, cuotaB=390))]
jr = o.js([c for _, c, _ in C]); bad = 0
for (n, c, exp), j in zip(C, jr):
    m = o.model(c)
    errs = [k for k in exp if abs(j[k] - exp[k]) > 0.01 or abs(m[k] - exp[k]) > 0.01]
    print(n, "OK" if not errs else errs); bad += bool(errs)
sys.exit(1 if bad else 0)
