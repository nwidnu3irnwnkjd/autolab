# Pre-verificación · retribucion-flexible-me-conviene (Constructor fiscal Sonnet, 2026-10-02)
Norma leída (consolidados BOE descargados el 2/10/2026): LIRPF art. 42 (y 43, 81, DA 61.ª), RIRPF arts. 45, 46, 46 bis, LGSS art. 147, ET art. 26. Oráculo: ops/verif/retribucion-flexible-me-conviene_oraculo.py (21 fijos + 800 aleatorios, 0 discrepancias > 0,5 €).

| Patrón | Estado |
|---|---|
| 1 Absolutos | hecho: grep de siempre/nunca/garantiza/solo tiene sentido/en todos los casos/cualquier en content, json y js: 0 hits. Frases «no baja la Seguridad Social» demostradas por ss igual en A y B (test) y por LGSS 147. |
| 2 Mecánica que mueve la base | modelado: lo exento no es rendimiento íntegro (42.3), SS deducible sobre el total, 19.2.f, art. 20 y DA 61.ª sobre íntegros. Declarado: ingreso a cuenta (solo adelanto), valoración de la especie (art. 43: se supone = sueldo cedido), comisiones de gestor. Efecto de art. 20/DA 61 con sueldos bajos: ahorro > tipo nominal (caso 20.000 €: 1.871 € sobre 2.906 €), dicho en la página. |
| 3 Territorial | foral: bloqueado (test); Canarias/Ceuta/Melilla: IRPF autonómico de params (Ceuta/Melilla no están); CyL, Murcia, La Rioja con aviso orientativo heredado. |
| 4 Redacción vigente y citas | 42.3.c: 500 € / 1.500 € discapacidad (Ley 26/2014 + 2022); 42.3.e: 1.500 €; 42.3.a incluye teletrabajo (RDL 35/2020); RIRPF 45.2.1.º «no podrá superar 11 euros diarios»; 46 bis.1.2.º «136,36 euros mensuales ... límite 1.500 anuales»; LGSS 147.2 «Únicamente no se computarán»; ET 26.1 «el salario en especie [no] podrá superar el treinta por ciento ... ni dar lugar a la minoración de la cuantía íntegra en dinero del SMI». Nota: el encargo hablaba de «productos a precios rebajados hasta 1.652,86 €»: no consta en el art. 42 vigente, no se modela. La guardería está en 42.3.b (no «42.3.b guardería en la empresa» como decía el backlog: b es servicios sociales y culturales, incluye el primer ciclo de educación infantil). |
| 5 Bordes | test.json en cada tope: seguro 500/501, comida 2.420/2.421 (220 d × 11), transporte 1.500/1.501, 30 % (9.000/9.001), SMI (2.906/2.907), seguro con discapacidad. |
| 6 Conceptos omitidos / defaults | defecto 30.000 €, 600 €, 1 persona, 220 días: hipótesis editables, no «no verificado». Beneficio de precio (póliza de grupo) = diferencia coste−sueldo cedido, input del usuario. |
| 7 / T Transitorias | LIRPF 42: Ley 26/2014 (efectos 2015), RDL 35/2020 (teletrabajo, 2020), Ley 28/2022 (letra f acciones, no modelada): ninguna DT/DF aplica en 2026 sobre las letras a, b, c, e; RIRPF 45/46/46 bis: RD 633/2015 y 1074/2017 ya en vigor. LGSS 147: Ley 12/2022 solo añade comunicación de planes de empleo. DA 61.ª LIRPF modelada (RDL 5/2026). |
| 8 Opción imposible | (a) producto «Otro» o comida sin días → exención 0: veredicto «la exención no existe» (casos 11, 7); (b) ceder más del 30 % o dejar el dinero bajo el SMI → escenario 4, sin cifra (casos 14, 16, 17); (c) foral → bloqueo (caso 18); (d) sueldo ≤ SMI → máximo 0. |
| N No modelado | en «Supuestos» de la página y en la nota del resultado: forales, vehículos, vivienda, préstamos a empleados, planes de pensiones de empleo, acciones (42.3.f), directivos, ingreso a cuenta, comisiones; criterio DGT sobre la sustitución de sueldo por especie NO contrastado (la ley no lo excluye; si el plan lo limita, el ahorro sería menor); jornada parcial (SMI proporcional) no modelada; prima del seguro repartida a partes iguales (si no, el tope exento baja y el ahorro también); deducción por maternidad (art. 81.2: peor caso calculado para guardería, no entra en el veredicto). |
| R Normas del año | RDL 26/2026: no toca arts. 42 LIRPF, 45/46/46 bis RIRPF, 147 LGSS ni 26 ET (grep del consolidado: solo menciona «artículo 42» del Código de Comercio y del reglamento de información); no se cita como fuente. Sin PGE 2026. |

## Supuestos «no todos de ley» para el Verificador
1. La empresa valora la especie por el sueldo cedido (coste para el pagador, art. 43 LIRPF) y cotiza por ese valor: si valora más o menos, cambia IRPF y SS de la parte tributable.
2. La sustitución de sueldo por producto exento mantiene la exención (criterio DGT no verificado); la ley no la excluye y el ET 26.1 la limita al 30 % y al SMI en dinero (SMI anual 17.094 en jornada completa).
3. Prima del seguro repartida por igual entre personas; tarjeta de transporte repartida en 12 meses (136,36 €/mes no limita hasta 1.500 €); comida: 11 € × días hábiles sin dietas.
4. Resultado = IRPF final (no retención); art. 20 y DA 61.ª copiados de comparar-ofertas (verificado por Opus).
5. Umbral de empate: 5 % del coste por tu cuenta (regla de Estilo c32), no de ley.
Rúbrica retribucion-flexible-me-conviene: 1=2 2=2 3=0 (hasta Opus) 4=2 5=2 6=2 7=2 8=2 9=1 10=2 → 17/20 con el punto 3 a 0 (19/20 cuando el Opus lo cierre); petición de clusters abierta en ops/requests.md.

R · RDL 26/2026 derogado el 2-10-2026 · BOE-A-2026-20526 · revisado c53
