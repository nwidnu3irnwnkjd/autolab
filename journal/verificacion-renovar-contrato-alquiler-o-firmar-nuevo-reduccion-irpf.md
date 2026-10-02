# Verificación fiscal · renovar-contrato-alquiler-o-firmar-nuevo-reduccion-irpf · 2026-10-02 (Verificador, Opus)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 2 · 8 1 · N 1 · R 0 · S 1 (no crítico en cifras; sí en el veredicto para contratos en tácita reconducción) · otros 0
Paso 0 (interpretación propia antes del JS): coincide con el bloque INTERPRETACION en 23.2 a/b/c/d, DT 38.ª, 17.6 y despeje. Diferencia: la prórroga solo es «el mismo contrato» dentro de los arts. 9-10 LAU; la tácita reconducción posterior (art. 1566 CC) es contrato nuevo según doctrina del TS, y el modelo la trata como prórroga.
Oráculo re-ejecutado hoy: 920 casos, 0 discrepancias. Cifras del lead/veredicto recalculadas a mano: 2.288 / 2.210 / 807,65 / 2.055,24 / 779,90 (rebaja máx. 2,51 %) / +942: todas correctas.

## Lectura de norma (API consolidada BOE, 2-10-2026)
- LIRPF a23: 6 versiones; penúltima BOE-A-2023-12203 (vig. 1-1-2024) = literal citado en preverif (90/70/60/50, «mientras se sigan cumpliendo», autoliquidación, «Tampoco… incumplan… apartado 6 del artículo 17»). Versión 31-12-2021 (BOE-A-2021-11473): «se reducirá en un 60 por ciento». OK.
- DT 38.ª (dt-6): 2 versiones; la 1.ª (Ley 12/2023) = «contratos… que se hubieran celebrado con anterioridad a la entrada en vigor de la Ley 12/2023… redacción vigente a 31 de diciembre de 2021». OK. La del RDL añadía apdo. 2 y el 80 % por prórroga tácita: sin efecto.
- BOE-A-2026-20526: el Congreso «acordó derogar» el RDL 26/2026 (art. 86.2 CE); el análisis «deja sin efecto» sus modificaciones de la Ley 35/2006 y de la Ley 29/1994. La penúltima versión es la aplicable: confirmado (confianza B mientras el consolidado LIRPF no se actualice).
- LAU a17: última versión BOE-A-2026-20526 (2-10-2026); apdos. 6 y 7 idénticos carácter a carácter a la versión Ley 12/2023; no quedan apdos. 8-9 del RDL. OK. LAU a10.1: prórroga anual hasta 3 años más tras 5/7. OK.
- DGT: no hay consulta sobre prórroga y DT 38.ª (la V0444-24 que cita algún blog trata contratos < 1 año, no esto). Manual AEAT 2024/2025: «60 %» para contratos anteriores, sin nada sobre prórroga.

## Puntos críticos
1. Prórroga de contrato anterior al 26-5-2023 → 60 %: DEFENDIBLE como S confianza B mientras siga dentro de los arts. 9 y 10 LAU (incluida la prórroga extraordinaria del 10.2, que mantiene «los términos y condiciones… del contrato en vigor»). NO defendible igual para: (a) tácita reconducción del art. 1566 CC tras agotar el art. 10 (contratos de 6-6-2013 a 5-3-2019 tenían 3+1 años y hoy están casi todos ahí): el TS la considera contrato nuevo → riesgo de 50 %; (b) «renovar» firmando documento nuevo o novando la renta más allá de la actualización: es contrato nuevo. El slug dice «renovar»: hay que separarlo de «prorrogar».
2. Art. 23.2 para contrato nuevo: modelo correcto (a 90 % con «más de un 5 %» estricto y actualización ya aplicada; b.1.º imposible al no ser «por primera vez»; b.2.º declarado; c 60 % rehab art. 41.1 RIRPF; d 50 %; prelación a>b>c>d). Omisión que cambia veredicto: ver punto 3.
3. Zona tensionada 17.6: el +10 % no es solo por rehabilitación: letras b) eficiencia energética −30 %, c) accesibilidad, d) contrato de 10 o más años (o derecho de prórroga potestativa de 10). Con tensionada=sí, rehab=no y renta nueva +1-10 %, el JS dice «incumple, pierdes toda reducción», falso para quien firma a 10 años o acredita b/c; marcar rehab=sí para sortearlo le da además un 60 % indebido (el 23.2.c exige rehab del art. 41.1, no b-d). 17.7 gran tenedor: declarado, OK.
4. Absolutos/citas: muestreo de 3 citas (23.2.c → art. 41.1 RIRPF; arts. 9-10 LAU; 23.2 autoliquidación): OK. Hallazgos en tabla.
5. Forales: País Vasco y Navarra declarados en «Supuestos y fuentes»; suficiente (no bloquear).

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué / norma |
|---|---|---|---|---|
| 1 | S | json (input fecha o nuevo select) + js nota + html Supuestos + FAQ1/FAQ5 | Distinguir «prórroga de los arts. 9-10 LAU (incl. 10.2)» de «tácita reconducción tras agotar el art. 10 / renovación con documento nuevo». Mínimo: aviso en nota y FAQ1/FAQ5: «si tu contrato ya agotó las prórrogas del art. 10 y sigue por tácita reconducción (art. 1566 Código Civil), el Supremo la trata como contrato nuevo y Hacienda podría aplicar el 50 %». Mejor: select `estado` = prórroga LAU / tácita reconducción → en esta, pctA = 50 con aviso (o mostrar ambos) | DT 38.ª «celebrado con anterioridad»; CC 1566; LAU 10.1 |
| 2 | N | json + js + html | Añadir input «¿Otra excepción del 17.6 (eficiencia energética, accesibilidad, contrato de 10 años o más)?»: sube el límite a +10 % sin dar el 60 %. Si no se modela, el veredicto `incumple` debe decir «salvo que acredites una de las excepciones b)-d) del art. 17.6 (p. ej. contrato de 10 años o más)» y el html «más un 10 % como máximo si hubo rehabilitación» debe listar las 4 letras | LAU 17.6 a)-d); 23.2.c solo rehab art. 41.1 |
| 3 | 8 | html «Cómo usar» o nota + FAQ5 | Declarar que firmar un contrato nuevo durante la prórroga obligatoria requiere el acuerdo del inquilino (el art. 9 le da a él la decisión de prorrogar) o que hayan terminado las prórrogas; el arrendador no puede imponerlo para subir la renta | LAU 9.1 y 10.1 |
| 4 | T | json FAQ4 | Quitar «sin efectos retroactivos»: la Resolución BOE-A-2026-20526 no lo dice y sugiere que un contrato firmado el 1-2/10/2026 conserva el 100/80 %. Sustituir por «esta calculadora aplica la Ley 12/2023 a todo el ejercicio 2026» | BOE-A-2026-20526 (texto íntegro) |
| 5 | T | json lead + veredicto + html lead | «firmar uno nuevo la baja al 50 %, salvo rehabilitación (60 %) o… (90 %)»: añadir «o 70 % si es alquiler social o vivienda con renta limitada por un programa público» (o «en general») | 23.2.b.2.º |
Recomendado (no bloquea): nota de prórroga desde 26-5-2023 con 90 % o 70 %: «mientras se sigan cumpliendo» puede perderse si la zona deja de estar declarada o el inquilino cumple 36 (lectura no aclarada por la DGT). params: renombrar `url_rdl` (apunta a la Resolución de derogación, no al RDL).

## Casos nuevos para test.json (base 800/7.000/30 %)
- Si se implementa el cambio 2 (`excepcion176`=si): tensionada=si, rehab=no, renta1=880 → incumple 0, pctB 50, prevB 3.560, cuotaB 534, resB 3.026, resA 2.288, dif +738, gana 2. Con renta1=880,01 → incumple 1, pctB 0.
- Mismo caso sin la excepción (estado actual): renta1=880, rehab=no → incumple 1, pctB 0 (ya cubierto por la lógica; dejarlo como regresión).
- Si se implementa el cambio 1 (`estado`=reconduccion, fecha=antes): renta1=800 → pctA 50, resA 2.210, resB 2.210, dif 0, gana 0; renta1=900 → resB 3.230, dif +1.020, gana 2.
- Borde de fecha (solo texto): contrato firmado el 26/5/2023 = «desde» (DT 38.ª: «con anterioridad a la entrada en vigor»; Ley 12/2023 en vigor el 26-5-2023). La etiqueta actual ya lo hace bien.
No escribí oráculo propio (ops/verif/<slug>.py): los casos de arriba se calculan con la fórmula ya verificada del Constructor.
Re-verificación: Sonnet si solo cambian textos (4, 5, 3 y aviso del 1); Opus ≤ 60k solo si se modelan `estado` o `excepcion176`.

## Re-verificación (2026-10-02, Opus, acotada)
VEREDICTO: PUBLICABLE CON CAMBIOS (2 de texto, sin impacto en cifras).
- (1) Modelo: `excepcion176` (rehab/energia/accesib/diez) sube el límite a ×1,10 y solo `rehab` da el 60 %; `fecha=reconduccion` → pctA 50. Correcto. Oráculo re-ejecutado: 925 casos, 0 discrepancias.
- (2) test.json: 880 «diez» → resB 3.026, dif +738, gana 2; 880,01 «energia» → incumple; 880 «ninguna» → incumple (regresión); reconducción 800 → dif 0; 900 → +1.020; accesibilidad 900 → 50 %, +942. OK.
- (3) Lead, veredicto, FAQ1/3/4/5 y html (Supuestos, 17.6 con las 4 letras, «Cómo usar», acuerdo del inquilino) OK. «sin efectos retroactivos» eliminado. Pendiente:
  a. JS veredicto `incumple`: la cláusula «salvo que acredites una de las excepciones del art. 17.6 (…)» solo debe salir si `excepcion176 === "ninguna"`; con una excepción ya marcada el límite ya incluye el +10 % y la frase es falsa. Con excepción: «supera el límite de X (última renta + 10 % por la excepción del art. 17.6)».
  b. html «Qué reducción te corresponde» → «Contrato nuevo: … 50 % en los demás casos»: cambiar por «50 % en general (70 % si es alquiler social o vivienda con renta limitada por un programa público, art. 23.2.b.2.º, no modelado)». Recomendado igual en FAQ2 tras «El 70 % de primera vez no vale…»: «(sí el 70 % de alquiler social o programa público, no modelado)».
- (4) Citas: 23.2.b.2.º (70 % social/programa público) bien descrito; 9.1 (prórroga obligatoria a voluntad del inquilino) y 10.1 (prórroga anual «obligatoriamente» si nadie notifica) sostienen «exige el acuerdo del inquilino»; art. 1566 CC = tácita reconducción. OK.
Tras a y b: PUBLICABLE sin nueva verificación (solo texto; re-ejecutar test.json).
