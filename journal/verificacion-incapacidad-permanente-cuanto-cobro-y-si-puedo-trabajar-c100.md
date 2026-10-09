# Re-verificación c100 (COLA ítem 8) · incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar (+ pension-viudedad-cuanto-cobro) · 2026-10-09 · Verificador fiscal (Opus)
Solo lectura: no se ha editado ninguna calculadora. Norma leída hoy con la API consolidada del BOE. La versión válida es la última de cada bloque **por id_norma**, no por fecha. También se leyó el texto del Diario.

## 1 · Incapacidad permanente
**VEREDICTO: PUBLICABLE CON CAMBIOS (solo texto, 0 errores de fórmula, ninguna cifra publicada es falsa)** · T 0 · 8 0 · N 1 · R 1 · S 0 · otros 0

**Paso 0.** Mi interpretación coincide con el bloque INTERPRETACION del oráculo en grados, BR, suelo del art. 196.2 párr. 3, complemento por mínimos por diferencia, bloqueos y compatibilidad. Los 6 cambios de la verificación del 2-oct siguen aplicados en el JS (l. 29-30 suelo, l. 38 compMin, l. 41 75 %).

**Norma (última versión por bloque, LGSS BOE-A-2015-11724):**
- a193: Ley 3/2024. a194, a195, a197 y DT 26.ª: Ley 2/2025 (BOE-A-2025-8567), en vigor el 1-5-2025; solo cambia «gran invalidez» por «gran incapacidad».
- a196: RDL 28/2018. Se releyó literal: tanto alzado; 55 % + incremento reglamentario; suelo de «menores de sesenta años con cónyuge no a cargo»; complemento 45 % + 30 % con mínimo del 45 %; 196.5 «sesenta y siete o más años».
- a198: Ley 7/2024 DF 13.ª y Ley 2/2025. Apartados 1, 2 (suspensión; el complemento no se suspende) y 3 (remite al 213.1): coinciden con la página.
- a199 y a200: texto original. a57: RDL 2/2023. a59: Ley 2/2025. a60: RDL 2/2023. DT 7.ª y DT 9.ª: originales.
- Bloques de la LGSS actualizados en 2026 (a190, a271, a299, a363, DA 18.ª/19.ª/61.ª, DA nuevas, DT 35.ª/45.ª/46.ª/47.ª): son desempleo, mutualistas alternativas, CNAE y no contributiva. **Ninguno toca los arts. 193-200, 57, 59 ni 219-223.**
- **RDL 25, 28 y 29/2026.** Su XML del Diario (-20265/-20822/-20823) contiene 0 menciones a «incapacidad permanente», «viudedad», «invalidez» y «8/2015». La única mención a la Seguridad Social del RDL 29 se refiere a viviendas del patrimonio de la TGSS. **No afectan.**
- **RD 241/2026** (BOE-A-2026-6977), leído literal:
  - Art. 3: límite de 3.359,60 €/mes.
  - Art. 9.2: complemento por diferencia hasta 9.442 € + el mínimo.
  - Anexo I, IP, columnas con cónyuge a cargo / unipersonal / cónyuge no a cargo:
    - Gran incapacidad: 26.385,80 / 19.660,20 / 18.662,00.
    - Absoluta y total con 65 años o más: 17.592,40 / 13.106,80 / 12.441,80.
    - Total entre 60 y 64 años: 17.592,40 / 12.262,60 / 11.590,60.
    - Total por enfermedad común con menos de 60 años: 9.662,80 / 9.662,80 / **9.580,20**, que es el suelo.
  - Todas las cifras coinciden con el JS (l. 3), con params y con content l. 14.
- **RDL 3/2026** (BOE-A-2026-2548): estado «Finalizado», sin derogación y con «Acuerdo de convalidación» publicado. El RD 241/2026 cita sus arts. 1 y 2.
- **Orden PJC/297/2026:** base mínima de 1.424,40 € (grupos 4-7, art. 3) y tope de 5.101,20 € (art. 2.1). Correctos.
- **LIRPF art. 7.f:** la última versión del bloque es BOE-A-2026-5060, que modifica otra letra; la f) mantiene su texto. Correcta.

**Ejecución:**
- Oráculo `ops/verif/…_oraculo.py`: 33 casos fijos + 700 de barrido, **0 discrepancias**.
- `ops/verif/….py`: 3/3 OK.
- `ops/check.py decidir`: 13.709/13.710. El único fallo es `test_numinput: falta dist/embed`: build en curso por otro agente, ajeno a estos slugs. El test.json de los dos slugs está OK.

**Muestreo de citas:**
- 196.4, 198.2 y 195: correctas.
- Aritmética del ejemplo de 61 años con trabajo: (9.442 + 12.262,60 − 12.000 − 9.580,20)/14 = 8,89 €. OK.

| # | Cl. | Archivo:línea | Texto actual → propuesto | Fuente |
|---|---|---|---|---|
| 1 | N (omitido) | content/…html:48 y calcs/…js:58 (NO_MODELA) | «No incluye: el cálculo detallado de la base reguladora con tus bases reales, …» → insertar tras «la retención del IRPF,»: «el complemento por brecha de género (36,90 € al mes por hijo, hasta 4, para mujeres con hijos y, en algunos casos, hombres; se suma a la pensión de la total, la absoluta y la gran incapacidad; no a la parcial, que no es pensión),». Igual en json:6 lead / content:1: «no calcula tu base reguladora con bases reales ni la retención del IRPF» → «no calcula tu base reguladora con bases reales, la retención del IRPF ni el complemento por brecha de género». | LGSS art. 60.1 (a60, versión BOE-A-2023-6967: «pensión contributiva de jubilación, de incapacidad permanente o de viudedad»); RD 241/2026 art. 12 (36,90 €). La de viudedad ya lo declara. |
| 2 | R | data/params.json:4890 (`incapacidad_permanente_2026.consulta`) | «consultado el 2/10/2026» → «consultado el 9/10/2026 (sin versiones nuevas de los arts. 193-200, 57, 59 ni 60; RDL 25, 28 y 29/2026 no los tocan)» | API consolidada, 9-10-2026 |

Recomendado, no bloquea: content:24, tras «El INSS puede revisar el grado si trabajas.», añadir: «Desde el 1-5-2025 la incapacidad permanente ya no extingue automáticamente el contrato: la empresa debe intentar ajustes razonables o un cambio de puesto antes de extinguirlo (art. 49.1.n del Estatuto de los Trabajadores, Ley 2/2025).» Hoy la página no lo dice ni lo calcula. Antes de publicar hay que verificar literal el art. 49 del ET (BOE-A-2015-11430), porque hoy no lo he leído.

## 2 · Pensión de viudedad (pension-viudedad-cuanto-cobro)
**VEREDICTO: PUBLICABLE CON CAMBIOS (texto)** · T 1 · 8 0 · N 1 · R 1 · S 0 · otros 0

**Norma:**
- LGSS a219 y a220: originales. a221, a222 y a223: Ley 21/2021 (BOE-A-2021-21652, en vigor el 1-1-2022). Sin versiones de 2026.
- Decreto 3158/1966: índice sin actualizaciones desde el 21-3-2009, así que el art. 31 sigue igual.
- RD 900/2018: sin modificaciones (el análisis solo da «de conformidad con»).
- Anexo I del RD 241/2026, viudedad: 17.592,40 / 13.106,80 / 12.262,60 / 9.931,60. Límite de 9.442 €. Brecha de género: 36,90 € (art. 12).
- RD 126/2026: SMI de 1.221 €/mes, así que el 75 % × 12 = 10.989 €.
- Todo coincide con el JS (l. 3) y con content l. 7 y 9: 19.373,60 / 21.704,60 / 22.548,80 y 1.256,60 / 936,20 / 875,90 / 709,40.
- RDL 25, 28 y 29/2026: no afectan (ver arriba).

**Ejecución:**
- Oráculo: 30 casos fijos + 700 de barrido, **0 discrepancias**.
- test.json: OK dentro de check.py.
- El ejemplo pendiente de la reverificación del 2-oct (content:25) ya está corregido: 52 %, 1.040 €, con aviso de 1.400 €.

| # | Cl. | Archivo:línea | Texto actual → propuesto | Fuente |
|---|---|---|---|---|
| 1 | T | content/pension-viudedad-cuanto-cobro.html:16 | «…y se extingue si te casas o constituyes una nueva pareja de hecho (art. 223.2).» → «…y se extingue si te casas o constituyes una nueva pareja de hecho (art. 223.2), salvo las excepciones que fija el reglamento.» Es la misma fórmula que ya usa json:121. | LGSS 223.2: «sin perjuicio de las excepciones establecidas reglamentariamente» |
| 2 | N | content/…html:9 y calcs/pension-viudedad-cuanto-cobro.js:62 | «Si tu pensión queda por debajo y tus ingresos sin ella no superan 9.442 € al año, puedes pedir el complemento por mínimos.» → «Si tu pensión queda por debajo del mínimo, puedes pedir el complemento por mínimos: es la diferencia hasta el mínimo, siempre que tus otros ingresos más la pensión no pasen de 9.442 € más el mínimo, todo en cómputo anual; con ingresos algo mayores puede quedar un complemento parcial.» En js:62: «Si tus ingresos sin esta pensión no superan " + eur(P.limIng) + " al año, puedes pedir…» → «Si tus otros ingresos más la pensión no superan " + eur(P.limIng) + " al año más el mínimo, puedes pedir (en parte o entero)…». Es el mismo criterio que se corrigió en IP el 2-oct. | RD 241/2026 art. 9.2; LGSS 59.1 |
| 3 | R | data/params.json:4457 (`viudedad_2026.consulta`) | «consultado el 2/10/2026» → «consultado el 9/10/2026» | API consolidada, 9-10-2026 |

## Re-verificación
Basta Sonnet: los 5 cambios son de texto, no cambian ninguna cifra ni la interpretación. Pasos:
1. Releer las líneas citadas.
2. Ejecutar los dos oráculos y `ops/verif/incapacidad-permanente-…py`.
3. Ejecutar `check.py` cuando haya terminado el build de dist/embed.

No hacen falta casos nuevos en test.json porque ningún cambio afecta al cálculo.
