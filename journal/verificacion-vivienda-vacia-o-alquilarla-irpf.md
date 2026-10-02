# Verificación fiscal · vivienda-vacia-o-alquilarla-irpf · 2026-10-02 (Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 1 · 8 0 · N 1 · R 1 · S 0 · otros 0 (ninguno cambia fórmula ni el ejemplo; el T cambia qué opción de «rev» elige parte de los usuarios)
Paso 0: mi lectura coincide con el bloque INTERPRETACION (85.1 por días; 23.1 + 23.2 solo sobre positivo; art. 24 = max(reducido, imputación de los días alquilados); días vacíos imputan). Oráculo re-ejecutado: 918 casos, 0 disc.; ops/verif/vivienda-vacia-o-alquilarla-irpf.py: 4 casos nuevos OK.

## Norma leída (API BOE, consolidado BOE-A-2006-20764, 2/10/2026)
- a85: 3 versiones; rige la de BOE-A-2014-12327 (vig. 1/1/2015). La del RDL 26/2026 (escala 1,1-3 %, vig. 1/1/2027) no aplica: derogado (BOE-A-2026-20526, leído: «Acuerdo de derogación del Real Decreto-ley 26/2026»).
- a24: rige la original (2006): «no podrá ser inferior al que resulte de las reglas del artículo 85». La del RDL («porcentaje medio efectivo», 2027) no aplica.
- a23: rige BOE-A-2023-12203 (vig. 1/1/2024): reducciones 90/70/60/50 «sólo ... sobre los rendimientos netos positivos»; 23.1.a.1.º tope intereses + reparaciones = ingresos íntegros, exceso 4 años.
- DT 38.ª (bloque dt-6): rige la de Ley 12/2023 (contratos anteriores → 23.2 a 31/12/2021 = 60 %). La del RDL (vig. 1/10/2026, apartado 2 y 80 %) no aplica.
- a48.a: rendimientos e imputaciones se integran y compensan «entre sí, sin limitación alguna» en la base general.
- DA 55.ª (bloque da-10), NO leída por el Constructor: tras las derogaciones de los RDL 9/2024, 16/2025, 2/2026 y 26/2026, su texto vigente es solo «durante el período impositivo 2023» (1,1 % si la revisión entró en vigor desde 1/1/2012). El RDL 26/2026 la extendía a 2026; derogado. Para 2026 rige la regla de 10 períodos del 85.1 (revisión en vigor 2016-2026). El Manual Renta 2025 aún dice «a partir de 1 de enero de 2012»: un usuario que lo lea elegirá mal.

## Supuestos B del Constructor
1. Mínimo art. 24 sobre días alquilados y reducción antes del mínimo: DEFENDIBLE. Manual 2025 «Rendimiento neto reducido»: el mayor entre el rendimiento «una vez aplicadas ... las reducciones» y el mínimo; «Rendimiento mínimo computable»: la cuantía del «régimen especial de imputación», que incluye la proporción por días del 85.1. Se mantiene confianza B solo por los días (sin literal expreso).
2. Gastos por días alquilados: CONFIRMADO para intereses (Manual, «Intereses y demás gastos de financiación»: «se calculan de forma proporcional al número de días ... en los que la vivienda se encuentre arrendada», por correlación ingresos-gastos) y amortización; para IBI, comunidad y seguro es la misma lógica de correlación. Recomendado (no obligatorio): citar el Manual en «Supuestos» en lugar de «nuestra lectura».
3. Pérdidas: la LEY SÍ las compensa (art. 48.a, sin límite, con trabajo y con la imputación de los días vacíos del mismo piso); solo el exceso de intereses + reparaciones sobre ingresos no es deducible ese año (23.1.a.1.º). El modelo usa max(rendimiento, 0) + imputación días vacíos: sobrestima el IRPF del alquilado cuando hay pérdida (caso «pérdida 60 días»: 32,55 € frente a unos −569 € de ahorro real). Ocurre solo con renta < gastos y refuerza «alquilar»: el veredicto no cambia, se acepta como límite. Lo que no se acepta es la frase, que lo presenta como regla legal (cambio N).
4. Recargo IBI (TRLRHL 72.4): no toca el IRPF de ninguna opción; solo sube el coste de «vacío» y refuerza alquilar. Declarado; correcto como límite.

## Texto ≤ cálculo, absolutos, citas (muestreo)
- Lead, veredicto y FAQ 1-4: cifras recalculadas (660/198/−7.198; 9.600−7.000, 1.300 → 390, 2.210; umbral 693,33 y 783,33; familiar 650 → 660 de base, 198 €): demostradas.
- «alquilarlo solo te hace pagar más IRPF si el rendimiento neto, ya reducido, supera esa imputación»: demostrada (cuotaB > cuotaA ⇔ redf > imputación de los días alquilados), también con la compensación legal de pérdidas.
- FAQ4 «No»: demostrada (con familiar, ≥ que vacío y ≥ que con un tercero a la misma renta).
- Citas a85 párr. 1-2, a24 y a23.1.b/23.2: literales coinciden con la versión vigente. sources: correcto.
- Forales: País Vasco y Navarra excluidos (bien). Ceuta y Melilla: justificado (deducción 60 %, art. 68.4). Canarias: aplica la LIRPF sin especialidad en arts. 23/24/85; recomendado quitarla de la lista de exclusiones (no obligatorio).

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | T | calcs/…json (ayuda de «rev», FAQ2), content «Cómo se calcula» (Vacío), params alquiler_irpf_2026.fuente_85 | Añadir: «En 2026 el 1,1 % exige que la revisión entrara en vigor entre 2016 y 2026. La ampliación a revisiones desde 2012 (disposición adicional 55.ª) solo rige para 2023: el Real Decreto-ley 26/2026, que la extendía a 2026, fue derogado. Si tu municipio se revisó entre 2012 y 2015, en 2026 es el 2 %.» Enlace https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#da-10 (ancla comprobada) | LIRPF 85.1 párr. 2 y DA 55.ª vigente; el Manual 2025 dice lo contrario y el usuario lo leerá |
| 2 | N | calcs/…js (note «Límites») y content «Supuestos» (2.º punto) | Sustituir «las pérdidas no se compensan con otras rentas» por «la calculadora no resta las pérdidas del alquiler de tus otras rentas, aunque la ley sí lo permite (art. 48), salvo el exceso de intereses y reparaciones sobre los ingresos, que se arrastra 4 años (art. 23.1): con pérdidas, el IRPF real del alquilado es menor que el que ves» | Frase presentada como regla legal y falsa (LIRPF 48.a) |
| 3 | R | content (párrafo Vigencia), calcs/…js (note Vigencia), json FAQ5 y lead | Decir que el RDL 26/2026 también cambiaba el art. 23.2 y la DT 38.ª (efectos 1/10/2026) y la DA 55.ª (1,1 % en 2026), y que nada de eso se aplica: se usa la Ley 12/2023 y la DT 38.ª anterior. Hoy solo nombra arts. 24 y 85 «con efectos de 2027» | Los cambios con efecto en 2026 son los de 23.2/DT 38.ª/DA 55.ª, no los de 24/85 |

## Casos nuevos para test.json (valores del oráculo = JS; ops/verif/vivienda-vacia-o-alquilarla-irpf.py)
- familiar con pérdida: V(fam=si, gastos=12000) → redf 660, cuotaB 198, resB −2598, famAplica 1
- familiar con 90 días vacíos, renta 600: minimo 497,26, impdv 162,74, cuotaB 198 (= vacío)
- pérdida con 60 días vacíos (documenta el límite): V(gastos=12000, dv=60) → redf −2005,48, cuotaB 32,55
- 2 % y familiar a 800: redf 1300 (> mínimo 1200), cuotaA 360, cuotaB 390

## Re-verificación (Sonnet)
Ejecutar el oráculo y ops/verif/vivienda-vacia-o-alquilarla-irpf.py; releer solo las frases de los cambios 1-3. Sin Opus: ninguna corrección cambia fórmula ni interpretación.
