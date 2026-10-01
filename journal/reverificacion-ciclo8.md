# Re-verificación ciclo 8 · 2026-10-02 (Sonnet)
## plan-pensiones-o-fondo-indexado: APTA PARA PUBLICAR
- Cambios 1-4 aplicados (js excede: art. 5.3/36.5/52.2; HTML límite: arrastre, 8.500 conjunto/10.000 total; FAQ 2 y sources; ETF art. 94.1.a en HTML y FAQ 5). Recomendados 5-7 aplicados (art. 56.2, art. 20, 40 % DT 12.ª con plazo de 2 años, liquidez con todas las contingencias). params.json: incremento_conjunto_max 8500, limite_total 10000, arrastre 5, multa 50.
- Test.json incluye casos 4, 8, 9 (5750, 20000, 150000).
- Oráculo: casos 1-11 OK (caso 11 JS -9632,54 vs art. 56.2 -9965,67, declarado como límite), barrido 500: 0 discrepancias.
- Corregido en sources (json): «; no se modelan: Ley 35/2006» (repetición/etiqueta errónea) -> «. Fuentes: Ley 35/2006».
## luz-fija-o-indexada: APTA PARA PUBLICAR
- CCF 3,113 €/kW·año en JS (L.ccf) y params (margen_comercializacion_fijo_eur_kw_ano); aviso >10 kW (MAXKW); Canarias/Ceuta/Melilla; textos valle/septiembre, «≤ 10 kW» (hasta 10 kW), IPC sept->nov, oct->dic; nota 12 meses (~15 €, casi empate = -14,72).
- Oráculo: 9 escenarios OK, «discrepancias JS vs Python (CCF=3.113): 0».
## Build y check
build.py: OK 29 páginas, 14 calculadoras; barómetro 140/140; AVISO diesel: caída simulada (esperado); check.py: 423/423.
