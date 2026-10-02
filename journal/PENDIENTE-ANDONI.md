# Pendiente de Andoni (cosas que los agentes no pueden hacer)

## LO PRIMERO: 5 cosas que solo tú puedes hacer para que Google y las IAs nos encuentren (actualizado 2-oct, c24)
Situación: la web está bien hecha y abierta a los buscadores (revisado hoy desde fuera, sin errores), pero Google aún no ha entrado ni una vez: nadie nos enlaza y nadie le ha avisado a mano. Por orden de impacto:
1. **Pedir a Google que entre (5 min, efecto en 1-3 días).** search.google.com/search-console → propiedad entremuchos.com → barra de arriba «Inspeccionar URL» → pega `https://entremuchos.com/` → «Solicitar indexación». Repite con `/decidir/`, `/hipoteca/`, `/ahorro/` y `/barometro/` (unas 10 al día como máximo). Es lo que más adelanta la primera visita de Google.
2. **Un enlace desde algo tuyo público (5 min, efecto en días).** Pon `https://entremuchos.com` en tu perfil de LinkedIn (sección «Sitio web») o en un post, o en tu GitHub. Hoy no nos enlaza nadie, y los enlaces son el camino principal por el que Google descubre webs nuevas.
3. **Dar de alta Bing (2 min, efecto en 2-7 días).** bing.com/webmasters → entra con la cuenta del dominio → «Importar desde Google Search Console». Bing alimenta a Copilot y a parte de ChatGPT, y es el único sitio que nos dirá si una IA nos cita.
4. **Añadir el «feed» en Search Console (1 min).** Menú izquierdo «Sitemaps» → escribe `feed.xml` → «Enviar». Avisa a Google de cada novedad (ya se lo indicamos también en el archivo para robots, así que esto es un refuerzo).
5. **Arreglar «www» (5 min, poco impacto en Google, evita un aviso de «web no segura»).** Quien escriba `https://www.entremuchos.com` ve hoy un error de certificado. En el panel de DNS del dominio, cambia el registro `www` para que apunte a `nwidnu3irnwnkjd.github.io` (en vez de a entremuchos.com); GitHub pone el certificado solo en unas horas.
Qué esperar: con 1-3 hechos, primeras páginas en Google en 1-2 semanas y primeras búsquedas con nosotros en 4-8 semanas (finales de octubre a finales de noviembre). Sin ellos, puede tardar bastante más. Si el 15-oct Google sigue sin haber entrado, lo revisamos juntos.

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
