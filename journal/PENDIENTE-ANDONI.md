# Pendiente de Andoni (cosas que los agentes no pueden hacer)

## LO PRIMERO (2-oct, c56): Google aún no ha leído ni el sitemap (enviado hace 21 h); solo tú puedes desbloquearlo
1. **Search Console → «Inspeccionar URL»** → `https://entremuchos.com/` → «Probar URL publicada» (confirma que Google puede leerla) → «Solicitar indexación»; repite con `/todas/`, `/decidir/`, `/barometro/` y `/guias/` (5 min).
2. **Un enlace desde algo tuyo ya visible**: web en tu perfil de LinkedIn o GitHub, o un post con el enlace (5 min). Hoy nos enlaza 0 webs: es la vía principal por la que Google y Bing descubren sitios nuevos.
3. **Bing**: bing.com/webmasters → «Importar desde Google Search Console» (2 min). Bing alimenta a Copilot y a ChatGPT; hoy `site:entremuchos.com` da 0.
4. **Search Console → Configuración → Usuarios → añadir `autolab-reader@entre-muchos-510320.iam.gserviceaccount.com` como «Completo»** (1 min): así enviamos nosotros el feed y los sitemaps nuevos y leemos las estadísticas de rastreo sin pedírtelo más.
5. **¿Nos dejas poner descripción, web y temas en el repo público de GitHub?** Responde «sí» (lo hacemos nosotros; es un enlace más desde un sitio que Google visita a diario).

## Hecho
- Repo GitHub `nwidnu3irnwnkjd/autolab`, token con acceso, GitHub Pages activo, dominio entremuchos.com con DNS correctas, hola@entremuchos.com creado. Online desde el 2026-10-01.

## Siguiente (para captar tráfico)
1. **Search Console**: entra en search.google.com/search-console con la cuenta de Workspace del dominio → "Añadir propiedad" → tipo **Dominio** → `entremuchos.com`. Se verifica sola (ya hay un TXT google-site-verification en las DNS). Luego Sitemaps → añadir `https://entremuchos.com/sitemap.xml`. Si quieres que yo lea los datos, dame acceso a la propiedad como usuario con un correo que me indiques, o pásame capturas semanales.
2. **GA4**: analytics.google.com → crear propiedad "Entre Muchos" → flujo web entremuchos.com → pásame el ID `G-XXXXXXXX`. Lo pongo en data/site.json.
3. **Titular del aviso legal**: dime qué nombre o sociedad quieres que figure (ahora: "Editor independiente").
4. **Regenerar el token** más adelante (se pegó en el chat) y pasarme el nuevo.

## Más adelante
- Arreglar «www» (5 min, poco impacto en Google): en el DNS, registro `www` → `nwidnu3irnwnkjd.github.io` (hoy da error de certificado).
- AdSense cuando haya >20–30 páginas y algo de tráfico. Afiliación (Awin/Tradedoubler) cuando haya tráfico medible.

## Posicionamiento en IAs y buscadores (2 minutos, cuando puedas)
- **Bing Webmaster Tools** (bing.com/webmasters): iniciar sesión con la cuenta de Workspace y "Importar desde Google Search Console". Bing alimenta a Copilot y a parte de ChatGPT; sin esto no nos ven.
- **Licencia de los datos del Barómetro: APLICADA el 2026-10-02 (decisión del Estratega como director): CC BY 4.0** solo para las cifras propias (`/barometro/#descargas`, `datos.json`, `datos.csv`); las series oficiales (BCE, MITECO, REE) conservan sus condiciones. Ojo: quien ya haya descargado los datos con CC BY la conserva aunque se retire después. Si no estás de acuerdo, dilo y se quita el aviso.
- **Search Console, 5 minutos (día 2: Google aún no ha leído el sitemap, las 6 URLs clave salen «Google no reconoce esta URL»):** (1) Inspección de URL → «Solicitar indexación» en `/`, `/decidir/`, `/barometro/`, `/guias/` y 2 calculadoras (la API no puede hacerlo); (2) Sitemaps → añadir `https://entremuchos.com/feed.xml` (feed Atom nuevo). (3) Opcional: un enlace a entremuchos.com desde un perfil público tuyo (LinkedIn/GitHub): hoy hay 0 enlaces externos y es la vía principal de descubrimiento.


## DECISIONES DE ANDONI (2-oct, tarde)
- No publicará nada en redes sociales ni similar: quitar de los planes cualquier tarea de redes/perfiles/posts y no proponer más (el kit de prensa en ops/prensa/ queda archivado, solo si él lo pide).
- Titular del aviso legal: se MANTIENE «Editor independiente» (no pedir nombre legal).
- Acceso online: Andoni puede abrir sesión él mismo en el navegador integrado de la app (Search Console, Bing, GoDaddy, GitHub) y el Orquestador opera ahí. Nunca teclear contraseñas ni códigos 2FA; las acciones que cambian permisos o ajustes de cuenta (añadir usuarios, DNS, descripción del repo) se confirman antes en el chat.


## HECHO el 2-oct tarde (sesión de Claude en el navegador de Andoni)
Indexación solicitada de las 5 URL clave, 5 sitemaps enviados, autolab-reader con permiso «Completo», sitemap.xml enviado en Bing. Solo quedan opcionales: CNAME www (GoDaddy) y descripción del repo de GitHub (necesita su «sí»).

