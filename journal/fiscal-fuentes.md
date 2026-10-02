# Fuentes fiscales y reguladas para calculadoras (Investigador, 2026-10-02)

Fecha de consulta de **todas** las cifras: **2026-10-02**, salvo que se diga otra cosa.
Método: texto consolidado del BOE descargado con la API oficial de datos abiertos
(`https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/<ID>/texto`, BOE-A-2006-20764 actualizado a 30/09/2026)
y disposiciones del Diario Oficial (`https://www.boe.es/diario_boe/txt.php?id=<ID>`). La cifra se ha leído en el artículo vigente, no en blogs.
Enlace corto de cada norma: `https://www.boe.es/buscar/act.php?id=<ID>` (consolidada) o `https://www.boe.es/diario_boe/txt.php?id=<ID>` (diario).

Escala de confianza:
- **A** = leída en el artículo vigente del BOE (o en el BOE de la disposición) y con fecha de efectos clara para 2026.
- **B** = leída en el BOE, pero la consolidación puede ir con retraso o la fecha de efectos depende de una condición o de una convalidación pendiente.
- **C** = fuente oficial secundaria (AEAT, manual práctico) sin leer el artículo de la ley.
- **NO VERIFICADO** = no se ha podido comprobar en fuente oficial: **no se usa** hasta verificarlo.

Regla del Constructor: cada fila con A/B/C se copia a `data/params.json` con `fuente`, `url`, `consultado: 2026-10-02` y `confianza`. Las B llevan aviso en la página. Las NO VERIFICADO bloquean la parte de la calculadora que las usa.

---

## 0. Nota de riesgos (qué NO publicar todavía)

1. **RDL 26/2026, de 29 de septiembre (BOE-A-2026-20266, vivienda): en vigor desde el 1/10/2026 y SIN convalidar.** El Congreso tiene 30 días hábiles. En 2026 ya se derogaron dos RDL fiscales (RDL 16/2025 y RDL 2/2026). Toca IRPF (DA 50.ª apdo. 6, DA 58.ª, DA 62.ª apdo. 6, DT 38.ª, alquiler) e IVA (art. 91: viviendas protegidas al 4 %, con efectos 1/12/2026). **No publicar nada que dependa de cambios del RDL 26/2026** hasta ver la resolución de convalidación en el BOE. Las cifras que usamos abajo (deducciones 20/40/60 %, 10/20 % autoconsumo) vienen del RDL 7/2026, que **sí está convalidado** (BOE-A-2026-7125).
2. **IVA e Impuesto Especial sobre la Electricidad de la luz y el gas en noviembre y diciembre de 2026: condicionales.** El RDL 25/2026 (BOE-A-2026-20265) baja el IVA al 10 % y el IEE al 0,5 % solo si el IPC de electricidad (o gas) del mes de referencia sube más de un 15 % interanual (dato del INE). Hasta que el INE publique, **no hay cifra cierta**: la calculadora `luz-fija-o-indexada` debe tomar 21 % y 5,11269632 % para octubre de 2026 y pedir confirmación para noviembre y diciembre.
3. **Calculadora ya publicada `calefaccion-gas-aerotermia-electrica`**: el IVA del gas natural y el Impuesto sobre Hidrocarburos han cambiado mes a mes en 2026 (RDL 7/2026 art. 42; RDL 18/2026 arts. 5-7 y 10-11; RDL 25/2026 arts. 13-15 y 18-19). El 21 % de IVA que usa `params.json` es correcto para octubre de 2026 (no hay rebaja para octubre en ninguna norma). Para noviembre y diciembre depende del IPC (ver punto 2). Los tipos del Impuesto sobre Hidrocarburos del gas natural para octubre-diciembre de 2026 (RDL 25/2026 art. 13) están **NO VERIFICADOS**: revisar la cifra «0,00234 €/kWh aprox.» de `params.json`.
4. **País Vasco y Navarra** (IRPF, ITP y deducciones forales): **NO VERIFICADO**. Ninguna calculadora debe dar cifra para estos territorios. Mostrar «no disponible para territorio foral».
5. **Mínimos personales y familiares autonómicos**: hay al menos 6 comunidades con mínimos propios (sección 1.5). La calculadora de conjunta/individual **no puede usar los mínimos estatales para la cuota autonómica** de esas comunidades sin avisar.
6. **Escalas autonómicas de 2027**: solo se conoce la de la Comunitat Valenciana. La escala estatal de 2027 depende de unos PGE 2027 que no existen. **No publicar cifras de 2027** salvo la valenciana, y con la etiqueta «aprobada, con efectos 1/1/2027».
7. **Deducción por maternidad, guardería autonómica, bono social**: los importes estatales están verificados; las deducciones autonómicas por guardería **NO VERIFICADAS** (17 normas distintas).
8. **Compensación de excedentes de autoconsumo**: no existe un «precio oficial» fijo. Con PVPC el precio es horario (Pmh − CDSVh, publicado por REE/e·sios). Cualquier «€/kWh de compensación» fijo es una **hipótesis del usuario**, no un dato oficial.

---

## 1. `declaracion-conjunta-o-individual` (ejercicio 2026, campaña abril-junio 2027) — PRIORIDAD 1

Norma base: Ley 35/2006 del IRPF, consolidada a 30/09/2026 — [BOE-A-2006-20764](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764).

### 1.1 Escala general estatal (art. 63.1) — confianza A
Vigente desde 1/1/2021 (Ley 11/2020, BOE-A-2020-17339); sin cambios para 2026. Para 2027 no hay cambio aprobado.

| Base liquidable desde (€) | Cuota íntegra (€) | Resto hasta (€) | Tipo estatal % |
|---|---|---|---|
| 0 | 0 | 12.450 | 9,50 |
| 12.450 | 1.182,75 | 7.750 | 12,00 |
| 20.200 | 2.112,75 | 15.000 | 15,00 |
| 35.200 | 4.362,75 | 24.800 | 18,50 |
| 60.000 | 8.950,75 | 240.000 | 22,50 |
| 300.000 | 62.950,75 | en adelante | 24,50 |

Regla del art. 63.1.2.º: a la cuota de la base se le resta la cuota que resulta de aplicar la misma escala al mínimo personal y familiar.

### 1.2 Escala del ahorro (arts. 66.1 estatal y 76 autonómica) — confianza A
Vigente desde 1/1/2025 (Ley 7/2024, disp. final 7.ª, BOE-A-2024-26694). El tramo autonómico del ahorro lo fija el Estado (art. 76) y es igual al estatal. **Tipo total = el doble.**

| Base ahorro desde (€) | Resto hasta (€) | Estatal % | Autonómico % | Total % |
|---|---|---|---|---|
| 0 | 6.000 | 9,5 | 9,5 | 19 |
| 6.000 | 44.000 | 10,5 | 10,5 | 21 |
| 50.000 | 150.000 | 11,5 | 11,5 | 23 |
| 200.000 | 100.000 | 13,5 | 13,5 | 27 |
| 300.000 | en adelante | 15 | 15 | 30 |

### 1.3 Tributación conjunta (art. 84) — confianza A
| Parámetro | Valor | Artículo |
|---|---|---|
| Reducción modalidad 1 (matrimonio con o sin hijos) | **3.400 €/año** | art. 84.2.3.º |
| Reducción modalidad 2 (monoparental) | **2.150 €/año** | art. 84.2.4.º |
| Orden de aplicación | primero a la base imponible general (sin dejarla negativa); el resto, a la del ahorro | art. 84.2.3.º y 4.º |
| Se aplica antes de | reducciones por previsión social (arts. 51, 53, 54 y DA 11.ª) | art. 84.2.3.º |
| Monoparental: exclusión | no se aplica si el contribuyente convive con el padre o la madre de algún hijo de la unidad | art. 84.2.4.º |
| Límites cuantitativos | iguales que en individual, **sin multiplicar** por miembros | art. 84.2 |
| Excepción: planes de pensiones | límites de los arts. 52, 53, 54 y DA 11.ª **por cada partícipe** | art. 84.2.1.º |
| Mínimo del contribuyente | **uno solo** (5.550 €), con los aumentos por edad de cada cónyuge | art. 84.2.2.º |
| Mínimos por descendientes | se aplican (no se aplica mínimo del contribuyente por los hijos) | art. 84.2.2.º |
| Reducción por rendimientos del trabajo (art. 20) en conjunta | **una sola vez**, calculada sobre la suma de rendimientos netos del trabajo de la unidad | AEAT, Manual Renta 2025, «Fase 3.ª: rendimiento neto reducido» — confianza **C** |

Fecha: el art. 84 no se ha modificado desde 2010. **No hay supresión aprobada** de la reducción de 3.400 € para 2026 ni para 2027 (comprobado en el consolidado a 30/09/2026).

### 1.4 Mínimo personal y familiar estatal (arts. 57-61) — confianza A
| Concepto | Importe anual | Artículo |
|---|---|---|
| Mínimo del contribuyente | 5.550 € | 57.1 |
| + más de 65 años | +1.150 € | 57.2 |
| + más de 75 años (adicional) | +1.400 € | 57.2 |
| Descendiente 1.º / 2.º / 3.º / 4.º y siguientes | 2.400 / 2.700 / 4.000 / 4.500 € | 58.1 |
| Descendiente menor de 3 años | +2.800 € | 58.2 |
| Requisitos del descendiente | menor de 25 años (o con discapacidad), conviva, rentas ≤ 8.000 € | 58.1 |
| Ascendiente > 65 (o con discapacidad) / > 75 | 1.150 € / +1.400 € | 59 |
| Discapacidad contribuyente ≥33 % / ≥65 % | 3.000 € / 9.000 € (+3.000 € de asistencia si procede) | 60.1 |
| Reparto entre progenitores | a partes iguales | 61.1.ª |

### 1.5 Mínimos autonómicos (sustituyen a los estatales para la cuota autonómica) — confianza A/B
| CCAA | Mínimo contribuyente | Descendientes 1.º-4.º | Norma (BOE consolidado) | Estado |
|---|---|---|---|---|
| Madrid | 5.956,65 (+1.234,26 >65; +1.502,58 >75) | ver art. 3 de la norma | DLeg 1/2010, art. 2 — [BOCM-m-2010-90068](https://www.boe.es/buscar/act.php?id=BOCM-m-2010-90068) | A (desde 2023) |
| C. Valenciana | 6.105 (+1.265; +1.540) | 2.640 / 2.970 / 4.400 / 4.950; <3 años +3.080 | Ley 13/1997, art. 2 bis — [BOE-A-1998-8202](https://www.boe.es/buscar/act.php?id=BOE-A-1998-8202) | A |
| Galicia | 5.789 (+1.199; +1.460) | 2.503 / 2.816 / 4.172 / 4.694; <3 años +2.920 | DLeg 1/2011, art. 4 bis — [BOE-A-2011-18161](https://www.boe.es/buscar/act.php?id=BOE-A-2011-18161) | A |
| Andalucía | 5.790 (+1.200; +1.460) | 2.510 / 2.820 / … (resto en el art.) | Ley 5/2021, art. 23 bis — [BOE-A-2021-17915](https://www.boe.es/buscar/act.php?id=BOE-A-2021-17915) | A (falta copiar 3.º y 4.º) |
| Asturias | 6.105 (+1.265; +1.540) | — | DLeg 2/2014, art. 2 bis (Ley 3/2025) — [BOE-A-2015-945](https://www.boe.es/buscar/act.php?id=BOE-A-2015-945) | A |
| Illes Balears | +10 % a mínimos >65/>75, 2.º-4.º descendiente, ascendientes y discapacidad | — | DLeg 1/2014, art. 2 — [BOE-A-2014-6925](https://www.boe.es/buscar/act.php?id=BOE-A-2014-6925) | A |
| Cataluña | 5.550 general (art. 611-2) | — | DLeg 1/2024, libro VI — [BOE-A-2024-6951](https://www.boe.es/buscar/act.php?id=BOE-A-2024-6951) | B (puede haber mínimo incrementado para rentas bajas: NO VERIFICADO) |
| La Rioja | estatales; deflactación automática si IPC dic. > 3 % (art. 31 ter, Ley 9/2025) | — | [BOE-A-2017-13750](https://www.boe.es/buscar/act.php?id=BOE-A-2017-13750) | B |
| Resto (Aragón, Canarias, Cantabria, CyL, CLM, Extremadura, Murcia) | **NO VERIFICADO** si tienen mínimos propios | | | no usar sin revisar |

### 1.6 Escalas autonómicas de la base liquidable general, ejercicio 2026 — confianza A salvo indicación
Formato: `desde | tipo %`. Cada tramo llega hasta el «desde» del siguiente. Cifras leídas en el BOE consolidado; la cuota acumulada se puede recalcular (comprobado en Valencia y Andalucía).

| CCAA | Tramos (desde € → tipo %) | Norma y artículo | Efectos / confianza |
|---|---|---|---|
| Andalucía | 0→9,50; 13.000→12,00; 21.100→15,00; 35.200→18,50; 60.000→22,50 | Ley 5/2021, art. 23 ([BOE-A-2021-17915](https://www.boe.es/buscar/act.php?id=BOE-A-2021-17915)), redacción DL 7/2022 | desde 2022 · A |
| Aragón | 0→9,50; 13.072,50→12,00; 21.210→15,00; 36.960→18,50; 52.500→20,50; 60.000→23,00; 80.000→24,00; 90.000→25,00; 130.000→25,50 | DLeg 1/2005, art. 110-1 ([BOA-d-2005-90006](https://www.boe.es/buscar/act.php?id=BOA-d-2005-90006)), Ley 17/2023 | desde 2023 · A |
| Asturias | 0→9,00; 12.450→12,00; 17.707,20→14,00; 33.007,20→19,20; 53.407,20→21,50; 70.000→22,50; 90.000→25,00; 175.000→26,00 | DLeg 2/2014, art. 2 ([BOE-A-2015-945](https://www.boe.es/buscar/act.php?id=BOE-A-2015-945)), Ley 3/2025 (en vigor dic-2025) | 2025 y 2026 · A |
| Illes Balears | 0→9,00; 10.000→11,25; 18.000→14,25; 30.000→17,50; 48.000→19,00; 70.000→21,75; 90.000→22,75; 120.000→23,75; 175.000→24,75 | DLeg 1/2014, art. 1 ([BOE-A-2014-6925](https://www.boe.es/buscar/act.php?id=BOE-A-2014-6925)), Ley 12/2023 | desde 2024 · A |
| Canarias | 0→9,00; 13.748→11,50; 19.422→14,00; 35.924→18,50; 57.566→23,50; 93.268→25,00; 123.745→26,00 | DLeg 1/2009, art. 18 bis ([BOC-j-2009-90008](https://www.boe.es/buscar/act.php?id=BOC-j-2009-90008)), Ley 9/2025 (efectos 1/1/2025) | 2025 y 2026 · A |
| Cantabria | 0→8,50; 13.000→11,00; 21.000→14,50; 35.200→18,00; 60.000→22,50; 90.000→24,50 | DLeg 62/2008, art. 1 ([BOCT-c-2008-90028](https://www.boe.es/buscar/act.php?id=BOCT-c-2008-90028)), Ley 3/2023 | desde 2024 · A |
| Castilla-La Mancha | 0→9,50; 12.450→12,00; 20.200→15,00; 35.200→18,50; 60.000→22,50 (igual a la estatal sin el tramo 300.000) | Ley 8/2013, art. 13 bis ([BOE-A-2014-1368](https://www.boe.es/buscar/act.php?id=BOE-A-2014-1368)) | desde 2015 · A |
| Castilla y León | 0→9,0; 12.450→12,0; 20.200→14,0; 35.200→18,5; 53.407,20→21,5 | DLeg 1/2013, art. 1 ([BOCL-h-2013-90254](https://www.boe.es/buscar/act.php?id=BOCL-h-2013-90254)), Ley 2/2022 | desde 2022 · **B** (consolidado actualizado por última vez el 17/07/2024) |
| Cataluña | 0→9,50; 12.500→12,50; 22.000→16,00; 33.000→19,00; 53.000→21,50; 90.000→23,50; 120.000→24,50; 175.000→25,50 | DLeg 1/2024, art. 611-1 ([BOE-A-2024-6951](https://www.boe.es/buscar/act.php?id=BOE-A-2024-6951)), DL 5/2025 | desde 2025 · A |
| Extremadura | 0→7,75; 12.450→9,75; 20.200→16,00; 24.200→17,50; 35.200→21,00; 60.000→23,50; 80.200→24,00; 99.200→24,50; 120.200→25,00 | DLeg 1/2018, art. 1 ([BOE-A-2018-8159](https://www.boe.es/buscar/act.php?id=BOE-A-2018-8159)), Ley 2/2026 de 3 de agosto | **efectos 1/1/2026** · A |
| Galicia | 0→9,00; 12.985,35→11,65; 21.068,60→14,90; 35.200→18,40; 60.000→22,50 | DLeg 1/2011, art. 4 ([BOE-A-2011-18161](https://www.boe.es/buscar/act.php?id=BOE-A-2011-18161)), Ley 7/2022 | desde 2022 · A |
| Madrid | 0→8,50; 13.362,22→10,70; 19.004,63→12,80; 35.425,68→17,40; 57.320,40→20,50 | DLeg 1/2010, art. 1 ([BOCM-m-2010-90068](https://www.boe.es/buscar/act.php?id=BOCM-m-2010-90068)), Ley 13/2023 | desde 2023 · A |
| Región de Murcia | 0→9,50; 12.450→11,20; 20.200→13,30; 34.000→17,90; 60.000→22,50 | DLeg 1/2010, art. 2 ([BOE-A-2011-10542](https://www.boe.es/buscar/act.php?id=BOE-A-2011-10542)) | **B**: la DA 5.ª fijaba escalas solo para 2019-2022; desde 2023 rige el art. 2. Confirmar que no hay escala transitoria para 2026 |
| La Rioja | 0→8,00; 12.450→10,60; 20.200→13,60; 35.200→17,80; 40.000→18,30; 50.000→19,00; 60.000→24,50; 120.000→27,00 | Ley 10/2017, art. 31 ([BOE-A-2017-13750](https://www.boe.es/buscar/act.php?id=BOE-A-2017-13750)), Ley 13/2023 | desde 2024 · A (posible deflactación por art. 31 ter: si el IPC de diciembre de 2025 fue > 3 %, NO VERIFICADO) |
| C. Valenciana | 0→8,8; 12.000→11,7; 22.000→14,6; 32.000→17; 42.000→19,4; 52.000→21,9; 62.000→24,4; 72.000→26,1; 100.000→27,35; 150.000→28,35; 200.000→29,35 | Ley 13/1997, art. 2 ([BOE-A-1998-8202](https://www.boe.es/buscar/act.php?id=BOE-A-1998-8202)), Ley 5/2026 de 31 de julio, art. 18 ([BOE-A-2026-19331](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-19331)) | **efectos 1/1/2026** · A |
| Ceuta y Melilla | escala estatal supletoria + deducción del 60 % (art. 68.4) | Ley 35/2006 | NO VERIFICADO en detalle |
| País Vasco / Navarra | IRPF foral completo | Normas forales | **NO VERIFICADO** |

**Escala conocida para 2027: solo C. Valenciana** (Ley 5/2026, disp. transitoria 3.ª, efectos 1/1/2027): 0→8,7; 12.000→11,6; 22.000→14,5; 32.000→16,9; 42.000→19,3; 52.000→21,8; 62.000→24,3; 72.000→26; 100.000→27,25; 150.000→28,25; 200.000→29,25. Confianza A.

### 1.7 Rendimientos del trabajo — confianza A
| Parámetro | Valor | Artículo |
|---|---|---|
| Gastos deducibles: cotizaciones SS, derechos pasivos, colegios de huérfanos | importe real | 19.2.a-c |
| Cuotas a sindicatos y colegios profesionales obligatorios | real, con límite reglamentario (colegios: 500 € en el Reglamento, **NO VERIFICADO** aquí) | 19.2.d |
| Defensa jurídica frente al pagador | hasta 300 €/año | 19.2.e |
| **Otros gastos** | **2.000 €/año** | 19.2.f |
| + movilidad geográfica (desempleado que se traslada) | +2.000 € (año del traslado y el siguiente) | 19.2.f |
| + discapacidad trabajador activo / ≥65 % o ayuda de terceros | +3.500 € / +7.750 € | 19.2.f |
| Límite de «otros gastos» | el rendimiento íntegro menos el resto de gastos | 19.2.f |
| En conjunta, los 2.000 € | se aplican a cada perceptor de rendimientos del trabajo (es un gasto de cada rendimiento) | inferido del art. 19.2.f: **confirmar en AEAT antes de publicar (C pendiente)** |

**Reducción por obtención de rendimientos del trabajo (art. 20, redacción RDL 4/2024, efectos 1/1/2024)** — sobre rendimiento neto = íntegro − gastos a) a e) (sin los 2.000 €); exige rentas distintas del trabajo ≤ 6.500 €:
- RN ≤ 14.852 €: **7.302 €**
- 14.852 < RN ≤ 17.673,52 €: 7.302 − 1,75 × (RN − 14.852)
- 17.673,52 < RN < 19.747,5 €: 2.364,34 − 1,14 × (RN − 17.673,52)
- RN ≥ 19.747,5 €: 0. El resultado no puede dejar el rendimiento negativo.

**Deducción por obtención de rendimientos del trabajo (DA 61.ª, redacción RDL 5/2026 con efectos 1/1/2026, BOE-A-2026-3810, convalidado por BOE-A-2026-6483)** — se resta de la cuota líquida total:
- Rendimientos íntegros del trabajo ≤ 17.094 €: **590,89 €**
- Entre 17.094 € y 20.048,45 €: 590,89 − 0,2 × (RIT − 17.094)
- Requisitos: relación laboral o estatutaria; otras rentas ≤ 6.500 €; límite: la parte de cuota íntegra estatal + autonómica que corresponda a esos rendimientos.
- 17.094 € = SMI 2026 (1.221 €/mes × 14), RD 126/2026 ([BOE-A-2026-3815](https://www.boe.es/buscar/act.php?id=BOE-A-2026-3815)).

### 1.8 Obligación de declarar (art. 96, ejercicio 2026) — confianza A
| Límite | Importe |
|---|---|
| Rendimientos íntegros del trabajo, un pagador (o 2.º y siguientes ≤ 1.500 €) | 22.000 € |
| Varios pagadores (2.º y siguientes > 1.500 €), pensiones compensatorias, pagador no obligado a retener, tipo fijo | 15.876 € |
| Capital mobiliario y ganancias con retención | 1.600 € |
| Rentas inmobiliarias imputadas, Letras del Tesoro, subvenciones VPO | 1.000 € |
| Rentas totales de cualquier tipo + pérdidas < 500 € | 1.000 € |
| Alta en RETA en cualquier momento del año | siempre obliga |
| Aportaciones a planes de pensiones que se quieran reducir | obligan a declarar (art. 96.4) |
Nota: la subida del límite de 15.876 € del RDL 9/2024 quedó sin efecto (derogación, BOE-A-2025-1136).

### 1.9 Otras deducciones estatales útiles para el veredicto — confianza A
- Maternidad (art. 81): 1.200 €/año por hijo < 3 años; +1.000 € por guardería autorizada (ver sección 6).
- Familia numerosa / discapacidad a cargo (art. 81 bis): 1.200 €/año (general), +100 % en categoría especial, +600 € por hijo que exceda el mínimo de la categoría. En conjunta se aplican en la declaración única (prorrateo entre contribuyentes con derecho, art. 81 bis.1).
- Cónyuge con discapacidad, sin rentas > 8.000 €: 1.200 €/año (art. 81 bis.1.d).

---

## 2. Energía: `luz-fija-o-indexada` y `placas-solares-merece-la-pena` — PRIORIDAD 2

### 2.1 Peajes de transporte y distribución 2.0TD, desde 1/1/2026 — confianza A
Resolución CNMC de 18/12/2025 — [BOE-A-2025-26348](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-26348).
| Término | P1 | P2 | P3 |
|---|---|---|---|
| Potencia peaje T+D (€/kW·año) | 23,324952 | 0,443770 | — |
| Energía peaje T+D (€/kWh) | 0,033261 | 0,016409 | 0,000077 |
| Exceso de potencia tipo 4-5 (€/kW·día) | 0,279426 | 0,005316 | — |

### 2.2 Cargos del sistema, segmento 1 (2.0TD), desde 1/1/2026 — confianza A
Orden TED/1524/2025, de 23 de diciembre — [BOE-A-2025-26705](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2025-26705).
| Término | P1 | P2 | P3 |
|---|---|---|---|
| Potencia cargos (€/kW·año) | 4,379461 | 0,281653 | — |
| Energía cargos (€/kWh) | 0,064292 | 0,012858 | 0,003215 |

Peaje + cargo de potencia 2.0TD = **27,704413 €/kW·año (P1)** y **0,725423 €/kW·año (P2)**. Peaje + cargo de energía = **0,097553 / 0,029267 / 0,003292 €/kWh** (P1/P2/P3). (Suma hecha por el Investigador; el Constructor debe recalcularla.)
El reparto de la financiación del bono social de 2026 se rehízo con la Orden TED/634/2026 (BOE-A-2026-13759): **importe por cliente NO VERIFICADO**.

### 2.3 PVPC — estructura del término de energía (RD 216/2014, consolidado) — confianza A
[BOE-A-2014-3376](https://www.boe.es/buscar/act.php?id=BOE-A-2014-3376), arts. 9 y 10 bis (redacción RD 446/2023):
- Coste de producción horario CPh = Pmh + Tah + SAh + OCh.
- Peso del mercado diario/intradiario **A = 0,45**; peso de la cesta de futuros **B = 0,55**.
- Cesta de futuros: anual 0,54; trimestral 0,36; mensual 0,10.
- Precios horarios: los publica REE (e·sios) cada día antes de las 20:15. **No hay un €/kWh fijo**: la calculadora debe pedir o cargar el precio medio del mes con fuente y fecha.
- Margen de comercialización fijo (CCF): **3,113 €/kW·año**, Orden ETU/1948/2016, anexo II ([BOE-A-2016-12274](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2016-12274)); sin orden posterior, se sigue aplicando · A− (contrastar con factura PVPC actual). Alquiler del contador: no modelado. El PVPC solo existe hasta 10 kW.

### 2.4 Impuestos sobre la factura de luz — confianza A/B
| Concepto | Valor vigente en octubre 2026 | Fuente | Nov-dic 2026 |
|---|---|---|---|
| Impuesto Especial sobre la Electricidad | **5,11269632 %** (mínimo 1 €/MWh uso doméstico) | Ley 38/1992, art. 99 — [BOE-A-1992-28741](https://www.boe.es/buscar/act.php?id=BOE-A-1992-28741) | 0,5 % **solo si** IPC electricidad sept./oct. > +15 % interanual (RDL 25/2026, arts. 20-21) · B |
| IVA electricidad (≤ 10 kW) | **21 %** | Ley 37/1992 (tipo general) | 10 % con la misma condición (RDL 25/2026, arts. 18-19) · B |
| Historia 2026 | IEE 0,5 % e IVA 10 % del 22/3 al 30/6 (RDL 7/2026, arts. 40 y 42); agosto y septiembre condicionados (RDL 18/2026, arts. 10-13) | | |

### 2.5 Bono social eléctrico 2026 — confianza A
- Descuentos **todo 2026**: vulnerable **42,5 %**, vulnerable severo **57,5 %** (RDL 7/2026, art. 1, convalidado; [BOE-A-2026-6544](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-6544)). Se aplican sobre el PVPC (solo con comercializadora de referencia).
- Requisitos de renta y energía con descuento: RD 897/2017 ([BOE-A-2017-11505](https://www.boe.es/buscar/act.php?id=BOE-A-2017-11505)) · requisitos **NO VERIFICADOS** en detalle.
- Bono social térmico: ayuda mínima aumentada (RDL 7/2026, art. 2): importe **NO VERIFICADO**.

### 2.6 TUR de gas (ya en `params.json`)
- TUR del 1/10/2026: [BOE-A-2026-20389](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20389) (ya verificado por el Constructor). El RDL 25/2026, art. 1 limita la variación del coste de la materia prima en la TUR: revisar si la resolución del 30/9 ya lo aplica.

### 2.7 Autoconsumo: compensación de excedentes — confianza A
RD 244/2019, art. 14 (consolidado; [BOE-A-2019-5089](https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089)):
- Requisitos para la compensación simplificada (art. 4.2.a): renovable, **potencia ≤ 100 kW**, contrato único de suministro, contrato de compensación, sin régimen retributivo.
- **Con PVPC**: el kWh vertido se valora al **Pmh − CDSVh** horario (precio del mercado menos coste de desvíos), publicado por REE.
- **Con comercializadora libre**: precio pactado en el contrato.
- **Tope**: la compensación no puede superar el valor de la energía consumida de la red en el periodo de facturación (máx. 1 mes). Lo que sobra se pierde (salvo «batería virtual» comercial, que no es regulada).
- No hay un precio oficial fijo de compensación: cualquier cifra es un supuesto.

### 2.8 Deducciones IRPF por autoconsumo y eficiencia (estatales) — confianza A
| Deducción | % | Base máx. anual | Plazo | Norma |
|---|---|---|---|---|
| Autoconsumo renovable en inmueble propio (con o sin baterías) | **10 %** | 5.000 € | cantidades pagadas del 1/1 al 31/12/2026; instalación terminada **en 2026** | DA 62.ª LIRPF, añadida por RDL 7/2026 art. 36.3 (convalidado) |
| Autoconsumo en edificio residencial (comunidad) | **20 %** | 5.000 € | igual | DA 62.ª.2 |
| Incompatible con | DA 50.ª para la misma instalación; requiere Certificado de Instalación Eléctrica (CIE) | | | DA 62.ª.3 y 5 |
| Obras que reduzcan ≥ 7 % la demanda de calefacción y refrigeración | 20 % | 5.000 € | pagos hasta 31/12/2026; certificado antes de 1/1/2027 | DA 50.ª.1 |
| Obras que reduzcan ≥ 30 % el consumo de energía primaria no renovable o lleguen a A/B | 40 % | 7.500 € | pagos hasta 31/12/2026; certificado antes de 1/1/2027 | DA 50.ª.2 |
| Rehabilitación energética del edificio (comunidad) | 60 % | 5.000 €/año, acumulado 15.000 € | pagos hasta **31/12/2027**; certificado antes de 1/1/2028 | DA 50.ª.3 |
No se pueden pagar en efectivo; se descuentan las subvenciones. Para 2027 solo sigue la del 60 % (comunidades). La del 10 % de autoconsumo **no existe para instalaciones terminadas en 2027** salvo nueva prórroga.
- **Bonificaciones IBI e ICIO** por placas: son potestativas de cada ayuntamiento (TRLRHL arts. 74.5 y 103.2) → **NO VERIFICADO** por municipio. La calculadora debe dejarlas como dato del usuario.
- Deducciones autonómicas por autoconsumo: **NO VERIFICADO**.

---

## 3. Planes de pensiones: `plan-pensiones-o-fondo-indexado` y `rescate-plan-pensiones-capital-o-renta` — PRIORIDAD 3

### 3.1 Límites de aportación y reducción (Ley 35/2006, arts. 51-52, 84.2.1.º) — confianza A
| Parámetro | Valor | Artículo |
|---|---|---|
| Límite conjunto general | el menor de **30 %** de (rend. netos trabajo + actividades) y **1.500 €/año** | 52.1 |
| Incremento por contribuciones empresariales (planes de empleo) | +8.500 €/año | 52.1.1.º |
| Aportación del trabajador al mismo plan de empleo: máx. según contribución empresarial | ≤ 500 € → 2,5 × contribución; 500,01-1.500 € → 1.250 + 0,25 × (C − 500); > 1.500 € → 1 × contribución; multiplicador 1 si rend. trabajo de esa empresa > 60.000 € | 52.1.1.º |
| Incremento autónomos (planes sectoriales o de empleo simplificados) | +4.250 €/año | 52.1.2.º |
| Tope de los dos incrementos juntos | 8.500 €/año (máximo total 10.000 €) | 52.1 |
| Seguros colectivos de dependencia pagados por la empresa | +5.000 €/año | 52.1 |
| Aportaciones a plan del cónyuge con rendimientos < 8.000 € | hasta 1.000 €/año adicionales | 51.7 |
| Exceso no reducido | se reduce en los 5 ejercicios siguientes | 52.2 |
| En conjunta | límites **por cada partícipe** | 84.2.1.º |
| Efecto | reduce la base imponible **general** (ahorro fiscal = tipo marginal general estatal + autonómico) | 51 |

### 3.2 Rescate — confianza A (ley) y C (40 %)
| Parámetro | Valor | Fuente |
|---|---|---|
| Naturaleza de la prestación | **rendimiento del trabajo** (base general, escala general), sea capital o renta | art. 17.2.a.3.ª LIRPF · A |
| Reducción del 40 % | solo en **capital**, solo por la parte de aportaciones hasta 31/12/2006, si pasaron > 2 años desde la primera aportación (salvo invalidez) | DT 12.ª LIRPF (remite al art. 17 del TRLIRPF de 2004) · A; el 40 % y los 2 años según AEAT, [Manual Renta 2025, régimen transitorio](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c03-rendimientos-trabajo/rendimiento-neto-trabajo-integrar-base-imponible/fase-1-determinacion-rendimiento-integro-trabajo/reducciones-aplicables-sobre-determinados-rendimientos-integros/c-regimen-transitorio-reducciones-aplicable-prestaciones/prestaciones-percibidas-forma-capital-derivadas.html) · C |
| Plazo para el 40 % | año de la contingencia y los 2 siguientes (contingencias desde 2015) | DT 12.ª.4 · A |
| Contingencias 2011-2014 | hasta el 8.º ejercicio siguiente | DT 12.ª.4 · A |
| Contingencias 2010 o antes | ya no (plazo acabó 31/12/2018) | DT 12.ª.4 · A |
| Rescate anticipado de aportaciones con más de 10 años (desde 2025) | mismo tratamiento que prestación | AEAT Manual 2025 · C (TRLPFP art. 8.8: **NO VERIFICADO** en BOE) |
| Renta: retenciones | según tabla general de retenciones del trabajo | no necesario para la decisión |

### 3.3 Fondo indexado (alternativa) — confianza A
- Ganancia al reembolsar → base del **ahorro** (escala 19-30 %, sección 1.2).
- Traspasos entre fondos sin tributar (art. 94 LIRPF): **NO VERIFICADO** en esta sesión; leer art. 94 antes de publicar.

---

## 4. Vivienda: `cuanto-ahorrar-para-comprar-casa` — PRIORIDAD 4

### 4.1 Vivienda nueva (primera entrega) — confianza A
| Concepto | Tipo | Norma |
|---|---|---|
| IVA vivienda (con hasta 2 garajes y anexos) | **10 %** | Ley 37/1992, art. 91.Uno.1.7.º — [BOE-A-1992-28740](https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740) |
| IVA VPO de régimen especial o promoción pública (entrega por el promotor) | **4 %** | art. 91.Dos.1.6.º · **B**: redacción cambiada por el RDL 26/2026 con efectos 1/12/2026, **sin convalidar** |
| Canarias: IGIC en lugar de IVA | **NO VERIFICADO** | |
| AJD (escritura de compra con IVA) | tipo general autonómico de documentos notariales (tabla 4.2) | TRLITPAJD art. 31.2 + norma autonómica |

### 4.2 ITP (vivienda usada) y AJD por comunidad, 2026 — confianza A salvo indicación
| CCAA | ITP general inmuebles | ITP reducido vivienda habitual (resumen; requisitos en la norma) | AJD general | AJD reducido vivienda habitual | Norma (BOE consolidado) |
|---|---|---|---|---|---|
| Andalucía | 7 % | 6 % si vivienda ≤ 150.000 €; 3,5 % jóvenes < 35 (≤ 150.000 €) o discapacidad (≤ 250.000 €) | 1,2 % | 1 % / 0,3 % / 0,1 % en los mismos supuestos | Ley 5/2021, arts. 41, 43, 49, 50 (redacción 2026) |
| Aragón | escala: 8 % hasta 400.000; 8,5 % hasta 450.000; 9 % hasta 500.000; 9,5 % hasta 750.000; 10 % resto (tipo medio) | NO VERIFICADO | 1,5 % | NO VERIFICADO | DLeg 1/2005, arts. 121-1 y 122-1 |
| Asturias | 8 % hasta 300.000; 9 % hasta 500.000; 10 % resto (según valor íntegro) | NO VERIFICADO | 1,2 % | NO VERIFICADO | DLeg 2/2014, arts. 26 y 34 |
| Illes Balears | tarifa: 8 % hasta 400.000; 9 % hasta 600.000; 10 % hasta 1.000.000; 12 % hasta 2.000.000; 13 % resto (tipo medio) | NO VERIFICADO (art. 17, reformado jun-2026) | 1,5 % | NO VERIFICADO | DLeg 1/2014, arts. 10 (redacción jun-2026) y 15 |
| Canarias | 6,5 % | 5 % vivienda habitual ≤ 200.000 € con requisitos; otros reducidos (familia numerosa, discapacidad, monoparental, VPO) | 0,75 % (1 % si la operación está sujeta a IGIC/IVA) | NO VERIFICADO | DLeg 1/2009, arts. 31-34 y 36 |
| Cantabria | **9 %** | 7 % hasta 300.000 € y 9 % en el exceso (vivienda habitual); 4 % familia numerosa, monoparental, discapacidad | 1,5 % | NO VERIFICADO | DLeg 62/2008, arts. 9 y 13 (Ley 5/2026, en vigor 1/5/2026) |
| Castilla-La Mancha | 9 % | NO VERIFICADO | 1,5 % | 0,75 % primera vivienda ≤ 180.000 € con hipoteca > 50 % | Ley 8/2013, arts. 19 y 21 |
| Castilla y León | 8 %; 10 % en la parte que exceda de 250.000 € | 4 % familia numerosa, discapacidad y otros (art. 25.3) | 1,5 % | NO VERIFICADO | DLeg 1/2013, arts. 24-25 · **B** (consolidado de 2024) |
| Cataluña | tarifa: 10 % hasta 600.000; 11 % hasta 900.000; 12 % hasta 1.500.000; 13 % resto (tipo medio); VPO 7 % | jóvenes, familia numerosa, monoparental, discapacidad, violencia machista (arts. 641-2 a 641-5 bis): tipos NO VERIFICADOS | 1,5 % (2 % hipotecas con prestador sujeto pasivo) | NO VERIFICADO | DLeg 1/2024, arts. 641-1 y 642-1 |
| Extremadura | escala: 8 % hasta 360.000; 10 % hasta 600.000; 11 % resto (por tramos) | 7 % vivienda ≤ 200.000 € y renta ≤ 30.000 € (55.000 € conjunta); 4 % zonas rurales y colectivos | 1,5 % | 0,5 % vivienda habitual (art. 47, Ley 2/2026) | DLeg 1/2018, arts. 36, 40, 41, 44 bis, 46, 47 |
| Galicia | **8 %** (2026) | 7 % vivienda habitual con requisitos | 1,5 % | 1 % con requisitos | DLeg 1/2011, arts. 14 y 15 (redacción 2026) |
| Madrid | 6 % | 4 % familia numerosa | 0,75 % | 0,4 % (≤ 120.000 €), 0,5 % (≤ 180.000 €) y otros (art. 32) | DLeg 1/2010, arts. 28, 29, 32, 36 |
| Región de Murcia | 7,75 % | NO VERIFICADO | 1,5 % | NO VERIFICADO | DLeg 1/2010, arts. 6 y 7 (Ley 3/2025) |
| La Rioja | 7 % | 5 % familia numerosa (3 % con requisitos) y otros | 1 % | NO VERIFICADO (art. 49) | Ley 10/2017, arts. 44, 45, 48 |
| C. Valenciana | 9 %; 11 % si el valor supera 1.000.000 € | 8 % jóvenes < 35 o VPO > 180.000 € (con límites de renta); otros reducidos | 1,4 % | **0,1 %** en la compra de vivienda habitual (art. 14.Uno.a, Ley 5/2026) | Ley 13/1997, arts. 13 y 14 |
| País Vasco / Navarra | **NO VERIFICADO** | | | | normas forales |
| Ceuta y Melilla | **NO VERIFICADO** (bonificación del 50 %) | | | | |

Para v1 recomiendo: tipo general por comunidad + **un** tipo de vivienda habitual solo donde la tabla lo da sin «NO VERIFICADO», con texto «puede pagar menos si cumple requisitos (joven, familia numerosa, discapacidad)».
El RDL 7/2026 (disp. final 3.ª) modificó el texto refundido estatal del ITP: **alcance NO VERIFICADO** (revisar si afecta a vivienda).

---

## 5. `autonomo-o-asalariado` — PRIORIDAD 5

Orden PJC/297/2026, de 30 de marzo, de cotización 2026 — [BOE-A-2026-7296](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7296). Confianza A.

### 5.1 RETA: base por rendimientos netos mensuales (art. 18.1) — las cifras de 2026 son **iguales a las de 2025** (tabla congelada)
| Tabla | Tramo | Rendimientos netos €/mes | Base mínima | Base máxima |
|---|---|---|---|---|
| Reducida | 1 | ≤ 670 | 653,59 | 718,94 |
| Reducida | 2 | > 670 y ≤ 900 | 718,95 | 900,00 |
| Reducida | 3 | > 900 y < 1.166,70 | 849,67 | 1.166,70 |
| General | 1 | ≥ 1.166,70 y ≤ 1.300 | 950,98 | 1.300,00 |
| General | 2 | > 1.300 y ≤ 1.500 | 960,78 | 1.500,00 |
| General | 3 | > 1.500 y ≤ 1.700 | 960,78 | 1.700,00 |
| General | 4 | > 1.700 y ≤ 1.850 | 1.143,79 | 1.850,00 |
| General | 5 | > 1.850 y ≤ 2.030 | 1.209,15 | 2.030,00 |
| General | 6 | > 2.030 y ≤ 2.330 | 1.274,51 | 2.330,00 |
| General | 7 | > 2.330 y ≤ 2.760 | 1.356,21 | 2.760,00 |
| General | 8 | > 2.760 y ≤ 3.190 | 1.437,91 | 3.190,00 |
| General | 9 | > 3.190 y ≤ 3.620 | 1.519,61 | 3.620,00 |
| General | 10 | > 3.620 y ≤ 4.050 | 1.601,31 | 4.050,00 |
| General | 11 | > 4.050 y ≤ 6.000 | 1.732,03 | 5.101,20 |
| General | 12 | > 6.000 | 1.928,10 | 5.101,20 |
Rendimiento neto computable: lo define el art. 308 LGSS (incluye una deducción por gastos genéricos del 7 %, 3 % en societarios): **NO VERIFICADO** en esta sesión → leer TRLGSS art. 308 antes de publicar.

### 5.2 Tipos RETA 2026 (art. 18.2 y 37)
| Concepto | Tipo |
|---|---|
| Contingencias comunes | 28,30 % |
| Contingencias profesionales | 1,30 % |
| Cese de actividad | 0,90 % |
| Formación profesional | 0,10 % |
| MEI (equidad intergeneracional) | 0,90 % |
| **Total** | **31,50 %** sobre la base elegida |
Tarifa plana y bonificaciones de nuevos autónomos: **NO VERIFICADO**.

### 5.3 Régimen General 2026 (asalariado)
| Concepto | Empresa | Trabajador | Total | Artículo |
|---|---|---|---|---|
| Contingencias comunes | 23,60 % | 4,70 % | 28,30 % | 4.a |
| Desempleo, contrato indefinido | 5,50 % | 1,55 % | 7,05 % | 33.2.a.1.º |
| Desempleo, contrato temporal | 6,70 % | 1,60 % | 8,30 % | 33.2.a.2.º |
| FOGASA | 0,20 % | — | 0,20 % | 33.2.b |
| Formación profesional | 0,60 % | 0,10 % | 0,70 % | 33.2.c |
| MEI | 0,75 % | 0,15 % | 0,90 % | 16 |
| AT y EP | tarifa de primas (DA 61.ª LGSS), varía por actividad | — | — | 4.b — **NO VERIFICADO** valor típico |
| Cotización de solidaridad | 1,15 % (0,96 + 0,19) sobre la parte entre 5.101,21 y 5.611,32 €/mes; tramos superiores en el art. 17 | | | 17 |
Indefinido típico (sin AT): empresa 30,65 %, trabajador 6,50 %.
- Tope máximo de base: **5.101,20 €/mes** (art. 2.1; RDL 3/2026).
- Base mínima grupos 4-7: **1.424,40 €/mes**; grupo 1: 1.989,30; grupo 2: 1.649,70; grupo 3: 1.435,20; grupos 8-11: 47,48 €/día (art. 3).
- SMI 2026: **1.221 €/mes (14 pagas) = 17.094 €/año**; 40,70 €/día (RD 126/2026, art. 1).
- 2027: **NO hay orden de cotización 2027**; no publicar cifras de 2027.

---

## 6. `guarderia-cuidadora-o-reducir-jornada` — PRIORIDAD 6

### 6.1 Deducción por maternidad (art. 81 LIRPF, redacción Ley 31/2022) — confianza A
| Parámetro | Valor |
|---|---|
| Importe | hasta **1.200 €/año** por hijo < 3 años (100 €/mes) |
| Quién | madre (o padre/tutor en los supuestos del art.), con prestación de desempleo al nacer o de alta en SS/mutualidad (≥ 30 días cotizados) |
| Incremento por guardería | hasta **+1.000 €/año** por gastos en guardería o centro de educación infantil **autorizado** (matrícula, asistencia, comida; meses completos) |
| Límite del incremento | gasto efectivo no subvencionado |
| Extensión | el año en que cumple 3, hasta el mes anterior al 2.º ciclo de infantil |
| Alta posterior al nacimiento | +150 € en el mes en que se cumplen los 30 días cotizados |
| Incompatibilidad | meses en que se cobra el complemento de ayuda para la infancia del IMV |
| Cuidadora o «canguro» | **no** dan derecho al incremento de 1.000 € (solo guardería autorizada) |

### 6.2 Empleada de hogar: cotización 2026 (Orden PJC/297/2026, arts. 15 y 35) — confianza A
Bases de contingencias comunes por retribución mensual (con prorrata de pagas extra):
| Tramo | Retribución €/mes | Base €/mes |
|---|---|---|
| 1 | ≤ 329,00 | 306,00 |
| 2 | 329,01-510,00 | 436,00 |
| 3 | 510,01-693,00 | 602,00 |
| 4 | 693,01-877,00 | 785,00 |
| 5 | 877,01-1.061,00 | 970,00 |
| 6 | 1.061,01-1.242,00 | 1.151,00 |
| 7 | 1.242,01-1.424,40 | 1.424,40 |
| 8 | ≥ 1.424,41 | retribución real (texto del tramo 8 sin cifra de base en la tabla: **confirmar**) |
| Tipo | Empleador | Empleada |
|---|---|---|
| Contingencias comunes | 23,60 % | 4,70 % |
| Desempleo indefinido / temporal | 5,50 % / 6,70 % | 1,55 % / 1,60 % |
| FOGASA | 0,20 % | — |
| MEI | 0,75 % | 0,15 % (art. 16, Régimen General) |
| AT/EP | tarifa de primas | — |
- SMI por hora de empleada de hogar externa: **9,55 €/hora** (RD 126/2026, art. 4.2).
- Reducción/bonificación del 20 % (o mayor) en la cuota empresarial de empleados de hogar: **NO VERIFICADO** (buscar en la LGSS / RDL 16/2022).

### 6.3 Reducción de jornada por cuidado de hijo
- Cotización al 100 % durante los dos primeros años de reducción por cuidado de menor (LGSS art. 237.3): **NO VERIFICADO** en esta sesión.

### 6.4 Deducciones autonómicas por guardería o cuidado de hijos
**NO VERIFICADO** para las 15 comunidades. Ejemplos que existen (por ver en sus normas): Madrid (gastos educativos y cuidado de hijos), Comunitat Valenciana, Galicia, Castilla y León, Aragón. No usar hasta leer cada artículo.

---

## 7. Lo que cambia en 2027 y ya se sabe
| Parámetro | 2027 | Fuente | Confianza |
|---|---|---|---|
| Escala autonómica C. Valenciana | nueva escala (sección 1.6) | Ley 5/2026, DT 3.ª | A |
| Deducción eficiencia 60 % (comunidades) | sigue: pagos hasta 31/12/2027 | DA 50.ª.3 | A |
| Deducción eficiencia 20 % y 40 % | termina: pagos hasta 31/12/2026 | DA 50.ª.1-2 | A |
| Deducción autoconsumo 10 %/20 % | termina: instalaciones terminadas en 2026 | DA 62.ª | A |
| Escala estatal, mínimos, art. 20, 3.400 € | sin cambios aprobados (no hay PGE 2027) | consolidado 30/09/2026 | A (puede cambiar con PGE o RDL) |
| Bono social 42,5 % / 57,5 % | solo «en el año 2026» | RDL 7/2026 art. 1 | A (en 2027 vuelve a la norma general salvo prórroga) |
| RETA 2027, SMI 2027, peajes y cargos 2027 | desconocidos | — | NO VERIFICADO |

---

## Candidatas c38 (Investigador, 2026-10-02) — 8 laborales/fiscales del backlog
Método: API de consolidados del BOE leída hoy (bloque, última versión). ET = BOE-A-2015-11430 · LGSS = BOE-A-2015-11724 · LIRPF = BOE-A-2006-20764 · RIRPF = BOE-A-2007-6820. Enlace: `https://www.boe.es/buscar/act.php?id=<ID>#<bloque>` (p. ej. `#a56`).
**RDL 26/2026** (BOE-A-2026-20266): a 2-oct-2026 la ficha del BOE no muestra resolución de convalidación. No toca ninguno de los artículos de abajo; en el art. 7 LIRPF solo cambia la letra ñ (ayudas a la rehabilitación). **Sí toca** TRLRHL art. 72 (IBI) y 107.4 (coeficientes de plusvalía municipal, desde el 1-12-2026) → plusvalía e IBI descartadas.

| Calculadora | Norma y bloque | Contenido verificado | Versión vigente | Confianza |
|---|---|---|---|---|
| indemnizacion-despido | ET [a56](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a56) | 33 días/año, se prorratea por meses, tope 24 mensualidades; salarios de tramitación solo si hay readmisión | 13-11-2015 (sin cambios) | A |
| | ET [a53](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a53).1.b-c | objetivo: 20 días/año, tope 12 mensualidades; preaviso de 15 días | LO 1/2025, 3-4-2025 | A |
| | ET [dtundecima](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#dtundecima) | contratos anteriores al 12-2-2012: 45 días hasta esa fecha + 33 después; tope 720 días salvo que el tramo anterior dé más, nunca más de 42 mensualidades | 2015 | A |
| | ET [a49](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a49).1.c-d | fin de temporal: 12 días/año (no en formativos ni sustitución); dimisión con el preaviso del convenio | 1-5-2025 | A |
| | LIRPF [a7](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a7).e | exenta la indemnización obligatoria del ET; la de convenio o pacto no, pero sí la acordada en conciliación (art. 63 LRJS); en ERE y en el 52.c, exenta hasta el límite del improcedente; tope de 180.000 € | 1-10-2026 (cambio solo en ñ) | A |
| | RIRPF a1 / [a73](https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a73) | desvinculación real; si vuelve a la empresa, autoliquidación complementaria | 2015 | A (art. 1: leer el texto antes de construir) |
| finiquito | ET [a38](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a38) | ≥ 30 días naturales, «no sustituible por compensación económica» (la excepción en la extinción es jurisprudencial: citarla como tal) | 2015 | A |
| baja-medica | LGSS [a169](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a169), [a171](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a171), [a173](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a173) | 365 + 180 días; común: subsidio desde el 4.º día, días 4-15 a cargo de la empresa; profesional: desde el día siguiente; casos especiales (menstruación, donación, interrupción del embarazo, semana 39) desde el día 1 o el 2; donación al 100 % | Ley 6/2024, 3-3-2025 | A |
| | [RD 53/1980](https://www.boe.es/eli/es/rd/1980/01/11/53) (BOE-A-1980-1003) | común: 60 % días 4-20, 75 % desde el 21 | — | C (web y BOE; leer el texto) |
| | Decreto 3158/1966 art. 2 (BOE-A-1966-21116) | 75 % de la base (profesional) | 1-12-2001 | A |
| permiso-nacimiento | ET [a48](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a48).4 | 19 semanas por progenitor (32 si es monoparental): a) 6 obligatorias a jornada completa; b) 11 (22) hasta los 12 meses; c) 2 (4) hasta los 8 años, intransferibles; b) y c) pueden ser a jornada parcial con acuerdo | RDL 9/2025, 31-7-2025; **convalidado** (Resolución de 9-9-2025, BOE-A-2025-17999) | A |
| | LGSS [a178](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a178), [a179](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a179) | carencia: < 21 años, ninguna; 21-25, 90 días en 7 años o 180 en la vida; ≥ 26, 180 en 7 años o 360 en la vida; 100 % de la base de contingencias comunes del mes anterior al previo al hecho causante /30 | 31-7-2025 / 1-1-2023 | A |
| | LIRPF a7.h | exentas las prestaciones por nacimiento, con el tope de la prestación máxima de la SS | 1-10-2026 | A |
| retribucion-flexible | LIRPF [a42](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a42).3 | a comedor; b guardería; c seguro de enfermedad 500 €/persona (1.500 € con discapacidad); e transporte colectivo 1.500 €/año; f acciones 12.000 € | 1-1-2023 | A |
| | RIRPF [a45](https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a45).2, a46, a46 bis | fórmulas indirectas de comida: 11 €/día; requisitos del seguro y del pago del transporte | 2018 / 2015 | A |
| subsidio-desempleo | LGSS [a274](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a274), [a275](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a275), [a277](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a277), [a278](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a278) | beneficiarios (< 45 años sin cargas: prestación agotada de ≥ 360 días; ≥ 90 días cotizados sin derecho a la contributiva); rentas ≤ 75 % del SMI sin pagas extra (también por miembro de la unidad familiar); duración en tabla; 95 % del IPREM los primeros 180 días, 90 % hasta el día 360, 80 % después | RDL 2/2024, 23-5-2024 (DT 1.ª superada) | A |
| aceptar-trabajo-con-paro | LGSS [a282](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a282).2-3 | prestación + trabajo a tiempo parcial: se descuenta la parte proporcional (pedirlo en 15 días hábiles). CAE, % del IPREM por trimestre (completa / ≥ 75 % / 50-75 % / < 50 % de jornada): T1 80/75/70/60 · T2 60/50/45/40 · T3 40/35/30/25 · T4 30/25/20/15 · T5 y siguientes 20/15/10/5; máximo 180 días, que se descuentan del subsidio | 23-5-2024 | A |
| kilometraje-y-dietas | RIRPF [a9](https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a9).A | 0,26 €/km + peajes y aparcamiento justificados (Orden HFP/792/2023, BOE-A-2023-16461); manutención con pernocta 53,34 € (España) / 91,35 € (extranjero); sin pernocta 26,67 / 48,08 €; estancia: lo justificado | 17-7-2023 | A |

Pendiente para el Constructor: el texto del RD 53/1980 (subir a A), LGSS art. 147 (qué conceptos cotizan: retribución flexible y vacaciones no disfrutadas), RIRPF art. 1 (desvinculación) y DT única del RDL 9/2025. Descartadas y por qué: ver la nota c38 del backlog.

---

## Candidatas c44 (Investigador, 2026-10-02) — 8 de SS/fiscal del backlog
Método: API de consolidados del BOE (bloque, última versión) y XML del Diario para normas sin consolidar, leídos hoy. Mismos ID que en c38; enlace `https://www.boe.es/buscar/act.php?id=<ID>#<bloque>`.
**RDL 26/2026** (BOE-A-2026-20266, publicado el 30-9-2026, en vigor el 1-10): votación de convalidación en el Congreso el 2-oct, con el no anunciado de PP, Vox y Junts. El análisis del BOE no muestra aún ninguna referencia posterior (ni convalidación ni derogación). Modifica, entre otros, LIRPF (art. 7.ñ y otros), RIRPF arts. 41 bis, 69, 75, 76, 93 y 94, TRLRHL arts. 72 y 107.4 y la Ley 12/2023. No toca ninguna norma de esta tabla. Hay que volver a mirarlo cuando el BOE publique la resolución.

| Calculadora | Norma y bloque | Contenido verificado | Versión vigente | Confianza |
|---|---|---|---|---|
| baja-medica (mejora) | [RD 53/1980](https://www.boe.es/buscar/doc.php?id=BOE-A-1980-1003), artículo único | común: 60 % de la BR del día 4 al 20 inclusive (texto leído en el BOE); el 75 % del día 21 es la regla general del Decreto 3158/1966 art. 2 | 1980 (no está consolidado; sin cambios conocidos) | A (antes C) |
| incapacidad-permanente | LGSS [a194](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a194), [a196](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a196), [a197](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a197), [a198](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a198) | grados; total ≥ 55 % de la base mínima (enfermedad común); complemento de gran incapacidad = 45 % de la base mínima + 30 % de la última base, mínimo 45 % de la pensión; BR común = bases de 96 meses / 112 (24 últimas a valor nominal) × % del art. 210.1 contando como cotizados los años hasta la edad ordinaria (50 % si < 15 años); total compatible con un trabajo de funciones distintas | Ley 2/2025, 1-5-2025 | A |
| | Decreto 1646/1972 art. 6; Orden 15-4-1969 | 55 % total, +20 % cualificada (≥ 55 años), 100 % absoluta | — | B (web; leer el texto) |
| | LIRPF [a7](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a7).f | exentas la absoluta y la gran incapacidad (límite: la prestación de la SS); la total tributa | 1-10-2026 (cambio del RDL 26/2026 solo en otra letra) | A |
| paro-autonomos | LGSS [a330](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a330), [a338](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a338), [a339](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a339) | requisitos (alta, carencia, situación legal de cese, acuerdo de actividad, al corriente); duración: 12-17 → 4 meses, 18-23 → 6, 24-29 → 8, 30-35 → 10, 36-42 → 12, 43-47 → 16, ≥ 48 → 24 (cotizados en 48 meses, ≥ 12 en los últimos 24); BR = media de las bases de 12 meses; 70 % (50 % en cese parcial y fuerza mayor parcial); máx. 175/200/225 % del IPREM, mín. 80/107 % | 2-3-2023 / 1-1-2023 | A |
| ayuda-alquiler-joven | RD 326/2026, Plan Estatal 2026-2030 ([BOE-A-2026-8872](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-8872)), arts. 133-137 | ≤ 35 años al solicitar; rentas ≤ 5 IPREM (5,5 con discapacidad ≥ 33 % o hijo de víctima de violencia de género; 6 con ≥ 65 %); alquiler ≤ 1.000 € piso / 600 € habitación (500/250 € en municipios ≤ 10.000 hab.); 2 años + hasta 2 de prórroga; incompatible con otras ayudas al alquiler; cuantía máx. 300 € (piso) / 200 € (habitación), con el límite del 60 % de la renta; no propietario ni pariente del casero | 24-4-2026 (Diario; sin referencias posteriores) | A (falta saber si el IPREM es de 12 o 14 pagas) |
| empleada-hogar | Orden PJC/297/2026 arts. 15 y 35 | tramos de base 2026 (sección 6.2) | 2026 | A |
| | RDL 16/2022 ([BOE-A-2022-14680](https://www.boe.es/buscar/act.php?id=BOE-A-2022-14680)) DA 1.ª | reducción del 20 % en la aportación empresarial por contingencias comunes; bonificación del 80 % en desempleo y Fogasa | 9-9-2022 | A (45 % familia numerosa y que no se suma al 20 %: B, buscar la norma) |
| | LGSS [a251](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a251) | IT común: subsidio desde el día 9; el empleador paga los días 4-8; sin pago delegado | 9-9-2022 | A |
| jubilacion-parcial | LGSS [a215](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a215) | sin relevo desde la edad ordinaria (reducción del 25-75 %); con relevo hasta 3 años antes, 33 años cotizados (25 con discapacidad ≥ 33 %), 6 de antigüedad, reducción del 25-75 % (20-33 % el 1.er año si anticipa > 2 años), relevista indefinido a tiempo completo y base ≥ 65 % de la del jubilado; se cotiza por la base de jornada completa | RDL 11/2024, 1-4-2025 | A |
| | RD 1131/2002 | cuantía = pensión × % de reducción | — | B |
| brecha-genero | LGSS [a60](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a60) | requisitos (mujer; hombre solo con los supuestos a y b); tope de 4 complementos; 14 pagas; fuera del límite máximo; se suma al mínimo | 18-3-2023 | A |
| | RDL 3/2026 ([BOE-A-2026-2548](https://www.boe.es/buscar/act.php?id=BOE-A-2026-2548)) art. 2.2 | **36,90 €/mes en 2026**; convalidado (Resolución de 26-2-2026, BOE-A-2026-4668); revalorización general del 2,7 %; lo desarrolla el RD 241/2026 | 2026 | A |
| orfandad | LGSS [a224](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a224), [a225](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a225) | < 21 años o incapacitado; prestación por violencia contra la mujer al 70 % de la BR con rentas ≤ 75 % SMI, conjunto hasta el 118 %; compatible con rentas del trabajo | 7-10-2022 / 3-3-2019 | A |
| | Orden 13-2-1967 art. 17 | 20 % de la BR por huérfano; incremento por orfandad absoluta; hasta 25 años si no trabaja o ingresa < SMI | — | B (leer el texto y el art. 224.2 completo) |
| ley-beckham | LIRPF [a93](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a93) | año del cambio + 5; no residente en los 5 anteriores; motivos (contrato, teletrabajo, administrador, emprendedor…); 24 % hasta 600.000 € y 47 % el exceso; rentas del ahorro con escala propia | Ley 7/2024, 22-12-2024 | A |

Descartadas en c44: complemento a mínimos (el límite de rentas lo fija la LPGE, art. 59 LGSS), renta vitalicia (LIRPF a25.3.a.2.º 40/35/28/24/20/8 % y a38.3 hasta 240.000 €, leídos; el 38.3 ya está en venta-vivienda), plan de pensiones de empleo (ya modelado).
