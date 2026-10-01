# Costes por ciclo
fecha-hora | 5h % | semanal % | extra EUR | nota
2026-10-01T20:41Z | 31 | 16 | 0.55 | ciclo 1 inicio (primera línea del día)
2026-10-01T21:20Z | ~33 | ~17 | 0.55+ | ciclo 1 cierre: Diseñador(opus,7min,134k tok) + Constructor(sonnet,1min,69k tok) + QA(haiku,1.6min,64k tok); 1 falso positivo de QA (sitemap) descartado
2026-10-01T21:08Z | 32 | 16 | 0.55 | ciclo 2 inicio (adelantado por Andoni)
2026-10-01T21:35Z | ~34 | ~17 | 0.55 | ciclo 2 cierre: Constructor(sonnet,2min,83k) + Diseñador(sonnet,2.7min,104k) + Estratega(opus,7.8min,141k) + QA(haiku,2.3min,66k); falso positivo QA (JSON-LD) descartado
2026-10-01T21:45Z | 35 | 17 | 0.55 | ciclo 3 inicio (adelantado por Andoni)
2026-10-01T22:10Z | ~37 | ~18 | 0.55 | ciclo 3 cierre: Diseñador(opus,14min,200k) + Constructor(sonnet,1.8min,79k) + Investigador(opus,5.4min,141k) + QA(haiku,1.4min,60k); cadencia acortada a 120 s por orden de Andoni
2026-10-01T21:40Z | 39 | 18 | 0.55 | ciclo 4 inicio
2026-10-01T21:54Z | ~44 | ~20 | 0.55 | ciclo 4 cierre: Constructor(sonnet,2.6min,94k)+Diseñador(sonnet,9.5min,190k)+Estratega(opus,9min,153k)+Mejorador(opus,5min,98k)+Verificador(sonnet,3min,80k)+QA(haiku,3.8min,97k); falso positivo QA (lineChart: ruido de consola de página de prueba borrada) descartado
2026-10-01T21:57Z | 44 | 18 | 0.55 | ciclo 5 inicio (refactor build.py T1 + lote de 2 calculadoras)
2026-10-01T22:06Z | ~48 | ~21 | 0.55 | ciclo 5 cierre: Diseñador(sonnet,refactor,72k,0.8min)+Constructor(sonnet,2 calcs+lineChart,105k,4.2min)+QA(haiku,94k,3.6min); build.py partido en ui.py/calcs_loader.py sin cambio de salida
