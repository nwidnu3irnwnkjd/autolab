#!/usr/bin/env python3
"""Oraculo independiente: gastos del alquiler de vivienda, quien paga y cuanto puede subir lo repercutido (LAU 20.1-3, 17.6, 21.4). Escrito desde la norma antes de abrir el .js.
INTERPRETACION
- Pacto (art. 20.1 pf. 1): comunidad, IBI (tributo) y tasa de basuras (tributo, LGT 2.2.a) solo pasan al inquilino si el pacto consta POR ESCRITO y determina el IMPORTE ANUAL a la fecha del contrato. Escrito sin importe, o sin escrito: validez nula -> paga el arrendador.
- Con pacto valido, el inquilino paga comunidad + IBI + basuras. Comunidad: durante los 5 primeros anos (7 si arrendador persona juridica) solo sube POR ACUERDO y nunca mas del DOBLE de lo que pueda subir la renta (art. 20.2 -> art. 18.1).
  El tope 20.2 excluye los tributos (IBI y basuras suben libremente con el recibo). (20.2 «por acuerdo de las partes»: sin acuerdo ni clausula de revision, dentro de 5/7 anos pct legal = 0; la clausula de revision es acuerdo anticipado y entra en el tope). Despues de 5/7 anos el 20.2 no limita: manda el pacto (se admite lo pedido).
- Gestion inmobiliaria y formalizacion (art. 20.1 ultimo parrafo): del arrendador siempre en vivienda (pf o pj, Ley 12/2023): lo cobrado al inquilino es rechazable.
- Suministros con contador (20.3) siempre del inquilino y pequenas reparaciones (21.4) del inquilino: no entran en el calculo (solo texto).
- Zona tensionada (17.6): solo aviso, no cambia el importe. Tope de subida = 2 x s (s = % maximo de actualizacion de la renta, dato del usuario, >= 0). Borde: p == 2s cabe.
- RDL 29/2026 (en vigor 8-10-2026, pendiente de convalidacion), art. 20 LAU nuevo: el IBI NO es repercutible al inquilino (salvo obligado tributario); la tasa de basuras suele tener al ocupante como contribuyente (TRLRHL 23.1.b y 23.2.a) y sigue siendo suya en contratos firmados desde el 8-10-2026 (firma="despues"; sin transitoria expresa, lectura propia por la regla general de que el contrato se rige por la ley de su firma; supuesto S, confianza B). Comunidad, tope 2x y honorarios (ahora art. 20.2/20.3) no cambian de mecanica.
- Se asume que el arrendador repercute las tres partidas y la agencia con los importes dados; «cuota de comunidad» = importe anual vigente antes de la subida de este ano.
"""
import json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JS = os.path.join(ROOT, "projects/decidir/calcs/gastos-alquiler-quien-paga.js")

def model(d):
    valido = d["pacto"] == "ok"
    tope = max(0.0, 2.0 * d["subidaRenta"])
    limitado = valido and d["tramo"] == "dentro"
    pct = (0.0 if d["acuerdo"] == "no" else min(d["subidaPedida"], tope)) if limitado else d["subidaPedida"]
    com_ped = d["comunidad"] * (1 + d["subidaPedida"] / 100.0)
    com_ley = d["comunidad"] * (1 + pct / 100.0) if valido else 0.0
    nuevo = d.get("firma", "antes") == "despues"
    ibi_ley = d["ibi"] if (valido and not nuevo) else 0.0
    bas_ley = d["basuras"] if valido else 0.0   # tasa de basuras: el ocupante suele ser el contribuyente (TRLRHL 23.1.b, 23.2.a): sigue siendo repercutible con firma despues
    hon_ley = 0.0
    pedido = com_ped + d["ibi"] + d["basuras"] + d["honorarios"]
    ley = com_ley + ibi_ley + bas_ley + hon_ley
    return dict(topePct=tope, pctLegal=(pct if valido else 0.0), limitado=1 if limitado else 0, comunidadPedida=com_ped, comunidadLegal=com_ley,
                excesoComunidad=com_ped - com_ley, ibiRechazable=d["ibi"] - ibi_ley, basurasRechazable=d["basuras"] - bas_ley,
                honorariosRechazable=d["honorarios"] - hon_ley, pedido=pedido, tuCargo=ley, rechazable=pedido - ley)

KEYS = list(model(dict(pacto="ok", comunidad=1, ibi=1, basuras=1, subidaPedida=1, subidaRenta=1, tramo="dentro", honorarios=1, acuerdo="si")))
def js(cases):
    src = open(JS).read().split("function eur(")[0]
    o = subprocess.run(["osascript", "-l", "JavaScript", "-e", src + "\nJSON.stringify(" + json.dumps(cases) + ".map(calcular));"], capture_output=True, text=True)
    if o.returncode: print(o.stderr); sys.exit(2)
    return json.loads(o.stdout)
B = dict(pacto="ok", comunidad=600, ibi=400, basuras=100, subidaPedida=10, subidaRenta=2.47, tramo="dentro", honorarios=500, acuerdo="si")
def V(**k): x = dict(B); x.update(k); return x
CASES = [("1 ejemplo", V()), ("2 borde p=2s", V(subidaPedida=4.94)), ("3 p justo encima", V(subidaPedida=4.95)), ("4 sin importe anual", V(pacto="sinimp")),
 ("5 sin pacto", V(pacto="no")), ("6 fuera de 5/7 anos", V(tramo="fuera")), ("7 renta 0 -> comunidad no sube", V(subidaRenta=0)), ("8 todo conforme", V(subidaPedida=0, honorarios=0)),
 ("9 todo cero", V(comunidad=0, ibi=0, basuras=0, subidaPedida=0, honorarios=0)), ("10 sin pacto y sin honorarios", V(pacto="no", honorarios=0, subidaPedida=0)),
 ("11 A1 sin acuerdo dentro", V(acuerdo="no")), ("12 A2 sin acuerdo, pedida 3 %", V(acuerdo="no", subidaPedida=3)), ("13 A3 sin acuerdo fuera", V(acuerdo="no", tramo="fuera")), ("14 sin acuerdo y pacto invalido", V(acuerdo="no", pacto="sinimp")), ("15 seguro sumado a comunidad", V(comunidad=750)),
 ("16 RDL29 firma despues: IBI no repercutible", V(firma="despues")), ("17 firma despues y fuera de 5/7", V(firma="despues", tramo="fuera")), ("18 firma despues sin pacto", V(firma="despues", pacto="no")),
 ("19 firma despues, subida en el tope, sin honorarios", V(firma="despues", subidaPedida=4.94, honorarios=0)), ("21 UI por defecto antes (basuras 0, renta 2 %)", V(basuras=0, subidaRenta=2)), ("22 UI por defecto despues", V(basuras=0, subidaRenta=2, firma="despues")), ("23 UI antes con renta 2,47", V(basuras=0)), ("24 despues, basuras del inquilino 100, renta 2", V(subidaRenta=2, firma="despues")), ("20 firma despues, todo cero", V(firma="despues", comunidad=0, ibi=0, basuras=0, subidaPedida=0, honorarios=0))]
if __name__ == "__main__":
    rnd = random.Random(58)
    def mk():
        return dict(pacto=rnd.choice(["ok", "ok", "sinimp", "no"]), comunidad=rnd.choice([0, 300, 600, rnd.uniform(0, 3000)]), ibi=rnd.choice([0, 400, rnd.uniform(0, 1500)]),
                    basuras=rnd.choice([0, 100, rnd.uniform(0, 400)]), subidaPedida=rnd.choice([0, 2.47, 4.94, 5, 10, rnd.uniform(0, 30)]), subidaRenta=rnd.choice([0, 1, 2.47, 3, rnd.uniform(0, 6)]),
                    firma=rnd.choice(["antes", "despues"]), tramo=rnd.choice(["dentro", "dentro", "fuera"]), acuerdo=rnd.choice(["si", "si", "no"]), honorarios=rnd.choice([0, 500, rnd.uniform(0, 2000)]))
    sweep = [mk() for _ in range(800)]
    allc = [c for _, c in CASES] + sweep; jr = js(allc); bad = 0
    for i, c in enumerate(allc):
        o = model(c); j = jr[i]
        diffs = [(k, j.get(k), o[k]) for k in KEYS if j.get(k) is None or abs(j[k] - o[k]) > 0.005]
        if i < len(CASES): print(CASES[i][0], {k: round(o[k], 2) for k in ("topePct", "comunidadLegal", "excesoComunidad", "pedido", "tuCargo", "rechazable")}, "OK" if not diffs else diffs)
        if diffs:
            bad += 1
            if i >= len(CASES): print("SWEEP DIFF", c, diffs)
    print("casos:", len(allc), "discrepancias:", bad)
    sys.exit(1 if bad else 0)
