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

El formulario envía el campo **Origen antes que Mensaje**: el lector de
correo de la Suite pega al mensaje todo lo que viene detrás de él, y con
otro orden el CRM recibía el mensaje contaminado.

## Pendiente antes de publicar en el dominio real

1. **Formulario**: envía a través de FormSubmit.co hacia `info@prevencionmadrid.es`. El **primer envío** manda un correo de activación a esa dirección: hay que abrirlo y pulsar el enlace de confirmación una sola vez.
2. **Dominio**: el sitio está pensado para servirse en `https://www.tpcmetal.es/` (las canónicas y el sitemap.xml ya apuntan ahí). Al publicarlo en IONOS (o apuntar el DNS a GitHub Pages) no hay que cambiar nada.
3. En el aviso legal aparece el correo `info@prevencion.com` (así está en la web actual; revisar si es una errata por `info@prevencionmadrid.es`).
