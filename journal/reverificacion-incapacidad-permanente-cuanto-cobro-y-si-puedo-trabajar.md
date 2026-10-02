# Reverificación · incapacidad-permanente-cuanto-cobro-y-si-puedo-trabajar · 2026-10-02 (Sonnet)
Cambios aplicados 5/5 (más fuentes): 
1. Suelo 684,30 €: JS (`suelo = sueloTC/14`, max con pen, también en el 75 %) y params `suelo_total_comun_anual` 9.580,2. OK.
2. Complemento por mínimos por diferencia (`compMin`: min(mín−pen, 9.442+mín−ingresos−pen)). OK.
3. Tope de pensión no contributiva (art. 9.5 y 9.7) declarado en el contenido. OK.
4. «Lectura propia»: 0 apariciones en html, js, json y params; texto literal con arts. 9.4 y 3.1. OK.
5. Cita del 100 % (Orden art. 17 + LGSS 197.1.b) y frase del suelo/regla de 9.442 en «Límites». OK.
fiscal-fuentes.md: fila de incapacidad-permanente (l. 453) con suelo; no encuentro ya la redacción antigua «≥ 55 % de la base mínima».
Verificador .py: 3/3 OK (45 a, base 1.200, funciones distintas = 684,30; 61 a con trabajo = 693,19; sin trabajo = 875,90).
check.py decidir: 10172/10172 OK (avisos externos diesel/hipoteca ajenos). qa_static --fiscal --changed: 0 BLOQUEANTE, 0 AVISO.
Absolutos: los 3 «siempre que» llevan condición legal. Cifras nuevas sin fuente: ninguna (684,30 = 9.580,20/14, anexo I RD 241/2026).
Pendiente menor: no comprobé a mano la confianza A en el json (grep sin coincidencias en la etiqueta); revisar si importa.
