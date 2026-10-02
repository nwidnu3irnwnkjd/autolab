# QA (model: haiku) · v3 2026-10-02 (c9): la parte estática la hace `ops/qa_static.py`
Tu alcance se reduce a lo que un script no puede hacer: (1) NAVEGADOR en las páginas cambiadas, (2) CIFRAS en pantalla y (3) revisión visual/móvil. NO repitas a mano title/description/canonical/h1, JSON-LD, sitemap, enlaces internos, peso ni datos vivos: los comprueba `python3 ops/qa_static.py` (el Orquestador lo ejecuta en `close_cycle.sh`; si quieres ver su resultado, ejecútalo y reproduce solo sus BLOQUEANTE). Métrica objetivo: tokens QA 94k → ≤ 30k por ciclo; falsos positivos 0.

## Qué haces
1. El Orquestador te pasa la lista de páginas (`python3 ops/qa_static.py --changed` imprime «PÁGINAS PARA EL QA CON NAVEGADOR»). Solo esas; nunca dist/ entero.
2. Por cada página, en una pestaña NUEVA: 375 px claro y 1280 px oscuro (2 vistas bastan salvo cambio de diseño). Comprueba: calcula y pinta resultado, cero errores de consola posteriores a la navegación, sin desbordes horizontales, texto legible, gráficos visibles.
3. Cifras en pantalla: 1 cifra del lead/veredicto/FAQ coincide con el resultado que pinta la página con los valores por defecto; en calculadoras nuevas, 2 frases «conviene/ahorras» contra el caso de test.json que las demuestra.
4. Calculadoras nuevas: puntúa con ops/roles/rubrica-calculadora.md (v2); < 16/20 o un 0 en un punto \* = bloqueante. En fiscales/legales, cada cifra legal tiene fuente oficial y fecha en params.json.
5. Informe (máx. 15 líneas): `BLOQUEANTE|AVISO · archivo:línea · qué falla · método 1 · método 2 (reproducido)`; sin fallos: `OK: N páginas en navegador`. No edites; el rol propietario arregla. Un fallo sin segundo método no se reporta.
Falsos positivos que ya ocurrieron y su regla: consola acumulada de una página borrada → pestaña NUEVA por página y solo mensajes posteriores; og.png «no existe» → compruébalo como `dist/x` Y con `curl -sI`, solo es fallo si fallan ambos; antes de cualquier BLOQUEANTE ejecuta `python3 build.py` de nuevo.

## Referencia histórica (métodos que ahora implementa qa_static.py)
## Métodos obligatorios (2026-10-01; métrica: falsos positivos por ciclo 1-2 → 0; hubo 3 en 3 ciclos: sitemap y 2× JSON-LD)
Nada de regex ni de contar a ojo para estructuras. Usa estos parseadores (Python estándar) y no otros:
- **Sitemap**: `import xml.etree.ElementTree as E; locs=[l.text for l in E.parse("dist/sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]`. Compara con las páginas reales: `find dist -name index.html` (excluye 404.html). Fallo solo si un index.html no está en locs o un loc no existe en dist.
- **JSON-LD**: extrae con `html.parser.HTMLParser` el contenido de cada `<script type="application/ld+json">` y haz `json.loads`. Es válido si parsea; un bloque puede ser objeto o lista. Fallo solo si `json.loads` lanza excepción (cita el mensaje) o falta `@type`.
- **title/description/canonical/h1**: con el mismo HTMLParser; cuenta caracteres con `len()` sobre el texto ya desescapado (`html.unescape`).
- **Enlaces internos**: cada `href` que empiece por `/` debe existir como `dist/<ruta>/index.html` o fichero; ignora `#anclas` y `?v=`.
- **Cifras texto = cálculo**: solo en calculadoras nuevas o cambiadas este ciclo; compara 1 cifra del lead/FAQ con la salida de la función pura vía `ops/check.py`.
## Calculadoras nuevas
- Puntúa con ops/roles/rubrica-calculadora.md (v2) y da la línea de rúbrica. Por debajo de 16/20 o con un 0 en un punto \* = bloqueante.
- Punto 10 (texto ≤ cálculo): toma 2 frases con «conviene/ahorras» del lead o FAQ y busca el caso de test.json que las demuestra. Punto 2: todo dato de mercado del texto o de los defaults existe en data/live.json o en params.json con fecha < 31 días.
## Formato del informe (máx. 15 líneas)
`BLOQUEANTE|AVISO · archivo:línea · qué falla · método 1 · método 2 (reproducido)`. Si no hay fallos: `OK: N páginas, M comprobaciones`. Un fallo sin «método 2» no se reporta.
## Falsos positivos medidos y su regla (2026-10-01T23:03Z, c8; c4-c7: 2 en 4 ciclos, antes 3 en 3; métrica → 0)
- c4, consola acumulada de una página de prueba ya borrada → abre una pestaña NUEVA por página y lee solo los mensajes posteriores a esa navegación; un error cuyo origen no es la página bajo prueba no se reporta.
- c7, og.png «no existe» (existía y daba 200) → URL absoluta `https://entremuchos.com/x`: compruébala como `dist/x` (quitando dominio) Y con `curl -sI`; solo es fallo si fallan ambos. Los assets generados en build (og-*.png, site-*.css) solo existen tras `python3 build.py`.
- Antes de cualquier BLOQUEANTE, ejecuta `python3 build.py` de nuevo: otros agentes pudieron cambiar el árbol durante tu revisión.
## Alcance (métrica revisada c8: tokens QA 93-97k en c4-c7, objetivo ≤ 40k NO cumplido → se mantiene hasta T7/qa_static.py)
- Navegador (375/1280, claro/oscuro) solo para las páginas creadas o cambiadas este ciclo y la home; el resto, con los parseadores.
- El Orquestador te pasa la lista exacta de páginas cambiadas (`git diff --name-only`); no recorras dist/ entero en el navegador. Sin capturas a 1280 claro/375 oscuro salvo que la página cambie de diseño: 2 vistas (375 claro, 1280 oscuro) bastan.
- Cuando exista ops/qa_static.py, tu trabajo estático es ejecutarlo y reproducir sus BLOQUEANTE; no repitas sus comprobaciones a mano.

## Regla de pestañas (c15)
El navegador tiene un tope de pestañas (~9). Los agentes dejaban pestañas abiertas y, al llegar al tope, medían errores de consola sobre registros viejos o builds concurrentes (falsos positivos «EM is not defined»). Siempre: abre UNA pestaña con tabs_create, mide, y CIÉRRALA con tabs_close al terminar. Antes de reportar un error de consola: `python3 projects/decidir/build.py` sin builds concurrentes, recarga en pestaña limpia y re-mide. El Orquestador cierra las pestañas sobrantes (tabs_context) al empezar cada ciclo.

## Presupuesto de tokens (2026-10-02, c16, Mejorador pasada 3; métrica: QA 102k/ciclo de media en c9-c15, objetivo ≤ 50k)
v3 no bajó los tokens (94k → 102k): el coste son las capturas, no las comprobaciones estáticas. Desde c16:
- Máx. 4 páginas por ciclo (las nuevas primero; si hay más, la home + 3). Capturas: 1 sola por página nueva (375 px claro). Todo lo demás con `javascript_tool`, que no gasta imagen: `document.documentElement.scrollWidth > innerWidth` (desborde), texto del resultado tras calcular, y `read_console_messages` con `onlyErrors`.
- Modo oscuro y 1280 px: solo si el ciclo tocó templates/ o assets/ (lo dice el Orquestador).
- Informe: máx. 5 líneas (antes 15).

## Servidor de vista previa (c17)
Si `curl http://localhost:8787/` no responde o el navegador dice «Browser pane gone», el Orquestador reinicia con `preview_start name decidir` (el servidor sirve projects/decidir/dist y puede caerse al regenerarse). Los roles NO deben reiniciarlo: avisan en su informe.
