# Procedimiento: Maqueta web AEI con Claude Code

Guía para crear una maqueta web para el portal de la AEI, revisarla iterativamente y entregarla al equipo de desarrollo para su integración en Drupal.

---

## 1. Estructura de carpetas del proyecto

```
nombre-proyecto/
│
├── .claude/                       # Datos Claude Code (no tocar)
│
│  ── ENTRADA (local, no va a git) ─────────────────────────────────
│
├── !ENTRADA/                      # Todo lo que tú pones: fuentes, imágenes, datos
│   ├── 01-inicial/               # Brief inicial, imágenes de referencia, indicaciones
│   ├── 02-revision-1/            # Documentos y notas de la 1ª ronda de revisión
│   ├── 03-revision-2/            # Documentos de la 2ª ronda
│   ├── 04-revision-N/            # Fragmentos .txt del equipo dev + imágenes definitivas
│   └── datos/                    # Datos originales y procesados (xlsx, csv...)
│
│  ── SALIDA (ES el repositorio git) ────────────────────────────────
│
└── !SALIDA/                       # Repositorio git — .git/ vive aquí dentro
    ├── .git/                      # Repositorio git (no tocar)
    ├── .gitignore
    ├── CLAUDE.md                  # Cargado automáticamente por Claude Code
    ├── index.html                 # Español
    ├── novedades.html
    ├── programa.html
    ├── convocatorias.html
    ├── ing/                       # Inglés
    │   ├── index.html
    │   ├── updates.html
    │   ├── programme.html
    │   └── calls.html
    ├── assets/                    # Fondos de banner (referenciados por URL absoluta)
    ├── scripts/
    │   └── gen_dist.py            # Script Python: genera HTML a partir de !ENTRADA/
    └── ~DOCS/                     # Documentación del proyecto (sorts last)
        ├── BRIEFING_PROYECTO.md
        └── PROCEDIMIENTO.md
```

### .gitignore mínimo
```
.claude/
```

> **Regla de oro:** Todo lo que esté en `!ENTRADA/` es tuyo y no va al repositorio.
> Todo lo que esté en `!SALIDA/` (excepto `.claude/`) se rastrea en git — los HTML los genera el script, nunca edites a mano.

---

## 2. Fase 1 — Brief inicial a Claude Code

### Cómo dar las directrices

Crear un fichero `!ENTRADA/01-inicial/BRIEF_INICIAL.md` con:

```markdown
## Proyecto
[Nombre del programa/convocatoria/sección de la AEI]

## Objetivo de la web
[Qué debe comunicar, a quién, para qué]

## Páginas necesarias
- Página 1: [nombre] — [contenido principal]
- Página 2: ...

## Contenido de cada página
[Textos, secciones, datos a mostrar]

## Imágenes disponibles
[Lista de ficheros en !ENTRADA/01-inicial/ con descripción de cada uno]

## Referencias de diseño
- Web AEI de referencia: [URL]
- Paleta de colores: [primario, secundario, acento]
- Tipografía: [si hay preferencia]

## Restricciones técnicas
- Drupal [versión]
- El header y footer institucional los pone Drupal
- Sin frameworks CSS externos (o con Bootstrap, según caso)

## Idiomas
- Solo español / Español + inglés

## Datos dinámicos
[Si hay tablas, gráficos o listados — descripción y fuente]
```

### Instrucción de arranque a Claude Code

```
Lee el fichero !ENTRADA/01-inicial/BRIEF_INICIAL.md y crea la maqueta completa.
Genera directamente los ficheros en !SALIDA/ (español) y !SALIDA/ing/ (inglés).
Cada fichero debe ser autocontenido: CSS en el body, imágenes embebidas en base64.
Sigue el estilo visual de la AEI (azul #1b4c96, variables CSS, sin frameworks externos).
```

Claude Code generará directamente los HTML en `!SALIDA/`. No hace falta estructura intermedia de `pages/`, `dist/` ni carpetas de CSS/JS separadas — todo va embebido.

---

## 3. Fase 2 — Revisiones iterativas

### Cómo dar indicaciones de revisión

Cada ronda de revisión va en un fichero en `!ENTRADA/0N-revision-N/`:

```markdown
## Revisión N — [fecha]

### Cambios de texto
- Página X, sección Y: sustituir "[texto actual]" por "[texto nuevo]"
- Página X: añadir párrafo: "[texto]"

### Cambios de imagen
- Página X, sección Y: cambiar imagen actual por [nombre-fichero.png]
  (fichero adjunto en esta misma carpeta)

### Cambios de diseño/layout
- [descripción precisa del cambio visual]

### Correcciones
- [lo que no funciona o está mal]
```

**Instrucción a Claude Code:**
```
Lee !ENTRADA/0N-revision-N/REVISION_N.md y aplica todos los cambios indicados.
Regenera los HTML al terminar.
```

### Buenas prácticas para revisiones

- **Una revisión por ronda**: no mezclar cambios de diferentes fechas en el mismo documento
- **Precisión**: indicar página, sección y texto exacto — evitar "cambia el apartado de novedades"
- **Imágenes**: dejar los ficheros nuevos en la carpeta de la revisión con nombres descriptivos
- **Textos aprobados**: si un texto ha sido validado por dirección, indicarlo explícitamente para que no se modifique

---

## 4. Fase 3 — Integración Drupal (fragmentos del equipo dev)

Cuando la maqueta esté aprobada, el equipo de desarrollo adapta el HTML a Drupal y devuelve ficheros `pagina N.txt` (fragmentos sin DOCTYPE/html/head/body, con CSS y JS embebidos). Dejar esos ficheros en `!ENTRADA/04-revision-N/`.

### Estructura del script `scripts/gen_dist.py`

```python
# 1. Cargar imágenes nuevas de !ENTRADA/0N-revision-N/ y redimensionarlas (PIL)
# 2. Leer pagina*.txt del equipo dev (!ENTRADA/0N-revision-N/)
# 3. Sustituir imágenes antiguas por base64 de las nuevas
# 4. Inyectar CSS extra antes del último </style>:
#    - footer { display: none !important }   ← oculta footer Drupal
#    - .banner-cofinanciacion { ... }        ← banner UE
#    - [fix específicos de Drupal si hay]
# 5. Añadir banner cofinanciación UE antes de <!-- FOOTER -->
# 6. Envolver en HTML mínimo (head solo con meta+title; CSS queda en body)
# 7. Aplicar tabla de traducciones EN_TRANS para versión inglés
# 8. Escribir !SALIDA/*.html (español) y !SALIDA/ing/*.html (inglés)
```

Ver `scripts/gen_ryc3.py` de este proyecto como referencia completa.

### Requisitos
```bash
pip install Pillow
python scripts/gen_dist.py
```

### Reglas de imagen para base64

| Tipo | Formato | Tamaño máximo | Calidad | Resultado aprox. |
|------|---------|--------------|---------|-----------------|
| Imagen de sección (foto, banda ancha) | **JPEG** | 1200×400 px | 85% | 30–170 KB |
| Logo institucional / banner con texto | **PNG** | 800×200 px | — | 40–90 KB |
| Icono | **PNG** | 200×200 px | — | < 10 KB |

Reglas adicionales:

- **Prohibido SVG** (ni inline `<svg>` ni referenciado `.svg`): los filtros de Drupal suelen reescribir o descartar elementos SVG al pegar. Rasterizar siempre a PNG (vectoriales) o JPEG (fotografías).
- **Redimensionar antes de codificar**: una imagen de 5 MB sin redimensionar produce un base64 de ~7 MB, haciendo el fichero inmanejable en Drupal.
- **PNG para texto/logo**, **JPEG para fotografías**: PNG conserva la nitidez en bordes y texto (imprescindible en logos), JPEG comprime mucho mejor fotografías al mismo nivel de calidad percibida.

---

## 5. Fase 4 — Entrega al equipo de desarrollo

### Qué entregar

| Fichero | Para qué |
|---------|---------|
| `!SALIDA/*.html` | Pegar en Drupal (español) |
| `!SALIDA/ing/*.html` | Pegar en Drupal (inglés) |
| `assets/` | Imágenes del live site (fondos de banners) |
| `BRIEFING_PROYECTO.md` | Documentación del proyecto |

**Los ficheros HTML son autocontenidos**: llevan CSS, JS e imágenes embebidas. El equipo solo necesita pegarlos en una "Página básica" de Drupal en formato Full HTML.

### Instrucciones para el equipo de desarrollo

```
Cada fichero en !SALIDA/ y !SALIDA/ing/ corresponde a una Página básica de Drupal.
Procedimiento:
1. Crear/editar la Página básica correspondiente
2. Formato de texto: Full HTML (sin filtros de etiquetas)
3. Pegar el contenido del fichero HTML completo
4. El header y footer de Drupal sustituyen al de la maqueta automáticamente
   (el CSS incluye footer { display: none !important })
5. Las imágenes están embebidas: no hay assets que subir al servidor

Si el editor CKEditor reescribe el código:
- Desactivar CKEditor para el formato Full HTML, o
- Pegar en modo "Código fuente" del editor

Si hay error al guardar (fichero muy grande):
- Subir post_max_size en php.ini a 32 MB o más
```

### GitHub Pages como previsualización

El repositorio se publica en GitHub Pages directamente desde `!SALIDA/` (raíz de `main`). Los mismos ficheros sirven tanto para previsualización como para entregar a Drupal — no hay carpeta `dist/` separada.

---

## 6. Gestión del repositorio

### Flujo de trabajo
```
1. Colocar fuentes en !ENTRADA/ (imágenes, fragmentos .txt, notas)
2. Claude Code aplica los cambios y regenera los HTML en !SALIDA/
3. El script imprime "OK — todo traducido" o avisos de cadenas sin traducir
4. Si hay avisos: corregir EN_TRANS en gen_ryc3.py y regenerar hasta que pase limpio
5. Claude Code hace commit y push a main
6. GitHub Pages publica automáticamente en 1-2 minutos
7. Revisión desde la URL de GitHub Pages
8. Si hay cambios: nueva instrucción a Claude Code → repetir
```

### Commits
- Usar mensajes descriptivos: `feat:`, `fix:`, `refactor:`, `docs:`
- Un commit por ronda de cambios significativa

### Ramas
- `main` — siempre la versión más reciente aprobada
- Para backup de versión anterior: crear tag `v1`, `v2`...

---

## 7. CLAUDE.md — Contexto persistente

El fichero `CLAUDE.md` en la raíz de `!SALIDA/` se carga automáticamente en cada sesión de Claude Code. Debe contener:

```markdown
# [Nombre del proyecto] — Contexto para Claude Code

## Proyecto
[Descripción breve]

## Stack técnico
- HTML5 estático, CSS3 con variables, JS vanilla
- Chart.js CDN si hay dashboard
- Sin frameworks externos
- CSS embebido en el body (no en head) para compatibilidad Drupal
- Imágenes embebidas en base64

## Carpetas clave
- Fuentes: !ENTRADA/0N-revision-N/ (fragmentos .txt + imágenes nuevas)
- Assets live site: assets/
- Script de generación: scripts/gen_dist.py
- Salida español: !SALIDA/ (raíz del repo)
- Salida inglés: !SALIDA/ing/

## Paleta de colores
- --aei-azul: #1b4c96
- --aei-azul-oscuro: #143a73
- --ryc-dorado: #c8a951

## Estado actual
[Versión actual, qué está aprobado, qué está pendiente]
```

Actualizar `CLAUDE.md` al inicio de cada fase nueva o cuando cambie algo significativo.

---

## 8. Lecciones aprendidas (proyecto RYC 2026)

### Hacer siempre desde el principio
- Separar claramente **!ENTRADA/** (tuyo, no va a git) de **!SALIDA/** (el repo) — nunca editar los HTML a mano
- Poner el **CSS en el body** en los fragmentos Drupal, no en `<head>` (Drupal lo descarta)
- **Redimensionar** las imágenes antes de codificarlas en base64 (máx. 1200×400 px)
- Comprobar que todos los assets referenciados en CSS existen en `assets/` antes de publicar

### Evitar
- Imágenes base64 sin redimensionar previo (ficheros de decenas de MB)
- Editar los ficheros HTML manualmente (se sobreescriben al regenerar)
- Usar Node.js/sharp si Python+PIL es suficiente (más sencillo, sin dependencias de npm)
- Regex con `[^>]*` para reemplazar atributos de `<img>` (elimina `alt` y `loading`)
- Carpetas `dist/` o `pages/` como intermedias — los ficheros definitivos van directamente a `!SALIDA/`
- **Elementos `<svg>` o recursos `.svg`**: los filtros de CKEditor/Drupal pueden descartarlos al pegar. Usar siempre PNG o JPEG rasterizado.
- **Ningún `<footer>` propio ni reglas CSS `footer/.footer`**: el footer institucional lo pinta Drupal con sus propias clases. Una regla `.footer { ... }` en nuestro CSS estilizaría (o rompería) el footer de Drupal; y `display: none` sobre `footer` lo ocultaría por completo. Si los fragmentos del equipo dev traen bloques "Footer", el script los limpia con `strip_footer_refs()`.
- **`<span>` decorativos dentro de `<h3>`/`<h2>`** para componer "badge + título" en una sola línea: Drupal (CKEditor, filtros) puede reinterpretar ese layout y colapsarlo. Separar siempre en elementos hermanos (`<div class="badge">…</div>` + `<div class="info"><h3>…</h3></div>`) con flex en el contenedor padre.
- **Hardcodear rutas absolutas** al proyecto: calcular siempre con `os.path.dirname(os.path.abspath(__file__))` por si la carpeta OneDrive cambia de nombre.
- **Patrones `EN_TRANS` sin delimitador de cierre**: si hay dos textos que comparten prefijo (ej. "Estabilización obligatoria con incentivo" vs "…con incentivo económico"), usar siempre el delimitador completo `<h3>…</h3>` para evitar que la regla corta "se coma" parte de la larga.

### Traducción automática
- La tabla `EN_TRANS` cubre texto estático bien, pero puede no alcanzar texto dentro de templates JavaScript
- Al terminar la generación, el script imprime automáticamente el resultado de la verificación:
  - `OK — todo traducido` → sin problemas
  - `AVISO ing/fichero.html: falta traducir "..."` → hay cadenas sin traducir
- Si aparece un aviso: añadir la cadena exacta (tal como aparece en el HTML, con `>` y `<`) a `EN_TRANS` en `scripts/gen_ryc3.py` y regenerar
- Revisar también manualmente tras cambios grandes: `aria-label`, textos de estado y botones generados por JS
