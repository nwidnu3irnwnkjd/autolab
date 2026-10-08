# Re-verificación fiscal/legal · indemnizacion-despido-objetivo-o-improcedente-neto (c86, 2026-10-08)
VEREDICTO: PUBLICABLE CON CAMBIOS (1 obligatorio de texto, sin cambios de cálculo) · T 0 · 8 1 · N 0 · R 0 · S 0 · otros 2 (no críticos)
Motivo de la elección: alta demanda, JS sin tocar desde el 2-10 (verificación del 2-10 con 2.ª pasada) y sin reverificación posterior.

## Norma leída hoy (API BOE consolidada, última versión de cada bloque)
- ET (BOE-A-2015-11430): art. 56 y DT 11.ª y art. 59: versión única de 2015, sin cambios. Art. 53: última versión BOE-A-2025-76 (LO 1/2025, vig. 3-4-2025); 53.1.b sigue en 20 días, prorrateo por meses, máx. 12 mensualidades.
- LIRPF (BOE-A-2006-20764) art. 7: última versión BOE-A-2026-20823 (RDL 29/2026, vig. 8-10-2026): solo cambia la letra ñ (PALP); la anterior (BOE-A-2026-20528) solo la x. Letra e) idéntica en todas las versiones desde la de 5-3-2026 (BOE-A-2026-5060): 180.000 €, párr. 2 (52.c → límite del improcedente), conciliación art. 63 LRJS. RDL 25/28/29-2026 (pendientes de convalidación) no tocan 7.e, 18.2 ni el ET: si alguno decae, no afecta.
- LIRPF art. 18.2: última versión BOE-A-2014-12327; 30 %, generación = años de servicio, 300.000 €, sin cambios.
- LGSS (BOE-A-2015-11724) art. 268.1 (15 días; vers. 2023) y art. 275.5.b (indemnización legal no computa; vers. BOE-A-2024-10235): citas correctas.
- LRJS (BOE-A-2011-15936) art. 65.1 (vers. BOE-A-2025-76): la conciliación «suspenderá la caducidad».
- Cifras 2026-2027: la calculadora no depende de cifras anuales (no hay SMI, bases ni escala); 20/33/45 días, 12/24/42 mensualidades, 720 días, 180.000 €, 30 %/300.000 € vigentes en 2026 y sin reforma publicada para 2027.

## Oráculo y tests
- ops/verif/indemnizacion-despido-objetivo-o-improcedente-neto_oraculo.py: barrido 900 + 22 fijos, 0 discrepancias; params OK.
- python3 ops/check.py: OK 13660/13660 (incluye los 22 casos de calcs/indemnizacion-despido-objetivo-o-improcedente-neto.test.json).
- Paso 0: INTERPRETACION del oráculo (puntos 1-7) coincide con mi lectura de la norma vigente. Sin cambio de interpretación → no hace falta 2.ª pasada Opus.

## Cambios
| # | Clase | Archivo · línea | Texto actual → propuesto | Fuente |
|---|---|---|---|---|
| 1 (obligatorio) | 8 / absoluto | calcs/indemnizacion-despido-objetivo-o-improcedente-neto.js · l. 49 (escenario 3) | «…(" + eur(legal) + "): la parte legal está exenta de IRPF y el exceso tributa, de modo que…» → «…(" + eur(legal) + "): " + (r.trib > P.igual ? "la parte exenta (" + eur(r.exento) + ") no tributa y el resto sí" : "toda la oferta está exenta de IRPF por ser un despido objetivo por causas económicas, técnicas, organizativas o de producción y no superar la indemnización del improcedente") + ", de modo que…». Hoy, en un objetivo 52.c con oferta entre los 20 días y la cifra del improcedente (p. ej. 30.000 €, 8 años, oferta 21.699 €), el veredicto dice «el exceso tributa» mientras el cálculo da tributable ≈ 0 (caso 18 del oráculo: trib 0,37 € por redondeo). | LIRPF art. 7.e, párr. 2 |
| 2 (recomendado) | cita | content/indemnizacion-despido-objetivo-o-improcedente-neto.html · l. 15; calcs/…json · l. 111 (FAQ 5) | «(art. 59.3) y la solicitud de conciliación lo suspende» → «(art. 59.3) y la solicitud de conciliación lo suspende (art. 65.1 de la Ley reguladora de la jurisdicción social)». El art. 59.3 ET dice literalmente «quedará interrumpido»; la norma que dice «suspenderá» es la LRJS, que es la que hay que citar. | LRJS art. 65.1; ET art. 59.3 |
| 3 (menor) | texto | calcs/…js · l. 61 | «…ni costes del proceso, La exención exige…» → «…ni costes del proceso. La exención exige…» (la 2.ª pasada del 2-10 lo corrigió en content, no en el JS). | — |
| 4 (menor) | fecha | calcs/…json · l. 9 (sources) y data/params.json `indemnizacion_despido_2026.fuente` | «texto consolidado a 30/9/2026» → «texto consolidado consultado el 8/10/2026 (LIRPF art. 7 en su versión del RDL 29/2026, sin cambios en la letra e)». | BOE-A-2026-20823 |

## Comprobado sin cambios
- Cifras de la página (13.151 / 21.699 / 8.548; 47.466 / 47.564; 47.342; 8.301 → 5.811 → 2.150 → 27.850): reproducidas por el oráculo y check.py.
- Lead, veredicto json, FAQ 1-4: condicionados correctamente (conciliación/sentencia; 52.c hasta el improcedente). Bloqueos y avisos forales correctos.
- Escenario 2 del improcedente («exenta hasta 180.000 €») queda matizado por el párrafo de condición que el JS añade siempre en el improcedente: aceptable.

## Caso nuevo para test.json (tras el cambio 1)
- tipo objetivo, causa eco, bruto 30.000, 8 años, antes 0, oferta 21.698, marginal 37 → escenario 3, exento 21.698, trib 0, neto 21.698; el texto del veredicto no debe contener «el exceso tributa».
