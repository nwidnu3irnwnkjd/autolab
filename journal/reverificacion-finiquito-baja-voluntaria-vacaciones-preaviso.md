# Reverificación · finiquito-baja-voluntaria-vacaciones-preaviso (2026-10-02)
Cambios aplicados 8/8 (solo lectura).
1 cotización por prorrata: js (prorr + tope, sin pagasPend entera), test.json (cot 87,14; 30-jun 131,99; 12 pagas sin cambio), json/html: OK.
2 Convenio 132 OIT con BOE-A-1974-1055 (txt.php 200): json sources, params.fuente, html y FAQ 2: OK.
3 baja voluntaria/despido (arts. 40, 41.3, 49.1.m, 50) en html, js y FAQ 5: OK.
4 despido objetivo 20 / improcedente 33 / disciplinario sin indemnización: OK.
5 "si no caben dentro del preaviso, retrasa la salida" (html) y js condicionado: OK.
6 IRPF tipo único regularizable (RIRPF 80.1, 86.1, 87.2.3.º) en html, label y FAQ 4: OK.
7 efecto del devengo (1.855 € vs 997 €) en html, json y params: OK.
8 "hasta un 13 %" en html y params.convenciones (c) + TS/TJUE retribución ordinaria: OK.
Cifras: lead, veredicto y FAQ usan 87 € de cotización, ~1.782 € netos y 796 € con 15 días de preaviso (recalculado: 1.340,64 x 6,5 % = 87,14; 2.199,29 - 329,89 - 87,14 = 1.782,26; menos 986 = 796).
Fuente RGC (RD 2064/1995, art. 23.1.A): enlace https://www.boe.es/buscar/act.php?id=BOE-A-1996-1579 en json sources; curl -sI = 200; título BOE confirma "Reglamento General sobre Cotización". Nota: el html no enlaza el RGC (solo lo cita por nombre); la fuente sí está en sources.
Absolutos sin condición: ninguno detectado.
ops/check.py decidir: OK 8366/8366 (avisos ajenos: diesel, tipo_hipoteca_fija).
