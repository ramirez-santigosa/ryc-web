# Web Ramón y Cajal 2026 — Contexto para Claude Code

## Proyecto
Web informativa sobre las novedades de la convocatoria RYC 2026 de la AEI.
Destino final: portal AEI en Drupal 9.5. GitHub Pages como previsualización.

## Estructura de carpetas
```
!ENTRADA/                  ← tus fuentes (local, no en git)
  04-tercera-revision/     ← pagina*.txt del equipo dev + imágenes fuente
  datos/
!SALIDA/                   ← salida local (no en git); el script genera aquí
  index.html / novedades-2026.html / programa-ryc.html / convocatorias.html
  ing/                     ← inglés
  assets/
  scripts/gen_ryc3.py
  ~DOCS/

Lo que git rastrea (copiado desde !SALIDA/ por el script):
  index.html · novedades-2026.html · programa-ryc.html · convocatorias.html
  ing/ · assets/ · scripts/ · ~DOCS/ · CLAUDE.md
```

## Stack técnico
- HTML5 estático · CSS3 con variables · JS vanilla · Chart.js CDN (solo programa)
- CSS embebido en el body (Drupal descarta el head)
- Imágenes de contenido embebidas en base64
- Fondos de banner referenciados por URL absoluta desde assets/

## Paleta de colores
- `--aei-azul: #1b4c96` — principal (títulos, nav, botones)
- `--aei-azul-oscuro: #143a73` — hover
- `--ryc-dorado: #c8a951` — acentos decorativos
- `--fondo-claro: #f0f4fa` — fondo general
- `--fondo-blanco: #ffffff` — tarjetas

## Páginas (español / inglés)
| Español | Inglés | Contenido |
|---------|--------|-----------|
| index.html | ing/index.html | Home RYC |
| novedades-2026.html | ing/updates-2026.html | Las 5 novedades |
| programa-ryc.html | ing/programme.html | Historia y dashboard |
| convocatorias.html | ing/calls.html | Histórico 2001–2026 |

## Generación
```bash
py scripts/gen_ryc3.py
```
Lee `!ENTRADA/04-tercera-revision/pagina 1-4.txt`, genera en `!SALIDA/`
y sincroniza automáticamente a la raíz del repo y a `ing/`.

## Estado actual — v2.3 (21-04-2026)
Versión aprobada. Pendiente: publicación ficha oficial convocatoria 2026.

## URLs
- GitHub Pages ES: https://ramirez-santigosa.github.io/ryc-web/
- GitHub Pages EN: https://ramirez-santigosa.github.io/ryc-web/ing/
- Repositorio: https://github.com/ramirez-santigosa/ryc-web
