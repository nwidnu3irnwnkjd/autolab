"""Casos propios del Verificador fiscal (Opus, 2026-10-02) para incapacidad-permanente.
Norma: LGSS 196.2 parr. 3 (suelo de la total por enfermedad comun = minimo IPT comun <60 con conyuge no a cargo,
9.580,20 EUR/ano en 2026, RD 241/2026 anexo I; sin limite de ingresos) y RD 241/2026 art. 9.2 (complemento por
minimos parcial: diferencia hasta 9.442 + minimo). Uso: python3 ops/verif/<slug>.py -> imprime los esperados;
el JS corregido debe dar estos 'pagado' (pension cobrada al mes con el trabajo indicado)."""
SUELO = 9580.20 / 14; LIM = 9442.0
def pagado_total_comun(br, edad, sal_mes, minimo_anual):
    pen = max(br * 0.55, SUELO)            # 196.2 parr. 3 (tope 3.359,60 no interviene en estos casos)
    ing = sal_mes * 12
    comp = max(min(minimo_anual - pen * 14, LIM + minimo_anual - ing - pen * 14), 0) / 14   # RD 241/2026 art. 9.2
    return round(pen + comp, 2)
CASOS = [
    # (descripcion, BR, edad, sueldo/mes, minimo anual, esperado pagado/mes)
    ("total comun 45a, 20 anos, base 1.200, funciones distintas 1.200 EUR", 1200 * 96 / 112, 45, 1200, 9662.80, 684.30),
    ("total comun 61a, 30 anos, base 900, funciones distintas 1.000 EUR", 900 * 96 / 112 * 0.9848, 61, 1000, 12262.60, 693.19),
    ("total comun 61a, 30 anos, base 900, sin trabajo", 900 * 96 / 112 * 0.9848, 61, 0, 12262.60, 875.90),
]
ok = True
for d, br, e, s, m, esp in CASOS:
    got = pagado_total_comun(br, e, s, m); ok &= abs(got - esp) < 0.01
    print(("OK " if abs(got - esp) < 0.01 else "XX ") + d + ": " + str(got) + " (esperado " + str(esp) + ")")
raise SystemExit(0 if ok else 1)
