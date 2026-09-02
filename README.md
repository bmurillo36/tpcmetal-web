# tpcmetal.es — web de TPC Metal

La web de **www.tpcmetal.es** (formación TPC del sector del metal, Centro
Médico Siglo XXI, Móstoles), rediseñada como sitio **estático puro**: sin
WordPress, sin base de datos y sin nada que se pueda caer.

## Qué hay

- `index.html` y las carpetas por sección (`contacto/`, `gracias/`,
  `aviso-legal/`, `política-de-cookies/`, `cómo-llegar/`, `sitemap/`…):
  una carpeta por URL, para que **las direcciones antiguas sigan valiendo**.
- `assets/` y `s/` — estilos e imágenes (se conservan las rutas del hosting
  anterior por el mismo motivo).
- `CNAME`, `robots.txt`, `sitemap.xml`, `llms.txt` — el SEO.
- `herramientas/cursos.py` — utilidades del listado de cursos.
- `PASO-A-PASO.md` — cómo publicar la web, paso a paso.

## La regla que manda

El rediseño **conserva las URLs y los textos que posicionan**: cambiar una
dirección o un título sin redirección es tirar el posicionamiento ganado.
El formulario de contacto envía con el campo *Origen* antes que *Mensaje*,
porque el lector de la Suite pega al mensaje todo lo que viene detrás.
