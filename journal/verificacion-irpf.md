# Verificación fiscal independiente — `declaracion-conjunta-o-individual` (IRPF 2026)

Verificador: Opus (independiente) · Fecha: 2026-10-02 · Alcance: solo lectura del proyecto; implementación propia en Python (`scratchpad/ver/irpf.py`), construida desde el BOE y la AEAT **antes** de abrir el `.js`, el `.test.json`, `content/` o `params.json`.

## VEREDICTO: **PUBLICABLE CON CAMBIOS**

El motor de cálculo es correcto en lo esencial: en los 12 escenarios coincide **al céntimo** con mi implementación independiente, y en un barrido aleatorio de 600 casos solo discrepa en 4, todos por el mismo defecto acotado (límite de la deducción DA 61.ª en conjunta con ahorro). Las tablas de `params.json` (estatal, ahorro, 15 escalas autonómicas, mínimos, 3.400/2.150, art. 19.2.f, art. 20 y DA 61.ª) coinciden **todas** con lo que obtuve yo del BOE. Antes de publicar hay que cambiar: (1) un error de fórmula (DA 61.ª en conjunta), (2) un caso que no es legal (monoparental sin hijos menores) y (3) dos afirmaciones del texto que son incorrectas o engañosas («aprovecha el mínimo personal del cónyuge sin ingresos» y «conviene cuando los sueldos son muy desiguales»).

---

## 1. Fuentes oficiales que consulté (por mi cuenta)

| Qué | Fuente |
|---|---|
| Ley 35/2006, texto consolidado (arts. 19, 20, 56-58, 61, 63, 66, 74, 76, 82-84, DA 61.ª) | https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764 (descargado el 2/10/2026, última actualización 30/09/2026) |
| DA 61.ª redacción RDL 5/2026 (590,89 €; 17.094; 20.048,45; 0,2) con efectos desde el 1/1/2026 | Mismo texto consolidado; RDL 5/2026 BOE-A-2026-3810, **convalidado** (Resolución del Congreso de 18/03/2026, BOE-A-2026-6483, según la API de análisis del BOE) |
| 2.000 € «por unidad familiar» en conjunta | AEAT, Manual Renta 2025, «Análisis de los gastos del art. 19.2.f)»: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c03-rendimientos-trabajo/rendimiento-neto-trabajo-integrar-base-imponible/fase-2-determinacion-rendimiento-neto/particular-analisis-gastos-articulo-19_2_f-lirpf.html |
| Art. 20 en conjunta: sobre la suma de rendimientos, sin multiplicar | AEAT, Manual Renta 2025, Fase 3.ª: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c03-rendimientos-trabajo/rendimiento-neto-trabajo-integrar-base-imponible/fase-3-determinacion-rendimiento-neto-reducido.html |
| DA 61.ª (requisitos, límite proporcional, ejemplos 1-3) | AEAT, Manual Renta 2025, cap. 18: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c18-cuota-liquida-resultante-autoliquidacion/deducciones-cuota-liquida-total/deduccion-obtencion-rendimientos-trabajo.html (no dice nada sobre la conjunta) |
| Escalas autonómicas 2025, para contrastar | AEAT, Manual Renta 2025, cap. 15, «Gravamen autonómico» (15 páginas, una por comunidad): https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-autonomico.html |
| Escalas y mínimos autonómicos 2026 (última versión de cada bloque, API de datos abiertos del BOE) | Madrid BOCM-m-2010-90068 · Andalucía BOE-A-2021-17915 · Aragón BOA-d-2005-90006 · Asturias BOE-A-2015-945 · Baleares BOE-A-2014-6925 · Canarias BOC-j-2009-90008 · Cantabria BOCT-c-2008-90028 · Castilla-La Mancha BOE-A-2014-1368 · Castilla y León BOCL-h-2013-90254 · Cataluña BOE-A-2024-6951 · Extremadura BOE-A-2018-8159 · Galicia BOE-A-2011-18161 · Murcia BOE-A-2011-10542 · La Rioja BOE-A-2017-13750 · C. Valenciana BOE-A-1998-8202 (todas en https://www.boe.es/buscar/act.php?id=…) |
| Cambios de 2026 que encontré en el BOE | Extremadura: Ley 2/2026, de 3 de agosto (BOE-A-2026-17839), con efectos 1/1/2026 · C. Valenciana: Ley 5/2026, de 31 de julio, art. 18 (BOE-A-2026-19331), con efectos 1/1/2026, y otra escala más (DT 3.ª) desde 2027 · Canarias: Ley 9/2025 (BOE-A-2026-7560), escala con efectos 2025 que sigue en 2026 · Asturias: Ley 3/2025 (BOE-A-2025-25707) |
| Castilla y León 2027 (no afecta a 2026) | Anteproyecto: primer tramo al 8,75 % desde el 1/1/2027 (Diario de Castilla y León, 1/9/2026); no está en el BOE |

## 2. Los 12 escenarios: mi cálculo frente a la calculadora

Inputs: `tipo, b1, b2, ss, ahorro, hijosMenores (<3), hijosMayores (3-24), ccaa`. «Individual» es la suma de los dos cónyuges. Tolerancia: 1 €.

| # | Escenario | Indiv. cónyuge 1 (mío) | Indiv. cónyuge 2 (mío) | Indiv. suma: mío / calc. | Conjunta: mío / calc. | Diferencia: mío / calc. | OK |
|---|---|---|---|---|---|---|---|
| S1 | Madrid, matrimonio, 40.000/0, SS 2.540, sin hijos | 7.224,68 | 0 | 7.224,68 / 7.224,68 | 6.268,80 / 6.268,80 | 955,88 / 955,88 | ✔ |
| S2 | Madrid, matrimonio, 40.000/0, 1 hijo <3 + 1 mayor | 6.489,08 | 0 | 6.489,08 / 6.489,08 | 4.748,99 / 4.748,99 | 1.740,09 / 1.740,09 | ✔ |
| S3 | Cataluña, matrimonio, 55.000/12.000, ahorro 2.000, 2 hijos | 12.931,91 | 0 | 12.931,91 / 12.931,91 | 15.685,25 / 15.685,25 | −2.753,34 / −2.753,34 | ✔ |
| S4 | Andalucía, matrimonio, 30.000/28.000, 1 hijo | 4.642,73 | 4.080,83 | 8.723,55 / 8.723,55 | 12.216,29 / 12.216,29 | −3.492,74 / −3.492,74 | ✔ |
| S5 | C. Valenciana, monoparental, 24.000, 2 hijos (1 <3) | 1.516,08 | — | 1.516,08 / 1.516,08 | 998,25 / 998,25 | 517,83 / 517,83 | ✔ |
| S6 | Galicia, monoparental, 15.000, 2 hijos (art. 20 y DA 61.ª) | 0 | — | 0 / 0 | 0 / 0 | 0 / 0 | ✔ |
| S7 | Castilla y León, matrimonio, 16.000/0, 1 hijo | 0 | 0 | 0 / 0 | 0 / 0 | 0 / 0 | ✔ |
| S8 | Murcia, matrimonio, 18.000/9.000, 2 hijos (rentas bajas) | 153,25 | 0 | 153,25 / 153,25 | 2.066,92 / 2.066,92 | −1.913,67 / −1.913,67 | ✔ |
| S9 | Madrid, matrimonio, 120.000/30.000, ahorro 40.000, 3 hijos | 41.877,72 | 7.979,04 | 49.856,76 / 49.856,76 | 55.952,54 / 55.952,54 | −6.095,78 / −6.095,78 | ✔ |
| S10 | C. Valenciana, matrimonio, 70.000/70.000, ahorro 10.000 | 19.531,56 | 19.531,56 | 39.063,11 / 39.063,11 | 50.946,69 / 50.946,69 | −11.883,58 / −11.883,58 | ✔ |
| S11 | Extremadura, matrimonio, 25.000/5.000, 2 hijos <3 | 2.328,88 | 0 | 2.328,88 / 2.328,88 | 1.632,57 / 1.632,57 | 696,30 / 696,30 | ✔ |
| S12 | Asturias, monoparental, 45.000, ahorro 8.000, 1 hijo <3 | 10.014,77 | — | 10.014,77 / 10.014,77 | 9.204,22 / 9.204,22 | 810,55 / 810,55 | ✔ |

La calculadora no devuelve la cuota de cada cónyuge por separado, así que el desglose por cónyuge es solo mío; la suma sí la he comparado. Comprobé S1 también a mano: base de 35.460 €, cuota estatal 3.883,60 € y autonómica 3.341,07 €.

**Barrido extra**: 600 casos aleatorios (15 comunidades, ahorro de 0 a 250.000 €, de 0 a 4 hijos, sueldos de 0 a 320.000 €). Discrepan 4 casos (sección 3.1).

**Ojo con el tipo de dato**: si `hijosMenores` o `hijosMayores` llegan como texto («1»), `minHijos` concatena (`may + men` → «01») y el resultado sale disparatado (S2 daría 1.322 € en vez de 6.489 €). En la página no ocurre, porque `leer()` aplica `parseFloat`; solo afecta a quien llame a `calcular()` directamente. Es robustez, no un error visible.

## 3. Discrepancias analizadas

### 3.1 Límite de la DA 61.ª en conjunta con ahorro — **ERROR de la calculadora (corregir)**
- Código: `lim = ci * Math.min(1, rn / (big + bia))`. `rn` es el rendimiento neto del trabajo **antes** de la reducción por conjunta, y `big` es la base general **después** de restar 3.400 o 2.150 €. El numerador y el denominador están en bases distintas: la proporción sale inflada y a menudo topa en 1. Así, la deducción puede comerse también la cuota que corresponde al ahorro.
- Norma: DA 61.ª.1, último párrafo: el límite es la parte de la suma de las cuotas íntegras «que proporcionalmente corresponda a los rendimientos netos del trabajo … computados para la determinación de las bases liquidables». La parte del trabajo que entra en la base liquidable es `big` (art. 84.2.3.º y 4.º: la reducción se aplica primero a la base general).
- Casos (cuota conjunta: calculadora / correcta con `big/(big+bia)`):
  - Monoparental, Canarias, 17.000 €, SS 1.080, ahorro 6.000, 1 hijo: 257,75 / 401,68.
  - Matrimonio, La Rioja, 19.250/0, SS 1.222, ahorro 3.000, 1 hijo <3 + 1 mayor: 0 / 9,08.
  - Matrimonio, Canarias, 16.500/0, SS 1.048, ahorro 6.000: 212,82 / 491,13.
- Peor caso que encontré: la conjunta sale **278 € más barata** de lo que debería. Solo pasa con rentas del trabajo familiares por debajo de 20.048 € y ahorro entre 1 € y 6.500 €. El sesgo favorece a la conjunta, así que puede cambiar el ganador en casos ajustados.
- Corrección: `ci * (big / (big + bia))`. Como alternativa defendible, `rn / (rn + s)`, calculando las dos magnitudes antes de la reducción; da valores intermedios (342,07 / 7,27 / 364,63). La de ahora no es defendible.

### 3.2 Monoparental sin hijos menores — **ERROR (caso no legal)**
- Con `tipo=mono` y 0 hijos, la calculadora dice que la conjunta ahorra 597,70 € (Madrid, 30.000 €). Lo mismo pasa si todos los hijos tienen entre 18 y 24 años, porque el selector «3 a 24 años» los junta con los de 3 a 17.
- Norma: art. 82.1.2.ª. La modalidad 2 la forman el padre o la madre con los hijos **menores** (o mayores incapacitados judicialmente) que convivan con él. Sin ningún hijo menor no hay unidad familiar, y la conjunta no existe.

### 3.3 Nada más
Todo lo demás coincide: escalas, mínimos, reparto 50/50 de los mínimos en individual (art. 61.1.ª), un único mínimo del contribuyente en conjunta (art. 84.2.2.º), el sobrante del mínimo que pasa al ahorro (art. 56.2), la reducción por conjunta que pasa al ahorro, el art. 20 con su condición de 6.500 € y la DA 61.ª sobre rendimientos **íntegros**.

## 4. Contraste de `params.json` → `irpf_2026`

| Tabla | params.json | Lo que obtuve yo (fuente) | Resultado |
|---|---|---|---|
| Escala estatal general | 9,5 / 12 / 15 / 18,5 / 22,5 / 24,5; tramos 12.450 / 20.200 / 35.200 / 60.000 / 300.000 | Art. 63.1, igual | ✔ |
| Ahorro (cada mitad) | 9,5 / 10,5 / 11,5 / 13,5 / 15; tramos 6.000 / 50.000 / 200.000 / 300.000 | Arts. 66.1 y 76 (Ley 7/2024), igual | ✔ |
| Conjunta | 3.400 / 2.150 | Art. 84.2.3.º y 4.º | ✔ |
| Mínimos estatales | 5.550; 2.400 / 2.700 / 4.000 / 4.500; +2.800 | Arts. 57 y 58 | ✔ |
| Art. 19.2.f y art. 20 | 2.000; 7.302; 14.852; 1,75; 17.673,52; 2.364,34; 1,14; 19.747,5; 6.500 | Igual (RDL 4/2024) | ✔ |
| DA 61.ª | 590,89; 17.094; 20.048,45; 0,2; 6.500 | Igual (RDL 5/2026, convalidado) | ✔ |
| Escalas de las 15 comunidades | — | Las 15 iguales al BOE. Extremadura y C. Valenciana ya llevan las escalas de 2026 (Ley 2/2026 y Ley 5/2026) | ✔ |
| Mínimos propios | Madrid, Andalucía, Asturias, Baleares (+10 % del 2.º al 4.º hijo), Canarias, Galicia, C. Valenciana | Igual. **No falta ninguna comunidad con mínimos distintos de los estatales** | ✔ |
| Texto de `minimo_nota` | CyL y Cataluña: «sin mínimos propios en el texto consolidado» | **Inexacto**: CyL tiene art. 1 bis y Cataluña art. 611-2, ambos con las mismas cuantías que el Estado. La Rioja tiene el art. 31 bis (solo discapacidad). Al cálculo no le afecta | corregir la redacción |
| Nota de CyL | «el texto consolidado no se ha actualizado desde 2022» | El art. 1 es de la Ley 2/2022, pero la consolidación del BOE se actualizó el 17/07/2024. La rebaja anunciada es para 2027 (anteproyecto) | corregir la redacción |

### Supuestos del constructor

| Supuesto | Valoración | Por qué |
|---|---|---|
| 2.000 € una sola vez por unidad familiar (corrigió al investigador) | **Correcto** | La AEAT dice literalmente que los gastos del art. 19.2.f «se aplican por unidad familiar en el supuesto de tributación conjunta» |
| Art. 20 sobre la suma, una sola vez | **Correcto** | La AEAT (Fase 3.ª) dice que se calcula sobre la cuantía conjunta, sin multiplicar por el número de perceptores |
| DA 61.ª sobre la suma de rendimientos íntegros en conjunta | **Aproximación aceptable, no confirmada** | Encaja con el art. 84.2 («idéntica cuantía», sin multiplicar) y con lo que hace la AEAT con el art. 20, pero la AEAT no lo dice expresamente para la DA 61.ª. Para parejas con dos sueldos bajos (por ejemplo 15.000 + 8.000) quita la deducción en conjunta: es conservador para la conjunta. Mantenerlo y avisarlo en el texto |
| Cotización repartida en proporción al sueldo | **Aproximación aceptable** | Es exacta si nadie supera la base máxima de cotización. Si uno la supera, el error en la cuota individual es pequeño (unos −114 € en S9 con las cotizaciones reales). Recomendable: pedir la cotización de cada cónyuge o avisarlo |
| Ahorro a partes iguales | **Aceptable si es ganancial** | El art. 11.3 imputa los rendimientos del capital al titular, y los bienes gananciales por mitad. Hay que decir en la página «si las cuentas o acciones son de los dos» |
| Hijos de 3-24 primero en el orden y menores de 3 al final | **Correcto** | El orden va por edad; el incremento de +2.800 € no depende del puesto |

## 5. Revisión del texto (`content/…html` y JSON)

1. **Incorrecto**. FAQ «¿Cuándo conviene la declaración conjunta?» dice: «aprovecha el mínimo personal que el cónyuge sin ingresos no podría usar por su cuenta». El HTML, en «A favor de la conjunta», dice: «el mínimo personal del cónyuge sin ingresos, que en individual se pierde». En conjunta solo hay **un** mínimo del contribuyente (art. 84.2.2.º); el propio HTML lo dice en «En contra» y se contradice. Lo que de verdad se recupera es la **mitad del mínimo por descendientes** que el cónyuge sin ingresos no puede usar en individual. Prueba: S1 (sin hijos), donde la ventaja de 955,88 € sale casi entera de los 3.400 € × 27,8 % de tipo marginal.
2. **Engañoso**. El lead, el veredicto, la FAQ 1 y la intro del HTML dicen que conviene si «hay mucha diferencia entre sueldos» o si los sueldos son «muy desiguales». La propia calculadora lo desmiente: con 55.000/12.000 gana la individual por 2.753 € (S3). El umbral del segundo sueldo bruto sale de unos **2.300 € a 7.300 €** al año (unos 3.600 € sin hijos, unos 5.500-7.300 € con hijos), según mi barrido en Madrid y Cataluña con primeros sueldos de 20.000 a 150.000 €. Hay que reformularlo como «cuando uno de los dos no tiene ingresos o gana muy poco (por debajo de unos pocos miles de euros al año)».
3. **No es correcto para monoparental**. La nota de resultado dice «En la conjunta firman los dos y responden solidariamente», también cuando el tipo es monoparental.
4. **Aceptable**. Modalidad 1 «con sus hijos menores»: falta «o mayores incapacitados judicialmente» (art. 82.1.1.ª b). Es una omisión menor.
5. **Correctas y con fuente**: art. 83 (la opción no vincula para otros años, abarca a todos, no se cambia tras el plazo y la regla de los 10 días); art. 82.3 (situación a 31 de diciembre); art. 84.6 (responsabilidad solidaria); la reducción de 2.150 € no se aplica si se convive con el otro progenitor (art. 84.2.4.º). No hay fechas de campaña inventadas, porque se remite a la AEAT.
6. **Sources**: las cifras están citadas. Solo hay que corregir la frase de CyL («consolidado sin actualizar desde 2022»; ver sección 4).

## 6. Cambios requeridos (archivo → qué)

1. `projects/decidir/calcs/declaracion-conjunta-o-individual.js`, función `liquidar`: cambiar `lim = big + bia > 0 ? ci * Math.min(1, rn / (big + bia)) : 0` por `lim = big + bia > 0 ? ci * big / (big + bia) : 0`.
2. `projects/decidir/calcs/declaracion-conjunta-o-individual.test.json`: añadir 2 casos de regresión con los valores correctos de cuota conjunta:
   - `{tipo:"mono", b1:17000, b2:0, ss:1080, ahorro:6000, hijosMenores:0, hijosMayores:1, ccaa:"canarias"}` → conjunta 401,68 € (individual ≈ 641,25 €).
   - `{tipo:"mat", b1:16500, b2:0, ss:1048, ahorro:6000, hijosMenores:0, hijosMayores:0, ccaa:"canarias"}` → conjunta 491,13 €.
   Antes, revisar si algún caso existente cambia.
3. `…js` (`pintar` y/o `comparar`) y `…json` (inputs): en monoparental exigir **al menos un hijo menor de 18 años**. Opciones: separar «3 a 17» y «18 a 24», o añadir un aviso o bloqueo: «La modalidad 2 exige convivir con al menos un hijo menor (art. 82.1.2.ª)». Con 0 hijos no se debe mostrar ninguna ventaja de la conjunta.
4. `…json` (`lead`, `veredicto`, FAQ 1) y `content/…html` (intro y «Por qué a veces sale mejor»): quitar «muy desiguales» o «mucha diferencia entre sueldos» y poner el criterio del segundo sueldo muy bajo. Sustituir «el mínimo personal del cónyuge sin ingresos» por «la mitad del mínimo por hijos que el cónyuge sin ingresos no puede aprovechar».
5. `…js` (`pintar`, nota): en monoparental no decir «firman los dos».
6. `…json` (FAQ 5 o texto de supuestos) y nota en la página: decir que el ahorro se reparte al 50 % «si es ganancial» y que la cotización se reparte en proporción al sueldo.
7. `projects/decidir/data/params.json` → `irpf_2026.ccaa.cyl` y `.cataluna.minimo_nota`, y nota de CyL; y la frase equivalente en `sources` del JSON: corregir la redacción como en la sección 4.
8. Opcional (robustez): en `comparar`, convertir `hijosMayores` y `hijosMenores` con `+d.x || 0`.

## 7. Confianza por comunidad (escala y mínimos 2026)

| Comunidad | Confianza | Nota |
|---|---|---|
| Andalucía, Aragón, Asturias, Baleares, Canarias, Cantabria, Castilla-La Mancha, Cataluña, Galicia, Madrid | **A** | Versión vigente en el BOE consolidado igual a la del Manual Renta 2025 de la AEAT, sin cambios para 2026 en el consolidado. Aragón: consolidación del 17/07/2025, algo más antigua; no encontré ninguna ley de 2026 |
| Extremadura | **A** | Ley 2/2026 (BOE-A-2026-17839), con efectos 1/1/2026; ya incorporada |
| C. Valenciana | **A** | Ley 5/2026, art. 18 (BOE-A-2026-19331), con efectos 1/1/2026; ya incorporada. Atención: en 2027 hay otra escala (DT 3.ª) |
| Castilla y León | **A−** (la calculadora la marca B) | Art. 1 de la Ley 2/2022 y art. 1 bis con mínimos iguales a los estatales. La rebaja anunciada es para 2027. El aviso «orientativo» se puede mantener por prudencia o quitar |
| Región de Murcia | **A−** (marcada B) | El art. 2 coincide con la AEAT 2025. La DA 5.ª solo cubre 2019-2022. No encontré ninguna escala para 2026 |
| La Rioja | **A−** (marcada B) | El art. 31 ter solo obliga a deflactar si el IPC riojano de diciembre supera el 3 %, y aun así necesitaría una ley. El IPC de La Rioja en noviembre de 2025 fue del 2,4 % (INE) y en el BOE no hay ninguna ley que deflacte. No verifiqué el dato exacto de diciembre |

## 8. Resumen de supuestos
- **Correctos**: los 2.000 € una sola vez por unidad familiar; el art. 20 sobre la suma; el orden de los hijos; el mínimo único en conjunta; el reparto 50/50 de los mínimos por hijos en individual.
- **Aproximaciones aceptables, si se avisan**: la DA 61.ª sobre la suma en conjunta (la AEAT no lo confirma, pero es coherente con el art. 84.2); la cotización en proporción al sueldo; el ahorro a partes iguales (solo si es ganancial).
- **Erróneos**: la proporción del límite de la DA 61.ª en conjunta; la monoparental sin hijos menores; las afirmaciones del texto sobre «el mínimo personal del cónyuge» y los «sueldos muy desiguales».

---

## Re-verificación (2026-10-02, después de las correcciones del constructor)

**Cambio en mi implementación:** el límite de la DA 61.ª ahora usa `big/(big+bia)`, la proporción del trabajo dentro de la base liquidable, tal como recomendé. La monoparental exige al menos un hijo menor de 18 años. Los hijos de 18 a 24 años (`hijosAdultos`) cuentan como «mayores» para el mínimo por descendientes.

1. **12 escenarios:** fallan **0 de 12**. Coinciden al céntimo en la cuota individual, la conjunta y la diferencia, con los mismos valores que la tabla de la sección 2.
   **Barrido aleatorio:** 1.000 casos nuevos, con `hijosAdultos`, ahorro hasta 250.000 € y las 15 comunidades. Fallan **0 de 1.000**. Hay 63 casos de monoparental sin hijos menores, y la calculadora los marca todos como `invalido`, igual que mi implementación.
2. **S3:** sí, son exactamente mis inputs: `mat`, 55.000/12.000, SS 4.255, ahorro 2.000, 0 hijos menores de 3, 2 de 3-17, Cataluña. Mi resultado independiente: individual 12.931,91 €, conjunta 15.685,25 €, diferencia **−2.753,34 €**. Es correcto.
3. **Los 4 casos nuevos de `test.json`, comprobados con mi implementación:**
   - Monoparental en Canarias: conjunta 401,68 € e individual 641,25 €. ✔
   - Matrimonio en Canarias: conjunta 491,13 €. ✔
   - Monoparental solo con hijos de 18 a 24 años: `invalido`. ✔
   - 55.000/12.000 en Cataluña: −2.753,34 €. ✔
4. **Texto (HTML y JSON):** las afirmaciones legales ya son correctas y llevan fuente:
   - un único mínimo personal en conjunta (art. 84.2.2.º);
   - la modalidad 2 exige hijos menores o mayores incapacitados judicialmente (art. 82.1.2.ª);
   - art. 83 y art. 84.6 (este último, ahora solo para el matrimonio);
   - los supuestos se declaran, y la DA 61.ª en conjunta figura como criterio no confirmado por la AEAT;
   - `params.json` lleva bien las notas de Castilla y León, Cataluña, Murcia y La Rioja.
   Comprobé también que «con 55.000 y 12.000 € gana la individual» se cumple con 0 a 4 hijos en Madrid, Cataluña y Valencia.
   **Queda una cifra demasiado estrecha, y el error es mío:** la horquilla del umbral «2.300-7.300 €» salió de mi barrido, que solo tenía primeros sueldos de 20.000 € o más y como mucho 3 hijos. Con un barrido más amplio (primer sueldo de 14.000 a 200.000 €, de 0 a 4 hijos, 5 comunidades), el umbral va de unos **20 € a 13.500 €**. El percentil 10 está en 1.850 € y el 90 en 10.400 €. Con primeros sueldos bajos, de unos 14.000 €, no hay umbral, porque no se paga cuota. Un ejemplo: Madrid, 25.000 € y 4 hijos (2 menores de 3) da un umbral de 13.487 €. La FAQ 1 lo dice de forma tajante («tiene que quedar por debajo de unos 2.300 a 7.300 €»), y es inexacto para familias numerosas.

### VEREDICTO FINAL: **APTA PARA PUBLICAR tras un retoque menor de texto**
El cálculo, las tablas, la validación y las afirmaciones legales están verificados. Falta un único cambio, que no toca el motor:
- `projects/decidir/calcs/declaracion-conjunta-o-individual.json`: en `lead`, `veredicto` y la FAQ 1, cambiar «del orden de 2.300 a 7.300 €» (y el «tiene que quedar por debajo de…» de la FAQ 1) por algo como «normalmente por debajo de unos 2.000-10.000 € brutos al año, y más con familias numerosas; la calculadora te da tu umbral exacto».
- `projects/decidir/content/declaracion-conjunta-o-individual.html`: el mismo cambio en la intro y en «Resultado típico».
Con ese cambio hecho, la calculadora queda APTA PARA PUBLICAR sin otra verificación, porque no afecta al cálculo.
