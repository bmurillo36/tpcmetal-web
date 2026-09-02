# -*- coding: utf-8 -*-
"""Genera el blog de la web a partir de los artículos en _blog/articulos/*.md.

Cada artículo es un fichero Markdown con una cabecera de datos y el texto:

    titulo: Qué es la Tarjeta Profesional de la Construcción
    descripcion: Resumen de 150 caracteres para Google y redes.
    fecha: 2026-09-07
    slug: que-es-la-tarjeta-profesional-de-la-construccion
    categoria: Tarjeta TPC
    entradilla: Dos frases que abren el artículo bajo el título.

    ## Primer apartado
    Texto en párrafos. **Negrita**, *cursiva*, [enlaces](https://...).
    - listas
    1. numeradas
    > citas

Produce /blog/<slug>/index.html por artículo, /blog/index.html con el listado,
las entradas del sitemap.xml y la sección Blog de llms.txt. No toca nada más.
Se ejecuta desde la raíz del repositorio:  python _blog/generar.py
Markdown mínimo, sin dependencias, para que funcione igual en el PC, el portátil y el servidor.
"""
import os, re, sys, json, html, glob, datetime, io

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
CFG = json.load(open('_blog/config.json', encoding='utf-8'))
PLANTILLA = open('_blog/plantilla.html', encoding='utf-8', newline='').read()
PLANTILLA_INDICE = open('_blog/plantilla-indice.html', encoding='utf-8', newline='').read()
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def fecha_texto(iso):
    a, m, d = iso.split('-')
    return '%d de %s de %s' % (int(d), MESES[int(m) - 1], a)

def slugify(s):
    s = s.lower()
    for a, b in zip('áéíóúüñ', 'aeiouun'): s = s.replace(a, b)
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:80]

def leer_articulo(ruta):
    t = open(ruta, encoding='utf-8-sig').read().replace('\r\n', '\n')
    cab, _, cuerpo = t.partition('\n\n')
    datos = {}
    for linea in cab.splitlines():
        if ':' in linea:
            k, v = linea.split(':', 1); datos[k.strip().lower()] = v.strip()
    faltan = [k for k in ('titulo', 'descripcion', 'fecha') if not datos.get(k)]
    if faltan: raise SystemExit('%s: faltan %s' % (ruta, ', '.join(faltan)))
    datos.setdefault('slug', slugify(datos['titulo']))
    datos.setdefault('categoria', CFG.get('categoria_por_defecto', 'Prevención'))
    datos.setdefault('entradilla', datos['descripcion'])
    datos['cuerpo_md'] = cuerpo.strip()
    datos['fichero'] = ruta
    return datos

# ---------- Markdown mínimo ----------
def en_linea(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)', lambda m: '<a href="%s"%s>%s</a>' % (m.group(2), '' if m.group(2).startswith('/') or CFG['dominio'] in m.group(2) else ' rel="noopener"', m.group(1)), s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
    return s

def md_a_html(md):
    out, parrafo, lista, tipo_lista, cita = [], [], [], None, []
    def cierra_parrafo():
        if parrafo: out.append('<p>%s</p>' % en_linea(' '.join(parrafo))); parrafo.clear()
    def cierra_lista():
        nonlocal tipo_lista
        if lista:
            out.append('<%s>%s</%s>' % (tipo_lista, ''.join('<li>%s</li>' % en_linea(x) for x in lista), tipo_lista)); lista.clear(); tipo_lista = None
    def cierra_cita():
        if cita: out.append('<blockquote><p>%s</p></blockquote>' % en_linea(' '.join(cita))); cita.clear()
    for linea in md.splitlines():
        l = linea.rstrip()
        if not l.strip():
            cierra_parrafo(); cierra_lista(); cierra_cita(); continue
        m = re.match(r'^(#{2,4})\s+(.*)', l)
        if m:
            cierra_parrafo(); cierra_lista(); cierra_cita()
            n = len(m.group(1)); out.append('<h%d>%s</h%d>' % (n, en_linea(m.group(2)), n)); continue
        m = re.match(r'^\s*[-*]\s+(.*)', l)
        if m:
            cierra_parrafo(); cierra_cita()
            if tipo_lista != 'ul': cierra_lista(); tipo_lista = 'ul'
            lista.append(m.group(1)); continue
        m = re.match(r'^\s*\d+[.)]\s+(.*)', l)
        if m:
            cierra_parrafo(); cierra_cita()
            if tipo_lista != 'ol': cierra_lista(); tipo_lista = 'ol'
            lista.append(m.group(1)); continue
        if l.startswith('>'):
            cierra_parrafo(); cierra_lista(); cita.append(l[1:].strip()); continue
        cierra_lista(); cierra_cita(); parrafo.append(l.strip())
    cierra_parrafo(); cierra_lista(); cierra_cita()
    return '\n'.join(out)

# ---------- Render ----------
def rellena(plantilla, valores):
    for k, v in valores.items(): plantilla = plantilla.replace('{{%s}}' % k, v)
    resto = re.findall(r'{{[A-Z_]+}}', plantilla)
    if resto: raise SystemExit('Quedan huecos sin rellenar en la plantilla: %s' % resto)
    return plantilla

def json_ld(a, url):
    d = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": a['titulo'], "description": a['descripcion'],
        "datePublished": a['fecha'], "dateModified": a.get('modificado', a['fecha']),
        "inLanguage": "es", "mainEntityOfPage": url, "url": url,
        "articleSection": a['categoria'],
        "author": {"@type": "Organization", "name": CFG['autor'], "url": CFG['url']},
        "publisher": {"@type": "Organization", "name": CFG['autor'], "url": CFG['url']},
        "isPartOf": {"@type": "Blog", "name": CFG['nombre_blog'], "url": CFG['url'] + CFG['ruta']},
    }
    if CFG.get('imagen'): d['image'] = CFG['url'] + CFG['imagen']
    return json.dumps(d, ensure_ascii=False)

def tarjeta(a):
    url = CFG['ruta'] + a['slug'] + '/'
    return ('<article class="%s"><p class="entrada-meta"><span class="entrada-cat">%s</span> · <time datetime="%s">%s</time></p>'
            '<h3><a href="%s">%s</a></h3><p>%s</p><p><a class="mas" href="%s">Leer el artículo</a></p></article>'
            % (CFG.get('clase_tarjeta', 'tarjeta entrada-blog'), html.escape(a['categoria']), a['fecha'], fecha_texto(a['fecha']), url, html.escape(a['titulo']), html.escape(a['descripcion']), url))

def rejilla(contenido):
    return '<div class="%s">%s</div>' % (CFG.get('clase_rejilla', 'rejilla'), contenido)

def main():
    ficheros = sorted(glob.glob('_blog/articulos/*.md'))
    articulos = [leer_articulo(f) for f in ficheros]
    hoy = datetime.date.today().isoformat()
    publicados = [a for a in articulos if a['fecha'] <= hoy]   # los de fecha futura esperan su día
    publicados.sort(key=lambda a: (a['fecha'], a['slug']), reverse=True)
    vistos = set()
    for a in publicados:
        if a['slug'] in vistos: raise SystemExit('slug repetido: ' + a['slug'])
        vistos.add(a['slug'])

    # artículos
    for i, a in enumerate(publicados):
        url = CFG['url'] + CFG['ruta'] + a['slug'] + '/'
        relacionados = [b for b in publicados if b is not a][:3]
        rel_html = ''.join(tarjeta(b) for b in relacionados) if relacionados else ''
        pagina = rellena(PLANTILLA, {
            'TITULO': html.escape(a['titulo']), 'DESCRIPCION': html.escape(a['descripcion']),
            'URL': url, 'RUTA_BLOG': CFG['ruta'], 'NOMBRE_BLOG': html.escape(CFG['nombre_blog']),
            'FECHA_ISO': a['fecha'], 'FECHA_TEXTO': fecha_texto(a['fecha']),
            'CATEGORIA': html.escape(a['categoria']), 'ENTRADILLA': html.escape(a['entradilla']),
            'CUERPO': md_a_html(a['cuerpo_md']), 'JSONLD': json_ld(a, url),
            'RELACIONADOS': (CFG.get('relacionados_inicio', '<section class="enlaces-rel" aria-labelledby="tit-rel"><h2 id="tit-rel">Más artículos</h2>') + rejilla(rel_html) + CFG.get('relacionados_fin', '</section>')) if rel_html else '',
        })
        carpeta = '.' + CFG['ruta'] + a['slug']
        os.makedirs(carpeta, exist_ok=True)
        open(carpeta + '/index.html', 'w', encoding='utf-8', newline='\n').write(pagina)

    # índice
    indice = rellena(PLANTILLA_INDICE, {
        'URL': CFG['url'] + CFG['ruta'], 'RUTA_BLOG': CFG['ruta'], 'NOMBRE_BLOG': html.escape(CFG['nombre_blog']),
        'DESCRIPCION': html.escape(CFG['descripcion_blog']),
        'LISTADO': rejilla(''.join(tarjeta(a) for a in publicados)) if publicados else '<p>Pronto publicaremos los primeros artículos.</p>',
        'NUMERO': str(len(publicados)),
    })
    os.makedirs('.' + CFG['ruta'], exist_ok=True)
    open('.' + CFG['ruta'] + 'index.html', 'w', encoding='utf-8', newline='\n').write(indice)

    # sitemap
    sm = open('sitemap.xml', encoding='utf-8', newline='').read()
    sm = re.sub(r'\s*<url>\s*<loc>' + re.escape(CFG['url'] + CFG['ruta']) + r'[^<]*</loc>.*?</url>', '', sm, flags=re.S)
    if CFG.get('sitemap_estilo') == 'largo':
        def entrada(loc, fecha, freq, prio):
            return '\n  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>' % (loc, fecha, freq, prio)
        nuevas = entrada(CFG['url'] + CFG['ruta'], publicados[0]['fecha'] if publicados else hoy, 'weekly', '0.8')
        nuevas += ''.join(entrada(CFG['url'] + CFG['ruta'] + a['slug'] + '/', a.get('modificado', a['fecha']), 'monthly', '0.6') for a in publicados)
        sm = sm.replace('\n</urlset>', nuevas + '\n</urlset>')
    else:
        nuevas = '<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (CFG['url'] + CFG['ruta'], publicados[0]['fecha'] if publicados else hoy)
        nuevas += ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (CFG['url'] + CFG['ruta'] + a['slug'] + '/', a.get('modificado', a['fecha'])) for a in publicados)
        sm = sm.replace('</urlset>', nuevas + '</urlset>')
    open('sitemap.xml', 'w', encoding='utf-8', newline='').write(sm)

    # llms.txt
    if os.path.exists('llms.txt'):
        ll = open('llms.txt', encoding='utf-8').read()
        ll = re.sub(r'\n## Blog\n.*?(?=\n## |\Z)', '', ll, flags=re.S).rstrip('\n') + '\n'
        bloque = '\n## Blog\n\n' + ''.join('- [%s](%s%s%s/): %s\n' % (a['titulo'], CFG['url'], CFG['ruta'], a['slug'], a['descripcion']) for a in publicados[:30])
        open('llms.txt', 'w', encoding='utf-8').write(ll + bloque)

    print('blog generado: %d artículos publicados (%d en espera por fecha)' % (len(publicados), len(articulos) - len(publicados)))
    for a in publicados[:10]: print('  ', a['fecha'], CFG['ruta'] + a['slug'] + '/')

if __name__ == '__main__':
    main()
