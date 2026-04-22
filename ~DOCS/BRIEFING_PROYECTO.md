# BRIEFING COMPLETO — Web Programa Ramón y Cajal 2026

## 1. Contexto del proyecto

### Organismo promotor
**Agencia Estatal de Investigación (AEI)**, dependiente del Ministerio de Ciencia, Innovación y Universidades del Gobierno de España.

### Objetivo
Crear una web informativa sobre las **novedades de la convocatoria 2026 del Programa Ramón y Cajal (RYC)**, que introduce cambios sustanciales respecto a convocatorias anteriores. La web comunica de forma clara y atractiva las 5 grandes novedades al público objetivo (personal investigador posdoctoral, universidades y centros de investigación).

### Destino final
La web se desplegará en el portal de la AEI, que funciona sobre **Drupal 9.5.11**. El contenido HTML/CSS/JS se integrará como bloque o plantilla dentro de Drupal, usando el header y footer institucionales del portal.

### Entornos
| Entorno | URL |
|---------|-----|
| Repositorio GitHub | https://github.com/ramirez-santigosa/ryc-web |
| Previsualización (GitHub Pages) — español | https://ramirez-santigosa.github.io/ryc-web/ |
| Previsualización (GitHub Pages) — inglés | https://ramirez-santigosa.github.io/ryc-web/ing/ |
| Drupal — ficheros para pegar | `!SALIDA/*.html` (español) y `!SALIDA/ing/*.html` (inglés) |

---

## 2. Estructura de ficheros (estado actual)

```
09-WEB NUEVO RYC 2026/   (carpeta del proyecto)
│
├── .claude/                     # Datos Claude Code (no tocar, no va a git)
│
│  ── ENTRADA (local, no va a git) ─────────────────────────────────
│
├── !ENTRADA/                    # Todo lo que tú pones
│   ├── 01-inicial/
│   ├── 02-primera-revision/
│   ├── 03-segunda-revision/
│   ├── 04-tercera-revision/     # pagina*.txt (dev) + imágenes definitivas
│   ├── 05-cuarta-revision/      # Documento de la 4ª revisión (traducciones, fix Drupal)
│   └── datos/                   # Datos originales (xlsx...)
│
│  ── SALIDA — ES el repositorio git (.git/ vive aquí dentro) ───────
│
└── !SALIDA/
    ├── .git/                    # Repositorio git (no tocar)
    ├── .gitignore
    ├── CLAUDE.md                # Cargado automáticamente por Claude Code
    ├── index.html               # Español
    ├── novedades-2026.html
    ├── programa-ryc.html
    ├── convocatorias.html
    ├── ing/                     # Inglés
    │   ├── index.html
    │   ├── updates-2026.html
    │   ├── programme.html
    │   └── calls.html
    ├── assets/                  # Fondos de banner (referenciados por URL absoluta)
    ├── scripts/
    │   └── gen_ryc3.py
    └── ~DOCS/                   # Documentación del proyecto
        ├── BRIEFING_PROYECTO.md
        └── PROCEDIMIENTO.md
```

> **Nota:** CSS, JS e imágenes de contenido están **embebidos** dentro de cada fichero HTML. La carpeta `assets/` contiene únicamente los fondos de banners que se cargan vía URL absoluta desde el CSS embebido (`https://ramirez-santigosa.github.io/ryc-web/assets/...`).
> Los mismos ficheros sirven tanto para GitHub Pages (previsualización) como para entregar a Drupal.

### Reglas de imagen
- **Sin SVG** (ni inline ni referenciado): los fragmentos pegados en Drupal pueden perder o reescribir elementos `<svg>` al pasar por los filtros del editor. Logos e iconos vectoriales se rasterizan a **PNG**. Fotos se guardan como **JPEG**. Todas las imágenes van **embebidas en base64** dentro del HTML.
- **Sin `<footer>` propio**: el HTML generado no contiene ningún elemento `<footer>` ni clase/regla CSS `.footer / .footer-grid / .footer-bottom`. El footer institucional lo pinta Drupal con sus propias clases — cualquier regla nuestra sobre `footer` interferiría (u ocultaría) con el footer de Drupal. El script `scripts/gen_ryc3.py` limpia esas referencias automáticamente con `strip_footer_refs()`.

---

## 3. Arquitectura técnica

### Stack
- **HTML5 estático** — sin frameworks ni preprocesadores
- **CSS3** con variables CSS (custom properties) para paleta de colores
- **JavaScript vanilla** — sin dependencias excepto Chart.js para gráficos
- **Chart.js 4.4.7** (CDN) — solo en `programa.html` para el dashboard interactivo

### Un único formato de entrega
Los mismos ficheros HTML sirven para GitHub Pages y para Drupal. Se generan con `scripts/gen_ryc3.py` a partir de los ficheros fuente en `!ENTRADA/04-tercera-revision/pagina*.txt` (versiones adaptadas por el equipo de desarrollo) y se escriben directamente en `!SALIDA/` (español) y `!SALIDA/ing/` (inglés).

| Destino | Ruta |
|---------|------|
| GitHub Pages (español) | `!SALIDA/*.html` (raíz de `main`) |
| GitHub Pages (inglés) | `!SALIDA/ing/*.html` |
| Drupal (español) | mismo `!SALIDA/*.html` |
| Drupal (inglés) | mismo `!SALIDA/ing/*.html` |

---

## 4. Paleta de colores

Definida en `:root` de `css/styles.css`:

| Variable | Valor | Uso |
|----------|-------|-----|
| `--aei-azul` | `#1b4c96` | Color principal (títulos, nav, botones, números) |
| `--aei-azul-oscuro` | `#143a73` | Hover |
| `--aei-azul-claro` | `#dae3f3` | Fondos suaves |
| `--ryc-dorado` | `#c8a951` | Acentos: líneas decorativas, nombre "Ramón y Cajal" en títulos |
| `--fondo-claro` | `#f0f4fa` | Fondo general del body |
| `--fondo-blanco` | `#ffffff` | Tarjetas y secciones |

---

## 5. Páginas y contenido

### index.html — Página principal
1. **Hero** — Fondo azul con siluetas, título, botones "Novedades 2026" y "Ver convocatorias"
2. **¿Qué es el Programa RYC?** — Descripción + foto edificio AEI + datos clave + botón "Conocer el programa"
3. **Novedades 2026** — 5 ítems numerados con iconos SVG
4. **Convocatorias recientes** — Cards 2026 (próxima), 2025 (tramitación), 2024 y 2023
5. **Banner UE** — Logo MICIU + texto cofinanciación
6. **Enlaces de interés** — Carrusel: 25 Años RYC, Vídeo, Web AEI, Convocatorias AEI, Europa Excelencia

### novedades-2026.html
1. **¿Para qué cambia la convocatoria?** — Grid 2 columnas
2. **Las 5 grandes novedades** — Imagen banda + número + contenido (novedades 2, 4, 5 con nuevas imágenes)
3. **Presentación en vídeo** — Embed YouTube
4. **¿Qué implica para las personas candidatas?** — 4 tarjetas

> **Nota (4ª revisión):** esta página **no** lleva el banner de cofinanciación UE — a diferencia de `index`, `programa-ryc` y `convocatorias`. Lo mismo aplica a su versión inglesa (`ing/updates-2026.html`).

### programa.html
1. **Historia y objetivos** — Origen 2001, objetivo principal
2. **El programa en cifras** — 4 datos + Dashboard Chart.js (género/año, área, CCAA)
3. **Evolución del programa** — Acordeones 2001–2026
4. **Impacto del programa** — Imagen excavación + 4 tarjetas
5. **25 años de excelencia** — CTA hacia web AEI

### convocatorias.html
Listado dinámico (JavaScript) de todas las convocatorias RYC 2001–2026 con enlaces a fichas en aei.gob.es.

---

## 6. Navegación

```
Inicio RYC | Novedades 2026 | Programa RYC | Convocatorias | 25 Años RYC ↗
```
- "25 Años RYC" enlaza directamente a `aei.gob.es` (sin página propia)
- Breadcrumb: Inicio > Convocatorias > Ramón y Cajal > [página actual]
- Menú responsive con hamburguesa en móvil

---

## 7. Textos sensibles — Decisiones editoriales

| Punto | Texto actual | Razón |
|-------|-------------|-------|
| Novedad 1 | "No será compatible con la convocatoria PID hasta el cuarto año de ejecución" | Redacción definitiva (2ª revisión) |
| Novedad 3 — ERC | Condiciones informe intermedio (texto largo) | Texto largo sobre mantenimiento de ayudas y trasvase |
| Novedad 4 | Sin cifra de 75.000€ | Eliminada por indicación |
| Novedad 5 — Europa Excelencia | "Se incrementa la dotación..." | Sin cifras (2ª revisión) |
| Novedad 5 — R3 | Certificado R3 como investigador/a establecido/a | Nueva viñeta añadida (2ª revisión) |
| CTA final | Apartado "¿Todo listo?" retirado | A la espera de ficha oficial convocatoria 2026 |
| Criterios evaluación | Orden: aportaciones, calidad, impacto, independencia, viabilidad | Reordenado en 2ª revisión |

---

## 8. Script de generación — `scripts/gen_ryc3.py`

Genera los HTML a partir de las páginas adaptadas por el equipo dev (`!ENTRADA/04-tercera-revision/pagina*.txt`) y los escribe directamente en `!SALIDA/`.

**Qué hace:**
1. Lee `pagina 1-4.txt` (fragmentos Drupal del equipo dev)
2. Redimensiona imágenes nuevas (PIL/Pillow, máx. 1200×400 px, JPEG 85%) y las embebe en base64
3. Inyecta CSS extra en el último `</style>` del fragmento: footer oculto, banner UE, fix tarjetas convocatorias
4. Añade el banner de cofinanciación UE antes del comentario `<!-- FOOTER -->` (en `index`, `programa-ryc` y `convocatorias` — **no** en `novedades-2026`)
5. Envuelve en HTML mínimo (`<head>` solo con charset+viewport+title; CSS queda en el body)
6. Genera versión inglés aplicando la tabla de traducciones `EN_TRANS`
7. Escribe `!SALIDA/*.html` (español) y `!SALIDA/ing/*.html` (inglés)
8. Verifica que no queden cadenas en español en los ficheros ingleses e imprime el resultado:
   - `OK — todo traducido` → sin problemas, listo para commit
   - `AVISO ing/fichero.html: falta traducir "..."` → añadir el patrón a `EN_TRANS` y regenerar

**Ruta del proyecto:** la constante `PROYECTO` se calcula automáticamente desde la ubicación del script (`__file__`), por lo que el script funciona independientemente del nombre de la carpeta OneDrive (que cambió de "MCI" a "MICIU" en abril 2026).

**Para regenerar** (desde `!SALIDA/` o con ruta completa):
```bash
python scripts/gen_ryc3.py
```

**Requisitos Python:**
```bash
pip install Pillow
```

**Imágenes fuente** (en `!ENTRADA/04-tercera-revision/`):
- `Novedades - 2 Entrevista.png`
- `Novedades - 4 Estabilización.png`
- `Novedades - 5 Integración convocatorias.png`
- `Programa - Impacto - Excavación.png`
- `MICIU+Cofinanciado+AEI.jpg`

---

## 9. Integración en Drupal

### Procedimiento recomendado
1. Abrir `!SALIDA/[pagina].html` (o `!SALIDA/ing/[pagina].html`) en un editor de texto
2. En Drupal: crear/editar "Página básica" → formato "Full HTML"
3. Pegar el contenido del fichero (incluido el `<!DOCTYPE html>` inicial — Drupal lo ignora)
4. Guardar y previsualizar

### Qué lleva cada fragmento Drupal
- Todo el CSS en `<style>` en el body (Drupal lo conserva; el navegador lo renderiza igual)
- Todo el JS en `<script>` antes del comentario `<!-- FOOTER -->`
- Imágenes embebidas en base64 (no dependen de rutas externas)
- CSS `footer, .footer { display: none !important }` para suprimir el footer de Drupal
- Banner cofinanciación UE con imagen base64

### Qué NO lleva
- Header/footer institucional AEI (se usa el de Drupal)
- Breadcrumb con contenido (contenedor vacío, Drupal lo gestiona)

### Problemas frecuentes en Drupal

| Causa | Síntoma | Solución |
|-------|---------|----------|
| Formato de texto filtra `<style>`/`<script>` | CSS/JS desaparecen al guardar | Usar **"Full HTML"** o deshabilitar filtros |
| CKEditor reescribe el HTML | Código se "limpia" al guardar | Desactivar editor o usar "Código fuente" antes de pegar |
| `post_max_size` PHP < 32 MB | Error al guardar páginas con imágenes base64 | Subir a ≥ 32 MB en php.ini |
| CSS en `<head>` descartado por Drupal | Estilos no se aplican | Los fragmentos ya tienen CSS en el body — correcto |

---

## 10. Lo que funcionó bien

- **Python + PIL** para redimensionar y embeber imágenes en base64: sencillo, sin dependencias pesadas
- **CSS en el body**: los fragmentos funcionan tanto en navegador como en Drupal (no se pierde el CSS al pegar)
- **Un único juego de ficheros** para GitHub Pages y Drupal: sin carpeta `dist/` separada, sin paso de sincronización
- **`!SALIDA/` ES el repositorio git**: `.git/` vive dentro — la raíz del proyecto queda limpia
- **GitHub Pages** para previsualización: permite compartir URLs antes de ir a producción
- **Traducción automática** con tabla `EN_TRANS`: cubre ~95% del contenido; requiere revisión manual de JS y textos dinámicos
- **Footer suprimido** con `display: none !important`: solución limpia sin modificar el HTML del fragmento

---

## 11. Lo que NO funcionó / problemas encontrados

| Problema | Causa | Solución aplicada |
|----------|-------|-------------------|
| Node.js + sharp para imágenes | Dependencias pesadas, build complejo | Reemplazado por Python + PIL |
| Imágenes base64 sin redimensionar | Tamaños de 18–80 MB, inmanejable | Redimensionado a 1200×400 px antes de codificar |
| `banner-cofinanciacion.png` no existía | Archivo nunca creado en assets/ | Generado desde `MICIU+Cofinanciado+AEI.jpg` → `banner-cofinanciacion.jpg` |
| CSS en `<head>` descartado por Drupal | Drupal elimina el `<head>` al pegar | CSS movido al body en el script de generación |
| `dist/` + carpetas `pages/` + `en/` redundantes | Tres ubicaciones para el mismo contenido | Unificado en `!SALIDA/` (español) y `!SALIDA/ing/` (inglés) — un solo juego de ficheros |
| Traducción automática incompleta | Patrones en `EN_TRANS` no coincidían con el HTML real (backticks vs `><`) | Verificación automática al generar + corrección de patrones |
| `wrap_fragment()` movía `<style>` al `<head>` | Diseño inicial del script | Eliminado; los `<style>` permanecen en el body |
| Regex greedy en imagen novedad 5 | `[^>]*` eliminó atributos `alt` y `loading` | Reemplazado por `str.replace()` sobre el src |
| `inject_css()` con ancla de texto frágil | El patrón `DRUPAL_HIDE` no existía en pagina3.txt | Reemplazado por `rfind('</style>')` — más robusto |
| Tarjetas convocatorias colapsadas en Drupal | `<span class="anio">` dentro de `<h3>` era reinterpretado por los filtros de Drupal | 4ª revisión: año extraído a `<div class="convocatoria-anio">` hermano del `.convocatoria-info`, CONV_FIX reforzado con `!important` |
| Patrones `EN_TRANS` con prefijos ambiguos | Regla corta "Estabilización obligatoria con incentivo" se aplicaba antes de la larga con "económico" y dejaba un residuo | Usar siempre el delimitador completo (`<h3>...</h3>`) en los patrones de `EN_TRANS` |
| `PROYECTO` hardcodeado a una ruta OneDrive concreta | El script fallaba al renombrarse la carpeta OneDrive (MCI→MICIU) | Autodetección vía `__file__` |

---

## 12. Historial de versiones

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| v1 | mar 2026 | Versión original: paleta granate/dorado, medalla en banner |
| v2 | abr 2026 | Rediseño completo: paleta azul AEI, banners con siluetas, sin medalla |
| v2.1 | 16-04-2026 | 2ª revisión editorial: texto Novedad 1 (PID), reorden criterios, viñeta R3 |
| v2.2 | 21-04-2026 | 3ª revisión: nuevas imágenes base64, banner EU, fix convocatorias CSS |
| v2.3 | 21-04-2026 | Unificación: un solo juego de ficheros para GitHub Pages y Drupal, `ing/` para inglés, limpieza repo |
| v2.4 | 21-04-2026 | Reorganización: `!SALIDA/` ES el repo (`.git/` dentro), raíz del proyecto limpia, gen_ryc3.py sin paso sync |
| v2.5 | 22-04-2026 | 4ª revisión: traducciones faltantes al EN (h3 novedades 3/4/5, alt, title, meta); banner UE retirado de novedades-2026 (ES/EN); rediseño tarjetas convocatorias (año como bloque, no span) para robustez en Drupal; PROYECTO en `gen_ryc3.py` autodetectado desde la ubicación del script |
| v2.6 | 22-04-2026 | 4ª revisión (continuación): banner cofinanciación UE dentro de `<main>` como `<section>` (no como `<div>` fuera); eliminadas TODAS las referencias a footer (CSS `.footer`, regla `display:none` sobre footer, comentario `<!-- FOOTER -->`) para que Drupal conserve su footer institucional; logo de cofinanciación convertido a PNG; regla "sin SVG, sin `<footer>`" documentada |
