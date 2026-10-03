# PLAN TRÁFICO · 2 semanas (3 → 16 oct 2026) · decidido por Andoni el 2-oct (c49)
Objetivo único: que Google/Bing e IAs nos descubran, que el clic sea atractivo y que quien llegue use, comparta y vuelva. Se acabó construir volumen: 101 calculadoras bastan.

## Reglas nuevas (prevalecen sobre loop-prompt/EQUIPO en lo que choquen)
- Constructor fiscal: 1 cada 2-3 ciclos como máximo (solo las que tienen fecha o demanda). No fiscales: solo con `demanda:` del Estratega. Vigilante de normas sigue.
- ~70 % del esfuerzo de cada ciclo va a tráfico: Diseñador (UX/funciones), Estratega (SERP, estacionales, actualidad), Investigador (consultas y calendario), Analista (métricas, desde que haya impresiones).
- Cada tarea lleva su KPI y se mide en la pasada semanal (lunes). Sin impresiones aún: se mide con la URL Inspection API (¿la conoce Google?) y GA4.

## KPIs (cuadro de mando en ops/metrics.py)
1. URLs conocidas por Google (inspección) y indexadas (hoy 0/138). 2. Impresiones y clics (hoy 0). 3. Sesiones externas GA4 y % que usa la calculadora (evento). 4. Comparticiones (clics en Compartir/Copiar). 5. Páginas embebidas/enlaces entrantes. Éxito semana 2: ≥ 50 URLs indexadas y primeras impresiones.

## Semana 1 (3-9 oct): descubrimiento y escaparate
A. Descubrimiento (Andoni 4 gestiones ya enviadas; yo): página `/todas/` (directorio HTML de todo), sitemap por secciones, enlaces desde la home a hubs y guías, robots/feeds revisados, IndexNow de todo, vigilar a diario la inspección GSC; si el 15-oct no hay rastreo: revisar propiedad y plan B.
B. Escaparate (cómo se ve fuera): imagen social única por página (ogimg), titles/descriptions de las 40 páginas con más potencial (patrón «¿X o Y? Calculadora 2026 con tus números»), fecha «Actualizado/revisado» visible, datos estructurados (WebApplication, FAQ, Breadcrumb, Dataset), snippet de respuesta primero.
C. Funciones que enganchan: botón Compartir (WhatsApp/copiar enlace) con tus números en la URL; «Añadir al calendario» (.ics) en los plazos; buscador interno en la home y por tema («Qué te conviene según tu situación»: autónomo, familia, vivienda, trabajo); «Plan completo» (R16.4) encadenando calculadoras.
D. Actualidad con fecha: barra «Esta semana» (BOE/IPREM/SMI/Euríbor/luz) diaria vía refresh; página «Qué cambia el 1 de enero de 2027» (se rellena sola cuando salgan SMI/IPREM/pensiones); páginas estacionales publicadas con 6-8 semanas de antelación: Navidad (lotería y premios, gastos), Black Friday (guía hecha), calefacción de invierno, rebajas, Renta 2026 (campaña abril 2027).

## Semana 2 (10-16 oct): amplificar lo que funcione
E. Leer GSC/GA4; duplicar lo que tenga impresiones (mejorar título, enlazar, ampliar), podar lo que no.
F. Activos enlazables: Barómetro mensual como nota citable (CC BY 4.0), «Datos 2026» descargables, widget «Inserta esta calculadora en tu web» (iframe ligero con crédito y enlace), kit de prensa y 5 borradores de correo a medios/blogs (solo borradores; el envío es de Andoni si quiere).
G. Repetición: calendario editorial semanal de actualidad (martes: BOE; jueves: precio luz/carburantes; viernes: Barómetro).

## Lo que necesito de Andoni (solo identidad/dinero)
Las 4 gestiones de indexación/Bing/CNAME (prioridad absoluta). Opcionales: perfiles sociales de la marca, un servicio de email si quieres alertas, enviar los borradores de prensa.

## Actualización 2-oct tarde (decisión de Andoni)
- Sin redes sociales ni perfiles públicos: se descartan "enlace desde perfil", posts y envío de prensa salvo petición suya. Titular legal: «Editor independiente».
- Las gestiones online (Search Console, Bing, GoDaddy www, README de GitHub) las hace el Orquestador en el navegador integrado cuando Andoni haya iniciado sesión; confirmar en chat las que cambian permisos o ajustes.
- 3-oct: sección de noticias «Qué cambia para ti» (/noticias/, ≤ 1 pieza/día laborable, solo con hecho oficial + cifra de calculadora, ≤ 3 pp/semana): plan y MVP en ops/PLAN-NOTICIAS.md.
