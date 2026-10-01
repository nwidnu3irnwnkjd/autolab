# Equipo de agentes (mantiene el Mejorador del equipo) · v2 2026-10-01

| Rol | Modelo | Frecuencia | Propiedad |
|---|---|---|---|
| Orquestador / Eficiencia | Sonnet 5.5 (sesión) | cada ciclo | ops/loop-prompt.md, ops/*.py, build.py (`main`, `write`, sitemap), costes, integración, barrido de requests |
| Constructor | Sonnet | cada ciclo, **lote de 2** calculadoras | calcs/, content/<slug>, data/backlog.md, data/params.json, `load_calcs` (→ calcs_loader.py) |
| Diseñador UI/UX | **Sonnet** (Opus solo para dirección visual nueva) | 1 de cada 3 ciclos (fase F casi cerrada: quedan F8-F12) | templates/, assets/, funciones UI de build.py (→ ui.py) |
| Estratega SEO/GEO | Opus cada 4 ciclos; Sonnet en los demás pares | ciclos pares | seo.py, content/guias, static/, data/clusters.json, ops/SEO-GEO.md |
| Investigador | Opus + web (Sonnet si es competencia de 1 calculadora) | backlog < 6 o cada 6 ciclos | journal/ideas.md, competencia.md, líneas nuevas del backlog |
| QA | Haiku | cada ciclo | solo lectura; métodos fijos en qa.md |
| Mejorador del equipo | Opus (Sonnet para medición rutinaria) | cada 8 ciclos o tras 2 ciclos con fallos de QA | ops/roles/*, EQUIPO.md, journal/ideas-equipo.md |

Rúbrica común de calculadoras: ops/roles/rubrica-calculadora.md (Constructor se autoevalúa, QA verifica).

## Cuándo usar cada modelo (regla: el modelo más barato que cumpla el criterio de «hecho»)
- **Haiku**: comprobaciones mecánicas con método fijo. Ej.: QA con los parseadores de qa.md, contar páginas, verificar longitudes, ping IndexNow, resumen de metrics.py, reescribir title/description dados los límites.
- **Sonnet**: ejecutar algo ya especificado. Ej.: calculadora del backlog con el patrón existente, tarea [ ] de DESIGN.md, ilustraciones/animaciones, guía de apoyo con fuentes dadas, migraciones (EM.eur), refactor sin cambio de salida, investigación web acotada a 1 competidor.
- **Opus**: decidir con incertidumbre o verificar algo con consecuencias. Ej.: verificación independiente de una calculadora fiscal/legal (obligatoria), estrategia SEO/GEO cada 4 ciclos, nueva dirección visual, ideas de proyecto nuevo, pasada del Mejorador.
- Señal de modelo mal asignado: un Opus que tarda > 8 min haciendo lo que dice una lista ya escrita (ciclo 3: Diseñador Opus 14 min/200k ejecutando F1-F7).

## Propiedad de archivos compartidos
- build.py está partido por funciones (ver tabla) hasta que exista ui.py / calcs_loader.py (tarea T1 en journal/ideas-equipo.md). Nadie edita una función ajena: petición.
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
