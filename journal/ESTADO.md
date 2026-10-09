# Estado del laboratorio — ciclo 87 (para el director; ≤ 40 líneas; historial hasta c87 en journal/historico/ESTADO-hasta-ciclo-87.md)
- Ciclos hechos: 87. Cada ciclo se añade UNA línea al final (no bloques) y se actualiza «ciclo N» de esta cabecera.
- Cifras: calculadoras 112, guías 19, noticias ~20, páginas 188, comprobaciones 13680. Online: https://entremuchos.com.
- Google: 53 URLs conocidas, 1 rastreada-indexada; 0 enlaces externos; diagnóstico = falta de autoridad.
## Reglas activas
- MODO CONTINUO (ciclos con ≥2 agentes cada 10-15 min); pausa solo 5h ≥ 70 % o semanal ≥ 90 %.
- Congelado de páginas nuevas hasta ≥ 30 URLs rastreadas.
- Privacidad: solo dentro de autolab/; nunca imprimir credenciales.
- Gasto extra ≤ 0,55 € (si > 0,55 € parar).
## Decisiones recientes
- Consentimiento de cookies en modo básico; fuente del sistema; UX pasada 3 hecha.
- «Casos típicos» en 40 calculadoras; enlazado interno mínimo 8.
## Riesgos / pendientes
- RDL 25/28/29 sin convalidar y sin fecha de pleno (sin Pleno 5-18 oct; estimación propia ~11/18-nov).
- 14-oct IPC/IRAV: actualizar irav_pct en actualizacion-renta-alquiler-irav-ipc (l.25) y checklist (l.41).
- jubilarse-en-2026-o-en-2027 caduca antes de ene-2027; paga-extra R2: parámetros 2027.
- Titular legal pendiente de Andoni; GA4 solo mide a quien acepta cookies.
- Pasada 3 del Optimizador el 12-oct; Director UX pasada 4 ~c90.
## Próximos hitos
- BOE 8-oct tras 07:00; 14-oct (INE IPC/IRAV); 20-oct (AEAT 3T); 29-oct (BCE); 30/31-oct.
## Log por ciclo (una línea cada uno)
- c87: ESTADO.md reducido de 240 a ≤ 40 líneas; contenido íntegro archivado en historico/.
- c88 (8-oct 03:30): ESTADO compactado (histórico en journal/historico/); journal/ENLACES-vias-adicionales.md: 11 vías de enlaces legítimas (mejores: datos.gob.es apps, Zenodo; requieren cuenta de Andoni; no se ejecutan sin su OK).
- c89 (8-oct 04:00): Opus reverificó sueldo-bruto-a-neto-2026 (oráculo 724+4 casos, 0 disc.; norma sin cambios; el RDL 29 no toca la retención): textos con la deducción estatal 10 % alquiler (art. 68.6, pendiente de convalidación; no cambia retención, sí Renta; nota «no obligado» ya no empuja a no declarar), aplicados. Casos típicos en 50 calculadoras (59/59). Abierto: Andalucía no releída (API 404).
- c90 (8-oct 05:00): BUG propio c82 corregido (campos decimales: «3.248» se leía como 3248; ahora data-dec por step<1, probado en navegador). UX pasada 4 ejecutada (acciones 2-8: banner sin tapar foco, cifra antes del veredicto, lead sin clamp, CTA guías/noticias, tablas, /todas/ tamaño real). Opus reverificó cuota-autonomos-ingresos-reales-regularizacion (1500 casos 0 disc.): 2 textos obligatorios (rendimiento 0 → Reducida 1 si hay ingresos; pluriactividad solo CC) + 4 recomendados aplicados. LECCIÓN: probar siempre escribir sobre un valor por defecto con decimales tras tocar em.js.
- c91 (8-oct 05:30): Opus reverificó venta-vivienda-plusvalia-irpf-exencion (814 casos 0 disc.): descripción corregida (no calcula plusvalía municipal), DA 65.ª LIRPF (RDL 29, vivienda vacía a entes públicos 8-10-26→31-12-27, pendiente de convalidación), art. 107.4 TRLRHL (coef. 20 años 0,40→0,30 desde 1-12-2026), fechas 8/10; aplicado. Nuevo ops/test_numinput.py bloqueante en check.py (evita repetir el bug de decimales). Avisos: 2 campos con default decimal sin data-dec (capitalizar-paro cuota, nomina-2027 base27) no leen como miles.
- c92 (8-oct 06:00): Casos típicos en 62 calculadoras (71/71). Diseñador: jubilación anticipada 30,6→28,9 KB gz (tabla DT34 reconstruida por interpolación, 960 celdas idénticas) + minify.py general (539 JS, 112 calcs mismo resultado). Corregidos enlaces markdown sin renderizar en 3 calcs de jubilación (sources).
- c93 (8-oct 06:30): Opus reverificó irpf-alquilar-vivienda-rendimiento-neto (810 casos 0 disc.; motor correcto para contratos hasta 1-12-2026): textos con corte DT 38.ª RDL 29 («entre 26-5-2023 y 1-12-2026»; antes de 26-5-2023: 60 %; desde 2-12-2026 sin 90/70/60/50 %), sources/params dejan de afirmar que el consolidado refleja la reversión, 10 % es del inquilino, requisitos 80 % prórroga; aplicado. Casos típicos en 77 calculadoras (86/86). PENDIENTE: 2 casos nuevos propuestos para test.json de esa calculadora (no añadidos).
- c94 (8-oct 06:40): +3 casos de test verificados (irpf-alquilar x2, venta-vivienda x1; 13710 comprobaciones). BOE 8-oct aún 404 a las 06:27.
- c95 (8-oct 07:40): GOOGLE: por 1.ª vez 78 conocidas / 10 rastreadas e indexadas (de 188). Optimizador pasada 3: las 10 son EXACTAMENTE las pedidas a mano el 7-oct; ninguna rastreada orgánicamente en 7 días; las 68 restantes = «descubierta, sin indexar» (no es calidad). Nuevo criterio de descongelado: ≥30 rastreadas + ≥10 orgánicas + ≥80 % indexadas. Acciones: Andoni pide 10 URL/día (textos en journal/PEDIR-A-ANDONI-INDEXACION-DIA1/2.md), enlace desde sus webs (etxea.com no enlaza; cotorrita.bar sin DNS), Zenodo/datos.gob.es. Hecho: lastmod solo por contenido material (data/lastmod.json, 133 URLs aún con 7-8 oct por cambios reales), kpis con columna «rastreadas no pedidas». Congelado: páginas nuevas; barridos de plantilla sin cambio de cifras; ≤1 noticia/día. E7 (50 pedidas vs 10 control) se lee el 22-oct.
- c96 (8-oct 07:50): BOE 8-oct (núm. 250) leído: sin novedades para la web (ni convalidación de RDL 25/28/29 —Cortes disueltas por RD 806/2026, elecciones 29-nov—, ni órdenes de cotización/AEAT/SEPE/Energía). Sin resumen del día (límite ≤1 noticia/día: ya publicada la de la luz).
- c97 (8-oct 09:00): paquete de datos para Zenodo/datos.gob.es preparado en journal/paquete-datos/ (6 CSV, README, fichas, ZIP, ops/gen_paquete_datos.py); falta titular legal y cuentas de Andoni.
- c98 (9-oct 00:10): noticia «Luz el viernes 9-oct» publicada (media 0,18782 €/kWh, +2,4 %; mín 14 h, máx 20 h; salto 18 h). Hoy viernes: «La semana en tu bolsillo» pendiente (no más de 1 noticia/día salvo resumen semanal); Andoni: día 1 de indexación pendiente de pegar (journal/PEDIR-A-ANDONI-INDEXACION-DIA1.md).
- c99 (9-oct 07:50): BOE 9-oct (núm. 251) sin novedades para la web. Publicada «La semana en tu bolsillo» 5-9 oct. Pendiente de Andoni: pegar texto indexación DÍA 1 (hoy) y DÍA 2 (mañana), titular legal, paquete de datos.
- 9-oct: Indexación DÍA 1 hecha por Andoni (10/10 Google y 10/10 Bing). Google: sitemap.xml (índice) figuraba «No se ha podido obtener» pese a 200/XML válido; reenviados por API los 7 sitemaps + feed (204). Lavarte: página enlazada https://www.lavarte.com/content/19-recursos-para-autonomos-y-pymes (200, sin nofollow); falta enlace en el pie. Sin enlaces internos desde lavarte.com hasta entonces.
- 9-oct: Bing día 2 enviado (10/10; cuota 80/100). Google día 2 se pide el 10-oct (cuota Search Console ~10/día, hoy gastada).
- c100 (9-oct 17:00): Opus reverificó incapacidad permanente y viudedad (733+730 casos, 0 disc.; RD 241/2026 coincide): textos con complemento brecha de género no incluido, extinción por nuevo matrimonio con excepciones (art. 223.2), complemento por mínimos como diferencia hasta 9.442 €; aplicado. Preparado el 14-oct: journal/PREP-14-OCT.md (inventario IRAV/IPC, procedimiento, plantillas). test_numinput: excepciones documentadas.
- c101 (9-oct 17:40): Casos típicos en 92 calculadoras (101/101 coinciden); quedan 11 sin ellos.
