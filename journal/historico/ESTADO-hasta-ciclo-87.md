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

## Ciclo 53 cerrado · FASE TRÁFICO
- RDL 26/2026 y 27/2026 DEROGADOS en el BOE (Resolución del Congreso 2-oct, BOE-A-2026-20526; sin retroactividad: rigieron 1-2 oct). Revisadas por constructores y verificadas por Opus: irpf-alquilar (mismos porcentajes 90/70/60/50 de la Ley 12/2023; cambios solo de texto), venta-vivienda (41 bis.3 previo; salvedad de ventas del 1-2 oct), compensar (95 ter ya no existe); 10 calculadoras con nota «revisado c53». El consolidado de LIRPF/RIRPF aparece «Desactualizado» en el BOE: el Vigilante debe releerlo cuando se actualice. El RDL también ampliaba la DA 55.ª (imputación de rentas 1,1 %): ninguna calculadora la modela.
- Widget «Insertar en tu web»: 102 /embed/<slug>/ (noindex,follow, canonical a la completa, pie con enlace) + /inserta/ + bloque en cada calculadora. Desborde móvil 375 px corregido (cabecera en 2 líneas); medición QA con iframes a 375 px (11 URLs ok).
- 5h 17 %, semanal 51 %, extra 0,55 €. Contexto orquestador 84 %.
- Siguiente (c54): «Plan completo» (R16.4), mantenimiento (Vigilante semanal; releer consolidados LIRPF/RIRPF), kpis, posible fiscal con fecha. Esperar indexación de Google.

## Ciclo 54 cerrado · FASE TRÁFICO
- «Plan completo» Compra de vivienda: 4 pasos (cuanto-ahorrar → alquilar-o-comprar → hipoteca 20/25/30 → fija-o-variable), bloque «Paso N de 4» con «Continúa con…» que arrastra precio/entrada/interés por #v=; data/planes.json; /plan/compra-vivienda/ (HowTo+FAQ). Params: menciones del RDL 26/2026 corregidas a «derogado» (R53.1 cerrada). LIRPF/RIRPF consolidados aún sin reflejar la reversión (30/09/2026).
- Lecciones: (1) un QA Haiku puede dar 404/«EM is not defined» si otro agente compila a la vez: repetir sin compilar antes de actuar; (2) tras añadir páginas ejecutar `python3 ops/og_raster.py`.
- 5h 24 %, semanal 53 %, extra 0,55 €. Contexto orquestador 86 % (compacta al 97 %: HANDOFF y PLAN-TRAFICO suficientes).
- Siguiente (c55): ver KPIs (journal/kpis.md); mantenimiento Vigilante; mejoras de engagement: más planes completos (autónomo: cuota → paro → módulos; despido: indemnización → paro → subsidio → trabajo); pendiente humano: indexación.

## Ciclo 55 cerrado · FASE TRÁFICO
- 3 planes completos (/plan/compra-vivienda/, /plan/autonomo/, /plan/despido/) con mapa de ids compartidos en data/planes.json y bloque «Paso N de M».
- 5h 29 %, semanal 54 %, extra 0,55 €. Contexto orquestador 87 %.
- Siguiente (c56): mantenimiento Vigilante (semanal); Mejorador Opus (c56 según EQUIPO v3.5) para revisar el plan de tráfico con KPIs; Estratega Opus: GEO (respuestas citables) y estacionales (Black Friday 27-nov, Navidad); semana 2 del plan desde el 10-oct.

## Ciclo 56 cerrado · CADENCIA POR PRESUPUESTO (EQUIPO v3.6)
- Mejorador: cada ciclo ≈ 0,85 pp semanal porque el contexto del Orquestador es enorme (≈880k): el sprint termina YA. Cadencia: un ciclo cada ~3 h; despertares intermedios (3600 s) = solo `get_usage` y a dormir sin leer archivos ni lanzar agentes (ver loop-prompt §3.4). Alternar tráfico completo/ligero; máx. 15 turnos del Orquestador por ciclo.
- Estratega: GEO en llms.txt (respuesta+cifra+fecha por calculadora, «Datos abiertos», «Cómo citar»), speakable, guía «Antes de fin de año», calendario editorial de 8 semanas y 8 consultas de cola larga (candidatas: paga extra [fiscal ya], plusvalía municipal [verificar tras derogación]).
- Diagnóstico: Google no ha leído ni el sitemap (21 h); la cuenta de servicio es solo lectura (para enviar sitemaps por API: darle «Completo» en Search Console + cambiar SCOPES en ops/gauth.py). journal/PENDIENTE-ANDONI.md «LO PRIMERO» tiene 5 líneas. Plan B 15-oct en journal/ideas-equipo.md.
- 5h 33 %, semanal 54 %, extra 0,55 €. Contexto 88 %.
- Siguiente (c57, ~3 h): T27 (reducir contexto del Orquestador), descubrimiento propio, fiscal paga extra, kpis.

## 2-oct tarde · gestiones online hechas por una sesión de Claude en el navegador de Andoni
- Search Console: indexación solicitada para /, /todas/, /decidir/, /barometro/, /guias/ (todas «se puede indexar», cola prioritaria); enviados feed.xml + 4 sitemaps hijos con URL completa; sitemap.xml ya enviado el 1-oct. La cuenta de servicio autolab-reader pasa a «Completo» y ops/gauth.py usa alcance webmasters (lectura y escritura): la API lista los 6 sitemaps (pendiente, 0 errores, sin descargar aún).
- Bing: entremuchos.com ya estaba en Webmaster Tools; enviado sitemap.xml (Processing, hasta 48 h).
- Pendiente humano: ya ninguno de «LO PRIMERO» (solo opcionales: www en GoDaddy; README del repo con su sí). Sin redes sociales (decisión suya). Titular legal «Editor independiente».
- Seguimiento: kpis.py cada ciclo (URLs conocidas de la muestra de 12); revisar el estado de sitemaps por API (`gauth.get(.../sitemaps)`); si el 6-oct siguen sin descargarse, plan B de journal/ideas-equipo.md.

## 2-oct tarde · GoDaddy y GitHub hechos (sesión de Claude en el navegador de Andoni)
- GitHub: descripción, sitio web y 10 topics del repo público guardados (verificado por API); README público con enlace subido (ac6d96c).
- GoDaddy: SOLO el CNAME www cambiado a nwidnu3irnwnkjd.github.io (19 registros antes y después; A, MX, TXT, SPF, DKIM, DMARC intactos). dig confirma el CNAME en 8.8.8.8; https://www.entremuchos.com aún sin certificado (esperado hasta ~1 h).
- Pendiente de seguimiento: comprobar `curl -sI https://www.entremuchos.com/` (debe dar 200/301 a la versión sin www); si en 2 h sigue sin certificado: en el repo → Settings → Pages, quitar y volver a poner el dominio personalizado (pedir a Andoni que su sesión de navegador lo haga, con su confirmación).
- Ya no queda ningún pendiente humano.

## 2-oct noche · MODO FIN DE SEMANA (ver ops/loop-prompt.md al final)
- Andoni: aprovechar los límites de su plan Claude el fin de semana. Objetivo semanal ≈ 90 % el lunes 5-oct 07:00 CEST; sin gastar extra usage. KPIs (19:00Z): 147 URLs en sitemap, Google reconoce 2 de 12 (primera señal tras la indexación manual), 3 clics/imp.? ver journal/kpis.md.
- Pilar ALQUILER en curso (Estratega Opus c57 investiga LAU/IRAV; luego calculadoras actualizacion-renta-alquiler-irav-ipc, fianza-y-garantias-adicionales-alquiler, gastos-alquiler-quien-paga + guía de cláusulas).
- Contexto del Orquestador 92 %: compactará pronto; tras eso medir pp/ciclo.

## Ciclo 57 cerrado · MODO FIN DE SEMANA (ver final de ops/loop-prompt.md)
- Pilar ALQUILER: guía /guias/clausulas-contrato-alquiler/ y 2 calculadoras verificadas por Opus: actualizacion-renta-alquiler-irav-ipc (regla vigente: sin cláusula no sube; tope IPC; desde el 26-5-2023 límite IRAV [DA 11.ª, confianza B]; IRAV agosto 2,47 %; IPC agosto 4,3 %; actualizar `irav_pct`/IPC en params cuando salgan los de septiembre ~mediados de octubre; el tope del 2 % del RDL 26/2026 NO rige) y fianza-y-garantias-adicionales-alquiler (fianza 1/2 meses; garantía adicional ≤ 2 meses en ≤5 [7 si pj] años; gastos de gestión y formalización siempre del arrendador desde la Ley 12/2023). Falta: gastos-alquiler-quien-paga (backlog), checklist de revisión de contrato y plan completo «Alquilar una vivienda» (planes.json).
- /todas/ ahora 67 KB raw (descripciones en assets/todas-<hash>.json); qa_static bloquea por gzip > 60 KB.
- Google reconoce 2 de 12 URLs (kpis); sitemaps pendientes (0 errores). Fin de semana: objetivo semanal ≈ 90 % el lun 5-oct 07:00 CEST (05:00Z); 5h 10 %, semanal 59 %, extra 0,55 €.
- IMPORTANTE para el siguiente despertar: el contexto del Orquestador se compacta al 97 %: leer ESTADO.md (resumen vivo + este bloque), ops/PLAN-TRAFICO.md, el final de ops/loop-prompt.md (modo fin de semana) y journal/PENDIENTE-ANDONI.md. Medir pp/ciclo en los 2 primeros ciclos tras la compactación y ajustar la cadencia.
- Siguiente (c58): paga extra (fiscal, demanda alta), gastos-alquiler-quien-paga, plan «Alquilar una vivienda», plusvalía municipal (verificar norma), kpis, Vigilante (consolidados LIRPF/RIRPF; cert www).

## Ciclo 58 cerrado · FIN DE SEMANA (contexto del Orquestador tras compactar: ~14 %)
- MEDIDO: c58 completo (doble fiscal + plan + Vigilante + Investigador Opus + 2 Opus) = ~1 pp semanal (59→60). Contexto bajo = ciclo barato. Ritmo permitido ≈0,54 pp/h hasta lun 5-oct 05:00Z; ciclos completos con MÁS agentes (2 fiscales + extra) cada ~25-30 min.
- Publicado: gastos-alquiler-quien-paga (Opus: acuerdo de las partes en 20.2; 5/7 años desde vigencia), paga-extra-navidad-cuanto-cobro-neto, plan /plan/alquilar-vivienda/, hubs enlazados (/hipoteca/ y /impuestos/).
- Vigilante: LIRPF/RIRPF/TRLRHL consolidados SIGUEN sin reflejar la derogación del RDL 26/2026 (reconsultar 5-oct). Plusvalía municipal/IBI descartadas hasta entonces. www.entremuchos.com sin certificado propio aún (GitHub Pages): si sigue el 3-oct, pedir a Andoni (su sesión de navegador) quitar y re-añadir el dominio en Settings→Pages. Sitemaps: hubs y guías leídos (0 indexadas); resto pendientes.
- Backlog fiscal nuevo (Investigador c58, journal/fiscal-fuentes.md «Candidatas c58»): pagas-extra-prorrateadas-o-14-pagas, vivienda-vacia-o-alquilarla-irpf, renovar-contrato-alquiler-o-firmar-nuevo-reduccion-irpf, jubilarse-en-2026-o-en-2027-edad-y-pension, nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad.
- Siguiente c59: 2 fiscales (pagas-extra-prorrateadas + renovar-contrato/ vivienda-vacia) + Opus; checklist «revisa tu contrato de alquiler»; Estratega Opus; Diseñador; enlaces inversos (finiquito, retención → paga extra).

## Ciclo 59 cerrado · FIN DE SEMANA
- Publicado: renovar-contrato-alquiler-o-firmar-nuevo-reduccion-irpf (Opus x2; 60 % solo prórroga arts. 9-10 LAU, tácita reconducción 50 %), pagas-extra-prorrateadas-o-14-pagas (Opus), guía revisa-tu-contrato-de-alquiler-checklist; hubs /hipoteca/ e /impuestos/ enlazados. 108 calculadoras.
- R58.3 falsa alarma: LGSS 270.2 = 70 %/60 % vigente (la API del BOE devuelve todas las versiones del bloque; usar la de fecha_vigencia MÁS ALTA).
- Consumo: c59 ≈ 0,3-0,5 pp semanal (60 %), 5h 20 %. Ritmo para 90 % el lun 5-oct 05:00Z: ≈ 0,55 pp/h → ciclos completos con espera mínima (600 s). Backlog de guías con `demanda:` (Estratega c59): seguros, paga extra diciembre neto, puente/Navidad, cuesta de enero, cambio de hora 25-oct (antes del 20-oct). Palancas de enlaces L1-L5 en ops/SEO-GEO.md «Ciclo 59» (README, WebSub, «Cita esta cifra», Dataset, URLs versionadas).
- Pendiente: live.tipo_hipoteca_fija con 32 días (revisar refresh/BCE), enlaces inversos finiquito/retención → paga extra, 4 peticiones abiertas viejas.
- Siguiente c60: Vigilante (cert www, sitemaps), palancas L1-L3, guías estacionales, calculadoras: vivienda-vacia-o-alquilarla-irpf, jubilarse-2026-o-2027, nomina-2027.

## Ciclo 60 cerrado · FIN DE SEMANA (3-oct)
- Publicado: vivienda-vacia-o-alquilarla-irpf (Opus: DA 55.ª solo rige 2023; en 2026 regla de 10 períodos art. 85.1) y jubilarse-en-2026-o-en-2027-edad-y-pension (Opus: revalorización de enero 2,7 % como HIPÓTESIS en params, demora medida desde la fecha en que se cumplió la edad; fecha de referencia móvil; CADUCA: el Vigilante debe retirarla/rehacerla antes de ene-2027). 110 calculadoras.
- Palancas de enlaces: WebSub (ops/websub_ping.py en close_cycle), bloque «¿Prefieres citarla?» en embed, README público con sección Datos abiertos. Pendientes L2/L3: anclas por cifra en barómetro/tablas y URL congelada /barometro/2026-10/.
- Lección: la API del BOE devuelve TODAS las versiones del bloque; usar la fecha_vigencia más alta (falsa alarma R58.3). Tras derogar RDL 26/2026 el consolidado puede mostrar texto derogado: usar la penúltima versión y citarlo en R.
- Consumo: 5h 26 %, semanal 61 % (c60 ≈ 1 pp; ritmo objetivo 0,57 pp/h hasta lun 5-oct 05:00Z). Contexto del Orquestador 23 %.
- Siguiente c61: Vigilante (cert www, sitemaps, IPC/IRAV), guías estacionales (paga extra diciembre neto, cambio de hora 25-oct, seguros), nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad (fiscal), L2/L3, enlaces inversos.

## Ciclo 61 cerrado · FIN DE SEMANA (3-oct tarde)
- Publicado: nomina-2027-cuanto-sube-la-cotizacion-mei-solidaridad (Opus: la base máxima sube por ley DT 38.ª: la cifra con base 2026 es el mínimo), guías paga-extra-diciembre-neto-retencion y cambio-de-hora-octubre-horas-valle-luz (evento del calendario enlaza). 111 calculadoras. Aviso falso de live.tipo_hipoteca_fija arreglado en qa_static (usa max_edad_dias de live.json).
- DECISIONES DE ANDONI 3-oct: (1) PRIVACIDAD: ningún agente fuera de autolab, sin credenciales (sección en loop-prompt); (2) montar sección de NOTICIAS: plan en ops/PLAN-NOTICIAS.md (formato «Qué cambia para ti», fuentes oficiales, no copiar prensa, 1 pieza/día laborable, tope 3 pp semanales; MVP hasta 10-oct: /noticias/AAAA/mm/slug/, NewsArticle, sitemap news, feed propio, bloque «En las noticias» en calculadoras, max-image-preview:large, política editorial, rol Redactor Sonnet; 5 piezas iniciales); (3) Optimizador de tráfico SEO+IA (ops/roles/optimizador-trafico.md, Opus cada 3 ciclos; primera pasada en curso → ops/OPTIMIZACION.md manda sobre el plan de tráfico).
- Tráfico real: GA4 93 sesiones/52 usuarios (parte propias); Search Console 0 impresiones; 0 URLs indexadas en sitemaps leídos. Revisar 6-oct.
- Consumo: 5h 7 %, semanal 62 %.
- Siguiente c62: ejecutar acciones top de OPTIMIZACION.md; MVP noticias (arquitectura en generador: Diseñador/Constructor técnico + Redactor); Vigilante lunes 5-oct (LIRPF/TRLRHL consolidados); jubilarse caduca antes de ene-2027.

## Ciclo 62 cerrado · 1.ª pasada del Optimizador (ops/OPTIMIZACION.md manda; lee su tabla §3)
- Hecho: #1 titles/H1/descriptions de 75 páginas (mapa journal/titles-2026-10-03.md, demanda journal/demanda-2026-10-03.md; no repetir demanda.py hoy); #2 «Ejemplo resuelto» en 9 insignia (ops/gen_ejemplos.py → data/ejemplos.json → ejemplos.py; cifras fijas con fecha; close_cycle lo regenera); #3 ops/inspect_all.py (URL Inspection de las 161 URL, 1 vez/20 h, journal/inspeccion.json; tarda >10 min: lanzar en segundo plano) — falta integrarlo en kpis.py.
- Congeladas las calculadoras nuevas (salvo bruto→neto) hasta ≥ 50 URLs indexadas; noticias con tope 2/semana; Opus solo si cambia cifra/norma.
- Siguiente (c63): #4 tablas de respuesta numérica con anclas (paro por nómina, dinero para comprar casa, cuota hipoteca, lotería) en páginas existentes; #5 calculadora bruto→neto (Opus ≤40k); #6 páginas de dato persistentes (/datos/irav/, euribor hoy, pvpc) autoactualizadas; #7 barómetro renombrado; MVP noticias técnico (/noticias/…, NewsArticle, max-image-preview:large, política editorial) con 5 piezas; integrar inspect_all en kpis.py.
- Consumo: 5h 9 %, semanal 63 %.

## Ciclo 63 cerrado · NOTICIAS + Optimizador #4-#7 (3-oct tarde)
- Publicado: sueldo-bruto-a-neto-2026 (Opus x2; 112 calculadoras), tablas de respuesta numéricas con anclas (paro por nómina, casa, cuota hipoteca, lotería; ops/gen_tablas_respuesta.py → data/tablas_respuesta.json), páginas permanentes /datos/ (irav-ipc-alquiler, euribor-hoy, precio-luz-hoy; datos.py), Barómetro renombrado, sección /noticias/ (noticias.py, check_noticia.py bloqueante en qa_static, feed, NewsArticle, política editorial, aviso legal con derechos de autor; 7 piezas incl. resumen del día, TUR gas, modelos 3T, cambio de base autónomos, IRAV 14-oct, derogación RDL, Euríbor). IndexNow ahora expande sitemaps hijo (~118 URL/ciclo).
- Orden de Andoni: noticias con más volumen (2-4/día, fines de semana, resumen diario y semanal). Rol: ops/roles/redactor-actualidad.md; cola: ops/noticias/cola.md. Pendiente: ops/triggers.py escribe aún en /actualidad/ (adaptar a content/noticias borradores), KPI de noticias en kpis.py, histórico mensual IRAV con fuente INE, hitos de noticias en events.json (Investigador).
- Inspección real de Google (3-oct 15:27Z): 1 indexada, 57 descubiertas sin indexar, 103 desconocidas de 161 URL. kpis.py ya lee journal/inspeccion.json.
- Consumo: 5h 24 %, semanal 65 % (c63 ≈ 2 pp). Ritmo objetivo 90 % el lun 05:00Z.
- Siguiente (c64): Redactor diario (resumen del día 4-oct, domingo: «La semana en tu bolsillo»), piezas de hechos nuevos del Vigilante; Optimizador pasada 2 (c65); experimentos E1/E2/E3 medición; enlaces inversos; revisar ejemplos/tablas tras cierre.

## Ciclo 64 cerrado · UX, noticias y popularidad (3-oct tarde)
- RDL 25/2026 (BOE-A-2026-20265; carburantes -20/-13/-6 c/l oct-dic, TUR gas con tope +35 % y deuda diferida 2,051412 c€/kWh que paga quien deje la TUR antes del 1-ene-2027, butano 19,55 €, IVA/IEE luz solo con IPC>15 % por subclase): pendiente de convalidación (plazo ~11-nov, sin fecha oficial). Verificación Opus en journal/verificacion-rdl-25-2026.md; avisos aplicados en calculadoras de gas/coche; piezas publicadas (10 noticias). Vigilar convalidación y IPC 14-oct (decide nov) y 13-nov (decide dic).
- UX: Director UX/UI (ops/roles/director-ux-ui.md, Opus cada 4 ciclos; próxima pasada c68) → ops/UX.md; ejecutado UX1.1-1.8 (primer input a ≤593 px en móvil, home 9800→6839 px, sin scroll-reveal ni gráficos diferidos [petición de Andoni], validación accesible, barra móvil A/B ux_var, resultado sticky ≥1024). gtag solo en entremuchos.com; eventos result_view y calc_error (verificar en DebugView producción). Pendiente: cabecera sticky 97 px móvil, deposito-letras-o-fondo-monetario desborda a 375 px, iframes embed lazy.
- Popularidad (orden de Andoni «lo que más gusta, más y más fácil»): ops/popularidad.py → data/popularidad.json con umbral (hoy insuficiente: 38 sesiones); home «Empieza por aquí»; «Otros también usan». Andoni podría activar filtro de tráfico interno en GA4 (opcional).
- ops/triggers.py escribe borradores en content/noticias; kpis con columnas Noticias, res, err. IndexNow expande sitemaps.
- Consumo: 5h 33 %, semanal 67 %.
- Siguiente (c65): Optimizador pasada 2 (resultados E1-E3, indexación inspeccionada), Redactor (resumen domingo + hechos de la cola), arreglar deposito-letras, Vigilante lunes 5-oct (consolidados), seguir el 14-oct.

## Ciclo 65 cerrado · lunes 5-oct noche (bucle retomado tras 2 días parado por cierre de sesión)
- ÓRDENES NUEVAS DE ANDONI (5-oct): sin gasto extra sin permiso; límites de SU usuario; hacerle sitio cuando trabaja (regla CONVIVENCIA en loop-prompt: get_usage + list_sessions antes de cada tanda; no tandas con 5h ≥ 50 %; semanal ≤ 90 %). Memoria: autolab-limites-uso.md.
- Optimizador pasada 2 (ops/OPTIMIZACION.md): Google conoce 63/177 URLs, 1 indexada (/guias/), 113 desconocidas; CAUSA PROPIA: sitemap-noticias y sitemap-datos nunca enviados → enviados el 5-oct por API (PUT sitemaps, 204) junto con sitemap.xml y feeds; sitemap-datos en robots.txt. Congeladas calculadoras/tablas/planes/guías nuevas hasta ≥ 30 URL rastreadas (noticias sí, por orden de Andoni; revisión 17-oct). Experimentos E4 (8 URL enlazadas desde /guias/ vs 8 control), E5 citas IA de /datos/, E6 GitHub datos. OPT1.7 (Brave submit-url, web/temas GitHub) espera el sí de Andoni. Próxima pasada Optimizador 12-oct o al llegar a 10 rastreadas.
- Vigilante pasada 7: consolidados LIRPF/RIRPF/TRLRHL YA reflejan la reversión del RDL 26/2026 (trampa: tomar la ÚLTIMA versión del bloque, no la de fecha_vigencia más alta; arts. 24 y 85 tienen versión 2027 del RDL derogado). Candidatas c65 plusvalía municipal e IBI con literal en fiscal-fuentes.md (congeladas por el Optimizador). RDL 25/2026: sin fecha de convalidación (Pleno 204 semana del 12-oct). www.entremuchos.com ya OK (301).
- Noticias: 13 publicadas (consolidado reversión, resumen del día y de la semana 5-oct). Pendientes menores: actualizar notas de irpf-alquilar-vivienda-rendimiento-neto («a 2/10 el consolidado no reflejaba la reversión»), kpis descubiertas/rastreadas, OPT2.4(b) 2 titles, OPT2.7 botón fuente preferida.
- Consumo: 5h 11 %, semanal 71 % (reset mar 6-oct 15:00Z). Objetivo ≤ 90 % en el reset.
- Siguiente (c66): lo permitido sin calculadoras nuevas: Redactor diario (martes: IPC… no, 14-oct), notas desfasadas de calculadoras con reversión (Constructor), kpis, convalidación RDL 25, actualizar notas R; no tandas si Andoni está activo.

## Ciclo 67 cerrado · martes 6-oct mañana
- Google (inspección 6-oct 05:22Z): conoce 74/181 URLs (63 antes de enviar los sitemaps de noticias/datos), 73 descubiertas sin indexar, 1 indexada, 0 rastreadas nuevas. Sitemaps leídos: datos, feed; noticias pendiente. Seguir: inspect_all en cada ciclo de mañana.
- Hecho: pendientes UX (deposito-letras desborde, cabecera estática en <600 px, iframes embed sin lazy, OPT2.7 enlace «fuentes preferidas» google.com/preferences/source?q=entremuchos.com en noticias). El QA reportó desborde de 5 px en home a 375 px que el Diseñador no reproduce (296 páginas a 375/360/320 sin desborde): falso positivo probable; si el QA vuelve a verlo, anotar el elemento con getBoundingClientRect().right > 375.
- Noticias: 6-oct sin publicar (sin material; «sin relleno»). Dato político: BOE 6-oct RD 806/2026 disuelve las Cortes (elecciones 29-nov): vigilar efecto en convalidación del RDL 25/2026 (Diputación Permanente) y en normas pendientes (SMI, pensiones 2027).
- Consumo: 5h 7 %, semanal 73 % (reset hoy 15:00Z). Regla de convivencia aplicada: usuario libre.
- Siguiente: a las 15:00Z reset semanal; mantener ciclos ligeros/Redactor/Vigilante; Optimizador pasada 3 el 12-oct; Director UX c68+; IPC/IRAV 14-oct.

## Ciclo 70 (6-oct tarde) · SEMANA NUEVA (reset 6-oct 15:00Z; semanal 0 %, próximo reset 13-oct 15:00Z)
- Regla CONVIVENCIA en uso: 6-oct mañana Andoni usó Claude por otro lado (+7 pp en 5h sin agentes míos) → no lancé nada; usuario libre desde las 12:45Z. Los ticks vacíos con contexto de ~600k cuestan ~0,5-1 pp/h: dormir 3600 s y un solo get_usage cuando no haya trabajo.
- Google (inspección 6-oct 15:10Z): conoce 87/182, 86 «descubierta sin indexar», 1 indexada, 0 rastreadas nuevas; la home y /datos/ aún sin conocer. Noticias 9/17 conocidas.
- Hecho: PVPC de mañana en /datos/precio-luz-hoy/ (refresh_data.py clave `manana`; crons 20:30 y 21:30 UTC en refresh.yml pushed OK; sin tokens). Noticia Cortes disueltas/RDL 25/2026 publicada. 14 noticias publicadas.
- Siguiente: IPC/IRAV 14-oct (pieza dato del mes con cifra real tras actualizar params irav_pct/IPC septiembre: Vigilante+Constructor+Opus si cambia fórmula/regla), Optimizador pasada 3 el 12-oct, Director UX pasada 2, inspect_all diario, seguir convalidación RDL 25/2026.

## Ciclo 71 (miércoles 7-oct) · RDL 28/2026 y RDL 29/2026 (BOE nº 249): vivienda y alquiler
- Hecho oficial del día: RDL 29/2026 (BOE-A-2026-20823, en vigor 8-oct) y RDL 28/2026 (BOE-A-2026-20822, en vigor 15-nov), casi idénticos a los 26/27 derogados el 2-oct. Pendientes de convalidación (Cortes disueltas por RD 806/2026, elecciones 29-nov; Diputación Permanente; estimación propia ~18-nov; riesgo alto de derogación; sin efecto retroactivo «en principio»).
- Reglas: tope 2 % (DF 6.ª) para cualquier contrato LAU con aniversario 8-oct-2026→31-dic-2027 (si renta supera el índice, ninguna subida); art. 18.1 IRAV tope en todo caso (también contratos pre-26-5-2023; cláusula sin índice → IRAV); art. 20: IBI no repercutible (basura depende de ordenanza: obligado tributario) para contratos firmados desde el 8-oct (supuesto B); art. 11, 36.5, DF 5.ª; RDL 28: prórroga tácita 5/7, preaviso 6 meses + indemnización; IRPF: reducciones nuevas solo contratos firmados después del 1-12-2026, deducción estatal 10 % alquiler habitual (base < 33.007,20 €, máx 1.163 €), DA 55.ª, 95 ter y 41 bis.3 vuelven.
- Cambios publicados: actualizacion-renta-alquiler-irav-ipc RECONSTRUIDA (Opus x1 + cambios), gastos-alquiler-quien-paga (Opus x1 + 17 cambios), notas con salvedad en fianza, irpf-alquilar, renovar-contrato, vivienda-vacia (opción r12), compensar, traspasar, venta-vivienda; guías clausulas y checklist reescritas; /datos/irav-ipc-alquiler/; noticia 2026-10-07-rdl-28-29 y avisos «Actualización» en 6 noticias previas.
- TRAMPA DE VERSIONES BOE: cuando LAU/LIRPF/TRLRHL/Ley 12/2023 se actualicen, LAU art. 10 tendrá versión RDL 28 (15-nov) como «más alta»; LIRPF arts. 24 y 85 versiones 2027 serán del RDL 29: fijarse en el id de versión. Vigilar convalidación (Diputación Permanente/Pleno) y reconsultar consolidados.
- Fix: datos.py sirve el último dato bueno si el refresco falla (timeout del BCE) → /datos/euribor-hoy/ ya no desaparece.
- Consumo: semanal ~5 %, usuario libre.
- 7-oct 07:53Z inspección Google: conocidas BAJAN a 53/183 (antes 87), 52 «descubierta sin indexar», 5 con estado vacío (¿cuota/errores de API?), 125 desconocidas, 1 indexada. Sin rastreo todavía. Para la pasada 3 del Optimizador (12-oct): ¿Google «olvida» URLs descubiertas por baja prioridad? Plan B: pedir a Andoni que, desde su navegador, solicite indexación de las ~10 URLs mejores (home, /noticias/, /datos/…) y reenvíe sitemaps; y Brave (OPT1.7).
## Resultado de la sesión de navegador de Andoni (7-oct tarde)
- Search Console: 9/10 URL con indexación solicitada (la 7, /decidir/hipoteca-fija-o-variable/, dio error genérico de Google; reintentar mañana); /guias/ ya indexada. sitemap-datos.xml y sitemap-noticias.xml «Correcto» (3 y 17 descubiertas). sitemap.xml y feed.xml «No se ha podido obtener»: el fichero responde 200 y es XML válido, los sitemaps hijos sí se leen → fallo transitorio de GSC; reenviados por API el 7-oct.
- Brave: enviado («Success»). GitHub OK (descripción, web, 10 topics). Bing: faltaba sitemap-noticias → enviado («Processing», 17); 10 URL enviadas (cuota 100/día).
- Pendiente: reintentar solicitud de indexación de /decidir/hipoteca-fija-o-variable/ (otro día); medir con inspect_all el 8-oct si las 9 pasan a «rastreadas».
## Segunda sesión de navegador de Andoni (7-oct noche) — DIAGNÓSTICO DE GOOGLE
- GSC: 1 indexada, 154 «Descubierta: actualmente sin indexar»; hipoteca-fija-o-variable solicitada OK. Rendimiento 28 d: 1 clic, 1 impresión (/guias/). Enlaces: 0 externos, 0 sitios. Rastreo: 6 solicitudes en total (30-sep→5-oct, último 5-oct, 1 solicitud); 67 % 200 y 33 % 404 (probable /favicon.ico y /apple-touch-icon.png → añadidos hoy a static/ y base.html); la mayoría de peticiones del bot de imágenes. sitemap.xml/feed.xml «No se ha podido obtener» (el resto 7 sitemaps Correcto). Bing: 90 URL admitidas (cuota agotada hoy); 0 clics/impresiones; AI Performance 0 citas.
- LECTURA: Google apenas visita el sitio y no tiene señales externas (0 enlaces). El cuello de botella es AUTORIDAD/ENLACES, no técnica. Palancas gratis y legítimas: (1) enlace desde un dominio de Andoni que Google ya rastrea (etxea.com, web de Lavarte u otros): único acelerador fuerte sin redes; (2) repo GitHub (hecho); (3) Brave/Bing (hecho); (4) esperar 2-4 semanas (dominio nuevo). Pasada 3 del Optimizador (12-oct) debe centrarse en estrategia de enlaces legítimos.
## Ciclo 74 (7-oct tarde) · modo continuo
- Opus re-verificó cuanto-cobro-de-paro: correcta (0 cambios; 2 mejoras opcionales: título de la tabla «nómina = base con pagas prorrateadas»; params consulta 7-oct + SMI 1.221 € RD 126/2026). Enlazado interno: mínimo de inlinks 1→4 (31 páginas con párrafo contextual, cabeceras de noticias, home «Últimas noticias»). favicon.ico y apple-touch-icon añadidos. Pendiente de Andoni: enlace desde cotorrita.bar (texto entregado), etxea.com u otra web suya.
## Ciclo 75 (7-oct noche) · UX pasada 2 aplicada
- UX2.1-2.10: barra móvil con el resultado real (variante por sesión), sticky del veredicto solo si cabe, tablas ≤4 col con 1.ª columna fija (Euríbor 3.905→959 px), error al escribir solo tras blur, «Aplicar este caso» en 19 páginas (caso_click), migas sin partir, buscador visible, «Últimas noticias» en la home (DOM = orden visual), etiqueta «Trabajo y prestaciones», tabla de sueldo con «Neto al mes» visible. Peso +≈1,2 KB gz (cacheado). Usa CSS anidado (Chrome 120/Safari 17.2/Firefox 117; fallback tabla con scroll). Pendiente: UX2.11 (grupo en directorio.py), E-UX3 (barra A/B por sesión) y E-UX4 (casos aplicables). Revisión propia a 375 px de 11 páginas: 0 desbordes.
## Ciclo 76 (7-oct noche)
- hipoteca-fija-o-variable reverificada por Opus y corregida: el umbral de equilibrio solo vale con Euríbor ESTABLE (si sube 1→2,95 %: la variable ahorra 7.200 €; si baja 2,95→1 %: cuesta 12.372 € más); input `fijo` desde live.tipo_hipoteca_fija (2,76 %), ejemplo 30.876 € y equilibrio 1,86 %; calcs_loader acepta ok=false dentro de max_edad_dias y avisa si el respaldo de params es antiguo. Editor: pasada 6 (15 calculadoras; FAQs ≤50 palabras). Pendiente Editor→Constructor: calefaccion sin caso de test con defaults; fuentes con fecha en seguro-salud, tren y portátil.
- La luz de mañana (8-oct) aún no estaba publicada por REE a las 21:00 locales: pieza pendiente para mañana (cola.md).
## Ciclo 77 (7-oct noche)
- alquilar-o-comprar reverificada (Opus) y corregida: H1 sin la «N» («a 10, 15 o 20 años»), nota de doble cruce («comprar supera a alquilar entre los años X e Y…»), declarada la deducción estatal 10 % del alquiler del RDL 29 (con ella el ejemplo baja a ≈+9,4k y cruce año 13), sin deducción por compra desde 2013, tope 2 % solo dentro del contrato hasta 31-12-2027. calefaccion: caso de test con defaults (gas 7.612 €; con 0,089 → 8.753 €). Casos típicos en 10 calculadoras más (29/29 coinciden). Pendiente: tren-avion-o-coche (enlace Geoportal sin validar), seguro-salud sin enlace.
## Ciclo 78 (7-oct noche)
- retencion-irpf-nomina-subir-o-no reverificada (Opus, oráculo 1.500 casos 0 disc.) y texto con la deducción estatal 10 % alquiler (RDL 29, solo baja el IRPF final). /todas/ con grupo «Trabajo y prestaciones» (15). Fichero journal/PEDIR-A-ANDONI-ENLACES.md con textos para cotorrita.bar/Lavarte/etxea.com y 8 directorios gratuitos válidos (Curlie, awesome-personal-finance, awesome-web-tools, awesome-calculators, Show HN, Product Hunt, Uneed, SaaSHub). Pendiente: noticia luz del jueves 8-oct (esperar bot 20:30/21:30Z).

## Ciclo 79 (7-oct)
Editor de calidad pasó las 19 guías (lead directo, FAQs ≤50 palabras, títulos con consultas reales). Opus verificó 3 puntos legales: 11 frases corregidas (euribor-hipoteca, clausulas-contrato-alquiler, revisa-tu-contrato checklist, luz x2); Sonnet re-check OK. Build/check/qa_static 0 BLOQUEANTE. Pendiente: noticia luz mañana (REE 0.0), BOE 8-oct, IPC 14-oct.

## Ciclo 80 (7-oct noche)
Opus re-verificó paga-extra-navidad (publicable, 828 casos 0 disc.; R1 aplicado: Orden PJC/297/2026 en params; R2 pendiente: parámetros 2027 con MEI 0,17 a partir de 1-1-2027). Barrido de vigencia: 9 archivos con «pendiente de convalidación» junto al RDL 25. Pendiente tras 14-oct: IRAV 2,47 % (actualizacion-renta-alquiler-irav-ipc l.25 y checklist l.41). Noticia luz 8-oct pendiente (REE).

## Ciclo 81 (7-oct noche)
Casos típicos en 10 calculadoras más (30 en total, 39/39 coinciden con el motor). Director UX pasada 3 (estática): 10 acciones en ops/UX.md (etiquetas largas 522/900, Google Fonts en 190 págs y /privacidad/ no lo dice, coma decimal en 790 campos, botón «Aplicar este caso», CTA en guías). Siguiente: Diseñador ejecuta acciones 1,3,4,2/10. Luz 8-oct aún sin publicar (REE).

## Ciclo 82 (8-oct madrugada)
Noticia «Luz el 8-oct» publicada (media 0,18335 €/kWh, −12,6 %; 14 h barata / 20 h cara; cifras de horas-valle verificada). UX pasada 3 acciones 1,3,4,7: etiquetas cortas + ayuda (522→75 etiquetas >60 car.), campos numéricos inputmode=decimal con coma/miles (em.js normaliza lecturas; resultados idénticos, probado en navegador: 300000 y 2,5), «Aplicar este caso» botón, 13 px mínimo. +≈0,8 KB gz. 0 desbordes a 375 px en 8 páginas. Pendiente UX: 2 y 10 (Google Fonts + /privacidad/; decisión mía: autoalojar o fuente sistema), 5, 6, 8, 9. BOE 8-oct sin leer (resumen del día).

## Ciclo 83 (8-oct madrugada)
Google Fonts eliminado (fuente del sistema; 0 terceros de fuentes), /privacidad/ veraz con el código, CTA «Calcula el tuyo» bajo el lead de 19 guías, Editor de calidad en 19 noticias (lead en resumen del 7-oct, salvedad convalidación). QA propio 375 px: 0 desbordes en 10 páginas. RIESGO ABIERTO: GA4 sin banner y cookies.html incorrecto → cola ítem 10 (prioritario c84).

## Ciclo 84 (8-oct madrugada)
CUMPLIMIENTO COOKIES hecho: banner Aceptar/Rechazar iguales, modo BÁSICO (gtag solo carga tras aceptar; rechazar borra _ga*), elección «1|AAAAMMDD» con renovación a 24 meses, em_uv solo con consentimiento, cookies.html y privacidad.html veraces (sin «IP anonimizada»; base legal consentimiento; transferencia EE. UU. por DPF; conservación 2/14 meses a confirmar en GA4). Opus legal: publicable con cambios, todos aplicados salvo titular (pendiente de Andoni en PENDIENTE-ANDONI.md). Probado en navegador a 375 px. EFECTO: GA4 solo medirá a quien acepte → las visitas en GA4 serán un subconjunto; usar Search Console/Bing para tendencia. Casos típicos: +10 calculadoras (49/49 coinciden; 40 con casos).

## Ciclo 85 (8-oct madrugada)
UX pasada 3 completa (acciones 1-10 salvo 5 ya hecha c83): veredicto del ejemplo con negrita solo en la 1.ª frase y sin nota «ops/verif» pública, content-visibility en /todas/ (buscador y 0 desbordes probados), speculation rules prefetch en home/hubs/guías/todas. Enlazado interno: 61 enlaces contextuales en ~40 páginas, mínimo de inlinks 4→8 en las 15 más débiles (0 huérfanas). Nota: negrita del veredicto de hipoteca-fija-o-variable acaba en coma (cosmético). E-UX5 (medir calc_error/calc_used) en 14 días con consentimiento: ojo, datos solo de quien acepta.

## Ciclo 86 (8-oct madrugada)
Opus reverificó indemnizacion-despido-objetivo-o-improcedente-neto (oráculo 900+22, 0 disc.; norma sin cambios; RDL 25/28/29 no afectan): 1 cambio obligatorio de texto (escenario 3: el veredicto dependía de r.trib, ya no dice «el exceso tributa» cuando tributable=0), conciliación → art. 65.1 LRJS (suspende), coma rota, fecha 8/10; aplicados por Constructor (+20 comprobaciones, caso nuevo en test). Editor pasada 8: 12 calculadoras, 14 FAQs recortadas, 10 a 5/5; tests con defaults en diesel e hipoteca. Pendiente: params.json indemnizacion_despido_2026.fuente aún «consolidado a 30/9/2026» (actualizar en próxima re-verificación). BOE 8-oct sin leer.

## Ciclo 87 (8-oct 03:00)
Vigilante: calendario verificado hasta 29-oct (INE 14/26/27/30-oct, BCE 29-oct, AEAT 3T 20-oct, Ley 4/2026 23-oct, hora 25-oct); congreso.es: sin Pleno semanas 5-11 y 12-18 oct → convalidación RDL 25/28/29 sin fecha oficial (estimaciones ~11/18-nov propias). Cola de noticias completada. Constructor: enlace roto BdE arreglado en euribor-hipoteca, fechas de consulta 8/10 en 3 guías y params indemnización (norma verificada vigente; art. 7 LIRPF modificado el 7-oct solo en ñ). BOE 8-oct aún no publicado a las 02:30 → leer tras 07:00.
