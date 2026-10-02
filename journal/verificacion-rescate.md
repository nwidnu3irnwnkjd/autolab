# Verificación fiscal independiente · rescate-plan-pensiones-capital-o-renta · 2026-10-02 (Opus)
VEREDICTO: **NO PUBLICAR** tal cual. El JS hace lo que dice el modelo (0 discrepancias), pero el modelo deja fuera los arts. 19.2.f y 20, y con ellos la afirmación central («la renta nunca paga más que el capital») **es falsa en el ejemplo por defecto** y en ~1/3 de los casos con otras rentas del trabajo de 12.000-19.700 €. Se arregla con un cambio de fórmula y de texto acotado (los parámetros ya están en params `irpf_2026.trabajo`, confianza A); después, re-verificación con Sonnet.
Fuentes que he leído hoy (curl boe.es, consolidado a 30/09/2026): Ley 35/2006 arts. 17.2.a.3.ª, 18.1-2, 19.2, 20 (RDL 4/2024), 57, 58, 63.1, 66.1, nueva deducción por rendimientos del trabajo (RDL 5/2026) y DT 12.ª; RDL 1/2002 art. 8.5, 8.6 y 8.8; Manual de Renta 2025 de la AEAT (40 %). No he localizado en el BOE el TRLIRPF de 2004 (derogado) con el 40 %; el porcentaje queda con confianza B (fuente AEAT).

## 1. Oráculos (tolerancia 1 €)
- Oráculo del constructor: 11 fijos + 600 aleatorios, 0 discrepancias, 0 propiedades rotas. check.py decidir: 1411/1411.
- Oráculo mío (scratchpad verif_rescate.py, escala estatal copiada del BOE, la autonómica de params): **JS = modelo** en Madrid (60.000 / 15.000 / 10 años: capital 20.801, renta 14.480, ahorro 6.321, N óptimo 18), Cataluña (120.000 / 22.000 / 1 hijo / 12 años / 3 %: 50.973 / 37.417 / 13.556 / 13), Valencia (35.000 / 11.000 / 6 años / 1 %: 10.510 / 7.913 / 2.597 / 40) y Andalucía (250.000 / 40.000 / 2 hijos / 20 años / 4 %: 110.900 / 92.500 / 18.400 / 17). Veredicto y nota cuadran con los números del modelo en los 4.

## 2. Discrepancia legal principal: arts. 19.2.f y 20 (pregunta 2 del constructor)
- Las prestaciones del plan son rendimiento del trabajo (17.2.a.3.ª), así que se les aplican los 2.000 € de gastos (19.2.f) y la reducción del art. 20: 7.302 € si el rendimiento neto es ≤ 14.852 €; baja 1,75 por cada euro hasta 17.673,52 €; baja 1,14 por euro hasta 19.747,5 €; es 0 por encima. Para calcular ese tramo, el neto solo descuenta los gastos a)-e). La ley no excluye las prestaciones de planes.
- La reducción que se va perdiendo crea un tramo con marginal efectivo muy alto (×2,75 y ×2,14), así que el impuesto **deja de ser convexo**. Con el capital la reducción se pierde una vez; con la renta, cada año en que el pago sube el rendimiento a esa banda. Mi cálculo con la ley real (otras = pensión íntegra, sin otras rentas que no sean del trabajo por encima de 6.500 €):
  | Caso | Modelo: capital / renta / ahorro | Ley real: capital / renta / ahorro | Mixto real |
  |---|---|---|---|
  | **Defecto Madrid 60.000, 15.000, 10 años** | 20.801 / 14.480 / **+6.321** | 21.669 / 25.393 / **−3.724** | 24.418 |
  | Madrid 20.000, 14.000, 5 años | 5.269 / 4.540 / +729 | 6.252 / 7.782 / −1.530 | 6.233 |
  | Andalucía 60.000, 12.000, 10 años | 20.981 / 14.068 / +6.913 | 21.283 / 17.684 / +3.599 | **12.210 < renta** |
  | Madrid 100.000, 17.000, 10 años | ahorro +11.873 | ahorro +6.381 (N óptimo 5, no 40) | — |
  | Otras ≥ 19.747,5 € (p. ej. 22.000) | = ley real si el usuario mete el neto tras 19.2.f | coincide | — |
  Barrido: con pensiones de 12.000 a 19.700 € y saldos de 15.000 a 120.000 €, la renta paga **más** que el capital en 631 de 2.000 casos y el mixto paga **menos** que la renta en 658. Con otras = 0 el sesgo va al revés (el modelo infravalora la renta). Con la ley real, el IRPF de la renta según N **no es monótono** (defecto: N=3 → 19.420; N=10 → 25.393; N=18 → 29.834), así que tampoco valen «más años no ahorran más» ni «el ahorro se agota a partir de cierto número de años».
- La nueva deducción por rendimientos del trabajo (RDL 5/2026, íntegros laborales < 20.048,45 €) también se pierde si otras rentas distintas de las laborales pasan de 6.500 €, y ahí cuentan los pagos del plan. Afecta a pocos (asalariado con sueldo bajo que rescata): basta con declararlo como límite.

## 3. El 40 % (DT 12.ª, leída en el BOE)
- Apartado 2: la parte de la prestación que corresponde a aportaciones hasta el 31/12/2006 puede aplicar la reducción del art. 17 del TRLIRPF vigente a 31/12/2006 (40 % en capital si han pasado más de 2 años desde la primera aportación, según la AEAT). Apartado 4: solo en el ejercicio de la contingencia o en los 2 siguientes. Para contingencias de 2011-2014 el plazo acababa el octavo ejercicio (ya vencido en 2026) y para las de 2010 o antes, el 31/12/2018. **Sigue vigente** para contingencias desde 2024. El art. 18.1 excluye los porcentajes en renta. «Si cobras después o en renta, la pierdes» es correcto.
- Lo que falla: según la AEAT, en la prestación mixta el beneficiario puede decidir qué parte del capital corresponde a aportaciones anteriores a 2007. La estrategia habitual (capital con 40 % para lo de antes de 2007 y renta para el resto) es un **mixto que puede ganar a la renta pura**. La frase «el mixto solo compensa / solo tiene sentido si necesitas ese dinero ya» (FAQ 4, HTML, nota del JS) es falsa en ese caso y también con el art. 20 (§2).

## 4. Aplicabilidad y casos límite
- País Vasco y Navarra fuera del selector y declarados: bien (tienen reglas forales propias para el capital; no las he verificado). Ceuta y Melilla: declarado (deducción del 60 % del art. 68.4). Aceptable.
- Liquidez (art. 8.8 TRLPFP, leído): desempleo de larga duración, enfermedad grave y aportaciones con ≥ 10 años de antigüedad. En planes de empleo, también si lo permiten el compromiso y las especificaciones (la FAQ 5 dice solo «individuales y asociados»). Tributan igual que las prestaciones (art. 17.2.a.3.ª, párr. 2). En json `sources` se llaman «prestaciones por contingencias especiales»: son supuestos de liquidez, no contingencias.
- Renta en N pagos: el art. 8.5 TRLPFP deja fijar fechas y modalidades al beneficiario «con las limitaciones … de las especificaciones». La frase de la página es correcta; conviene citar el artículo.
- N=1, saldo muy alto, rentabilidad −5/15 %, otras muy altas: sin NaN y el veredicto es coherente dentro del modelo. Mínimo por edad (+1.150/+1.400): sesgo pequeño y declarado; aceptable.
- Ambiguo: «No modela la tributación de lo que ganes con el capital… y favorece a la renta». Omitirla favorece al **capital**. Debe decir «incluirla favorecería aún más a la renta».

## 5. Supuestos
Aceptables y declarados: otras rentas constantes; pagos al inicio de año; descuento a g, de modo que la diferencia es solo IRPF (razonable y bien explicado); mixto = capital en el año 1; escalas de 2026 constantes; sin mínimos por edad ni deducciones. **Erróneo**: excluir los arts. 19.2.f y 20 (es ley aplicable, no una simplificación, y cambia el ganador). El input «otras rentas … neto de gastos» no es compatible con aplicar el art. 20.

## 6. Cambios obligatorios
| Archivo | Qué |
|---|---|
| calcs/…js + oráculo | Base de cada año = I − mín(2.000, I) − red20(I), con I = otras rentas del trabajo íntegras + pago del plan (params `irpf_2026.trabajo`). Input nuevo «otras rentas no del trabajo» (sin art. 20 si pasan de 6.500 €) o supuesto declarado. N óptimo = mínimo global hasta 40 (ya lo es), sin afirmar monotonía. |
| calcs/…json inputs | «otras»: «pensión o sueldo bruto anual (rendimiento íntegro del trabajo, menos cotizaciones)». |
| json lead, veredicto, FAQ 1; HTML lead e intro | Quitar «nunca paga más / igual o menos». Poner: «suele pagar menos con saldos grandes; con pensiones bajas (menos de ~19.750 €) repartir puede costar más porque cada año pierdes la reducción del art. 20». |
| json FAQ 4; HTML «Mixto»; nota del JS | Quitar «solo tiene sentido si necesitas el dinero». Añadir que el mixto puede ganar con aportaciones hasta 2006 (40 % en capital, la parte elegible la decide el beneficiario, AEAT) o con la reducción del art. 20. |
| HTML «Cómo decidir» y ejemplo 1 | Recalcular con el nuevo modelo; quitar «más años no ahorran más» salvo que el número lo demuestre. |
| HTML supuestos / json sources | Quitar «gastos deducibles y reducción art. 20» de lo excluido; corregir «favorece a la renta»; «supuestos de liquidez» en vez de «contingencias especiales»; FAQ 5: planes de empleo si sus especificaciones lo permiten; citar art. 8.5 TRLPFP; límite: deducción RDL 5/2026. |
| test.json | Casos nuevos (ley real, tol 1 €): Madrid 60.000 / 15.000 / 10 años / 2 % → capital 21.669, renta (valor de hoy) 25.393, mixto 50 % 24.418; Madrid 20.000 / 14.000 / 5 años → 6.252 / 7.782; Andalucía 60.000 / 12.000 / 10 años → 21.283 / 17.684 / mixto 12.210; Madrid 60.000 / 0 / 10 años → 15.338 / 0. |
Re-verificación: Sonnet ejecuta el oráculo corregido y estos 4 casos, y relee las frases marcadas. Hace falta otra vez Opus solo si cambia el tratamiento de «otras rentas».

## Re-verificación (2026-10-02, Opus, tras la corrección del constructor)
VEREDICTO FINAL: **PUBLICABLE CON CAMBIOS** (solo texto; ninguna fórmula cambia). Después basta con que Sonnet relea las frases; no hace falta otra vez Opus.
**Números.** El JS actual coincide con mi implementación de los arts. 19.2.f y 20 en 309 casos: los 4 escenarios, los 5 del informe y 300 aleatorios. Coinciden capital, renta, mixto, N óptimo y mixto óptimo; hay 0 diferencias de más de 1 €. Oráculo del constructor: 616 casos, 0 diferencias. ops/verif/…-verificador.py: 0. check.py: 1482/1482.
| Escenario | Capital | Renta (valor de hoy) | Mixto 50 % | N óptimo | Mixto óptimo | Ganador |
|---|---|---|---|---|---|---|
| Madrid 60.000 / 15.000 / 10 años | 21.669 | 25.393 | 24.418 | 3 (19.420) | 100 % | capital |
| Madrid 20.000 / 14.000 / 5 años | 6.252 | 7.782 | 6.233 | 32 (0) | 76 % (5.341) | capital |
| Andalucía 60.000 / 12.000 / 10 años | 21.283 | 17.684 | 12.210 | 27 (0) | 55 % (11.802) | renta |
| Cataluña 120.000 / 22.000 / 1 hijo / 12 años / 3 % | 50.577 | 36.421 | 38.819 (30 %) | 40 | 0 % | renta |
| Valencia 35.000 / 11.000 / 6 años / 1 % | 10.700 | 5.981 | 5.761 | 10 (0) | 33 % (4.496) | renta |
HTML: «sin otras rentas» (32.458 / 0; 13.831 − 2.000 − 7.302 < 5.550) y «otras rentas 400.000» (90.000 = 90.000) son correctos.
**Norma.** La reducción del art. 20 y los 2.000 € se aplican una vez al año, sobre otras rentas + pago. El umbral se mide sobre el íntegro menos las cotizaciones (art. 20, último párrafo: gastos a-e), tal como pide el nuevo campo. La base no baja de 0. Renta: pagos al inicio de cada año, con el saldo restante a g; es razonable y está declarado. N óptimo: mínimo global entre 1 y 40 años. Mixto óptimo: barrido de 0 a 100 % de 1 en 1 sin suponer monotonía; está bien, aunque solo para el N del usuario. La DT 12.ª está bien tratada: no se modela, se declara en lead, FAQ 3 y 4, HTML y nota, e incluye la estrategia de cobrar en capital lo aportado hasta 2006 y el resto en renta. Liquidez (art. 8.8, planes de empleo) y art. 8.5: correctos.
**Cambios que quedan:**
| Archivo | Qué | Por qué |
|---|---|---|
| calcs/…js `pintar` (veredicto) | «Un mixto con el X % … pagaría aún menos» solo si vanImpMixtoOpt < serieMin; si no, poner «Con tu plazo de N años, un mixto con el X % en capital pagaría Z €, menos que la renta y el capital de ese plazo». | Hoy se contradice con la frase anterior en 3 de 5 escenarios. Por ejemplo, en Madrid 20.000/14.000 la renta de 32 años paga 0 € y el mixto «aún menos» paga 5.341 € (pasa igual en Andalucía y Valencia). |
| json sources + HTML «Supuestos» | Declarar: «se supone que no tienes rentas distintas de las del trabajo de más de 6.500 €; si las tienes, no hay reducción del art. 20 y la renta sale mejor de lo que indica el cálculo». | Es una condición del art. 20 que hoy no se declara. |
| JS nota, json sources, HTML | RDL 5/2026: «se pierde si lo que cobras del plan más tus otras rentas no laborales supera 6.500 € al año». | Para esa deducción, los pagos del plan cuentan como rentas distintas de las laborales. |
| json FAQ 1 | «Tampoco se ahorra más con más años» → «No siempre se ahorra más con más años». | En Cataluña el óptimo es 40 años. |
| json lead y veredicto, HTML lead y «Renta» | «con pagos que te dejan por debajo de 19.747,50 €» → «si sin el plan cobras menos de 19.747,50 € y los pagos te meten en la banda de 14.852 a 19.747,50 €, donde se pierde la reducción». Quitar del veredicto «(el 40 %) o solo en parte (la reducción del art. 20 sí entra)» y poner «el 40 % no está incluido». | Por debajo de 14.852 € la renta conserva la reducción completa y es cuando más gana: con otras rentas de 0 €, la renta paga 0. La cláusula del veredicto es confusa. |
| JS nota | «ahorra X € de IRPF que la renta pura» → «… frente a la renta pura». | Redacción. |
