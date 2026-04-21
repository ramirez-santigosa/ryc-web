# Procedimiento: Maqueta web AEI con Claude Code

Guía para crear una maqueta web para el portal de la AEI, revisarla iterativamente y entregarla al equipo de desarrollo para su integración en Drupal.

---

## 1. Estructura de carpetas del proyecto

```
nombre-proyecto/
│
├── BRIEFING_PROYECTO.md       # Documentación completa del proyecto
├── PROCEDIMIENTO.md           # Esta guía
├── CLAUDE.md                  # Contexto persistente para Claude Code
├── .gitignore
│
│  ── ENTRADA (carpetas de trabajo, no van al repositorio) ──────────
│
├── entrada/                   # Archivos fuente que tú pones aquí
│   ├── 01-inicial/            # Brief inicial, imágenes de referencia, indicaciones
│   ├── 02-revision-1/         # Documentos y notas de la 1ª ronda de revisión
│   ├── 03-revision-2/         # Documentos de la 2ª ronda
│   └── 04-revision-N/         # Fragmentos .txt del equipo dev + imágenes definitivas
│
├── datos/                     # Datos originales y procesados (xlsx, csv...)
│
│  ── SOPORTE (imágenes del live site, van al repositorio) ──────────
│
├── assets/                    # Imágenes referenciadas por URL absoluta desde dist/
│   └── icons/                 # Iconos PNG
│
│  ── SCRIPTS (van al repositorio) ─────────────────────────────────
│
├── scripts/
│   └── gen_dist.py            # Script Python: genera dist/ a partir de entrada/
│
│  ── SALIDA (generado automáticamente, va al repositorio) ──────────
│
└── dist/                      # Fragmentos para pegar en Drupal — NO editar a mano
    ├── esp/                   # Español: inicio.html, novedades.html, programa.html, convocatorias.html
    └── ing/                   # Inglés: home.html, updates.html, programme.html, calls.html
```

### .gitignore mínimo
```
entrada/
datos/
.claude/
```

> **Regla de oro:** Todo lo que esté en `entrada/` y `datos/` es tuyo y no va al repositorio.
> Todo lo que esté en `dist/` lo genera el script — nunca edites esos ficheros a mano.

---

## 2. Fase 1 — Brief inicial a Claude Code

### Cómo dar las directrices

Crear un fichero `entrada/01-inicial/BRIEF_INICIAL.md` con:

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
[Lista de ficheros en entrada/01-inicial/ con descripción de cada uno]

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
Lee el fichero entrada/01-inicial/BRIEF_INICIAL.md y crea la maqueta completa.
Genera directamente los fragmentos en dist/esp/ (y dist/ing/ si hay inglés).
Cada fichero debe ser autocontenido: CSS en el body, imágenes embebidas en base64.
Sigue el estilo visual de la AEI (azul #1b4c96, variables CSS, sin frameworks externos).
```

Claude Code generará directamente los fragmentos en `dist/esp/`. No hace falta estructura intermedia de `pages/` ni carpetas de CSS/JS separadas — todo va embebido en los HTML de salida.

---

## 3. Fase 2 — Revisiones iterativas

### Cómo dar indicaciones de revisión

Cada ronda de revisión va en un fichero en `entrada/0N-revision-N/`:

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
Lee entrada/0N-revision-N/REVISION_N.md y aplica todos los cambios indicados.
Regenera dist/ al terminar.
```

### Buenas prácticas para revisiones

- **Una revisión por ronda**: no mezclar cambios de diferentes fechas en el mismo documento
- **Precisión**: indicar página, sección y texto exacto — evitar "cambia el apartado de novedades"
- **Imágenes**: dejar los ficheros nuevos en la carpeta de la revisión con nombres descriptivos
- **Textos aprobados**: si un texto ha sido validado por dirección, indicarlo explícitamente para que no se modifique

---

## 4. Fase 3 — Integración Drupal (fragmentos del equipo dev)

Cuando la maqueta esté aprobada, el equipo de desarrollo adapta el HTML a Drupal y devuelve ficheros `pagina N.txt` (fragmentos sin DOCTYPE/html/head/body, con CSS y JS embebidos). Dejar esos ficheros en `entrada/04-revision-N/`.

### Estructura del script `scripts/gen_dist.py`

```python
# 1. Cargar imágenes nuevas de entrada/0N-revision-N/ y redimensionarlas (PIL)
# 2. Leer pagina*.txt del equipo dev (entrada/0N-revision-N/)
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

Redimensionar siempre antes de codificar en base64. Una imagen de 5 MB sin redimensionar produce un base64 de ~7 MB, haciendo el fichero inmanejable.

---

## 5. Fase 4 — Entrega al equipo de desarrollo

### Qué entregar

| Fichero | Para qué |
|---------|---------|
| `dist/esp/*.html` | Pegar en Drupal (español) |
| `dist/ing/*.html` | Pegar en Drupal (inglés) |
| `assets/` | Imágenes del live site (referencia, fondos de banners) |
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
   (el CSS incluye footer { display: none !important })
5. Las imágenes están embebidas: no hay assets que subir al servidor

Si el editor CKEditor reescribe el código:
- Desactivar CKEditor para el formato Full HTML, o
- Pegar en modo "Código fuente" del editor

Si hay error al guardar (fichero muy grande):
- Subir post_max_size en php.ini a 32 MB o más
```

### GitHub Pages como previsualización

Si el repositorio está publicado en GitHub Pages, los ficheros `dist/` funcionan directamente en el navegador (son HTML completos). Compartir las URLs con el equipo de desarrollo y con dirección para validación antes de ir a Drupal.

---

## 6. Gestión del repositorio

### Flujo de trabajo
```
1. Colocar fuentes en entrada/ (imágenes, fragmentos .txt, notas)
2. Claude Code aplica los cambios y regenera dist/
3. Claude Code hace commit y push a main
4. GitHub Pages publica automáticamente en 1-2 minutos
5. Revisión desde la URL de GitHub Pages
6. Si hay cambios: nueva instrucción a Claude Code → repetir
```

### Commits
- Usar mensajes descriptivos: `feat:`, `fix:`, `refactor:`, `docs:`
- Un commit por ronda de cambios significativa
- Incluir siempre los ficheros `dist/` en el commit

### Ramas
- `main` — siempre la versión más reciente aprobada
- Para backup de versión anterior: crear tag `v1`, `v2`...

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
- CSS embebido en el body (no en head) para compatibilidad Drupal
- Imágenes embebidas en base64 en dist/

## Carpetas clave
- Fuentes: entrada/0N-revision-N/ (fragmentos .txt + imágenes nuevas)
- Assets live site: assets/
- Script de generación: scripts/gen_dist.py
- Salida: dist/esp/ y dist/ing/

## Paleta de colores
- --aei-azul: #1b4c96
- --aei-azul-oscuro: #143a73
- --ryc-dorado: #c8a951
- [etc.]

## Estado actual
[Versión actual, qué está aprobado, qué está pendiente]
```

Actualizar `CLAUDE.md` al inicio de cada fase nueva o cuando cambie algo significativo.

---

## 8. Lecciones aprendidas (proyecto RYC 2026)

### Hacer siempre desde el principio
- Separar claramente **entrada/** (tuyo) de **dist/** (generado) — nunca editar dist/ a mano
- Poner el **CSS en el body** en los fragmentos Drupal, no en `<head>` (Drupal lo descarta)
- **Redimensionar** las imágenes antes de codificarlas en base64 (máx. 1200×400 px)
- Comprobar que todos los assets referenciados en CSS existen en `assets/` antes de publicar

### Evitar
- Imágenes base64 sin redimensionar previo (ficheros de decenas de MB)
- Editar los ficheros `dist/` manualmente (se sobreescriben al regenerar)
- Usar Node.js/sharp si Python+PIL es suficiente (más sencillo, sin dependencias de npm)
- Regex con `[^>]*` para reemplazar atributos de `<img>` (elimina `alt` y `loading`)
- Estructuras paralelas redundantes (p.ej. `pages/` + `dist/esp/` para lo mismo)

### Traducción automática
- La tabla `EN_TRANS` cubre texto estático bien, pero **no alcanza el texto dentro de templates JavaScript**
- Revisar manualmente: botones generados por JS, textos de estados, `aria-label`
- Verificar siempre: `grep -n "Ver \|Más \|Histórico" dist/ing/*.html`
