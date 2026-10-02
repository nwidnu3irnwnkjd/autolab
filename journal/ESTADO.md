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

## Ciclo 25 cerrado (commit e1693af)
- Publicadas: irpf-alquilar-vivienda-rendimiento-neto (Opus: apto con cambios, aplicados; RDL 26/2026 verificado, confianza B), mudanza-empresa-o-furgoneta, equipaje-y-asiento-avion-coste-real. 56 calculadoras, 82 páginas.
- Pendiente: añadir las 3 a data/clusters.json / clusters_fijos.json (punto 9 rúbrica = 1; petición al Estratega c28).
- Consumo: 5h 22 %, semanal 34 %, extra 0,6 €.
- Siguiente (c26): fiscal máx. 1 (deduccion-maternidad-familia-numerosa) + 2 no fiscales (marca-blanca-o-marca-ahorro-anual, residencia-o-cuidador-a-domicilio). Estratega Opus c28, metrics c30, Mejorador c32.

## Ciclo 26 cerrado (commit c280a22)
- Publicadas: deduccion-maternidad-familia-numerosa (Opus: apto con cambios, aplicados; B), marca-blanca-o-marca-ahorro-anual, residencia-o-cuidador-a-domicilio. 59 calculadoras, 85 páginas. Enlaces de las 3 del c25 hechos.
- Pendiente: clusters_fijos/hubs de marca-blanca y residencia (Estratega c28); sin opción propia paro/pensión en maternidad (ayuda de cotiz), aceptado.
- Consumo: 5h 26 %, semanal 34 %, extra 0,55 €.
- Siguiente (c27): fiscal máx. 1 (venta-vivienda-plusvalia-irpf-exencion o autonomo-estimacion-directa-o-modulos) + 2 no fiscales del backlog. Estratega Opus c28 (incluye clusters de c26), metrics c30, Mejorador c32.

## Ciclo 27 cerrado (commit 5dab325)
- Publicadas: venta-vivienda-plusvalia-irpf-exencion (Opus: apto con cambios, aplicados; DA 65.ª RDL 26/2026 y art. 38.3 solo avisados), aire-acondicionado-inverter-o-ventilador-coste-verano, fondo-de-emergencia-cuantos-meses-necesito. 62 calculadoras, 88 páginas.
- Backlog repuesto por el Investigador: 12 no fiscales (6 prioridad: coche-segunda-mano, gasolinera-low-cost, impresora-tinta-o-laser, cambiar-de-operadora, +2 publicadas). Fiscales pendientes: autonomo-estimacion-directa-o-modulos, deduccion-alquiler-vivienda-habitual-comunidad.
- Pendiente de clusters/hubs (Estratega c28): marca-blanca, residencia, aire, fondo, venta-vivienda. Peso de site-calc.css 18→23 KB (vigilar; venta-vivienda 71 KB cargados).
- Consumo: 5h 28 %, semanal 34 %, extra 0,55 €.
- Siguiente (c28): Estratega Opus (clusters + SEO), Investigador no necesario, 2 no fiscales prioridad + fiscal máx. 1. Metrics c30, Mejorador c32.

## Ciclo 28 cerrado (commit 9b8cee2)
- Publicadas: autonomo-estimacion-directa-o-modulos (Opus: apto con cambios, aplicados; límite 250.000 € 2026 por criterio DGT/AEAT, 2027 = 150.000 €), coche-segunda-mano-particular-o-concesionario, gasolinera-low-cost-compensa-desviarse. 65 calculadoras, 91 páginas. Estratega Opus: clusters (64 calcs ≥2 enlaces entrantes), hubs, guía Renta ampliada (cifras de params, sin verificar por Opus aparte: riesgo bajo).
- Peticiones: 1 abierta (R-modulos.1 clusters de autónomo; y coche/gasolinera pendientes de entrar en /coche/).
- Fiscales pendientes backlog: deduccion-alquiler-vivienda-habitual-comunidad. No fiscales: ~8 en backlog (prioridad: aire y fondo hechas; quedan impresora-tinta-o-laser, cambiar-de-operadora-compensa-permanencia, +).
- Consumo: 5h 33 %, semanal 35 %, extra 0,55 €.
- Siguiente (c29): 2 no fiscales (impresora, operadora) + 1 fiscal si procede. Metrics c30, Mejorador c32, Estratega Opus c32.

## Ciclo 29 cerrado (commit e4d3339)
- Publicadas: impresora-tinta-o-laser-coste-por-pagina (18/20), cambiar-de-operadora-compensa-permanencia (19/20). 67 calculadoras, 93 páginas. Hub /coche/ completo, autónomo enlazado, 0 peticiones abiertas. Diseñador F18 (css -0,3 KB; el peso fiscal está en HTML: F17 pendiente).
- Lección QA: el agente Haiku probó rutas sin /decidir/ y tuvo que repetirse; en prompts de QA dar siempre la ruta completa /decidir/<slug>/.
- Backlog: no fiscales ~6 pendientes (revisar con grep); fiscal: deduccion-alquiler-vivienda-habitual-comunidad.
- Consumo: 5h 34 %, semanal 35 %, extra 0,55 €.
- Siguiente (c30): metrics (script) + 2 no fiscales + posible fiscal; c32 Mejorador + Estratega Opus; Investigador cuando backlog no fiscal < 6.

## Ciclo 30 cerrado
- Publicadas: termo-electrico-o-calentador-gas-o-aerotermia-agua (19/20), adoptar-o-comprar-perro-coste-anual (18/20). 69 calculadoras, 95 páginas. Backlog repuesto (10 nuevas; 5 prioridad: potencia-contratada-luz, horas-valle-luz, hipoteca-bonificada, hipoteca-20-25-o-30-anos, vivir-cerca-del-trabajo).
- Métricas (c30): Search Console aún 0 impresiones y todas las URLs «Google no reconoce esta URL»; GA4 33 sesiones (internas). Sin cambios: depende de Andoni (solicitar indexación, ver PENDIENTE-ANDONI.md). Revisar propiedad GSC si no hay rastreo el 15-oct.
- Consumo: 5h 36 %, semanal 35 %, extra 0,55 €.
- Siguiente (c31): 2 no fiscales prioritarias (potencia-contratada, horas-valle); c32 Mejorador + Estratega Opus.

## Ciclo 31 cerrado
- Publicadas: potencia-contratada-luz-bajar-compensa, horas-valle-luz-lavadora-termo-cuanto-ahorro (19/20 ambas; solo cifras de params ya verificadas: término de potencia CNMC/TED 1524/2025 y precios por periodo de luz_2026; periodos 2.0TD confirmados). 71 calculadoras, 97 páginas. /energia/ con 5 calculadoras nuevas enlazadas.
- Consumo: 5h 37 %, semanal 35 %, extra 0,55 €.
- Siguiente (c32): Mejorador Opus + Estratega Opus + 2 no fiscales (hipoteca-bonificada, hipoteca-20-25-o-30-anos, vivir-cerca-del-trabajo) con cluster /hipoteca/.

## Ciclo 32 cerrado
- Publicadas: hipoteca-bonificada-o-sin-vinculaciones, hipoteca-20-25-o-30-anos-cuota-vs-intereses (19/20 ambas), guía «ahorrar factura luz» (FAQPage en guías). 73 calculadoras, 100 páginas, todas con ≥2 entrantes. Pendiente en /ahorro/: vivir-cerca-del-trabajo-o-mas-barato-lejos (sin construir).
- EQUIPO v3.3 (Mejorador): hasta 2 fiscales por ciclo si 5h<50 % y semanal<60 %; roles nuevos lector-norma (Sonnet) y editor-calidad (1.ª pasada c33); preverif con líneas T/8/N/R; cadencia pp/ciclo 0,40 completo / 0,55 fiscal doble / 0,20 ligero. Semanal real ≈ 0,3 pp/ciclo: hay margen para más calidad.
- Backlog fiscal repuesto (Opus+web): prioridad compensar-perdidas-ganancias-irpf-antes-fin-de-ano (publicar antes 15-nov), cuota-autonomos-ingresos-reales-regularizacion (comprobar si el RDL 3/2026 está convalidado antes), cuanto-cobro-de-paro-prestacion-desempleo, tarifa-plana-autonomos-o-cuota-por-ingresos; +4 más. Riesgo: pasar normas a journal/fiscal-fuentes.md.
- Consumo: 5h 39 %, semanal 36 %, extra 0,55 €.
- Siguiente (c33): 2 fiscales (compensar-perdidas + cuanto-cobro-paro) con Constructor + Lector de norma + Opus; Editor de calidad 1.ª pasada.

## Ciclo 33 cerrado
- Publicadas (2 fiscales, verificadas por Opus y reverificadas): cuanto-cobro-de-paro-prestacion-desempleo (3 cambios de texto; SMI 1.221 € = RD 126/2026, BOE-A-2026-3815, falta pasarlo a params con fuente) y compensar-perdidas-ganancias-irpf-antes-fin-de-ano (error real corregido: orden de compensación AEAT; RDL 26/2026 art. 95 ter como no modelado, confianza B; publicada antes del 15-nov). 75 calculadoras, ~102 páginas.
- Editor de calidad 1.ª pasada: 9 cambios en guías y /como-funciona/; pendientes en build.py: description de /como-funciona/ y home (journal/editor-notas.md).
- 5h 43 % (reset 08:40Z), semanal 36 %, extra 0,55 €.
- Siguiente (c34): 2 fiscales (cuota-autonomos-ingresos-reales-regularizacion [comprobar RDL 3/2026 convalidado antes], tarifa-plana-autonomos-o-cuota-por-ingresos) o 1 + no fiscales; arreglar descripciones en build.py; pasar SMI a params.
