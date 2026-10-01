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
2026-10-01T22:09Z | 45 | 19 | 0.55 | ciclo 6 inicio (Constructor lote 2 + Estratega frescura + Investigador fuentes fiscales); métricas SC: 0 indexadas/0 impresiones
2026-10-01T22:20Z | ~48 | ~20 | 0.55 | ciclo 6 cierre: Constructor(sonnet,113k)+Estratega(sonnet,113k)+Ingeniero sync(sonnet,116k)+Investigador(opus,en curso)+QA(haiku,94k); datos vivos: luz/carburantes/Euríbor/tiempo; defaults y Barómetro sincronizados con live.json
2026-10-01T22:26Z | 51 | 19 | 0.55 | ciclo 7 inicio (Constructor IRPF + IEH gas; Diseñador Pulso móvil)
2026-10-01T22:58Z | ~50 | ~20 | 0.55 | ciclo 7 cierre: Constructor IRPF(sonnet,210k)+fixes(sonnet,94k)+Diseñador Pulso(sonnet,97k)+Verificador IRPF Opus(231k+253k)+QA(haiku,93k); falso positivo QA (og.png, existe y 200 en producción)
2026-10-01T23:01Z | 3 | 20 | 0.55 | ciclo 8 inicio (Constructor pensiones+luz; Estratega frescura fase 2; Mejorador del equipo pasada 2)
2026-10-01T23:23Z | 10 | 21 | 0.55 | ciclo 8 cierre: Constructor lote fiscal(sonnet,219k)+Estratega frescura f2(sonnet,154k)+Mejorador pasada 2(opus,123k)+Diseñador R8.2(sonnet,92k)+Verificadores fiscales Opus pensiones(108k)+luz(117k)+fixes Sonnet(77k+91k)+re-verificación Sonnet(85k)+QA haiku(70k); 14 calculadoras; 6 errores reales cazados por verificadores (2 legales en pensiones, margen PVPC, avisos de ámbito)
