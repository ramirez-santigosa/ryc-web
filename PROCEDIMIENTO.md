# Procedimiento: Maqueta web AEI con Claude Code

Guía para crear una maqueta web para el portal de la AEI, revisarla iterativamente y entregarla al equipo de desarrollo para su integración en Drupal.

---

## 1. Estructura de carpetas del proyecto

Crear esta estructura desde el principio. Las carpetas `docs/` y `datos/` son locales (en .gitignore); el resto va al repositorio.

```
nombre-proyecto/
│
├── BRIEFING_PROYECTO.md       # Descripción completa del proyecto
├── PROCEDIMIENTO.md           # Esta guía
├── CLAUDE.md                  # Contexto persistente para Claude Code
├── .gitignore
│
├── index.html                 # Página principal (español)
├── pages/                     # Páginas interiores (español)
├── en/                        # Versión inglés
│   └── pages/
│
├── assets/                    # Imágenes del live site
│   └── icons/
├── css/
│   ├── styles.css             # Variables globales, layout, nav
│   └── [nombre-proyecto].css  # Estilos específicos del proyecto
├── js/
│   ├── main.js
│   └── datos.json             # Si hay dashboard de datos
│
├── dist/                      # Fragmentos para Drupal (generados por script)
│   ├── esp/
│   └── ing/
│
├── scripts/
│   └── gen_dist.py            # Script Python de generación
│
├── docs/                      # LOCAL — no en git
│   ├── 01-inicial/            # Brief inicial, imágenes de referencia, indicaciones
│   ├── 02-revision-1/         # Documentos de la 1ª ronda de revisión
│   ├── 03-revision-2/         # Documentos de la 2ª ronda
│   └── 04-revision-N/         # Fragmentos .txt del equipo dev + imágenes definitivas
│
└── datos/                     # LOCAL — no en git
    ├── brutos/                # Datos originales (xlsx, csv)
    └── [procesados]           # Datos preparados para la web
```

### .gitignore mínimo
```
docs/
datos/
.claude/
```

---

## 2. Fase 1 — Brief inicial a Claude Code

### Cómo dar las directrices

Crear un fichero `docs/01-inicial/BRIEF_INICIAL.md` con:

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
[Lista de ficheros en docs/01-inicial/ con descripción de cada uno]

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
Lee el fichero docs/01-inicial/BRIEF_INICIAL.md y crea la maqueta completa:
- index.html y pages/*.html con el contenido indicado
- css/styles.css y css/[proyecto].css
- js/main.js con menú móvil y navegación
- assets/ con las imágenes de docs/01-inicial/
Sigue el estilo visual de la AEI (azul #1b4c96, variables CSS, sin frameworks externos).
```

---

## 3. Fase 2 — Revisiones iterativas

### Cómo dar indicaciones de revisión

Cada ronda de revisión va en un fichero en `docs/0N-revision-N/`:

```markdown
## Revisión N — [fecha]

### Cambios de texto
- Página X, sección Y: sustituir "[texto actual]" por "[texto nuevo]"
- Página X: añadir párrafo: "[texto]"

### Cambios de imagen
- Página X, sección Y: cambiar imagen actual por [nombre-fichero.png]
  (fichero adjunto en esta carpeta)

### Cambios de diseño/layout
- [descripción precisa del cambio visual]

### Correcciones
- [lo que no funciona o está mal]
```

**Instrucción a Claude Code:**
```
Lee docs/0N-revision-N/REVISION_N.docx (o .md) y aplica todos los cambios indicados.
```

### Buenas prácticas para revisiones

- **Una revisión por ronda**: no mezclar cambios de diferentes fechas en el mismo documento
- **Precisión**: indicar página, sección y texto exacto — evitar "cambia el apartado de novedades"
- **Imágenes**: dejar los ficheros nuevos en la carpeta de la revisión con nombres descriptivos
- **Textos sensibles**: si un texto ha sido aprobado por dirección, indicarlo explícitamente para que no se modifique

---

## 4. Fase 3 — Generación de fragmentos Drupal

Cuando la maqueta esté aprobada, el equipo de desarrollo adapta el HTML a Drupal y devuelve ficheros `pagina N.txt` (fragmentos sin DOCTYPE/html/head/body, con CSS y JS embebidos).

### Estructura del script `scripts/gen_dist.py`

```python
# 1. Cargar imágenes nuevas y redimensionarlas (PIL)
# 2. Leer pagina*.txt del equipo dev (docs/0N-revision-N/)
# 3. Sustituir imágenes antiguas por base64 de las nuevas
# 4. Inyectar CSS extra antes del último </style>:
#    - footer { display: none !important }   ← oculta footer Drupal
#    - .banner-cofinanciacion { ... }        ← banner UE
#    - [fix específicos de Drupal si hay]
# 5. Añadir banner cofinanciación UE antes de <!-- FOOTER -->
# 6. Envolver en HTML mínimo (head solo con meta+title; CSS queda en body)
# 7. Aplicar tabla de traducciones EN_TRANS para versión inglés
# 8. Escribir dist/esp/*.html y dist/ing/*.html
```

Ver `scripts/gen_ryc3.py` de este proyecto como referencia completa.

### Requisitos
```bash
pip install Pillow
python scripts/gen_dist.py
```

### Reglas de imagen para base64

| Tipo | Tamaño máximo | Calidad | Resultado aprox. |
|------|--------------|---------|-----------------|
| Imagen de sección (banda ancha) | 1200×400 px | JPEG 85% | 30–170 KB |
| Logo / banner institucional | 900×200 px | JPEG 90% | 35–45 KB |
| Icono | 200×200 px | PNG | < 10 KB |

Redimensionar siempre antes de codificar en base64. Una imagen de 5 MB sin redimensionar produce un base64 de ~7 MB, lo que hace el fichero inmanejable.

---

## 5. Fase 4 — Entrega al equipo de desarrollo

### Qué entregar

| Fichero | Para qué |
|---------|---------|
| `dist/esp/*.html` | Pegar en Drupal (español) |
| `dist/ing/*.html` | Pegar en Drupal (inglés) |
| `assets/` | Imágenes del live site (referencia) |
| `BRIEFING_PROYECTO.md` | Documentación del proyecto |

**Los ficheros `dist/esp/` y `dist/ing/` son autocontenidos**: llevan CSS, JS e imágenes embebidas. El equipo solo necesita pegarlos en una "Página básica" de Drupal en formato Full HTML.

### Instrucciones para el equipo de desarrollo

```
Cada fichero en dist/esp/ y dist/ing/ corresponde a una Página básica de Drupal.
Procedimiento:
1. Crear/editar la Página básica correspondiente
2. Formato de texto: Full HTML (sin filtros de etiquetas)
3. Pegar el contenido del fichero HTML completo
4. El header y footer de Drupal sustituyen al de la maqueta automáticamente
   (el CSS incluye footer { display: none !important } para suprimir el footer
   de la maqueta si quedara algún residuo)
5. Las imágenes están embebidas: no hay assets que subir al servidor

Si el editor CKEditor reescribe el código:
- Desactivar CKEditor para el formato Full HTML, o
- Pegar en modo "Código fuente" del editor

Si hay error al guardar (fichero muy grande):
- Subir post_max_size en php.ini a 32 MB o más
```

### GitHub Pages como previsualización

El repositorio sirve automáticamente como previsualización:
- Español: `https://ramirez-santigosa.github.io/ryc-web/`
- Inglés: `https://ramirez-santigosa.github.io/ryc-web/en/`

Compartir estas URLs con el equipo de desarrollo y con dirección para validación antes de ir a Drupal.

---

## 6. Gestión del repositorio

### Flujo de trabajo
```
1. Claude Code edita los ficheros HTML/CSS/JS/assets
2. Claude Code hace commit y push a main
3. GitHub Pages publica automáticamente en 1-2 minutos
4. Revisión desde la URL de GitHub Pages
5. Si hay cambios: nueva instrucción a Claude Code → repetir
```

### Commits
- Usar mensajes descriptivos: `feat:`, `fix:`, `refactor:`, `docs:`
- Un commit por ronda de cambios significativa
- El script de generación se ejecuta y los ficheros `dist/` se incluyen en el commit

### Ramas
- `main` — siempre la versión más reciente aprobada
- Si se quiere mantener un backup de versión anterior: crear tag `v1`, `v2`...

---

## 7. CLAUDE.md — Contexto persistente

El fichero `CLAUDE.md` en la raíz del proyecto se carga automáticamente en cada sesión de Claude Code. Debe contener:

```markdown
# [Nombre del proyecto] — Contexto para Claude Code

## Proyecto
[Descripción breve]

## Stack técnico
- HTML5 estático, CSS3 con variables, JS vanilla
- Chart.js CDN si hay dashboard
- Sin frameworks externos

## Convenciones de código
- Variables CSS: --aei-azul, --ryc-dorado, etc.
- Clases BEM-like: .novedad-banda, .convocatoria-card
- Imágenes: assets/ para live site; base64 en dist/ 

## Estado actual
[Versión actual, qué está aprobado, qué está pendiente]

## Rutas importantes
- Live site: [URL GitHub Pages]
- Repositorio: [URL GitHub]
- Script generación: scripts/gen_dist.py
```

Actualizar `CLAUDE.md` al inicio de cada fase nueva o cuando cambie algo significativo.

---

## 8. Lecciones aprendidas (proyecto RYC 2026)

### Hacer siempre desde el principio
- Definir desde el inicio si hay **una o dos versiones** (GitHub Pages / Drupal) y cómo se relacionan
- Usar `scripts/gen_dist.py` para generar `dist/` desde el principio — nunca editar `dist/` a mano
- Poner el **CSS en el body** en los fragmentos Drupal (no en `<head>`)
- Comprobar que todos los assets referenciados **existen** en el repo antes de publicar

### Evitar
- Imágenes base64 sin redimensionar previo (ficheros de decenas de MB)
- Múltiples formatos de salida para el mismo propósito (confusión sobre qué usar)
- Editar los ficheros `dist/` manualmente (se sobreescriben al regenerar)
- Usar Node.js/sharp si Python+PIL es suficiente (más sencillo, sin dependencias de npm)
- Regex con `[^>]*` para reemplazar atributos de `<img>` (elimina atributos `alt` y `loading`)

### Traducción automática
- La tabla `EN_TRANS` cubre texto estático bien, pero **no alcanza el texto dentro de templates JavaScript**
- Revisar manualmente: botones generados por JS, textos de estados, `aria-label`
- Verificar siempre con grep: `grep -n "Ver \|Más \|Histórico" en/pages/*.html`
