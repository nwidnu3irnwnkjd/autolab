# Reverificación · compensar-perdidas-ganancias-irpf-antes-fin-de-ano · 2026-10-02 (Sonnet, solo lectura)
RESULTADO: 5/5 cambios aplicados. Sin problemas pendientes.

1. Fórmula (liquidar): aplicado. Fase 1 ejercicio (nuevo b contra 25 % de a; a negativo contra 25 % de b), fase 2 saldo antiguo contra b y luego 25 % restante de a. test.json incluye los 2 casos nuevos del Opus (caducaCon 2.000; baseSin 250 / cuota 47,50).
2. Texto Supuestos: aplicado (primero lo del año, después saldos anteriores, 25 % conjunto, Manual AEAT). FAQ 3 coherente.
3. Fondos: aplicado en content (art. 94.1.a, 1 año no cotizados / 2 meses ETF), ayuda de `perdida` y FAQ 2.
4. CAIF art. 95 ter: aplicado en content «Qué no incluye», sources y params.fuente («no modifica estos artículos y añade el art. 95 ter»).
5. DA 39.ª: aplicado (no aplica en 2026, plazo de 4 años vencido); sin rastro de «puede permitir compensar más».
Extras recomendados: ayuda de `recompra` avisa del todo-o-nada y content cita la DA 12.ª.

Ejecuciones: ops/verif/<slug>.py -> 3/3 OK (caducaCon 2000, arrastreCon 4000, baseSin 250). ops/check.py decidir -> OK 6071/6071 (avisos ajenos: diesel, tipo_hipoteca_fija).
Absolutos y cifras legales nuevas sin fuente: ninguno detectado (cifras 25 %, 4 años, 2/12 meses, escala 19-30 % con fuente en sources/params).
