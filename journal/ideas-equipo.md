# Ideas de mejora del equipo (cambios grandes; mantiene el Mejorador del equipo)
Estado: `[ ]` propuesta · `[>]` asignada a un ciclo · `[x]` hecha · `[~]` descartada. Cada idea con coste, beneficio y métrica.

## Pasada 1 · 2026-10-01 (tras ciclos 1-3)

### [x] T1 · Partir build.py por propiedad: `ui.py` + `calcs_loader.py` (HECHA ciclo 5: diff vacío salvo ?v=, check.py OK)
- Problema: build.py (191 líneas) lo han editado Diseñador (c1 +36, c3 +16: ill/ILL/card/404), Estratega (c2 +73) y Orquestador; la petición `default_from` del Constructor lleva 3 ciclos parada porque build.py no es suyo; F8 (minificar) también está bloqueada ahí. Con agentes en paralelo editando el árbol de trabajo, dos Edit al mismo fichero en un ciclo se pisan sin aviso.
- Tarea concreta (un solo agente Sonnet, ciclo en que NADIE más toca build.py/seo.py; ~6 min, ~60k tokens):
  1. `cd projects/decidir && python3 build.py && cp -r dist /tmp/dist-antes` (o en el scratchpad).
  2. Crear `ui.py` (propietario: Diseñador) con `asset_v`, `ill`, `ILL`, `ICONS`, `tema`, `card`, `catalog_body`, `notfound_body`, `head_extra` y, en `render_calc`, la parte de HTML (cabecera `.ph`, formulario de inputs) como `calc_header(c)` y `calc_form(c)`.
  3. Crear `calcs_loader.py` (propietario: Constructor) con `load_calcs(root, params)`; implementar ahí `"default_from": "params.clave"` (resuelve la petición de c1) y rellenar `tema` por defecto con `ui.tema`.
  4. build.py queda como orquestación (Orquestador): `write`, `render_calc` (montaje + JSON-LD base), `main`, sitemap. seo.py sigue del Estratega.
  5. Criterio de hecho: `diff -r /tmp/dist-antes dist` vacío salvo `?v=` (refactor sin cambio de salida), `ops/check.py` OK, QA OK. Después, en el mismo ciclo o el siguiente, el Diseñador hace F8 (minificar) dentro de ui.py/copiado de assets con la función que exponga.
- Beneficio: elimina la principal fuente de peticiones cruzadas (3 de 11 tocaban build.py) y de choques; el Constructor deja de esperar. Métrica: ediciones de build.py por > 1 rol en un ciclo → 0; peticiones abiertas > 1 ciclo → 0.
- Quién: el Diseñador (Sonnet) en el ciclo 5 (tiene capacidad: la fase F está casi cerrada). El Orquestador no lanza al Estratega en ejecución sobre build.py ese ciclo.

### [ ] T2 · Alinear loop-prompt.md con EQUIPO.md v2 (lo hace el Orquestador; el Mejorador solo puede tocar cadencias)
Ya cambiado por el Mejorador (parámetros de cadencia): Investigador cada 6 ciclos/backlog < 6; Mejorador cada 8. Falta, fuera de mi permiso:
- Diseñador: «1 de cada 3 ciclos» desde ya (DESIGN F1-F7 hecho; F8-F12 son mejoras), no «siempre hasta completar».
- Constructor: «siguiente lote de 2 calculadoras».
- Paso 2.1: barrer requests con el protocolo de EQUIPO.md y anotar en costes.md «peticiones abiertas: N».
- Paso 3.3: horas de costes.md con `date -u +%FT%RZ` (hoy hay una línea de cierre con hora futura) y tokens/minutos por rol tal cual los devuelve cada Agent.
- Coste: 0. Beneficio: que las mejoras de los roles se apliquen de verdad y las métricas sean fiables.

### [ ] T3 · `ops/qa_static.py`: QA estática determinista (dueño: Orquestador; Sonnet, ~40k tokens una vez)
- Script sin dependencias con los parseadores de qa.md (sitemap, JSON-LD, title/description/canonical/h1, enlaces internos, peso por página). Salida `BLOQUEANTE|AVISO archivo:línea`.
- Beneficio: falsos positivos → 0 por construcción; el QA Haiku pasa de ~63k a ~25k tokens/ciclo (solo navegador y cifras). Se paga en 1-2 ciclos.

### [ ] T4 · No esperar al rol más lento (pipeline)
- El ciclo dura lo que el rol más lento (Opus 7-14 min) aunque Constructor y QA acaben en 2 min. Opción: lanzar los roles largos (Investigador, Estratega Opus, Mejorador) en segundo plano y recoger su resultado en el ciclo siguiente, sin bloquear el commit de las calculadoras.
- Coste: complejidad en el Orquestador (archivos tocados por un rol que sigue vivo no entran en el commit). Beneficio: camino crítico ~6 min → más ciclos/h. Ojo: más ciclos/h = más gasto/h; aplicar solo junto con T5.

### [ ] T5 · Ajuste de cadencia por presupuesto semanal (con cifras)
- Medido: ~3,1 ciclos/h, ~0,7 pp semanales por ciclo (16 → 18 % en 3 ciclos; resolución 1 pp → rango 0,5-1,0).
- Proyección 24 h a 120 s, sin cambios: ~69 ciclos × 0,7 = +46 pp → semanal ~64 % al terminar el sprint (rango 52-87 %). Central por debajo del 70 %, pero el rango alto cruza el 70 % (modo ahorro) y roza el 85 % (pausa total), y después queda el resto de la semana.
- Con los cambios de modelo de v2 (Opus medio por ciclo ~205k → ~77k): estimo ~0,45 pp/ciclo; los ciclos bajan a ~15 min (4 c/h) → ~96 ciclos × 0,45 = +43 pp → ~61 %. El gasto por hora casi no cambia, pero se produce el doble (2 calculadoras/ciclo, sin esperas Opus).
- Propuesta (no aplicada: los 120 s los fijó Andoni): disparador «si semanal ≥ 55 % antes de acabar las 24 h → 600 s». Tras el sprint, elegir la cadencia con: pp/día permitidos = (80 − semanal actual) / días hasta el reset semanal (de `get_usage`). Referencia: a 0,45 pp/ciclo, 600 s ≈ 2,4 c/h ≈ +26 pp/día; 1800 s ≈ 1,3 c/h ≈ +14 pp/día. Con ~61 % y 5 días hasta el reset, solo cabe ~1800 s.

### [ ] T6 · Rol nuevo «Verificador fiscal» (Opus, bajo demanda)
- Ya es obligatorio en constructor.md para calculadoras fiscales; formalizarlo como rol con su archivo (entrada: norma + 3 casos; salida: tabla esperado/obtenido) evita que el Constructor improvise el prompt. Coste: ~80-120k Opus por calculadora fiscal (pocas). Activar con declaracion-conjunta-o-individual (antes de marzo 2027).
