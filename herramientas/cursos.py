#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cursos por semanas, desde la hoja de Google de Pedro, dentro de index.html.

La hoja (pestaña 0) tiene: fila 1 con el título y «Actualizado dd/mm/aaaa hh:mm»;
fila 2 la cabecera «Curso, Horario, Apertura, Cierre, Horas»; y una fila por
convocatoria. «Horario» trae una línea por día: «dd/mm/aaaa de HH:MM a HH:MM».
Las convocatorias sin horario (Personal directivo) son on-line: se ponen con su
periodo. Las filas idénticas son grupos distintos y se juntan («2 grupos»).

Genera HTML ESTÁTICO (Google lo lee; el iframe de Google Calendar no) y lo mete
entre las marcas <!-- CURSOS:INICIO --> y <!-- CURSOS:FIN --> de los ficheros
indicados. Uso:  python3 herramientas/cursos.py [index.html ...]
"""
import csv, io, re, sys, html, os, urllib.request
from datetime import date, datetime, timedelta

# La consola de Windows va en cp1252 y revienta con los acentos y el "OK".
# Sin esto el script hace su trabajo pero termina con un error feo.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass
from collections import OrderedDict

HOJA = "https://docs.google.com/spreadsheets/d/14mcRaWiZxxqZe0Q_Jucohp-oGbQGyQhxz2SwLI1Zc9c/export?format=csv&gid=0"
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def es(d):            # dd/mm/aaaa
    return d.strftime("%d/%m/%Y")

def leer(fuente):
    if fuente.startswith("http"):
        crudo = urllib.request.urlopen(urllib.request.Request(fuente, headers={"User-Agent": "Mozilla/5.0 tpcmetal"}), timeout=30).read().decode("utf-8")
    else:
        crudo = open(fuente, encoding="utf-8").read()
    filas = list(csv.reader(io.StringIO(crudo)))
    titulo = filas[0][0] if filas else ""
    m = re.search(r"Actualizado (\d{2}/\d{2}/\d{4} \d{2}:\d{2})", titulo)
    actualizado = m.group(1) if m else ""
    grupos = OrderedDict()
    for r in filas[2:]:
        if len(r) < 4 or not r[0].strip():
            continue
        curso = re.sub(r"\s+", " ", r[0]).strip()
        horario = r[1].strip()
        try:
            ap = datetime.strptime(r[2].strip(), "%Y-%m-%d").date()
            ci = datetime.strptime(r[3].strip(), "%Y-%m-%d").date()
        except ValueError:
            continue
        sesiones = []
        for m in re.finditer(r"(\d{2})/(\d{2})/(\d{4}) de (\d{2}:\d{2}) a (\d{2}:\d{2})", horario):
            d = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
            sesiones.append((d, m.group(4), m.group(5)))
        clave = (curso, ap, ci, tuple(sesiones))
        grupos[clave] = grupos.get(clave, 0) + 1
    convocatorias = [dict(curso=k[0], apertura=k[1], cierre=k[2], sesiones=list(k[3]), grupos=n) for k, n in grupos.items()]
    return actualizado, convocatorias

def bonito(curso):
    # nombres largos y en mayúsculas de la hoja -> legibles, sin cambiar el sentido
    c = curso
    if c.isupper():
        c = c.capitalize()
    c = c.replace("(6 HORAS)", "(6h)").replace("(6 horas)", "(6h)")
    return c

def semanas(convocatorias):
    if not convocatorias:
        return []
    primero = min(min([c["apertura"]] + [s[0] for s in c["sesiones"]]) for c in convocatorias)
    ultimo = max(max([c["cierre"]] + [s[0] for s in c["sesiones"]]) for c in convocatorias)
    lunes = primero - timedelta(days=primero.weekday())
    salida = []
    while lunes <= ultimo:
        domingo = lunes + timedelta(days=6)
        dias = OrderedDict()
        online = []
        for c in convocatorias:
            for d, h1, h2 in c["sesiones"]:
                if lunes <= d <= domingo:
                    dias.setdefault(d, []).append((h1, h2, c))
            if not c["sesiones"] and lunes <= c["apertura"] <= domingo:
                online.append(c)
        if dias or online:
            salida.append((lunes, domingo, OrderedDict(sorted(dias.items())), online))
        lunes += timedelta(days=7)
    return salida

def generar(actualizado, convocatorias):
    sem = semanas(convocatorias)
    partes = []
    partes.append('<div class="cursos-semanas" id="cursos-semanas">')
    partes.append('  <p class="cursos-nota">Convocatorias abiertas y pendientes en nuestro centro de Móstoles, por semanas de lunes a domingo. '
                  + ('Actualizado el ' + html.escape(actualizado.replace(" ", " a las ")) + '. ' if actualizado else '')
                  + 'Fechas en formato dd/mm/aaaa. Llame para reservar plaza.</p>')
    for lunes, domingo, dias, online in sem:
        partes.append('  <section class="semana">')
        partes.append('    <h3 class="semana-titulo">Semana del %s al %s</h3>' % (es(lunes), es(domingo)))
        for d, lista in dias.items():
            partes.append('    <div class="dia">')
            partes.append('      <h4 class="dia-titulo"><span class="dia-nombre">%s</span> <time datetime="%s">%s</time></h4>' % (DIAS[d.weekday()], d.isoformat(), es(d)))
            partes.append('      <ul class="dia-cursos">')
            for h1, h2, c in sorted(lista, key=lambda x: (x[0], x[2]["curso"])):
                dur = c["cierre"] != c["apertura"]
                extra = (' <span class="curso-periodo">(del %s al %s)</span>' % (es(c["apertura"]), es(c["cierre"]))) if dur else ''
                gr = (' <span class="curso-grupos">%d grupos</span>' % c["grupos"]) if c["grupos"] > 1 else ''
                partes.append('        <li><span class="curso-hora">%s–%s</span> <span class="curso-nombre">%s</span>%s%s</li>' % (h1, h2, html.escape(bonito(c["curso"])), extra, gr))
            partes.append('      </ul>')
            partes.append('    </div>')
        for c in online:
            partes.append('    <div class="dia online"><h4 class="dia-titulo"><span class="dia-nombre">On-line</span></h4><ul class="dia-cursos"><li><span class="curso-nombre">%s</span> <span class="curso-periodo">del %s al %s</span></li></ul></div>'
                          % (html.escape(bonito(c["curso"])), es(c["apertura"]), es(c["cierre"])))
        partes.append('  </section>')
    partes.append('</div>')
    return "\n".join(partes)

def inyectar(fichero, bloque):
    s = open(fichero, encoding="utf-8").read()
    ini, fin = "<!-- CURSOS:INICIO -->", "<!-- CURSOS:FIN -->"
    if ini not in s or fin not in s:
        print("  sin marcas CURSOS:INICIO/FIN en", fichero); return False
    a = s.index(ini) + len(ini); b = s.index(fin)
    s = s[:a] + "\n" + bloque + "\n" + s[b:]
    open(fichero, "w", encoding="utf-8").write(s)
    return True

if __name__ == "__main__":
    fuente = os.environ.get("CURSOS_CSV", HOJA)
    actualizado, conv = leer(fuente)
    bloque = generar(actualizado, conv)
    ficheros = sys.argv[1:] or ["index.html"]
    for f in ficheros:
        if inyectar(f, bloque):
            print("✔", f)
    print("convocatorias:", len(conv), "· semanas:", len(semanas(conv)), "· actualizado:", actualizado)
