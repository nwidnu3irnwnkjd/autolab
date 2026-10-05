# OPTIMIZACIÓN DE TRÁFICO · pasada 2 · 2026-10-05 (Optimizador, Opus; sitio online desde el 1-oct)
Manda sobre el resto del plan de tráfico (loop-prompt §53). Mediciones de hoy: `ops/inspect_all.py --force` (177 URL, 21:09Z), `ops/seo_audit.py`, `ops/demanda.py` (29 semillas sin sugerencias), API de GSC (searchAnalytics y sitemaps) y GA4 (Data API) con gauth, y búsquedas públicas `site:` en Brave y Bing. 1 pp ≈ 270k tokens.

## 1. Diagnóstico medido (5-oct)
- **Google no ha rastreado casi nada en 5 días.** Indexada 1 de 177 URL (/guias/, rastreada el 2-oct; las 5 URL con «Solicitar indexación» de Andoni siguen sin rastrear, la home incluida). «Descubierta: sin indexar» 63 (3-oct: 57) y «Google no reconoce» 113. Rastreadas: 1. Por tipo:
  | Tipo | URL | Indexada | Descubierta | Desconocida |
  |---|---|---|---|---|
  | Calculadoras /decidir/ | 112 | 0 | 41 | 71 |
  | Guías | 19 (+índice) | índice | 10 | 9 |
  | Hubs y páginas sueltas (home incl.) | 18 | 0 | 7 | 11 |
  | Tablas 2026 y planes | 10 | 0 | 4 | 6 |
  | Noticias | 12 | 0 | 0 | 12 |
  | Datos (/datos/*) | 4 | 0 | 0 | 4 |
  Lectura: «Descubierta» significa que Google aplazó el rastreo (support.google.com/webmasters/answer/7440203). No ha leído las páginas, así que aún **no hay ningún juicio de calidad**. Lo que entra primero son las URL de los sitemaps que Google ya descargó: calculadoras, guías, hubs y tablas. Noticias y datos son 0/16 conocidas porque **sus sitemaps nunca se han enviado** a GSC. Además, el índice `sitemap.xml` sigue «pendiente», sin ninguna descarga desde el 1-oct (API de sitemaps). Brave: 0 resultados para `site:entremuchos.com`. Bing: ninguna URL del dominio aparece al buscar «entremuchos.com».
- **GSC: 1 impresión y 1 clic en total** (3-oct, /guias/, escritorio, España). No hay consultas visibles, así que **todavía no se puede evaluar ningún title reescrito**. GA4 7 d: 69 sesiones en el dominio (localhost: 8, ya separado gracias a UX1.4). «google / organic» marca 23, pero todas son de móvil en Madrid y entran en / y /politica-ia, mientras GSC solo cuenta 1 clic. Las trato como propias o como redirecciones de google.com, **no como SEO**. popularidad.py: datos insuficientes (0 calculadoras con ≥ 5 vistas).
- **La técnica sigue bien:** 177 indexables = sitemap, 0 títulos ni descriptions duplicados, 0 huérfanas y profundidad máxima de 3. Los «5 rotos» de seo_audit son falsos positivos: son enlaces `data:text/calendar` de las noticias. robots permite CCBot, Bravebot (vía `*`) y los bots de IA. Faltan `sitemap-datos.xml` en robots.txt y el envío de noticias y datos a GSC.
- **Coste frente a resultado:** se han gastado ≈ 67 pp de cuota y hay 0 impresiones reales. Hasta que Google rastree, **cada token que va a URL nuevas tiene un retorno de 0 a corto plazo**. Lo que acelera es lo que hace que Google rastree y lo que hace que otros enlacen.

## 2. Evaluación de lo hecho desde la pasada 1 (evidencia → decisión)
| # | Qué | Estado medido | Decisión |
|---|---|---|---|
| 1 Titles | Hecho (journal/titles-2026-10-03.md). Semillas sin sugerencias: 45 → 29 | Las 29 que quedan son dilemas de baja demanda («comedor escolar o tupper»). **Se cierra el bucle**, salvo 3 retoques (OPT2.4). Sin GSC no hay más que optimizar |
| 2 Ejemplo resuelto | Hecho en las 9 insignia (gen_ejemplos + check) y movido bajo el formulario (UX1.2) | Sigue. Falta la cifra en la meta description (hoy hipoteca-fija no tiene ninguna) → OPT2.3 |
| 3 Medición | Hecho: inspect_all diario sobre todo el sitemap y kpis lee inspeccion.json | Sigue. Añadir a kpis las columnas «descubiertas» y «rastreadas» (OPT2.6) |
| 4 Tablas | Hechas 4: paro `#nomina-*`, hipoteca `#hipoteca-1*`, lotería `#premio-*` y sueldo `#bruto-*`. Casa por precio: no la encuentro en dist | Sigue, pero **ninguna tabla más** hasta tener impresiones (E1 sin empezar) |
| 5 Sueldo neto | Publicada, con title de demanda y tabla | Sigue. Es candidata a enlazarse desde /guias/ (OPT2.2) |
| 6 Datos | 3 páginas vivas (euribor-hoy, irav-ipc-alquiler, precio-luz-hoy), 3-8 enlaces entrantes, **0 conocidas** porque su sitemap no está enviado | Sigue. Arreglar descubrimiento (OPT2.1, 2.2) |
| 7 Barómetro | Title de demanda, pero «(oct 26)» se lee como «26 de octubre» | Corregir a «octubre 2026» (OPT2.4) |
| 8 Brave y GitHub | Sigue esperando el «sí» de Andoni (OPT1.7). Brave confirma 0 páginas | **Sube a #2:** es lo más barato que queda |
| Noticias | 16 en el sitemap y 0 conocidas. Orden de Andoni: más volumen | Se respeta la orden, pero hoy cada pieza tiene alcance 0. Que cada una enlace a una página de datos o calculadora y no cree taxonomías. Revisar el 17-oct con inspección |
| UX | UX1.1-1.8 hechas; el formulario queda a ≤ 593 px en las 112 | No toca tráfico de buscadores. Sin acción mía |
| OPT1.4 | seo_audit no está en close_cycle | Hacer, con el filtro de `data:` (OPT2.5) |

## 3. Qué acelera la indexación de un dominio nuevo, sin dinero ni cuentas (verificado)
- **Google:** rastrear lleva «de días a semanas» y repetir la petición no lo acelera (developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl, act. 10-dic-2025). Los sitemaps son la vía para muchas URL, así que **los que no se envían no cuentan**. Mueller y Splitt (Search Off the Record, 16-jul-2026) dicen que las dudas de calidad sobre el sitio hacen que Google rastree menos, y que una página sin enlaces que apunten a ella baja en la cola. Lo práctico: (1) enviar todos los sitemaps; (2) enlazar desde la única página indexada (/guias/), que Google volverá a rastrear antes que las desconocidas; (3) conseguir enlaces externos desde páginas que Google ya rastrea.
- **Brave:** índice propio, sin consola ni IndexNow; se descubre por search.brave.com/submit-url (sin cuenta) y por la telemetría opcional de su navegador (merj.com/blog/how-brave-search-discovers-new-pages). Hoy tenemos 0 páginas allí.
- **Bing → ChatGPT y Copilot:** IndexNow ya está activo y llega a Bing, Yandex, Seznam, Naver y Yep. Copilot cita según sus «grounding queries»: el informe AI Performance de BWT añadió Intents, Topics y Citation Share el 16-jun-2026 (blogs.bing.com). Una fuente secundaria (2026) calcula que el 87 % de las citas de ChatGPT coinciden con el top 10 de Bing.
- **Common Crawl** (base de muchos LLM) descubre por enlaces, y los dominios nuevos con enlaces pueden entrar en 1-2 meses (fuente secundaria, 2026). Ya permitimos CCBot. Un enlace desde GitHub, que se rastrea a diario, es la vía sin coste.
- **Fuentes preferidas de Google** (developers.google.com/search/docs/appearance/preferred-sources, act. 18-sep-2026): es global para Top Stories y, desde el 27-may-2026, también para AI Overviews y AI Mode. Usa el enlace `https://www.google.com/preferences/source?q=entremuchos.com` y hay botón oficial en español. Google no dice que mejore el ranking, pero quien nos elige ve nuestras piezas marcadas y hace el doble de clics (blog.google, 27-may-2026). Coste casi 0 y solo funciona cuando haya noticias indexadas.
- **Directorios:** solo Curlie, que es humano, gratuito y alimenta OpenWebSearch.eu. Pide un formulario con correo, así que necesita el «sí» de Andoni, y su impacto es bajo. Las listas de «500 directorios» son spam de enlaces: no.
- **Citas de IA, estado del arte:** solo ≈ 11 % de los dominios citados coinciden entre ChatGPT y Perplexity. Perplexity favorece contenido de menos de 30 días; ChatGPT, el de Bing (estudios secundarios de 2026, a tomar con cautela). La evidencia experimental sigue siendo la del paper GEO (KDD 2024): cifras con fuente y citas literales. Mito vigente: «el schema FAQ da +40 % de citas» circula en blogs de 2026 sin método; Ahrefs (may-2026) no encontró efecto. **No se toca el schema.**

## 4. Lista priorizada nueva (impacto ÷ coste). El Orquestador delega 1-4 antes que nada
| # | Acción | Dueño | Hecho cuando | Métrica | Coste |
|---|---|---|---|---|---|
| 1 | **Enviar a GSC** `sitemap-noticias.xml` y `sitemap-datos.xml`, y reenviar `sitemap.xml`, con la API (PUT webmasters/v3/sitemaps; gauth ya tiene el scope `webmasters`). Añadir `Sitemap: …/sitemap-datos.xml` a robots.txt | Orquestador (sin LLM) | La API lista 8 sitemaps, con lastDownloaded en noticias y datos | Noticias y datos conocidas > 0 en inspect_all a los 7 días | 0,02 pp |
| 2 | **Brave submit-url** con la home y **web y temas del repo de GitHub** (OPT1.7). Volver a pedir el «sí» de Andoni en una sola línea | Orquestador → Andoni | Hecho o descartado | Resultados de `site:` en Brave a los 7 días; GSC > Enlaces | 0,01 pp |
| 3 | **Puerta desde la página indexada:** en /guias/, bloque «Datos al día y calculadoras más buscadas» con 8 enlaces: /datos/euribor-hoy/, /datos/irav-ipc-alquiler/, /datos/precio-luz-hoy/, sueldo-bruto-a-neto-2026, hipoteca-fija-o-variable, alquilar-o-comprar, cuanto-cobro-de-paro y hipoteca-20-25-o-30. Es E4 | Estratega (Sonnet ≤ 20k) | Los 8 enlaces están en /guias/ en producción | Días hasta «rastreada» de los 8 frente al control | 0,05 pp |
| 4 | **Cifra en la meta description** de las 9 insignia y de las 3 páginas de datos, tomada del ejemplo resuelto o de live.json, con mes y año («Con 150.000 € a 25 años la fija sale X € más cara si…, oct-2026») | Estratega + build | seo_audit: 12/12 descriptions con cifra en € o % | CTR en GSC cuando haya impresiones | 0,1 pp |
| 5 | **Página de datos como respuesta citable:** en las 3 /datos/, primera frase con respuesta y fecha, tabla HTML del histórico, CSV o JSON descargable (CC BY) y «Cómo citar». Es E5 | Estratega + Orquestador | Las 3 cumplen | Citas en el panel de 10 preguntas y en Bing AI Performance | 0,2 pp |
| 6 | **Dataset abierto en el repo de GitHub** (cuenta del proyecto, no de Andoni): carpeta `datos/` con los CSV de euríbor, IRAV y tablas 2026, y un README con «Cómo citar» que enlace a cada /datos/. Es E6 | Orquestador | Publicado en el repo | GSC > Enlaces (github.com); Common Crawl index a los 60 días | 0,05 pp |
| 7 | Botón **«Añádenos como fuente preferida en Google»** (enlace oficial, botón en español) en /noticias/ y en el pie de las piezas | Diseñador | Visible en /noticias/ | — (señal a futuro) | 0,02 pp |
| 8 | Retoques finales de titles: barómetro «(octubre 2026)»; «Hipoteca a 30 años, 25 o 20: cuota e intereses»; «Dietas exentas IRPF 2026 y kilometraje (0,26 €/km)». **Después, ninguna pasada más de titles** hasta tener datos de GSC | Estratega | demanda.py sin esas 3 | Impresiones por página a 28 días | 0,03 pp |
| 9 | seo_audit ignora los href `data:` y entra en close_cycle como aviso (OPT1.4). kpis.py añade las columnas «descubiertas» y «rastreadas» | Orquestador | Fila nueva en kpis.md | — | 0,02 pp |
| 10 | Opcional, con el «sí» de Andoni: Curlie (formulario con correo). Él decide si dedica 5 minutos a «Solicitar indexación» de 10 URL al día; no es necesario | Andoni | — | — | 0 |

## 5. Dejar de hacer (o seguir sin hacer)
- **No hay calculadoras, tablas, planes ni guías nuevas hasta que haya ≥ 30 URL rastreadas.** Siguen con 0 alcance y engordan el patrón de escala que preocupa a Google. Excepción: un cambio legal que afecte a una calculadora que ya existe.
- **No hay más pasadas de titles, schema, llms.txt ni Speakable.** Sin impresiones no hay señal que optimizar.
- **Noticias:** la orden de volumen es de Andoni y se respeta. Lo que cambia es que cada pieza enlace a una página de datos o calculadora, que no se creen archivos mensuales ni de tema, y que se mida el 17-oct (≥ 50 % conocidas a 7 días, o se recorta según PLAN-NOTICIAS §5).
- **No pedir el reindexado una y otra vez**, no pagar «indexadores», no usar listas de directorios ni pings masivos.
- **Los experimentos E1-E3 siguen pausados:** su reloj empieza al indexarse, no al publicarse.

## 6. Experimentos (hipótesis medible y barata)
- **E4 · Puerta desde la página indexada (#3).** Hipótesis: las 8 URL enlazadas desde /guias/ llegan a «rastreada» una mediana de ≥ 5 días antes que 8 calculadoras de control que no llevan ese enlace (paro-autónomos, baja médica, finiquito, subsidio, contado-o-financiar, hipoteca bonificada, subrogar y seguro todo riesgo). Medición: inspect_all diario, comparando la fecha de `ultimo_rastreo`. Si no gana a los 21 días, el enlazado interno no es la palanca y todo se pone en los enlaces externos (#2, #6).
- **E5 · Página de datos que se cita (#5).** Hipótesis: a 28 días de indexarse, /datos/euribor-hoy/ o irav-ipc-alquiler aparecen citadas en ≥ 2 de las 10 preguntas fijas («euríbor hoy», «IRAV septiembre 2026»…) en Perplexity, ChatGPT sin sesión o Bing Copilot, frente a 0 de las calculadoras equivalentes. Registro el día 1 y el 15 de cada mes en SEO-GEO.md.
- **E6 · El dataset en GitHub como vía de descubrimiento (#6).** Hipótesis: en 21 días GSC > Enlaces muestra github.com como dominio que enlaza y las 3 /datos/ pasan de «desconocida» a «descubierta» antes que las noticias del mismo día. Si en 60 días Common Crawl no tiene ninguna URL del dominio, se descarta como vía hacia los LLM.

## 7. Herramientas
- `ops/inspect_all.py [--force]` (diario) → journal/inspeccion.json. Desglose por tipo: agrupar por el primer segmento de la ruta, como en la tabla del §1.
- `ops/seo_audit.py decidir` y `ops/demanda.py decidir --out f` (1 vez al día como máximo). Comprobar si ya hay impresiones: GSC searchAnalytics con `dataState: all` por fecha y página.
- Próxima pasada: el 12-oct o en cuanto inspect_all dé ≥ 10 rastreadas. Ese día mido E4 y las primeras consultas por title.
