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

## ESTADO VIVO (actualizado c48; detalle de ciclos 25-47 en journal/archivo-ciclos-25-47.md)
- 100 calculadoras, 11 guías, /tablas-2026/ (5 páginas de dato propio), ~135 páginas. 5h 59 %→reset 13:40Z, semanal 48 %, extra 0,55 €. Sprint (120 s) hasta ~2026-10-02T21:00Z, pero EQUIPO v3.5 fija 600 s desde c48 (pp real ≈ 0,85/ciclo con fiscal).
- Equipo v3.5: fiscal = Constructor + Opus (+ reverificación Sonnet); fiscal doble suspendida hasta el reset; ciclos alternan fiscal y mantenimiento (Vigilante de normas + Editor + QA); no fiscales solo con `demanda:` del Estratega; qa_static --fiscal informativo.
- RIESGO RDL 26/2026: según prensa rechazado el 2-oct, sin Resolución en el BOE (journal/rdl-26-2026-estado.md, 3 consultas). Al publicarse: Vigilante revisa irpf-alquilar-vivienda-rendimiento-neto (DT 38.ª, 60/70/90 %), venta-vivienda (41 bis.3), notas «R» y /tablas-2026/.
- Search Console: 0 impresiones, sitemap pendiente (día 2). Andoni tiene pasos de indexación/feed/Bing/CNAME www (PENDIENTE-ANDONI.md).
- Fiscales pendientes: paro-autonomos (en curso c48), ayuda-alquiler-joven, jubilacion-parcial, brecha-genero, orfandad, Ley Beckham, deduccion-alquiler-comunidad; tarifa plana APARCADA (sin norma 2026).
- Deuda: R48.1-R48.4 en ops/requests.md (fuentes coche-nuevo/renting, R1/R2 fiscal, peso gzip, ESTADO corto).
- Recuperación: `git log --oneline -3`; `tail -2 journal/costes.md`; `grep -n '^- \[ \]' ops/requests.md`; `ls -t journal/verificacion-*.md | head -3`.
