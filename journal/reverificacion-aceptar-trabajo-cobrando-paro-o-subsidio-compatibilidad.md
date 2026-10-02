# Reverificación · aceptar-trabajo-cobrando-paro-o-subsidio-compatibilidad · 2026-10-02
RESULTADO: 6/6 cambios aplicados, sin pendientes.
1 (S crítico, subsidio tras paro >12 m): opción «subsidio59» en json, bloqueo 6 en js, test con expect bloqueo 6, nota en supuestos del html. OK.
2 (8, LISOS 25.4.a/47.1.b): condicionado en js (ganador A, línea de oferta adecuada), json FAQ y html (veredicto, ejemplo sueldo 300 €, supuestos). OK.
3 (absoluto «no hay compatibilidad»): añadido «salvo desde el décimo mes… DA 59.ª» en lead, veredicto, FAQ 1, html y js. OK.
4 (R): bloqueo 5 y html precisan paros nacidos desde 1-4-2025, parcial pasa a CAE desde el 10.º mes, desistimiento 15 días hábiles. OK.
5 (N): tope 375 % IPREM (2.250 €) declarado en html, json y params.json (da59_tope_salario_pct_iprem), pendiente de reglamento. OK.
6 (subsidio, texto): la nota «No incluye» del html dice «hasta el 80 %… y menos desde el principio si vienes de agotar un paro de más de 12 meses reconocido desde el 1-4-2025, DA 59.ª.4»; el json no repite la frase antigua. OK.
Sin cifras legales nuevas sin fuente (375 %/2.250 €, tabla DA 59 y LISOS figuran en params.json con fuente).
ops/check.py decidir: OK 9113/9113 comprobaciones (avisos live preexistentes: diesel, tipo_hipoteca_fija, no relacionados).
qa_static --fiscal --changed: 2 calculadoras, 0 BLOQUEANTE, 0 AVISO.
