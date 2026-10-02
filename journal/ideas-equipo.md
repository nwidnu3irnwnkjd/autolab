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

### [~] T2 · (c8: PARCIAL — lote de 2, Diseñador 1/3 y cadencias ya están en loop-prompt; lo que falta, barrido de requests y horas `date -u`, pasa a T7 como script) Alinear loop-prompt.md con EQUIPO.md v2 (lo hace el Orquestador; el Mejorador solo puede tocar cadencias)
Ya cambiado por el Mejorador (parámetros de cadencia): Investigador cada 6 ciclos/backlog < 6; Mejorador cada 8. Falta, fuera de mi permiso:
- Diseñador: «1 de cada 3 ciclos» desde ya (DESIGN F1-F7 hecho; F8-F12 son mejoras), no «siempre hasta completar».
- Constructor: «siguiente lote de 2 calculadoras».
- Paso 2.1: barrer requests con el protocolo de EQUIPO.md y anotar en costes.md «peticiones abiertas: N».
- Paso 3.3: horas de costes.md con `date -u +%FT%RZ` (hoy hay una línea de cierre con hora futura) y tokens/minutos por rol tal cual los devuelve cada Agent.
- Coste: 0. Beneficio: que las mejoras de los roles se apliquen de verdad y las métricas sean fiables.

### [x] T3 · (HECHA c9: ops/qa_static.py) (c8: se integra en T7, prioridad 1) `ops/qa_static.py`: QA estática determinista (dueño: Orquestador; Sonnet, ~40k tokens una vez)
- Script sin dependencias con los parseadores de qa.md (sitemap, JSON-LD, title/description/canonical/h1, enlaces internos, peso por página). Salida `BLOQUEANTE|AVISO archivo:línea`.
- Beneficio: falsos positivos → 0 por construcción; el QA Haiku pasa de ~63k a ~25k tokens/ciclo (solo navegador y cifras). Se paga en 1-2 ciclos.

### [>] T4 · (c8: aplicar SOLO a la cadena fiscal, ver T8) No esperar al rol más lento (pipeline)
- El ciclo dura lo que el rol más lento (Opus 7-14 min) aunque Constructor y QA acaben en 2 min. Opción: lanzar los roles largos (Investigador, Estratega Opus, Mejorador) en segundo plano y recoger su resultado en el ciclo siguiente, sin bloquear el commit de las calculadoras.
- Coste: complejidad en el Orquestador (archivos tocados por un rol que sigue vivo no entran en el commit). Beneficio: camino crítico ~6 min → más ciclos/h. Ojo: más ciclos/h = más gasto/h; aplicar solo junto con T5.

### [x] T5 · (c8: aplicada en loop-prompt con datos reales, ver EQUIPO.md c8.7) Ajuste de cadencia por presupuesto semanal (con cifras)
- Medido: ~3,1 ciclos/h, ~0,7 pp semanales por ciclo (16 → 18 % en 3 ciclos; resolución 1 pp → rango 0,5-1,0).
- Proyección 24 h a 120 s, sin cambios: ~69 ciclos × 0,7 = +46 pp → semanal ~64 % al terminar el sprint (rango 52-87 %). Central por debajo del 70 %, pero el rango alto cruza el 70 % (modo ahorro) y roza el 85 % (pausa total), y después queda el resto de la semana.
- Con los cambios de modelo de v2 (Opus medio por ciclo ~205k → ~77k): estimo ~0,45 pp/ciclo; los ciclos bajan a ~15 min (4 c/h) → ~96 ciclos × 0,45 = +43 pp → ~61 %. El gasto por hora casi no cambia, pero se produce el doble (2 calculadoras/ciclo, sin esperas Opus).
- Propuesta (no aplicada: los 120 s los fijó Andoni): disparador «si semanal ≥ 55 % antes de acabar las 24 h → 600 s». Tras el sprint, elegir la cadencia con: pp/día permitidos = (80 − semanal actual) / días hasta el reset semanal (de `get_usage`). Referencia: a 0,45 pp/ciclo, 600 s ≈ 2,4 c/h ≈ +26 pp/día; 1800 s ≈ 1,3 c/h ≈ +14 pp/día. Con ~61 % y 5 días hasta el reset, solo cabe ~1800 s.

### [x] T6 · (c8: creado ops/roles/verificador-fiscal.md, alcance reducido) Rol nuevo «Verificador fiscal» (Opus, bajo demanda)
- Ya es obligatorio en constructor.md para calculadoras fiscales; formalizarlo como rol con su archivo (entrada: norma + 3 casos; salida: tabla esperado/obtenido) evita que el Constructor improvise el prompt. Coste: ~80-120k Opus por calculadora fiscal (pocas). Activar con declaracion-conjunta-o-individual (antes de marzo 2027).

## Pasada 2 · 2026-10-01T23:03Z (ciclo 8, datos de c4-c7)

### [x] T7 · (HECHA c9: ops/close_cycle.sh con --dry-run; falta el primer cierre real) `ops/close_cycle.sh` (+ `ops/qa_static.py`): cierre de ciclo en un comando (dueño: Orquestador; Sonnet, ~70k tokens una vez; ciclo 9)
- Problema medido: cada ciclo el Orquestador repite a mano ~10 pasos y deja 3 commits (ciclo, «estado IndexNow», «estado ciclo N»: ver `git log`); costes.md tiene horas desordenadas y valores «~»; el QA Haiku gasta 94k/ciclo, la mitad en comprobaciones estáticas deterministas; las peticiones se resuelven sin marcar.
- Especificación (bash + python estándar, sin red salvo git/curl/IndexNow; `set -euo pipefail`; sale ≠ 0 al primer rojo y NO hace commit):
  1. `close_cycle.sh <N> "<mensaje>" <5h%> <semanal%> <extraEUR> "<roles y tokens>"` (los % los da get_usage, que es MCP y no se puede llamar desde bash).
  2. `cd projects/decidir && python3 build.py && cd ../.. && python3 ops/check.py` → rojo = salir.
  3. `python3 ops/qa_static.py` (T3): sitemap ↔ index.html, JSON-LD `json.loads` + `@type`, title ≤ 60 / description ≤ 155 / canonical / 1 h1 (HTMLParser + unescape), enlaces internos, peso < 60 KB, og:image existe en dist; y además: (a) cada `default_from: live.*` resuelve a un dato con `ok` y fecha ≤ 7 d (45 d Euríbor); (b) números de lead/veredicto/FAQ de las calculadoras cambiadas que no aparecen en params/live/salida de test → AVISO (semilla del Editor YMYL, T9). Salida `BLOQUEANTE|AVISO archivo:línea`; BLOQUEANTE = salir.
  4. Imprime para el QA Haiku la lista de páginas cambiadas (`git diff --name-only HEAD` → rutas de dist) — el QA solo hace navegador y cifras sobre esa lista.
  5. Recuento de requests: líneas `- [ ]` de ops/requests.md con su `abierta cN`; las de N < ciclo−1 se imprimen como «ABIERTA > 1 ciclo: dueño».
  6. Añade a journal/costes.md la línea `$(date -u +%FT%RZ) | 5h | semanal | extra | ciclo N cierre: roles…; peticiones abiertas: K; páginas: P`.
  7. `git add -A && git commit -m "ciclo N: …"` (UN commit), `pull --rebase` con el credential helper del loop-prompt; si el pull trae data/live.json, repite 2-3; `push`.
  8. Espera hasta 180 s a que cada página nueva dé 200 en https://entremuchos.com (curl en bucle cada 15 s); `python3 ops/indexnow.py`; `git commit --amend` NO (ya empujado): el estado de IndexNow entra en el commit del ciclo siguiente.
  9. Imprime un resumen de 5 líneas para ESTADO.md (el Orquestador lo redacta; el script no escribe ESTADO.md).
- Beneficio: −2 commits/ciclo, costes.md fiable, QA Haiku 94k → ~30k (≈ −0,07 pp/ciclo ≈ −1,5 pp/día al ritmo del sprint), −3-5 min de cierre del Orquestador, recuento de peticiones automático. Se paga en 1-2 ciclos.
- Criterio de hecho: ejecutado en el ciclo 9 de punta a punta; qa_static.py da 0 BLOQUEANTE en el estado actual y detecta un fallo inyectado a propósito (title de 70 caracteres en una copia del dist).

### [>] T8 · Cadena fiscal en paralelo y más barata (dueño: Orquestador + Constructor + Verificador; desde el ciclo 9)
- Medido c7 (IRPF): Constructor 210k + Verificador Opus 231k + correcciones 94k + re-verificación Opus 253k = ~790k (~0,85 pp semanales) y 33 min de ciclo (el resto de roles esperando). Encontró 4 errores reales (1 fórmula de borde, 1 combinación no legal, 2 textos que prometían más que el cálculo). Las tablas (15 CCAA) ya estaban bien: el Investigador las había verificado en c6; el verificador las rehízo todas.
- ¿Cuándo compensa? Siempre para impuestos/cotizaciones (YMYL; un error cambia el ganador para usuarios reales y es la página con más riesgo reputacional). No compensa repetir tablas ya verificadas con fecha ni una segunda pasada Opus completa.
- Cómo abaratar (ya en roles): oráculo Python del Constructor + barrido ≥ 500 casos contra el JS real (cazaría el error de la DA 61.ª con Sonnet); Verificador Opus solo aplicabilidad legal + texto ≤ cálculo + supuestos + bordes + tablas por muestreo (≤ 12 min); re-verificación Sonnet re-ejecutando scripts. Estimado: Opus 484k → ~120-150k; total ~790k → ~400k por fiscal (−0,4 pp cada una).
- Pipeline (parte de T4): la fiscal NO bloquea el ciclo. Ciclo N: Constructor fiscal + oráculo; ciclo N+1: Verificador (en segundo plano) mientras el resto del ciclo publica; ciclo N+2: correcciones + re-verificación Sonnet + publicación. La calculadora no entra en el sitemap hasta el veredicto (la deja fuera del commit o con `"borrador": true` — petición al Orquestador para que build.py lo respete). Coste: complejidad en el commit; beneficio: ciclos de ~12 min en vez de 33 con fiscal.
- Límite de scope: 1 fiscal en vuelo a la vez; las ramas < 1 % de usuarios que no cambian el veredicto se declaran como límite, no se modelan.

### [x] T9 · (HECHA c9: chequeo YMYL en qa_static.py) «Editor de calidad/YMYL» como script, no como rol (dueño: Orquestador; dentro de T7.3b; ~20k extra)
- Coste/beneficio: un rol LLM por ciclo costaría ~60-90k (~0,07 pp/ciclo) para revisar textos que casi no cambian; los errores de texto vistos (2 en IRPF, Euríbor del día 1) los evitan mejor la rúbrica v2 (punto 10), el checklist del Constructor y un chequeo determinista: frases con «Ley|art\.|BOE|RDL|%|€» en content/ y calcs/*.json sin enlace a fuente en la misma sección, y números del texto que no salen de params/live/tests → AVISO. Decisión: **script ahora (en T7), rol nunca salvo que el script dé > 3 avisos reales por ciclo.**

### [ ] T10 · «Analista de datos» (Search Console/GA4) — dejar en ideas
- Hoy 0 indexadas / 0 impresiones: no hay nada que analizar; metrics.py cada 6 ciclos ya lo cubre. Activar como Sonnet (no Opus) cada 6 ciclos cuando haya ≥ 100 impresiones/semana o ≥ 5 páginas con impresiones; salida: 3 páginas a mejorar con su consulta y CTR, al Estratega. Coste ~40k por pasada; beneficio: priorizar con datos reales en vez de hipótesis.

### [ ] T11 · Marcado del Pulso a ui.py (dueño: Diseñador + Estratega, 1 ciclo sin otros cambios en seo.py; Sonnet ~40k)
- En c7 el Diseñador editó `seo.pulso_html` (marcado) y `ops/check_live.py` (archivos ajenos). Separar: `seo.pulso_data(LIVE, slug)` (Estratega, datos y fuentes) → `ui.pulso_card(items)` (Diseñador, HTML). Métrica: ediciones de archivo ajeno → 0. Criterio de hecho: diff de dist vacío.

### [ ] T12 · «Agente de enlaces/difusión» — dejar en ideas
- Lo cubre la palanca 4 del Estratega (propuestas, nunca spam) y casi todo requiere cuentas → PENDIENTE-ANDONI. Sin indexación todavía, difundir no se puede medir. Activar (Sonnet, 1 vez por semana, solo lista de 5 sitios/comunidades con el recurso concreto que aportamos) cuando el Barómetro tenga 2 meses de datos o haya ≥ 20 calculadoras indexadas. Coste ~50k/semana.

### [ ] T13 · Investigador en el ciclo 9
- Tras c8 (pensiones + luz) el backlog queda con 1 no fiscal (placas) y 3 fiscales: la regla «< 6 no fiscales» ya se cumple. Foco Sonnet con web: 6 calculadoras no fiscales de alto volumen («X o Y» de hogar, coche, energía) para no depender de la cadena fiscal cara.

## Pasada 3 · 2026-10-02T02:30Z (ciclo 16, datos de c8-c15)

### [>] T8 · estado c16
- Abaratamiento hecho (Opus 484k → 150k por fiscal). Pipeline no bloqueante: NO hecho; las fiscales siguen alargando el ciclo (24-29 min frente a ~13). Tras el sprint, con ciclos espaciados por presupuesto, el pipeline pierde valor: **se aparca** salvo que vuelva una cadencia alta.

### [>] T14 · (c24: NO HECHA en 8 ciclos → PRIORIDAD 1 del Orquestador, próximo ciclo sin fiscal o el primer ligero) `ops/qa_static.py --fiscal`: chequeos deterministas de los patrones 1, 3 y 4 (dueño: Orquestador; Sonnet ~50k una vez)
- (a) Absolutos sin condición: frases de content/<slug>.html y de lead/veredicto/faq de calcs/<slug>.json con `siempre|nunca|garantiza|solo tiene sentido|en todos los casos` y sin `si |salvo|con la|sin |cuando|excepto` en la misma frase → AVISO. Habría marcado donativos, rescate y autónomo (3 de 8).
- (b) Cifras legales: cada número con `€|%` en una frase con `art\.|Ley|RDL|RD |DA ` debe estar en params.json bajo una clave con `_fuente` (y fecha de consolidación) → AVISO si no. Sustituye al YMYL actual «sin enlace en la sección», que da 64 AVISO de ruido.
- (c) Ámbito: toda calc con `"fiscal": true` debe mencionar País Vasco/Navarra y Canarias (y Ceuta/Melilla si hay IVA/IGIC/IPSI) en página o sources → AVISO.
- Beneficio: ~1-2 cambios menos por fiscal para el Opus (~−20k Opus, ~−0,02 pp por fiscal) y que el aviso YMYL vuelva a ser leíble (0-3 por ciclo en vez de 64). Coste: ~50k una vez. Criterio de hecho: sobre el estado de c14 (antes de las correcciones del rescate) marca «nunca paga más».

### [ ] T15 · Cierre de verdad en 1 commit y con poca salida (dueño: Orquestador; ~20k)
- Medido c9-15: 2 commits por ciclo porque ESTADO.md y el journal se escriben DESPUÉS de close_cycle.sh. Arreglo: el Orquestador escribe ESTADO.md y journal antes (con los datos que ya tiene) y el script los incluye en su `git add -A`; el resumen de 5 líneas solo corrige ESTADO en el ciclo siguiente.
- close_cycle.sh imprime con `tee` toda la salida de qa_static (64 AVISO ≈ 4k tokens en el contexto del Orquestador por cierre): imprimir solo BLOQUEANTE, el recuento de AVISO y los 5 primeros.
- Peticiones > 1 ciclo: el script ya las lista pero nadie las cierra porque el dueño no se lanza ese ciclo (Estratega solo pares). Regla: si una petición llega a 3 ciclos y el dueño no está en el ciclo, el Orquestador la resuelve si es ≤ 2 min o la marca `[~]` con motivo. Métrica: > 1 ciclo 6 → ≤ 1.
- Beneficio: −1 commit/ciclo, −4-8k tokens de contexto/ciclo, cumplir T7.

### [ ] T16 · «Editor de calidad» de contenido: pasada única, no rol permanente
- Coste/beneficio: rol por ciclo ≈ 80k Sonnet (~0,08 pp, ~1,8 pp/día al ritmo del sprint) para textos que casi no cambian entre ciclos; lo que de verdad falla (absolutos, cifras legales) lo cubren T14 y la pre-verificación. Inconsistencias que sí hay entre 29 calculadoras (disclaimer, «Supuestos y fuentes», formato del veredicto, tuteo, nombres de impuestos) se arreglan mejor de una vez.
- Propuesta: tras el sprint, en un ciclo ligero, 1 Sonnet ~150k lee lead/veredicto/FAQ de todas las calculadoras (no el HTML entero) y abre peticiones al Constructor con una guía de estilo de 15 líneas en ops/roles/rubrica-calculadora.md. Repetir solo si se superan 50 calculadoras.

### [ ] T10 · «Analista de datos» (actualizado c16): sigue sin activar
- GA4 y GSC existen pero 0 indexadas / 0 impresiones; metrics.py cada 6 ciclos basta. Disparador sin cambios: ≥ 100 impresiones/semana o ≥ 5 páginas con impresiones → Sonnet ~40k cada 6 ciclos (o 1 vez/día tras el sprint), salida 3 páginas a mejorar al Estratega.

### [x] T17 · (CERRADA c24: 1 FP en c16-c23, ninguno de consola) Pestañas del navegador (anotado c15): medir antes de hacer más
- Regla de c15 en qa.md (1 pestaña por agente, tabs_close, el Orquestador limpia al empezar). Si en c17-c20 vuelve un falso positivo de consola, el QA usa `read_console_messages` con `pattern` del archivo de la página y el Orquestador ejecuta los builds en serie (nadie hace build mientras el QA mide). Coste 0.

### [ ] T18 · Contexto del Orquestador (70 % de 1M a c15)
- Aplicado c16.5 (informes ≤ 5 líneas). Además, fuera de mi permiso (Orquestador): no releer requests.md/SEO-GEO.md/EQUIPO.md enteros cada ciclo (`grep '^- \[ \]'`, `tail`), leer de los verificadores solo la línea VEREDICTO, y antes de la autocompactación dejar ESTADO.md al día (ya es la memoria). Métrica: % de contexto por ciclo anotado en ESTADO.md; ≤ 25k/ciclo.

## Pasada 4 · 2026-10-02T05:20Z (ciclo 24, datos de c16-c23)

### [>] T14 · añadido c24 (además de a-c)
- (d) Citas sin artículo: «según el Manual», «según la AEAT», «la ley establece» sin `art.` ni enlace en la misma frase → AVISO (c23 IMV). (e) Toda calc fiscal debe tener journal/preverif-<slug>.md con 8 líneas (patrones 1-8) → AVISO si falta. Coste total T14 ~50-60k Sonnet una vez; criterio de hecho igual que antes (marca «nunca paga más» en el estado de c14) + marca la cita «según el Manual» del estado de c23 previo a las correcciones.

### [ ] T19 · Experimento «lector de norma» Sonnet en las 2 próximas fiscales (dueño: Orquestador; ~50k Sonnet por fiscal)
- Problema: en paro (c19) y jubilación (c18) el oráculo del Constructor reprodujo su propia lectura (0 discrepancias en 600 casos) y el error salió con el Opus, que necesitó 2.ª pasada (+112k, +154k). En SL (c21) el 15 % de nueva creación se vendía sin la exclusión del art. 29.1.b. Patrón común: interpretación, no aritmética.
- Prueba: en paralelo al Constructor fiscal (no después), un Sonnet con rol constructor.md que recibe SOLO el slug, la pregunta y las leyes a leer (sin calcs/ ni oráculo) y entrega ≤ 10 líneas: para cada opción, qué cobra/paga, cuánto tiempo, artículos y DT, y qué la hace imposible (patrones 7 y 8). El Orquestador compara con el bloque `INTERPRETACION` del oráculo: si difieren, la discrepancia va al Verificador como entrada.
- Coste/beneficio: +~0,05 pp por fiscal. Beneficio esperado: evitar la 2.ª pasada Opus en 1 de cada 3 fiscales (~130k Opus ≈ 0,14 pp → ~0,05 pp por fiscal) y cazar antes un error que invierte el veredicto. Neutral en tokens, positivo en riesgo. **Decisión tras 2 fiscales**: se queda si caza ≥ 1 diferencia real que el Opus confirme; si 0 de 2, se descarta (el paso 0 del Verificador, gratis dentro de su presupuesto, cubre lo mismo). Por qué no un Opus o un rol fijo: el paso 0 + patrones 7-8 ya cuestan ~0; un rol fijo sin evidencia sería +0,05 pp × 5 fiscales pendientes.

### [ ] T20 · HANDOFF del Orquestador: lo que falta para reanudar sin pérdida (dueño: Orquestador; AHORA, antes del 97 %)
Revisado ESTADO.md a c23: el HANDOFF dice quién es, preferencias, el ciclo y credenciales, pero faltan los datos que se pierden en la compactación. Añadir (≤ 10 líneas; bloque listo para pegar):
```
- Estado en vuelo: ciclo N en curso/cerrado; agentes lanzados y sin recoger (descripción, archivos que tocan); fiscal en qué paso (construida / verificador / fixes / re-verificación / publicada) y su journal/preverif-<slug>.md y verificacion-<slug>.md.
- Calendario de roles: Estratega Opus c28 (Sonnet en pares), Investigador c28 (o backlog < 6 no fiscales), Mejorador c32, metrics.py c30; Diseñador 1 de cada 3 (último c21 → c24/25).
- Presupuesto: reset semanal 2026-10-06T15:00Z; sprint a 120 s hasta 2026-10-02T21:00Z salvo semanal ≥ 55 % (→ 600 s); después loop-prompt §3.4 (ligero por defecto, 1 de 4 completo); fiscales antes de que el semanal pase del 70 % (~4-oct 16:00Z).
- Cómo recuperar el estado en 4 comandos: `git log --oneline -3`; `tail -2 journal/costes.md`; `grep -n '^- \[ \]' ops/requests.md`; `ls -t journal/verificacion-*.md journal/preverif-*.md | head -3`.
- No releer: SEO-GEO.md, requests.md, ideas.md, verificacion-pendiente.md, EQUIPO.md enteros (usar grep/tail).
- Encargo del QA: solo URL + input a cambiar + texto de aviso a buscar (qa.md v4 hace el resto); ruido conocido en qa.md.
- Siguiente tarea de equipo: T14 (qa_static --fiscal), T15 (1 commit), T19 en las 2 próximas fiscales.
```
- Además, corregir en ESTADO.md la línea «Fiscal: 5 calculadoras verificadas… Pendientes: placas, rescate» (desfasada desde c14; contradice «14 verificadas» de la línea de gasto) y la de calidad («5 falsos positivos en 7 ciclos»: ahora 1 en 8). Un HANDOFF con datos viejos es peor que ninguno.
- Métrica: tras la compactación, el primer ciclo se cierra sin releer archivos largos y sin repetir trabajo (comparar `git log` del ciclo siguiente con el anterior).

### [ ] T15 · estado c24: sin hacer (2 commits por ciclo; la parte de peticiones sí: 3 abiertas, 2 hechas sin marcar). Sin cambios en la propuesta.
### [ ] T16 · estado c24: sin hacer; 76 páginas (> 50 calculadoras): toca tras el sprint, en el primer ciclo ligero con margen.
### [ ] T10 · estado c24: sigue sin activar (0 impresiones).

