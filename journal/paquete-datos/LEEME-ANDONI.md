# Qué tienes que hacer (≈15 min)
IMPORTANTE: Zenodo y datos.gob.es piden un autor/titular. Hasta que decidas el nombre, NO se puede publicar bajo identidad real: o das tu nombre (o el de la entidad) o no publicamos. Tampoco inventamos uno.
1. Revisa journal/paquete-datos/README.md: marcadores [NOMBRE A COMPLETAR POR ANDONI]; sustitúyelos en README, ficha-zenodo.md y ficha-datosgobes.md.
2. Verifica (o quita del ZIP) los CSV de luz y carburantes: sus condiciones de reutilización no pudimos leerlas (ver README, apartado Licencia).
3. Crea cuenta en https://zenodo.org (puedes entrar con GitHub/ORCID).
4. Haz zip de la carpeta csv/ junto a README.md: `cd journal/paquete-datos && zip -r paquete.zip README.md csv`.
5. En Zenodo: New upload, sube el ZIP, pega los campos de ficha-zenodo.md, Publish.
6. Copia el DOI resultante y pégalo en el README (cita) si quieres.
7. Crea cuenta en https://datos.gob.es, inicia sesión, «Añadir una nueva aplicación» en /es/aplicaciones.
8. Pega ficha-datosgobes.md (ajusta si el formulario pide otros campos).
9. Envíame el enlace de Zenodo (y el de datos.gob.es): yo añado los enlaces en pie/Recursos de las webs.
10. Para regenerar datos antes de subir: `python3 ops/gen_paquete_datos.py`.
