# Verificación fiscal · kilometraje-y-dietas-exentas-irpf · 2026-10-02 (Verificador Opus, v3.4)
VEREDICTO: PUBLICABLE CON CAMBIOS · T 0 · 8 0 · N 0 · R 1 · S 1 · otros 1 (absolutos) · críticos 0
Paso 0 (norma leída antes del oráculo): coincide con el bloque INTERPRETACION. Oráculo re-ejecutado: 17 fijos + 800 aleatorios, 0 discrepancias; --contenido OK.

## Norma leída (BOE, 2/10/2026)
- RIRPF art. 9 (BOE-A-2007-6820), versiones 2007, 2008 y 2023 (la última, vigente desde el 17/7/2023, la introduce la Orden HFP/792/2023). 9.A.2.b conserva «0,19 euros por kilómetro recorrido», y el consolidado añade una nota «Téngase en cuenta» que remite al art. único.1 de la Orden (0,26).
- Orden HFP/792/2023 (BOE-A-2023-16461): dictada al amparo del art. 9.A.5 del RIRPF (revisión por el Ministro). Su art. único.1 fija 0,26 €/km para 9.A.2.b (vehículo propio, no transporte público), «siempre que se justifique la realidad del desplazamiento», más peajes y aparcamiento justificados. El art. único.2 aplica 0,26 a 9.B.1.a. Entró en vigor el 17/7/2023, día de su publicación. No hay revisión posterior: el análisis del RD 462/2002 solo recoge la Orden HFP/793/2023 en su art. 18.1, y el art. 9 no tiene ninguna versión de 2024 a 2026. El RDL 26/2026 no toca el art. 9.
- Presentación de la cifra: el texto actual es correcto. Mejora opcional: «el art. 9.A.2.b fija 0,19 €; la Orden HFP/792/2023, dictada por la habilitación del art. 9.A.5, lo revisa a 0,26 €».
- 9.A.3: manutención con pernocta 53,34 € (España) y 91,35 € (extranjero); sin pernocta 26,67 € y 48,08 €; estancia por lo que se justifique (transportistas: 15 € y 25 € sin justificar); siempre en un municipio distinto del de trabajo habitual y del de residencia. No son exentas si el desplazamiento dura más de 9 meses continuados (sin descontar vacaciones ni enfermedad). El pagador acredita el día, el lugar y el motivo del desplazamiento (este requisito es de 9.A.3, no del kilometraje). 9.A.4 (centros móviles): la FAQ es correcta. 9.A.6: el exceso tributa. Todo coincide con params.json.
- LGSS art. 147.2.b (BOE-A-2015-11724, versión del 1/1/2023): no computan en la base la locomoción ni la manutención y estancia «en la cuantía y con el alcance previstos» en la normativa del IRPF. Por tanto el exceso cotiza; la página, el JS y el oráculo lo tratan igual. El 6,50 % del trabajador (4,70 + 1,55 + 0,10 + MEI 0,15) es correcto para contrato indefinido; en temporal sería 6,55 %, y la página ya declara «indefinido».
- LIRPF 17.1.d y 19.2 («exclusivamente»): la locomoción no pagada no se deduce, salvo en las relaciones laborales especiales del art. 9.B. La FAQ es correcta.

## Cambios obligatorios
| # | Clase | Archivo | Qué | Por qué |
|---|---|---|---|---|
| 1 | otros (absoluto) | calcs/…json lead y veredicto; content lead | «hasta 0,26 € por km no pagas IRPF ni cotización» → añadir «en desplazamientos de trabajo fuera de tu centro habitual (no casa-trabajo) y justificados». En el veredicto, «no se puede restar en tu IRPF» → «en general no se puede restar» | 9.A.2 exige desplazamiento fuera del centro y justificación; 9.B es la excepción |
| 2 | R | content, «Ten los justificantes» | «La empresa debe acreditar el día, el lugar y el motivo» es el requisito de las dietas (9.A.3); para el kilometraje, «hay que justificar la realidad del desplazamiento» (9.A.2.b y Orden) | cita aplicada a otro apartado |
| 3 | S | calcs/…json input «tipo» (y params tipo_nota si se cita) | «30 % para un sueldo de unos 20.000 a 35.000 €» → el tramo 20.200-35.200 € es de base liquidable, que equivale a un bruto de unos 24.000-40.000 €. Escribir «base liquidable de 20.200 a 35.200 € (bruto de unos 24.000 a 40.000 €)» o quitar la cifra de sueldo | LIRPF art. 63: escala sobre la base liquidable. No cambia ninguna cifra porque el tipo lo pone el usuario |

## Supuestos S revisados (defendibles y declarados en la página)
Son defendibles y están declarados: el tipo marginal lo pone el usuario; la misma dieta con y sin pernocta; peajes con efecto neto 0 (exentos por lo justificado: Orden y 9.A.2.b); solo manutención en España; sin base máxima. Ninguno cambia el veredicto.
## T/8/N/R
T: el art. 9 no tiene DT y la DF del RD 1804/2008 está agotada. 8: los bloqueos son correctos (más de 365 días; sin km ni días). N: extranjero, más de 9 meses, estancia, transportistas, personal de vuelo, base máxima y comedor (RIRPF art. 45) están declarados. R: RDL 26/2026 correcto (no toca 9 RIRPF, 17/19 LIRPF ni 147 LGSS).
## Casos de prueba nuevos
Ninguno obligatorio: los bordes 26,67/26,68 y 0,26=0,26 ya están en test.json.
