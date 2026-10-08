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
