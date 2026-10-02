# Equipo de agentes (mantiene el Mejorador del equipo) · v3 2026-10-01T23:03Z (ciclo 8; v2 2026-10-01 c4)

| Rol | Modelo | Frecuencia | Propiedad |
|---|---|---|---|
| Orquestador / Eficiencia | Sonnet 5.5 (sesión) | cada ciclo | ops/loop-prompt.md, ops/*.py, build.py (`main`, `write`, sitemap), costes, integración, barrido de requests |
| Constructor | Sonnet | cada ciclo, **lote de 2** calculadoras (o 1 fiscal) | calcs/, content/<slug>, data/backlog.md, data/params.json, calcs_loader.py, ops/verif/<slug>_oraculo.py |
| Diseñador UI/UX | **Sonnet** (Opus solo para dirección visual nueva) | 1 de cada 3 ciclos (fase F casi cerrada: quedan F8-F12) | templates/, assets/, funciones UI de build.py (→ ui.py) |
| Estratega SEO/GEO | Opus cada 4 ciclos; Sonnet en los demás pares | ciclos pares | seo.py, content/guias, static/, data/clusters.json, ops/SEO-GEO.md |
| Investigador | Opus + web (Sonnet si es competencia de 1 calculadora) | backlog < 6 o cada 6 ciclos | journal/ideas.md, competencia.md, líneas nuevas del backlog |
| Verificador fiscal/legal (nuevo c8) | Opus para la revisión legal; Sonnet para re-verificar | cada calculadora fiscal/legal | journal/verificacion-<slug>.md, ops/verif/<slug>.py (ops/roles/verificador-fiscal.md) |
| QA | Haiku | cada ciclo | solo lectura; métodos fijos en qa.md |
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
