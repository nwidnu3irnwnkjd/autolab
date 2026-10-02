# Estado del laboratorio (para el director; actualizar cada ciclo)
- Ciclos completados: 24 (cerrado). Sprint 24 h a 120 s hasta ~02-oct 21:00 UTC (ahora ~07:40 CEST). Ciclo 25 (impar): Constructor fiscal (máx. 1: irpf-alquilar-vivienda-rendimiento-neto o deduccion-maternidad-familia-numerosa) con T19 (segundo constructor barato) + no fiscal (2 del backlog); T14 (qa_static --fiscal) del Orquestador cuando haya margen. Estratega Opus c28, Mejorador c32, metrics c30.
- Online: https://entremuchos.com. 53 calculadoras, 8 guías, hubs /hipoteca/ /coche/ /energia/ /impuestos/ /ahorro/, Barómetro v2, feed Atom, Pulso vivo, calendario, actualidad.
- Fiscal: 14 calculadoras fiscales/legales verificadas por Opus (conjunta, pensiones, luz, autónomo, vivienda, depósito, jubilación, paro, ofertas, SL, obligado a declarar, donativos, rescate, placas); más de 40 errores reales cazados; cadena v3.2 (constructor + oráculo propio + Opus + re-verificación). Falsos positivos de QA: 1 en 8 ciclos.
- Calidad: QA con regla de pestañas y script fijo (qa.md v4); 1 falso positivo en 8 ciclos.
- Search Console: 0 indexadas / 0 impresiones a 2-oct 00:30 CEST. Medir de nuevo 3-4 oct (metrics.py cada 6 ciclos).
- Pendiente Andoni (solo identidad/dinero): Bing Webmaster Tools (importar de GSC); regenerar token GitHub; 2FA GitHub y GoDaddy.
- Ideas en cola: hubs /hipoteca/ y /coche/ (solo si aportan), notas por disparador en /actualidad/, informe PDF, proyecto 2 alimentos (Investigador lo recomendó), IA limitada para clientes (Cloudflare, cuando haya tráfico).
- Gasto: extra 0,55 EUR; 5h 20 %; semanal 33 % (02-oct 07:40 CEST). Contexto del orquestador 96 %: compactación inminente (HANDOFF ampliado al final de este archivo). Pendiente Andoni: ver journal/PENDIENTE-ANDONI.md «LO PRIMERO» (incluye CNAME de www para el certificado).

## HANDOFF (si el contexto del orquestador se compacta, lee esto)
- Quién soy: Orquestador del laboratorio autolab (/Users/andonimcbpro/Claude Code/autolab) para Andoni; sesión Sonnet 5.5 con /loop activo (ScheduleWakeup 60-120 s en el sprint). Prompt del bucle: ops/loop-prompt.md; reglas: CLAUDE.md, ops/EQUIPO.md, ops/roles/*.md. Memoria del proyecto: ~/.claude/projects/-Users-andonimcbpro-Claude-Code/memory/ (autolab-proyecto, andoni-preferencias-trabajo).
- Preferencias de Andoni: no revisar nada él, sin informes largos; respuestas breves; solo pedirle lo que requiera su identidad o dinero. Aprobó el gasto hasta 500 € de tokens en 5 días (tope duro del loop: extra 400 € / 100 €/día / semanal 85 %).
- Ciclo: get_usage → lanzar roles en paralelo (Agent con model) → verificar fiscales con Opus (cadena v3.1) → QA Haiku solo navegador (UNA pestaña, cerrarla) → `bash ops/close_cycle.sh N "msg" 5h% sem% extra "roles"` → actualizar ESTADO.md → ScheduleWakeup. Preview local: preview_start name decidir si cae (puerto 8787).
- Credenciales: ~/.config/autolab/github_token y google-sa.json (nunca imprimir). Repo público nwidnu3irnwnkjd/autolab, deploy GitHub Pages en entremuchos.com, refresh diario (Actions 07:15 UTC) hace commit del bot: close_cycle hace pull --rebase.
- Pendiente de Andoni (identidad): Search Console «Solicitar indexación» de https://entremuchos.com/, añadir feed.xml como sitemap, Bing Webmaster Tools; regenerar el token de GitHub; 2FA GitHub/GoDaddy. Google aún no ha pedido robots.txt (día 2); revisar la propiedad en GSC si el 15-oct sigue sin rastreo.
- Siguientes ideas: hub /impuestos/ (necesita ≥ 6 páginas: 2 guías IRPF), guías estacionales (Navidad/Black Friday sin deudas, Renta 2027, coste real de hijos/mascota/coche), 12 calculadoras nuevas en data/backlog.md (journal/ideas.md las prioriza), proyecto 2 (alimentos) solo cuando haya señal; IA limitada para clientes vía Cloudflare cuando haya tráfico; Analista de datos cuando haya ≥ 100 impresiones/semana.

## HANDOFF ampliado (T20, c24)
- Estado en vuelo: ciclo 24 en curso (Estratega Opus lanzado: métricas + auditoría Googlebot + hub ahorro; Mejorador ya recogido). Tras recoger: QA navegador (gimnasio, cocinar-en-casa), `bash ops/close_cycle.sh 24 ...`, actualizar ESTADO, ScheduleWakeup 60-120 s. Fiscal en curso: ninguna.
- Calendario de roles: Estratega Opus c28 (Sonnet en pares), Investigador c28 (o backlog < 6 no fiscales), Mejorador c32, metrics.py c30; Diseñador 1 de cada 3 (último c21 → c24/25).
- Presupuesto: reset semanal 2026-10-06T15:00Z; sprint a 120 s hasta 2026-10-02T21:00Z salvo semanal ≥ 55 % (→ 600 s); después loop-prompt §3.4 (ligero por defecto, 1 de 4 completo); fiscales antes de que el semanal pase del 70 % (~4-oct 16:00Z).
- Recuperar estado en 4 comandos: `git log --oneline -3`; `tail -2 journal/costes.md`; `grep -n '^- \[ \]' ops/requests.md`; `ls -t journal/verificacion-*.md journal/preverif-*.md | head -3`.
- No releer enteros: SEO-GEO.md, requests.md, ideas.md, verificacion-pendiente.md, EQUIPO.md (usar grep/tail).
- Encargo del QA: URL + input a cambiar + texto de aviso a buscar (qa.md v4 hace el resto; máx. 4 capturas, 0 scroll).
- Siguiente tarea de equipo: T14 (qa_static --fiscal), T15 (1 commit por ciclo), T19 (segundo constructor barato) en las 2 próximas fiscales. T20 aplicado.

## ESTADO VIVO (actualizado c49; detalle de ciclos 25-47 en journal/archivo-ciclos-25-47.md)
- 100 calculadoras, 11 guías, /tablas-2026/ (5 páginas de dato propio), ~135 páginas. 5h 59 %→reset 13:40Z, semanal 48 %, extra 0,55 €. Sprint (120 s) hasta ~2026-10-02T21:00Z, pero EQUIPO v3.5 fija 600 s desde c48 (pp real ≈ 0,85/ciclo con fiscal).
- Equipo v3.5: fiscal = Constructor + Opus (+ reverificación Sonnet); fiscal doble suspendida hasta el reset; ciclos alternan fiscal y mantenimiento (Vigilante de normas + Editor + QA); no fiscales solo con `demanda:` del Estratega; qa_static --fiscal informativo.
- RIESGO RDL 26/2026: según prensa rechazado el 2-oct, sin Resolución en el BOE (journal/rdl-26-2026-estado.md, 3 consultas). Al publicarse: Vigilante revisa irpf-alquilar-vivienda-rendimiento-neto (DT 38.ª, 60/70/90 %), venta-vivienda (41 bis.3), notas «R» y /tablas-2026/.
- Search Console: 0 impresiones, sitemap pendiente (día 2). Andoni tiene pasos de indexación/feed/Bing/CNAME www (PENDIENTE-ANDONI.md).
- Fiscales pendientes: paro-autonomos (en curso c48), ayuda-alquiler-joven, jubilacion-parcial, brecha-genero, orfandad, Ley Beckham, deduccion-alquiler-comunidad; tarifa plana APARCADA (sin norma 2026).
- Deuda: R48.1-R48.4 en ops/requests.md (fuentes coche-nuevo/renting, R1/R2 fiscal, peso gzip, ESTADO corto).
- Recuperación: `git log --oneline -3`; `tail -2 journal/costes.md`; `grep -n '^- \[ \]' ops/requests.md`; `ls -t journal/verificacion-*.md | head -3`.

## Ciclo 48 cerrado
- Publicadas: paro-autonomos-cese-actividad-cuanto-cobro (Opus: 5 cambios de texto, ninguno en cifras; 101 calculadoras) y guía «Subir tu sueldo neto…» (12 guías). 5 `demanda:` nuevas no fiscales en backlog: manta eléctrica, lavavajillas, neumáticos de invierno, forfait de esquí, residencia canina.
- Equipo v3.5: cadencia 600 s desde c48 (pp real 0,85/ciclo con fiscal), fiscal doble suspendida, ciclos alternan fiscal y mantenimiento (Vigilante de normas + Editor + QA).
- RDL 26/2026: consulta 3: según Público el Congreso lo rechazó el 2-oct; sin Resolución en BOE. Vigilante lo revisa en c49.
- 5h 2 % (reset 18:40Z), semanal 49 %, extra 0,55 €.
- Siguiente (c49): ciclo de MANTENIMIENTO: Vigilante de normas (BOE RDL + inventario) + R48.1/R48.2 + Editor + QA; ScheduleWakeup 600 s.

## Ciclo 49 cerrado · CAMBIO DE FASE
- Andoni (2-oct): «suficiente contenido y herramientas; viremos a posicionamiento, atractivo interno/externo, funcionalidades, actualidad: todo pensado en TRÁFICO; plan a 2 semanas». Plan en ops/PLAN-TRAFICO.md; loop-prompt tiene la sección «FASE TRÁFICO» (desde c50). Cadencia 600 s.
- c49 (mantenimiento): journal/vigencias.md creado (65 ids BOE; RDL 26/2026 sin Resolución en BOE); R48.1-R48.3 hechas; Editor pasada 4 (36+12 calculadoras revisadas); qa_static mide gzip (0 de 138 páginas > 30 KB).
- 5h 4 %, semanal 49 %, extra 0,55 €.
- Siguiente (c50): arrancar semana 1 del plan: /todas/, sitemaps por secciones, OG por página, titles de las 40 mejores, compartir, .ics, buscador, barra «Esta semana».

## Ciclo 50 cerrado · FASE TRÁFICO, semana 1 (ver ops/PLAN-TRAFICO.md)
- Hecho: /todas/ (directorio con filtro; 63 KB), sitemap.xml como índice + 4 sitemaps por sección, home con «Por situación» y «Novedades», 40 titles/descriptions reescritos (journal/escaparate-c50.md), WebApplication con dateModified/author/publisher, «Actualizado: fecha», 123 imágenes sociales PNG únicas (ops/og_raster.py; si se añade página: ejecutar og_raster y commitear projects/decidir/og/), botón Compartir con #v= y URL actualizada, «Añadir al calendario» (.ics) y eventos GA4 share_click/calc_used/calendar_add.
- Google: sigue sin conocer ninguna URL (inspección: «no reconoce esta URL»); GSC 0 impresiones; sitemap pendiente. Esperar a que Andoni haga la indexación manual.
- 5h 7 %, semanal 50 %, extra 0,55 €.
- Siguiente (c51): semana 1 resto: barra «Esta semana» (BOE/luz/carburantes/Euríbor) diaria, página «Qué cambia el 1-ene-2027», estacionales (Navidad/lotería, Black Friday, calefacción), buscador por situación mejorado, «Plan completo» (R16.4). Vigilante: reconsultar BOE (RDL 26/2026).

## Ciclo 51 cerrado · FASE TRÁFICO
- Hecho: «Esta semana» (semana.py: luz, gasolina, diésel, Euríbor, próximo plazo; datos >7 días se etiquetan), página /que-cambia-1-enero-2027/ (10 filas «pendiente de norma»), calculadora loteria-navidad-premio-neto-hacienda (Opus: 4 cambios menores; 40.000 € exentos por décimo [DA 33.ª, desde 2020 DT 35.ª], 20 % sobre el exceso; prorrateo entre cotitulares literal), evento Sorteo de Navidad 22-dic «por confirmar», 125 imágenes sociales. check_live admite ≤16 eventos.
- Peticiones nuevas: R51.1 (sección «Novedades normativas» en vigencias.md para la tarjeta), R51.2 (luz de mañana en el cron).
- BOE: RDL 26/2026 aún sin Resolución (3.ª consulta del Vigilante, sumario 2-oct). Próxima: sumarios 3-5 oct.
- Al añadir páginas: ejecutar `python3 ops/og_raster.py` y commitear projects/decidir/og/.
- 5h 10 %, semanal 50 %, extra 0,55 €.
- Siguiente (c52): semana 1 resto: estacionales (calefacción de invierno, rebajas, Black Friday check), buscador por situación mejorado, «Plan completo» (R16.4), cuadro de mando de KPIs (metrics.py), borradores de prensa (kit) para semana 2.

## Ciclo 52 cerrado · FASE TRÁFICO
- Hecho: asistente «¿Cuál es tu situación?» (home y /todas/; data/asistente.json, el build falla si un slug no existe; eventos GA4 asistente_paso/resultado), 2 guías (Lotería y Hacienda; Cuánto gasta cada aparato en invierno), kit de prensa en ops/prensa/ (SOLO borradores; Andoni decide si envía), ops/kpis.py → journal/kpis.md (en close_cycle). Home: HOME_N 12→6 por peso (≤60 KB).
- KPIs hoy: 140 URLs en sitemap; 0/12 conocidas por Google; 0 clics/impresiones; GA4 18 sesiones (propias).
- 5h 13 %, semanal 51 %, extra 0,55 €.
- Siguiente (c53): «Plan completo» (R16.4 piloto hipoteca), widget embebible + página «Inserta», vigilar BOE 3-5 oct (RDL 26/2026), revisar KPIs; después fiscal con fecha (retención/Renta no; ver ayuda alquiler joven RD 326/2026).
