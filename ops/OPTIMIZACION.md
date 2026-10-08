# OPTIMIZACIÓN DE TRÁFICO · pasada 3 · 2026-10-08 (Optimizador, Opus; adelantada por las primeras 10 indexadas)
Manda sobre el resto del plan de tráfico (loop-prompt §53). Medido hoy: journal/inspeccion.json (188 URL, 04:27Z), API de sitemaps y searchAnalytics de GSC (gauth), enlaces internos y tamaño en `projects/decidir/dist`, lastmod de los 7 sitemaps, popularidad.json y comprobación pública de las webs de Andoni. Script de análisis en el scratchpad (no se ha ejecutado nada en el sitio). La pasada 2 queda resumida en el §6.

## 1. Diagnóstico: por qué estas 10 y no las otras 68
**Corrección de la premisa:** no hay URL «rastreadas sin indexar». Las 68 son **«Descubierta: actualmente sin indexar»**, es decir, Google las conoce pero **no las ha rastreado nunca** (`ultimo_rastreo` vacío). Las 110 restantes son «desconocidas». Rastreadas: 10, e indexadas: las 10.
- **Las 10 indexadas son exactamente las 10 de `journal/PEDIR-A-ANDONI-INDEXACION.md`**: home, /noticias/, /datos/, precio-luz-hoy, irav-ipc-alquiler, sueldo-bruto-a-neto-2026, hipoteca-fija-o-variable, la noticia RDL 28-29, /guias/ y /todas/. Las 10 se rastrearon el 7-oct entre las 16:45 y las 16:58Z, una ráfaga de 13 minutos tras la «Solicitar indexación» manual. En 7 días, **ninguna URL que no se haya pedido se ha rastreado**. /guias/, rastreada el 2-oct, también se había pedido. Datos/euribor-hoy no se pidió y sigue en «Descubierta», aunque está a 1 clic de 3 indexadas.
- **Las demás variables no las separan:**
  | Variable | 10 indexadas | 68 descubiertas | 110 desconocidas |
  |---|---|---|---|
  | Tipo | 3 datos, 2 calc., 2 noticias, home, guías, todas | 44 calc., 9 guías, 10 hubs | 67 calc., 18 noticias |
  | Enlaces internos entrantes (mediana) | 112 (enlazadas en el menú o el pie) | 9 | 8 |
  | Tamaño del HTML (mediana) | 20 KB | 31 KB | 29 KB |
  | Sitemap | hubs 4, datos 2, calc. 2, noticias 2 | calc. 43, hubs 10, guías 9 | calc. 67, noticias 18 |
  Las 178 no indexadas están **a 1 clic de una página indexada** (la home enlaza 177 de ellas). El descubrimiento está resuelto y **el enlazado interno no es el cuello de botella**: lo que falta es demanda de rastreo. Las URL más enlazadas coinciden con las pedidas porque se eligieron por valor, no porque ser hub las haya hecho rastrear.
- **Hipótesis contrastables (con fecha):**
  - H1. Hoy Google solo rastrea lo que se le pide; su demanda de rastreo propia para el dominio es casi 0 (dominio de 8 días, 0 enlaces externos y 188 URL de golpe). Contraste: si antes del 15-oct se rastrea **≥ 1 URL no pedida**, ha empezado el rastreo orgánico. Si siguen en 0, se confirma.
  - H2. La calidad no frena, por ahora: 10 de 10 rastreadas están indexadas, y entre ellas hay 2 calculadoras, 1 noticia y 2 de datos. Contraste: si en la siguiente tanda pedida aparece **«Rastreada: actualmente sin indexar» en > 20 %**, hay un problema de unicidad o de patrón de escala, sobre todo en las calculadoras de dilemas menores.
  - H3. Ni el tipo ni el tamaño explican nada; solo la petición. Se contrasta con E7 (§5): URL pedidas frente a URL de control equivalentes.
  - H4. El lastmod pierde valor como señal. **139 de 194 URL de los sitemaps tienen lastmod del 7 o del 8 de octubre**, porque `seo.calc_lastmod` toma la fecha de los ficheros de la plantilla y del cálculo, que tocan los barridos de UX y de calidad. Google usa lastmod solo si es «consistente y verificablemente exacto» (developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap). Con 0 rastreos orgánicos no se puede medir el efecto todavía; es una medida preventiva.
- **Otros datos:** el índice `sitemap.xml` y `feed.xml` están «pendientes» desde el reenvío del 7-oct. Los 7 sitemaps hijos están descargados, aunque `sitemap-calculadoras.xml` solo el 3-oct. GSC da 0 impresiones del 4 al 7 de octubre, y lo normal es que los datos lleguen con 2-3 días de retraso. Las primeras impresiones de las 10 se esperan del 9 al 11 de octubre. popularidad.json: datos insuficientes (82 sesiones, 0 calculadoras con ≥ 5 vistas). No hay ningún enlace externo verificable: la home de etxea.com no enlaza y cotorrita.bar no resuelve en DNS hoy.

## 2. Acciones ordenadas por tráfico ÷ tokens (máximo 8)
| # | Acción | Dueño | Hecho cuando | Métrica | Coste |
|---|---|---|---|---|---|
| 1 | **«Solicitar indexación» de 10 URL nuevas al día durante 5 días** (9-13 oct). Es la única palanca con efecto medido: 10/10 rastreadas en minutos. No se repite ninguna URL (lo que no sirve es repetir, no pedir URL distintas). La cuota diaria (≈ 10) no es pública. **Día 1:** /datos/euribor-hoy/, /tablas-2026/, /decidir/, /barometro/, /que-cambia-1-enero-2027/, /decidir/alquilar-o-comprar/, /decidir/cuanto-cobro-de-paro-prestacion-desempleo/, /decidir/hipoteca-20-25-o-30-anos-cuota-vs-intereses/, /decidir/paga-extra-navidad-cuanto-cobro-neto/ y /decidir/loteria-navidad-premio-neto-hacienda/. **Día 2:** baja-medica-cuanto-cobro-incapacidad-temporal, cuota-autonomos-ingresos-reales-regularizacion, finiquito-baja-voluntaria-vacaciones-preaviso, indemnizacion-despido-objetivo-o-improcedente-neto, jubilarse-en-2026-o-en-2027-edad-y-pension, subsidio-desempleo-cuanto-cobro-y-cuanto-dura, amortizar-o-invertir, luz-fija-o-indexada, /hipoteca/ y /calendario/. **Días 3-5:** el Estratega elige 10 al día por demanda.py, **excluyendo las 10 de control de E7**, y reserva 1 hueco para la noticia del día | Orquestador prepara el texto diario (mismo formato que PEDIR-A-ANDONI-INDEXACION) → Andoni lo pega (2 min) | 50 URL pedidas | Rastreadas en inspect_all: 10 → ≥ 50 el 14-oct. % indexadas/rastreadas (H2) | ≈ 0,01 pp |
| 2 | **Enlace editorial desde las webs reales de Andoni ya rastreadas** (Lavarte, etxea.com y cotorrita.bar cuando resuelva), con los bloques ya escritos en PEDIR-A-ANDONI-ENLACES (a-c). Un solo enlace en el pie o en «Recursos» | Andoni | El enlace se ve en la página pública (lo compruebo con curl) | GSC > Enlaces; primera URL no pedida rastreada | 0 |
| 3 | **Higiene de lastmod:** `calc_lastmod` solo cambia con contenido material (params, cifras, texto del cálculo o live_date que se muestra) y no con cambios de plantilla, CSS ni UX. Hubs y guías: la fecha de su contenido propio. Objetivo: ≤ 15 % de las URL con lastmod de los últimos 2 días cuando no hay cambio de datos | Constructor (Sonnet ≤ 30k) | build + check: el recuento de lastmod recientes baja de 139 a < 30 sin cambio de params | Vuelve a descargarse sitemap-calculadoras (API de sitemaps) | 0,05 pp |
| 4 | **Zenodo + datos.gob.es Aplicaciones** (vías 1 y 3 de ENLACES-vias-adicionales): una ficha que reutiliza datos públicos y un DOI para los CSV de /datos/ y /tablas-2026/ que enlace a las páginas. Son dominios rastreados a diario y dan señal de entidad | Orquestador prepara la ficha y el ZIP → Andoni crea la cuenta y lo sube | Ficha publicada o DOI emitido | Rastreo orgánico de /datos/* y /tablas-2026/ en 14 días | 0,05 pp |
| 5 | **/datos/ citables (OPT2.6, sigue abierta):** respuesta y fecha en la primera frase, tabla del histórico, CSV CC BY y «Cómo citar». Lo necesitan el #4 y E5 | Estratega + Orquestador | Las 3 cumplen | Citas en el panel de IA (E5) | 0,2 pp |
| 6 | **Noticias: 1 al día como máximo, y en la petición de indexación del día.** 23 en el sitemap: 2 indexadas (las 2 pedidas), 3 descubiertas y 18 desconocidas, aunque el sitemap de noticias se descargó el 6-oct. Sin petición, una noticia caduca antes de rastrearse | Orquestador / Redactor | ≤ 1 noticia al día, cada una en la lista del día | Noticias conocidas a 7 días | ahorra ≈ 0,1 pp al día |
| 7 | **Bing y Brave:** con el Claude del navegador de Andoni, confirmar que las 10 del 7-oct se enviaron en BWT y Brave (paso 2-4 del texto). Si se hizo, en adelante enviar a BWT las 10 diarias del #1 en el mismo pegado | Andoni (pegado del #1) | Respuesta de 5 líneas recibida | `site:` en Bing y Brave | 0 |
| 8 | **Revisión de H2 con la primera tanda:** si > 20 % de las pedidas sale «Rastreada: sin indexar», auditar unicidad de esas calculadoras (texto en común con hermanas, valor del ejemplo, intención duplicada) antes de pedir más | Optimizador (Opus ≤ 40k) el 12-oct | Informe de 10 líneas | % indexadas/rastreadas | 0,15 pp si se dispara |

**Qué se descongela y qué no.** Se descongelan: mejoras de contenido material en páginas existentes, /datos/ y una noticia al día. **Siguen congeladas**: calculadoras, guías, tablas, planes y hubs nuevos. **Criterio numérico nuevo para descongelar** (el de «≥ 30 rastreadas» ya no sirve, porque las peticiones manuales lo inflan) — deben cumplirse las tres condiciones en inspect_all:
- (a) ≥ 30 URL rastreadas;
- (b) **≥ 10 de ellas rastreadas sin petición manual** (orgánicas);
- (c) ≥ 80 % de las rastreadas, indexadas.

Si se cumplen, se descongelan 2 páginas nuevas a la semana, solo con demanda medida (demanda.py o consultas de GSC). Si (b) sigue en 0 el 22-oct, el congelado se mantiene y todo el esfuerzo pasa a los enlaces externos.

## 3. Enlaces externos, revisados
- **Realidad hoy: 0 enlaces externos verificables.** Sin ellos no hay rastreo orgánico (H1). Andoni prioriza sus propias webs (PEDIR-A-ANDONI-ENLACES, «orden recomendado» 1) y no quiere cuentas nuevas ni redes. Por eso:
  1. **Webs propias** (#2): coste 0 y dominio ya rastreado. Es lo único que puede activar el rastreo orgánico esta semana.
  2. **Zenodo y datos.gob.es** (#4): necesitan cuenta, pero son institucionales y no comerciales. Es el mejor retorno entre lo que pide alta.
  3. **Un PR único a awesome-web-tools** desde el repo del proyecto: enlace nofollow, pero sirve para descubrir porque GitHub se rastrea a diario. Nada más en GitHub hasta tener E6.
  4. Curlie, LibGuides y Finanzas para Todos: solo con borrador mío y envío de Andoni, después de que haya 30 páginas indexadas, para que el revisor no encuentre un sitio vacío en Google.
- **Descartado:** Show HN, Product Hunt, Uneed, SaaSHub, listas de directorios y Wikipedia/Wikidata. El público no es el nuestro, el enlace es nofollow o de pago, o hay riesgo de patrón artificial (el detalle está en los dos ficheros de enlaces).

## 4. Dejar de hacer (bajo retorno medido)
- **Bloques de enlaces internos nuevos** (tipo E4): las 178 URL ya están a 1 clic de una indexada. E4 se cierra sin efecto: de las 8 enlazadas desde /guias/, solo se rastrearon las pedidas.
- **Barridos de UX y de calidad que tocan plantillas de 112 calculadoras sin cambiar cifras**: no las ve nadie (0 rastreadas) y ensucian el lastmod (#3). Los barridos legales y fiscales con cambio de cifra siguen.
- **Más noticias que una al día y pasadas de titles, descriptions o schema**: 0 impresiones, nada que optimizar. Se retoman con 28 días de GSC.
- **Llenar la cola del modo continuo con pulidos**: si no queda trabajo de esta lista, el ciclo debe ser corto (Vigilante + noticia) y no inventar tareas.

## 5. Experimentos
- **E7 · Petición frente a control (H1/H3).** 50 URL pedidas del 9 al 13 de octubre (#1) frente a 10 de control que no se piden nunca. Control: contado-o-financiar-coche, hipoteca-bonificada-o-sin-vinculaciones, subrogar-hipoteca-merece-la-pena, seguro-vida-hipoteca-banco-o-externo, kilometraje-y-dietas-exentas-irpf, donativos-irpf-cuanto-desgrava-y-cuanto-donar, vivienda-vacia-o-alquilarla-irpf, traspasar-fondo-o-reembolsar-irpf, irpf-alquilar-vivienda-rendimiento-neto y renovar-contrato-alquiler-o-firmar-nuevo-reduccion-irpf. Métrica, con inspect_all diario, el **22-oct**: % rastreadas e indexadas de cada grupo. Lectura:
  - Si el control está a 0 y las pedidas ≥ 80 %, H1 se confirma: se siguen pidiendo 10 al día hasta cubrir el sitemap y todo el esfuerzo va a los enlaces externos.
  - Si el control está > 0, ha empezado el rastreo orgánico y se mira la condición (b) del descongelado.
- **E8 · Enlace externo como disparador.** El día que se vea publicado el primer enlace de una web de Andoni (#2), se anota la fecha. Métrica: días hasta la primera URL no pedida rastreada y número de URL rastreadas orgánicamente en los 14 días siguientes. Comparación: la tasa orgánica previa, que es 0 en 7 días. Fecha de lectura: enlace + 14 días, y como muy tarde el 5-nov.
- E5 (citas en IA de /datos/) sigue en marcha. Su reloj ya ha empezado para irav-ipc-alquiler y precio-luz-hoy (indexadas el 7-oct); se lee el 4-nov. E6 (dataset en GitHub) se queda en espera hasta #5.

## 6. Estado de la pasada 2
Hechas: OPT2.1 (los 7 sitemaps están en GSC; datos y noticias descargados el 5 y el 6 de octubre), OPT2.3, OPT2.4, OPT2.5 y OPT2.7. Abiertas: OPT2.2 (Brave y GitHub), que pasa al #7, y OPT2.6, que pasa al #5. OPT2.8 (congelado) queda **sustituida por el criterio del §2**. Retoques de titles: no se tocan más.

## 7. Herramientas y próxima pasada
`ops/inspect_all.py [--force]` (diario) y `ops/kpis.py`. Pendiente para el Orquestador: añadir a kpis una columna «rastreadas no pedidas», con la lista de pedidas acumulada en `journal/indexacion-pedidas.txt`, para medir la condición (b) y E7 sin LLM. Próxima pasada: el 15-oct (primeras impresiones y H2), o antes si aparece «Rastreada: sin indexar».
