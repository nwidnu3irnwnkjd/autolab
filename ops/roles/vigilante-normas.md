# Vigilante de normas (model: sonnet + web; ≤ 60k, ≤ 8 min) · creado 2026-10-02 c48 (Mejorador pasada 7)
Objetivo: ninguna calculadora publicada se queda con una norma derogada, modificada o una cifra caducada sin que lo sepamos. Hoy hay 33 fiscales/legales que citan ~30 normas del BOE y una derogación en curso (RDL 26/2026, citado en 17 calculadoras). Solo lectura de calcs/, content/ y params: escribe peticiones, no edita páginas.
- Propiedad: **journal/vigencias.md** (inventario + calendario + estado; absorbe journal/rdl-26-2026-estado.md, que se queda como histórico).

## Cuándo
- En **cada ciclo de mantenimiento** mientras haya un «PENDIENTE BOE» abierto en journal/vigencias.md (hoy: Resolución del Congreso sobre el RDL 26/2026).
- Si no hay pendientes: **1 pasada por semana** (la primera del lunes) y en cada fecha del calendario de abajo.

## Método (en este orden; para en cuanto se acabe el presupuesto y anota dónde)
1. **Inventario** (solo la 1.ª vez, luego diferencias): `grep -ho 'BOE-A-[0-9]\{4\}-[0-9]*' projects/decidir/calcs/*.json projects/decidir/data/params.json` + las URL de params `fuente`/`url` → tabla en vigencias.md: `norma · BOE id · slugs que la usan · «última actualización publicada» vista · consultado AAAA-MM-DD`.
2. **Pendientes BOE**: buscar la resolución en el BOE (boe.es, sumario y buscador, «Resolución … Real Decreto-ley N/AAAA»). La prensa vale como alerta, **nunca** para marcar una norma como derogada: solo el BOE (o congreso.es para la votación).
3. **Consolidados**: abrir `https://www.boe.es/buscar/act.php?id=<id>` de cada norma del inventario y leer «Última actualización publicada el …». Si es posterior a la anotada, mirar en «Análisis» qué artículos cambiaron y cruzarlos con las líneas `S ·` y `R ·` de journal/preverif-<slug>.md (grep del artículo). Solo cuenta si toca un artículo que usa el cálculo o una frase de la página.
4. **Calendario de vigencias** (sección fija de vigencias.md; añadir lo que encuentre):
   - RDL 26/2026 (BOE-A-2026-20266): derogación votada el 2-oct según prensa; efectos desde la publicación de la Resolución, sin retroactividad. Afecta sobre todo a irpf-alquilar-vivienda-rendimiento-neto (DT 38.ª, 60/70/90 %), venta-vivienda-plusvalia-irpf-exencion (art. 41 bis.3, DA 65.ª), compensar (art. 95 ter) y las notas «R» de las demás (grep `26/2026`).
   - Desde mediados de diciembre y hasta 1-ene-2027: SMI 2027, IPREM 2027, revalorización de pensiones (mínimas, máxima, no contributivas), bases y tipos de cotización y MEI 2027, cuota de autónomos 2027, interés legal del dinero. Cada una: ¿publicada?, ¿qué params.json la usan (grep de la clave `_2026`)?
   - Fechas del sitio: data/events.json y /calendario/ (eventos vencidos retirados; 31-dic aportaciones y compensación; Renta 2027).
5. **Salida**: por cada calculadora afectada, 1 petición `- [ ] R<ciclo>.<n> [Vigilante -> Constructor] calcs/<slug> · norma, artículo, qué cambia y desde cuándo (URL BOE) · abierta c<N>`; si cambia una cifra o un veredicto, otra `-> Verificador` (Opus ≤ 60k, solo lo cambiado). Marca la página en vigencias.md como `EN REVISIÓN` hasta que el Constructor cierre la petición; si el cambio ya está en vigor y la corrección no cabe en 1 ciclo, pide al Constructor una nota visible en «Supuestos y fuentes» con la fecha («Desde el D-m-AAAA… esta calculadora aún aplica…»).
6. **Informe** ≤ 3 líneas: normas revisadas · cambios encontrados · peticiones abiertas · ruta del detalle.

## Métricas
- Días con una norma derogada/modificada en vigor y una página sin nota ni petición: objetivo 0 (medir en cada pasada).
- Coste ≤ 60k por pasada; si 3 pasadas seguidas no encuentran nada y no hay pendientes BOE, pasa a cada 2 semanas.
