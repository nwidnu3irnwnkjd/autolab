# Verificación fiscal · venta-vivienda-plusvalia-irpf-exencion · 2026-10-02 (Verificador Opus, v3.2)
VEREDICTO: PUBLICABLE CON CAMBIOS (6 obligatorios, 3 críticos; 0 errores de fórmula)
Norma leída: BOE-A-2026-20266 (RDL 26/2026, texto íntegro: DA 65.ª y 66.ª LIRPF nuevas, DF 3.ª.Uno RIRPF 41 bis.3), API BOE consolidado LIRPF a38 (apdo. 3, Ley 26/2014), params irpf_2026.escala_ahorro_mitad.

## Paso 0 · interpretación propia vs oráculo
Coincide en: ganancia (34-35: VT = precio − gastos/tributos del vendedor; VA = precio + mejoras + gastos/tributos sin intereses − amortizaciones), 33.4.b (65+/dependencia severa o gran dependencia, total, sin reinvertir), 38.1 + RIRPF 41.1/41.3 (proporción reinvertido / (VT − principal pendiente del préstamo con que se compró), 2 años), escala del ahorro 19/21/23/27/30 % (tramos 6.000/50.000/200.000/300.000; params y JS coinciden; cuotas 570/5.190/22.440/35.940 correctas). «Importe obtenido» neto de gastos de venta: defendible (RIRPF 41.1 habla de «valor de transmisión», que por 35.2 ya es neto de gastos; criterio coincidente del Manual AEAT). Ejemplo recalculado a mano: 115.000 € de ganancia, 251.000 € necesarios, 9.658 € y 25.450 € OK.
Diferencia (no de fórmula, de input): qué cuenta como «reinvertido» (cambio 3).

## Cambios obligatorios
| # | Patrón | Archivo · dónde | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | 2/7/8 (crítico) | json faqs «¿Qué pasa si no era mi vivienda habitual?», faq 65+ («La exención no alcanza a una segunda vivienda: ahí la ganancia tributa entera»), html «Vivienda no habitual: no hay exención», nota «Límites» del JS, sources/params («no cambia ninguna rama calculada») | Declarar la nueva DA 65.ª LIRPF: venta onerosa de vivienda a entes/sociedades públicos de vivienda social entre 1/10/2026 y 31/12/2027, valor de transmisión < 800.000 €, desocupada 2 años sin causa justificada: exenta 100 % si VT ≤ 200.000 €, y (800.000 − VT)/600.000 entre 200.000 y 800.000; el resto, reinversión en la Cuenta Financia Europa Reinversión (DA 66.ª, 6 meses). RDL sin convalidar: solo aviso, no modelar. Quitar «tributa entera» como absoluto. | RDL 26/2026 art. (modif. LIRPF) Once y Doce. La preverif decía «arts. 33-38 sin cambios» y no vio la DA nueva; la opción «heredada vacía» del select es justo el caso objetivo. |
| 2 | 2/1 (crítico) | mismas frases de no habitual y 65+ | Mayores de 65 que venden una vivienda NO habitual (u otro bien): exclusión si destinan lo obtenido en 6 meses a una renta vitalicia asegurada, máx. 240.000 €, proporcional. Declararlo como límite. | Art. 38.3 LIRPF (Ley 26/2014), leído en BOE. |
| 3 | 6 (crítico) | json input reinv.ayuda, html «Cómo usar el resultado», faq «¿Cómo evito pagar…?» | Decir que cuenta como reinvertido todo lo que pagas por la nueva vivienda habitual en plazo, aunque lo financies con una hipoteca nueva o subrogada (no solo el dinero de la venta). Sin esto, quien compra con hipoteca mete solo su efectivo y la calculadora le da IRPF de más. | Doctrina del Tribunal Supremo (2024): no es necesario emplear el dinero obtenido; vale la financiación ajena (elderecho.com/el-ts-establece-que-la-reinversion-de-la-venta-de-un-inmueble-en-otra-vivienda-habitual-mediante-hipoteca-tambien-da-derecho-a-la-exencion-del-irpf). |
| 4 | 4 | json select hab/hab65 («menos de 65» / «más de 65»), lead, veredicto, faq, html, verdict JS | «65 años o más» (la ley dice «mayores de 65 años» = cumplidos); hoy quien tiene exactamente 65 no tiene opción y la nota JS ya dice «con 65 o más» (incoherente). | Art. 33.4.b LIRPF. |
| 5 | 3/8 | lead, html «Qué no incluye», nota JS | No residentes: no es «la retención del 3 %», es que la calculadora no aplica (tributan por IRNR, 19 %). Añadir también la deducción del 60 % de Ceuta y Melilla (art. 68.4 LIRPF) como no modelada. | TRLIRNR arts. 24-25; LIRPF 68.4. |
| 6 | 4 | json input venta.ayuda | «si es inferior al valor de mercado, prevalece este» es ambiguo (puede leerse que prevalece el precio): «prevalece el valor normal de mercado». | Art. 35.2 LIRPF. |

## Recomendados (no bloquean)
- DT 9.ª: el aviso es suficiente (declarado en lead, FAQ, nota; dirección «igual o menor» correcta; corte 31/12/1994 correcto: > 2 años de permanencia a 31/12/1996 redondeando). Mejor: «puede ser bastante menor; si compraste antes de 1987, la parte generada hasta el 19/1/2006 puede no tributar, con el tope de 400.000 €».
- input sit.ayuda: añadir las excepciones a los 3 años (matrimonio, separación, traslado laboral, fallecimiento), como ya hace el html.
- Verdict de pérdida: sobra «comprobar que la pérdida sea computable» (la de la vivienda habitual es computable; art. 33.5 no la excluye).
- Borde hipoteca = valor de transmisión (obtenido 0): el JS exime con reinversión 0; exigir que se compre nueva vivienda habitual (texto) — caso < 1 %.
- JS lleva la escala escrita a mano en P.tab en vez de leer params: valores idénticos hoy; que el Constructor la lea de irpf_2026.escala_ahorro_mitad.
- El RDL cambia también los coeficientes de la plusvalía municipal (TRLRHL 107.4) desde 1/12/2026: solo relevante si se enlaza una calculadora de IIVTNU.

## Casos nuevos para test.json
- hipoteca = venta − gventa, sit hab, reinv 0 → hoy exenta total; si se cambia a exigir compra, test de texto.
- Ningún caso de fórmula nuevo: las 6 correcciones son de texto/aviso. Re-verificación Sonnet: releer solo las frases de la tabla.
