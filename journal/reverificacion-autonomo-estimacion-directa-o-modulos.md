# Reverificación autonomo-estimacion-directa-o-modulos (Sonnet, 2/10/2026)
Cambios aplicados: 6/6. check.py decidir: OK 5138/5138 (avisos ajenos: diesel, tipo_hipoteca_fija).

1. Renuncia conjunta módulos/IVA simplificado: aplicado (js nota y content, art. 33.2 RIVA + art. 36 RIRPF). grep "por separado|se deciden|aparte" = 0 hits en content, js y json.
2. 2027: aplicado. Avisa de 150.000 € (75.000 € a empresas) sin prórroga ni Orden de 2027; cita nota AEAT/DGT 1/4/2026 para 2026 (content, js, json FAQ).
3. Aviso B2B: aplicado (aviso150 = I > 125.000 y <= límite; títulos "léelo si facturas más de 125.000 €").
4. Aviso art. 109.2: aplicado (dice que solo vale para actividades profesionales y no se aplica en módulos).
5. Bloqueo 3: aplicado ("Si en el año anterior tus ingresos superaron...").
6. Ceuta/Melilla (DA 64.ª) y Canarias (IGIC, art. 36 RIRPF): aplicado en content y js.

Tests: añadidos ingresos 130.000 -> aviso150=1 y 125.000 -> 0; el caso 250.001 comprueba bloqueo=3 pero no el texto "año anterior" (el formato test.json solo compara campos numéricos); verificado a mano en js línea 71.
Absolutos/cifras sin fuente: no detectados; las cifras legales nuevas (150.000/75.000/250.000/125.000, 10 %, 60 %) proceden del informe Opus y llevan cita.
Pendientes: ninguno bloqueante.
