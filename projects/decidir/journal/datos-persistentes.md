# /datos/: páginas de dato persistentes (E3, 2026-10-03)
- datos.py genera /datos/irav-ipc-alquiler/, /datos/euribor-hoy/, /datos/precio-luz-hoy/ e índice /datos/ desde data/live.json y data/params.json; el build las regenera (refresh.yml ya actualiza esos JSON). dateModified = fecha del dato.
- HUECO IRAV/IPC: params.renta_alquiler_2026 solo trae IRAV e IPC de agosto de 2026 (publicado 2026-09-15). No hay enero-julio con fuente en el repo; no se muestran. Cuando refresh_data.py (o params) lleve el IRAV de septiembre (mediados de octubre) hay que añadir la serie mensual; pendiente: guardar histórico mensual del IRAV en params con fuente INE.
- Euríbor: serie mensual de 24 meses de live.json (BCE). Luz: solo hay 2 días de historial diario en live.json; la tabla diaria crece sola.
- E3: medir impresiones a 28 días de /datos/irav-ipc-alquiler/ frente a las notas de /actualidad/ del mismo dato.
