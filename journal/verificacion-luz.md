# Verificación independiente · luz-fija-o-indexada · 2026-10-02 (Verificador fiscal, Opus)
VEREDICTO: **PUBLICABLE CON CAMBIOS** (cálculo correcto contra la norma; falta un concepto regulado que da la vuelta al caso «media 12 meses», y textos a matizar).
Oráculo propio: ops/verif/luz-fija-o-indexada.py (Python desde la norma + JS por osascript; 9 escenarios, 0 discrepancias > 1 €). check.py: 389/389 OK.

## 1. Norma (consultada hoy en BOE)
- Potencia 2.0TD: peaje 23,324952 + 0,443770 (BOE-A-2025-26348) + cargos 4,379461 + 0,281653 (BOE-A-2025-26705) = **28,429836 €/kW·año** ✔.
- RD 216/2014 consolidado, art. 10 bis: A = 0,45 «mercado diario e intradiario», B = 0,55 futuros ✔ (la FAQ dice solo «mercado diario»: matiz).
- **Margen de comercialización fijo (CCF)**: el RD 216/2014 consolidado define FPU = FPUP + FPUC + CCF·Pot, con CCF «fijado por orden». Orden ETU/1948/2016 (BOE-A-2016-12274), anexo II: **3,113 €/kW·año**; no hay orden posterior que lo cambie (se sigue aplicando; la cifra de 4 € citada por el Constructor es la redacción original, ya sustituida). Confianza A− (valor BOE; vigencia por prórroga, contrastar con una factura PVPC actual). NO es «no verificable» y NO es «ligero»: +18,2 € con impuestos a 4,6 kW.
- IEE Ley 38/1992 art. 99: 5,11269632 % con cuota mínima 1 €/MWh (usos no industriales) ✔; el JS aplica max(% · base, 0,001 · kWh) sobre potencia+energía y el IVA sobre base+IEE ✔ (orden correcto; alquiler de contador fuera de la base del IEE, coherente con excluirlo).
- IVA octubre 2026 = 21 % ✔. RDL 25/2026 (BOE-A-2026-20265): arts. 18-21 solo noviembre (si IPC electricidad de septiembre > +15 % interanual) y diciembre (IPC de octubre); IVA 10 % solo **potencia ≤ 10 kW** o vulnerable severo; IEE 0,5 % con mínimo 1 €/MWh. En septiembre no se aplicó la rebaja. Aviso de la página correcto; falta «≤ 10 kW» y qué mes de IPC decide cada mes.
- Circular 3/2020: punta 10-14 y 18-22, llano 8-10, 14-18, 22-24, valle 0-8 L-V; sábados, domingos y festivos nacionales de fecha fija no sustituibles = valle ✔ (inputs y FAQ correctos; horario peninsular).
- Ámbito no declarado/bloqueado: PVPC solo hasta **10 kW** (RD 216/2014, art. 4/5) y 2.0TD hasta 15 kW: el input potencia no tiene máximo. Canarias (IGIC), Ceuta y Melilla (IPSI) no usan IVA 21 %; el precio REData usado es el peninsular.

## 2. Datos REData (descargados hoy, apidatos.ree.es, serie PVPC 1001, 8.760 h)
| Dato | Constructor | Verificador |
|---|---|---|
| Media sep-2026 (720 h) | 0,18397 | 0,183975 ✔ |
| Media oct-25 a sep-26 | 0,14253 | 0,142528 ✔ |
| Punta / llano / valle (€/kWh) | 0,20476 / 0,13307 / 0,11936 | 0,204757 / 0,133071 / 0,119356 ✔ |
| Factores | 1,4366 / 0,9336 / 0,8374 | 1,43661 / 0,93365 / 0,83742 ✔ (sin festivos: 1,4229 / 0,9298 / 0,8393) |
| Septiembre por periodo | — | 0,2362 / **0,1613 / 0,1698** → factores 1,284 / 0,877 / **0,923** |
Septiembre: el valle (0,170) salió **más caro que el llano** (0,161). Causa: la solar hunde el precio de mercado de 14-18 h (llano) y no la noche (valle 0-8 h, sin solar, con demanda de climatización), y la diferencia de mercado supera la ventaja del valle en peajes y cargos de energía (≈ 0,003 frente a 0,029 €/kWh). Ya ocurre de junio a septiembre (valle ≈ llano). Es real, no un error.
Efecto de mezclar la media de un mes con la forma de 12 meses: con 30/30/40 el factor es 1,046 (12 m) frente a 1,018 (forma de sept.) → el PVPC se sobreestima ≈ 20 €; con 10/10/80 es 0,907 frente a 0,955 → se **subestima** ≈ 30 € (favorece al PVPC justo al perfil al que se le recomienda). Declarado solo en genérico.

## 3. Texto ≤ cálculo
| Frase | ¿Demostrada? | Corrección |
|---|---|---|
| HTML: margen comercialización «no verificado… favorece ligeramente al PVPC» | No | Modelarlo (3,113 €/kW·año) y quitar la frase |
| Nota: «con la media de 12 meses … 735 €» (defecto) | Sí sin CCF; con CCF son 753 € y la fija sigue ganando (−14,7 €) | Decir explícitamente quién gana con la media de 12 meses y que es casi empate |
| HTML: «la punta es la más cara, el valle la más barata» | Solo en 12 m; falso jun-sep 2026 | «… en los últimos 12 meses; en verano el valle ha salido igual o más caro que el llano» |
| HTML/lead: «el PVPC compensa si consumes en valle y llano»; «lavadora… de noche, el PVPC se beneficia» | Parcial | Matizar: la ventaja del valle viene sobre todo de peajes y cargos y en meses solares se reduce |
| Defecto = media del mes en curso (sept.: el mes más caro de 12, +29 % sobre la media anual) | Sesgo hacia la fija sin aviso | Avisar en la nota cuánto se aparta de la media de 12 meses (o usar ésta por defecto, coherente con los factores) |
| FAQ impuestos nov-dic | Sí | Añadir «potencia ≤ 10 kW»; nov depende del IPC de sept., dic del de oct. |
| FAQ «bono social solo con PVPC» | Sí (RD 897/2017) | — |
| Veredicto/lead «estimación, no previsión»; «PVPC cambia cada hora» | Sí | — |
No declarado: financiación del bono social (Orden TED/1524/2025: 6,979247 €/CUPS·año comercializadoras; reparto rehecho por Orden TED/634/2026, importe NO VERIFICADO), potencias distintas en P1/P2, Península. Excedentes/autoconsumo: declarado ✔.

## 4. Escenarios (JS vs Python, € con impuestos; tol 1 €)
| Escenario | Fija JS/Py | PVPC JS/Py | Dif JS/Py | Equilibrio €/MWh JS/Py | PVPC +CCF | Dif media12 +CCF |
|---|---|---|---|---|---|---|
| 1 Defecto | 738,69/738,69 | 900,71/900,73 | −162,02/−162,03 | 192,46/192,47 | 918,94 | −14,72 (gana fija) |
| 2 Consumo 0 | 166,35/166,35 | 166,33/166,33 | 0,02/0,02 | —/— | 184,54 | −18,19 |
| 3 3,45 kW, 2.000 kWh | 474,83/474,83 | 602,56/602,57 | −127,73/−127,75 | 180,22/180,22 | 616,23 | −33,71 |
| 4 5,75 kW muy punta 50/30/20 | 1123,68/1123,68 | 1435,68/1435,71 | −312,00/−312,02 | 214,51/214,52 | 1458,47 | −58,06 |
| 5 Muy valle 10/10/80, −10 % | 738,69/738,69 | 739,39/739,40 | −0,70/−0,71 | 150,18/150,19 | 757,62 | +60,91 |
| 6 PVPC gana (0,1425, fija 0,16) | 776,85/776,85 | 683,59/683,60 | 93,26/93,24 | 135,56/135,56 | 701,82 | +74,93 |
| 7 Fija gana (0,11, +10 %) | 586,07/586,07 | 974,15/974,16 | −388,08/−388,10 | 211,71/211,71 | 992,38 | −167,35 |
| 8 Fija = equilibrio 0,192458 | 900,69/900,69 | 900,71/900,73 | −0,02/−0,03 | 192,46/192,47 | 918,94 | +147,28 |
| 9 Mínimo IEE (base fija 0) | 3,63/3,63 | 900,71/900,73 | — | 236,06/236,06 | — | — |
Precio de equilibrio: la bisección del JS coincide con la forma cerrada (≤ 0,01 €/MWh).

## 5. Cambios obligatorios
1. calcs/luz-fija-o-indexada.js: añadir `ccf: 3.113` a L y usar `d.potencia * (L.pot + L.ccf)` en costePvpc. data/params.json luz_2026: nueva clave `margen_comercializacion_fijo` 3,113 €/kW·año, Orden ETU/1948/2016 anexo II, https://www.boe.es/buscar/doc.php?id=BOE-A-2016-12274, confianza A−. test.json: recalcular los 4 casos (+18,2 € en PVPC a 4,6 kW) y añadir los escenarios 2, 5 y 8 de este informe.
2. Formulario (js/json): potencia > 10 kW → aviso/bloqueo «el PVPC solo existe hasta 10 kW»; avisar «Península y Baleares; Canarias (IGIC), Ceuta y Melilla (IPSI) tienen otros impuestos».
3. Nota del resultado (js): decir quién gana con la media de 12 meses y cuánto se aparta el precio usado de esa media; si el signo cambia, decirlo.
4. content/…html y json (lead, «Qué estás comparando», «Revisa tu perfil», supuestos): matizar «valle el más barato» (12 m; jun-sep 2026 valle ≥ llano); quitar «margen no verificado… ligeramente»; declarar que se usa la forma de 12 meses aunque el precio sea de un mes (±20-30 € en los perfiles probados).
5. FAQ impuestos (json): «≤ 10 kW» y mes de IPC que decide nov/dic. FAQ PVPC: «mercado diario e intradiario». FAQ «Qué no incluye»: sustituir el margen por «financiación del bono social (unos 7 €/año, también la cobran casi todas las fijas)» y «potencias distintas en punta y valle».
6. journal/fiscal-fuentes.md §2.3: el CCF sí está fijado (3,113, Orden ETU/1948/2016); §2.4 «< 10 kW» → «≤ 10 kW».

## 6. Supuestos
Aceptables (declarados): forma por periodo de 12 meses; media simple de horas; potencia igual P1/P2; 365 días; sin contador, excedentes ni bono social; IVA/IEE de octubre aplicados al año; festivos de fecha fija como valle (efecto < 0,015 en factores).
Erróneos: omitir el CCF (regulado y conocido) y llamarlo «no verificado/ligero»; presentar «valle más barato» como regla sin la excepción observada en jun-sep.
Re-verificación: Sonnet basta (ejecutar ops/verif/luz-fija-o-indexada.py con CCF activado en el JS y releer las frases de §3).
