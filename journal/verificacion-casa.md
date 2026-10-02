# Verificación fiscal independiente · cuanto-ahorrar-para-comprar-casa · 2026-10-02 (Opus)
VEREDICTO: **PUBLICABLE CON CAMBIOS** (1 error de fórmula en Baleares; 4 textos incorrectos o incompletos; 2 avisos que faltan y cambian la cifra en miles de euros).
Método: textos consolidados del BOE descargados hoy (fecha de última actualización entre paréntesis) y leídos artículo por artículo; Ley 1/2026 de Castilla-La Mancha (DOCM 30/3/2026, PDF oficial); guía oficial de la ATC (Cataluña) para la base del AJD. Oráculo del Constructor: 10 fijos + 624 aleatorios, 0 discrepancias. Casos propios: 10 escenarios calculados a mano desde la norma contra el JS (osascript): 9 OK (diferencia < 1 €) y 1 DIF (Baleares nueva ≥ 1 M €).

## Tipos contrastados (14/14)
| CCAA | ITP usada (JS) | AJD nueva (JS) | Norma (consolidado) | Estado |
|---|---|---|---|---|
| Madrid | 6 % | 0,4 % ≤120k / 0,5 % ≤180k / 0,75 %, aplicado a todo el valor | DLeg 1/2010 arts. 28, 32 (10/07/2026) | ok. **Falta aviso**: art. 30 bis y 38 bis, bonificación del 10 % de ITP y AJD en vivienda habitual ≤ 250.000 € |
| Andalucía | 7 % | 1,2 % | Ley 5/2021 arts. 41, 49 (31/12/2025) | ok (6 % y 1 % en vivienda habitual ≤ 150.000 €, arts. 43.1.a y 50.1.a) |
| Aragón | escala 8/8,5/9/9,5/10 | 1,5 % | DLeg 1/2005 arts. 121-1, 122-1 (07/07/2025) | ok |
| Asturias | 8/9/10 % sobre todo el valor (300k/500k) | 1,2 % | DLeg 2/2014 arts. 26, 34 (31/12/2025) | ok |
| Illes Balears | escala 8/9/10/12/13 | 1,5 % | DLeg 1/2014 arts. 10, 15, **17 bis** (13/06/2026) | ITP ok. **AJD ERROR**: art. 17 bis pone el 2 % cuando el valor es **igual o superior** a 1.000.000 €. Además, art. 17.1: 1 % para la primera vivienda habitual ≤ 270.151,20 € |
| Cantabria | 9 % | 1,5 % | DLeg 62/2008 arts. 9, 13 (30/04/2026) | ok. **Aviso incompleto**: 9.2 (7 % hasta 300.000 € en vivienda habitual, sin otro requisito), 9.3.c (4 % para menores de 40 años), 13.3 (1 % de AJD en vivienda habitual) y 13.4 (0,1 %) |
| Castilla-La Mancha | 9 % | 1,5 % | Ley 8/2013 arts. 19, 21 (consolidado 31/01/2023) + Ley 1/2026 | general ok (la Ley 1/2026 solo cambia los reducidos). **Texto ERROR**: el límite del 0,75 % de AJD es ahora 240.000 €, no 180.000 € (Ley 1/2026, art. 21.2) |
| Castilla y León | 8 % + 10 % sobre el exceso de 250.000 € | 1,5 % | DLeg 1/2013 arts. 24, 25 (14/05/2024) | ok, mantener «orientativa» |
| Cataluña | escala 10/11/12/13 | 1,5 % | DLeg 1/2024 arts. 641-1, 642-1 (22/05/2026) | ok |
| Extremadura | escala por tramos 8/10/11 | 1,5 % | DLeg 1/2018 arts. 36, 46 (04/08/2026) | ok; texto de reducidos (arts. 40, 41, 47) ok |
| Galicia | 8 % | 1,5 % | DLeg 1/2011 arts. 14, 15 (27/03/2026) | ok; 7 % y 1 % con límite de patrimonio de 240.000 € |
| Murcia | 7,75 % | 1,5 % | DLeg 1/2010 arts. 6, 7 (24/07/2025) | ok |
| La Rioja | 7 % | 1 % | Ley 10/2017 arts. 44, 48 (30/12/2025) | ok |
| C. Valenciana | 9 %; 11 % sobre todo el valor si > 1 M € | 1,4 % | Ley 13/1997 arts. 13, 14 (10/08/2026) | tipo «demás casos» ok. Ver 0,1 % abajo |
| IVA | 10 % | | Ley 37/1992 art. 91.Uno.1.7.º (30/09/2026) | ok |

**Base del AJD en vivienda nueva**: la correcta es el precio **sin IVA**. TRLITPAJD art. 30.1 dice «valor declarado», con mínimo del valor del art. 10. La guía práctica oficial de la ATC (p. 44) usa una base de 120.000 € y dice «nunca se suma el IVA a la base imponible». El JS lo sigue. Las lecturas «precio + IVA» son erróneas.
**Exclusiones**: correctas. País Vasco y Navarra tienen régimen foral; Canarias, IGIC y su propio ITP/AJD; Ceuta y Melilla, IPSI en lugar de IVA y bonificación del 50 %. Están declaradas en el formulario y en la nota.

## Discrepancias y omisiones relevantes
1. **Baleares, nueva, valor ≥ 1.000.000 €**: el JS aplica 1,5 % y la ley 2 %. Con 1.200.000 € el JS da 138.000 € y la ley 144.000 € (error de 6.000 €).
2. **Valencia, AJD 0,1 %** (art. 14.Uno.a): el único requisito es que sea vivienda habitual (concepto del IRPF), sin edad ni renta. Casi todo el que use esta calculadora compra su vivienda habitual, así que el 1,4 % sobrestima 3.250 € con 250.000 €. Es un **error por omisión del caso principal**, no un aviso aceptable tal como está: el aviso existe, pero sin cifra y la tabla del HTML lo contradice (12,4 %).
3. Otras rebajas cuyo único requisito es vivienda habitual (+ valor) y que mueven miles de euros: **Cantabria** 7 % hasta 300.000 € (−5.000 € con 250.000 €) y AJD 1 %; **Madrid** −10 % de cuota ≤ 250.000 € (−1.500 € en el caso por defecto: la cifra de 67.500 € del lead, el veredicto y la FAQ 1 sería 66.000 € si es vivienda habitual); **Andalucía** 6 %/1 % ≤ 150.000 €; **Baleares** AJD 1 % en la primera vivienda ≤ 270.151,20 €. Las rebajas para jóvenes son muy comunes y grandes: CyL 4 % (< 36), Cantabria 4 % (< 40), Andalucía 3,5 % (< 35, ≤ 150k), Extremadura 4 % (< 36, con renta), Baleares 0,5 % de AJD (< 36).
4. **Valor de referencia del Catastro** (TRLITPAJD art. 10.2): la base es el mayor entre precio y valor de referencia. No se declara en la página (supuesto 3 del Constructor). Es frecuente y puede subir el ITP.

## Cambios obligatorios
| Archivo | Qué |
|---|---|
| data/params.json `vivienda_2026.ccaa.baleares.ajd` (y regenerar el JS) | `{"tipo":"bloque","tramos":[[0,1.5],[999999.99,2]]}` (art. 17 bis, «igual o superior»), con norma «DLeg 1/2014, arts. 10, 15 y 17 bis». Oráculo: AJD de Baleares 2 % si v ≥ 1.000.000 |
| test.json (+ oráculo) | Casos nuevos: Baleares nueva 1.000.000 → ajd 20.000; 999.999 → 14.999,99; 1.200.000 → impuestos 144.000. Madrid nueva 120.000 → ajd 480. CyL usada 400.000 → itp 35.000 |
| params `clm.red` | «…de hasta **240.000 €**… (art. 21.2 de la Ley 8/2013, redacción de la Ley 1/2026)»; añadir el 6 % de ITP en el mismo supuesto (art. 19.2); fuente: consolidado de 2023 + Ley 1/2026 DOCM-q-2026-90065 |
| params `madrid.red` | Añadir: «bonificación del 10 % del ITP y del AJD si es tu vivienda habitual y vale hasta 250.000 € (arts. 30 bis y 38 bis)» |
| params `cantabria.red` | Añadir: 4 % para menores de 40 años (art. 9.3.c) y AJD del 1 % en vivienda habitual (0,1 % para menores de 40 y otros, art. 13.3-4) |
| params `baleares.red` | Sustituir el genérico por: «AJD del 1 % (0,5 % menores de 36) en la primera vivienda habitual de hasta 270.151,20 € (art. 17); 2 % si vale 1 M € o más (art. 17 bis)» |
| JS (nota) para Valencia, Cantabria, Madrid ≤ 250k, Andalucía ≤ 150k y Baleares ≤ 270.151,20 € | **Mínimo**: aviso cuantificado («si va a ser tu vivienda habitual pagarías unos X € menos»). **Recomendado**: un selector «¿Será tu vivienda habitual?» (por defecto sí) que aplique solo estas 5 reglas sin requisitos personales, con re-verificación |
| content HTML, supuestos | «en el resto es un tipo único» → «en Baleares sube al 2 % desde 1.000.000 €; en el resto es un tipo único». Añadir la frase del valor de referencia del Catastro (art. 10.2 TRLITPAJD). Tabla: en la cabecera, «tipo general, si no aplicas ninguna rebaja de vivienda habitual» y nota en Valencia (0,1 % → 11,1 % en nueva) |
| JSON lead / veredicto / FAQ 1 | Añadir «con el tipo general» a «67.500 € en una usada de Madrid»; FAQ 2: «del 0,75 % (Madrid) al 1,5 % **para 250.000 €** (0,4 % en Madrid hasta 120.000 € y 2 % en Baleares desde 1 M €)» |
| JSON `sources` y nota del JS | El AJD de la hipoteca lo paga el banco por el **art. 29 del TRLITPAJD (RDL 17/2018)**, no por la Ley 5/2019; citarlo. Baleares: añadir art. 17 bis |

## Texto ≤ cálculo (resto)
Lead: «7 %–11 % usada; 11,75 %–12,5 % nueva» comprobado para 250.000 € con tipo general (máximo Cataluña 10 %, mínimo Madrid 6 %; nueva Madrid 11,75 %, máximo 12,5 %). Tabla del HTML: 6/6 cifras ok. «Mueve unos 10.000 €» ok. FAQ 4 (625 € / 538 €) ok (537,83). «Los bancos suelen financiar hasta el 80 %» se acepta: va con «suelen» y «no es norma legal». «Nunca los dos grupos a la vez» es correcto (art. 7.5 TRLITPAJD).

## Supuestos
Aceptables y declarados como hipótesis editables: gastos de 2.500 € («estimación… no es una cifra oficial» en la etiqueta, la FAQ 3, la nota y las fuentes); plazo de 25 años (nota, HTML, fuentes); rentabilidad; entrada del 20 %; cuota fija del art. 31.1 omitida (céntimos por folio: irrelevante). El AJD sobre el precio sin IVA es correcto, no una hipótesis.
Euríbor + 1 punto: hoy da 4,247 % (Euríbor de septiembre 3,247 %, BCE, live.json). Es razonable y prudente como valor por defecto (los diferenciales variables habituales están en 0,5–1 punto). Está en la etiqueta y en «Hipótesis editables» de las fuentes; en la nota del resultado conviene escribir «Euríbor a 12 meses (X %) más 1 punto, hipótesis editable», no solo «un diferencial». No es obligatorio.
Erróneo: ninguno de los declarados. Faltaba el del valor de referencia (cambio obligatorio arriba).
Re-verificación: Sonnet basta (oráculo + ops/check.py + mis 10 casos de la tabla anterior, con el de Baleares esperando 144.000 €). Opus solo si se implementa el selector de vivienda habitual.
