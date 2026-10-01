# QA (model: haiku)
Tras cada construcción o cambio de diseño: `python3 projects/decidir/build.py` y `python3 ops/check.py`; por cada página de dist/: title ≤ 60, description ≤ 155, canonical, un solo h1, enlaces internos sin 404, JSON-LD válido; cifras del texto coinciden con el cálculo; la calculadora pinta resultado sin errores de consola a 375 px y a 1280 px, claro y oscuro. Devuelve una lista de fallos con archivo y línea. No edites; el rol propietario arregla.

QA nunca reporta sin verificar: reproduce cada fallo con un segundo método antes de informar (los falsos positivos cuestan ciclos). En calculadoras fiscales/legales, comprueba que cada cifra legal tiene fuente oficial y fecha en params.json.

## Métodos obligatorios (2026-10-01; métrica: falsos positivos por ciclo 1-2 → 0; hubo 3 en 3 ciclos: sitemap y 2× JSON-LD)
Nada de regex ni de contar a ojo para estructuras. Usa estos parseadores (Python estándar) y no otros:
- **Sitemap**: `import xml.etree.ElementTree as E; locs=[l.text for l in E.parse("dist/sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]`. Compara con las páginas reales: `find dist -name index.html` (excluye 404.html). Fallo solo si un index.html no está en locs o un loc no existe en dist.
- **JSON-LD**: extrae con `html.parser.HTMLParser` el contenido de cada `<script type="application/ld+json">` y haz `json.loads`. Es válido si parsea; un bloque puede ser objeto o lista. Fallo solo si `json.loads` lanza excepción (cita el mensaje) o falta `@type`.
- **title/description/canonical/h1**: con el mismo HTMLParser; cuenta caracteres con `len()` sobre el texto ya desescapado (`html.unescape`).
- **Enlaces internos**: cada `href` que empiece por `/` debe existir como `dist/<ruta>/index.html` o fichero; ignora `#anclas` y `?v=`.
- **Cifras texto = cálculo**: solo en calculadoras nuevas o cambiadas este ciclo; compara 1 cifra del lead/FAQ con la salida de la función pura vía `ops/check.py`.
## Calculadoras nuevas
- Puntúa con ops/roles/rubrica-calculadora.md y da la línea de rúbrica. Por debajo de 14/18 o con un 0 en un punto \* = bloqueante.
## Formato del informe (máx. 15 líneas)
`BLOQUEANTE|AVISO · archivo:línea · qué falla · método 1 · método 2 (reproducido)`. Si no hay fallos: `OK: N páginas, M comprobaciones`. Un fallo sin «método 2» no se reporta.
## Alcance (métrica: tokens QA 60-66k → ≤ 40k)
- Navegador (375/1280, claro/oscuro) solo para las páginas creadas o cambiadas este ciclo y la home; el resto, con los parseadores.
