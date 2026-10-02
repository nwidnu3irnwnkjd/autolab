#!/usr/bin/env python3
"""Oraculo independiente: donativos IRPF (Ley 49/2002 art. 19; Ley 35/2006 art. 69.1). Escrito desde la norma ANTES del .js.
Norma: deduccion en cuota = 80 % de los primeros 250 EUR de la base de deduccion y 40 % del resto (45 % si hay recurrencia con la misma
entidad); la base de deduccion no puede exceder el 10 % de la base liquidable (LIRPF art. 69.1; Ley 49/2002 art. 19.2). Sin arrastre en IRPF.
Uso: python3 ops/verif/donativos-irpf-cuanto-desgrava-y-cuanto-donar.py  -> casos fijos + barrido aleatorio JS vs Python."""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = "donativos-irpf-cuanto-desgrava-y-cuanto-donar"

def oraculo(donado, rec, bl, adicional, ambito="comun"):
    if ambito not in ("comun", "ceutamelilla"):
        return {"invalido": 1}
    limite = 0.10 * max(bl, 0)
    def deduccion(x):
        base = min(x, limite)
        return 0.80 * min(base, 250) + (0.45 if rec else 0.40) * max(base - 250, 0)
    ded = deduccion(donado)
    tot = deduccion(donado + adicional)
    return {
        "invalido": 0, "limite": limite, "baseDeduccion": min(donado, limite), "exceso": max(donado - limite, 0),
        "deduccion": ded, "costeNeto": donado - ded, "importeTramo80": min(250, limite),
        "deduccionTotal": tot, "deduccionAdicional": tot - ded, "costeNetoAdicional": adicional - (tot - ded),
        "avisoBase": 2 if bl < 5550 else (1 if bl < 15000 else 0),
    }

def js_eval(cases):
    js = open(os.path.join(ROOT, "projects/decidir/calcs", SLUG + ".js")).read().split("function eur(")[0]
    h = js + "\nJSON.stringify(" + json.dumps(cases) + ".map(function(c){return calcular(c);}));"
    out = subprocess.run(["osascript", "-l", "JavaScript", "-e", h], capture_output=True, text=True)
    if out.returncode: sys.exit("error JS: " + out.stderr)
    return json.loads(out.stdout.strip())

def main():
    random.seed(20261002)
    fijos = [(300, 0, 25000, 0), (0, 0, 25000, 0), (250, 0, 25000, 0), (251, 0, 25000, 0), (251, 1, 25000, 0),
             (3000, 0, 20000, 0), (2000, 1, 20000, 0), (500, 0, 0, 0), (100, 0, 1000, 150), (250, 1, 2500, 1), (10000, 1, 100000, 5000),
             (400, 0, 1800, 0), (400, 0, 5549, 0), (400, 0, 5550, 0), (400, 0, 14999, 0), (400, 0, 15000, 0), (100, 0, 12000, 200), (15000, 1, 90000, 0), (100, 1, 20000, 0)]
    casos = [dict(donado=a, recurrente=b, bl=c, adicional=d, ambito="comun") for a, b, c, d in fijos]
    casos += [dict(donado=1000, recurrente=0, bl=30000, adicional=0, ambito=a) for a in ("vasco", "navarra")]
    casos += [dict(donado=1000, recurrente=0, bl=30000, adicional=0, ambito="ceutamelilla")]
    for _ in range(600):
        bl = random.choice([0, random.uniform(0, 5000), random.uniform(0, 40000), random.uniform(0, 300000)])
        casos.append(dict(donado=random.choice([0, 250, 251, round(random.uniform(0, 600), 2), round(random.uniform(0, 8000), 2), round(random.uniform(0, 60000), 2)]),
                          recurrente=random.randint(0, 1), bl=round(bl, 2), adicional=random.choice([0, round(random.uniform(0, 3000), 2)]), ambito="comun"))
    res = js_eval(casos); mal = 0
    for c, r in zip(casos, res):
        o = oraculo(c["donado"], c["recurrente"], c["bl"], c["adicional"], c["ambito"])
        for k, v in o.items():
            x = r.get(k)
            if x is None or x != x or abs(x - v) > 1:
                mal += 1; print("DISCREPANCIA", c, k, x, v)
    print(f"{len(casos)} casos (19 fijos + 3 ambitos + 600 aleatorios): {mal} discrepancias > 1 EUR")
    sys.exit(1 if mal else 0)
if __name__ == "__main__":
    main()
