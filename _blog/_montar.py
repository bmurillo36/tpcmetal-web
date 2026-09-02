# -*- coding: utf-8 -*-
"""Montaje inicial del blog de tpcmetal.es (rama editorial), hecho el 02/09/2026. Se deja por si hay que rehacer la plantilla.
1) enlace «Blog» en el menú, el menú móvil y el pie de todas las páginas;
2) plantillas _blog/plantilla.html y _blog/plantilla-indice.html a partir de contacto/index.html, con rutas absolutas;
3) CSS del blog en css/editorial.css."""
import os, re, glob, io, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(RAIZ)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
def rd(p): return open(p, encoding='utf-8', newline='').read()
def wr(p, t): open(p, 'w', encoding='utf-8', newline='').write(t)

# 1. enlaces Blog
n = 0
for p in ['index.html'] + glob.glob('*/index.html') + ['404.html']:
    if not os.path.exists(p) or p.startswith('blog/'): continue
    t = rd(p); o = t
    if 'href="/blog/"' not in t:
        # menú de escritorio: antes del enlace a Cómo llegar
        t = re.sub(r'(\n\s*)(<a href="(?:\.\./|\./)?c(?:%C3%B3|ó)mo-llegar/">Cómo llegar</a>)', r'\1<a href="/blog/">Blog</a>\1\2', t, count=1)
        # menú móvil: antes del li de Cómo llegar
        t = re.sub(r'(\n\s*)(<li><a href="(?:\.\./|\./)?c(?:%C3%B3|ó)mo-llegar/">Cómo llegar</a></li>)', r'\1<li><a href="/blog/">Blog</a></li>\1\2', t, count=1)
        # pie: columna Web, después de Cómo llegar
        t = re.sub(r'(<li><a href="(?:\.\./|\./)?c(?:%C3%B3|ó)mo-llegar/">Cómo llegar</a></li>)(\n\s*)(<li><a href="(?:\.\./|\./)?aviso-legal/">)', r'\1\2<li><a href="/blog/">Blog</a></li>\2\3', t, count=1)
    if t != o: wr(p, t); n += 1
print('páginas con enlace Blog:', n)

# 2. plantillas a partir de contacto/index.html
t = rd('contacto/index.html').replace('\r\n', '\n')
i = t.find('<header class="masthead">'); j = t.find('<main id="main">'); k = t.find('</main>')
cab, cabecera, pie = t[:i], t[i:j], t[k + len('</main>'):]
def absolutas(s):
    s = s.replace('href="../', 'href="/').replace('src="../', 'src="/').replace('href="./"', 'href="/"')
    s = re.sub(r'href="(#[a-z]+)"', r'href="/\1"', s)
    s = re.sub(r'href="(c(?:%C3%B3|ó)mo-llegar/|aviso-legal/|pol(?:%C3%AD|í)tica-de-cookies/|contacto/|sitemap/)"', r'href="/\1"', s)
    return s
cab, cabecera, pie = absolutas(cab), absolutas(cabecera), absolutas(pie)
cab = re.sub(r'<title>.*?</title>', '<title>{{TITULO}} | Tarjeta TPC Sector del Metal</title>', cab, flags=re.S)
cab = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="{{DESCRIPCION}}">', cab)
cab = re.sub(r'<meta name="keywords" content="[^"]*">\n?', '', cab)
cab = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="{{URL}}">', cab)
cab = re.sub(r'<link rel="alternate" hreflang="es-ES" href="[^"]*">', '<link rel="alternate" hreflang="es-ES" href="{{URL}}">', cab)
cab = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">', cab)
cab = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="{{URL}}">', cab)
cab = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="{{TITULO}}">', cab)
cab = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="{{DESCRIPCION}}">', cab)
cab = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">{{JSONLD}}</script>', cab, count=1, flags=re.S)
assert cab.count('{{JSONLD}}') == 1 and 'href="/css/editorial.css"' in cab
# aria-current del menú: quitarlo (no estamos en Inicio)
cabecera = cabecera.replace(' aria-current="page"', '')
articulo = ('<main id="main">\n\n<section class="section section--tight grid">\n  <div class="col-lead">\n'
            '    <nav class="eyebrow eyebrow--steel" aria-label="Ruta de navegación" style="margin-bottom:2rem">\n'
            '      <a href="/" style="color:inherit;text-decoration:none">Inicio</a> · <a href="{{RUTA_BLOG}}" style="color:inherit;text-decoration:none">Blog</a> · <span style="color:var(--ember)">{{CATEGORIA}}</span>\n    </nav>\n'
            '    <h1 class="display" style="max-width:18ch">{{TITULO}}</h1>\n'
            '    <p class="lead" style="margin-top:1.5rem">{{ENTRADILLA}}</p>\n'
            '    <p class="entrada-meta"><time datetime="{{FECHA_ISO}}">{{FECHA_TEXTO}}</time> · Prevención Siglo 21</p>\n  </div>\n</section>\n\n'
            '<section class="section section--tight grid">\n  <div class="col-text">\n    <article class="articulo body">\n{{CUERPO}}\n'
            '      <div class="btn-row" style="margin-top:2.5rem"><a class="btn btn--ember" href="tel:+34630292516">Llamar al 630 29 25 16</a><a class="btn btn--ghost" href="/contacto/">Pedir información</a></div>\n'
            '    </article>\n  </div>\n</section>\n\n{{RELACIONADOS}}\n\n</main>')
wr('_blog/plantilla.html', cab + cabecera + articulo + pie)
cab_i = cab.replace('<title>{{TITULO}} | Tarjeta TPC Sector del Metal</title>', '<title>{{NOMBRE_BLOG}} | Cursos y trámites de la TPC del metal</title>')
cab_i = cab_i.replace('<meta property="og:title" content="{{TITULO}}">', '<meta property="og:title" content="{{NOMBRE_BLOG}}">').replace('content="article"', 'content="website"')
cab_i = cab_i.replace('<script type="application/ld+json">{{JSONLD}}</script>', '<script type="application/ld+json">{"@context":"https://schema.org","@type":"Blog","name":"{{NOMBRE_BLOG}}","url":"{{URL}}","description":"{{DESCRIPCION}}","publisher":{"@type":"Organization","name":"Prevención Siglo 21","url":"https://www.tpcmetal.es"}}</script>')
indice = ('<main id="main">\n\n<section class="section section--tight grid">\n  <div class="col-lead">\n'
          '    <nav class="eyebrow eyebrow--steel" aria-label="Ruta de navegación" style="margin-bottom:2rem"><a href="/" style="color:inherit;text-decoration:none">Inicio</a> · <span style="color:var(--ember)">Blog</span></nav>\n'
          '    <h1 class="display" style="max-width:14ch">{{NOMBRE_BLOG}}</h1>\n    <p class="lead" style="margin-top:1.5rem">{{DESCRIPCION}}</p>\n  </div>\n</section>\n\n'
          '<section class="section section--warm">\n  <div class="grid">\n    <div class="col-main">\n      <p class="eyebrow">Artículos ({{NUMERO}})</p>\n{{LISTADO}}\n    </div>\n  </div>\n</section>\n\n</main>')
wr('_blog/plantilla-indice.html', cab_i + cabecera + indice + pie)
print('plantillas escritas')

# 3. CSS
c = rd('css/editorial.css')
if '.articulo{' not in c:
    c = c.rstrip('\n') + ('\n/* Blog */\n.articulo{max-width:var(--measure)}.articulo h2{margin:2.2rem 0 .8rem;font-family:var(--font-display);font-size:1.7rem;line-height:1.15}'
        '.articulo h3{margin:1.8rem 0 .6rem;font-size:1.15rem}.articulo p{margin:0 0 1.1rem}.articulo ul,.articulo ol{margin:0 0 1.1rem;padding-left:1.4rem}.articulo li{margin-bottom:.4rem}'
        '.articulo blockquote{margin:1.4rem 0;padding:.9rem 1.2rem;border-left:3px solid var(--ember);background:var(--paper-warm)}.articulo blockquote p{margin:0;font-size:.95rem}'
        '.entrada-meta{font-size:.9rem;color:var(--ink-soft);margin-top:1rem}.entrada-cat{font-weight:600;color:var(--ember);text-transform:uppercase;letter-spacing:.06em;font-size:.75rem}'
        '.entrada-blog h3{margin:.4rem 0 .5rem;font-family:var(--font-display);font-size:1.35rem;line-height:1.2}.entrada-blog h3 a{color:inherit;text-decoration:none}.entrada-blog h3 a:hover{color:var(--ember)}'
        '.entrada-blog .mas{font-weight:600;color:var(--ember);text-decoration:none}.entrada-blog .mas:hover{text-decoration:underline}\n')
    wr('css/editorial.css', c); print('css del blog añadido')
