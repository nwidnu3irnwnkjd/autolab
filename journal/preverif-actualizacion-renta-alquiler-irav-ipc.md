# Pre-verificación · actualizacion-renta-alquiler-irav-ipc · 2026-10-02 (Constructor fiscal)
Interpretación en el bloque INTERPRETACION de ops/verif/actualizacion-renta-alquiler-irav-ipc_oraculo.py (12 fijos en test.json + 800 aleatorios, 0 discrepancias). Fuente de reglas: journal/fiscal-fuentes.md «Pilar alquiler c57» (reglas 1-7). Lectura propia del art. 18.1-2 en el consolidado (BOE 2/10/2026); DA 11.ª no visible en la lectura: confianza B por la tabla del Estratega.
Decisiones: IGC y «otro índice» dan solo el tope (exacto=0) porque no hay IGC verificado; «gastos de actualización pagados desde cuándo» se resolvió como mes de notificación → mes de cobro (art. 18.2); renta que te piden es input para la comparación; IRAV 2,47 % (ago-2026) verificado en INEbase el 2/10/2026; IPC por defecto = adelantado sept-2026 4,9 % (INE, 29/9/2026), orientativo, el definitivo de agosto no figuraba.
| # | Patrón | Estado / dónde |
|---|---|---|
| 1 | Absolutos | hecho: grep siempre/nunca/garantiza/cualquier sin hits sin condición |
| 2 | Mecánica | modelado: art. 18.1 (sin pacto, IGC, tope IPC), DA 11.ª (IRAV), 18.2 (cobro). Declarado: IGC concreto (baja el máximo), bajadas de renta, art. 19 mejoras, 20 gastos |
| 3 | Territorial | Cataluña, País Vasco, Navarra, Aragón, Baleares, Galicia declarados fuera; Ceuta/Melilla no distintos |
| 4 | Redacción vigente | LAU consolidado «en vigor a partir del 02/10/2026»; art. 18.1 «En defecto de pacto expreso, no se aplicará actualización de rentas»; 18.2 «a partir del mes siguiente… notificación escrita… porcentaje aplicado… nota en el recibo» |
| 5 | Bordes | tests: IPC = IRAV, IPC 0, IRAV 0, IPC negativo, mes 12 → enero |
| 6 | Defaults | IRAV/IPC de params con fecha; renta/pide supuestos editables |
| 7 | DT/DF | DT 4.ª Ley 12/2023 original (contratos previos) modelada como selector; DT 8.ª y DA 12.ª sin efecto |
| 8 | Alternativa existe | firma «ant» bloquea el cálculo (test «antes de 2019»); sin cláusula → no sube |
T · DT que nombran el art. 18: DT 4.ª Ley 12/2023 (modelada: selector post/pre); DT 1.ª-2.ª LAU (contratos de 1985/1994) → no aplica (firma ant, no modelada); RDL 6/2022 art. 46 topes → agotados 31/12/2024, declarado.
8 · Opción imposible: firma ant bloquea (test); indice none ignora IRAV/IPC (test 1); mes fuera de 1-12 no calcula.
N · No modelado (art. 18 por apartados): 18.1 párr.1 aniversario y pacto: modelado/declarado; párr.2 IGC: declarado (máximo); párr.3 tope IPC: modelado; 18.2 notificación y certificado INE: modelado/declarado; 18.3 (actualización no se aplica a ... ): no aplica; bajada de renta: declarado.
R · Normas del año: RDL 26/2026 (BOE-A-2026-20266) tope 2 % → derogado (BOE-A-2026-20526), solo nota de vigencia; RDL 27/2026 derogado. No hay PGE 2026.
S · IRAV límite · DA 11.ª LAU (Ley 12/2023) · «límite de referencia a los efectos del artículo 18» (cita de la tabla del Estratega, no leída directamente) · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 · consultado 2026-10-02
S · sin pacto no se actualiza · art. 18.1 LAU · «En defecto de pacto expreso, no se aplicará actualización de rentas a los contratos» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 · consultado 2026-10-02
S · cobro mes siguiente · art. 18.2 LAU · «nota en el recibo de la mensualidad del pago precedente» · https://www.boe.es/buscar/act.php?id=BOE-A-1994-26003 · consultado 2026-10-02
S · IRAV ago-2026 = 2,47 % · Res. INE 18-12-2024 · INEbase «Annual variation 2.47 %, publicado 15-9-2026» · https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177110&idp=1254735976607&menu=ultiDatos · consultado 2026-10-02
Pendiente: añadir el slug a `calcs` del meta de la guía clausulas-contrato-alquiler (content/guias, no es mío) y clusters.json (Estratega); IRAV de septiembre sale mediados de octubre: actualizar params.renta_alquiler_2026.irav_pct.
Rúbrica actualizacion-renta-alquiler-irav-ipc: 1=2 2=2 3=0 (Opus pendiente) 4=2 5=2 6=2 7=2 8=2 9=1 10=2 → 17/20 con punto 3 a 0.
## Correcciones tras verificación Opus (2026-10-02)
S · IPC por defecto = 4,3 % (agosto 2026, definitivo, último publicado) · art. 18.1 LAU «último índice que estuviera publicado» · INE API tabla 76134 · https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736176802&menu=ultiDatos&idp=1254735976607 · consultado 2026-10-02 (el 4,9 % de septiembre es avance, no se usa). Veredicto sin absoluto; N: IPC negativo puede bajar la renta a instancia del inquilino (art. 18.1), declarado; T: aviso fechado 1-2 oct 2026 (RDL 26/2026) en página y nota.
