# CLAUDE.md — tpcmetal.es

Rediseño del sitio **TPC Sector del Metal** (Prevencion Siglo 21, Mostoles).

## La regla que gobierna este repositorio

**No se pierde el posicionamiento.** El rediseño mantiene *exactamente* los
mismos textos, direcciones, titulos y metadatos que el sitio anterior. Eso no es
una preferencia estetica: es la razon de ser del proyecto. Antes de cambiar un
`<title>`, una `<meta name="description">` o la ruta de una pagina, para y
preguntate que buscador la tiene indexada.

Las carpetas con nombre son las direcciones: `contacto/`, `aviso-legal/`,
`como-llegar/`, `politica-de-cookies/`. **Renombrar una carpeta es romper una
URL.** Si hay que moverla, hace falta redireccion.

## Que hay

Estatico, sin compilacion: `index.html`, `404.html`, `assets/`, `robots.txt`,
`sitemap.xml` + `sitemap/`, y `llms.txt`.

`llms.txt` es el resumen que se da a los buscadores con IA. Dice quien es el
centro: homologado por la Fundacion Laboral de la Construccion, **n.º de
registro 0505101086**, en Mostoles, cursos presenciales para la Tarjeta
Profesional de la Construccion del sector metal, titular **Centro Medico Siglo
XXI, S.L.** Si cambian los datos de contacto o el titular, cambian aqui tambien.

## Al tocar algo

1. `sitemap.xml` tiene que seguir listando lo que existe, ni mas ni menos.
2. `robots.txt` no debe bloquear lo que quieres que se indexe.
3. `404.html` tiene que seguir devolviendo 404 de verdad, no 200 con cara de
   error: una pagina de error que responde 200 se indexa como si fuera buena.
