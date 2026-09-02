# tpcmetal.es — Paso a paso para publicar sin perder SEO

Web reconstruida en `C:\Users\Pedro\Desktop\CLAUDE\tpcmetal.es`.
Fecha: 29/08/2026.

---

## 0. Lo primero: el aviso importante sobre Base44

Base44 genera **aplicaciones React con Vite** (lo he comprobado en tus apps
`renovartpc.es` y `Reciclajemetal.es`: tienen `vite.config.js`, `src/App.jsx` y
enrutado en cliente). En una app así, **el servidor devuelve el mismo HTML para
todas las rutas** y es el navegador quien decide qué pintar.

Para `renovartpc.es` o `reciclajemetal.es` eso da igual: son dominios nuevos sin
histórico. **Para `tpcmetal.es` no da igual**, porque tiene posicionamiento que
no quieres perder: si Google pide `https://www.tpcmetal.es/contacto/` y el
servidor le devuelve el HTML de la portada, esa URL pierde su contenido y su
posición.

Por eso la web la he hecho en **HTML estático puro**: 7 ficheros `.html`
independientes, uno por URL. Así cada dirección devuelve su contenido real.

Tienes dos caminos:

| | Camino A — Base44 | Camino B — hosting estático |
|---|---|---|
| Lo que pediste | Sí | No |
| Riesgo SEO | **Medio-alto** (hay que verificar el paso 4A) | **Ninguno** |
| Esfuerzo | Medio | Bajo |
| Coste | El de tu plan Base44 | Gratis (Netlify/Cloudflare) o el de IONOS |

**Mi recomendación:** haz el Camino A si te apetece tenerlo todo junto en Base44,
pero **no cambies el DNS hasta superar la verificación del paso 4A**. Si esa
verificación falla, vete al Camino B: son 10 minutos y el SEO queda intacto.

---

## 1. Antes de nada: activar el formulario (5 minutos, obligatorio)

Los dos formularios (portada y contacto) envian a **mbarberosala@gmail.com**
mediante FormSubmit, **sin captcha**, como pediste. FormSubmit exige una
activacion unica:

1. Abre la web ya publicada (o el ensayo local del paso 2).
2. Rellena el formulario con datos de prueba y envialo.
3. FormSubmit mandara un correo a **mbarberosala@gmail.com** con el asunto
   *"Confirm your email"*. Abrelo y pulsa el boton de activacion.
4. Vuelve a enviar el formulario. A partir de ahi llegan todos los avisos.

> **Hasta que no hagas ese clic, los formularios no entregan nada.**

### Por que el formulario esta montado exactamente asi

Tu Suite lee el buzon mbarberosala@gmail.com y mete los avisos en el CRM con
`modulo_crm/crm/parser.py`. Probe los dos formularios contra ese parser. Dos
cosas conviene respetar si algun dia tocas el formulario:

- **El asunto** contiene una de las frases que reconoce `es_lead()`:
  `Nuevo formulario de contacto desde tpcmetal.es`. Asi lo aceptan tanto el
  parser antiguo como el nuevo.
- **Los nombres de campo**, en este orden:
  `Nombre, Email, Telefono, Curso, Mensaje, Acepto, Origen`.
  El de consentimiento **se llama `Acepto`** porque el parser lo usa para saber
  donde termina el mensaje. Con un nombre largo como
  `Acepta_politica_privacidad`, el campo Mensaje se traga el consentimiento y
  el origen.

Verificado: `es_lead` da True y salen limpios nombre, email, telefono, curso y
mensaje. El campo `Curso` es un extra: el parser tambien lo captura, asi que en
el CRM veras que curso pidio cada persona.

> **Nota:** hay una copia **desactualizada** del parser en
> `Desktop\CLAUDE\Prevencion Siglo 21 SUITE DEFINITIVA...\modulo_crm\crm\parser.py`.
> La que corre en produccion (VPS, `/opt/suite`) es mas nueva y reconoce
> FormSubmit directamente. Si alguna vez pruebas cosas contra la copia local,
> actualizala antes con `git pull` de Suite20.

**Si prefieres ocultar el correo del codigo fuente** (recomendable contra el
spam): entra en <https://formsubmit.co>, genera el alias para
mbarberosala@gmail.com y sustituye `https://formsubmit.co/mbarberosala@gmail.com`
por `https://formsubmit.co/TU_ALIAS_AQUI` en `index.html` y `contacto/index.html`.

---

## 2. Ensayo local (2 minutos)

Antes de subir nada, míralo en tu ordenador:

```bash
cd "C:\Users\Pedro\Desktop\CLAUDE\tpcmetal.es"
python -m http.server 8899
```

Y abre <http://127.0.0.1:8899/>.

> **Importante:** no abras los `.html` con doble clic. Las rutas son absolutas
> (`/css/editorial.css`), que es lo correcto en producción, pero con `file://`
> no funcionan. Usa siempre el servidor local.

Comprueba: portada, `/contacto/`, `/cómo-llegar/`, `/aviso-legal/`,
`/política-de-cookies/`, `/sitemap/`. Ya lo he verificado: las 14 rutas
devuelven 200 y no hay errores en consola.

---

## 3. Publicar con GitHub Pages

El repositorio ya está: `github.com/bmurillo36/tpcmetal-web`, rama **`editorial`**.

### 3.1 Decir a Pages que sirva la rama editorial

1. Entra en <https://github.com/bmurillo36/tpcmetal-web/settings/pages>
2. En **Build and deployment - Source** elige **Deploy from a branch**.
3. En **Branch** selecciona **`editorial`** y carpeta **`/ (root)`**. Guarda.
4. Espera 1-2 minutos a que termine el despliegue (lo ves en la pestaña
   *Actions* del repositorio).

> Ojo: ahora mismo Pages sirve la rama `main`, que es la otra versión. Al
> cambiar a `editorial` cambia lo que se ve en la vista previa. `main` no se
> borra ni se toca.

### 3.2 Revisarla antes de tocar nada

Ábrela aquí:

    https://bmurillo36.github.io/tpcmetal-web/

**Esta vista previa funciona entera**: estilos, imágenes, menú, formulario y
todos los enlaces. La he preparado con rutas relativas justamente para eso, para
que puedas revisarla del todo antes de mover el DNS. Míralas todas: la portada,
`contacto/`, `cómo-llegar/`, `aviso-legal/`, `política-de-cookies/` y
`sitemap/`. Y en el móvil, que es lo que importa.

> Lo único que no funcionará en la vista previa es el envío del formulario: al
> enviarlo salta a `www.tpcmetal.es/gracias/`, que todavía es la web vieja. En
> cuanto el dominio apunte a Pages, funciona.

---

## 4. El dominio en IONOS, paso a paso

**No hagas esto hasta haber revisado la vista previa del punto 3.2.** En cuanto
cambies el DNS, la web vieja deja de verse.

### 4.1 Antes de nada: crear el buzón info@tpcmetal.es

La web publica ese correo en todas las páginas. Si no existe, los correos
rebotan.

1. IONOS - **Correo** (o *Email*) - **Crear dirección de correo**.
2. Crea `info@tpcmetal.es`. Si no quieres otro buzón que revisar, créalo como
   **alias o reenvío** hacia el correo que ya leas.

### 4.2 Desconectar IONOS MyWebsite del dominio

El dominio está enganchado al editor visual de IONOS. Hay que soltarlo.

1. IONOS - **Dominios y SSL** - busca `tpcmetal.es`.
2. En la columna *Uso* / *Destino* verás que apunta a **MyWebsite**.
3. Pulsa la rueda dentada - **Ajustar destino del dominio** (o *Cambiar uso*).
4. Elige **desconectar** o **apuntar a una dirección IP / servidor externo**.
   IONOS te avisará de que la página actual dejará de verse: es lo esperado.

> **No borres el paquete de MyWebsite todavía.** Déjalo unos días por si hay que
> volver atrás.

### 4.3 Poner los registros DNS de GitHub

1. IONOS - **Dominios y SSL** - `tpcmetal.es` - pestaña **DNS**.
2. **Borra o edita** los registros `A`, `AAAA` y `CNAME` que apunten a IONOS
   MyWebsite. **Deja intactos los `MX` y los `TXT`**: son el correo y las
   verificaciones. Si los tocas, dejas de recibir correo.
3. Crea estos registros.

**Para `www`, que es la versión canónica:**

| Tipo | Nombre | Valor | TTL |
|---|---|---|---|
| CNAME | `www` | `bmurillo36.github.io` | 1 hora |

**Para el dominio sin www (`tpcmetal.es`), cuatro registros A:**

| Tipo | Nombre | Valor |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

**Y, si IONOS te deja, los cuatro AAAA de IPv6. Son opcionales:**

| Tipo | Nombre | Valor |
|---|---|---|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

### 4.4 Decirle a GitHub cuál es el dominio

1. Vuelve a <https://github.com/bmurillo36/tpcmetal-web/settings/pages>
2. En **Custom domain** escribe exactamente `www.tpcmetal.es` y pulsa **Save**.
3. GitHub creará solo un fichero `CNAME` en la rama `editorial`. No lo borres ni
   lo edites.
4. GitHub comprobará el DNS. Puede tardar de 10 minutos a unas horas. Cuando
   aparezca **DNS check successful**, marca la casilla **Enforce HTTPS**.

> Si *Enforce HTTPS* está en gris, el certificado aún se está emitiendo. Espera
> y vuelve a entrar; suele tardar menos de una hora.

### 4.5 Lo que GitHub hace solo

No tienes que configurar nada más para esto:

- `http://` pasa a `https://`, una vez marcado *Enforce HTTPS*.
- `tpcmetal.es` redirige a `www.tpcmetal.es`, porque el dominio personalizado es
  el de `www`.
- La página de error usa `404.html`, que ya está hecha.

> Los ficheros `.htaccess`, `_redirects` y `vercel.json` del repo **Pages los
> ignora**. No estorban y sirven si algún día mueves la web a otro alojamiento.
> Las redirecciones de las direcciones sin tilde (`/como-llegar/` y
> `/politica-de-cookies/`) no dependen de ellos: son páginas HTML con `noindex`
> y redirección propia, y en Pages funcionan.

---

## 5. Actualizar la web a partir de ahora

Cambias los ficheros en la carpeta del proyecto y:

    git add -A
    git commit -m "lo que has cambiado"
    git push

GitHub Pages vuelve a publicar solo en un par de minutos.

Si lo que cambia son los cursos, antes del commit:

    python herramientas/cursos.py index.html

---

## 6. Comprobación post-publicación (el mismo día)

```bash
for u in "/" "/contacto/" "/c%C3%B3mo-llegar/" "/aviso-legal/" "/pol%C3%ADtica-de-cookies/" "/sitemap/" "/robots.txt" "/sitemap.xml" "/llms.txt"; do
  echo -n "$u -> "
  curl -s -o /dev/null -w "%{http_code}\n" "https://www.tpcmetal.es$u"
done
```

Las 9 deben dar **200**. Y estas dos deben dar **301**:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.tpcmetal.es/como-llegar/
curl -s -o /dev/null -w "%{http_code}\n" http://tpcmetal.es/
```

---

## 7. Google (SEO)

1. **Search Console** → propiedad `https://www.tpcmetal.es/`.
2. *Sitemaps* → vuelve a enviar `sitemap.xml`.
3. *Inspección de URLs* → pide indexación de las 5 URLs históricas, una a una.
4. *Cobertura* → vigila 15 días que no aparezcan 404 nuevos.
5. **Google Tag Manager**: el contenedor **GTM-KPPWWKD5** está puesto en las
   7 páginas (script en `<head>` y `<noscript>` en `<body>`). No hay que tocar
   nada en GTM.
6. **Google Ads**: las URLs de destino de tus campañas no cambian, así que los
   anuncios siguen funcionando. Aun así, entra en Ads y usa
   *"Comprobar URL final"* en cada anuncio el día del cambio.
7. **Google Business Profile**: comprueba que la web enlazada sea
   `https://www.tpcmetal.es/`.

---

## 8. Qué se ha conservado exactamente

- **Las 5 URLs originales**, con sus tildes: `/`, `/contacto/`,
  `/cómo-llegar/`, `/aviso-legal/`, `/política-de-cookies/`.
- **`/sitemap/`**, que estaba enlazada en el pie de la web antigua.
- **Los `<title>` y `keywords`** de cada página (mejorados, sin perder términos).
- **Google Tag Manager GTM-KPPWWKD5**.
- **Los dos sellos de Emagister** (calidad y valoraciones), con sus enlaces.
- **El calendario de Google** incrustado
  (`td0d9je4jt6r5sga4t97f5gk5k@group.calendar.google.com`, zona Europe/Madrid).
- **El mapa de Google** de la página *Cómo llegar*, con su clave original.
- **Todos los enlaces salientes**: prevencionmadrid.es, Google Maps
  (`maps.app.goo.gl/nEMHDDJqMXuCooTM6`), Apple Maps, Emagister.
- **Todos los correos**: info@tpcmetal.es, mbarberosala@gmail.com,
  centro@femte.es, info@tpcmetal.es.
- **Los textos legales íntegros** (aviso legal y política de cookies).
- **La programación de cursos** de agosto y septiembre.

## 9. Qué se ha añadido

**Teléfonos pulsables** — `tel:+34630292516` y `tel:+34916170423` aparecen 12
veces en la portada: barra superior, botón de portada, calendario, formulario y
pie. En el móvil se llama con un toque.

**SEO técnico**
- `canonical` y `hreflang es-ES` en las 7 páginas.
- Open Graph y Twitter Card completos.
- `geo.region`, `geo.position` e `ICBM` (Móstoles, 40.341751 / -3.863215).
- `robots.txt` y `sitemap.xml` nuevos.
- `.htaccess`, `_redirects` y `vercel.json` con las 301 (HTTPS, www y alias sin
  tilde).
- Páginas alias `/como-llegar/` y `/politica-de-cookies/` en `noindex` con
  `canonical` a la versión con tilde: quien escriba la URL sin acento llega
  igual, y Google no ve contenido duplicado.

**GEO / AEO (para ChatGPT, Claude, Perplexity y AI Overviews)**
- **`llms.txt`**: ficha estructurada del centro que los buscadores de IA leen
  directamente (datos, catálogo de cursos, normativa, cómo citar el sitio).
- **`robots.txt`** con permiso explícito para GPTBot, ClaudeBot, PerplexityBot,
  OAI-SearchBot, Google-Extended y Applebot-Extended.
- **7 preguntas frecuentes** con marcado `FAQPage`, redactadas como las escribe
  la gente en el buscador y respondidas en un párrafo autocontenido: es el
  formato que los asistentes citan.
- **Datos estructurados** `EducationalOrganization` + `LocalBusiness`,
  `ItemList` con los **6 cursos** (`Course` con duración ISO y modalidad),
  `BreadcrumbList`, `WebSite`, `Place` y `ContactPage`.
- **`speakable`** para asistentes de voz.

**Accesibilidad y rendimiento**
- Enlace *"saltar al contenido"*, foco visible, `aria-current`, `aria-label`.
- Sin librerías JavaScript: solo 6 líneas para el año del pie.
- Imágenes en SVG (pesan 3-5 KB y se ven nítidas en cualquier pantalla).
- `loading="lazy"` en todo lo que no está en la primera pantalla.
- Hoja de estilo única, ~14 KB.

---

## 10. Las imágenes

Renombradas con nombres orientados a la tarjeta TPC del sector del metal:

| Fichero | Uso |
|---|---|
| `tarjeta-tpc-metal-portada-editorial.svg` | Portada a sangre |
| `curso-tpc-metal-especialidades-aula-taller.svg` | Franja del aula-taller |
| `tarjeta-tpc-metal-tramitacion-flc-mostoles.svg` | Plano centro → tramitación |
| `tarjeta-tpc-metal-trabajador-cinturon-herramientas.png` | Foto original tuya |
| `tarjeta-tpc-metal-acero-cepillado-cabecera.jpg` | Textura original (reserva) |
| `tpc-metal-logo.svg` | Logotipo y favicon |

**Pendiente:** quería generar fotografías nuevas con IA (soldador, taller,
instalación), pero la API de imágenes de Google devolvió cuota agotada
(`limit: 0`) tanto en el modelo *pro* como en el *flash*. Las ilustraciones SVG
que he hecho son originales y encajan con el diseño, pero si quieres fotografía
real, dímelo otro día y las genero: solo hay que sustituir los ficheros
manteniendo el mismo nombre, sin tocar el código.

---

## 11. Mantenimiento habitual

**Cambiar la programación de cursos:** en `index.html`, sección
`<!-- PROGRAMACIÓN DETALLADA -->`. Es una lista `<dt>`/`<dd>` por día.

**El calendario de Google** se actualiza solo desde tu cuenta de Google. No hay
que tocar la web.

**Cambiar el correo del formulario:** busca `formsubmit.co` en `index.html` y en
`contacto/index.html`.

**Añadir una página nueva:** copia `contacto/index.html`, cambia el contenido, y
añade la URL a `sitemap.xml` y al pie de las 7 páginas.

---

## 12. Móvil (el canal principal de entrada)

Comprobado a 390 px de ancho en la portada y en contacto.

**Navegación.** Bajo 900 px aparece un botón **MENÚ** con los 8 destinos del
sitio. Es un `<details>` de HTML: funciona sin JavaScript y se cierra solo al
pulsar un enlace.

**Barra fija inferior.** Siempre visible en móvil, con dos acciones:
**LLAMAR AHORA** (naranja, a `tel:+34630292516`) y **RESERVAR PLAZA**. Alto de
56 px y se respeta el área segura del iPhone (`env(safe-area-inset-bottom)`).

**Barra superior.** En móvil deja solo los dos teléfonos, centrados y pulsables;
se oculta el correo y la etiqueta para que no se amontonen.

**Formularios.** Campos a 16 px — por debajo de eso Safari en iPhone hace zoom
automático al tocar el campo, que es la causa habitual de abandono. Casilla de
consentimiento de 24 px y teclado adecuado en cada campo (`inputmode="tel"`,
`type="email"`).

**Calendario de Google.** Bajo 760 px se carga en **modo agenda** (lista de
días), que es legible en un teléfono; el mensual no lo es.

**Botones.** Mínimo 52 px de alto y a ancho completo.

**Tipografía y ritmo.** Titulares, capitular, citas y espaciado tienen escala
propia para 620 px y otra para 380 px. Las URLs y correos largos no rompen la
maqueta (`overflow-wrap:anywhere`).

**Peso.** Sin librerías. Las ilustraciones son SVG de 3-5 KB. Solo hay dos
imágenes de mapa de bits en todo el sitio. Esto ayuda al Core Web Vitals móvil,
que es factor de posicionamiento.

### Cómo comprobarlo tú

Con el servidor local arrancado, en Chrome: F12 → icono de móvil
(Ctrl+Shift+M) → elige *iPhone 14 Pro* → recarga. O directamente desde tu
teléfono, en la misma wifi, entrando a `http://IP-DE-TU-PC:8899/`.

---

## 13. Los cursos vienen de tu hoja de Google

El bloque de convocatorias de la portada **no se escribe a mano**. Lo genera un
script a partir de tu hoja:

<https://docs.google.com/spreadsheets/d/14mcRaWiZxxqZe0Q_Jucohp-oGbQGyQhxz2SwLI1Zc9c>

Para actualizar la web cuando cambies la hoja:

```
cd "C:\Users\Pedro\Desktop\CLAUDE\tpcmetal.es"
python herramientas/cursos.py index.html
```

Escribe HTML estático entre las marcas `CURSOS:INICIO` y `CURSOS:FIN`. Estático
a propósito: Google no lee el iframe del calendario, así que si los cursos solo
estuvieran ahí no los indexaría. El iframe sigue estando, debajo.

Ahora mismo saca **24 convocatorias en 7 semanas**, de lunes a domingo, con
fechas dd/mm/aaaa, horario, periodo y el número de grupos cuando hay varios.

> **Regla:** cambias la hoja, ejecutas el script, commit. Nunca edites a mano lo
> que hay entre las dos marcas: el script lo sobrescribe.

Es el mismo script que usa la otra rama del repo, sin modificar, para que valga
para las dos versiones.

---

## 14. Imágenes en las rutas antiguas

Además de las nuevas en `/img/`, el sitio conserva las **9 imágenes originales
en sus rutas de siempre**, `/s/cc_images/` y `/s/img/`. No se ven en la web,
pero mantienen vivas las URLs que Google Imágenes ya tiene indexadas. El fichero
`.nojekyll` está para que GitHub Pages las sirva tal cual.

De ahí salieron dos mejoras: la foto del trabajador ahora es la de 736x700 en
vez de la de 266x200, y la página *Cómo llegar* recupera el **plano real de
transporte de Móstoles** (líneas de autobús, la DGT, el polígono Los Rosales),
más útil que cualquier esquema dibujado.
