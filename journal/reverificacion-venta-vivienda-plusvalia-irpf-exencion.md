# Reverificación (Sonnet) · venta-vivienda-plusvalia-irpf-exencion · 2026-10-02
Cambios aplicados: 5/6. check.py decidir: OK 4842/4842 (avisos ajenos: diesel, tipo_hipoteca_fija).

| # | Estado | Nota |
|---|---|---|
| 1 DA 65.ª | OK | Declarada en lead, veredicto, faq no habitual, html, nota JS y params; ya no queda «tributa entera». Texto de sources cita DF 3.ª.Uno y DA 65.ª/66.ª, no los apartados Once/Doce del RDL (menor). DA 66.ª (Cuenta Financia Europa) solo en sources/params. |
| 2 Art. 38.3 | OK | Declarado como límite en faq 65+, faq no habitual, html y nota JS (6 meses, 240.000 €). |
| 3 Hipoteca cuenta como reinversión | OK | reinv.ayuda, html (2 sitios), faq «¿Cómo evito…?» y nota JS. |
| 4 «65 o más» | PARCIAL | Select, lead, veredicto, html y JS ya dicen «65 años o más». Quedan 2 «Si tienes más de 65 años» en faqs (json líneas 106 y 110, art. 38.3). Cambiar a «Si tienes 65 años o más». |
| 5 No residentes + Ceuta/Melilla | OK | Lead, html y nota JS: IRNR sin «3 %», art. 68.4 añadido. |
| 6 venta.ayuda | OK | «prevalece el valor de mercado» tras «valor normal de mercado»; inequívoco. |

Absolutos / cifras nuevas: sin absolutos relevantes; cifras 200.000/800.000/240.000/6 meses proceden de la lectura BOE del Opus y están enlazadas a RDL (url_rdl) y art. 38.3; params confianza A coherente con aviso «pendiente de convalidación». Menor: nombre interno de test «vivienda no habitual: tributa todo» (no visible al usuario).

Pendiente: corregir los 2 «más de 65».
