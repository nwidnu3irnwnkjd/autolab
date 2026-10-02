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

## Ciclo 34 cerrado
- Publicadas (verificadas Opus, cambios aplicados y reverificados): pension-viudedad-cuanto-cobro (límite del 70 % por edad literal del art. 31.2 Decreto 3158/1966; el 27.034,40 € solo como aviso) y traspasar-fondo-o-reembolsar-irpf (art. 49.1.b: otras ganancias no modeladas, DT 36.ª ETF extranjeros). 77 calculadoras. SMI 2026 en params (smi_2026). Descripción de /como-funciona/ corregida.
- Pregunta de Andoni sobre visitas respondida: GA4 50 sesiones/33 usuarios (internas), GSC 0 impresiones, sitemap pendiente sin descubiertas; acciones para él ya en PENDIENTE-ANDONI.md.
- 5h 48 % (reset 08:40Z), semanal 37 %, extra 0,55 €.
- Fiscales pendientes: cuota-autonomos-ingresos-reales-regularizacion, tarifa-plana-autonomos (comprobar RDL 3/2026 convalidado antes), jubilacion-activa-o-dejar-de-trabajar, retencion-irpf-nomina-subir-o-no, deduccion-alquiler-vivienda-habitual-comunidad.
- Siguiente (c35): con 5h reseteado, 2 fiscales o 1 fiscal + 2 no fiscales (vivir-cerca-del-trabajo etc.); Estratega ligero; c36 Estratega Opus + T24 (páginas de dato propio).

## Ciclo 35 cerrado
- Publicadas: retencion-irpf-nomina-subir-o-no (Opus: 7 cambios, entre ellos el segundo pagador por orden de cuantía art. 96.3.a.1.º), vivir-cerca-del-trabajo-o-mas-barato-lejos, hipoteca-mas-entrada-o-conservar-ahorros (19/20). 80 calculadoras.
- 5h 1 % (reseteado), semanal 38 %, extra 0,55 €.
- Andoni pidió pasos para: indexación home, feed.xml en GSC, Bing Webmaster, CNAME www. Respondido en chat (punto 5 enlaces externos descartado por él).
- Siguiente (c36): Estratega Opus + T24 páginas de dato propio; fiscales: cuota-autonomos y tarifa-plana (comprobar RDL 3/2026), jubilacion-activa, deduccion-alquiler-comunidad.

## Ciclo 36 cerrado
- Publicadas (verificadas Opus, cambios aplicados): jubilacion-activa-o-dejar-de-trabajar (art. 214 tras RDL 11/2024; 2 pasadas Opus; demorar sin cotizar arts. 152/311) y cuota-autonomos-ingresos-reales-regularizacion (RDL 3/2026 convalidado, plazo 30 abril por RDL 14/2022 DF 10.1; publicar antes del 31-dic). 82 calculadoras.
- T24 hecho: /tablas-2026/ + 4 páginas de datos propios (IRPF por CCAA, cuota autónomos, ITP/AJD, SMI/IPREM/paro/pensiones) con CSV/JSON y JSON-LD; revisar y renombrar en enero 2027.
- Andoni recibió pasos para indexación, feed.xml, Bing y CNAME www (sin enlaces externos).
- 5h 8 %, semanal 39 %, extra 0,55 €.
- Fiscales pendientes: tarifa-plana-autonomos-o-cuota-por-ingresos, deduccion-alquiler-vivienda-habitual-comunidad. No fiscales ~7 en backlog.
- Siguiente (c37): 2 no fiscales + tarifa-plana (fiscal); c40 Mejorador + Estratega Opus; metrics c36 (hacer) → siguiente c42.

## Ciclo 37 cerrado
- Publicadas: pc-sobremesa-o-portatil-coste-a-5-anos (18/20), comedor-escolar-o-tupper (19/20). 84 calculadoras.
- tarifa-plana-autonomos APARCADA: el importe de 80 € para 2026 no está en norma vigente (RDL 13/2022 DT 5.ª solo 2023-2025; sin PGE 2026). Retomar si sale norma (pre-verif listo en journal/preverif-tarifa-plana-*.md). Buena aplicación de la regla «sin cifra verificada no se publica».
- Metrics c37: GSC 0 impresiones, sitemap pendiente; GA4 54 sesiones/36 usuarios (internos).
- 5h 10 %, semanal 39 %, extra 0,55 €.
- Fiscales pendientes: deduccion-alquiler-vivienda-habitual-comunidad (necesita tablas por CCAA; considerar Investigador Opus). Reponer fiscales: Investigador cuando <4.
- Siguiente (c38): 2 no fiscales + Investigador fiscal Opus (nuevas fiscales); c40 Mejorador + Estratega Opus.

## Ciclo 38 cerrado
- Publicadas: garaje-comprar-alquilar-o-aparcar-en-la-calle, curso-online-bootcamp-o-fp-coste-y-retorno (19/20). 86 calculadoras.
- Backlog fiscal repuesto por Investigador Opus (artículos leídos hoy en BOE consolidado): prioridad indemnizacion-despido, finiquito-y-vacaciones, baja médica IT (60/75 % confianza C: RD 53/1980), permiso nacimiento 19 semanas (RDL 9/2025 convalidado); +retribución flexible (publicar antes 15-nov), subsidio por desempleo, aceptar trabajo cobrando paro, kilometraje y dietas exentas. Descartadas: plusvalía municipal/IBI (RDL 26/2026 toca arts. 107.4 y 72 TRLRHL), ISD, decesos.
- 5h 12 %, semanal 40 %, extra 0,55 €.
- Siguiente (c39): 2 fiscales (indemnizacion-despido + permiso-nacimiento) con Opus; c40 Mejorador + Estratega Opus.

## Ciclo 39 cerrado
- Publicadas (verificadas Opus; cambios aplicados): indemnizacion-despido-objetivo-o-improcedente-neto (error real: art. 7.e párr. 2 LIRPF exime el objetivo 52.c hasta la cifra del improcedente; selector de causa; 2 pasadas Opus) y permiso-nacimiento-cuanto-cobro-y-como-repartir (acotada a nacimientos desde 31-7-2025: los de 2-8-2024 a 30-7-2025 tienen 16+2 semanas). 88 calculadoras.
- 5h 17 %, semanal 40 %, extra 0,55 €.
- Fiscales pendientes: finiquito-baja-voluntaria-vacaciones-preaviso, baja-medica-cuanto-cobro-incapacidad-temporal (confianza C 60/75 %: RD 53/1980, verificar), retribucion-flexible-me-conviene (antes 15-nov), subsidio-desempleo, aceptar-trabajo-cobrando-paro, kilometraje-y-dietas-exentas-irpf, deduccion-alquiler-comunidad. No fiscales: vacaciones, estufa, gafas, viaje-organizado.
- Siguiente (c40): Mejorador Opus + Estratega Opus + 2 fiscales (retribucion-flexible, finiquito); revisar Mejorador qué reforzar con presupuesto sobrante.

## Ciclo 40 cerrado
- Publicadas (verificadas Opus; cambios aplicados): finiquito-baja-voluntaria-vacaciones-preaviso (crítico: la paga extra pendiente ya cotizó por prorrateo, RGC art. 23.1.A) y retribucion-flexible-me-conviene (crítico: guardería exenta hace perder el incremento de 1.000 € del art. 81.2 LIRPF: veredicto condicional). 90 calculadoras; guía «Me han despedido…» (Estratega Opus). 
- EQUIPO v3.4 (Mejorador): Lector de norma suspendido y sustituido por línea S (supuestos) en preverif; no fiscal 1 por ciclo solo con `demanda:`; Editor en cada ciclo sin fiscal doble con editorial.md; pp/ciclo medido 0,80/0,50/0,25; objetivo semanal 78 %; T14 v3 (`qa_static --fiscal`) a implementar por el Orquestador en el próximo ciclo sin fiscal doble. Medido: 4 de 9 fiscales con error crítico = supuesto de norma sin leer.
- 5h 24 %, semanal 42 %, extra 0,55 €.
- Fiscales pendientes: baja-medica-cuanto-cobro-incapacidad-temporal, subsidio-desempleo-cuanto-cobro-y-cuanto-dura, aceptar-trabajo-cobrando-paro-o-subsidio, kilometraje-y-dietas-exentas-irpf, deduccion-alquiler-comunidad.
- Siguiente (c41): ciclo SIN fiscal doble → implementar T14 v3 (qa_static --fiscal) + 1 fiscal + Editor + 1 no fiscal con demanda.

## Ciclo 41 cerrado
- Publicada: kilometraje-y-dietas-exentas-irpf (Opus: 3 cambios menores; 0,26 €/km = Orden HFP/792/2023, el Reglamento consolidado sigue en 0,19). 91 calculadoras.
- Herramienta: `python3 ops/qa_static.py --fiscal [--changed|--full]` (T14 v3) en close_cycle.sh como paso informativo: 77 avisos sobre 27 fiscales (R1 params sin url/fecha 14, R2 var P sin params 6, R3 literales 22, R4 absolutos 3, R6 preverif sin T/8/N/R/S 27). Deuda a limpiar en ciclos ligeros: R2/R3 (retencion-irpf, declaracion-conjunta).
- Editor: pasada válida sobre 12 calculadoras (journal/editorial.md): leads sin condición 6→2, frases >30 palabras 38→28.
- 5h 32 %, semanal 43 %, extra 0,55 €.
- Fiscales pendientes: baja-medica (confianza C), subsidio-desempleo, aceptar-trabajo-cobrando-paro, deduccion-alquiler-comunidad. No fiscales: vacaciones, estufa, gafas, viaje-organizado (solo con `demanda:` del Estratega).
- Siguiente (c42): metrics + 1 fiscal (subsidio-desempleo) + tarea de mejora (limpiar R2/R3 de fiscales) + Editor.

## Ciclo 42 cerrado
- Publicada: subsidio-desempleo-cuanto-cobro-y-cuanto-dura (Opus: 6 errores; crítico art. 275.5.e [el sueldo/paro que ya no se cobra no cuenta como renta]; cuantía general 95/90/80 % del IPREM [570/540/480 €], 80 % solo mayores de 52 [480 €]). 92 calculadoras, ~126 páginas.
- Nueva /tablas-2026/trabajo-prestaciones/ (5.ª página de dato propio, solo claves A de params).
- Editor 2.ª pasada (12 calculadoras, FAQ >50 palabras 38→0). Pendientes del Editor: fuentes nuevas para coche-nuevo-o-seminuevo y comprar-coche-o-renting (necesitan URL en sources).
- Metrics c42: GSC 0 impresiones/sitemap pendiente; GA4 57 sesiones/39 usuarios (internos).
- Decisión: no refactorizar constantes legales fuera de var P (R2/R3 de qa_static --fiscal) en calculadoras ya verificadas: riesgo > beneficio; solo en calculadoras nuevas.
- 5h 37 %, semanal 44 %, extra 0,55 €.
- Fiscales pendientes: baja-medica (confianza C), aceptar-trabajo-cobrando-paro, deduccion-alquiler-comunidad. Investigador fiscal cuando <3.
- Siguiente (c43): 1 fiscal (aceptar-trabajo-cobrando-paro o baja-medica) + Editor + Estratega ligero; c44 Estratega Opus.

## Ciclo 43 cerrado
- Publicada: aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad (Opus: 5 cambios; crítico: DA 59.ª.4 LGSS [paro > 12 meses reconocido desde 1-4-2025] cambia el CAE del subsidio: select con bloqueo; LISOS 25.4.a/47.1.b rechazo de oferta adecuada). Nota de DA 59.ª.4 añadida al subsidio-desempleo (cuanto-cobro-de-paro sin cambios). 93 calculadoras.
- Editor 3.ª pasada (12 calculadoras, FAQ >50 palabras recortadas).
- 5h 44 % (reset 13:40Z), semanal 45 %, extra 0,55 €.
- Fiscales pendientes: baja-medica (confianza C: RD 53/1980), deduccion-alquiler-comunidad. Reponer (Investigador Opus) en c44.
- Siguiente (c44): Estratega Opus + Investigador fiscal Opus (reponer) + Editor; después del sprint (21:00Z) pasar a cadencia de presupuesto.

## Ciclo 44 cerrado
- Publicado: guía «Autónomo en 2026…» (FAQPage), 4 eventos nuevos en /calendario/ (+ clave `pendientes` con «Fecha por confirmar»), "Guías para entenderlo" en /tablas-2026/. 11 guías, 93 calculadoras.
- Backlog fiscal repuesto (Opus, BOE hoy): prioridad incapacidad permanente, paro de autónomos, ayuda alquiler joven (RD 326/2026), empleada de hogar; +jubilación parcial, brecha de género (36,90 €), orfandad, Ley Beckham; baja médica sube a confianza A. `demanda:` no fiscal (SEO-GEO): radiador de aceite o calefactor, secadora o tendedero, freidora de aire u horno, cuánto cuesta un bebé el primer año.
- RIESGO: RDL 26/2026 votado el 2-oct con el no de PP, Vox y Junts; el BOE aún no publica la resolución. Si se deroga: revisar las calculadoras que lo citan (irpf-alquilar [DT 38.ª y reducciones 60/70/90 %], retención/despido/venta-vivienda como «no modelado», cita de art. 95 ter). Comprobar BOE en c45-c46.
- 5h 47 % (reset 13:40Z), semanal 46 %, extra 0,55 €.
- Siguiente (c45): comprobar estado BOE del RDL 26/2026; 1-2 fiscales (baja-medica, incapacidad permanente) + 1 no fiscal con demanda (secadora o tendedero).

## Ciclo 45 cerrado
- Publicadas: baja-medica-cuanto-cobro-incapacidad-temporal (Opus: 5 cambios; base reguladora literal en Decreto 1646/1972 art. 13; >545 días = prolongación de efectos 174.5), radiador-aceite-calefactor-o-bomba-calor-cuanto-gasta y secadora-o-tendedero-coste-por-lavado (primeras con `demanda:` del Estratega, 19/20). 96 calculadoras.
- RDL 26/2026: convalidación votada el 2-oct (PP, Vox y Junts en contra); resultado NO confirmado, sin resolución en BOE. Ver journal/rdl-26-2026-estado.md. Reconsultar en c46-c47; si se deroga: revisar irpf-alquilar-vivienda-rendimiento-neto (DT 38.ª y 60/70/90 %), venta-vivienda (art. 41 bis.3), notas «R» de otras fiscales y /tablas-2026/.
- 5h 51 % (reset 13:40Z), semanal 46 %, extra 0,55 €.
- Fiscales pendientes: incapacidad-permanente, paro-autonomos-cese, ayuda-alquiler-joven (RD 326/2026), empleada-hogar, jubilacion-parcial, brecha-genero, orfandad, Ley Beckham, deduccion-alquiler-comunidad. No fiscales con demanda: freidora de aire u horno, cuánto cuesta un bebé.
- Siguiente (c46): reconsultar RDL 26/2026 + 1-2 fiscales (incapacidad-permanente, empleada-hogar) + 1 no fiscal con demanda; metrics.

## Ciclo 46 cerrado
- Publicadas: empleada-hogar-cuanto-cuesta-contratar-cotizacion (Opus: 3 cambios menores; tramos/tipos/SMI 9,55 €/h confirmados; el 45 % solo cuidadora exclusiva, DA 3.ª bis RDL 1/2023) y freidora-de-aire-u-horno-cuanto-gasta (demanda #3, 19/20). 98 calculadoras.
- RDL 26/2026: consulta 2 sin resultado confirmado de la votación del 2-oct; BOE consolidado sin derogación; reconsultar en 1-3 días (journal/rdl-26-2026-estado.md).
- 5h 55 % (reset 13:40Z), semanal 47 %, extra 0,55 €.
- Fiscales pendientes: incapacidad-permanente, paro-autonomos-cese, ayuda-alquiler-joven, jubilacion-parcial, brecha-genero, orfandad, Ley Beckham, deduccion-alquiler-comunidad. No fiscal con demanda restante: cuánto cuesta un bebé el primer año.
- Siguiente (c47): Mejorador Opus (c48?) / Estratega Opus c48; c47: 1 fiscal + cuánto-cuesta-un-bebé + reconsulta RDL.
