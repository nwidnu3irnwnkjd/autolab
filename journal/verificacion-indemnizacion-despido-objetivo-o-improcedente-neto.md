# Verificación fiscal/legal · indemnizacion-despido-objetivo-o-improcedente-neto (Verificador Opus, 2026-10-02)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 2 · N 1 · R 0 · otros 2 · crítico: N1 (art. 52.c)
Norma leída hoy (API BOE consolidado): ET a53, a56, a52, DT 11.ª; LIRPF a7.e, a18.2; LGSS a275.5.b. Oráculo re-ejecutado: 900+18, 0 discrepancias.

## Paso 0: interpretación propia vs INTERPRETACION del oráculo
- 1-4 (ET): coincide. DT 11.ª.2 literal: 45 d/año hasta el 12-2-2012 y 33 después, cada tramo prorrateado por meses; tope 720 días salvo que el tramo anterior dé más (entonces ese es el máximo), nunca > 42 mensualidades. El objetivo no tiene tramo de 45 (la DT solo regula el improcedente; DT 11.ª.3 fomento, declarada). Mecánica del oráculo correcta.
- 5 (art. 7.e): DIFIERE. Párrafo 2 literal: en el despido del art. 52.c (causas del 51.1: económicas, técnicas, organizativas, de producción o fuerza mayor) «quedará exenta la parte de indemnización percibida que no supere los límites establecidos con carácter obligatorio... para el despido improcedente». El oráculo y el JS eximen solo los 20 días en todo objetivo. El 52.c es la causa de la gran mayoría de objetivos (52.a ineptitud, 52.b falta de adaptación y 52.e son minoritarias; 52.d derogada).
- 6 (art. 18.2): coincide. 30 %, generación = años de servicio, > 2 años, no aplica la regla de 5 años a estos rendimientos; 300.000 € sobre la «cuantía del rendimiento íntegro» (aplicarlo a la parte no exenta es defendible: lo exento no es rendimiento íntegro sujeto); fase 700.000,01-1.000.000 € = 300.000 − (rend − 700.000), cero desde 1.000.000. Cifras y cálculo correctos.
- 7: IRPF = tributable reducido × marginal: supuesto declarado, defendible.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | N (crítico) | calcs .js/.json/.test.json + oráculo + content | Modelar la causa del objetivo: selector «52.c causas económicas, técnicas, organizativas o de producción (por defecto) / otra causa (52.a, b, e)». Si 52.c: exento = min(oferta, legal del improcedente con DT 11.ª, 180.000); si otra: min(oferta, 20 días, 180.000). Quitar el 52.c de «Qué no incluye». | Art. 7.e párr. 2 LIRPF. Hoy, una oferta de 33 días en un objetivo 52.c sale gravada en el exceso sobre 20 días cuando está exenta. Cambia la interpretación: re-verificación Opus ≤ 60k solo de esta pieza. |
| 2 | 8 | content, json (FAQ 3, resultado del improcedente) | La exención del improcedente exige que la improcedencia se reconozca en conciliación ante el servicio administrativo (art. 63 LRJS) o en sentencia; lo pagado por pacto privado (p. ej. reconocida en la carta sin conciliación) es «pacto» y tributa. Añadirlo como condición junto a la cifra exenta del improcedente. | Art. 7.e párr. 1 y 3 LIRPF (excluye convenio, pacto o contrato; solo la conciliación del art. 63 LRJS deja de ser pacto). La opción «improcedente exento» solo existe por esa vía. |
| 3 | 8 | content («Topes»), json sources | Quitar «la equivalencia que usa la propia disposición transitoria (720 días son 24 mensualidades)»: la DT 11.ª no la establece (fija 720 días y 42 mensualidades por separado). Redactar como supuesto: «una mensualidad = 30 días; si se toma el salario mensual (bruto/12), los topes de 12/24/42 mensualidades son un 1,4 % mayores (12 mensualidades = 365 días)». | Texto ≤ norma; el supuesto infravalora el tope y el usuario podría aceptar menos. |
| 4 | otros (absoluto) | lead (content y json), «Qué parte tributa», FAQ 3 | «el exceso sobre la legal tributa» / «La que se pacta por encima de la legal tributa» / «lo que la empresa ofrezca por encima de la legal tributa»: condicionar («salvo en el objetivo por causas económicas..., exento hasta la del improcedente»). Se resuelve con el cambio 1. | Art. 7.e párr. 2. |
| 5 | otros (cita) | content y FAQ 5 | «la solicitud de conciliación lo interrumpe» → «lo suspende». | Art. 65.1 LRJS: la conciliación «suspenderá» los plazos de caducidad. |

## Comprobado sin cambios
- Cifras de la página recalculadas: 13.151 / 21.699 / 8.548; 47.466 vs 47.564 (+1 día); 47.342 (360 días); 8.301 → 5.811 → 2.150 → 27.850. Correctas.
- ET 53.1.b (20 d, 12 mens.), 56.1 (33 d, 24 mens.), 59.3 (20 días hábiles, caducidad), DT 11.ª.1-3: citas correctas.
- RIRPF art. 1 (3 años, presunción salvo prueba en contrario): correcta. LGSS 275.5.b (indemnización legal no computa en el subsidio): correcta.
- T: DT 11.ª modelada bien; DT 22.ª LIRPF (180.000 € para despidos anteriores al 1-8-2014): superada en 2026, no aplica. R: RDL 26/2026 no toca ET 52/53/56/DT 11.ª ni LIRPF 7.e/18.2 (solo 7.ñ). LIS: no aplica.
- Supuestos (a)-(h): defendibles y declarados, salvo la justificación de (a) (cambio 3). (d) cambia con el cambio 1. (g) correcto: lo acordado en conciliación queda exento hasta la legal del improcedente.
- Bloqueos (antes > M, meses > 11, M = 0, marginal > 55): correctos. Forales avisados.

## Casos nuevos para test.json (tras el cambio 1)
- Objetivo 52.c, 30.000 €, 8 años, oferta 21.699 → exento 21.699, tributable 0, neto 21.699.
- Objetivo 52.c, 30.000 €, 8 años, oferta 30.000 → exento 21.699, tributable 8.301, reducción 2.490, IRPF (37 %) ≈ 2.150.
- Objetivo otra causa, mismo caso, oferta 21.699 → exento 13.151, tributable 8.548.
- Objetivo 52.c con alta 1-2012 (tramo de 45 en el límite exento, no en lo legal del objetivo): 36.000 €, 14 a 8 m, antes = 1 mes, oferta 47.564 → exento 47.564.

## 2.ª pasada Opus (2026-10-02, solo piezas cambiadas)
VEREDICTO: PUBLICABLE CON 2 CAMBIOS MENORES (texto; sin cambios de cálculo). Oráculo re-ejecutado: 900 + 22 fijos, 0 discrepancias.
(a) Selector: `lim = objetivo && causa !== "otra" ? legalImp : legal`, y luego exento = min(cobrado, lim, 180.000). legalImp incluye la DT 11.ª (45/33, 720, 42). Coincide con el art. 7.e, párr. 2. En el improcedente la causa se ignora. Los 4 casos nuevos dan lo esperado: 52.c con 21.699 → exento 21.698,63 (tributa 0,37 € de redondeo); 52.c con 30.000 → tributable 8.301,37, IRPF 2.150,05; otra causa con 21.699 → exento 13.150,68, tributable 8.548,32; 52.c con tramo de 45 → exento 47.564 (nota: mi caso decía 14 a 8 m, que da un improcedente de 47.835,62; la oferta queda por debajo y está igualmente toda exenta: correcto).
(b) Textos: conciliación/sentencia en la página, la FAQ 3 y el resultado del improcedente: bien. «Supuesto propio, no de la ley» y el 1,4 % en la página y en sources: bien. «Suspende» en la página y la FAQ 5: bien. Absolutos condicionados en el lead, el cuerpo y la FAQ 3: bien.
(c) Fusión de inputs: leer() lee bruto/anios/meses/antes/oferta/marginal + tipo + causa; ids de json = ids de leer. Sin errores de cálculo.
Cambios restantes:
1. content, «Qué no incluye»: «…costes del procedimiento judicial, En el País Vasco…» → «…judicial. En el País Vasco…» (frase rota al quitar el 52.c).
2. lead (json y content): «la indemnización legal está exenta de IRPF hasta 180.000 €» → añadir «(en el improcedente, si se reconoce en conciliación o sentencia)». Es el único absoluto que queda; el cuerpo ya lo condiciona.
Opcional: la FAQ 3 repite dos veces la condición de conciliación (en el paréntesis y en «Ojo:»); quitar una.
