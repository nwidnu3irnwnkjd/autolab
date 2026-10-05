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
| incapacidad-permanente | LGSS [a194](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a194), [a196](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a196), [a197](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a197), [a198](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a198) | grados; total por enfermedad común: la pensión no puede ser inferior al mínimo de menores de 60 años con cónyuge no a cargo (art. 196.2 párr. 3, RDL 28/2018, vigente desde 2019); complemento de gran incapacidad = 45 % de la base mínima + 30 % de la última base, mínimo 45 % de la pensión; BR común = bases de 96 meses / 112 (24 últimas a valor nominal) × % del art. 210.1 contando como cotizados los años hasta la edad ordinaria (50 % si < 15 años); total compatible con un trabajo de funciones distintas | Ley 2/2025, 1-5-2025 | A |
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

---

## Pilar alquiler c57 (Estratega/Investigador Opus, 2026-10-02 tarde) — LAU vigente tras derogar los RDL 26/2026 y 27/2026

**Leído hoy** en el consolidado de la LAU ([BOE-A-1994-26003](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003), «última actualización publicada el 02/10/2026, en vigor a partir del 02/10/2026»), que ya marca como «Se deja sin efecto» todo lo que añadieron el RDL 26/2026 (derogado: [BOE-A-2026-20526](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20526)) y el RDL 27/2026 (prórroga de contratos; también derogado: [BOE-A-2026-20527](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20527)). Arts. 9 bis, 21 bis, DA 12.ª y DT 8.ª quedan «(Sin efecto)». Ley 12/2023 ([BOE-A-2023-12203](https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203)): su consolidado sigue en «30/09/2026» y **aún muestra la DT 4.ª en la redacción del RDL 26/2026** (retraso de consolidación); la redacción que vuelve a regir es la original del [diario](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-12203) (leída): «continuarán rigiéndose por lo establecido en el régimen jurídico que les era de aplicación». IRAV: Resolución INE de 18-12-2024 ([BOE-A-2024-26685](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-26685), leída) y [INEbase IRAV](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177110&idp=1254735976607&menu=ultiDatos).

### Qué rige HOY para actualizar la renta de vivienda (regla para la calculadora `actualizacion-renta-alquiler-irav-ipc`)
1. **Sin cláusula de actualización en el contrato → no se actualiza** (LAU art. 18.1 párr. 1). A
2. **Cláusula que pacta actualizar sin decir índice → IGC** (Índice de Garantía de Competitividad) de la última cifra publicada (art. 18.1 párr. 2). A
3. **Tope en todo caso: la variación del IPC** del último índice publicado en la fecha de actualización (art. 18.1 párr. 3). A
4. **Contratos firmados desde el 26-5-2023: tope = IRAV** del último mes publicado (DA 11.ª LAU, añadida por la Ley 12/2023: el índice INE «se fijará como límite de referencia a los efectos del artículo 18»; Resolución INE con efectos desde el 1-1-2025; el INE dice que los contratos posteriores al 26-5-2023 «se revisarán en base al IRAV»). Como el IRAV es por definición el mínimo entre IPC, IPC subyacente y una tasa media ajustada (β = 2, α = 0,5), **si pactan IPC, la subida queda limitada al IRAV**. **B** (el art. 18 sigue diciendo «IPC»; la aplicación del IRAV se apoya en la DA 11.ª, la DT 4.ª original y el criterio del INE; no hay sentencia que lo cierre: presentarlo como «límite según la DA 11.ª y el INE»).
5. **Contratos anteriores al 26-5-2023**: se rigen por su cláusula y por la redacción del art. 18 vigente cuando se firmaron (DT 4.ª original Ley 12/2023). Para los firmados desde el 6-3-2019 (RDL 7/2019) es la regla 1-3 (tope IPC). Los topes extraordinarios del art. 46 del RDL 6/2022 (IGC/2 % hasta 31-12-2023; 3 % en 2024, redacción de la DF 6.ª Ley 12/2023, leída) **se agotaron el 31-12-2024**. B (anteriores a 2019: no modelar, aviso «consulta tu contrato»).
6. **Tope del 2 % del RDL 26/2026: NO rige.** Solo estuvo en vigor 1-2 oct 2026; la derogación no es retroactiva. Una actualización notificada en esos dos días es un caso marginal: aviso «consulta a un profesional». C
7. **Cuándo se cobra**: desde el mes siguiente a la notificación por escrito con el porcentaje aplicado (vale una nota en el recibo anterior); el inquilino puede pedir el certificado del INE (art. 18.2). A. No hay «preaviso de un mes» legal (error frecuente en competidores).
- **Dato vivo**: IRAV **agosto 2026 = 2,47 %**, publicado el 15-9-2026 (INEbase). El de septiembre sale con el IPC de septiembre (mediados de octubre; fecha exacta **por confirmar** en el calendario INE). Para `data/live.json`: serie IRAV mensual del INE (dos decimales).

### Tabla norma · artículo · regla · enlace · vigencia · confianza
| Tema | Norma · art. | Regla (resumen fiel) | Enlace | Vigencia | Conf. |
|---|---|---|---|---|---|
| Régimen y excepción | LAU 4.2 | Vivienda: pactos dentro del Título II; supletorio Código Civil. **Excepción**: > 300 m² o renta inicial anual > 5,5 × SMI anual (vivienda entera): manda la voluntad de las partes y solo en su defecto el Título II | [a4](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a4) | redacción RDL 7/2019 (la del RDL 26/2026 sin efecto) | A |
| Nulidad | LAU 6 | Nulas y «no puestas» las estipulaciones que modifiquen en perjuicio del arrendatario/subarrendatario las normas del Título II, salvo que la norma lo autorice | [a6](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a6) | original | A |
| Cesión y subarriendo | LAU 8 | Cesión solo con consentimiento escrito; subarriendo solo parcial y con consentimiento escrito; precio del subarriendo ≤ renta | [a8](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a8) | original | A |
| Duración mínima | LAU 9.1-2 | Libre; si < 5 años (7 si arrendador persona jurídica), prórroga obligatoria anual hasta 5/7 salvo que el inquilino avise 30 días antes. Sin plazo: 1 año. Cómputo desde contrato o puesta a disposición | [a9](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a9) | RDL 7/2019 | A |
| Recuperar por necesidad | LAU 9.3 | Solo arrendador persona física, pasado el 1.er año, si consta **expresamente en el contrato**; aviso ≥ 2 meses; si no la ocupa en 3 meses: reposición hasta 5 años o 1 mensualidad por año que faltara | [a9](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a9) | RDL 7/2019 | A |
| Prórroga tácita | LAU 10.1 | Pasados 5/7 años sin aviso (arrendador 4 meses, inquilino 2 meses): prórroga anual hasta 3 años más; el inquilino puede salir avisando 1 mes antes de cada anualidad | [a10](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a10) | Ley 12/2023 (RDL 26 y 27/2026 sin efecto) | A |
| Prórroga extraordinaria | LAU 10.2-3 | Vulnerabilidad acreditada + gran tenedor: hasta 1 año. Zona tensionada declarada: hasta 3 años a petición del inquilino (excepciones: nuevo contrato, acuerdo, necesidad 9.3) | [a10](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a10) | Ley 12/2023 | A |
| Desistimiento | LAU 11 | Inquilino puede desistir pasados ≥ 6 meses avisando ≥ 30 días; puede pactarse indemnización de 1 mensualidad por año que reste (proporcional) | [a11](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a11) | Ley 4/2013 | A |
| Subrogación por muerte | LAU 16 | Cónyuge, pareja ≥ 2 años (o hijos comunes), descendientes, ascendientes, hermanos, discapacidad ≥ 65 %; notificar en 3 meses; renuncia pactable solo en contratos > 5/7 años y nunca con vulnerables | [a16](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a16) | RDL 7/2019 | A |
| Pago de la renta | LAU 17.2-4 | Mensual, primeros 7 días salvo pacto; **nunca más de 1 mensualidad por adelantado**; pago electrónico (metálico solo excepcional); recibo con conceptos separados | [a17](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a17) | Ley 12/2023 | A |
| Renta en zona tensionada | LAU 17.6-7 | Nuevo contrato ≤ última renta (5 años) actualizada; +10 % solo por rehabilitación, eficiencia −30 %, accesibilidad o contrato ≥ 10 años. Gran tenedor (o vivienda sin alquiler en 5 años si la resolución lo dice): índice de precios de referencia | [a17](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a17) | Ley 12/2023 (17.7: DT 7.ª, cuando el sistema de índices esté aprobado) | A (zonas: por CCAA, B) |
| Actualización | LAU 18 + DA 11.ª | Ver bloque «Qué rige HOY» | [a18](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a18) · [da-11](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#da) | RDL 7/2019 + Ley 12/2023 | A/B |
| IRAV | Res. INE 18-12-2024 | min(IPC, IPC subyacente, TVAMA); TVAMA = min(2 + 0,5·(IPC − 2), 2 + 0,5·(IPCsub − 2)); mensual, 2 decimales; efectos 1-1-2025 | [BOE-A-2024-26685](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2024-26685) | desde 1-1-2025 | A |
| Mejoras del arrendador | LAU 19 | Pasados 5/7 años: subida = capital invertido × (interés legal + 3 puntos), máx. 20 % de la renta; o antes, por acuerdo, sin reiniciar plazos | [a19](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a19) | RDL 7/2019 | A |
| Gastos generales (comunidad, IBI…) | LAU 20.1-2 | Pueden pactarse a cargo del inquilino **por escrito y con importe anual a la fecha del contrato**; subida máx. anual el doble de la de la renta durante 5/7 años (salvo tributos) | [a20](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a20) | Ley 12/2023 | A |
| Gestión inmobiliaria | LAU 20.1 último párr. | «Los gastos de gestión inmobiliaria y los de formalización del contrato serán a cargo del arrendador» (sin distinguir persona física/jurídica) | [a20](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a20) | Ley 12/2023 (desde 26-5-2023) | A |
| Suministros con contador | LAU 20.3 | Siempre del inquilino | [a20](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a20) | — | A |
| Conservación | LAU 21 | Reparaciones para habitabilidad: arrendador, sin subir renta (salvo daño imputable al inquilino); obra > 20 días: rebaja proporcional; urgentes: el inquilino puede hacerlas y reclamarlas; pequeñas reparaciones por desgaste: inquilino | [a21](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a21) | original (21 bis sin efecto) | A |
| Obras del inquilino | LAU 23 | Las que cambien la configuración: consentimiento escrito; nunca las que reduzcan la seguridad | [a23](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a23) | Ley 4/2013 | A |
| Tanteo y retracto | LAU 25 | Tanteo 30 días naturales desde notificación fehaciente; retracto 30 días; **renuncia pactable** (25.8): entonces aviso de venta con 30 días | [a25](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a25) | Ley 4/2013 | A |
| Fianza | LAU 36.1-4 | Obligatoria, en metálico: **1 mensualidad** (vivienda), 2 (otros usos); sin actualizar los 5/7 primeros años; en cada prórroga puede ajustarse a 1 mensualidad de la renta vigente; devolución: interés legal pasado 1 mes desde la entrega de llaves | [a36](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a36) | RDL 7/2019 (36.5 y 36.7 del RDL 26/2026 sin efecto) | A |
| Garantía adicional | LAU 36.5 | Cualquier tipo pactable; en vivienda con contrato ≤ 5/7 años, **máx. 2 mensualidades** | [a36](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#a36) | RDL 7/2019 | A |
| Depósito de fianza | LAU DA 3.ª | Las CCAA pueden obligar a depositarla en su organismo (sin interés) | [da-3](https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003#datercera) | — | A (cada CCAA: NO VERIFICADO) |
| Gran tenedor | Ley 12/2023 art. 3.k | > 10 inmuebles urbanos residenciales o > 1.500 m² residenciales (sin garajes ni trasteros); en zona tensionada puede bajarse a ≥ 5 si la CCAA lo motiva | [a3](https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203#a3) | original (el consolidado aún marca la modificación del RDL 26/2026; el texto original y el mostrado coinciden en sustancia) | B |
| Zonas tensionadas | Ley 12/2023 art. 18 | Las declara la administración competente en vivienda (CCAA), con resolución ministerial | [a18](https://www.boe.es/buscar/act.php?id=BOE-A-2023-12203#a18) | original | A (listado de zonas: NO VERIFICADO) |
| Contratos previos | Ley 12/2023 DT 4.ª (original) | Los anteriores al 26-5-2023 siguen con su régimen; adaptación voluntaria si no es contraria a la ley | [diario](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2023-12203) | original (la del RDL 26/2026 decae) | B (consolidación pendiente) |

**Avisos de página obligatorios**: (a) no es asesoramiento; (b) Cataluña, País Vasco, Navarra, Aragón, Baleares y Galicia tienen derecho civil propio y varias CCAA regulan depósito de fianza, zonas tensionadas e índices: no se modelan; (c) contratos > 300 m² o renta > 5,5 × SMI: art. 4.2; (d) temporada/turístico: fuera (art. 3 y 5.e).
**Calculadoras que salen de aquí** (backlog c57): `actualizacion-renta-alquiler-irav-ipc` (F; reglas 1-7; dato vivo IRAV), `fianza-y-garantias-adicionales-alquiler` (F; art. 36 + 17.2 + DA 3.ª como aviso), `gastos-alquiler-quien-paga` (F; art. 20 + 21.4 + 17.6 en zona tensionada).

## Candidatas c58
- 2026-10-02 (Vigilante, pasada 4): plusvalía municipal (TRLRHL 107) e IBI (TRLRHL 72) siguen DESCARTADAS: el consolidado BOE-A-2004-4214 aún no recoge la reversión por la Resolución BOE-A-2026-20526 (estado «Desactualizado», sin nota «se deja sin efecto»). Reconsultar https://www.boe.es/buscar/act.php?id=BOE-A-2004-4214 en 2-3 días; si aparece la nota, pasan a verificables.

---

## Candidatas c58 (Investigador, 2026-10-02 noche) — 6 laborales/fiscales: pagas extra, pilar alquiler (casero), 2027 ya en el BOE
Método: API de consolidados del BOE leída hoy (`/texto/bloque/<id>`, todas las versiones). ET = BOE-A-2015-11430 · LGSS = BOE-A-2015-11724 · LIRPF = BOE-A-2006-20764 · RIRPF = BOE-A-2007-6820 · TRLRHL = BOE-A-2004-4214. Enlace: `https://www.boe.es/buscar/act.php?id=<ID>#<bloque>`.

**RDL 26/2026 DEROGADO** — Resolución de 2-10-2026 del Congreso ([BOE-A-2026-20526](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20526), BOE núm. 245, leída): «acordó derogar el Real Decreto-ley 26/2026». Su análisis «DEJA SIN EFECTO»: los cambios en LIRPF («determinados preceptos», sección 8.ª del título X, DA 65.ª y 66.ª), RIRPF (arts. 41 bis, 69, 75, 76, 93, 94, DA 8.ª), **TRLRHL art. 72 y, con efectos 1-12-2026, art. 107.4**, LIVA arts. 20 y 91, LAU, Ley 12/2023 (art. 3 y DT 4.ª). **Para el Vigilante (plusvalía/IBI)**: a 2-oct la API consolidada del TRLRHL **aún muestra como última versión la del RDL 26/2026** en a72 (vigencia 1-10-2026) y a107 (vigencia 1-10-2026); la redacción que vuelve a regir es la versión anterior de cada bloque (a107: BOE-A-2026-2024, vigencia 28-1-2026; a72: Ley 12/2023, vigencia 26-5-2023). Lo mismo en LIRPF: a23, a24, a85 y DT 38.ª (`dt-6`) siguen con la versión RDL 26/2026 como última → **usar la penúltima**. Re-mirar cuando el BOE actualice el consolidado.

### c58-1 `pagas-extra-prorrateadas-o-14-pagas` — «Pagas prorrateadas o 14 pagas»
| Norma · bloque | Texto literal clave | Versión | Conf. |
|---|---|---|---|
| ET [a31](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11430#a31) | «dos gratificaciones extraordinarias al año, una de ellas con ocasión de las fiestas de Navidad […] podrá acordarse en convenio colectivo que las gratificaciones extraordinarias se prorrateen en las doce mensualidades» | 13-11-2015 (sin cambios) | A |
| LGSS [a147](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a147).1 | «Las percepciones de vencimiento superior al mensual se prorratearán a lo largo de los doce meses del año» | 1-1-2023 | A |
| LGSS [a270](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a270).1 | BR del paro = «promedio de la base por la que se haya cotizado por dicha contingencia durante los últimos ciento ochenta días» (excluidas horas extra) | 1-1-2023 | A |
| RIRPF [a83](https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a83).2 regla 1.ª | «la suma de las retribuciones […] que […] vaya normalmente a percibir el contribuyente en el año natural» | 8-2-2024 | A |
| RIRPF [a86](https://www.boe.es/buscar/act.php?id=BOE-A-2007-6820#a86).1 | tipo = cuota de retención / cuantía total del 83.2, «con dos decimales»; mínimo 2 % en contratos < 1 año (86.2) | 26-1-2023 | A |
Reglas para el Constructor: (1) la decisión no es individual: el prorrateo lo permite el convenio (aviso). (2) Bases de cotización, paro e IT (BR = base del mes anterior, que ya incluye la prorrata) **no cambian**. (3) Retención anual idéntica; si la empresa recalcula (RIRPF a87) puede variar el reparto mensual. (4) Finiquito: con prorrateo no queda paga pendiente; sin prorrateo se debe la parte devengada (enlaza `finiquito-baja-voluntaria-vacaciones-preaviso`). Intención: «me conviene cobrar las pagas prorrateadas», «pagas prorrateadas paro». Riesgo YMYL: medio (no hay error grave posible: el neto anual es el mismo). Transitorias: ninguna.

### c58-2 `paga-extra-navidad-cuanto-cobro-neto` — «Paga de Navidad: entera o proporcional»
Mismas normas que c58-1 (ET a31, LGSS a147.1, RIRPF a80.1 «aplicar a la cuantía total de las retribuciones […] el tipo de retención que corresponda», a86.1). Reglas: paga bruta = importe del convenio × días devengados / días del periodo (anual o 1-jul a 31-dic, editable); cotización en diciembre: 0 adicional (ya prorrateada mes a mes); neto = bruta × (1 − tipo de la nómina). Avisos: devengo, cuantía y si la IT/excedencia descuentan los fija el convenio (no se modela; editable). Intención: «cuánto cobro de paga extra de Navidad», «paga extra si entré en septiembre». Pico 15-nov/22-dic; publicar antes del 10-nov. YMYL bajo-medio. Conf. A (ley), convenios NO VERIFICADO (inputs del usuario).

### c58-3 `vivienda-vacia-o-alquilarla-irpf` — «Piso vacío o alquilado»
| Norma · bloque | Texto literal clave | Versión a usar | Conf. |
|---|---|---|---|
| LIRPF [a85](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a85).1 | «tendrá la consideración de renta imputada la cantidad que resulte de aplicar el 2 por ciento al valor catastral, determinándose proporcionalmente al número de días […] revisados […] en el período impositivo o en el plazo de los diez períodos impositivos anteriores, el porcentaje será el 1,1 por ciento»; excluidos vivienda habitual, suelo no edificado, inmuebles en construcción | Ley 26/2014, vigencia 1-1-2015 (la del RDL 26/2026, con efectos 2027, **sin efecto**) | A |
| LIRPF [a23](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a23).1 | gastos deducibles: intereses + reparación y conservación con límite de los ingresos (exceso 4 años); tributos; amortización «3 por ciento sobre el mayor de […] el coste de adquisición satisfecho o el valor catastral, sin incluir el valor del suelo» | Ley 12/2023 (1-1-2024) | A |
| LIRPF a23.2 | 90/70/60/50 % (ver c58-4) | Ley 12/2023 | A |
| LIRPF [a24](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a24) | «cónyuge o un pariente, incluidos los afines, hasta el tercer grado inclusive […] el rendimiento neto total no podrá ser inferior al que resulte de las reglas del artículo 85» | original 2006 (la del RDL 26/2026 sin efecto) | A |
Intención: «tributa un piso vacío», «imputación de rentas inmobiliarias», «alquilar a un familiar Hacienda». Pico Renta 2027 (abr-jun) y dic (decisión de alquilar en enero). YMYL medio. Transitorias: DT 38.ª para contratos previos (c58-4). Recargo del IBI a viviendas vacías (TRLRHL a72.4): fuera, Vigilante.

### c58-4 `renovar-contrato-alquiler-o-firmar-nuevo-reduccion-irpf` — «Prorrogar el contrato o firmar uno nuevo» (casero)
| Norma · bloque | Texto literal clave | Versión a usar | Conf. |
|---|---|---|---|
| LIRPF [a23](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a23).2 (penúltima versión) | a) «90 por ciento cuando se hubiera formalizado por el mismo arrendador un nuevo contrato […] en una zona de mercado residencial tensionado, en el que la renta inicial se hubiera rebajado en más de un 5 por ciento»; b) 70 % si «hubiera alquilado por primera vez la vivienda» en zona tensionada y arrendatario de 18-35 años (o Administración/ESFL/programa público); c) 60 % rehabilitación (RIRPF a41.1) terminada en los 2 años previos; d) «50 por ciento, en cualquier otro caso». Requisitos al celebrar el contrato; solo sobre rendimientos declarados antes de comprobación | Ley 12/2023, vigencia 1-1-2024 | A |
| LIRPF [DT 38.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#dt-6) (penúltima versión) | «contratos de arrendamiento de vivienda que se hubieran celebrado con anterioridad a la entrada en vigor de la Ley 12/2023 […] la reducción prevista en el apartado 2 del artículo 23 de esta ley en su redacción vigente a 31 de diciembre de 2021» | Ley 12/2023 | A |
| LIRPF a23.2 a 31-12-2021 | «se reducirá en un 60 por ciento» | Ley 11/2021 (11-7-2021) | A |
**NO USAR**: la última versión del consolidado (RDL 26/2026: 100/95/90/85/70 % y 50/40/30/25/20/15 % según la renta, apartado 2 de la DT 38.ª y 80 % en prórroga tácita): derogada el 2-10-2026. Regla: prórroga (obligatoria art. 9 o tácita art. 10 LAU) de un contrato anterior al 26-5-2023 = mismo contrato → 60 % (confianza **B**: interpretación, buscar consulta DGT V-xxxx antes de construir). Contrato nuevo (aunque sea con el mismo inquilino) → 50 % salvo los supuestos a-c; la zona tensionada solo cuenta si está declarada (listado NO VERIFICADO: input del usuario). Intención: «reducción 60 alquiler contrato nuevo», «renovar contrato alquiler pierdo reducción». YMYL medio-alto (error = cuota mal declarada). Pico Renta 2027 y vencimientos de contratos firmados en 2021-2022 (5 años → 2026-2027).

### c58-5 `jubilarse-en-2026-o-en-2027-edad-y-pension` — «Jubilarme en 2026 o en 2027» (2027 ya en el BOE)
| Norma · bloque | Texto literal clave | Versión | Conf. |
|---|---|---|---|
| LGSS [DT 7.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dtseptima) | «2026 38 años y 3 meses o más. 65 años. Menos de 38 años y 3 meses. 66 años y 10 meses. A partir del año 2027 38 años y 6 meses o más. 65 años. Menos de 38 años y 6 meses. 67 años.» | 2-1-2016 | A |
| LGSS [DT 40.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dt-11) | «Desde 1 de enero de 2026 […] dividir entre 352,33 la suma de las 302 bases de cotización de mayor importe comprendidas dentro del período de los 304 meses […]. Desde 1 de enero de 2027 […] entre 354,67 la suma de las 304 bases […] de los 308 meses»; desde 2037, a209.1 íntegro (324 de 348 / 378) | RDL 2/2023, 1-4-2023 | A |
| LGSS [DT 4.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dtcuaa).7 | «cuando el hecho causante se produzca con posterioridad al 31 de diciembre de 2025 y antes de 31 de diciembre de 2040, la entidad gestora aplicará en su integridad lo previsto en el artículo 209.1 en su redacción vigente el día 1 de enero de 2023 cuando dicho cálculo resulte más favorable» (300 meses / 350, 24 últimos nominales) | 25-12-2024 | A |
| LGSS [a209](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a209).1.b | lagunas: 48 primeras con base mínima, resto al 50 %; [DT 41.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dt-12): mujeres (y hombres con a60.1.b) meses 49-60 al 100 % y 61-84 al 80 % | 1-1-2026 | A |
| LGSS a210 | % por años cotizados (ya en `jubilacion-anticipada-o-demorada`) | — | A (reutilizar params) |
Inputs ≤ 8 (backlog). Simplificación permitida: base media constante por tramos (aviso «estimación; la oficial, en Tu Seguridad Social»). Pensión máxima/mínima 2027: NO VERIFICADO (LPGE/RDL de revalorización). Intención: «edad de jubilación 2027», «me jubilo en 2026 o 2027». YMYL alto. Publicar antes de dic-2026.

### c58-6 `nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad` — «Nómina de 2026 o de 2027» (2027 ya en el BOE)
| Norma · bloque | Texto literal clave | Versión | Conf. |
|---|---|---|---|
| LGSS [DT 43.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dt-14) (MEI, a127 bis) | «En el año 2026, será de 0,90 puntos porcentuales, de los que el 0,75 corresponderá a la empresa y el 0,15 al trabajador. En el año 2027, será de 1 punto porcentual, del que el 0,83 corresponderá a la empresa y el 0,17 al trabajador»; 2028 1,10 (0,92 + 0,18); desde 2029 1,2 (1,00 + 0,2) | RDL 2/2023, 1-4-2023 | A |
| LGSS [a19 bis](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#a1-4) | solidaridad sobre la retribución del a147 que supere la base máxima; tramos hasta +10 %, +10-50 %, > 50 %; reparto «misma proporción que […] contingencias comunes» | 1-1-2025 | A |
| LGSS [DT 42.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dt-13) | «2026 1,15 1,25 1,46 2027 1,38 1,5 1,75» (… 2045 5,50 6,00 7,00) | 1-4-2023 | A |
| LGSS [DT 38.ª](https://www.boe.es/buscar/act.php?id=BOE-A-2015-11724#dt-9) | 2024-2050 la LPGE fija el tope máximo «conforme a lo establecido en el artículo 19.3 […] se le sumará una cuantía fija anual de 1,2 puntos porcentuales» | 1-4-2023 | A (cifra 2027 NO VERIFICADO: no hay PGE ni orden 2027 → input editable) |
Resto de tipos del trabajador (4,70 CC, 1,55/1,60 desempleo, 0,10 FP): los de 2026 (sección 5.3), con aviso «2027 sin orden de cotización». Intención: «cuánto me quitan de la nómina en 2027», «MEI 2027». Pico dic-ene. YMYL medio (diferencias de céntimos a decenas de €; útil para sueldos > base máxima).

Descartadas en c58: plusvalía e IBI (Vigilante; ver arriba), deducción autonómica del inquilino (no hay fuente estatal: la estatal solo para contratos anteriores a 2015, DT 15.ª; ojo: su consolidado también muestra versión RDL 26/2026 → penúltima), régimen «vivienda tensionada» del RDL 26/2026 (derogado), Verifactu 2027 (no es «X o Y» calculable con cifras; posible guía).

## Candidatas c65
- 2026-10-05 (Vigilante, pasada 7): los consolidados ya reflejan la reversión (API `/texto`, última versión de cada bloque = BOE-A-2026-20526, fecha_vigencia 2026-10-02, con la nota «Se deja sin efecto la modificación … por Resolución de 2 de octubre de 2026 que publica el Acuerdo del Congreso de los Diputados por el que se deroga el Real Decreto-ley 26/2026»). Las dos candidatas descartadas en c58 pasan a VERIFICABLES. Enlace base: `https://www.boe.es/buscar/act.php?id=BOE-A-2004-4214#<bloque>`. Aviso de lectura: en LIRPF a24/a85 la versión de fecha_vigencia más alta (2027-01-01) es la del RDL 26/2026 y no rige; tomar la última versión del bloque.
- **c65-1 plusvalía municipal** (IIVTNU) · TRLRHL [a107](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4214#a107).4 · literal: «sin que pueda exceder de los límites siguientes: Periodo de generación Coeficiente Inferior a 1 año. 0,15 1 año. 0,15 2 años. 0,14 3 años. 0,14 4 años. 0,16 5 años. 0,18 6 años. 0,19 7 años. 0,20 8 años. 0,19 9 años. 0,15 10 años. 0,12 11 años. 0,10 12 años. 0,09 13 años. 0,09 14 años. 0,09 15 años. 0,09 16 años. 0,10 17 años. 0,13 18 años. 0,17 19 años. 0,23 Igual o superior a 20 años. 0,40» · nota del consolidado: «Se deja sin efecto la modificación de los importes máximos de los coeficientes señalados en el apartado 4, por Resolución de 2 de octubre de 2026 … Ref. BOE-A-2026-20526» · versión a usar: la de 2026-10-02 (coeficientes máximos previos al RDL 26/2026: 0,15 / 0,15 / 0,14 …; los del RDL, 0,17 / 0,16 / 0,16 …, decaen) · confianza A para máximos legales; el coeficiente real lo fija cada ordenanza (NO VERIFICADO por municipio: input del usuario) · YMYL medio · riesgo: el art. 107.4 prevé actualización anual por norma con rango legal (vigilar PGE/RDL de fin de año).
- **c65-2 IBI** · TRLRHL [a72](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4214#a72) · literal 72.1: «El tipo de gravamen mínimo y supletorio será el 0,4 por ciento cuando se trate de bienes inmuebles urbanos y el 0,3 por ciento cuando se trate de bienes inmuebles rústicos, y el máximo será el 1,10 por ciento para los urbanos y 0,90 por ciento para los rústicos»; 72.4: «los ayuntamientos podrán exigir un recargo de hasta el 50 por ciento de la cuota líquida del impuesto» para inmuebles residenciales desocupados más de dos años y titulares de cuatro o más inmuebles, «hasta el 100 por ciento» si el periodo supera tres años · nota: «Se deja sin efecto la modificación del título y del apartado 4, así como la adición de los apartados 4 bis y 4 ter por Resolución de 2 de octubre de 2026 … Ref. BOE-A-2026-20526» (desaparecen el recargo a alojamientos de uso turístico y el régimen de zona tensionada) · confianza A; tipos reales por ordenanza municipal (NO VERIFICADO) · YMYL medio.
- Sin cambio de estado: RDL 25/2026 (hidrocarburos/TUR) sigue vigente y pendiente de convalidación (ver journal/vigencias.md, Pasada 7).
