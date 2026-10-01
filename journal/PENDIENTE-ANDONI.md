# Pendiente de Andoni (cosas que los agentes no pueden hacer)

## Para estar online hoy (orden)
1. **Repositorio GitHub**: crear repo vacío `autolab` (privado vale) y pasarme la URL + o bien añadir una clave SSH de esta máquina a GitHub, o bien un token (fine-grained, solo ese repo, permiso contents:write).
2. **Hosting gratis con deploy automático**: Cloudflare Pages conectado al repo. Build command: `cd projects/decidir && python3 build.py` · Output: `projects/decidir/dist`. (Alternativa: GitHub Pages con el workflow que dejaré en `.github/workflows/`.)
3. **Dominio**: comprar uno (.es o .com, ~10 €/año) y apuntarlo en Cloudflare Pages. Candidatos a comprobar: quemeconviene.es / .com, decidirbien.es, cualmeconviene.es. Hasta entonces usamos el subdominio *.pages.dev.
4. **Search Console**: añadir la propiedad y pasarme la meta de verificación (va en `data/site.json`).
5. **Analítica**: GA4 (gratis) → pasarme el ID `G-XXXX`; o Plausible (de pago) → el dominio.
6. **Email de contacto** del proyecto (un alias vale) para aviso legal y Search Console.

## Más adelante
- AdSense (cuando haya >20–30 páginas y algo de tráfico). Redes de afiliación (Awin/Tradedoubler) cuando la web esté publicada.
- Nombre/razón del titular en el aviso legal (ahora: "Editor independiente").
