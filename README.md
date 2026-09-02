# tpcmetal-web — Rediseño de www.tpcmetal.es

Rediseño moderno del sitio **TPC Sector del Metal** (Prevención Siglo 21, Móstoles), manteniendo **exactamente** los mismos textos, direcciones web, títulos y metadatos del sitio actual para **no perder el posicionamiento en Google**.

## Qué se mantiene idéntico (SEO)

- **URLs**: `/`, `/contacto/`, `/cómo-llegar/`, `/aviso-legal/`, `/política-de-cookies/`, `/sitemap/` — con tildes, igual que ahora.
- **Títulos de página** (`<title>`), **meta description**, **meta keywords** y textos: copiados literalmente del sitio actual.
- Todos los teléfonos, direcciones postales, textos legales y el calendario de cursos.

## Qué mejora

- Diseño moderno móvil-primero: botón fijo de **Llamar / E-mail / Cómo llegar** siempre visible en el móvil.
- Carga muy rápida: HTML + un solo CSS, sin frameworks, sin jQuery, sin fuentes externas.
- **SEO técnico**: `sitemap.xml`, `robots.txt`, canónicas, Open Graph.
- **GEO (posicionamiento en buscadores de IA)**: fichero `llms.txt` y datos estructurados Schema.org (LocalBusiness, cursos, preguntas frecuentes, coordenadas GPS del centro).
- Accesibilidad: contraste, etiquetas, navegación por teclado.

## Estructura

```
index.html                    Portada (cursos, calendario, formulario, FAQ)
contacto/index.html           Contacto
gracias/index.html            Página de gracias tras enviar el formulario
cómo-llegar/index.html        Ubicación con mapa
aviso-legal/index.html        Aviso legal y privacidad
política-de-cookies/index.html
sitemap/index.html            Mapa del sitio (página)
sitemap.xml, robots.txt, llms.txt, 404.html
assets/ y s/                  Estilos e imágenes (rutas del hosting anterior)
herramientas/cursos.py        Cursos por semanas desde la hoja de Google
PASO-A-PASO.md                Cómo publicar la web, paso a paso
```

## El formulario y el CRM

El formulario envía a **`https://formularios.tpcmetal.es/enviar/tpcmetal`**,
el servicio de formularios propio del VPS: apunta cada envío antes de
mandarlo al buzón, y el Monitor cruza esa lista con el CRM para avisar si un
lead se pierde por el camino. La web de origen la da el propio destino
(`/enviar/tpcmetal`). En la versión antigua de `main` el envío era distinto
y el campo **Origen iba antes que Mensaje** (el lector de la Suite pega al
mensaje todo lo que viene detrás de él); en `editorial` ya no hace falta.

## Publicada y funcionando (comprobado el 02/09/2026)

1. **La web está en producción**: `www.tpcmetal.es` apunta por CNAME a
   GitHub Pages (`bmurillo36.github.io`), que sirve la rama **editorial**.
   El plan antiguo de subirla a IONOS quedó superado: IONOS conserva el DNS
   y el correo; la web la sirve Pages, y con el push queda publicada.
2. **Lo de FormSubmit de la primera versión ya no aplica**: el formulario va
   por el servicio propio (véase arriba), y los leads de tpcmetal.es llegan
   al CRM — se ve en la pestaña Mail del Monitor.
3. La medición va con Tag Manager propio, **GTM-KPPWWKD5** (02/09/2026).
4. **Único repaso pendiente**: en el aviso legal aparece el correo
   `info@prevencion.com` (venía así de la web antigua); confirmar si es una
   errata por `info@prevencionmadrid.es`.
