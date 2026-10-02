# Verificación fiscal independiente (Opus): donativos-irpf-cuanto-desgrava-y-cuanto-donar · 2026-10-02
VEREDICTO: PUBLICABLE CON CAMBIOS (3 cambios obligatorios de texto/aviso; ninguna fórmula errónea).

## Fuentes leídas hoy (BOE consolidado, descargado 2/10/2026)
- Ley 49/2002 (última actualización 20/12/2023: ninguna norma de 2026 la toca). Art. 19.1 (RDL 6/2023): 80 % hasta 250 €, 40 % resto; 45 % sobre lo que exceda de 250 € a favor de la misma entidad «siendo el importe ... de este ejercicio y el del período impositivo anterior, igual o superior, en cada uno de ellos, al del ejercicio inmediato anterior». Art. 19.2 remite al límite del art. 69.1 LIRPF. Art. 20.1: arrastre 10 años SOLO en IS. Art. 17.2: contraprestación simbólica ≤ 15 % y ≤ 25.000 €. Art. 22: PGE puede elevar 5 puntos porcentajes y límites. Art. 18.1.a: dinerario = importe.
- Ley 35/2006 (últ. act. 30/09/2026). Art. 68.3 a/b/c (Ley 49/2002; 10 % fundaciones no acogidas; 20 % partidos, base máx. 600 €). Art. 68.4: Ceuta/Melilla 60 %. Art. 69.1: base ≤ 10 % de la base liquidable (sin redacción nueva desde 2013). Art. 67.1.b (RDL 26/2026): 50 % de 68.2-68.5 contra cuota estatal; 67.2 no negativa. RDL 26/2026 en art. 68 solo añade el apartado 6 (vivienda): no toca donativos. Ningún RDL 2026 (2, 5, 6, 7, 10, 22, 23, 26) menciona donativos (búsqueda «donativ» en el texto: solo arts. 68 y 105). Art. 57: mínimo del contribuyente 5.550 €.
- AEAT Manual Renta 2025, «Límite aplicable»: base liquidable = casillas 0500 + 0510 (0505 si hay compensación de bases negativas); 15 % prioritarias. AEAT Deducciones autonómicas 2025, C. Valenciana (art. 4.Uno.s y DA 16ª Ley 13/1997): 20 % de los primeros 250 € compatible con la estatal.

## 1. Cifras y artículos: correctos y vigentes en 2026
250 €/80 %, 40 %, 45 % ✔ (RDL 6/2023, vigente). Límite 10 % sobre BL general + ahorro ✔ (AEAT 0500+0510). Sin arrastre en IRPF ✔ (art. 19 no lo prevé; art. 20 es IS). Ceuta/Melilla 60 % ✔. Forales excluidos ✔. Prioritarias declaradas ✔ (matiz: el 15 % del IRPF lo fija la Ley de PGE sobre el 69.1, no el art. 22 directamente; aceptable).
Recurrencia: FAQ 2 coincide con la norma vigente (este año ≥ año pasado y año pasado ≥ el anterior). PERO el label del input, FAQ 1 y la sección HTML «Qué es la recurrencia» usan la lectura antigua (pre-2024: «los dos años anteriores, cada año ≥ el anterior»), que no exige que el importe de ESTE año sea ≥ al del año pasado. Ejemplo engañoso: 100 €/200 €/150 € → el usuario contesta «Sí» y la norma da 40 %, no 45 %. → cambio 1.

## 2. Casos engañosos
- Base liquidable baja: el límite por cuota NO es una omisión de nicho. Con BL < mínimo personal (5.550 €, más con hijos/edad, art. 57-61) la cuota íntegra es 0 y la deducción real es 0; el veredicto dice «Donar 400 € te desgrava 144 €» con BL 1.800 (probado con el JS). Desde ~7.000-13.000 € de BL (según mínimos) la cuota puede cortar. El aviso genérico al final de la nota no basta: el número grande es falso para ese usuario. → cambio 2.
- «Siempre te cuesta dinero / coste neto positivo / siempre pierdes dinero»: demostrado solo para la deducción estatal (máx. 80 %). Con la autonómica valenciana (20 % de los primeros 250 € si aplicas la estatal) el primer tramo llega al 100 %: coste 0 €, nunca negativo. → cambio 3 (matizar «con la deducción estatal»; «nunca ganas dinero» sí es defendible con las CCAA vistas, sin verificar las 15).
- Partidos (20 %, 600 €), fundaciones no acogidas (10 %), especie (art. 18.1.b), varias entidades, prioritarias, Ceuta/Melilla, forales: excluidos y declarados ✔. Importe grande con tope (15.000 € rec., BL 90.000 → 4.137,50 €) ✔. Base 0 ✔; base negativa tecleada se clampa a 0 ✔.
- Adicional cuando ya se está en el tope: el texto dice «la deducción sube de 144 € a 144 € (0 € más)» → cambio 4 (menor).

## 3. Texto ≤ cálculo
| frase | demostrada | corrección |
|---|---|---|
| Lead/veredicto: 300 € → 220 € ded., 80 € netos | sí (BL ≥ ~7.000) | — |
| «siempre te cuesta dinero» (lead, json lead, HTML l.32 «siempre pierdes dinero», l.16, nota JS) | solo estatal | cambio 3 |
| Veredicto 0,20/0,60/0,55 €/€ hasta el 10 % | sí | — |
| FAQ 2: 2.000 €, BL 20.000: 987,50 vs 900 | sí (200+0,45·1.750 / 200+0,40·1.750) | — |
| FAQ 3: exceso sin arrastre en IRPF; 10 años solo IS (art. 20) | sí (norma) | — |
| FAQ 4: certificado art. 24; 15 % art. 17.2 | sí (parcial: falta «y 25.000 €» y destino/irrevocabilidad del certificado) | opcional |
| «no depende de tu tipo marginal» | sí (salvo tope por cuota) | — |
| Ceuta/Melilla «no cubre tu territorio» | correcto pero conservador: allí la deducción de donativos es la misma; el 60 % solo reduce la cuota disponible | opcional: calcular con aviso |

## 4. Oráculos
Oráculo del constructor: 614 casos, 0 discrepancias > 1 €. check.py decidir: OK 1715/1715. Mis 5 escenarios (Python desde la norma, scratchpad): 150 €/BL 12.000 → 120; 1.200 € rec./BL 30.000 → 627,50; 400 €/BL 1.800 → 144 (tope 180); 15.000 € rec./BL 90.000 → 4.137,50; BL −5.000 → 0. Dif. máx. 0,00 €. 5 veredictos UI (mock de EM/document) sin contradicción con los números salvo los cambios 2 y 4.

## Cambios obligatorios
1. calcs/…json input `recurrente` label → «¿Donaste a esa misma entidad en los dos años anteriores, y este año y el pasado donas cada uno igual o más que el año previo?»; FAQ 1 (l.73) y content/…html l.21 («Qué es la recurrencia»): misma redacción que FAQ 2 (art. 19.1 Ley 49/2002, redacción RDL 6/2023).
2. calcs/…js pintar(): si bl < 5.550 → veredicto tone "warn": «Con esa base liquidable tu cuota íntegra probablemente es 0 € (mínimo personal 5.550 €, art. 57 LIRPF): la deducción solo se aplica hasta tu cuota; comprueba casillas 0545+0546». Si bl < 15.000 → añadir esa frase en la nota (no al final, junto al veredicto). Mejor (opcional): input «cuota íntegra estatal+autonómica» y deducción = min(ded/2, cuota/2)·2. Añadir a test.json el caso BL 1.800 / 400 € con el aviso.
3. json lead y veredicto, html l.1, l.16, l.32 y nota del JS: «siempre te cuesta dinero» → «con la deducción estatal siempre te cuesta dinero (alguna deducción autonómica, p. ej. la valenciana del 20 % de los primeros 250 €, puede dejar ese tramo a coste 0, nunca en ganancia)».
4. calcs/…js nota adicional: si deduccionAdicional < 0,005 → «esa cantidad extra no desgrava nada: ya estás en el tope del 10 %».
Opcionales: label `bl` «(casillas 0500+0510; si compensas bases negativas, 0505+0510)»; FAQ 4 «≤ 15 % y ≤ 25.000 €»; en conjunta el tope del 10 % es sobre la BL conjunta (no verificado el reparto del tramo de 250 €; no afirmarlo).

## Supuestos
Aceptables (declarados): una sola entidad; 250 € sobre el conjunto (es literal del art. 19.1); BL general + ahorro; dinerario; régimen común; sin prioritarias; sin autonómicas (con aviso). Erróneo como está: «no se limita por la cuota» presentado solo como letra pequeña, cuando invierte el resultado para BL bajas (cambio 2).
