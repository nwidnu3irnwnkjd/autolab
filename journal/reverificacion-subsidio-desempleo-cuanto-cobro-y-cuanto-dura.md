# Reverificación (Sonnet, solo lectura) · subsidio-desempleo-cuanto-cobro-y-cuanto-dura · 2026-10-02
RESULTADO: 6/6 cambios aplicados · sin problemas bloqueantes

1. 275.5.e: OK en label de `renta` (json), content (requisito de renta) y notas "Cómo sale" del JS (rama general y d52).
2. d52: OK. bigNumber = r.m52 = 480; el texto dice que es el subsidio que corresponde (art. 274.3) y que no se cobra a la vez que el general; content (ejemplo mayor de 52) igual.
3. 269.2: OK en label de `dias`, content y FAQ ("que no hayas usado ya... el informe de vida laboral no los descuenta").
4. 205.1.b: OK en label de `jub`, content y FAQ ("15 años cotizados, 2 de ellos en los últimos 15").
5. "con 52 años o más": OK en veredicto; no queda "más de 52".
6. "cónyuge o pareja, o hijos a cargo (basta uno)": OK en content; no queda "e hijos".

Casos nuevos en test.json (3/3): agotado 360 d/40/0 hijos/renta 0 -> 6 m, 3.420; 55 años jub sí -> d52=1, m52=480; cónyuge sí renta 1.500 -> cargas, 30 m, 15.300. Valores = informe.
Absolutos ("siempre/nunca/garantiz/ninguno"): 0 en content. Cifras legales nuevas: ninguna; params.json (subsidio_desempleo_2026) con fuente, 275.5.e/269.2/205.1.b citados en el texto (params cita 205.1.a; 205.1.b y 269.2 no aparecen en su campo `fuente`, menor).

Ejecución: check.py decidir -> OK 8768/8768 comprobaciones (avisos ajenos: diesel, tipo_hipoteca_fija); qa_static --fiscal --changed -> 1 calculadora, 0 BLOQUEANTE, 0 AVISO.
