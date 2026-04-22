#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generación páginas RYC 2026 — Tercera revisión
!SALIDA/ ES el repositorio git — el script genera directamente aquí.
  Español -> !SALIDA/  (index.html, novedades-2026.html, programa-ryc.html, convocatorias.html)
  Inglés  -> !SALIDA/ing/
Mismos ficheros para GitHub Pages y para entregar a Drupal.
"""
import base64, os, re, io
from PIL import Image

PROYECTO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC      = PROYECTO + "/!ENTRADA/04-tercera-revision"
SRC_R4   = PROYECTO + "/!ENTRADA/05-cuarta revision"   # 4ª revisión (dev team)
BASE     = PROYECTO + "/!SALIDA"   # raíz del repo git
OUT_ESP  = BASE
OUT_ING  = BASE + "/ing"

os.makedirs(OUT_ING, exist_ok=True)

# ---- IMÁGENES ----
def resize64(fname, max_w, max_h, quality=85, fmt='JPEG'):
    path = SRC + '/' + fname
    img = Image.open(path)
    if img.mode in ('RGBA', 'P'):
        if fmt == 'JPEG':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                bg.paste(img, mask=img.split()[3])
            else:
                bg.paste(img)
            img = bg
        else:
            img = img.convert('RGBA')
    w, h = img.size
    ratio = min(max_w / w, max_h / h) if (w > max_w or h > max_h) else 1
    if ratio < 1:
        img = img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == 'JPEG':
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        mime = 'image/jpeg'
    else:
        img.save(buf, format='PNG', optimize=True)
        mime = 'image/png'
    d = base64.b64encode(buf.getvalue()).decode('ascii')
    print(f'  {fname}: {img.size} -> {len(d)//1024}KB')
    return f'data:{mime};base64,{d}'

print('Cargando imágenes...')
nov2 = resize64('Novedades - 2 Entrevista.png',         1200, 400)
nov4 = resize64('Novedades - 4 Estabilización.png',     1200, 400)
nov5 = resize64('Novedades - 5 Integración convocatorias.png', 1200, 400)
prog = resize64('Programa - Impacto - Excavación.png',  1200, 400)
eu   = resize64('MICIU+Cofinanciado+AEI.jpg',            800, 200, fmt='PNG')
print('OK\n')

# ---- LIMPIEZA DE REFERENCIAS A FOOTER ----
# Los fragmentos pagina*.txt traen un bloque CSS `.footer/.footer-grid/.footer-bottom`
# y un comentario <!-- ===== FOOTER ===== --> heredado de una maqueta previa.
# En Drupal no queremos NADA relacionado con footer en el HTML pegado:
#   - el footer institucional lo pinta Drupal con sus propias clases `.footer` / `<footer>`
#   - cualquier regla `.footer { ... }` en el CSS embebido estiliza (o rompe) el footer de Drupal
#   - un `display: none` sobre selectores `footer` se cargaría el footer institucional entero
# Por eso aquí NO inyectamos ningún `display: none` sobre footer, y además eliminamos
# las reglas CSS y el comentario HTML con `strip_footer_refs()`.

FOOTER_CSS_BLOCK_RE = re.compile(
    r'/\*\s*-{2,}\s*Footer\s*-{2,}\s*\*/.*?(?=/\*\s*-{2,}\s*[^-])',
    re.DOTALL | re.IGNORECASE,
)
FOOTER_BODY_COMMENT_RE = re.compile(r'\n?<!--\s*=+\s*FOOTER\s*=+\s*-->\n?')

def strip_footer_refs(content):
    """Elimina del fragmento todas las referencias a footer para que Drupal conserve el suyo."""
    content = FOOTER_CSS_BLOCK_RE.sub('', content)
    content = FOOTER_BODY_COMMENT_RE.sub('\n', content)
    return content


# ---- AISLAMIENTO EN WRAPPER .ryc-page ----
# El fragmento que se pega en Drupal debe afectar SOLO a su propio contenedor.
# - Se envuelve todo el HTML del body en <div class="ryc-page">…</div>.
# - Las reglas CSS globales (body, html, *, img, a, main) se reescriben para
#   que solo apliquen dentro de .ryc-page; así no cambian la estética del
#   resto del portal de la AEI.
# - Las variables de :root se mantienen (solo declaran custom properties;
#   no estilan nada por sí mismas).
# - Las reglas con clase propia (.algo, .hero-…) ya están bastante aisladas
#   por el nombre, y las nuevas se nombran con prefijo .ryc-*.
WRAPPER_CLASS = 'ryc-page'

GLOBAL_CSS_SCOPE = [
    # Reset box-sizing: aislamos DENTRO del wrapper pero con :where() para no añadir
    # especificidad — si no, "* { box-sizing }" con especificidad 0,0,0 pasaría a 0,1,0
    # y podría pisar reglas más específicas inesperadamente.
    (re.compile(r'^\s*\*\s*,\s*\n?\s*\*::before\s*,\s*\n?\s*\*::after\s*\{', re.M),
     f':where(.{WRAPPER_CLASS}, .{WRAPPER_CLASS} *, .{WRAPPER_CLASS} *::before, .{WRAPPER_CLASS} *::after) {{'),
    # body / html / main: reescribimos a `.ryc-page` (especificidad 0,1,0) porque QUEREMOS
    # que estas reglas base (tipografía, color de fondo…) ganen sobre el tema de Drupal.
    (re.compile(r'^\s*html\s*\{',     re.M), f'.{WRAPPER_CLASS} {{'),
    (re.compile(r'^\s*body\s*\{',     re.M), f'.{WRAPPER_CLASS} {{'),
    (re.compile(r'^\s*main\s*\{',     re.M), f'.{WRAPPER_CLASS} main {{'),
    # img / a / a:hover: reescribimos a `:where(.ryc-page) img` para mantener la
    # especificidad original (0,0,1). Así las reglas con clase (p.ej.
    # `.cofinanciacion-logos { height: 72px }`, `.btn-ryc { color: #fff }`,
    # `.novedad-banda img { max-height: 320px }`) siguen ganando como antes,
    # y la regla global solo aporta lo mínimo imprescindible.
    (re.compile(r'^\s*img\s*\{',      re.M), f':where(.{WRAPPER_CLASS}) img {{'),
    (re.compile(r'^\s*a\s*\{',        re.M), f':where(.{WRAPPER_CLASS}) a {{'),
    (re.compile(r'^\s*a:hover\s*\{',  re.M), f':where(.{WRAPPER_CLASS}) a:hover {{'),
]

def scope_global_css(content):
    """Reescribe las reglas CSS globales para que solo afecten dentro de .ryc-page."""
    for pat, repl in GLOBAL_CSS_SCOPE:
        content = pat.sub(repl, content)
    return content

RYC_PAGE_END_MARKER = '<!-- /.ryc-page -->'

def wrap_in_page_container(content):
    """Envuelve el HTML del fragmento (todo lo que va tras el último </style>) en .ryc-page.

    Añade un marcador `<!-- /.ryc-page -->` justo antes del cierre `</div>` del wrapper
    para poder insertar la sección de cofinanciación UE como ÚLTIMA sección DENTRO del
    wrapper (ver `add_banner`)."""
    idx = content.rfind('</style>')
    if idx == -1:
        return f'<div class="{WRAPPER_CLASS}">\n{content}\n{RYC_PAGE_END_MARKER}\n</div>'
    cut = idx + len('</style>')
    return (content[:cut]
            + f'\n<div class="{WRAPPER_CLASS}">\n'
            + content[cut:]
            + f'\n{RYC_PAGE_END_MARKER}\n</div>\n')


# ---- LIMPIAR JS LEGACY DE RENDER DE CONVOCATORIAS ----
# El convocatorias.txt de la 4ª revisión incluye, como referencia, un <script>
# que renderizaba las tarjetas dinámicamente a partir de un array JS. Ya no es
# necesario: el HTML de las cards viene pre-renderizado con clases .ryc-card.
# Además, ese JS buscaba un id="lista-convocatorias" que no existe en la nueva
# estructura, y fallaría con un error al intentar hacer contenedor.appendChild.
CONV_RENDER_JS_RE = re.compile(
    r'<script>\s*/\*\s*=+\s*\n*\s*DATOS DE CONVOCATORIAS.*?</script>',
    re.DOTALL
)

def strip_convocatorias_render_js(content):
    """Elimina el primer <script> (datos + render dinámico) del fragmento de convocatorias."""
    return CONV_RENDER_JS_RE.sub('', content)

# ---- CSS BANNER ----
BANNER_CSS = """
/* --- Banner cofinanciación EU --- */
.banner-cofinanciacion {
  background: var(--fondo-blanco);
  border-top: 1px solid var(--borde-suave);
  margin-top: 2rem;
  padding: 1.25rem 1rem;
}
.banner-cofinanciacion .container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.cofinanciacion-logos { height: 72px; width: auto; flex-shrink: 0; }
.cofinanciacion-texto { margin: 0; font-size: 0.95rem; color: var(--texto-secundario); line-height: 1.5; }
@media (max-width: 600px) {
  .banner-cofinanciacion .container { flex-direction: column; align-items: flex-start; gap: 0.75rem; }
}
"""

# ---- CSS FIX CONVOCATORIAS ----
CONV_FIX = """
/* === FIX Drupal: tarjetas convocatorias (estructura año-bloque) === */
.convocatoria-card {
  background-color: #ffffff !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: center !important;
  flex-wrap: nowrap !important;
  gap: 1rem !important;
}
.convocatoria-card.vigente {
  background: linear-gradient(90deg, rgba(27,76,150,0.03), #ffffff) !important;
}
.convocatoria-anio {
  flex: 0 0 auto !important;
  background: var(--aei-azul) !important;
  color: var(--texto-claro) !important;
  padding: 0.45rem 0.7rem !important;
  border-radius: 4px !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
  min-width: 3.5rem !important;
  text-align: center !important;
  line-height: 1 !important;
  white-space: nowrap !important;
  display: inline-block !important;
}
.convocatoria-info {
  flex: 1 1 auto !important;
  min-width: 0 !important;
}
.convocatoria-info h3 {
  display: block !important;
  margin: 0 0 0.25rem !important;
}
.convocatoria-card > a,
.convocatoria-card > span,
.convocatoria-card .btn-aei,
.convocatoria-card .btn-ryc,
.convocatoria-card a[class^="btn"] {
  flex: 0 0 auto !important;
  flex-shrink: 0 !important;
  white-space: nowrap !important;
  display: inline-block !important;
}
@media (max-width: 600px) {
  .convocatoria-card {
    flex-direction: column !important;
    align-items: flex-start !important;
  }
  .convocatoria-card > a,
  .convocatoria-card > span { align-self: stretch !important; text-align: center !important; }
}
"""

def eu_banner_html(lang='es'):
    txt = ('El Programa Ramón y Cajal está cofinanciado por la Unión Europea'
           if lang == 'es' else
           'The Ramón y Cajal Programme is co-funded by the European Union')
    alt = ('Ministerio de Ciencia e Innovación — Cofinanciado por la Unión Europea — AEI'
           if lang == 'es' else
           'Ministry of Science and Innovation — Co-funded by the European Union — AEI')
    # Se inserta como <section> dentro de <main> (última del cuerpo de la página),
    # NUNCA como <footer>: el footer lo pone Drupal.
    return f'''
<!-- ===== COFINANCIACIÓN UE (sección del cuerpo, última del main) ===== -->
<section class="banner-cofinanciacion">
  <div class="container">
    <img src="{eu}" alt="{alt}" class="cofinanciacion-logos">
    <p class="cofinanciacion-texto">{txt}</p>
  </div>
</section>
'''

# ---- LEER PÁGINAS ----
def rpage(n):
    with open(SRC + f'/pagina {n}.txt', 'r', encoding='utf-8') as f:
        return f.read()

# p1-p3: páginas 1-3 siguen viniendo de la 3ª revisión.
# p4 (convocatorias): 4ª revisión — el dev team ha entregado una versión
# ya validada en Drupal, con cards estáticas y clases BEM prefijadas (.ryc-*).
def r_convocatorias_4r():
    with open(SRC_R4 + '/convocatorias.txt', 'r', encoding='utf-8') as f:
        return f.read()

p1, p2, p3 = rpage(1), rpage(2), rpage(3)
p4 = r_convocatorias_4r()

# ---- CAMBIOS DE IMÁGENES ----
# pagina 2: novedad 2 (entrevista unsplash)
p2 = p2.replace(
    'src="https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&amp;h=400&amp;fit=crop&amp;crop=top" style="object-position: center 55%;"',
    f'src="{nov2}"')

# pagina 2: novedad 4 (edificio AEI en la banda del número 4)
p2 = re.sub(
    r'(src="https://ramirez-santigosa\.github\.io/ryc-web/assets/edificio-aei-bandera\.jpg" />)(\s*<div class="banda-titulo"><span class="novedad-numero">4</span>)',
    lambda m: f'src="{nov4}" />' + m.group(2),
    p2)

# pagina 2: novedad 5 (dron AEI)
p2 = p2.replace(
    'src="https://ramirez-santigosa.github.io/ryc-web/assets/aei-dron.png" style="filter: brightness(1.7) contrast(0.9); object-position: center 70%;"',
    f'src="{nov5}"')

# pagina 3: impacto (conferencia-lateral)
p3 = p3.replace(
    'src="/sites/default/files/inline-images/conferencia-lateral.jpg"',
    f'src="{prog}"')

# ---- INYECTAR CSS EN EL ÚLTIMO </style> DE CADA PÁGINA ----
def inject_css(content, extra):
    # Find last </style> and inject before it
    idx = content.rfind('</style>')
    if idx == -1:
        return content
    return content[:idx] + extra + '\n</style>' + content[idx+8:]

# Limpiar el JS legacy de render dinámico del fragmento de convocatorias (4ª revisión)
p4 = strip_convocatorias_render_js(p4)

# Primero eliminamos todas las referencias a footer (CSS + comentario HTML)
p1 = strip_footer_refs(p1)
p2 = strip_footer_refs(p2)
p3 = strip_footer_refs(p3)
p4 = strip_footer_refs(p4)

# La página de convocatorias ya trae sus propias reglas .ryc-card robustas;
# no necesita CONV_FIX (que era un parche para la estructura antigua).
EXTRA_CSS_P = BANNER_CSS
p1 = inject_css(p1, EXTRA_CSS_P)
p2 = inject_css(p2, EXTRA_CSS_P)
p3 = inject_css(p3, EXTRA_CSS_P)
p4 = inject_css(p4, EXTRA_CSS_P)

# Aislar estilos: scopar reglas globales + envolver HTML en .ryc-page.
# IMPORTANTE: esto debe hacerse ANTES de add_banner, para que el banner se
# inserte DENTRO del wrapper (antes del marcador <!-- /.ryc-page -->).
p1 = wrap_in_page_container(scope_global_css(p1))
p2 = wrap_in_page_container(scope_global_css(p2))
p3 = wrap_in_page_container(scope_global_css(p3))
p4 = wrap_in_page_container(scope_global_css(p4))

# ---- AÑADIR BANNER EU COMO ÚLTIMA SECCIÓN DENTRO DEL WRAPPER .ryc-page ----
# El banner va DENTRO del cuerpo de la página, NUNCA en un <footer>: el footer
# institucional lo pinta Drupal.
# Se inserta antes del marcador `<!-- /.ryc-page -->` que añade wrap_in_page_container.
# Como fallback (si no hay wrapper todavía) se usa `</main>`.
def add_banner(content, lang='es'):
    if RYC_PAGE_END_MARKER in content:
        return content.replace(RYC_PAGE_END_MARKER,
                               eu_banner_html(lang) + '\n' + RYC_PAGE_END_MARKER, 1)
    if '</main>' in content:
        return content.replace('</main>', eu_banner_html(lang) + '</main>', 1)
    return content + eu_banner_html(lang)

p1 = add_banner(p1)
# p2 (novedades 2026) NO lleva banner de cofinanciación UE — indicación 4ª revisión
p3 = add_banner(p3)
p4 = add_banner(p4)


# ---- ACTUALIZAR ENLACES NAV (español) ----
NAV_ES = {
    'href="https://www.aei.gob.es/inicio-ryc"':         'href="index.html"',
    'href="https://www.aei.gob.es/novedades-ryc-2026"': 'href="novedades-2026.html"',
    'href="https://www.aei.gob.es/programa-ryc-2026"':  'href="programa-ryc.html"',
    'href="https://www.aei.gob.es/convocatorias-ryc"':  'href="convocatorias.html"',
    'href="https://www.aei.gob.es/novedades-ryc-2026" rel=" noopener" target="_blank"': 'href="novedades-2026.html"',
    'href="https://www.aei.gob.es/convocatorias-ryc" rel=" noopener" target="_blank"':  'href="convocatorias.html"',
    'href="https://www.aei.gob.es/programa-ryc-2026" rel=" noopener" target="_blank"':  'href="programa-ryc.html"',
    "'https://www.aei.gob.es/novedades-ryc-2026'": "'novedades-2026.html'",
}

def apply_nav(content, nav_map):
    for old, new in nav_map.items():
        content = content.replace(old, new)
    return content

p1 = apply_nav(p1, NAV_ES)
p2 = apply_nav(p2, NAV_ES)
p3 = apply_nav(p3, NAV_ES)
p4 = apply_nav(p4, NAV_ES)

# ---- ENVOLVER EN HTML MÍNIMO (CSS queda en el body → válido para Drupal y navegador) ----
def wrap_fragment(content, title, lang='es'):
    # Eliminar meta charset/viewport y title del fragmento (los ponemos en el head limpio)
    content = re.sub(r'^<meta charset="UTF-8"><meta[^>]+>\s*\n?', '', content)
    content = re.sub(r'^<title>[^<]*</title>\s*\n?', '', content)
    # Los <style> se quedan en el body: Drupal los conserva, el navegador los renderiza igual
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
</head>
<body>
{content.strip()}
</body>
</html>"""

html_p1 = wrap_fragment(p1, 'Inicio — Programa Ramón y Cajal')
html_p2 = wrap_fragment(p2, 'Novedades 2026 — Programa Ramón y Cajal')
html_p3 = wrap_fragment(p3, 'Programa RYC — Agencia Estatal de Investigación')
html_p4 = wrap_fragment(p4, 'Convocatorias — Programa Ramón y Cajal')

# ---- ESCRIBIR ESPAÑOL (raíz) ----
print('Generando español...')
pages_es = [
    ('index.html',          html_p1),
    ('novedades-2026.html', html_p2),
    ('programa-ryc.html',   html_p3),
    ('convocatorias.html',  html_p4),
]
for fname, content in pages_es:
    with open(OUT_ESP + '/' + fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  {fname}  {len(content)//1024}KB')

# ==============================================================
# TRADUCCIÓN AL INGLÉS
# ==============================================================
EN_TRANS = [
    # Nav
    ('>Inicio RYC<',        '>RYC Home<'),
    ('>Novedades 2026<',    '>2026 Updates<'),
    ('>Programa RYC<',      '>RYC Programme<'),
    ('>Convocatorias<',     '>Calls<'),
    ('>25 Años RYC<',       '>25 Years RYC<'),
    ('aria-label="Abrir menú"', 'aria-label="Open menu"'),
    ('aria-label="Navegación principal"', 'aria-label="Main navigation"'),
    # EU banner
    ('El Programa Ramón y Cajal está cofinanciado por la Unión Europea',
     'The Ramón y Cajal Programme is co-funded by the European Union'),
    ('Ministerio de Ciencia e Innovación — Cofinanciado por la Unión Europea — AEI',
     'Ministry of Science and Innovation — Co-funded by the European Union — AEI'),
    # Breadcrumb
    ('aria-label="Ruta de navegación"', 'aria-label="Breadcrumb"'),
    # Meta description (index)
    ('content="Convocatoria de ayudas del Programa Ramón y Cajal (RYC) de la Agencia Estatal de Investigación. Incorporación de personal investigador posdoctoral destacado al sistema español de I+D+i."',
     'content="Grant call for the Ramón y Cajal Programme (RYC) of the State Research Agency. Incorporation of outstanding postdoctoral researchers into the Spanish R&amp;D&amp;I system."'),
    # Page 1 - Hero
    ('Programa <span>Ramón y Cajal</span>',
     '<span>Ramón y Cajal</span> Programme'),
    ('Incorporamos al mejor personal investigador posdoctoral al sistema español de ciencia, tecnología e innovación. Desde 2001, impulsando la excelencia científica.',
     'We incorporate the best postdoctoral researchers into the Spanish science, technology and innovation system. Since 2001, driving scientific excellence.'),
    ('>Ver convocatorias<', '>View calls<'),
    # Page 1 - Section ¿Qué es?
    ('¿Qué es el Programa Ramón y Cajal?',
     'What is the Ramón y Cajal Programme?'),
    ('El Programa Ramón y Cajal promueve la incorporación de personal investigador posdoctoral, de todas las nacionalidades y áreas de conocimiento, con una trayectoria destacada, en organismos de investigación del Sistema Español de Ciencia, Tecnología e Innovación.',
     'The Ramón y Cajal Programme promotes the incorporation of postdoctoral researchers of all nationalities and knowledge areas, with outstanding careers, into research organisations of the Spanish Science, Technology and Innovation System.'),
    ('Desde su primera convocatoria en 2001, el programa ha sido el principal instrumento para atraer y retener talento investigador en España, con el objetivo de que las personas beneficiarias adquieran las competencias y capacidades que les permitan obtener un puesto de carácter estable.',
     'Since its first call in 2001, the programme has been the main instrument to attract and retain research talent in Spain, with the aim that fellows acquire the skills and capabilities to obtain a permanent position.'),
    ('El programa se ha reforzado desde 2018 incrementando el número de contratos y el salario mínimo de los beneficiarios.',
     'The programme has been strengthened since 2018 by increasing the number of contracts and the minimum salary of fellows.'),
    ('Años de convocatorias',    'Years of calls'),
    ('Años de duración de la ayuda', 'Years of fellowship duration'),
    ('>Conocer el programa<',    '>Learn about the programme<'),
    ('alt="Sede de la Agencia Estatal de Investigación" class="seccion-imagen"',
     'alt="Headquarters of the State Research Agency" class="seccion-imagen"'),
    # Page 1 - Novedades
    ('Novedades de la Convocatoria 2026', '2026 Call Updates'),
    ('Financiación de un proyecto propio de I+D+i',
     'Funding for an own R&amp;D&amp;I project'),
    ('Cada ayuda incluirá financiación para un proyecto de investigación de 5 años, con dotación suficiente para contratar al menos una persona investigadora predoctoral durante 4 años.',
     'Each fellowship will include funding for a 5-year research project, with sufficient allocation to hire at least one predoctoral researcher for 4 years.'),
    ('Entrevista en el proceso de evaluación',
     'Interview in the evaluation process'),
    ('Se incorpora una entrevista en el proceso de evaluación, poniendo el foco en el grado de independencia y la capacidad de liderazgo y la viabilidad del proyecto.',
     'An interview is incorporated into the evaluation process, focusing on the degree of independence, leadership capacity and project viability.'),
    ('Incentivos para participar en el ERC',
     'Incentives to participate in ERC calls'),
    ('Hasta un 30% de incremento en la cofinanciación del salario y acceso a Europa Excelencia para quienes concurran a convocatorias del Consejo Europeo de Investigación.',
     'Up to a 30% increase in salary co-funding and access to Europa Excelencia for those applying to European Research Council calls.'),
    ('<h3>Estabilización obligatoria con incentivo</h3>',
     '<h3>Mandatory stabilisation with incentive</h3>'),
    ('La creación de un puesto permanente en el área de la persona beneficiaria de la ayuda Ramón y Cajal será requisito obligatorio, apoyado con una incentivación para la entidad beneficiaria.',
     "The creation of a permanent position in the fellow's area will be mandatory, supported by an incentive for the host institution."),
    ('Integración con Consolidación Investigadora',
     'Integration with Research Consolidation'),
    ('La convocatoria de Consolidación Investigadora se suprime: sus objetivos quedan cubiertos por la nueva estructura de las ayudas RYC.',
     'The Research Consolidation call is abolished: its objectives are covered by the new structure of RYC fellowships.'),
    ('>Ver todas las novedades en detalle<', '>See all updates in detail<'),
    # Page 1 - Convocatorias recientes
    ('Convocatorias recientes', 'Recent calls'),
    ('Convocatoria Ramón y Cajal 2026', 'Ramón y Cajal 2026 Call'),
    ('Próxima publicación — Nuevas condiciones', 'Upcoming publication — New conditions'),
    ('>Ver novedades<', '>View updates<'),
    ('Convocatoria Ramón y Cajal 2025', 'Ramón y Cajal 2025 Call'),
    # Página 4 (convocatorias.txt 4ª revisión) — estados con coletilla (reglas específicas ANTES
    # de las genéricas "Resuelta"/"En tramitación" para que no las "corten" por la mitad).
    ('>Próxima — Nuevas condiciones: proyecto propio, entrevista, incentivos ERC<',
     '>Upcoming — New conditions: own project, interview, ERC incentives<'),
    ('>Resuelta — Incorpora la obligatoriedad de estabilización<',
     '>Resolved — Incorporates mandatory stabilisation<'),
    ('>Resuelta — Se introduce la ayuda para la atracción de talento y la división en dos fases<',
     '>Resolved — Talent attraction grant and two-phase structure introduced<'),
    ('>Resuelta — Modalidad investigador/a novel (suprimida en 2022)<',
     '>Resolved — Early-career researcher track (discontinued in 2022)<'),
    ('En tramitación', 'In progress'),
    ('Convocatoria Ramón y Cajal 2024', 'Ramón y Cajal 2024 Call'),
    ('Resuelta', 'Resolved'),
    ('Convocatoria Ramón y Cajal 2023', 'Ramón y Cajal 2023 Call'),
    ('>Ver histórico completo<', '>View full history<'),
    # Page 1 - Cards
    ('Enlaces de interés', 'Useful links'),
    ('25 Años de Ramón y Cajal', '25 Years of Ramón y Cajal'),
    ('Web conmemorativa con la historia, testimonios e hitos del programa a lo largo de un cuarto de siglo de excelencia científica.',
     'Commemorative website with the history, testimonials and milestones of the programme over a quarter century of scientific excellence.'),
    ('>Visitar<', '>Visit<'),
    ('Vídeo: Novedades RYC 2026', 'Video: RYC 2026 Updates'),
    ('Presentación en vídeo de los cambios sustanciales de la convocatoria 2026 del programa Ramón y Cajal.',
     'Video presentation of the substantial changes in the 2026 Ramón y Cajal Programme call.'),
    ('>Ver vídeo<', '>Watch video<'),
    ('Web de la AEI', 'AEI Website'),
    ('Portal principal de la Agencia Estatal de Investigación con toda la información sobre convocatorias, ayudas y programas.',
     'Main portal of the State Research Agency with all information on calls, grants and programmes.'),
    ('>Ir a la AEI<', '>Go to the AEI<'),
    ('Convocatorias AEI', 'AEI Calls'),
    ('Buscador de todas las convocatorias de la Agencia Estatal de Investigación, incluyendo Ramón y Cajal.',
     'Search engine for all State Research Agency calls, including Ramón y Cajal.'),
    ('>Ver convocatorias<', '>View calls<'),
    ('Programa de ayudas para personas investigadoras que han participado en convocatorias del ERC sin obtener financiación.',
     'Fellowship programme for researchers who have participated in ERC calls without obtaining funding.'),
    ('>Más información<', '>More information<'),
    # Page 2 - Hero
    ('La convocatoria <span>Ramón y Cajal</span> se transforma en 2026',
     'The <span>Ramón y Cajal</span> call transforms in 2026'),
    ('Cambios sustanciales para fortalecer la carrera investigadora e impulsar la excelencia de las universidades y los centros de investigación.',
     'Substantial changes to strengthen research careers and boost excellence in universities and research centres.'),
    ('¿Para qué cambia la convocatoria?', 'Why is the call changing?'),
    ('Fortalecer la carrera del personal investigador posdoctoral',
     'Strengthening the postdoctoral research career'),
    ('Las personas investigadoras beneficiarias de las ayudas Ramón y Cajal contarán con los recursos necesarios para liderar un proyecto de investigación propio, consolidando así una trayectoria orientada a su estabilización en el sistema español de ciencia, posicionándolas en una senda de alto potencial, y así favoreciendo su proyección como referentes de liderazgo científico.',
     'Ramón y Cajal fellows will have the necessary resources to lead their own research project, consolidating a career path towards stabilisation in the Spanish science system, positioning them on a high-potential track and promoting their projection as scientific leadership benchmarks.'),
    ('Mejorar el posicionamiento internacional de las universidades y los centros de investigación españoles',
     'Improving the international standing of Spanish universities and research centres'),
    ('Las instituciones a las que se incorporen las personas investigadoras beneficiarias contarán con una ayuda vinculada a su estabilización, reforzando así su proyección estratégica en aquellas áreas donde oferten plazas, y asentando trayectorias hacia la excelencia de su actividad científica.',
     'Host institutions will receive support linked to the stabilisation of fellows, reinforcing their strategic standing in the areas where they offer positions and consolidating pathways towards scientific excellence.'),
    ('Las 5 grandes novedades', 'The 5 major updates'),
    # Page 2 - H3 de las 5 novedades en detalle (titulares de banda)
    ('<h3>Financiación de un proyecto propio de I+D+i</h3>',
     '<h3>Funding for an own R&amp;D&amp;I project</h3>'),
    ('<h3>Entrevista en el proceso de evaluación</h3>',
     '<h3>Interview in the evaluation process</h3>'),
    ('<h3>Incentivos para participar en convocatorias del ERC</h3>',
     '<h3>Incentives for participating in ERC calls</h3>'),
    ('<h3>Estabilización obligatoria con incentivo económico</h3>',
     '<h3>Mandatory stabilisation with financial incentive</h3>'),
    ('<h3>Integración y simplificación de convocatorias</h3>',
     '<h3>Integration and simplification of calls</h3>'),
    # Page 2 - Alt/title de las imágenes de banda
    ('alt="Sede de la Agencia Estatal de Investigación" loading="lazy"',
     'alt="Headquarters of the State Research Agency" loading="lazy"'),
    ('alt="Vista aérea del edificio de la AEI"',
     'alt="Aerial view of the AEI building"'),
    ('title="Presentación novedades programa Ramón y Cajal 2026"',
     'title="Ramón y Cajal Programme 2026 updates presentation"'),
    ('alt="Galaxia espiral NGC 4414 — NASA/Hubble"', 'alt="Spiral galaxy NGC 4414 — NASA/Hubble"'),
    ('Cada ayuda Ramón y Cajal incluirá, además de la cofinanciación del salario, la financiación para la ejecución de un proyecto de investigación de 5 años de duración, que será objeto de la evaluación.',
     'Each Ramón y Cajal fellowship will include, in addition to salary co-funding, funding for a 5-year research project, which will be subject to evaluation.'),
    ('<strong>Dotación suficiente</strong> para contratar al menos una persona investigadora predoctoral durante 4 años',
     '<strong>Sufficient allocation</strong> to hire at least one predoctoral researcher for 4 years'),
    ('<strong>No será compatible</strong> con la convocatoria PID hasta el cuarto año de ejecución, dado que la ayuda Ramón y Cajal incluye la financiación de un proyecto de investigación',
     '<strong>Not compatible</strong> with the PID call until the fourth year of execution, since the Ramón y Cajal fellowship includes project funding'),
    ('Costes elegibles similares a los de PID: personal, movilidad, equipamiento, fungibles, publicaciones, congresos y costes indirectos (25%)',
     'Eligible costs similar to PID: personnel, mobility, equipment, consumables, publications, conferences and indirect costs (25%)'),
    ('Permite iniciar una línea de investigación y crear un grupo propio desde el primer día',
     'Allows starting a research line and creating an own group from day one'),
    ('alt="Entrevista profesional con varias personas"', 'alt="Professional interview with several people"'),
    ('Se incorpora una entrevista con las comisiones técnicas como parte esencial de la evaluación, alineando el proceso con las mejores prácticas europeas (como el ERC).',
     'An interview with the evaluation panels is incorporated as an essential part of the assessment, aligning the process with best European practices (such as the ERC).'),
    ('<strong>Criterios de evaluación:</strong>', '<strong>Evaluation criteria:</strong>'),
    ('Aportaciones científico-técnicas de la persona candidata',
     'Scientific and technical contributions of the candidate'),
    ('Calidad y novedad de la propuesta de proyecto de investigación',
     'Quality and novelty of the research project proposal'),
    ('Impacto científico, económico y social esperado de los resultados',
     'Expected scientific, economic and social impact of the results'),
    ('Grado de independencia y liderazgo', 'Degree of independence and leadership'),
    ('Viabilidad de la propuesta de proyecto de investigación',
     'Feasibility of the research project proposal'),
    ('alt="Bandera de la Unión Europea"', 'alt="Flag of the European Union"'),
    ('Para las personas investigadoras que durante los tres primeros años de la ayuda RYC presenten una solicitud en las convocatorias del ERC (Starting, Consolidator o Advanced Grants):',
     'For researchers who during the first three years of the RYC fellowship submit an application to ERC calls (Starting, Consolidator or Advanced Grants):'),
    ('<strong>ERC financiada:</strong> incremento del 30% en la cofinanciación del salario',
     '<strong>ERC funded:</strong> 30% increase in salary co-funding'),
    ('<strong>ERC con máxima calificación sin financiación:</strong> habilitación como elegible en Europa Excelencia modalidad A + incremento del 10% del salario',
     '<strong>ERC with top rating without funding:</strong> eligibility for Europa Excelencia mode A + 10% salary increase'),
    ('<strong>ERC segunda fase sin máxima calificación:</strong> habilitación como elegible en Europa Excelencia modalidad B + incremento del 10% del salario',
     '<strong>ERC second phase without top rating:</strong> eligibility for Europa Excelencia mode B + 10% salary increase'),
    ('En solicitudes sucesivas, los incrementos pueden llegar al 20% y 30%',
     'In successive applications, increases can reach 20% and 30%'),
    ('Siempre que la evaluación del informe intermedio sea favorable:',
     'Provided the mid-term report evaluation is favourable:'),
    ('Se mantiene la ayuda de incentivación', 'The incentive support is maintained'),
    ('Se mantiene la ayuda para la realización del proyecto hasta un límite máximo de cinco años desde el inicio de la ayuda RyC',
     'Project funding is maintained up to a maximum of five years from the start of the RYC fellowship'),
    ('La cuantía que, dentro del concepto de contratación del/de la IP, no sea ejecutada como consecuencia de la creación del puesto de trabajo de carácter permanente podrá ser trasvasada a la ayuda correspondiente a la ejecución del proyecto',
     "The amount within the PI's employment concept not executed due to the creation of the permanent post may be transferred to the project execution funding"),
    ('La creación de un puesto de trabajo permanente en el área de la persona beneficiaria será un requisito obligatorio para cumplir con la ejecución de la ayuda.',
     "The creation of a permanent post in the fellow's area will be a mandatory requirement for the execution of the fellowship."),
    ('<strong>Ayuda a la entidad beneficiaria</strong> para la creación de una plaza permanente',
     '<strong>Support for the host institution</strong> for the creation of a permanent post'),
    ('Si el puesto se crea antes de finalizar la ayuda, las cantidades de cofinanciación del salario pueden trasvasarse al proyecto',
     'If the post is created before the fellowship ends, salary co-funding amounts may be transferred to the project'),
    ('La ayuda para la creación del puesto se mantiene hasta su efectiva creación',
     'Support for post creation is maintained until the post is effectively created'),
    ('Las modificaciones permiten una simplificación del panorama de ayudas de la AEI:',
     'The modifications enable a simplification of the AEI fellowship landscape:'),
    ('<strong>Se suprime</strong> la convocatoria de Consolidación Investigadora, cuyos objetivos quedan cubiertos por la nueva RYC',
     '<strong>The Research Consolidation call is abolished</strong>, its objectives being covered by the new RYC'),
    ('<strong>Desaparece</strong> la ayuda específica de atracción de talento (ya incluida en la financiación del proyecto)',
     '<strong>The specific talent attraction grant disappears</strong> (already included in project funding)'),
    ('Se incrementa la dotación de las ayudas en la convocatoria de Europa Excelencia',
     'The funding of Europa Excelencia grants is increased'),
    ('Se otorgará el certificado R3 de Investigador como investigador/a establecido/a para aquellas personas que obtengan la ayuda',
     'The R3 Researcher Certificate as an established researcher will be awarded to those who obtain the fellowship'),
    ('Presentación en vídeo', 'Video presentation'),
    ('Presentación oficial de las novedades del programa Ramón y Cajal para la convocatoria 2026:',
     'Official presentation of the Ramón y Cajal Programme updates for the 2026 call:'),
    ('¿Qué implica para las personas candidatas?', 'What does it mean for applicants?'),
    ('Propuesta científica sólida', 'Sound scientific proposal'),
    ('Los criterios de evaluación incorporan la valoración de la propuesta científica, esto exige presentar un proyecto de investigación novedoso, ambicioso, viable y con impacto.',
     'The evaluation criteria incorporate the assessment of the scientific proposal, requiring a novel, ambitious, feasible and impactful research project.'),
    ('Liderazgo e independencia', 'Leadership and independence'),
    ('La persona beneficiaria RYC se convierte en IP desde el inicio.',
     'The RYC fellow becomes PI from the outset.'),
    ('Visión europea', 'European vision'),
    ('Los incentivos para el ERC premian la ambición internacional. Preparar una solicitud al ERC durante los tres primeros años es una oportunidad estratégica.',
     'ERC incentives reward international ambition. Preparing an ERC application during the first three years is a strategic opportunity.'),
    ('Estabilidad garantizada', 'Guaranteed stability'),
    ('La obligatoriedad de crear un puesto permanente refuerza el compromiso de las instituciones con la carrera de la persona investigadora.',
     "The mandatory creation of a permanent post reinforces the institutional commitment to the researcher's career."),
    # Page 3 - Hero
    ('25 años incorporando al mejor personal investigador posdoctoral al sistema español de ciencia, tecnología e innovación.',
     '25 years incorporating the best postdoctoral researchers into the Spanish science, technology and innovation system.'),
    # Page 3 - Retrato Santiago Ramón y Cajal (alt + onerror alt + comentario)
    ('alt="Santiago Ramón y Cajal (1852–1934). Dominio público, Wikimedia Commons."',
     'alt="Santiago Ramón y Cajal (1852–1934). Public domain, Wikimedia Commons."'),
    ("this.alt='Santiago Ramón y Cajal en su microscopio. Wellcome Collection, dominio público.'",
     "this.alt='Santiago Ramón y Cajal at his microscope. Wellcome Collection, public domain.'"),
    ('<!-- Retrato de Santiago Ramón y Cajal (Wikimedia Commons, dominio público) -->',
     '<!-- Portrait of Santiago Ramón y Cajal (Wikimedia Commons, public domain) -->'),
    ('Historia y objetivos', 'History and objectives'),
    ('Origen del programa', 'Origins of the programme'),
    ('La primera convocatoria de ayudas del programa Ramón y Cajal fue publicada en el BOE del 19 de abril de 2001 con una dotación económica de 122,22 millones de euros, con el objetivo de incorporar al sistema español de ciencia, tecnología e innovación a personal investigador posdoctoral con trayectorias brillantes y prometedoras.',
     'The first Ramón y Cajal Programme call was published in the Official State Gazette on 19 April 2001 with a budget of €122.22 million, to incorporate postdoctoral researchers with outstanding and promising careers into the Spanish science, technology and innovation system.'),
    ('Desde su inicio, las solicitudes de participación son presentadas tanto por los Centros de I+D, que ofertan plazas en todas las áreas de conocimiento, como por las personas candidatas. Tras la evaluación y resolución, las personas seleccionadas contactan con los centros para firmar los acuerdos de incorporación y el contrato.',
     'From the outset, applications are submitted both by R&amp;D centres, which offer positions in all knowledge areas, and by candidates. After evaluation and resolution, selected individuals contact the centres to sign incorporation agreements and contracts.'),
    ('Objetivo principal', 'Main objective'),
    ('Promover la incorporación en organismos de investigación del Sistema Español de Ciencia, Tecnología e Innovación de personal investigador, tanto de nacionalidad española como extranjera, con una trayectoria destacada, con el fin de que adquieran las competencias y capacidades que les permitan obtener un puesto de carácter estable.',
     'To promote the incorporation into research organisations of the Spanish Science, Technology and Innovation System of researchers, both Spanish and foreign nationals, with outstanding careers, so that they acquire the skills and capabilities to obtain a permanent position.'),
    ('A partir de la convocatoria 2026, los objetivos se amplían para facilitar el desarrollo de líneas de investigación propias, la creación de grupos, la retención de talento y la mejora de la participación española en las convocatorias del ERC.',
     'From the 2026 call onwards, the objectives are expanded to facilitate the development of own research lines, group creation, talent retention and the improvement of Spanish participation in ERC calls.'),
    ('El programa en cifras', 'The programme in numbers'),
    ('Año de la primera convocatoria', 'Year of the first call'),
    ('Convocatorias publicadas', 'Published calls'),
    ('Años de duración de cada ayuda', 'Years of duration per fellowship'),
    ('De RYC que obtienen un ERC (StG o CoG)', 'Of RYC fellows who obtain an ERC (StG or CoG)'),
    ('Personas beneficiarias del programa Ramón y Cajal (2001–2024)',
     'Ramón y Cajal Programme fellows (2001–2024)'),
    ('Por género y año', 'By gender and year'),
    ('Por área temática', 'By thematic area'),
    ('Por comunidad autónoma', 'By autonomous community'),
    ("'Por género y año'", "'By gender and year'"),
    ("'Por área temática'", "'By thematic area'"),
    ("'Por comunidad autónoma'", "'By autonomous community'"),
    ('Personas beneficiarias por año y género', 'Fellows by year and gender'),
    ("'N.º de personas beneficiarias'", "'No. of fellows'"),
    ('N.º de personas beneficiarias', 'No. of fellows'),
    ('Personas beneficiarias por área temática y género (2001–2024)',
     'Fellows by thematic area and gender (2001–2024)'),
    ('Personas beneficiarias por comunidad autónoma y género (2001–2024)',
     'Fellows by autonomous community and gender (2001–2024)'),
    ('Fuente: Agencia Estatal de Investigación. Datos de convocatorias RYC 2001–2024.',
     'Source: State Research Agency. Data from RYC calls 2001–2024.'),
    ('Evolución del programa', 'Programme evolution'),
    ('A lo largo de sus 25 años, el programa ha incorporado cambios significativos para adaptarse a las necesidades del sistema de I+D+i:',
     'Over its 25 years, the programme has incorporated significant changes to adapt to the needs of the R&amp;D&amp;I system:'),
    ('2001 — Creación del programa', '2001 — Programme creation'),
    ('Primera convocatoria publicada el 19 de abril de 2001. Dotación de 122,22 M€. Ayudas de 5 años con cofinanciación de contratación y dotación adicional para investigación.',
     'First call published on 19 April 2001. Budget of €122.22M. 5-year fellowships with employment co-funding and additional research allocation.'),
    ('2012 — Ayuda para creación de puestos permanentes',
     '2012 — Support for permanent post creation'),
    ('Se incluye como gasto elegible una ayuda para la creación de puestos de trabajo de carácter permanente. Los Centros de I+D que creen puestos permanentes en el ámbito de la persona investigadora contratada recibirán una ayuda económica adicional.',
     "Support for the creation of permanent posts is included as an eligible cost. R&amp;D centres that create permanent posts in the fellow's area will receive additional financial support."),
    ('2021 — Turno para jóvenes personas investigadoras',
     '2021 — Track for early-career researchers'),
    ('Con la desaparición de la convocatoria Juan de la Cierva Incorporación, se incluye un turno específico para jóvenes personas investigadoras con fecha de doctorado entre 2017 y 2019. Este turno desaparece en 2022.',
     'With the end of the Juan de la Cierva Incorporation call, a specific track for early-career researchers with a doctoral date between 2017 and 2019 is included. This track is discontinued in 2022.'),
    ('2022 — Atracción de talento y dos fases',
     '2022 — Talent attraction and two phases'),
    ('Se reservan ayudas específicas para atraer personal investigador del extranjero (ayuda para la atracción del talento) con dotación adicional incrementada. La ayuda se divide en dos fases: primera fase de 3 años (37.800 €/año) y segunda fase de 2 años (46.900 €/año) condicionada a evaluación positiva de la actividad (criterios R3).',
     "Specific grants to attract researchers from abroad (talent attraction grant) with increased additional funding are reserved. The fellowship is divided into two phases: first phase of 3 years (€37,800/year) and second phase of 2 years (€46,900/year) conditional on a positive activity assessment (R3 criteria)."),
    ('2023 — Estabilización obligatoria', '2023 — Mandatory stabilisation'),
    ('Se incorpora la obligatoriedad de que las entidades beneficiarias garanticen el compromiso de crear puestos de trabajo permanentes con perfil adecuado a las plazas cubiertas.',
     "The obligation for host institutions to guarantee a commitment to create permanent posts with a profile appropriate to the positions covered is incorporated."),
    ('2026 — Transformación integral', '2026 — Comprehensive transformation'),
    ('La mayor transformación del programa: financiación de proyecto propio, entrevista en la evaluación, incentivos para el ERC, estabilización con incentivación para la entidad beneficiaria, e integración de la convocatoria de Consolidación Investigadora.',
     'The greatest transformation of the programme: own project funding, interview in the evaluation, ERC incentives, stabilisation with incentives for the host institution, and integration of the Research Consolidation call.'),
    ('>Ver novedades 2026 en detalle<', '>See 2026 updates in detail<'),
    ('Impacto del programa', 'Programme impact'),
    ('Fortalecimiento de la carrera investigadora',
     'Strengthening research careers'),
    ('El programa ofrece un entorno propicio para el desarrollo del liderazgo científico emergente, permitiendo a las personas investigadoras construir trayectorias independientes.',
     'The programme offers a conducive environment for the development of emerging scientific leadership, enabling researchers to build independent career paths.'),
    ('Efecto tractor', 'Multiplier effect'),
    ('Las personas beneficiarias RYC actúan como catalizadoras para atraer talento y recursos adicionales a las instituciones del sistema español de I+D+i.',
     'RYC fellows act as catalysts to attract talent and additional resources to institutions in the Spanish R&amp;D&amp;I system.'),
    ('Beneficio institucional', 'Institutional benefit'),
    ('Las instituciones receptoras ganan en talento, recursos y prestigio, fortaleciendo sus capacidades de investigación en todas las áreas de conocimiento.',
     'Host institutions gain in talent, resources and prestige, strengthening their research capabilities across all knowledge areas.'),
    ('Posicionamiento europeo', 'European positioning'),
    ('Con las nuevas modificaciones de 2026, el programa busca dar un salto cualitativo para situar a España donde le corresponde en el Espacio Europeo de Investigación.',
     'With the new 2026 modifications, the programme seeks a qualitative leap to position Spain where it belongs in the European Research Area.'),
    ('25 años de excelencia científica', '25 years of scientific excellence'),
    ('Descubre la historia completa del programa, testimonios de personal investigador y los hitos más destacados en la web conmemorativa del 25 aniversario.',
     'Discover the complete history of the programme, researcher testimonials and the most notable milestones on the 25th anniversary commemorative website.'),
    ('>Web 25 Años RYC<', '>25 Years RYC Website<'),
    # Page 4 JS strings
    ("anio: 2026,", "anio: 2026,"),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2026)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2026)"'),
    ("estado: \"Próxima\"", 'estado: "Upcoming"'),
    ('notas: "Nuevas condiciones: proyecto propio, entrevista, incentivos ERC"',
     'notas: "New conditions: own project, interview, ERC incentives"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2025)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2025)"'),
    ("estado: \"En tramitación\"", 'estado: "In progress"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2024)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2024)"'),
    ("estado: \"Resuelta\"", 'estado: "Resolved"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2023)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2023)"'),
    ('notas: "Incorpora la obligatoriedad de estabilización"',
     'notas: "Incorporates mandatory stabilisation"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2022)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2022)"'),
    ('notas: "Se introduce la ayuda para la atracción de talento y la división en dos fases"',
     'notas: "Talent attraction grant and two-phase structure introduced"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2021)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2021)"'),
    ('notas: "Turno para jóvenes personas investigadoras (desaparece en 2022)"',
     'notas: "Early-career researcher track (discontinued in 2022)"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2020)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2020)"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2019)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2019)"'),
    ("titulo: \"Ayudas para contratos Ramón y Cajal (RYC-2018)\"",
     'titulo: "Ramón y Cajal fellowship grants (RYC-2018)"'),
    # Page 4 HTML (cards estáticas 4ª revisión — texto plano sin comillas)
    # Prefijo común de los títulos de card. Aplica a los 9 años; el sufijo "YYYY)" queda igual.
    ('Ayudas para contratos Ramón y Cajal (RYC-', 'Ramón y Cajal fellowship grants (RYC-'),
    ('Histórico de Convocatorias Ramón y Cajal',
     'Ramón y Cajal Calls History'),
    ('Listado de convocatorias del programa Ramón y Cajal publicadas por la Agencia Estatal de Investigación, ordenadas de la más reciente a la más antigua.',
     'List of Ramón y Cajal Programme calls published by the State Research Agency, ordered from most recent to oldest.'),
    # JS dynamic strings
    ("'Próxima'", "'Upcoming'"),
    ("'Abierta'", "'Open'"),
    ("c.estado === 'Próxima' || c.estado === 'Abierta'",
     "c.estado === 'Upcoming' || c.estado === 'Open'"),
    ("c.estado === 'Abierta'", "c.estado === 'Open'"),
    ('>Ver ficha &#8599;<', '>View details &#8599;<'),
    ('>Ver ficha ↗<', '>View details ↗<'),
    ("'Ver novedades'", "'View updates'"),
    ('>Ficha no disponible<', '>Details not available<'),
    # Common
    ("'Mujeres'", "'Women'"),
    ("'Hombres'", "'Men'"),
    # Titles
    ('Inicio — Programa Ramón y Cajal', 'Home — Ramón y Cajal Programme'),
    ('Novedades 2026 — Programa Ramón y Cajal', '2026 Updates — Ramón y Cajal Programme'),
    ('Programa RYC — Agencia Estatal de Investigación', 'RYC Programme — State Research Agency'),
    ('Convocatorias — Programa Ramón y Cajal', 'Calls — Ramón y Cajal Programme'),
    # p3 hero
    ('Programa <span style="color: var(--ryc-dorado);">Ramón y Cajal</span>',
     '<span style="color: var(--ryc-dorado);">Ramón y Cajal</span> Programme'),
]

NAV_EN = {
    'href="index.html"':          'href="index.html"',
    'href="novedades-2026.html"': 'href="updates-2026.html"',
    'href="programa-ryc.html"':   'href="programme.html"',
    'href="convocatorias.html"':  'href="calls.html"',
    "'novedades-2026.html'":      "'updates-2026.html'",
}

def translate_en(content):
    for es, en in EN_TRANS:
        content = content.replace(es, en)
    content = apply_nav(content, NAV_EN)
    content = content.replace('lang="es"', 'lang="en"')
    return content

html_p1_en = translate_en(html_p1)
html_p2_en = translate_en(html_p2)
html_p3_en = translate_en(html_p3)
html_p4_en = translate_en(html_p4)

print('\nGenerando inglés...')
pages_en = [
    ('index.html',        html_p1_en),
    ('updates-2026.html', html_p2_en),
    ('programme.html',    html_p3_en),
    ('calls.html',        html_p4_en),
]
for fname, content in pages_en:
    with open(OUT_ING + '/' + fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ing/{fname}  {len(content)//1024}KB')

# ---- VERIFICACIÓN: comprobar que no quedan cadenas en español en los ficheros ingleses ----
# Frases que NUNCA deben aparecer en la versión inglesa
SPANISH_PHRASES = [
    'Ver ficha',
    'Ver novedades',
    'Ver histórico',
    'Ficha no disponible',
    'Ver convocatorias',
    'Conocer el programa',
    'Ir a la AEI',
    'Ver vídeo',
    'Más información',
    'Ver todas las novedades',
    'Ver novedades 2026',
    'Web 25 Años RYC',
    'Próxima publicación',
    'En tramitación',
    'Abrir menú',
    'Ruta de navegación',
    'Novedades 2026<',       # como título/nav
    'Inicio RYC<',
    'Programa RYC<',
    'Convocatorias<',
    # 4ª revisión — títulos h3 novedades en detalle
    'Incentivos para participar',
    'Integración y simplificación',
    'incentivo económico',
    'Estabilización obligatoria con incentivo',
    'Financiación de un proyecto propio',
    'Entrevista en el proceso',
    # Alt / title con restos
    'Sede de la Agencia Estatal de Investigación"',
    'Vista aérea del edificio',
    'Presentación novedades programa',
    'Dominio público',
    'dominio público',
    'Convocatoria de ayudas del Programa',
]

print('\nVerificando traducción inglesa...')
warnings = []
for fname, content in pages_en:
    for phrase in SPANISH_PHRASES:
        if phrase in content:
            warnings.append(f'  AVISO ing/{fname}: falta traducir "{phrase}"')

if warnings:
    print('  *** CADENAS SIN TRADUCIR ***')
    for w in warnings:
        print(w)
    print(f'  Total: {len(warnings)} aviso(s)')
else:
    print('  OK — todo traducido')

print('\nListo. Ficheros generados en !SALIDA/ — listos para git y Drupal.')
