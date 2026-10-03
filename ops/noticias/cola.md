# Cola de hechos para Noticias
Alta: Vigilante (hechos oficiales), `ops/triggers.py` y calendario `data/events.json` (`"noticia": true`). Salida: el Redactor de actualidad toma 1-3 líneas por tanda y escribe `content/noticias/AAAA-MM-DD-slug.html` (estado `borrador`); al publicarse la línea pasa a `[x]` con la ruta.
Formato (una línea por hecho): `- [ ] fecha · tipo · hecho · URL oficial · calcs · prioridad`
- fecha = fecha del hecho en el documento oficial (AAAA-MM-DD). tipo = alerta | dato-mes | cuenta-atras | explicador | resumen-dia | resumen-semana.
- URL = documento oficial exacto (BOE-A-…, nota INE, serie BCE, sede AEAT); nunca prensa (la prensa solo sirve de alerta para buscar el documento).
- calcs = slugs de calculadoras separados por coma (los que cambian de cifra). prioridad = alta | media | baja (alta: cambia una cifra ya publicada; sin hecho oficial + cifra propia no hay pieza).
Reglas: más de una pieza al día y también fines de semana si hay hechos; sin hechos no se rellena (el resumen del día lista plazos próximos). Seguimiento de indexación a 2 y 6 semanas; si la mayoría sale «Rastreada: sin indexar», recorte automático (PLAN-NOTICIAS §5).

## Pendientes
- [ ] 2026-10-29 · dato-mes · Decisión de tipos del BCE (jueves) y efecto en la hipoteca variable · https://www.ecb.europa.eu/press/govcdec/mopo/html/index.en.html · hipoteca-fija-o-variable · media
- [ ] 2026-10-09 · resumen-semana · «La semana en tu bolsillo» del 5 al 9 de octubre (viernes): hechos oficiales de la semana con enlace a su pieza · https://www.boe.es/ · actualizacion-renta-alquiler-irav-ipc · alta

- [ ] 2026-10-14 · dato-mes · IRAV y IPC de septiembre (INE, calendario: 14-oct): publicar la cifra real y actualizar la cuenta atrás con modified real · https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177110&idp=1254735976607&menu=ultiDatos · actualizacion-renta-alquiler-irav-ipc · alta
- [ ] 2026-10-23 · alerta · Entrada en vigor de la Ley 4/2026 (discapacidad y dependencia; 20 días tras el BOE del 3-oct) y DF 8.ª (art. 7.x LIRPF); sin cifra propia salvo que una calculadora la use: valorar · https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20528 · - · baja
- [ ] 2026-10-29 · dato-mes · IPC adelantado de octubre (INE; fecha por confirmar en el calendario del INE antes de publicar) · https://www.ine.es/dynt3/Calendario/calenHTML.htm · hipoteca-fija-o-variable · baja
- [ ] 2026-10-30 · cuenta-atras · Última semana de plazo de cambio de base (31-oct) ; el INE publica el avance del PIB del 3T el 30-oct (calendario) · https://www.ine.es/ · cuota-autonomos-ingresos-reales-regularizacion · media
- [ ] 2026-11-02 · dato-mes · Tipos hipotecarios oficiales de octubre (BdE, BOE de primeros de noviembre; fecha por confirmar) · https://www.boe.es/ · hipoteca-fija-o-variable · media


## Hechas
- [x] 2026-10-02 · alerta · Derogación de los RDL 26/2026 y 27/2026 (Resoluciones del Congreso) · https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20526 · actualizacion-renta-alquiler-irav-ipc, irpf-alquilar-vivienda-rendimiento-neto · alta → content/noticias/2026-10-03-derogados-rdl-26-27-2026-alquiler-irpf.html
- [x] 2026-09-30 · dato-mes · Euríbor 12 meses de septiembre (BCE), migrada de /actualidad/ · https://data.ecb.europa.eu/data/datasets/FM/FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA · hipoteca-fija-o-variable, amortizar-plazo-o-cuota · alta → content/noticias/2026-09-30-euribor-sube-2026-09.html
- [x] 2026-10-20 · cuenta-atras · Fin del plazo de los modelos trimestrales del 3T (AEAT); publicar el 10 y el 17 de octubre · https://sede.agenciatributaria.gob.es/ · cuota-autonomos-ingresos-reales-regularizacion · alta → projects/decidir/content/noticias/2026-10-03-modelos-3t-plazo-20-octubre.html (publicar el 10 y el 17 sigue pendiente: actualizar sin repetir)
- [x] 2026-10-31 · cuenta-atras · Plazo de cambio de base de cotización de autónomos (events.json «autonomo-cambio-base»); publicar el 21 y el 28 de octubre · https://www.seg-social.es/ · cuota-autonomos-ingresos-reales-regularizacion · alta → projects/decidir/content/noticias/2026-10-03-cambio-base-autonomo-31-octubre.html
- [x] 2026-10-14 · dato-mes · IPC e IRAV de septiembre (INE; IRAV con efectos en el alquiler de noviembre) · https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177110&idp=1254735976607&menu=ultiDatos · actualizacion-renta-alquiler-irav-ipc · alta → projects/decidir/content/noticias/2026-10-03-irav-ipc-septiembre-14-octubre.html (cuenta atrás; el dato-mes real sigue pendiente el 14-oct)
- [x] 2026-10-01 · alerta · TUR del gas desde el 1-oct (BOE-A-2026-20389) · https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-20389 · calefaccion-gas-aerotermia-electrica · alta → projects/decidir/content/noticias/2026-10-03-tur-gas-octubre-2026.html
- [x] 2026-10-03 · resumen-dia · «Lo que importa hoy» del 3-oct · https://www.boe.es/boe/dias/2026/10/03/ · varias · alta → projects/decidir/content/noticias/2026-10-03-resumen-2026-10-03.html
