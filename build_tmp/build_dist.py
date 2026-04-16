"""
Empaqueta las páginas de la web RYC en 5 HTML autocontenidos en dist/.
- CSS embebido en <style>
- JS embebido en <script>
- Imágenes/assets locales convertidos a data: base64
- Recursos remotos (CDN, aei.gob.es, unsplash, wikimedia) se mantienen
- Enlaces internos reescritos a pagina1..5.html
"""
import base64
import mimetypes
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

# Mapa de ruta original -> destino paginaN.html
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

# El enlace externo "25 Años RYC" del menú apunta a la página 5 (landing local)
NAV_25_EXT_URL = "https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal"


def file_to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "application/octet-stream"
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


def embed_css_url(css_text: str, css_dir: Path) -> str:
    """Reemplaza url('../assets/x.png') dentro del CSS por data: URLs."""
    def repl(m):
        url = m.group(1).strip().strip('"').strip("'")
        if url.startswith(("http://", "https://", "data:")):
            return f"url({url})"
        target = (css_dir / url).resolve()
        if not target.exists():
            return m.group(0)
        return f"url('{file_to_data_uri(target)}')"
    return re.sub(r"url\(([^)]+)\)", repl, css_text)


def load_css(filename: str) -> str:
    path = ROOT / "css" / filename
    return embed_css_url(path.read_text(encoding="utf-8"), path.parent)


def load_js(filename: str) -> str:
    return (ROOT / "js" / filename).read_text(encoding="utf-8")


CSS_GLOBAL = load_css("styles.css") + "\n\n/* === ryc.css === */\n" + load_css("ryc.css")
JS_MAIN = load_js("main.js")


def resolve_local_path(href: str, html_path: Path) -> Path | None:
    """Devuelve el Path local si href apunta a un asset relativo del repo."""
    if href.startswith(("http://", "https://", "data:", "mailto:", "#", "//", "javascript:")):
        return None
    candidate = (html_path.parent / href).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    return candidate if candidate.exists() and candidate.is_file() else None


def embed_local_images(html: str, html_path: Path) -> str:
    """Convierte src='...' (img/iframe/source) locales a data: URLs."""
    def repl(m):
        attr = m.group(1)
        quote = m.group(2)
        url = m.group(3)
        target = resolve_local_path(url, html_path)
        if target is None:
            return m.group(0)
        return f'{attr}={quote}{file_to_data_uri(target)}{quote}'
    # src="..." y src='...'
    return re.sub(
        r'(src)=(["\'])([^"\']+)\2',
        repl,
        html,
    )


def embed_inline_bg(html: str, html_path: Path) -> str:
    """Embeb url('../assets/...') en atributos style inline."""
    def repl(m):
        url = m.group(1).strip().strip('"').strip("'")
        if url.startswith(("http://", "https://", "data:")):
            return m.group(0)
        target = resolve_local_path(url, html_path)
        if target is None:
            return m.group(0)
        return f"url('{file_to_data_uri(target)}')"
    return re.sub(r"url\(([^)]+)\)", repl, html)


def replace_links(html: str, current_page: str) -> str:
    """Reescribe href entre las 5 páginas."""
    # 1) Reescribir href del enlace externo "25 Años RYC" del menú principal hacia pagina5.html
    html = re.sub(
        r'(<a\s[^>]*href=)"' + re.escape(NAV_25_EXT_URL) + r'"([^>]*\bclass="[^"]*\bnav-destacado\b[^"]*"[^>]*)>',
        lambda m: f'{m.group(1)}"pagina5.html"' + re.sub(r'\s*target="_blank"', '', m.group(2)) + ">",
        html,
    )

    # 2) Reescribir hrefs internos siguiendo el mapa
    def href_repl(m):
        prefix = m.group(1)
        href = m.group(2)
        suffix = m.group(3)
        # Eliminar fragmento si lo hubiera
        frag = ""
        if "#" in href:
            href, frag = href.split("#", 1)
            frag = "#" + frag
        if href in PAGE_MAP:
            new = PAGE_MAP[href] + frag
            return f'{prefix}"{new}"{suffix}>'
        return m.group(0)
    html = re.sub(r'(<a\s[^>]*href=)"([^"]+)"([^>]*)>', href_repl, html)

    # 3) Marcar la página activa en el menú
    # Quitar todos los class="active" en <a> del nav
    def clean_active(m):
        body = m.group(0)
        body = re.sub(r'\s+class="active"', "", body)
        body = re.sub(r'class="active"\s*', '', body)
        return body
    # Aplicar solo dentro de #nav-menu
    nav_match = re.search(r'(<ul\s+id="nav-menu">)(.*?)(</ul>)', html, re.DOTALL)
    if nav_match:
        nav_inner = nav_match.group(2)
        nav_inner_clean = re.sub(r'(<a\s[^>]*?)\s+class="active"', r'\1', nav_inner)
        # Marcar como activa el href de current_page
        nav_inner_clean = re.sub(
            r'(<a\s+href="' + re.escape(current_page) + r'")(\s*[^>]*)>',
            lambda m: m.group(1) + ' class="active"' + m.group(2) + '>',
            nav_inner_clean,
            count=1,
        )
        html = html[: nav_match.start()] + nav_match.group(1) + nav_inner_clean + nav_match.group(3) + html[nav_match.end():]
    return html


def inline_assets(html: str, html_path: Path) -> str:
    """Sustituye <link rel=stylesheet local> y <script src local> por contenido inline."""
    # Quitar <link rel="stylesheet" href=".../styles.css|ryc.css">
    def link_repl(m):
        href = m.group(1)
        if href.endswith("styles.css") or href.endswith("ryc.css"):
            return ""  # se inyecta CSS_GLOBAL más arriba como bloque <style>
        # otros (CDN, etc.) se mantienen
        return m.group(0)
    html = re.sub(
        r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*/?>',
        link_repl,
        html,
    )
    # Insertar bloque <style> con CSS_GLOBAL antes de </head>
    html = html.replace(
        "</head>",
        f"<style>\n{CSS_GLOBAL}\n</style>\n</head>",
        1,
    )

    # Reemplazar <script src="...main.js"> por contenido
    def script_repl(m):
        src = m.group(1)
        if src.endswith("main.js"):
            return f"<script>\n{JS_MAIN}\n</script>"
        # si es CDN externo, dejar tal cual
        return m.group(0)
    html = re.sub(
        r'<script\s+src="([^"]+)"\s*></script>',
        script_repl,
        html,
    )
    return html


def build_page(source_relpath: str, dest_name: str) -> str:
    src = ROOT / source_relpath
    html = src.read_text(encoding="utf-8")
    html = inline_assets(html, src)
    html = embed_local_images(html, src)
    html = embed_inline_bg(html, src)
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

  <!-- ===== HEADER INSTITUCIONAL ===== -->
  <header class="header-institucional">
    <div class="container">
      <div class="logos-institucionales">
        <a href="https://www.ciencia.gob.es/" target="_blank" title="Ministerio de Ciencia, Innovación y Universidades">
          <img src="https://www.aei.gob.es/themes/custom/vartheme_aei/images/logo_ministerio_ciencia.svg" alt="Ministerio de Ciencia, Innovación y Universidades" onerror="this.alt='MICINN'; this.style.height='auto'">
        </a>
        <a href="https://www.aei.gob.es/" target="_blank" title="Agencia Estatal de Investigación">
          <img src="https://www.aei.gob.es/themes/custom/vartheme_aei/logo_aei.svg" alt="Agencia Estatal de Investigación" onerror="this.alt='AEI'; this.style.height='auto'">
        </a>
      </div>
      <div class="site-name">
        <span class="first-letter">Agencia</span>
        <span class="first-letter">Estatal</span>
        de
        <span class="first-letter">Investigación</span>
      </div>
    </div>
  </header>

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

  <!-- ===== BREADCRUMB ===== -->
  <div class="breadcrumb" aria-label="Ruta de navegación">
    <a href="https://www.aei.gob.es/">Inicio</a>
    <span>&rsaquo;</span>
    <a href="pagina1.html">Ramón y Cajal</a>
    <span>&rsaquo;</span>
    <strong>25 Años RYC</strong>
  </div>

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

  <!-- ===== FOOTER ===== -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <h4>Programa Ramón y Cajal</h4>
          <ul>
            <li><a href="pagina3.html">Sobre el programa</a></li>
            <li><a href="pagina2.html">Novedades 2026</a></li>
            <li><a href="pagina4.html">Histórico de convocatorias</a></li>
          </ul>
        </div>
        <div>
          <h4>Agencia Estatal de Investigación</h4>
          <ul>
            <li><a href="https://www.aei.gob.es/" target="_blank">Portal AEI</a></li>
            <li><a href="https://www.aei.gob.es/convocatorias" target="_blank">Convocatorias AEI</a></li>
            <li><a href="https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal" target="_blank">25 Años RYC</a></li>
          </ul>
        </div>
        <div>
          <h4>Contacto</h4>
          <ul>
            <li><a href="https://www.aei.gob.es/" target="_blank">www.aei.gob.es</a></li>
            <li>Agencia Estatal de Investigación</li>
            <li>Ministerio de Ciencia, Innovación y Universidades</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Agencia Estatal de Investigación. Ministerio de Ciencia, Innovación y Universidades. Gobierno de España.</p>
      </div>
    </div>
  </footer>

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
