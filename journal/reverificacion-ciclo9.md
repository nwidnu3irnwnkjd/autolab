# Re-verificación ciclo 9 (Sonnet, 2026-10-02)

## A) autonomo-o-asalariado: APTA PARA PUBLICAR
Cambios 1-6 del informe Opus comprobados en calcs/*.{js,json,test.json} y content/*.html (projects/decidir):
1. Veredicto JS: «a partir de X al año sin IVA... cobras siempre lo mismo o más (en algunas franjas estrechas justo antes de esa cifra ya puedes ganar más)»; aviso de «justo antes de un cambio de tramo» cuando factura < facturaIgual y gana autónomo; sin «al menos». HTML «Cómo decidir» con «salvo franjas estrechas». OK
2. «Sin contar la tarifa plana del primer año» en lead y veredicto; tarifa plana = Ley 20/2007 art. 38 ter (HTML, FAQ 4, nota JS), sin cuantía. OK
3. Art. 32.2 (único cliente) en HTML supuestos y nota «No incluye» (250-500 €), FAQ 4 y FAQ 5 (art. 32.2.1.º: 2.000 € y hasta 6.498 €). OK
4. 20 % del art. 32.3 «primer año con beneficios y del siguiente»: FAQ 4, HTML, nota JS. OK
5. «La cuota se paga cada mes aunque no factures (al año siguiente se regulariza)». OK
6. test.json: casos 40000/46000 (netoAutonomo 30258,72; facturaIgual 46213,16) y 25000/17060 Valencia (cuotaReta 3211,75; facturaIgual 30509,74). OK
Oráculo: `barrido 520 + 11 fijos: 0 casos con discrepancias > 1 EUR` (11 casos OK).

## B) cuanto-ahorrar-para-comprar-casa: APTA PARA PUBLICAR
Aplicado: Baleares AJD bloque [[0,1.5],[999999.99,2]] (art. 17 bis) en params; avisos «hab» cuantificados (Valencia 0,1 % nueva, Cantabria 7 %/1 %, Madrid 10 % ≤250k, Andalucía 6 %/1 % ≤150k, Baleares 1 % ≤270.151,20) con JS que muestra el ahorro; CLM 240.000 € (art. 21.2, Ley 1/2026) y 6 % ITP; «tipo general» en lead, veredicto, FAQ 1/2, tabla HTML (nota Valencia 11,1 %); Catastro art. 10.2 en sources y HTML; art. 29 TRLITPAJD (RDL 17/2018) en sources, nota JS, FAQ 2 y HTML; «Euríbor + 1 punto» en nota JS, etiqueta y sources; FAQ 2 con 0,4 % Madrid / 2 % Baleares. Cifras HTML recalculadas (Valencia 12,4 %/11,1 %, Madrid 7/11,75 %, etc.) coinciden con params.
Oráculo: `barrido 646 + 22 fijos: 0 casos con discrepancias > 0,01 EUR` (22 casos OK, incl. Baleares 1.200.000 -> 144.000, Valencia hab 3.250, Cantabria 5.000).

## C) Lectura HTML/FAQ
Sin afirmaciones legales sin fuente, sin cifras contradictorias con params, sin repeticiones evidentes: no se editó nada. Observación menor (no bloqueante): FAQ 5 de casa dice que no se aplican tipos reducidos, correcto con los avisos (solo cuantifican, no cambian la cifra).

## D) Build y check
`OK: 31 páginas, 16 calculadoras → dist/` · `OK barómetro: 140/140` · `AVISO diesel: caída simulada` · `OK check_live` · `OK: 636/636 comprobaciones`
