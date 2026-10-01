# Estrategia viva de posicionamiento (SEO + GEO) — entremuchos.com
Mantiene el Estratega. Formato: hipótesis → experimento → métrica → resultado → decisión.

## Estado inicial (2026-10-01)
- Sitio online, calculadoras publicadas, sitemap enviado a Search Console, GA4 conectado.
- **Línea base (ops/metrics.py, 2026-10-01):** sitemap pendiente, 0 descubiertas, 0 indexadas, 0 clics, 0 impresiones. GA4 sin datos.

## Qué funciona hoy (investigación oct 2026, con fuentes)
1. **Google (incluidas AI Overviews y AI Mode): no hay requisitos ni marcado especiales.** Basta con estar indexado y ser apto para fragmento; ni schema ni archivos "para IA" son necesarios. Las AI Overviews se miden en Search Console (tipo "Web"). → Lo que mueve la aguja en Google es indexación, contenido útil "people-first" y página rápida. [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
2. **`Google-Extended` solo controla el uso para entrenar Gemini;** no afecta a la inclusión ni al ranking en Search. Permitirlo no tiene coste. [Google common crawlers](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers)
3. **ChatGPT search depende de `OAI-SearchBot`**: si se bloquea, no apareces en respuestas de ChatGPT search. `GPTBot` = entrenamiento; `ChatGPT-User` = lecturas a petición del usuario (robots.txt puede no aplicarse). Cambios de robots tardan ~24 h. [OpenAI: Overview of crawlers](https://developers.openai.com/api/docs/bots)
4. **Claude: tres bots independientes** — `ClaudeBot` (entrenamiento), `Claude-SearchBot` (índice de búsqueda), `Claude-User` (lecturas a petición). Bloquear uno no bloquea los otros. [Anthropic: ¿rastrea Anthropic la web?](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
5. **Perplexity:** `PerplexityBot` indexa para mostrar y enlazar en resultados (no entrena); `Perplexity-User` = peticiones de usuario. [Perplexity crawlers](https://docs.perplexity.ai/guides/bots)
6. **llms.txt:** formato = H1 + blockquote de resumen + secciones H2 con listas `[nombre](url): nota` + sección `Optional`. [llmstxt.org](https://llmstxt.org/). **Evidencia de uso: casi nula.** Estudios 2026 (Ahrefs ~137 k dominios, análisis de 500 M de eventos de bots) indican que los crawlers de IA casi nunca piden /llms.txt y ningún laboratorio declara usarlo en producción. [digitalapplied: llms.txt adoption & evidence 2026](https://www.digitalapplied.com/blog/llms-txt-in-practice-adoption-evidence-2026), [geoly: does llms.txt work](https://www.geoly.ai/blog/does-llms-txt-work). → Lo mantenemos porque cuesta cero y se genera solo, pero **no es una palanca**: no esperar efecto.
7. **IndexNow:** clave 8-128 caracteres hex en `/<clave>.txt`, POST JSON `{host, key, keyLocation, urlList}` a `api.indexnow.org` (hasta 10 000 URLs; 200/202 = OK; 403 clave; 422 host; 429 abuso). Enviar solo URLs nuevas/cambiadas; no garantiza indexación. Llega a Bing (y con ello a Copilot) y al resto de buscadores participantes. [IndexNow docs](https://www.indexnow.org/documentation), [Bing IndexNow](https://www.bing.com/indexnow/getstarted)
8. **Bing Webmaster Tools tiene informe "AI Performance"** (citas en Copilot y resúmenes de Bing, consultas de grounding, Citation Share desde jun 2026). Es la única medición directa de citas en IA disponible gratis. [Bing blog feb 2026](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview), [SEJ](https://www.searchenginejournal.com/bing-webmaster-tools-adds-ai-citation-performance-data/566874/)
9. **Schema:** HowTo rich results retirados (2023); FAQ rich results dejaron de mostrarse del todo en mayo de 2026. El marcado sigue sirviendo para que Google entienda la página, pero no da fragmentos enriquecidos. [SEJ: HowTo/FAQ](https://www.searchenginejournal.com/google-downgrades-visibility-of-howto-and-faq-rich-results/493522/), [Google Search docs updates](https://developers.google.com/search/updates). → Mantener FAQPage/Breadcrumb/WebApplication/Article por entendimiento; **HowTo solo si una calculadora trae pasos reales** (campo opcional `howto`), sin esperar rich result.

## Hipótesis
- H1 (indexación): el freno ahora es que Google no ha descubierto nada. Sitemap con lastmod real + enlazado interno denso + IndexNow aceleran el descubrimiento (Bing antes que Google).
- H2 (GEO): a los asistentes les citan páginas con respuesta directa al principio, cifras con fuente oficial y tablas limpias. Las guías "respuesta primero" (Euríbor, comisiones Ley 5/2019) son más citables que una calculadora sola, y empujan a la calculadora (el foso: el cálculo con tus números no lo replica la IA).
- H3 (clúster): enlazar cada calculadora con 2-3 afines y con sus guías concentra autoridad temática en "hipoteca y vivienda", el clúster con más demanda en España.

## Implementado (ciclo 2026-10-01, reversible)
| Cambio | Dónde | Cómo revertir |
|---|---|---|
| `robots.txt` con permiso explícito a Googlebot, Bingbot, Applebot, OAI-SearchBot, ChatGPT-User, GPTBot, Claude-SearchBot, Claude-User, ClaudeBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended, CCBot, DuckAssistBot, MistralAI-User + sitemap | `projects/decidir/static/robots.txt` | editar el archivo |
| `llms.txt` y `llms-full.txt` generados en cada build desde calculadoras y guías (pregunta, respuesta corta, criterios, parámetros, FAQs, fuentes) | `seo.write_llms` | quitar la llamada en `main()` |
| IndexNow: clave en `static/<clave>.txt` y `ops/indexnow.py` (envía solo URLs con lastmod nuevo; estado en `ops/.indexnow-state.json`) | `ops/indexnow.py` | borrar clave y script |
| Sitemap con **lastmod real**: último commit de los archivos de contenido de cada página (git log; si hay cambios sin commit, fecha del archivo) + fecha de parámetros si aparecen en la página. Workflow con `fetch-depth: 0` para que funcione en CI | `seo.lastmod`, `write(..., lastmod=)`, `.github/workflows/pages.yml` | volver a `date.today()` |
| Clústeres: afinidad (mismo tema +10, palabras clave compartidas +1), 2-3 relacionadas por calculadora → `data/clusters.json`; `render_calc` lo usa si existe | `seo.build_clusters` | borrar `data/clusters.json` (vuelve al orden por tema) |
| Schema: `Article` (autor "Equipo de Entre Muchos", datePublished = primer commit, dateModified = lastmod) en calculadoras y guías; `HowTo` opcional (`"howto": [...]` en el JSON); `Organization` + `WebSite` con `SearchAction` (`/decidir/?q=`, ya soportado por app.js) en la home. Todo el JSON-LD validado con `json.loads` | `seo.calc_jsonld`, `seo.home_jsonld` | quitar las llamadas |
| Guías: `/guias/euribor-hipoteca/` y `/guias/amortizacion-anticipada-comisiones/` + índice `/guias/`; respuesta primero, tabla, ejemplo con cifras verificadas contra la calculadora, fuentes BOE/BdE; enlazadas desde las calculadoras de su clúster ("Guías para entenderlo") y entre sí. Cifras de mercado vía `{{euribor_12m}}`/`{{fecha}}` de `data/params.json` | `content/guias/*.html`, `seo.guide_page` | borrar los .html |

Verificación del ciclo: build OK, `ops/check.py decidir` OK, 16 páginas con title ≤ 60 y description ≤ 155, JSON-LD parseable, 0 enlaces internos rotos.

## Cómo se usa IndexNow en el ciclo
Tras cada push a main, **cuando el deploy de GitHub Pages haya terminado** (la clave debe responder 200):
```
cd "/Users/andonimcbpro/Claude Code/autolab" && python3 ops/indexnow.py --all   # primera vez
cd "/Users/andonimcbpro/Claude Code/autolab" && python3 ops/indexnow.py         # ciclos siguientes: solo URLs con lastmod cambiado
```
`--dry-run` muestra qué enviaría. Commitear `ops/.indexnow-state.json` tras enviar.

## Qué medir y cuándo
- **+48-72 h (3-4 oct 2026):** `python3 ops/metrics.py decidir 7` → sitemap procesado (descubiertas/indexadas), primeras páginas con impresiones y sus consultas. En Search Console > Inspección de URL, pedir indexación de home, 5 calculadoras y 2 guías si siguen "descubiertas, no indexadas".
- **+7 días:** consultas con impresiones por página; ¿aparecen consultas informativas (euríbor, comisión amortización) en las guías? Bing Webmaster Tools (si Andoni lo da de alta): URLs indexadas por IndexNow y AI Performance (citas).
- **+28 días:** CTR por página; páginas con impresiones y 0 clics → reescribir title/description. Comparar clics a calculadoras desde guías (GA4, referer interno).
- Registro en "Experimentos y resultados" abajo, con fecha y cifras.

## Siguientes 5 palancas (priorizadas)
1. **Bing Webmaster Tools** (requiere cuenta de Andoni → PENDIENTE-ANDONI): importar desde Search Console; da indexación Bing (base de Copilot/ChatGPT search) y el único informe de citas en IA.
2. **Respuesta corta citable en cada calculadora** (campo `veredicto` en el JSON, 1-2 frases con la regla de decisión y una cifra con fuente) visible arriba y usada en llms-full.txt. Petición al Constructor.
3. **Más guías del clúster hipoteca** con intención informativa y volumen: "gastos de compraventa por comunidad (ITP)", "cuánto dinero necesito para comprar una casa", "hipoteca mixta: cuándo conviene"; cada una enlazada a su calculadora.
4. **Recurso enlazable con datos propios:** "Barómetro mensual de hipotecas" (Euríbor BdE, Euríbor de equilibrio fija/variable del mes calculado con nuestra herramienta). Dato único y fechado = citable por IAs y prensa.
5. **Breadcrumbs visibles + hub `/decidir/hipoteca/`** (página de tema con calculadoras y guías del clúster) y enlace "Guías" en la navegación (petición al Diseñador).

## Experimentos y resultados
- 2026-10-01 · E1 descubrimiento: sitemap lastmod real + IndexNow + clúster + 2 guías. Métrica: URLs indexadas (GSC) y en Bing a 72 h y 7 días. Base: 0/0. Resultado: pendiente.

## Hallazgos del Investigador (2026-10-01)
No se pudo consultar ChatGPT, Perplexity ni AI Overviews directamente desde el agente (sin acceso a esas interfaces); lo siguiente sale de estudios publicados y del SERP observado. Detalle en `journal/competencia.md`.
1. **AIO en finanzas España es casi universal:** aparecen en el 80,9 % de 32.901 keywords financieras; 35 dominios acaparan la mitad de las citas; en **hipotecas los comparadores se llevan el 43,34 %** de las citas (HelpMyCash, Finect, Rankia entre los más citados de su categoría); bancos 25 %, sector público solo 3,85 %; YouTube es el dominio más citado (12,42 %). [SE Ranking, jul-2026](https://seranking.com/es/blog/google-ai-overviews-estudio-finanzas-espana/). → Competimos en la categoría "comparador/herramienta": es la que más cita AIO en nuestro clúster principal.
2. **Las IA no citan lo mismo:** ChatGPT tira de Wikipedia (≈48 % de su top-10), Perplexity de Reddit (≈47 %), AIO más repartido (Reddit, YouTube). [Profound, 680 M de citas, ago-2024 a jun-2025](https://www.tryprofound.com/blog/ai-platform-citation-patterns). Solo ~11 % de dominios coinciden entre ChatGPT y Perplexity ([AuthorityTech 2026](https://authoritytech.io/curated/ai-citation-11-percent-platform-overlap-per-engine-audit-2026)). → No hay una sola táctica GEO.
3. **Estar en el top 10 no garantiza la cita:** análisis 2026 indican que una parte grande de las citas de AIO sale de fuera del top 10 orgánico ([rigolco: 57 %](https://rigolco.com/analisis/citas-aio-57-fuera-top10/); [optimoclick: 38 % desde top 10](https://www.optimoclick.com/blog/actualizacion-el-38-de-las-citas-de-ia-overview-provienen-de-las-10-paginas-principales/)). Lo citado suele ser un bloque autocontenido (<60 palabras), con dato específico, reciente y con fuente ([ighenatt](https://ighenatt.es/recursos/geo/contenido-citable-ai-overviews/)); fuentes secundarias, tratar como orientativo.
4. **Patrón de los competidores citables:** fecha visible y dato del mes (los líderes no lo tienen: iAhorro fija/variable con datos de dic-2024), respuesta en la primera frase, tabla limpia. Ninguno publica un **dato propio** (p. ej. euríbor de equilibrio del mes).
5. **Acciones derivadas:** (a) campo `veredicto` (palanca 2) con una cifra fechada y fuente; (b) Barómetro mensual con datos propios (palanca 4; ver `journal/ideas.md`, idea A); (c) presencia en YouTube/Reddit queda fuera de alcance pasivo, no perseguir ahora; (d) medir citas en Bing AI Performance cuando Andoni dé de alta Bing Webmaster Tools.

## Ciclo 2 (2026-10-01, noche) · E2 Barómetro v1 + enlazado
**Medición previa (`python3 ops/metrics.py decidir 7`, 2026-10-01 23:48 CEST):** sitemap pendiente, 0 descubiertas, 0 indexadas, 0 clics, 0 impresiones; GA4 sin datos. Esperado (sitio de horas). Siguiente lectura: 3-4 oct.

**Hipótesis H4 (GEO, del Investigador):** un dato propio, fechado y reproducible que nadie más publica («Euríbor de equilibrio fija/variable del mes», «coste por km según motor con precios de la fecha», «rentabilidad que hay que batir para que invertir gane a amortizar») es lo único que una IA no puede sintetizar de otra fuente: si nos rastrean, solo pueden citarnos. Bloques autocontenidos <60 palabras, cifra en negrita, fecha visible y fuente.

**Experimento:** `/barometro/` (respuesta corta con 3 cifras arriba → 4 tablas → metodología y fuentes → «cómo citar») + `/barometro/datos.json` (supuestos, tablas, fecha, y la lista de comprobaciones). Schema `Dataset` (con `DataDownload` JSON, `temporalCoverage`, `spatialCoverage` España) + `Article` + `BreadcrumbList`. Enlazado desde: home (bloque «Barómetro de octubre de 2026» antes de «Cómo funciona», insertado en build sin tocar la plantilla), footer, las 3 calculadoras de las que salen los datos («Dato del mes», con la cifra y enlace a su ancla), la guía del Euríbor, llms.txt («Datos propios») y llms-full.txt. Cifras de octubre de 2026: fija 2,60 % vs variable Euríbor 2,10 % + 0,8 → la fija compensa si el Euríbor medio desde el año 2 supera el **1,78 %**; 15.000 km/año × 5 años → gana el **híbrido** (0,36 €/km, 376 € menos que el de gasolina); hipoteca al 3 % → invertir necesita **3,54 %** anual antes del 19 % de impuestos (reduciendo plazo).

**Rigor (cifras = cálculo):** `projects/decidir/barometro.py` porta 1:1 las funciones puras de las 3 calculadoras y toma supuestos de `data/params.json` + defaults de `calcs/<slug>.json`. `ops/check_barometro.py` ejecuta el **JS real** de cada calculadora (osascript) con las mismas entradas: 137/137 cifras coinciden (tol. 0,01), y verifica que `dist/barometro/datos.json` está al día. `ops/check.py decidir` lo llama al final: si el Constructor cambia una fórmula o un default, el check falla hasta reconstruir. Al cambiar `params.json` cada mes, el barómetro se actualiza solo en el build.

**Métrica:** (a) GSC: impresiones/consultas de `/barometro/` («euribor de equilibrio», «a partir de qué euribor compensa la fija», «coste por km coche eléctrico») a 7 y 28 días; (b) Bing AI Performance (citas) cuando Andoni dé de alta BWT; (c) GA4: clics barómetro → calculadoras; (d) prueba manual mensual en ChatGPT/Perplexity con «¿a partir de qué euríbor compensa una hipoteca fija en octubre de 2026?» (registrar si cita entremuchos.com). **Resultado:** pendiente (base 0).

**Enlazado (clústeres):** `seo.build_clusters` ahora suma cercanía entre temas (`NEAR`: energía↔coche/vivienda, hipoteca↔ahorro), normaliza género/número en palabras clave (eléctrico≈eléctrica) y descarta palabras vacías («barato», «mejor»…). Efecto: calefacción (nueva, 7.ª calculadora) enlaza a diésel/eléctrico y alquilar-o-comprar en vez de a hipoteca fija/variable; coche→coche+calefacción en vez de alquilar-o-comprar. Se regenera solo con cada calculadora nueva.

**Hubs /hipoteca/ y /coche/: evaluados, NO creados.** Hipoteca tiene 4 calculadoras + 2 guías y ya existe `/decidir/#hipoteca` (filtro) + clúster denso; coche solo 2 calculadoras: un hub hoy sería una lista con texto de relleno y competiría con `/decidir/` y con el barómetro por las mismas consultas genéricas. Disparador para crearlos: ≥6 páginas propias en el tema **o** GSC muestre consultas genéricas de tema («calculadoras hipoteca») con impresiones en `/decidir/`. Entonces: hub con mapa de decisión («vas a firmar» / «ya tienes hipoteca»), cifras del barómetro y guías.

**Cómo revertir:** en `build.py` quitar `import barometro`, el bloque `BARO = barometro.build(...)`, el `write(barometro.PATH, ...)`, `barometro.calc_link(...)` en `render_calc`, el `seo.insert_before(...)` de la home (volver a `HOME.substitute(cards=cards)`) y `extra=` en `write_llms`; borrar `projects/decidir/barometro.py`, `ops/check_barometro.py` y las 3 líneas finales de `ops/check.py`; quitar `<a href="/barometro/">Barómetro</a>` del footer de `templates/base.html` y la frase final de la nota de `content/guias/euribor-hipoteca.html`. Clústeres: quitar `NEAR`, la normalización de `_tokens` y las palabras añadidas a `_STOP`.

**Siguiente (v2 del barómetro):** archivo histórico mensual (`/barometro/2026-10/` congelado + serie en `datos.json`) en cuanto cambie `params.json` por primera vez; añadir alquilar-o-comprar (años de equilibrio) y calefacción (coste anual por sistema) con su comprobación JS; licencia de los datos (propuesta CC BY 4.0 en PENDIENTE-ANDONI) y nota de prensa/recurso enlazable cuando haya 2 meses de serie.
