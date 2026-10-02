# Reverificación · baja-medica-cuanto-cobro-incapacidad-temporal (2/10/2026)
RESULTADO: 5/5 cambios aplicados; sin problemas pendientes.
1. Decreto 1646/1972 art. 13.1-2 con enlace BOE-A-1972-944: OK en html (Cómo se calcula), json, params.fuente. Sin frases «no hay artículo»/«no hemos encontrado». curl -sI del enlace: 200.
2. «a cargo de»: OK en html, json (lead, FAQ), js (nota); con pago delegado la empresa abona.
3. >545 días = prolongación de efectos (174.5/174.2): OK en bloqueo (js), ayuda de «dias», veredicto/FAQ (json) y html Duración. Sin «se extingue y no cobras».
4. Aviso visible de carencia 172.a: OK en html (viñeta Requisito), lead y nota del js junto al resultado.
5. «90 días naturales»: OK en html y json; sin «tres meses».
Absolutos: solo «todos los» en contextos acotados (mejora aplicada a todos los días, declarado). Sin cifras legales nuevas sin fuente.
ops/check.py decidir: OK 9553/9553. qa_static --fiscal --changed: 0 BLOQUEANTE, 0 AVISO.
Nota menor: el lead (primer párrafo) cita la carencia sin «art. 172.a» (sí aparece en el html y la nota).
