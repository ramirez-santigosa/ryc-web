"""
Empaqueta la web RYC en 5 HTML "semi-autocontenidos" para Drupal.

Modo OPCIÓN B:
- CSS embebido en <style>
- JS embebido en <script>
- Imágenes y fondos LOCALES -> URL REMOTA a GitHub Pages (no base64)
- Se ELIMINA el header institucional (fondo blanco con logos MICIU/AEI)
- Se VACÍA la barra del breadcrumb (se deja como barra blanca sin contenido)
- Se ELIMINA el footer
- Los <svg> inline se sustituyen por <img> PNG servidos desde GitHub Pages
- Recursos remotos (Chart.js CDN, aei.gob.es, Wikimedia, Unsplash, YouTube) se mantienen
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

REMOTE_BASE = "https://ramirez-santigosa.github.io/ryc-web"

PAGE_MAP = {
    "index.html":                 "pagina1.html",
    "../index.html":              "pagina1.html",
    "pages/novedades-2026.html":  "pagina2.html",
    "novedades-2026.html":        "pagina2.html",
    "pages/programa.html":        "pagina3.html",
    "programa.html":              "pagina3.html",
    "pages/convocatorias.html":   "pagina4.html",
    "convocatorias.html":         "pagina4.html",
}
NAV_25_EXT_URL = "https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal"


def rewrite_css_urls_to_remote(css_text: str, css_dir: Path) -> str:
    """Sustituye url('../assets/x.png') por URL remota GitHub Pages."""
    def repl(m):
        url = m.group(1).strip().strip('"').strip("'")
        if url.startswith(("http://", "https://", "data:")):
            return f"url({url})"
        target = (css_dir / url).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        return f"url('{REMOTE_BASE}/{rel}')"
    return re.sub(r"url\(([^)]+)\)", repl, css_text)


def load_css(filename: str) -> str:
    path = ROOT / "css" / filename
    return rewrite_css_urls_to_remote(path.read_text(encoding="utf-8"), path.parent)


def load_js(filename: str) -> str:
    return (ROOT / "js" / filename).read_text(encoding="utf-8")


CSS_GLOBAL = load_css("styles.css") + "\n\n/* === ryc.css === */\n" + load_css("ryc.css")
JS_MAIN = load_js("main.js")


def remote_url_for(href: str, html_path: Path) -> str | None:
    """Devuelve URL remota GitHub Pages si href apunta a asset local del repo."""
    if href.startswith(("http://", "https://", "data:", "mailto:", "#", "//", "javascript:")):
        return None
    candidate = (html_path.parent / href).resolve()
    try:
        rel = candidate.relative_to(ROOT).as_posix()
    except ValueError:
        return None
    if not candidate.exists():
        return None
    return f"{REMOTE_BASE}/{rel}"


def rewrite_local_images(html: str, html_path: Path) -> str:
    """<img src='...'> local -> URL remota GitHub Pages."""
    def repl(m):
        attr = m.group(1)
        quote = m.group(2)
        url = m.group(3)
        new = remote_url_for(url, html_path)
        if new is None:
            return m.group(0)
        return f'{attr}={quote}{new}{quote}'
    return re.sub(r'(src)=(["\'])([^"\']+)\2', repl, html)


def rewrite_inline_bg(html: str, html_path: Path) -> str:
    """url('../assets/...') en atributos style inline -> URL remota."""
    def repl(m):
        url = m.group(1).strip().strip('"').strip("'")
        if url.startswith(("http://", "https://", "data:")):
            return m.group(0)
        new = remote_url_for(url, html_path)
        if new is None:
            return m.group(0)
        return f"url('{new}')"
    return re.sub(r"url\(([^)]+)\)", repl, html)


def strip_header_footer(html: str) -> str:
    """Elimina <header class="header-institucional">...</header> y <footer class="footer">...</footer>."""
    html = re.sub(
        r'<header\s+class="header-institucional">.*?</header>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<footer\s+class="footer">.*?</footer>\s*',
        "",
        html,
        flags=re.DOTALL,
    )
    return html


def empty_breadcrumb(html: str) -> str:
    """Vacía el contenido del <div class="breadcrumb">...</div> dejando el contenedor."""
    return re.sub(
        r'(<div\s+class="breadcrumb"[^>]*>).*?(</div>)',
        r'\1\2',
        html,
        count=1,
        flags=re.DOTALL,
    )


# Mapa de iconos SVG inline -> PNG (por orden de aparición en index.html)
SVG_ICON_REPLACEMENTS = [
    # Novedad 1: euro / dorado
    (r'<svg[^>]*stroke="#c8a951"[^>]*>.*?</svg>',
     '<img src="{base}/assets/icons/novedad-1.png" class="novedad-icono-svg" width="72" height="72" alt="" aria-hidden="true">'),
    # Novedad 2: personas / azul + path "M23 21v-2"
    (r'<svg[^>]*stroke="#1b4c96"[^>]*>(?:(?!</svg>).)*?M23 21v-2.*?</svg>',
     '<img src="{base}/assets/icons/novedad-2.png" class="novedad-icono-svg" width="72" height="72" alt="" aria-hidden="true">'),
    # Novedad 3: globo / azul + estrellas FFCC00
    (r'<svg[^>]*stroke="#1b4c96"[^>]*>(?:(?!</svg>).)*?#FFCC00.*?</svg>',
     '<img src="{base}/assets/icons/novedad-3.png" class="novedad-icono-svg" width="72" height="72" alt="" aria-hidden="true">'),
    # Novedad 4: casa / azul + polyline "9 22"
    (r'<svg[^>]*stroke="#1b4c96"[^>]*>(?:(?!</svg>).)*?9 22 9 12.*?</svg>',
     '<img src="{base}/assets/icons/novedad-4.png" class="novedad-icono-svg" width="72" height="72" alt="" aria-hidden="true">'),
    # Novedad 5: cajas / verde
    (r'<svg[^>]*stroke="#2e7d32"[^>]*>.*?</svg>',
     '<img src="{base}/assets/icons/novedad-5.png" class="novedad-icono-svg" width="72" height="72" alt="" aria-hidden="true">'),
]


def replace_inline_svgs(html: str) -> str:
    for pattern, replacement in SVG_ICON_REPLACEMENTS:
        html = re.sub(pattern, replacement.format(base=REMOTE_BASE), html, flags=re.DOTALL)
    return html


def inline_assets(html: str) -> str:
    """Sustituye <link rel=stylesheet local> y <script src local> por contenido inline."""
    def link_repl(m):
        href = m.group(1)
        if href.endswith("styles.css") or href.endswith("ryc.css"):
            return ""
        return m.group(0)
    html = re.sub(
        r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*/?>',
        link_repl,
        html,
    )
    # Insertar <style> antes de </head>
    html = html.replace(
        "</head>",
        f"<style>\n{CSS_GLOBAL}\n</style>\n</head>",
        1,
    )

    def script_repl(m):
        src = m.group(1)
        if src.endswith("main.js"):
            return f"<script>\n{JS_MAIN}\n</script>"
        return m.group(0)
    html = re.sub(
        r'<script\s+src="([^"]+)"\s*></script>',
        script_repl,
        html,
    )
    return html


def replace_links(html: str, current_page: str) -> str:
    # Reescribir "25 Años RYC" del menú (externo) a pagina5.html
    html = re.sub(
        r'(<a\s[^>]*href=)"' + re.escape(NAV_25_EXT_URL) + r'"([^>]*\bclass="[^"]*\bnav-destacado\b[^"]*"[^>]*)>',
        lambda m: f'{m.group(1)}"pagina5.html"' + re.sub(r'\s*target="_blank"', '', m.group(2)) + ">",
        html,
    )

    def href_repl(m):
        prefix = m.group(1)
        href = m.group(2)
        suffix = m.group(3)
        frag = ""
        if "#" in href:
            href, frag = href.split("#", 1)
            frag = "#" + frag
        if href in PAGE_MAP:
            new = PAGE_MAP[href] + frag
            return f'{prefix}"{new}"{suffix}>'
        return m.group(0)
    html = re.sub(r'(<a\s[^>]*href=)"([^"]+)"([^>]*)>', href_repl, html)

    # Marcar página activa en el nav
    nav_match = re.search(r'(<ul\s+id="nav-menu">)(.*?)(</ul>)', html, re.DOTALL)
    if nav_match:
        nav_inner = nav_match.group(2)
        nav_inner = re.sub(r'(<a\s[^>]*?)\s+class="active"', r'\1', nav_inner)
        nav_inner = re.sub(
            r'(<a\s+href="' + re.escape(current_page) + r'")(\s*[^>]*)>',
            lambda m: m.group(1) + ' class="active"' + m.group(2) + '>',
            nav_inner,
            count=1,
        )
        html = html[: nav_match.start()] + nav_match.group(1) + nav_inner + nav_match.group(3) + html[nav_match.end():]
    return html


def build_page(source_relpath: str, dest_name: str) -> str:
    src = ROOT / source_relpath
    html = src.read_text(encoding="utf-8")
    html = inline_assets(html)
    html = rewrite_local_images(html, src)
    html = rewrite_inline_bg(html, src)
    html = replace_inline_svgs(html)
    html = strip_header_footer(html)
    html = empty_breadcrumb(html)
    html = replace_links(html, dest_name)
    out = DIST / dest_name
    out.write_text(html, encoding="utf-8")
    return f"{source_relpath} -> dist/{dest_name} ({len(html):,} bytes)"


# ---- Página 5: landing "25 Años RYC" ----
PAGE5_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>25 Años Ramón y Cajal — Agencia Estatal de Investigación</title>
  <meta name="description" content="Web conmemorativa de los 25 años del Programa Ramón y Cajal (2001-2026): historia, hitos y testimonios.">
__CSS__
</head>
<body>

  <!-- ===== NAVEGACIÓN ===== -->
  <nav class="nav-principal" aria-label="Navegación principal">
    <div class="container">
      <button class="nav-toggle" aria-label="Abrir menú" aria-expanded="false">&#9776;</button>
      <ul id="nav-menu">
        <li><a href="pagina1.html">Inicio RYC</a></li>
        <li><a href="pagina2.html">Novedades 2026</a></li>
        <li><a href="pagina3.html">Programa RYC</a></li>
        <li><a href="pagina4.html">Convocatorias</a></li>
        <li><a href="pagina5.html" class="active nav-destacado">25 Años RYC</a></li>
      </ul>
    </div>
  </nav>

  <!-- ===== BREADCRUMB (vacío) ===== -->
  <div class="breadcrumb" aria-label="Ruta de navegación"></div>

  <!-- ===== HERO ===== -->
  <section class="hero-novedades">
    <h1>25 Años de <span>Ramón y Cajal</span></h1>
    <p>Un cuarto de siglo impulsando la excelencia científica en España: historia, hitos y testimonios del programa.</p>
  </section>

  <main>

    <section class="seccion text-center">
      <h2 class="seccion-titulo" style="border:none; text-align:center;">Web conmemorativa</h2>
      <p style="max-width: 720px; margin: 0 auto 1.5rem; color: var(--texto-secundario);">
        La Agencia Estatal de Investigación dispone de una web específica con todo el contenido conmemorativo
        del 25 aniversario del programa Ramón y Cajal: testimonios, hitos, datos y eventos.
      </p>
      <p>
        <a href="https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal" target="_blank" class="btn-ryc">Ir a la web 25 Años RYC &#8599;</a>
      </p>
    </section>

    <section class="seccion">
      <h2 class="seccion-titulo">Hitos del programa</h2>
      <div class="datos-clave" style="grid-template-columns: repeat(4, 1fr);">
        <div class="dato-item"><div class="dato-numero">2001</div><div class="dato-label">Primera convocatoria</div></div>
        <div class="dato-item"><div class="dato-numero">+25</div><div class="dato-label">Convocatorias publicadas</div></div>
        <div class="dato-item"><div class="dato-numero">5</div><div class="dato-label">Años de duración de la ayuda</div></div>
        <div class="dato-item"><div class="dato-numero">2026</div><div class="dato-label">Transformación integral</div></div>
      </div>
    </section>

    <section class="seccion text-center">
      <a href="pagina1.html" class="btn-ryc-outline">Volver al inicio</a>
    </section>

  </main>

  <script>
__JS__
  </script>
</body>
</html>
"""


def build_page5() -> str:
    html = PAGE5_HTML_TEMPLATE.replace("__CSS__", f"  <style>\n{CSS_GLOBAL}\n  </style>")
    html = html.replace("__JS__", JS_MAIN)
    out = DIST / "pagina5.html"
    out.write_text(html, encoding="utf-8")
    return f"(generada) -> dist/pagina5.html ({len(html):,} bytes)"


def main():
    results = []
    results.append(build_page("index.html", "pagina1.html"))
    results.append(build_page("pages/novedades-2026.html", "pagina2.html"))
    results.append(build_page("pages/programa.html", "pagina3.html"))
    results.append(build_page("pages/convocatorias.html", "pagina4.html"))
    results.append(build_page5())
    print("\n".join(results))


if __name__ == "__main__":
    main()
