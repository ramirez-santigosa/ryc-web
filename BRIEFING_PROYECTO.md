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
| Previsualización (GitHub Pages) — inglés | https://ramirez-santigosa.github.io/ryc-web/en/ |
| Drupal — fragmentos para pegar | `dist/esp/` y `dist/ing/` |

---

## 2. Estructura de ficheros (estado actual)

```
ryc-web/
│
├── index.html                   # Página principal ES (GitHub Pages)
├── pages/
│   ├── novedades-2026.html      # Novedades 2026 ES
│   ├── programa.html            # Programa RYC ES
│   └── convocatorias.html       # Histórico de convocatorias ES
│
├── en/                          # Versión inglés (GitHub Pages)
│   ├── index.html
│   └── pages/
│       ├── novedades-2026.html
│       ├── programa.html
│       └── convocatorias.html
│
├── dist/                        # Fragmentos para pegar en Drupal
│   ├── esp/                     # Español
│   │   ├── inicio-ryc.html      (~73 KB)
│   │   ├── novedades-2026.html  (~269 KB — imágenes embebidas en base64)
│   │   ├── programa-ryc.html    (~248 KB)
│   │   └── convocatorias.html  (~68 KB)
│   └── ing/                     # Inglés
│       ├── ryc-home.html
│       ├── updates-2026.html
│       ├── programme.html
│       └── calls.html
│
├── assets/                      # Imágenes live site
│   ├── novedades-entrevista.jpg      # Novedad 2 (nueva, 3ª revisión)
│   ├── novedades-estabilizacion.jpg  # Novedad 4 (nueva, 3ª revisión)
│   ├── novedades-integracion.jpg     # Novedad 5 (nueva, 3ª revisión)
│   ├── programa-excavacion.jpg       # Impacto programa (nueva, 3ª revisión)
│   ├── banner-cofinanciacion.jpg     # Banner EU/MICIU (nueva, 3ª revisión)
│   ├── edificio-aei-bandera.jpg      # Foto sede AEI (sección "Qué es")
│   ├── icons/                        # Iconos SVG+PNG de las 5 novedades
│   └── [otros fondos y fotos]
│
├── css/
│   ├── styles.css               # Estilos globales
│   └── ryc.css                  # Estilos específicos RYC
│
├── js/
│   ├── main.js                  # Interactividad
│   └── datos-ryc.json           # Datos del dashboard
│
├── scripts/
│   └── gen_ryc3.py              # Script Python: genera dist/esp/ y dist/ing/
│
├── BRIEFING_PROYECTO.md         # Este fichero
├── PROCEDIMIENTO.md             # Guía para repetir la experiencia
├── CLAUDE.md                    # Contexto para Claude Code
└── .gitignore
```

**Fuera del repositorio (carpeta local, en `docs/` y `datos/`):**
```
docs/
├── 01-inicial/       # Brief inicial, indicaciones, imágenes de referencia
├── 02-primera-revision/  # Documentos y logs de la 1ª revisión
├── 03-segunda-revision/  # Documentos de la 2ª revisión
└── 04-tercera-revision/  # Imágenes fuente + pagina*.txt (fragmentos del equipo dev)
datos/
├── brutos/           # Datos originales de convocatorias (xlsx)
└── RYC*.xlsx         # Datos procesados para el dashboard
```

---

## 3. Arquitectura técnica

### Stack
- **HTML5 estático** — sin frameworks ni preprocesadores
- **CSS3** con variables CSS (custom properties) para paleta de colores
- **JavaScript vanilla** — sin dependencias excepto Chart.js para gráficos
- **Chart.js 4.4.7** (CDN) — solo en `programa.html` para el dashboard interactivo

### Dos formatos de entrega
| Formato | Dónde | Para qué |
|---------|-------|---------|
| **Live site** | `index.html` + `pages/` + `en/` | GitHub Pages: previsualización, referencias externas CSS/assets |
| **Drupal fragments** | `dist/esp/` + `dist/ing/` | Pegar en Drupal: CSS en el body, imágenes embebidas en base64, head mínimo |

Los fragmentos Drupal se generan con `scripts/gen_ryc3.py` a partir de los ficheros fuente en `docs/04-tercera-revision/pagina*.txt` (versiones adaptadas por el equipo de desarrollo).

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

Genera los fragmentos Drupal en `dist/esp/` y `dist/ing/` a partir de las páginas adaptadas por el equipo dev (`docs/04-tercera-revision/pagina*.txt`).

**Qué hace:**
1. Lee `pagina 1-4.txt` (fragmentos Drupal del equipo dev)
2. Redimensiona imágenes nuevas (PIL/Pillow, máx. 1200×400 px, JPEG 85%) y las embebe en base64
3. Inyecta CSS extra en el último `</style>` del fragmento: footer oculto, banner UE, fix tarjetas convocatorias
4. Añade el banner de cofinanciación UE antes del comentario `<!-- FOOTER -->`
5. Envuelve en HTML mínimo (`<head>` solo con charset+viewport+title; CSS queda en el body)
6. Genera versión inglés aplicando tabla de traducciones `EN_TRANS`
7. Escribe `dist/esp/*.html` y `dist/ing/*.html`

**Para regenerar:**
```bash
python scripts/gen_ryc3.py
```

**Requisitos Python:**
```bash
pip install Pillow
```

**Imágenes fuente** (en `docs/04-tercera-revision/`):
- `Novedades - 2 Entrevista.png`
- `Novedades - 4 Estabilización.png`
- `Novedades - 5 Integración convocatorias.png`
- `Programa - Impacto - Excavación.png`
- `MICIU+Cofinanciado+AEI.jpg`

---

## 9. Integración en Drupal

### Procedimiento recomendado
1. Abrir `dist/esp/[pagina].html` en un editor de texto
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
- **Una sola carpeta de salida por idioma** (`dist/esp/` y `dist/ing/`): elimina confusión entre formatos
- **GitHub Pages** para previsualización: permite compartir URLs antes de ir a producción
- **Doble estructura**: live site (`pages/`) para GitHub Pages + fragmentos (`dist/`) para Drupal
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
| `dist/pagina*.html` + `dist/esp/*.html` redundantes | Dos formatos para el mismo propósito | Unificados en `dist/esp/` y `dist/ing/` únicamente |
| Traducción automática incompleta en JS | `EN_TRANS` hace replace de texto estático, no toca templates JS | Corrección manual en los ficheros generados |
| `wrap_fragment()` movía `<style>` al `<head>` | Diseño inicial del script | Eliminado; los `<style>` permanecen en el body |
| Regex greedy en imagen novedad 5 | `[^>]*` eliminó atributos `alt` y `loading` | Reemplazado por `str.replace()` sobre el src |
| `inject_css()` con ancla de texto frágil | El patrón `DRUPAL_HIDE` no existía en pagina3.txt | Reemplazado por `rfind('</style>')` — más robusto |

---

## 12. Historial de versiones

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| v1 | mar 2026 | Versión original: paleta granate/dorado, medalla en banner |
| v2 | abr 2026 | Rediseño completo: paleta azul AEI, banners con siluetas, sin medalla |
| v2.1 | 16-04-2026 | 2ª revisión editorial: texto Novedad 1 (PID), reorden criterios, viñeta R3 |
| v2.2 | 21-04-2026 | 3ª revisión: nuevas imágenes base64, banner EU, fix convocatorias CSS, `dist/esp/` + `dist/ing/` |
| v2.3 | 21-04-2026 | Live site corregido (`pages/`, `en/`), "See details" traducido, unificación dist/, limpieza repo |
