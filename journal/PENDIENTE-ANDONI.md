# Pendiente de Andoni (cosas que los agentes no pueden hacer)

## Hecho
- Repo GitHub `nwidnu3irnwnkjd/autolab`, token con acceso, GitHub Pages activo, dominio entremuchos.com con DNS correctas, hola@entremuchos.com creado. Online desde el 2026-10-01.

## Siguiente (para captar tráfico)
1. **Search Console**: entra en search.google.com/search-console con la cuenta de Workspace del dominio → "Añadir propiedad" → tipo **Dominio** → `entremuchos.com`. Se verifica sola (ya hay un TXT google-site-verification en las DNS). Luego Sitemaps → añadir `https://entremuchos.com/sitemap.xml`. Si quieres que yo lea los datos, dame acceso a la propiedad como usuario con un correo que me indiques, o pásame capturas semanales.
2. **GA4**: analytics.google.com → crear propiedad "Entre Muchos" → flujo web entremuchos.com → pásame el ID `G-XXXXXXXX`. Lo pongo en data/site.json.
3. **Titular del aviso legal**: dime qué nombre o sociedad quieres que figure (ahora: "Editor independiente").
4. **Regenerar el token** más adelante (se pegó en el chat) y pasarme el nuevo.

## Más adelante
- AdSense cuando haya >20–30 páginas y algo de tráfico. Afiliación (Awin/Tradedoubler) cuando haya tráfico medible.

## Posicionamiento en IAs y buscadores (2 minutos, cuando puedas)
- **Bing Webmaster Tools** (bing.com/webmasters): iniciar sesión con la cuenta de Workspace y "Importar desde Google Search Console". Bing alimenta a Copilot y a parte de ChatGPT; sin esto no nos ven.
- **Licencia de los datos del Barómetro: APLICADA el 2026-10-02 (decisión del Estratega como director): CC BY 4.0** solo para las cifras propias (`/barometro/#descargas`, `datos.json`, `datos.csv`); las series oficiales (BCE, MITECO, REE) conservan sus condiciones. Ojo: quien ya haya descargado los datos con CC BY la conserva aunque se retire después. Si no estás de acuerdo, dilo y se quita el aviso.
- **Search Console, 5 minutos (día 2: Google aún no ha leído el sitemap, las 6 URLs clave salen «Google no reconoce esta URL»):** (1) Inspección de URL → «Solicitar indexación» en `/`, `/decidir/`, `/barometro/`, `/guias/` y 2 calculadoras (la API no puede hacerlo); (2) Sitemaps → añadir `https://entremuchos.com/feed.xml` (feed Atom nuevo). (3) Opcional: un enlace a entremuchos.com desde un perfil público tuyo (LinkedIn/GitHub): hoy hay 0 enlaces externos y es la vía principal de descubrimiento.
