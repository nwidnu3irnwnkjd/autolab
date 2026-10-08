# Series de referencia para decidir: Euríbor, hipotecas, carburantes, luz y alquiler (España)

Recopilación en CSV de las series públicas que usa la web https://entremuchos.com/datos/ (calculadoras para decidir sobre hipoteca, coche, luz y alquiler). Cada fila lleva fecha, valor, unidad, fuente y URL de la fuente. No hay datos propios inventados ni estimaciones: solo se redistribuyen valores leídos de fuentes oficiales y se ordenan en un formato uniforme.

## Ficheros (csv/)
| Fichero | Contenido | Filas | Fuente |
|---|---|---|---|
| euribor_12m_mensual.csv | Euríbor a 12 meses, media mensual (%) | 24 (2024-10 a 2026-09) | Banco Central Europeo, Data Portal |
| tipo_hipoteca_vivienda_nuevas_operaciones_mensual.csv | Tipo de interés medio de nuevas hipotecas de vivienda (%) | 24 (2024-09 a 2026-08) | BCE, serie MIR |
| gasolina95_media_diaria.csv / diesel_media_diaria.csv | Precio medio diario (€/l), media simple de estaciones de la Península y Baleares | 6 cada uno (2026-10-02 a 2026-10-07) | MITECO, Geoportal de gasolineras |
| pvpc_media_diaria.csv | PVPC, media de las 24 horas (€/kWh) | 6 (2026-10-02 a 2026-10-07) | Red Eléctrica (REData) |
| irav_ipc_alquiler.csv | IRAV e IPC (tasa anual, definitivo), agosto 2026 (%) | 2 | INE |

**Pocos puntos:** carburantes, PVPC (6 días) e IRAV/IPC (1 mes) son series cortas: empezamos a archivarlas en octubre de 2026. No sirven para análisis históricos; sí para consulta y como punto de partida. Se publicarán versiones nuevas del dataset (Zenodo) al ampliarse.

## Licencia
- Nuestro tratamiento (selección, estructura, normalización de los ficheros): **CC BY 4.0** https://creativecommons.org/licenses/by/4.0/deed.es
- Los datos originales pertenecen a sus fuentes y se rigen por sus condiciones, que no cambia esta licencia:
  - BCE: se debe citar al BCE como fuente y declarar las alteraciones (verificado en su aviso legal).
  - INE: su aviso legal exige citar la fuente y no alterar el sentido; no se pudo leer automáticamente, VERIFICAR.
  - Red Eléctrica: su aviso legal pide citar a Red Eléctrica y la fecha de actualización, conservar el sentido y prohíbe la explotación comercial; las condiciones específicas de REData no se pudieron leer, VERIFICAR antes de publicar pvpc_media_diaria.csv (si hay duda, retirarlo del ZIP).
  - MITECO (precios de carburantes): condiciones de reutilización no localizadas, VERIFICAR (si hay duda, retirar los ficheros de carburantes).
- Transformación aplicada: las medias diarias de carburantes (media simple de estaciones) y PVPC (media de 24 horas) las calcula la web a partir de los datos de origen.

## Cómo citar
Editor independiente [NOMBRE A COMPLETAR POR ANDONI] (2026). *Series de referencia para decidir: Euríbor, hipotecas, carburantes, luz y alquiler (España)* [Conjunto de datos]. Zenodo. DOI: [DOI TRAS PUBLICAR]. https://entremuchos.com/datos/

Cita también a la fuente original de cada serie (columna `fuente`).

## Aviso
Datos informativos, sin garantía; no son asesoramiento financiero. Pueden revisarse tras su publicación en la fuente. Reproducible: se generan con un script a partir de ficheros de datos con fecha de consulta.
Generado a partir de los datos publicados el 2026-10-07.
