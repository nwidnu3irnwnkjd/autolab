# Entre Muchos · calculadoras para decidir con tus números

**Sitio:** https://entremuchos.com · **Datos abiertos (CC BY 4.0):** [Barómetro](https://entremuchos.com/barometro/) y [Tablas 2026](https://entremuchos.com/tablas-2026/)

Entre Muchos reúne más de cien calculadoras gratuitas en español para decidir «¿X o Y?» con tus propios datos: hipoteca, vivienda, coche, energía, impuestos (IRPF), trabajo, paro, pensiones, autónomos, familia y ahorro. Cada página da el veredicto, la cifra que lo justifica, los supuestos y las fuentes oficiales (BOE, AEAT, Seguridad Social, BCE, INE). Los cálculos se hacen en tu navegador; no se envían datos. No es asesoramiento financiero ni fiscal.

## Cómo se hace
- Sitio estático generado con Python (sin dependencias): `projects/decidir/build.py` → `dist/`, desplegado con GitHub Pages.
- Cada calculadora son funciones puras con casos de prueba y un cálculo independiente de contraste (`ops/verif/`).
- Las cifras legales salen de `projects/decidir/data/params.json`, con su fuente, fecha de consulta y nivel de confianza.
- Metodología, política de IA y cómo citar: https://entremuchos.com/como-funciona/ · https://entremuchos.com/politica-ia/

## Operar en local
- Construir: `cd projects/decidir && python3 build.py`
- Servir: `bash ops/serve.sh decidir` → http://localhost:8787
- Comprobar: `python3 ops/check.py decidir`

## Datos abiertos y cómo citar
- Barómetro mensual (CC BY 4.0): https://entremuchos.com/barometro/ · datos: https://entremuchos.com/barometro/datos.json
- Tablas 2026 (CC BY 4.0): https://entremuchos.com/tablas-2026/
- Cita: «Entre Muchos · entremuchos.com», con enlace a la página de origen. Detalle: https://entremuchos.com/como-funciona/
- Insertar una calculadora en tu web (iframe gratuito): https://entremuchos.com/inserta/
- Feed Atom (con WebSub): https://entremuchos.com/feed.xml

## Por temas
[Hipotecas](https://entremuchos.com/hipoteca/) · [Coche](https://entremuchos.com/coche/) · [Energía](https://entremuchos.com/energia/) · [Impuestos](https://entremuchos.com/impuestos/) · [Ahorro](https://entremuchos.com/ahorro/) · [Guías](https://entremuchos.com/guias/) · [Calendario](https://entremuchos.com/calendario/) · [Todas las calculadoras](https://entremuchos.com/todas/)

## Licencias
Datos publicados (Barómetro y tablas): CC BY 4.0, citando «Entre Muchos · entremuchos.com». Código: todos los derechos reservados salvo indicación en contrario.
