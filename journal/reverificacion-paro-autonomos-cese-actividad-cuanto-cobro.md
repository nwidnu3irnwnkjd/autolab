# Reverificación · paro-autonomos-cese-actividad-cuanto-cobro (2/10/2026)
Solo lectura de json, js, test.json, html y params. Cambios aplicados 5/5.

1. Suspende vs no existe (340.1.c): json lead/veredicto/faq 3 y 5, html lead y bullet «Trabajo», js nota de condTrabajo («se suspende»): OK. No quedan frases «no existe» para trabajar a la vez.
2. Edad 330.1.d: «salvo que no tengas la cotización exigida» en json veredicto y faq 3, js MSG 3, html: OK.
3. 18 meses desde el reconocimiento (338.3): json veredicto, faq 3, js MSG 5, opción «me la reconocieron», html: OK.
4. Cuota solo en plazo (337.6): json veredicto y faq 4, html bullet, js nota «La cuota»: OK.
5. TRADE 331.2.a / 333.1.b: json lead, js MSG 1, html lead y bullet: OK. Opcional recomendado («en los motivos económicos» para el cierre del establecimiento) también aplicado.

Absolutos/cifras sin fuente: ninguna cifra nueva; las cuantías salen de params.paro_autonomos_cese_2026 (confianza A).
Pendiente menor (no bloqueante): json faq 3 dice «el derecho no existe si dejas la actividad por decisión propia» sin la salvedad TRADE (el veredicto sí lista al TRADE como causa legal).

ops/check.py decidir: OK 10523/10523 comprobaciones.
qa_static --fiscal --changed: 1 calculadora; sin avisos; 0 BLOQUEANTE, 0 AVISO.
