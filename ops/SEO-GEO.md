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
