# KPIs de tráfico (PLAN-TRAFICO) · una fila por ejecución (`python3 ops/kpis.py`, 1 vez por ciclo en close_cycle.sh)

**Regla de lectura.** Éxito de la semana 2 (16-oct-2026): **≥ 50 URLs conocidas/indexadas por Google** (con 12 URLs de muestra, «Conocidas» ≥ 12 de 12 y el sitemap procesado en Search Console equivale a ese umbral; hasta entonces, la tendencia de «Conocidas/12» es la señal) **y primeras impresiones** (Impr. 7d > 0). Si el 15-oct «Conocidas» sigue en 0: revisar propiedad y plan B.
Tendencia ↑ ↓ = compara «Conocidas», «Impr.» y «Sesiones» con la fila anterior (en ese orden). n/d = la API falló. Eventos 7 d: share_click / calc_used / calendar_add / asistente_paso / asistente_resultado (0 si aún no existen). «Sesiones» incluye tráfico propio (no separable).

| Fecha (UTC) | URLs sitemap | Conocidas /12 | Clics 7d | Impr. 7d | Pos. | Sesiones 7d | Usuarios 7d | share | calc | cal | as_paso | as_res | Top 5 páginas (vistas) | Tend. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-02 15:00Z | 140 | 0 | 0 | 0 | — | 18 | 12 | 0 | 0 | 0 | 0 | 0 | / (115); /decidir/ (36); /decidir/alquilar-o-comprar/ (35); /decidir/hipoteca-fija-o-variable/ (35); /decidir/amortizar-o-invertir/ (30) | inicio |
