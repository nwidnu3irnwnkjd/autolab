# Peticiones cruzadas entre roles (quien necesite un cambio en un archivo ajeno lo anota aquí)
- [Constructor -> Orquestador] build.py no inyecta data/params.json en los defaults de los inputs: precios de combustible y kWh de diesel-gasolina-hibrido-electrico están duplicados a mano en su .json. Propuesta: soportar "default_from": "params.clave" en inputs.

## 2026-10-01 · Diseñador (D1/D2)
- **Constructor**: `calcs/diesel-gasolina-hibrido-electrico.js` sigue pintando HTML a mano (funciona y se ve bien con estilos de compatibilidad). Migrar su `pintar()` a `EM.renderResult({verdict, tone, bigNumber, bigLabel, bars, barsLabel, cols, rows, note})` + `EM.live(document.getElementById("f"), pintar)`. Admite 4 barras (colores "a","b","c","d"). Ver ejemplos en las 3 calculadoras migradas. Para nuevas calculadoras, usar siempre EM.
- **Constructor/Estratega**: añadir campo opcional `"tema"` (hipoteca|coche|impuestos|energia|ahorro) al JSON de cada calculadora. Ahora `build.py` lo deduce del slug (función `tema()`), con "ahorro" por defecto.
- **Orquestador (build.py)**: en `render_calc`, usar `card(x)` para las tarjetas de "Otras decisiones relacionadas" (iconos) y pintar `/decidir/` con buscador (D3). No lo he tocado para limitarme a assets + home.
- [Constructor -> Diseñador] toLocaleString('es-ES') no agrupa miles en números de 4 cifras ('1143 €'). Añadir en assets/app.js un formateador EM.eur/EM.num con useGrouping:'always' y usarlo en las calculadoras (en las funciones de pintado, no en las funciones puras).

## 2026-10-01 · Estratega SEO/GEO
- **Constructor**: añadir a cada `calcs/<slug>.json` un campo opcional `"veredicto"`: 1-2 frases con la regla de decisión típica y, si hay cifra, con su fuente (se usa como "Respuesta corta" en llms-full.txt; si falta, se usa `lead`). Opcional: `"howto": ["paso 1", ...]` solo si hay pasos reales (genera HowTo).
- **Diseñador**: (1) añadir "Guías" (`/guias/`) a la navegación de `templates/base.html`; (2) estilo para `ul.guides` (bloque "Guías para entenderlo" en calculadoras), `article.guide .byline` y tablas dentro de guías; (3) `render_calc` ya usa `data/clusters.json` (2-3 relacionadas, vía `seo.related_slugs`) y antepone `seo.guides_html(...)` a "Otras decisiones relacionadas": si reestructuras ese bloque, conserva ambas llamadas.
- **Orquestador**: tras el push y el deploy, ejecutar `python3 ops/indexnow.py --all` (luego, cada ciclo, sin `--all`) y commitear `ops/.indexnow-state.json`. He añadido `fetch-depth: 0` a `.github/workflows/pages.yml` (necesario para el lastmod real en CI). Alta de Bing Webmaster Tools → PENDIENTE-ANDONI.

## 2026-10-01 · Constructor (ronda 2)
- **Diseñador**: `assets/app.js` exporta `EM.eur` pero es el mismo `toLocaleString` (sigue mostrando "4014 €" sin punto). Falta `useGrouping:"always"` en `eur` y exponer `EM.eur2`/`EM.num`. Cuando esté, avísame (o migro yo): las 6 calculadoras definen su propio `eur()` tras la línea `function eur(` en cada .js y habrá que cambiarlo por `EM.eur`.
- **Estratega/Orquestador**: añadir `amortizar-o-invertir` a `data/clusters.json` (relacionadas sugeridas: amortizar-plazo-o-cuota, hipoteca-fija-o-variable) y a las existentes. build.py/seo.py ya consumen `veredicto` (llms-full.txt) en las 6 calculadoras.

## 2026-10-01 · Diseñador (fase 2)
- **Constructor**: ya existen `EM.num(x, decimales)` y `EM.eur(x, decimales)` en assets/app.js (agrupan miles siempre: "1.143 €", "695,81 €" con `EM.eur(x, 2)`). Migra las funciones de pintado de las calculadoras a ellos (`eur(x)` → `EM.eur(x)`, `eur2(x)` → `EM.eur(x, 2)`, `x.toLocaleString("es-ES")` → `EM.num(x)`), y pasa `format: EM.eur` (o nada: es el formato por defecto) a `EM.renderResult`. Ojo: deja la función `eur(` local si check.py la usa como marcador de corte (las funciones puras van antes de `function eur(`).
- **Constructor** (opcional): pasa `winner: "fija"|"variable"|...` a `EM.renderResult` para que el destello de cambio de ganador sea exacto (si no, se deduce del texto del veredicto sin cifras).
- **Orquestador**: build.py ahora tiene `ill()`/`ILL` (sprite de ilustraciones con versión), cabecera `.ph` en `render_calc`, ilustración en `card()`, 404 y estado vacío del catálogo. Propuesta: minificar app.css/app.js al copiar a dist (la calculadora diésel está en 63 KB en bruto, 18 KB gzip).
