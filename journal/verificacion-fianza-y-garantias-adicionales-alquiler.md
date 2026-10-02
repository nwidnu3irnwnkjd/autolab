# Verificación fiscal/legal · fianza-y-garantias-adicionales-alquiler · 2026-10-02 (Verificador Opus, c57)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 0 · N 1 · R 0 · S 1 (crítico) · otros 2
Leído hoy en la API del BOE (consolidado LAU, versión BOE-A-2026-20526, vigencia 2/10/2026): arts. 4, 17, 20, 36 (historial de versiones del 20.1) y DT 4.ª de la Ley 12/2023 en el diario original.

## Paso 0 · mi interpretación frente al bloque INTERPRETACION
- 36.1 fianza 1 (vivienda) / 2 (uso distinto): coincide.
- 36.5 garantía ≤ 2 mensualidades solo en vivienda y contratos «de hasta cinco años de duración» (7 pj); duración pactada, «hasta» incluido: coincide. Prórroga obligatoria (art. 9) no cambia nada: un contrato de 1-3 años sigue siendo «de hasta 5». Uso distinto: «cualquier tipo de garantía», sin tope: coincide.
- **DIFIERE**: «lo pedido por encima como fianza no es exigible». El 36.5 admite «cualquier tipo de garantía ... adicional a la fianza en metálico»: un depósito mayor es garantía adicional en metálico y computa con la garantía en el tope de 2 (o sin tope). La propia página lo dice («un depósito mayor solo cabe como garantía adicional, dentro de su límite») pero el cálculo no lo hace.
- 20.1 gestión y formalización: confirmado SIEMPRE del arrendador, pf o pj. Historial del 20.1: RDL 7/2019 (6-3-2019) «cuando este sea persona jurídica» → Ley 12/2023 (26-5-2023) sin distinción → RDL 26/2026 (1-10-2026) «no podrán ser repercutidos ... bajo ningún concepto» → derogado, vuelve el texto de la Ley 12/2023. El encargo («solo pj») reflejaba la redacción de 2019, no la del RDL 26/2026.
- 36.4 interés legal: no modelado y declarado (FAQ + «Qué no incluye»): correcto, es de la devolución, no de la firma.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | S crítico | calcs/…js + oráculo | Exceso de fianza = garantía adicional: `extraF = max(0, fianza − fm)`; `exG = tope ? max(0, (garantia + extraF) − 2)·R : 0`; `exFianza` desaparece (o 0). Fila «Fianza»: «La ley permite» = legal; el exceso se mueve a la fila de garantía | Art. 36.5 párr. 1. Hoy: vivienda pf 5 años, fianza 2 + garantía 0 → dice «puedes negarte a pagar 900 €» (real: 0); 6 años, fianza 3 → 1.800 € (real: 0, sin tope); uso distinto fianza 3 → 900 € (real: 0) |
| 2 | S | content html «Cómo se calcula» + JS piezas | Sustituir «se cuenta como no exigible» por «se trata como garantía adicional y suma en su límite de 2 mensualidades» | Coherencia con 1 |
| 3 | T | content html «Qué no incluye» + FAQ comisión | Añadir: «Para contratos firmados antes del 6-3-2019 no existía el tope de 2 mensualidades de garantía (DT 1.ª RDL 7/2019), y entre el 6-3-2019 y el 25-5-2023 la comisión solo era obligatoriamente del casero si era persona jurídica (DT 4.ª Ley 12/2023): esta calculadora aplica la ley a contratos que se firman hoy» | Preverif decía «declarado» pero no está en la página ni en el JS |
| 4 | N | content html (art. 4.2) | Cambiar «se rigen sobre todo por lo pactado» por «fianza y garantía (art. 36, Título IV) se aplican igual; el adelanto (17.2) y la comisión (20.1) pueden pactarse» | Art. 4.1: Títulos I y IV imperativos; 4.2 párr. 2 solo libera el Título II |
| 5 | otros (territorial) | html y nota JS | Quitar «que fijan depósitos o tipos distintos» y «derechos civiles propios»; decir «la fianza, la garantía, el adelanto y la comisión son de la LAU y rigen en toda España; lo que cambia por comunidad es el depósito de la fianza (DA 3.ª)» | Ninguna CCAA fija otra cuantía de fianza; la frase sugiere que la LAU no rige allí |
| 6 | otros | json, ayuda de duración | «se prorroga hasta 5 (7 si el casero es persona jurídica)» | Art. 9.1 |

## Casos nuevos para test.json (en ops/verif/fianza-y-garantias-adicionales-alquiler.py)
viv pf 5a fianza 2 gar 0 → noExigible 0 · viv pf 5a fianza 2 gar 2 → 900 · viv pf 6a fianza 3 → 0 · uso fianza 3 → 0 · ejemplo (1/3/1/900) → 1.800 · pj 7a gar 3 → 900. Los 9 casos actuales siguen valiendo (fianza = 1 en todos salvo comprobar el 9).

## Sin cambios (comprobado)
Absolutos: lead y veredicto van condicionados (vivienda, ≤ 5/7 años); «nunca/en ningún caso» solo en la cita literal del 17.2. Citas por muestreo (36.1, 36.5, 20.1, 17.2): literales correctas. 36.2 bien resumido. 8: renta/duración ≤ 0 bloqueadas; uso distinto ignora arr/duración sin efecto en el resultado. R: el RDL 26/2026 solo aparece como nota de derogación.
Re-verificación: Sonnet, ejecutar ops/verif/fianza-y-garantias-adicionales-alquiler.py (necesita node) + oráculo del Constructor actualizado, y releer las frases 2-6. No hace falta otro Opus.
