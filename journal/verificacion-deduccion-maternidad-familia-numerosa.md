# Verificación fiscal deduccion-maternidad-familia-numerosa (Verificador Opus, 2026-10-02)
VEREDICTO: PUBLICABLE CON CAMBIOS · 5 cambios obligatorios (1 crítico) · interpretación del Paso 0 DIFIERE del oráculo en un punto (meses de maternidad).
Fuentes leídas hoy (API BOE datos abiertos): LIRPF arts. 81 (red. Ley 31/2022) y 81 bis (red. Ley 6/2018) vigentes; RIRPF art. 60 bis; Ley 40/2003 art. 2; RDL 26/2026 (0 menciones a 81, 81 bis, maternidad o familia numerosa). Sin PGE 2026: cuantías sin cambios en 2026.

## Paso 0: interpretación propia
1. Art. 81: requisito de actividad solo en un momento (paro al nacer, o alta con 30 días cotizados al nacer o después). Después, los meses son los posteriores al cumplimiento en que la madre tiene derecho al mínimo por ese hijo <3 (art. 81.3). NO exige seguir de alta. Sin tope de cotizaciones (confirmado: el Constructor acierta).
2. Guardería: hasta 1.000 €, proporcional a meses simultáneos con los requisitos de 81.1 y 81.2, tope gasto no subvencionado (confirmado).
3. Art. 81 bis.c: 1.200 € / +100 % especial / +600 € por hijo sobre el mínimo; meses con alta (cualquier día del mes) O con paro/pensión (RIRPF 60 bis.2.2.ª-3.ª); tope de cotizaciones devengadas tras cumplir requisitos solo sobre la base y NO aplicable a perceptores de paro/pensión (60 bis.1 in fine). Confirmado.
4. 81 y 81 bis acumulables entre sí y con el mínimo por descendientes (ninguna norma las excluye). Confirmado.
DIFERENCIA: el oráculo y el JS usan un solo `meses` («de alta en la SS») para 81 y 81 bis. Para el 81 eso es la ley anterior a 2023.

## Cambios obligatorios
| # | Patrón | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 CRÍTICO | 2/6 | calcs .js/.json + oráculo | Separar `mesesMat` (meses con hijo <3 y derecho al mínimo, tras cumplir el requisito) de `mesesFam` (meses con alta, paro o pensión y título). mat y guardería (min(guarMeses, mesesMat)) y anticipo 140 usan mesesMat; 81 bis y anticipo 143 usan mesesFam. | Art. 81.1 y 81.3: la madre que deja de estar de alta (excedencia, fin de contrato) conserva la maternidad; hoy la calculadora se la recorta hasta 1.200 €/hijo. |
| 2 | 1/4 | .json lead, veredicto, ayuda de n3, label de meses; .html lead | Quitar «Si estás de alta» / «de alta ... y con 30 días cotizados» como condición actual. Redacción: «si cobrabas paro al nacer tu hijo, o en ese momento o después estuviste de alta con 30 días cotizados; no hace falta seguir de alta». | Art. 81.1 vigente. |
| 3 | 2/8 | .js/.json | Añadir opción «cobro paro o pensión» (sin tope) o, como mínimo, la ayuda de `cotiz`: «si cobras paro o pensión, escribe 1.200 o más». Hoy la página dice «con paro o pensión no hay tope» pero con cotiz 0 el cálculo quita los 1.200 €. | 81 bis.2 y RIRPF 60 bis.1 último inciso. |
| 4 | 8 | .js | fam = mono2 con titulares = 2: bloquear o forzar 1. | 81 bis.1.c: exige la totalidad del mínimo por los dos hijos, solo puede tenerlo un progenitor. |
| 5 | 6 | .json/.html «Qué no incluye» y mensaje de inválido | Ampliar «familias con dos hijos y uno con discapacidad» a todos los casos equiparados de 2 hijos (art. 2.2 Ley 40/2003: ascendientes con discapacidad, viudo/a con 2 hijos, huérfanos). | El formulario los bloquea; deben estar declarados. |

## Supuestos del Constructor
(1) mínimo especial = 5: defendible, declarado. (2) 81 + 81 bis acumulables: correcto. (3) mismos meses/gasto por hijo: declarado. (4) guardería ≤ meses con derecho: correcto, pero con mesesMat (cambio 1). (5) anticipo no recortado por tope: correcto (lo anticipado se regulariza). No modelado y bien avisado: 150 € del mes de 30 días, complemento de infancia IMV, discapacidad a cargo, adopción/acogimiento, guardería tras 3 años, forales, autonómicas. Añadir a límites (no obligatorio): cesión del derecho entre titulares (RIRPF 60 bis) y requisitos mínimos de alta para el anticipo (60 bis.3, 15 días/mes jornada completa).

## Citas muestreadas
81.1 (1.200 €, mínimo art. 58), 81 bis.2 (tope cotizaciones íntegras), 60 bis.1 RIRPF (incrementos fuera del tope): correctas. Ejemplo 3.233 € / 200 €/mes / 833 € recalculado: correcto.

## Casos nuevos para test.json (tras el cambio 1 y 3)
- A: n3 1, mesesMat 12, mesesFam 6, general 3 hijos, cotiz 2.000, guardería 10 meses 3.000 € → mat 1.200 + guar 833,33 + fam 600 = 2.633,33.
- B: n3 0, mesesFam 12, general 3, paro/pensión todo el año, cotiz 0 → fam 1.200 (sin recorte).
- C: n3 1, mesesMat 12, mesesFam 0, fam no, guardería 12 meses 5.000 € → 2.200.
- D: mono2, titulares 2 → inválido (o titulares tratado como 1: 1.200 con 12 meses y cotiz ≥ 1.200).
Re-verificación: Sonnet basta (la interpretación queda fijada aquí); ejecutar el oráculo actualizado con estos 4 casos y releer las frases de los cambios 2 y 5.
