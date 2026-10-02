# Equipo de agentes (mantiene el Mejorador del equipo) · v3.5 2026-10-02T13:35Z (ciclo 48; v3.4 2026-10-02T10:20Z c40; v3.3 2026-10-02T07:40Z c32; v3.2 2026-10-02T05:20Z c24; v3.1 2026-10-02T02:30Z c16; v3 2026-10-01T23:03Z c8; v2 2026-10-01 c4)

| Rol | Modelo | Frecuencia | Propiedad |
|---|---|---|---|
| Orquestador / Eficiencia | Sonnet 5.5 (sesión) | cada ciclo | ops/loop-prompt.md, ops/*.py, build.py (`main`, `write`, sitemap), costes, integración, barrido de requests |
| Constructor | Sonnet | **ciclo fiscal**: 1 fiscal + 1 no fiscal con `demanda:`; **ciclo de mantenimiento**: tarea de mejora (v3.5: peticiones del Vigilante y del Editor, `qa_static --fiscal` R1/R2) | calcs/, content/<slug>, data/backlog.md, data/params.json, calcs_loader.py, ops/verif/<slug>_oraculo.py |
| Diseñador UI/UX | **Sonnet** (Opus solo para dirección visual nueva) | 1 de cada 3 ciclos (fase F casi cerrada: quedan F8-F12) | templates/, assets/, funciones UI de build.py (→ ui.py) |
| Estratega SEO/GEO | Opus cada 4 ciclos; Sonnet en los demás pares | ciclos pares | seo.py, content/guias, static/, data/clusters.json, ops/SEO-GEO.md |
| Investigador | Opus + web (Sonnet si es competencia de 1 calculadora) | backlog < 6 no fiscales, **< 4 fiscales (Opus + web, c32)** o cada 6 ciclos | journal/ideas.md, competencia.md, líneas nuevas del backlog |
| Verificador fiscal/legal (nuevo c8) | Opus para la revisión legal; Sonnet para re-verificar | cada calculadora fiscal/legal (1 por ciclo fiscal, v3.5) + re-verificación de cambios del Vigilante (≤ 60k) | journal/verificacion-<slug>.md, ops/verif/<slug>.py (ops/roles/verificador-fiscal.md) |
| ~~Lector de norma~~ (c32; **suspendido c40**: 0 lanzamientos en 9 fiscales) | — | sustituido por la línea S de preverif + `qa_static --fiscal` | (ops/roles/lector-norma.md, archivado) |
| Editor de calidad (c32) | Sonnet ≤ 120k | **cada ciclo de mantenimiento** hasta cubrir las 67 no fiscales (36 hechas); luego 1/día | journal/editorial.md (obligatorio), peticiones (ops/roles/editor-calidad.md) |
| Vigilante de normas (nuevo c48) | Sonnet + web ≤ 60k | cada ciclo de mantenimiento mientras haya PENDIENTE BOE; si no, 1/semana + calendario | journal/vigencias.md, peticiones (ops/roles/vigilante-normas.md) |
| QA | Haiku | cada ciclo (máx. 4 páginas, **≤ 4 capturas, 0 scroll, ≤ 30 llamadas**, script JS fijo de qa.md v4) | solo lectura; métodos fijos en qa.md |
| Mejorador del equipo | Opus (Sonnet para medición rutinaria) | cada 8 ciclos o tras 2 ciclos con fallos de QA | ops/roles/*, EQUIPO.md, journal/ideas-equipo.md |

Rúbrica común de calculadoras: ops/roles/rubrica-calculadora.md **v2** (10 puntos, ≥ 16/20; nuevo punto \*10 «texto ≤ cálculo» y dato de mercado de live.json en el punto 2). Constructor se autoevalúa, QA verifica.
Roles ad hoc vistos en c4-c7 sin archivo («Verificador» c4 Sonnet 80k, «Ingeniero sync» c6 Sonnet 116k, Verificador IRPF c7 Opus 484k): todo agente lanzado debe tener rol con archivo; si no lo hay, el Orquestador usa el del dueño de los archivos que toca.

## Cuándo usar cada modelo (regla: el modelo más barato que cumpla el criterio de «hecho»)
- **Haiku**: comprobaciones mecánicas con método fijo. Ej.: QA con los parseadores de qa.md, contar páginas, verificar longitudes, ping IndexNow, resumen de metrics.py, reescribir title/description dados los límites.
- **Sonnet**: ejecutar algo ya especificado. Ej.: calculadora del backlog con el patrón existente, tarea [ ] de DESIGN.md, ilustraciones/animaciones, guía de apoyo con fuentes dadas, migraciones (EM.eur), refactor sin cambio de salida, investigación web acotada a 1 competidor.
- **Opus**: decidir con incertidumbre o verificar algo con consecuencias. Ej.: verificación independiente de una calculadora fiscal/legal (obligatoria), estrategia SEO/GEO cada 4 ciclos, nueva dirección visual, ideas de proyecto nuevo, pasada del Mejorador.
- Señal de modelo mal asignado: un Opus que tarda > 8 min haciendo lo que dice una lista ya escrita (ciclo 3: Diseñador Opus 14 min/200k ejecutando F1-F7).

## Propiedad de archivos compartidos
- build.py YA está partido (T1 hecha, c5): `ui.py` → Diseñador (asset_v, ill, ICONS, tema, card, catalog_body, notfound_body, head_extra, calc_header, calc_form); `calcs_loader.py` → Constructor (load_calcs, `default_from`); `build.py` → Orquestador (write, render_calc, main, sitemap); `seo.py` → Estratega. Nadie edita un archivo ajeno: petición.
- `ops/verif/` (c8): `<slug>_oraculo.py` → Constructor; `<slug>.py` → Verificador fiscal. ops/*.py y ops/*.sh siguen siendo del Orquestador (check_live.py y check_barometro.py: Estratega).
- Dos agentes del mismo ciclo nunca editan el mismo archivo. Si el Orquestador lanza una tarea que toca build.py, ese ciclo es el único que lo toca.

## Protocolo de peticiones cruzadas (ops/requests.md)
- Formato de línea: `- [ ] R<ciclo>.<n> [Origen -> Destino] archivo · qué hace falta · abierta c<N>`.
- Al resolver: `- [x] R… · resuelta c<M> por <rol>` (o `- [~] R… · rechazada: motivo`). No se borran; el Orquestador archiva las [x] de > 3 ciclos al final del fichero.
- Quién barre: (1) cada rol, al empezar, resuelve las abiertas `-> <su rol>`; (2) el Orquestador, en el paso 2.1, resuelve o reasigna las que tengan > 1 ciclo y anota cuántas quedan abiertas en costes.md.
- Objetivo: 0 peticiones abiertas > 1 ciclo.
### Estado tras el ciclo 3 (barrido del Mejorador, 2026-10-01)
- ABIERTA desde c1 (3 ciclos): `default_from: "params.clave"` en inputs (Constructor -> Orquestador). → entra en T1 (calcs_loader).
- PARCIAL desde c1: campo `"tema"` en cada calcs/*.json (2 de 7). → Constructor, ciclo 4 o 5, 1 min.
- ABIERTA desde c3: minificar app.css/app.js en dist (= DESIGN F8; toca build.py). → T1, después.
- Resueltas: migrar diésel a EM, card() en relacionadas, EM.eur/EM.num con miles (y migración en curso en c4), veredicto en las 6, Guías en la nav, clúster de amortizar-o-invertir, IndexNow inicial.

## Rendimiento medido (pasada 1, ciclos 1-3)
- Ciclos: 3 en 56 min (commits 21:00, 21:18, 21:37 UTC) → ~3,1 ciclos/h; duración ~19 min; camino crítico = rol Opus más lento (7 / 7,8 / 14 min). Publican 3/3 (100 %).
- Tokens por ciclo: 267k / 394k / 480k (media 380k); Opus = 50 % / 36 % / 71 %. Constructor: 1 calculadora por ~77k Sonnet (mejor valor por token).
- Consumo: semanal 16 → 18 % en 3 ciclos (~0,7 pp/ciclo, resolución 1 pp); 5 h 31 → 39 %. Extra: 0,55 EUR (sin cambio).
- QA: 3 falsos positivos en 3 ciclos (sitemap, 2× JSON-LD) → métodos fijos en qa.md.
- Datos poco fiables: las horas de «cierre» de costes.md son estimadas (22:10Z escrita antes de que ocurriera). Usar siempre `date -u +%FT%RZ`.

## Rendimiento medido (pasada 2, ciclos 4-7; medido 2026-10-01T23:03Z al inicio de c8)
Fuentes: `git log` (commit de cada ciclo, UTC: c4 21:54:56, c5 22:06:05, c6 22:20:50, c7 22:58:57) y costes.md (tokens por rol tal como los devolvió cada Agent).
| Métrica | Pasada 1 (c1-3) | c4 | c5 | c6 | c7 | Media c4-7 |
|---|---|---|---|---|---|---|
| Duración (inicio→commit, min) | ~19 | 15 | 9 | 12 | 33 | 17 |
| Intervalo entre commits de ciclo (min) | 18,5 | 17,6 | 11 | 15 | 38 | 20,5 → **2,9 ciclos/h** |
| Tokens totales (k) | 380 | 712 | 271 | ~577 (Investigador sin dato; ~141k est.) | 978 | **~635** |
| Tokens Opus (k) | 205 | 251 | 0 | ~141 | 484 (verificador IRPF) | **~219** (sin verificación fiscal: ~98) |
| Calculadoras publicadas | 1/ciclo | 1 (+migración EM.eur) | 2 | 2 | 1 fiscal | **1,5/ciclo** |
| Tokens Constructor por calculadora no fiscal (k) | ~77 | 94 | 52 | 56 | — | **~54** (c5-6) |
| Falsos positivos QA | 3 | 1 (consola) | 0 | 0 | 1 (og.png) | **0,5/ciclo** |
| Tokens QA (k) | 63 | 97 | 94 | 94 | 93 | **94** |
| Ediciones de archivo ajeno | — | ? | 0 (T1 autorizada) | build.py por 2 roles (Estratega: Pulso; sync: fecha Barómetro) | seo.py y check_live.py por el Diseñador | **2 de 4 ciclos** |
- Consumo real (solo lecturas de get_usage, sin «~»): semanal 16 % (20:41Z) → 20 % (23:01Z): +4 pp en 140 min y 7 ciclos = **~1,7 pp/h, ~0,57 pp/ciclo**, ~1,1 pp por millón de tokens mezclados (resolución 1 pp: rango 1,3-2,1 pp/h). 5 h: 31 → 51 % en 1 h 45 min (~11 pp/h); reiniciada al 3 % a las 23:01Z. Extra: 0,55 EUR, sin cambio.
- Proyección (sprint a 120 s hasta 2026-10-02 21:00Z, ~22 h): +37 pp → **~57 % semanal** (rango 49-66 %). Después, a 600 s (~2 ciclos/h con ciclos de ~17 min) ≈ 1,1 pp/h ≈ 27 pp/día → cruzaría el 70 % (ahorro) en ~12 h y el 85 % (pausa) en ~25 h, es decir, **hacia el 2026-10-03 ~22:00Z**, mucho antes de un reset semanal a 5 días. Conclusión: no hay margen para más paralelismo global; sí para reasignar (cadena fiscal más barata, ver c8.4). Cambio de cadencia aplicado en loop-prompt (c8.7).
- Ritmo: el ciclo no lo marca un rol Opus de 7-14 min como en c1-3, sino (a) la cadena fiscal Constructor → Verificador → correcciones → re-verificación (c7, 33 min, 72 % del tiempo y 49 % de los tokens) y (b) el QA secuencial (~3,6 min, 94k) más el cierre del Orquestador (3 commits por ciclo: ciclo, IndexNow, estado).
- Costes.md sigue con horas fuera de orden (c4 inicio 21:40Z antes del cierre de c3 22:10Z) y valores «~»: el registro debe salir de un script (T7).
### Peticiones abiertas > 1 ciclo (c8)
- R-C.1 [-> Estratega] clusters subrogar/guardería: **hecha en data/clusters.json, sin marcar** → Estratega la marca [x].
- R-live.3 [-> Orquestador] fecha del Barómetro: **hecha en build.py l.93-95 (c6, `BARO['fecha_datos']`), sin marcar** → Orquestador la marca [x].
- R-live.4 [-> Estratega] gas/tarifa nocturna en live: condicional → `[~] condicional`.
- R6.2 [-> Constructor] plan fiscal: no es una petición sino un plan de 5 calculadoras (1/5 hecha) → seguir en backlog.
- Diagnóstico: 0 peticiones bloqueadas de verdad; el fallo es de anotación (se resuelven sin marcar y sin nº de ciclo: «abierta c-actual»). El recuento automático va en T7.

## Rendimiento medido (pasada 3, ciclos 8-15; medido 2026-10-02T02:20Z al inicio de c16)
Fuentes: `git log` (commit «ciclo N», UTC: c8 23:23:33, c9 00:14:03, c10 00:27:55, c11 00:39:20, c12 00:58:37, c13 01:22:26, c14 01:51:40, c15 02:15:16) y costes.md (líneas de cierre de close_cycle.sh, ya con `date -u`).
| Métrica | Pasada 2 (c4-7) | c9-c15 | Comentario |
|---|---|---|---|
| Intervalo entre ciclos (min) | 20,5 | **24,5** (c9 50, c10 14, c11 11, c12 19, c13 24, c14 29, c15 24) | sin fiscal ~13 min; con fiscal 24-29 min |
| Ciclos/h | 2,9 | **2,45** (c10-15: 2,97) | 15 ciclos en 5,6 h desde 20:41Z |
| Tokens subagentes/ciclo (k) | ~635 | **726** (sin fiscal c10-11: 406; con fiscal c13-15: 836) | el Orquestador no está contado |
| Semanal | 0,57 pp/ciclo | **0,75 pp/ciclo; 1,86 pp/h** (20 % 23:01Z → 26 % 02:15Z) | ~1,0 pp por millón de tokens de subagentes |
| Calculadoras/ciclo | 1,5 | **2,1** (29 en dist; 15 nuevas en c9-15) | |
| Opus por fiscal (k) | 484 (IRPF) | **150 de media** (pensiones 108, luz 117, autónomo 140, casa 169, placas 115, rescate 295 en 2 pasadas, donativos 103) | objetivo c8.1 ≤ 150k: cumplido justo |
| Coste total por fiscal (k, Sonnet+Opus) | ~790 | placas 449, rescate 692, donativos 431 | |
| Re-verificación Sonnet (k) | 253 Opus | **86** (82-93) | objetivo ≤ 40k NO cumplido, −66 % |
| QA Haiku (k) | 94 | **102** (90-129) | objetivo ≤ 30k NO cumplido |
| Falsos positivos QA | 0,5/ciclo | **5 en 7 ciclos** (consola con pestañas viejas al llegar al tope de ~9) | regla de pestañas c15 |
| Commits por ciclo | 3 | **2** («ciclo N» + «estado ciclo N») | objetivo 1 no cumplido |
| Peticiones abiertas al cierre | 2-3 > 1 ciclo | 5, 7, 3, 7, 8, 6, 7; **6 > 1 ciclo** ahora (R6.2, R9.3, R12.2 ×2, R13.3, donativos→Estratega) | objetivo 0 no cumplido |
| AVISO de qa_static (sitio entero) | — | **64**, casi todos YMYL «sin enlace en la sección» con la fuente en otra sección | ruido: nadie los mira |
- Proyección: 26 % a las 02:18Z; a 1,86 pp/h el semanal llega al 55 % hacia las **17:50Z** (salta la salvaguarda → 600 s) y cierra el sprint a las 21:00Z en **~58 %** (rango 55-61). Con 600 s fijos después (~1,3 pp/h) cruzaría el 70 % hacia el 3-oct 06:00Z y el 85 % (pausa total) hacia el **3-oct ~18:00Z**, unos 3 días antes del reset (asumido a ~5 días, 7-oct ~02:00Z; confirmar con `resetsIn`). Con la fórmula de presupuesto (objetivo 80 %): permitido = 22 pp ÷ ~100 h = 0,22 pp/h → ~15 ciclos ligeros/día (0,35 pp) o ~7 completos/día (0,75 pp); llega al reset con ~80 % y sin pausa.
- Contexto del Orquestador: ~70 % de 1M a c15 (~45k/ciclo si creció linealmente desde c1). Lo que más entra: informes largos de subagentes (verificadores y QA hasta 15-60 líneas), la salida completa de qa_static (64 AVISO ≈ 4k tokens por ejecución) y relecturas de archivos largos (requests.md 26 KB, SEO-GEO.md 51 KB, EQUIPO.md 15 KB). Al ritmo actual autocompacta (97 %) en ~6 ciclos.
### Evaluación de los cambios de c8 y T7 (revisión programada c16)
- c8.1 Verificador con rol: **CONSOLIDADO** (Opus/fiscal 484k → 150k; 1 NO PUBLICAR evitado en rescate). c8.2 oráculo: **PARCIAL**: 0 discrepancias en 8/8, pero 4 de los errores de fondo fueron de modelo (artículos omitidos), que un oráculo del mismo autor no ve → pre-verificación por patrones (c16.1). c8.3 checklist: consolidado (sin datos de mercado inventados nuevos salvo el residual R12.1 del día 1). c8.4 re-verificación Sonnet: consolidado, objetivo ajustado (c16.2). c8.5 reglas QA: **NO CUMPLIDO** (5 FP/7) → regla de pestañas c15 (medir en c17-20). c8.6 roles con archivo: parcial («Ingeniero T7», «fixes», «textos» se lanzan como Constructor/Orquestador sin decirlo; aceptable). c8.7 cadencia: pendiente del fin del sprint; fórmula corregida (c16.4).
- T7 close_cycle.sh + qa_static: **SE MANTIENE** (no se revierte: costes.md ya fiable y ordenado, recuento de peticiones automático, 0 BLOQUEANTE falsos), pero 3 de sus 4 métricas no se movieron: commits 3 → 2 (no 1), QA 94k → 102k (no 30k), peticiones > 1 ciclo 6 (no 0). Minutos de cierre: no medibles (no hay hora de inicio de cierre); el intervalo sin fiscal bajó de ~15 a ~13 min. Causas y arreglo: T15 (ideas-equipo.md) y c16.3.
### Peticiones abiertas > 1 ciclo (c16) y dueño
- R6.2 [-> Constructor] plan fiscal de 5 calculadoras: ya son 8 verificadas → el Orquestador la marca [x].
- R9.3 [-> Constructor], R12.2 bici «2045 km» [-> Constructor]: Constructor al empezar c16 (1-2 min).
- R12.2 barometro_historico.json y R13.3 IndexNow de /hipoteca/ y /feed.xml [-> Orquestador]: close_cycle ya hace commit -A e IndexNow → marcar [x] si están en git y en el último IndexNow.
- donativos → Estratega (sin nº) y R15.1: Estratega Opus de c16 (ya planificado en ESTADO.md); la línea sin nº se marca [x] junto con R15.1.

## Rendimiento medido (pasada 4, ciclos 16-23; medido 2026-10-02T05:17Z al inicio de c24)
Fuentes: `git log` (commit «ciclo N», UTC: c15 02:15, c16 02:29, c17 02:47, c18 03:14, c19 03:39, c20 03:59, c21 04:32, c22 04:48, c23 05:11), costes.md, get_usage (05:14Z: 5 h 17 %, semanal 32 %, reset semanal **2026-10-06T15:00Z**, no el 7-oct supuesto), transcripciones de los subagentes QA (llamadas y capturas) y de la sesión del Orquestador (contexto).
| Métrica | Pasada 3 (c9-15) | c16-c23 | Objetivo c16 | Estado |
|---|---|---|---|---|
| Intervalo entre ciclos (min) | 24,5 | **22** (fiscal 18-33, media 24; no fiscal 14-16) | — | ciclos/h 2,45 → **2,73** (c1-c23: 2,69) |
| Tokens subagentes/ciclo (k) | 726 | **714** (con fiscal 783; sin fiscal 509) | — | = |
| Semanal | 0,75 pp/ciclo; 1,86 pp/h | **0,75 pp/ciclo; 2,05 pp/h** (26 % 02:15Z → 32 % 05:11Z); ~1,05 pp por millón | — | pp_por_ciclo 0,75 confirmado |
| Opus por fiscal, 1 pasada (k) | 150 | **105** (depósito 97, ofertas 109, SL 115, obligado 97) | ≤ 110 (c16.1-2) | **CUMPLIDO** |
| Opus por fiscal con 2.ª pasada (k) | 295 (rescate) | jubilación 272, paro 206 → media global **149** | — | 2 de 6 fiscales: interpretación compartida por oráculo y JS |
| Cambios obligatorios del Verificador por fiscal | ~5 | **~4** (5, 4, 3+1, 3, 3, 5) | ≤ 2 (c16.1) | NO cumplido; patrón 4 (citas) sube a 6 |
| Coste total por fiscal (k, Sonnet+Opus) | 431-692 | **~460** (346-648) | — | = |
| Re-verificación / textos Sonnet (k) | 86 | **60-61** (c18, c19; en el resto «fixes» 76-130k) | ≤ 40 (c16.2) | parcial (−30 %) |
| QA Haiku (k) | 102 | **110** (62, 108, 114, 96, 139, 69, 144, 144) | ≤ 50 (c16.3) | **NO cumplido**: ver causa abajo |
| Falsos positivos QA | 5 en 7 ciclos | **1 en 8** (c23 coma decimal) | 0 (regla c15) | casi: regla de pestañas consolidada |
| Peticiones `[ ]` abiertas > 1 ciclo | 6 | **3**: R6.2 (c6) y R12.2 (c12) YA HECHAS sin marcar (bici usa `EM.num`), R16.4 propuesta en espera | 0 | fallo de anotación, no de trabajo |
| Contexto del Orquestador por ciclo | ~45k (estimado) | **~30k** (726k a c16 → 943k a c23; medido en la transcripción). Pero c8-c15 real también fue ~27k: el 45k era una media desde c1 | ≤ 25k (c16.5) | NO se redujo; informes de subagentes ya cortos (40 informes, ~24k en total, ~600 tokens cada uno) |
| Commits por ciclo | 2 | **2** | 1 (T15) | T15 sin hacer |
- **QA: qué explica los ~140k.** Suelo fijo 38,5k (sistema + esquemas de herramientas, medido en el 1.er turno). Con 1-4 capturas: 62k (c16, 37 llamadas) y 69k (c21, 24 llamadas); con 28-41 capturas y 20-37 `scroll`: 108-144k (≈ 96-114 llamadas). Las pestañas suman ~8 llamadas: no son la causa. La causa son los encargos del Orquestador («gráfico de barras», «tabla legible», «aviso visible»), que Haiku comprueba mirando y desplazándose, pese a la regla «1 captura». Arreglo c24.1: topes duros de capturas/llamadas y un script JS fijo en qa.md que devuelve todo eso en 1 llamada. Objetivo realista ≤ 65k (≤ 50k exigiría ≤ 10 llamadas).
- **Contexto del Orquestador**: de lo que entra desde c16 (~210k), lo controlable son los prompts que el Orquestador escribe a los agentes (~36k: ~800 tokens × 44 agentes), las notificaciones de los agentes (~24k), get_usage (~6k) y su propio razonamiento. Ya no hay volcados grandes (qa_static y relecturas de archivos son < 4k). Tras la compactación el contexto vuelve a ~100-150k; lo importante ahora es el HANDOFF (T20).
- **Proyección (reset real 6-oct 15:00Z)**: a 2,05 pp/h el semanal llega al 55 % hacia las **16:30Z** (salvaguarda → 600 s: ~1,9 ciclos/h, ~1,4 pp/h) y cierra el sprint a las 21:00Z en **~61 %** (rango 58-64). Después, fórmula del loop-prompt §3.4: permitido = (80 − 61) ÷ 90 h = **0,21 pp/h** → ciclo ligero (0,35) cada ~1,7 h o completo (0,75) cada ~3,6 h; con 3 ligeros : 1 completo, ~0,45 pp de media → ~11 ciclos/día; llega al reset en ~80 % sin pausa. Cruzará el 70 % (modo ahorro, sin Opus ni fiscales) hacia el 4-oct ~16:00Z: las fiscales que queden (5 en backlog) deben ir antes. **La fórmula es correcta con los datos; no cambio parámetros**: 0,75 completo medido de nuevo (ciclo con fiscal ≈ 0,82, completo sin fiscal ≈ 0,53); 0,35 ligero sin medir aún (estimado 0,25-0,30 con QA ≤ 65k): se mantiene por prudencia y se mide en los 3 primeros ligeros.
### Evaluación de c16.1-5 (revisión programada c24)
- c16.1 pre-verificación por patrones: **PARCIAL** — los 6 patrones siguen saliendo (~4 cambios por fiscal, no ≤ 2), pero ningún error de fórmula y 1 solo NO PUBLICAR (paro). Se amplía con los patrones 7 (DT y convenciones) y 8 (opción inexistente) y la regla de citas (c24.2). No se saca ningún patrón (todos > 0 en 3 fiscales seguidas).
- c16.2 Verificador con presupuesto: **CUMPLIDO** en 1 pasada (105k); la 2.ª pasada (2 de 6) es el coste que queda → paso 0 de lectura propia (c24.3). Re-verificación 86k → ~60k, objetivo 40k no cumplido: se mantiene.
- c16.3 QA ≤ 50k: **NO CUMPLIDO** (110k) → c24.1; objetivo corregido a ≤ 65k.
- c16.4 cadencia: **CORRECTA** con datos reales (0,75 pp/ciclo de nuevo); solo cambia el reset (6-oct 15:00Z) en la proyección.
- c16.5 informes cortos: **CUMPLIDO en los informes** (~600 tokens), **NO en la métrica** (contexto ~30k/ciclo): el resto es estructural (prompts a agentes, razonamiento). No se revierte.
- T17 pestañas: **CONSOLIDADO** (1 FP en 8 ciclos, y no de consola) → cerrada. T14 (`qa_static --fiscal`): **NO HECHA** → prioridad 1 del Orquestador en el próximo ciclo sin fiscal. T15: no hecha.
### Peticiones abiertas > 1 ciclo (c24) y dueño
- R6.2 y R12.2: hechas → el Orquestador las marca [x] al empezar c24 (regla T15: ≤ 2 min, dueño ausente). R16.4: propuesta sin programar → `[~] en espera de tráfico` hasta que haya impresiones en /hipoteca/.

## Rendimiento medido (pasada 5, ciclos 24-31; medido 2026-10-02T07:30Z al inicio de c32)
Fuentes: `git log` (c24 05:28Z … c31 07:22Z), costes.md, transcripciones de 41 subagentes (pico de contexto, llamadas, capturas).
| Métrica | c16-c23 | c24-c31 | Objetivo c24 | Estado |
|---|---|---|---|---|
| Ciclos/h | 2,73 | **3,7** (13-24 min; fiscal ~18-24, ligero ~12-14) | — | sube: menos 2.ªs pasadas y QA más corto |
| Semanal | 0,75 pp/ciclo; 2,05 pp/h | **~0,3 pp/ciclo; ~1,05 pp/h** (32 % c23 → 35 % c31; lectura entera, ±0,1) | — | **pp_por_ciclo 0,75 → 0,40 completo / 0,20 ligero** |
| 5 h | — | 5 % (c20) → 37 % (c31) ≈ 9,4 pp/h | < 70 % | margen para ~1,4× (tope 2 fiscales: 5h < 50 %) |
| Fiscales publicadas | 6 en 8 ciclos | **4 en 4 ciclos** (c25-c28) + 0 en c29-c31 (backlog fiscal agotado: queda 1) | — | **cuello de botella = backlog fiscal**, no presupuesto |
| Opus por fiscal (pico, k) | 105 (1 pasada), 149 global | **95-123 (media 107), 0 segundas pasadas** | ≤ 110; 2.ª pasada 0 | **CUMPLIDO** (c24.3) |
| Cambios obligatorios por fiscal | ~4 | **4-6** (4, 5, 6, 6; 0 de fórmula); clases repetidas: transitorias, patrón 8, no modelado, cita RDL 26/2026 | ≤ 2 | **NO cumplido** → c32.2 |
| Coste por calculadora fiscal (pico, k) | ~460 | **~410** (Constructor 172-260 + Opus 95-123 + reverif 61-79) ≈ 0,2 pp | — | = |
| Coste por calculadora no fiscal (k) | ~55 | **~55** (lote de 2 en 98-127k; c31: 120k) ≈ 0,05 pp | ≤ 80 | = |
| QA Haiku (pico, k) | 110 | **50-65** (30-43 llamadas, 0-2 capturas) | ≤ 65; ≤ 4 capturas | **CUMPLIDO** (c24.1); llamadas 30-43 > 30 |
| Fallos/falsos positivos QA | 1 en 8 | **1** (Haiku probó rutas sin /decidir/) | 0 | regla de rutas en qa.md |
| Estratega Sonnet ligero / Investigador Sonnet (k) | 73-125 / 77-89 | **53-62 / 53-59** | — | baratos |
| Peticiones abiertas > 1 ciclo | 3 | **0** (c29-c31) | 0 | **CUMPLIDO** |
- **Coste por rol en un ciclo completo con 1 fiscal (~0,40 pp)**: Constructor fiscal ~45 %, Opus ~25 %, reverif ~15 %, no fiscal + QA ~15 %. Ligero (~0,20 pp): Constructor 2 no fiscales ~110k + QA ~60k + Estratega ligero ~60k.
- **Proyección (reset 6-oct 15:00Z)**: a 35 % (07:22Z) y ~1,1-1,5 pp/h con las mejoras de c32, el sprint cierra a las 21:00Z en **~50-55 %** (si toca 55 % antes, 600 s). Después: (80 − 53) ÷ 90 h ≈ **0,30 pp/h** → ciclo completo (0,40) cada ~1,3 h ≈ 18/día, o mezcla con fiscal doble (0,55) cada ~1,8 h. Cruce del 70 % (fin de Opus/fiscales) hacia el **5-oct ~09:00Z** (antes: 4-oct 16:00Z). Con la fórmula vieja (0,75) el loop habría dejado ~25 pp sin usar en el reset.
### Evaluación de c24.1-4 (revisión programada c32)
- c24.1 QA v4: **CUMPLIDO** (110k → 50-65k, capturas 28-41 → 0-2). Se mantiene; tope de 30 llamadas se supera a menudo sin coste visible: no se endurece.
- c24.2 patrones 7-8 + preverif por archivo: **PARCIAL** — 0 segundas pasadas, pero los cambios siguen en 4-6 y caen en 4 clases fijas → c32.2 (4 líneas obligatorias T/8/N/R) y lector de norma.
- c24.3 paso 0 del Verificador: **CUMPLIDO** (0 de 4 con 2.ª pasada; en maternidad el paso 0 detectó la diferencia de interpretación en la 1.ª pasada). Se mantiene.
- c24.4 T19 experimento: **NO EJECUTADO** (no se lanzó en ninguna fiscal) → pasa a rol fijo con decisión tras 4 fiscales (c32.3), porque ya no hay restricción de presupuesto.
- T14 (`qa_static --fiscal`), T15 (1 commit/ciclo): siguen sin hacer (2 commits por ciclo: «ciclo N» + «estado ciclo N»). T16 → rol Editor (c32.4). T20 HANDOFF: aplicado.

## Rendimiento medido (pasada 6, ciclos 32-39; medido 2026-10-02T10:15Z al inicio de c40)
Fuentes: `git log` (c32 07:35Z … c39 10:04Z), costes.md, 51 transcripciones de subagentes (pico de contexto y llamadas), journal/verificacion-*.md (línea VEREDICTO).
| Métrica | c24-c31 | c32-c39 | Objetivo c32 | Estado |
|---|---|---|---|---|
| Ciclos/h | 3,7 | **3,2** (12-31 min; doble fiscal ~23-30) | — | baja por la fiscal doble |
| Semanal | ~0,3 pp/ciclo | **0,62 pp/ciclo; ~2,0 pp/h** (35 % c31 → 40 % c39) | — | estimado por tipo: **doble 0,80 · 1 fiscal 0,50 · ligero 0,25** (4×0,8+2×0,5+2×0,3 ≈ 4,8 vs 5 medido) |
| 5 h | ≤ 37 % | **≤ 48 %** | < 60 % (c32.1) | ok |
| Fiscales publicadas | 4 en 7 ciclos | **9 en 8 ciclos (~2,5 h)**, 0 NO PUBLICABLE, 1 aparcada por falta de norma (tarifa plana: regla bien aplicada) | ≥ 8/día | **CUMPLIDO** (c32.1); ciclo doble ≈ 0,8 pp = justo en el tope de reversión |
| Cambios obligatorios por fiscal | 4-6 | **3-7, media 4,9** (paro 3, viudedad 3, cuota 4, compensar 5, jubilación activa 5, indemnización 5, traspasar 6, permiso 6, retención 7). Por clase (44): **otros 22** (absolutos 6, citas/ámbito 5, patrón 2 «artículo que mueve la base» 4), N 8, 8 7, T 4, R 3 | ≤ 3 | **NO cumplido** (c32.2) → c40.2/c40.3 |
| Errores críticos (cambian cifra o veredicto) | — | **4 en 9**: art. 49.1.b (traspasar), arts. 152/311 LGSS (jubilación activa), art. 7.e párr. 2 / 52.c (indemnización), orden de compensación (compensar). Todos «supuesto de norma no leído», 0 aritméticos | 0 | el oráculo no los ve (reproduce la lectura) |
| 2.ª pasada Opus | 0 de 4 | **2 de 9** (jubilación activa, indemnización: cambios de interpretación) | 0 | aceptable: solo en cambios grandes |
| Coste por fiscal (pico, k) | ~410 | **~400**: Constructor 104-252 (media 195) + Opus 85-119 (media 102) + reverif 68-85 (+ fixes) ≈ 0,30-0,40 pp | — | = |
| Coste por no fiscal (k) | ~55 | **~55-75** (1-2 por agente en 103-153k) ≈ 0,06 pp | ≤ 80 | = |
| QA Haiku | 50-65k | **58-66k**, 25-38 llamadas, 0-2 capturas; 0 fallos reales; 1 ruta mal probada | ≤ 65k | ok |
| Lector de norma (c32.3) | — | **0 lanzamientos en 9 fiscales** (el Verificador lo anota: «no hay journal/lector-<slug>.md») | ≥ 2 de 4 | **NO EJECUTADO** → suspendido (c40.3) |
| Editor de calidad (c32.4) | — | 2 pasadas (74k, 55k) **sobre guías/home, 0 calculadoras**, sin journal/editorial.md ni línea base, 0 peticiones | línea base + ≥ 90 % | **NO CUMPLIDO en la forma** → c40.1 |
| Investigador fiscal Opus (c32.5) | — | 2 pasadas (79k, 136k); backlog fiscal repuesto 2 veces (c32, c38: 8) | ≥ 4 siempre | CUMPLIDO |
| Tráfico | 0 | **0 impresiones, 0 páginas conocidas por Google (día 2)**; indexación manual de Andoni | — | 88 calculadoras sin señal: más páginas no es la palanca ahora |
- **Coste por rol, ciclo doble (~0,8 pp)**: 2 Constructores fiscales ~50 %, 2 Opus ~25 %, reverif ~10 %, Estratega ligero + QA + no fiscal ~15 %. El 75 % del gasto va a fiscales; las 24 no fiscales del periodo costaron ~0,06 pp cada una y no tienen tráfico que las justifique todavía.
- **Proyección al reset (2026-10-06T15:00Z)** con 2,0 pp/h: 55 % hacia las **17:30Z** (regla de sprint → 600 s); con 600 s (~2,1 ciclos/h ≈ 1,3 pp/h) el sprint cierra a las 21:00Z en **~59-60 %**. Después: (78 − 60) ÷ 90 h ≈ **0,20 pp/h** → ciclo doble cada ~4 h, 1 fiscal cada ~2,5 h, ligero cada ~1,25 h. Cruce del 70 % (fin de Opus) hacia el **4-oct ~23:00Z**; luego ahorro a 0,25 pp/ciclo hasta 75-78 % en el reset. Con los pp viejos (0,40/0,55) la fórmula habría dormido la mitad de lo necesario y cruzado el 85 % (pausa total) hacia el 5-oct.
### Evaluación de c32.1-7 (revisión programada c40)
- c32.1 fiscal doble: **CUMPLIDO** (9 en 8 ciclos, 0 NO PUBLICABLE, 5h ≤ 48 %). Se mantiene; ciclo doble ≈ 0,8 pp (tope de reversión): no se sube a 3 (+0,4 pp/ciclo, mismo cuello: lectura de norma).
- c32.2 líneas T/8/N/R: **PARCIAL** — T y R casi resueltos (4 y 3 en 9), N y 8 siguen (8 y 7), y el grueso está en «otros» → c40.2 (línea S) y c40.3 (control automático).
- c32.3 Lector de norma: **NO EJECUTADO** por 2.ª vez (era T19) → se suspende: un rol que el Orquestador no lanza en 9 ocasiones no es una mejora; su función pasa al Constructor (línea S) y a qa_static --fiscal.
- c32.4 Editor: **mal ejecutado** (guías en vez de calculadoras, sin editorial.md) → c40.1.
- c32.5 Investigador fiscal: **CUMPLIDO**. c32.6 rutas de QA: 1 fallo más (el encargo pasó slug sin ruta) → regla para el Orquestador en c40.5. c32.7 cadencia: pp subestimados (0,40/0,55 vs 0,50/0,80 reales) → c40.4.

## Rendimiento medido (pasada 7, ciclos 40-47; medido 2026-10-02T13:30Z al inicio de c48)
Fuentes: `git log` (c39 10:04Z … c47 13:23Z), costes.md, línea VEREDICTO de las 8 verificaciones c40-c47.
| Métrica | c32-c39 | c40-c47 | Objetivo c40 | Estado |
|---|---|---|---|---|
| Ciclos/h | 3,2 | **2,4** (8 en 3 h 19 min; 16-31 min) | — | baja: Editor + fiscal en casi todos |
| Semanal | 0,62 pp/ciclo | **1,0 pp/ciclo; 2,4 pp/h** (40 % → 48 %); sin c40 (Mejorador + Estratega Opus + doble = 2 pp): **0,86** | 0,50 con 1 fiscal | **NO**: el ciclo «1 fiscal» real cuesta **~0,85** (Constructor fiscal + Opus + reverif + Editor + no fiscal + Estratega + QA), no 0,50 |
| 5 h | ≤ 48 % | **≤ 59 %** | < 60 % | al límite |
| Calculadoras publicadas | 9 fiscales + ~11 no fiscales | **8 fiscales + 5 no fiscales** (100 en total); 0 NO PUBLICABLE; tarifa plana aparcada (regla bien aplicada) | no fiscales ≤ 8/día | CUMPLIDO |
| Cambios del Opus por fiscal | 4,9 | **5,1** (3-9: finiquito 9, incapacidad 6, subsidio 6, baja 5, aceptar 5, retribución 4, empleada 3, kilometraje 3). Por clase (41): otros 15, N 10, S 9, 8 6, R 1, T 0 | ≤ 3 (línea S) | **NO** |
| Críticos | 4 de 9 | **5 de 8** (N 3: arts. 275.5.e, 81.2, complemento por mínimos; S 2: RGC 23.1.A en finiquito, compatibilidad en aceptar-trabajo); 1 error de fórmula (borde) | ≤ 1 de 4 | **NO**, pero 0 publicados: el Opus los caza todos |
| T y R | 4 / 3 en 9 | **0 / 1 en 8** | — | resueltos: la línea S/T/R funciona donde es mecánica |
| Editor (c40.1) | 0 calculadoras | **3 pasadas válidas, 36 no fiscales**, journal/editorial.md con línea base; FAQ > 50 p 117 → 0, leads sin condición 6 → 0; **0 peticiones** (5 pendientes solo anotados) | ≥ 90 % el 5-oct | en curso (36/67 = 54 %) |
| `qa_static --fiscal` (c40.3) | — | **hecho c41**; 33 fiscales, 80 avisos, 0 bloqueantes: R1 14 (1 clave), R2 6, R3 23, R6 28 | 0 avisos por fiscal nueva | las 8 nuevas sin R2; R1/R2 viejos sin dueño → R48.2 |
| Peso | — | **48 páginas > 60 KB cargados, 26 > 70, 2 > 80** (hub ahorro 82); en **gzip la peor ~22 KB** | — | deuda cosmética (R48.3), no de velocidad |
| Tráfico | 0 | **0 impresiones, 0 URL conocidas (día 2)** | — | sin señal: no hay base para elegir por datos |
- **Coste por rol, ciclo fiscal (~0,85 pp)**: cadena fiscal (Constructor ~200k + Opus ~100k + reverif ~75k) ≈ 55 %; Editor ~60-75k, no fiscal ~60k, Estratega ligero ~60k, QA ~60k ≈ 45 %. Ciclo sin fiscal (c44: Estratega Opus + Investigador Opus) ≈ 0,5-1; ligero/mantenimiento estimado **~0,30**.
- **Proyección al reset (2026-10-06T15:00Z)** desde 48 % a las 13:23Z. *Sin cambios* (120 s, ~2,4 ciclos/h × 0,86): 55 % hacia las 16:20Z → 600 s → sprint cierra en **~61 %**; luego (78 − 61) ÷ 90 h = 0,19 pp/h ≈ 1 ciclo fiscal cada 4,5 h; 70 % hacia el 5-oct ~00:00Z. *Con c48* (600 s ya + alternancia fiscal 0,85 / mantenimiento 0,30, ~1 par/h): sprint cierra en **~56-57 %**; luego 0,23 pp/h ≈ 1 par cada ~4,9 h (≈ 5 fiscales/día); 70 % hacia el **5-oct ~05:00Z**, ahorro a 0,30 hasta **76-78 %** en el reset; 0 h de pausa.
### Evaluación de c40.1-6 (revisión programada c48)
- c40.1 mix: **CUMPLIDO** en no fiscales (5 en 8 ciclos, todas con `demanda:`) y Editor (36 calculadoras con línea base). Fallo de forma: los pendientes del Editor no se convierten en peticiones → editor-calidad.md (c48.4) y R48.1.
- c40.2 línea S: **NO cumple** (5,1 cambios, 5/8 críticos). T y R bajan a ~0; S y N siguen porque son lectura de cada letra del artículo, que el Constructor no hace bien. No se reactiva el Lector (0 de 9 lanzamientos) ni se añade un 2.º Opus: el Opus caza el 100 % y el coste del crítico es una reverif (~75k ≈ 0,05 pp). Se refuerza N por letra (c48.3) y se cambia la métrica a «0 críticos publicados» + críticos N ≤ 1 de 4.
- c40.3 `qa_static --fiscal`: **CUMPLIDO**. c40.4 pp: **subestimados otra vez** (0,50 → 0,85 real) → c48.1. c40.5 rutas QA: 0 fallos. c40.6 dato propio: /tablas-2026/trabajo-prestaciones (c42) = 2 de 3; brief proyecto 2: post-sprint (sin cambios).

## Registro de cambios
- 2026-10-01: equipo v1 creado (6 roles + Estratega SEO/GEO + Mejorador del equipo). Cadencia 20 min, tope 400 EUR extra y 100 EUR/día.
- 2026-10-01 (v2, Mejorador pasada 1). Cada cambio, con la métrica que debe moverse:
  1. Diseñador a Sonnet por defecto; máx. 2 tareas/8 min → tokens Opus del Diseñador ≈ 0; camino crítico ≤ 8 min.
  2. Constructor en lote de 2 calculadoras → calculadoras/ciclo 1 → 2 sin alargar el ciclo.
  3. Estratega Opus solo cada 4 ciclos → Opus del Estratega 70k → 35k por ciclo de media.
  4. Investigador cada 6 ciclos o backlog < 6 → 47k → ~23k por ciclo de media.
  5. Mejorador cada 8 ciclos → 37k → ~19k por ciclo de media.
  6. QA con parseadores fijos y navegador solo en páginas cambiadas → falsos positivos 1/ciclo → 0; tokens QA ≤ 40k.
  7. Rúbrica de calculadora → reintentos de QA por calculadora → 0.
  8. Protocolo de peticiones con estado y barrido → peticiones abiertas > 1 ciclo: 3 → 0.
  9. Propiedad de build.py por funciones (provisional hasta T1) → ediciones de build.py por > 1 rol en un ciclo → 0.
  Revisión: en la pasada 2 (ciclo ~12) comparar cada métrica; revertir lo que no mejore.
- 2026-10-01: ops/loop-prompt.md, solo parámetros de cadencia: Investigador 3 → 6 ciclos (o backlog < 6), Mejorador 4 → 8 ciclos. Motivo: backlog de 12 pendientes y pocas novedades cada 4 ciclos de 20 min. Métrica: tokens Opus por ciclo ~205k → ~77k (con los cambios 1, 3, 4 y 5). Resto de alineación pendiente del Orquestador (journal/ideas-equipo.md T2).
- 2026-10-01T23:03Z (v3, Mejorador pasada 2, ciclo 8). Evaluación de v2 con los datos de c4-c7 y cambios:
  - v2.1 Diseñador Sonnet → **CONSOLIDADO**: 0 tokens Opus del Diseñador en c4-c7 (antes 134-200k). Camino crítico ≤ 8 min: incumplido en c4 (9,5 min, 5 entregas); cumplido en c5 y c7. Se refuerza el tope de 2 tareas (disenador.md). Métrica: tokens Diseñador ≤ 100k/ciclo.
  - v2.2 Constructor en lote de 2 → **CONSOLIDADO**: 1,5 calculadoras/ciclo (2 en c5 y c6), ~54k por calculadora no fiscal (objetivo ≤ 80k). El backlog solo tiene 2 no fiscales tras c8: Investigador en c9 (regla backlog < 6 no fiscales).
  - v2.3 Estratega Opus cada 4 → **CONSOLIDADO**: Opus medio c4-7 = 38k/ciclo (objetivo ≤ 40k).
  - v2.4 Investigador cada 6 → **CONSOLIDADO con excepción**: se lanzó en c6 por la necesidad fiscal (bien: sus tablas resultaron 100 % correctas según el verificador).
  - v2.5 Mejorador cada 8 → consolidado (98k en c4, c8 ahora).
  - v2.6 QA con parseadores → **PARCIAL**: falsos positivos 1 → 0,5/ciclo (los de JSON-LD/sitemap desaparecieron; quedan consola y URL absoluta, con regla nueva en qa.md); tokens 63k → 94k, objetivo ≤ 40k **NO cumplido** → no se revierte (los parseadores sí sirven), se sustituye la parte estática por un script (T7). Métrica: tokens QA ≤ 40k cuando exista qa_static.py.
  - v2.7 Rúbrica → **SE AMPLÍA a v2**: 0 reintentos de QA por calculadora en c5-c7, pero no cazó los 2 textos falsos ni el caso no legal del IRPF (los cazó el verificador Opus). Nuevo punto \*10 «texto ≤ cálculo», dato de mercado de live.json en el punto 2, combinaciones no legales en el 6. Métrica: errores hallados después del Constructor → 0.
  - v2.8 Protocolo de peticiones → **NO CUMPLIDO en la forma**: 2-3 abiertas > 1 ciclo, todas ya hechas o condicionales; se mantiene y se automatiza el recuento (T7).
  - v2.9 Propiedad de build.py → **MEJORADO pero no 0**: T1 hecha; build.py por 2 roles en c6, seo.py por el Diseñador en c7. Regla en disenador.md; T11 para mover el marcado del Pulso a ui.py.
  - c8.1 Rol nuevo Verificador fiscal/legal (ops/roles/verificador-fiscal.md; era T6). Métrica: Opus por calculadora fiscal 484k → ≤ 150k con los mismos hallazgos.
  - c8.2 Constructor escribe primero un oráculo Python + barrido ≥ 500 casos contra el JS real (constructor.md). Métrica: errores de fórmula que llegan al verificador → 0.
  - c8.3 Checklist de calidad en constructor.md y estratega-seo-geo.md (datos de mercado de live.json; texto ≤ cálculo). Métrica: datos de mercado escritos de memoria → 0.
  - c8.4 Re-verificación fiscal con Sonnet re-ejecutando scripts (no un segundo Opus). Métrica: tokens de re-verificación 253k → ≤ 40k.
  - c8.5 QA: reglas para los 2 falsos positivos de c4/c7 y lista exacta de páginas cambiadas (qa.md). Métrica: falsos positivos 0,5 → 0/ciclo.
  - c8.6 Todo agente lanzado tiene archivo de rol (fin de roles ad hoc). Métrica: agentes sin rol por ciclo → 0.
  - c8.7 loop-prompt, solo cadencia: tras el sprint de 24 h, cadencia por presupuesto en vez de 600 s fijos; y salvaguarda «semanal ≥ 55 % antes de acabar el sprint → 600 s». Motivo: a 600 s la proyección cruza el 85 % hacia el 3-oct ~22:00Z. Métrica: semanal ≤ 80 % en el reset sin pausa total.
  Próxima revisión: ciclo 16 (o tras la 2.ª calculadora fiscal con el protocolo nuevo, lo que llegue antes).
- 2026-10-02 (c9, Orquestador): T3, T7 y T9 HECHAS. `ops/qa_static.py` (QA estática determinista: sitemap, JSON-LD, title/description/canonical/h1, enlaces, peso 60/75 KB, og:image, llms/robots/barómetro, datos vivos con fecha, YMYL: frases con Ley/art./BOE/%/€ sin enlace a fuente y números del texto que no salen de params/live/tests; `--changed` lista las páginas para el QA con navegador) y `ops/close_cycle.sh` (build+check+qa_static, recuento de peticiones, costes.md con `date -u`, UN commit, pull --rebase, push, espera 200, IndexNow, resumen de 5 líneas; `--dry-run`). ops/roles/qa.md v3: el QA Haiku solo hace navegador, cifras en pantalla y revisión visual/móvil. loop-prompt §3 sustituye los pasos manuales por `bash ops/close_cycle.sh`.
  Métricas objetivo: tokens QA 94k → ≤ 30k/ciclo; commits por ciclo 3 → 1; peticiones abiertas > 1 ciclo → 0 (recuento automático, ahora exige `abierta c<N>` en cada línea `- [ ]`); falsos positivos de QA estático 0 por construcción; horas de costes.md siempre `date -u`. Rol «Editor YMYL»: solo si qa_static da > 3 AVISO YMYL reales por ciclo. Revisión: ciclo 16.

- 2026-10-02 (c15, Orquestador): regla de pestañas del navegador en roles/qa.md y para todos los roles que prueban en navegador: abrir una pestaña, cerrarla al terminar; el Orquestador limpia pestañas al empezar cada ciclo. Métrica: falsos positivos de consola por ciclo → 0.
- 2026-10-02T02:30Z (v3.1, Mejorador pasada 3, ciclo 16). Cambios aplicados, cada uno con su métrica (revisión: ciclo 24 o al terminar el sprint, lo que llegue antes):
  - c16.1 constructor.md: «Pre-verificación fiscal» con los 6 patrones que el Opus cazó en 8/8 fiscales (absolutos, artículos que mueven la base, ámbito territorial, redacción vigente, bordes, conceptos regulados omitidos) + grep de absolutos. Métrica: cambios obligatorios del Verificador por fiscal ~5 → ≤ 2; Opus/fiscal 150k → ≤ 110k.
  - c16.2 verificador-fiscal.md: empieza por la tabla del Constructor, presupuesto ≤ 110k/10 min, informe de 3 líneas; re-verificación Sonnet sin navegar ni releer la norma. Métrica: re-verificación 86k → ≤ 40k.
  - c16.3 qa.md: máx. 4 páginas, 1 captura por página nueva, el resto con javascript_tool/consola; oscuro y 1280 solo si cambian templates/assets; informe ≤ 5 líneas. Métrica: QA 102k → ≤ 50k/ciclo (objetivo de v3 de 30k inalcanzable con navegador).
  - c16.4 loop-prompt, solo cadencia: pp_por_ciclo 0,57 → 0,75 (completo) / 0,35 (ligero); tras el sprint ciclo ligero por defecto y 1 de cada 4 completo; modo ahorro también por presupuesto (1200 s fijos acababan en pausa total en ~17 h); esperas > 3600 s en tramos con despertar mínimo. Métrica: semanal ≤ 80 % en el reset, 0 horas en pausa total.
  - c16.5 Informe final ≤ 5 líneas en constructor, diseñador, estratega, investigador (≤ 3 el verificador); detalle a archivos. Métrica: crecimiento del contexto del Orquestador ~45k → ≤ 25k por ciclo (medir el % de contexto en ESTADO.md cada ciclo).
  - No se revierte nada: T7 se mantiene (ver evaluación); lo que falla de T7 va a T15 (Orquestador).
- 2026-10-02T05:20Z (v3.2, Mejorador pasada 4, ciclo 24). Cambios aplicados, cada uno con su métrica (revisión: ciclo 32 o tras los 3 primeros ciclos ligeros del post-sprint):
  - c24.1 qa.md v4: máx. 4 capturas, 0 `scroll`, máx. 30 llamadas, una pestaña para todo el QA, script JS fijo (desborde, resultado, gráficos, PDF, miles sin punto, NaN, aviso buscado) y regla del falso positivo «coma decimal». El Orquestador encarga al QA solo URL + input a cambiar + texto de aviso a buscar (sin «mira que se vea…»). Métrica: QA 110k → ≤ 65k/ciclo; capturas por QA 28-41 → ≤ 4.
  - c24.2 constructor.md: patrones 7 (DT/DF y convenciones de cómputo) y 8 (¿la opción existe para este usuario?), regla de citas en el 4 (pegar 1 línea del artículo), pre-verificación en journal/preverif-<slug>.md (no en verificacion-pendiente.md, 50 KB), bloque `INTERPRETACION` en la cabecera del oráculo. Métrica: cambios obligatorios por fiscal ~4 → ≤ 2; citas erróneas por fiscal ~1 → 0.
  - c24.3 verificador-fiscal.md: paso 0 «lectura propia antes del oráculo», muestreo de 3 citas, 2.ª pasada Opus ≤ 60k y solo de lo cambiado. Métrica: fiscales con 2.ª pasada Opus 2/6 → 0; Opus por fiscal (media global) 149k → ≤ 110k.
  - c24.4 Decisión sobre un «segundo constructor» Sonnet que reescriba el oráculo desde la norma sin ver el JS: **no como rol fijo**; experimento T19 en las 2 próximas fiscales (≤ 50k Sonnet, solo la lectura de la norma, sin código). Coste/beneficio: +~0,05 pp por fiscal frente a un ahorro esperado de ~0,05 pp (1/3 de las fiscales evitaría ~130k Opus) más el riesgo de publicar con una lectura errónea; solo compensa si caza ≥ 1 de 2. Analista de datos: no (0 impresiones). Editor de calidad: sigue como pasada única T16 (no hecha; tras el sprint, en un ciclo ligero).
  - No se cambia ningún parámetro del loop-prompt (pp_por_ciclo 0,75/0,35 confirmados; ver proyección). No se revierte nada.
- 2026-10-02T07:40Z (v3.3, Mejorador pasada 5, ciclo 32). Con presupuesto sobrante (semanal 35 % a 4,3 días del reset), el gasto se pasa a calidad y tráfico. Cada cambio con su métrica (revisión: ciclo 40 o tras 4 fiscales con el protocolo nuevo):
  - c32.1 **Hasta 2 fiscales por ciclo** en paralelo (loop-prompt §1, constructor.md, verificador-fiscal.md) si 5h < 50 %, semanal < 60 % y hay 2 con fuentes; con doble fiscal, el no fiscal baja a 1. Métrica: fiscales verificadas publicadas por día (c25-c31: 4 en 7 ciclos) → ≥ 8/día; 0 NO PUBLICABLE; ciclo doble ≤ 0,6 pp y ≤ 30 min.
  - c32.2 constructor.md: 4 líneas obligatorias en preverif (T transitorias desde el consolidado, 8 opción imposible con test, N no modelado con efecto, R normas del año / RDL 26/2026 solo si toca); el Verificador cuenta por clase en su VEREDICTO. Métrica: cambios obligatorios por fiscal 4-6 → ≤ 3.
  - c32.3 Rol **Lector de norma** (ops/roles/lector-norma.md, Sonnet ≤ 50k, era T19): lee la ley sin ver el código, en paralelo. Métrica: el Opus confirma una diferencia suya en ≥ 2 de 4 fiscales → se queda; si no, se quita. (No un 2.º Opus: el Opus ya da 0 errores de fórmula y 0 segundas pasadas; lo que falta es lectura previa barata.)
  - c32.4 Rol **Editor de calidad e intención de búsqueda** (ops/roles/editor-calidad.md + «Estilo» en la rúbrica, era T16): lead con respuesta+cifra (fragmentos y resúmenes de IA), title = consulta real, FAQ como consultas, coherencia en 71 calculadoras. Métrica: % de calculadoras con los 5 puntos ok (línea base en la 1.ª pasada) → ≥ 90 % en 3 días; cuando haya impresiones, CTR revisadas vs no revisadas.
  - c32.5 investigador.md: disparador **< 4 fiscales pendientes → Opus con web, foco fiscal estacional** (31-dic y Renta 2027). Métrica: backlog fiscal con fuentes ≥ 4 siempre (hoy 1).
  - c32.6 qa.md: regla de rutas (`/decidir/<slug>/`, curl antes de reportar 404). Métrica: fallos de QA por ruta → 0.
  - c32.7 loop-prompt, solo cadencia: pp_por_ciclo 0,75/0,35 → **0,40 completo / 0,55 fiscal doble / 0,20 ligero** (medido c24-c31); tras el sprint, completo por defecto y ligero solo si permitido < 0,25 pp/h; ahorro con 0,20. Métrica: semanal 75-80 % en el reset (con la fórmula vieja ~55 %), 0 horas de pausa.
  - Rechazados con motivo: Constructor no fiscal en lote de 3 (97 páginas en 31 ciclos: riesgo de «contenido escalado», principio 2; mejor calidad que cantidad); Estratega Opus más frecuente (0 impresiones: sin datos, otra pasada Opus repite hipótesis; se sube a cada 2 ciclos cuando haya ≥ 5 páginas con impresiones); 2.º Verificador Opus (ver c32.3). No se revierte nada.
- 2026-10-02T10:20Z (v3.4, Mejorador pasada 6, ciclo 40). 88 calculadoras y 0 páginas conocidas por Google: el gasto pasa de **cantidad a profundidad** (calidad de lo publicado, control automático de cifras, datos propios). Cada cambio con su métrica (revisión: ciclo 48 o al terminar el sprint + 4 ciclos):
  - c40.1 **Mix**: Constructor no fiscal 2 → **1 por ciclo (0 con fiscal doble)** y solo de líneas del backlog con intención de búsqueda marcada por el Estratega; el hueco lo ocupa una **tarea de mejora** (Constructor Sonnet ≤ 100k: aplica las peticiones del Editor y añade tests de contenido). Editor de calidad **cada ciclo sin fiscal doble**, solo calculadoras, journal/editorial.md obligatorio (si falta, la pasada no cuenta). Métricas: % de calculadoras con los 5 puntos ok (línea base en la 1.ª pasada válida) → ≥ 90 % el 5-oct; peticiones del Editor resueltas en ≤ 2 ciclos; calculadoras nuevas no fiscales/día ~20 → ≤ 8.
  - c40.2 constructor.md: línea **S · Supuestos de norma** en preverif (cada exención, tope, importe del año, fecha de entrada en vigor/DT y regla de compatibilidad que usa el cálculo: artículo + ≤ 1 línea literal + URL BOE con fecha; lo que no tenga literal se declara en la página o se aparca, como tarifa plana) y grep de «artículos que remiten» (patrón 2). Métrica: cambios obligatorios por fiscal 4,9 → ≤ 3; críticos 4/9 → ≤ 1/4.
  - c40.3 Lector de norma **suspendido** (archivo conservado; reactivable si los críticos no bajan en 4 fiscales). T14 rehecho como **`qa_static.py --fiscal`** (especificación en ideas-equipo T14 v3; dueño Orquestador, en el próximo ciclo sin fiscal doble). Métrica: avisos del control por fiscal antes del Opus → 0; cambios «otros» del Opus 22/9 → ≤ 1 por fiscal.
  - c40.4 loop-prompt, solo cadencia: pp_por_ciclo **0,80 doble / 0,50 una fiscal / 0,25 ligero** (medido c32-c39) y objetivo de la fórmula 80 → **78** (margen de lectura entera ±1). Métrica: semanal 75-80 % en el reset, 0 horas de pausa total, 0 cruces del 85 %.
  - c40.5 loop-prompt §2: el Orquestador pasa al QA las URL completas que imprime `qa_static --changed`, nunca slugs sueltos. Métrica: fallos de QA por ruta → 0.
  - c40.6 Profundidad y frescura con el presupuesto libre del sprint: Estratega Opus (cada 4) dedica su pasada a **1 página de dato propio** (T24; ya hay /tablas-2026/) y el ligero a frescura (actualidad/barómetro con fecha) en vez de clusters cuando no haya calculadora nueva. Proyecto 2: solo un **brief** (Investigador Opus ~140k, 1 vez, post-sprint), sin construir hasta el disparador de 100 impresiones. Métrica: páginas de dato propio 1 → 3 el 6-oct; enlaces/citas externos a 30 días.
  - Rechazados: 3 fiscales por ciclo (+0,4 pp/ciclo sin quitar el cuello de botella de lectura); quitar la 2.ª pasada Opus (2 de 9, en cambios de interpretación: es donde está el riesgo); arrancar el proyecto 2 ya (0 señal del 1; repartiría la indexación manual de Andoni).
- T14 v3 **IMPLEMENTADO** (2/10/2026): `python3 ops/qa_static.py --fiscal [--changed] [--full]` (reglas R1-R8 por calculadora fiscal; BLOQUEANTE solo si falta toda clave de params; integrado en close_cycle.sh como paso informativo).
- 2026-10-02T13:35Z (v3.5, Mejorador pasada 7, ciclo 48). 100 calculadoras, 0 impresiones y una derogación en curso: el gasto pasa de **profundidad a vigencia y mantenimiento**. Cada cambio con su métrica (revisión: ciclo 56 o el 4-oct 12:00Z, lo que llegue antes):
  - c48.1 loop-prompt, solo cadencia: **600 s ya** (no 120 s hasta 21:00Z); **fiscal doble suspendida** hasta el reset; pp_por_ciclo **0,85 fiscal / 0,30 mantenimiento** (medido c41-c47). Métrica: semanal 75-80 % en el reset, 0 h de pausa, 0 cruces del 85 %; ≥ 4 fiscales/día post-sprint.
  - c48.2 **Alternancia fiscal / mantenimiento** (loop-prompt §1). Ciclo de mantenimiento = Vigilante + Constructor «tarea de mejora» + Editor + QA, sin Opus salvo re-verificación ≤ 60k. Métrica: peticiones `-> Constructor` cerradas en ≤ 2 ciclos; `qa_static --fiscal` R1+R2 20 → 0 el 4-oct.
  - c48.3 constructor.md, línea N por **cada apartado y letra** del artículo que define el derecho. Métrica: críticos N 3 de 8 → ≤ 1 de 4; métrica de cambios totales sustituida por «0 críticos publicados».
  - c48.4 Rol nuevo **Vigilante de normas** (ops/roles/vigilante-normas.md, Sonnet + web ≤ 60k; journal/vigencias.md). Primer encargo: Resolución del RDL 26/2026 en el BOE (17 calculadoras lo citan) e inventario de las ~30 normas BOE citadas; calendario de vigencias de enero de 2027 (SMI, IPREM, pensiones, cotización/MEI, autónomos). Coste ~0,05 pp por pasada. Métrica: 0 días con norma cambiada en vigor y página sin nota ni petición. Editor: pendientes → peticiones (R48.1 abre los 5 actuales).
  - c48.5 Retorno marginal (decisión): 1.º vigencia (cifras legales que caducan o se derogan en páginas YMYL ya publicadas), 2.º deuda de calidad barata (R1/R2, fuentes del Editor), 3.º fiscales con fecha (31-dic, Renta 2027) a 1 por ciclo fiscal, 4.º no fiscales solo con `demanda:` (1 por ciclo fiscal), 5.º brief del proyecto 2 (1 vez, post-sprint, sin construir), 6.º métricas: metrics.py cada 6 ciclos sin cambios (Search Console da 0 hasta que Google rastree; no hay nada que medir más a menudo).
  - Rechazados: reactivar el Lector de norma (0 de 9 lanzamientos; el Opus caza el 100 %); arrancar el proyecto 2 (0 señal del 1); seguir a 120 s (las 90 h post-sprint se quedarían con 1 fiscal cada 4,5 h); bajar el umbral de peso (la página real pesa ~22 KB gzip: R48.3).
