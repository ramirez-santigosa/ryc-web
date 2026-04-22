# DIRECTRICES TÉCNICAS — Maquetas HTML para portales Drupal

Guía genérica y reusable para nuevos proyectos. Nace de las lecciones aprendidas en la web RYC 2026 (ver `BRIEFING_PROYECTO.md` para el proyecto actual).

Público objetivo: responsable técnico / desarrollador / IA asistente que va a maquetar un bloque HTML independiente para pegarlo dentro de un portal Drupal.

---

## 1. Principio rector: aislamiento

La maqueta se entrega como **un bloque HTML autocontenido** que:

1. **No modifica la estética del resto del portal** en el que se incrusta.
2. **No depende de rutas locales** (imágenes embebidas, sin enlaces a `assets/` relativos).
3. **No toca el `<header>` ni el `<footer>`** institucional del portal — esos los pinta el CMS.

Todo lo que rompa alguna de estas tres reglas tarde o temprano da problemas al pegar en Drupal.

---

## 2. Stack

| Elemento | Recomendación |
|---|---|
| HTML | HTML5 estático, sin frameworks ni preprocesadores |
| CSS | CSS3 con variables (custom properties), **embebido en el body** del fragmento (no en `<head>`: Drupal lo descarta) |
| JS | Vanilla, sin dependencias. Excepciones permitidas: CDN estables tipo Chart.js si hacen falta gráficos |
| Imágenes | **PNG** para logos, iconos y cualquier cosa con texto; **JPEG** para fotografías. **Nunca SVG** (los filtros de Drupal los reescriben o descartan) |
| Entrega | Un solo fichero HTML por página, **con CSS, JS e imágenes embebidas** en base64 |

---

## 3. Reglas de imagen

| Tipo | Formato | Tamaño máximo | Calidad | Resultado aprox. |
|------|---------|---------------|---------|------------------|
| Foto de sección (banda ancha) | **JPEG** | 1200×400 px | 85% | 30–170 KB |
| Logo / banner institucional (con texto) | **PNG** | 800×200 px | — | 40–90 KB |
| Icono | **PNG** | 200×200 px | — | < 10 KB |

- **Redimensionar antes de codificar** en base64. Una imagen de 5 MB sin redimensionar produce un base64 de ~7 MB y el fichero resulta inmanejable en Drupal.
- **Sin SVG**: ni inline `<svg>` ni referenciados `.svg`. Rasterizar siempre. Razón: los filtros de CKEditor/Drupal los pueden descartar al pegar.
- **Sin dependencias externas**: nada de URLs a `images.unsplash.com`, `upload.wikimedia.org`, etc. Todo embebido en base64.

---

## 4. Aislamiento CSS — contenedor `.<prefijo>-page`

Todo el HTML visible se envuelve en un **único contenedor con clase propia**:

```html
<div class="ryc-page">
  ...contenido...
</div>
```

Y **todas las reglas CSS globales** (selectores sin clase: `body`, `html`, `*`, `img`, `a`, `main`) se reescriben para aplicarse **sólo dentro** de ese contenedor.

### Dos estrategias según si quieres "ganar" o no sobre otras reglas

| Regla original | Reescritura | Especificidad | Efecto |
|---|---|---|---|
| `body { … }`   | `.ryc-page { … }`                 | 0,1,0 | Gana sobre tema Drupal; aplica tipografía / fondo al wrapper |
| `html { … }`   | `.ryc-page { … }`                 | 0,1,0 | Idem |
| `main { … }`   | `.ryc-page main { … }`            | 0,1,1 | Gana (solo hay un `<main>` propio) |
| `*, *::before, *::after { … }` | `:where(.ryc-page, .ryc-page *, …) { … }` | **0,0,0** | Resetea sin aumentar especificidad |
| `img { … }`    | `:where(.ryc-page) img { … }`     | **0,0,1** | Lo mínimo; NO pisa `.logo { height: 72px }`, `.banda img { max-height: 320px }`, etc. |
| `a { … }`      | `:where(.ryc-page) a { … }`       | **0,0,1** | NO pisa `.btn { color: #fff }` (los botones conservan el texto blanco) |
| `a:hover { … }`| `:where(.ryc-page) a:hover { … }` | **0,0,2** | Idem |

> **Por qué `:where()`**: sin él, `.ryc-page img` (0,1,1) pisaría a `.logo-cofinanciacion` (0,1,0) con `height: 72px` → logo enorme. Y `.ryc-page a { color: azul }` pisaría a `.btn-primary { color: #fff }` → botones azul-sobre-azul ilegibles.

### Posición del wrapper

El wrapper se abre **justo después del PRIMER `</style>`** del fragmento. Si hay dos bloques `<style>` separados por HTML (patrón que a veces usa el dev team), hay que envolver desde el primer cierre, no desde el último — de lo contrario el `<nav>` y otros elementos quedan fuera del wrapper y no heredan la tipografía del body.

---

## 5. Nomenclatura BEM con prefijo

Para **componentes nuevos** (cards, listas, widgets…), usar clases con **prefijo corto** y formato BEM:

```css
.ryc-card               /* bloque */
.ryc-card__titulo       /* elemento */
.ryc-card__estado       /* elemento */
.ryc-card--vigente      /* modificador del bloque */
.ryc-card__estado--proxima   /* modificador del elemento */
.ryc-btn
.ryc-btn--dorado
.ryc-btn--outline
```

Ventajas:

- El prefijo (`ryc-`, `inv-`, `conv-`…) garantiza que no colisiona con nada del CMS.
- BEM separa estructura (bloque) de variantes (modificador) sin depender del anidamiento.
- Un `<div class="ryc-card__titulo">` es más robusto en Drupal que un `<h3>` con clase: los filtros pueden reescribir atributos y estilos de elementos semánticos (`h3`, `button`, `form`…) más agresivamente.

---

## 6. Sin `<footer>` propio, sin `<header>` propio

El footer y el header institucionales los pinta **el CMS**. La maqueta **nunca** debe:

- Incluir un elemento `<footer>` ni `<header>` propio.
- Definir reglas CSS sobre `footer`, `.footer`, `.footer-grid`, `.footer-bottom`, `header`, `.header-institucional`, etc. (aunque no haya elemento asociado): el día que Drupal renderiza un `<div class="footer">`, nuestra regla `.footer { background: azul }` lo estilizaría por accidente.
- Ocultar footer con `display: none !important` sobre `footer` o similar: **oculta también el footer institucional**.

Si los fragmentos del equipo dev traen bloques CSS "Footer" o comentarios `<!-- FOOTER -->`, limpiarlos antes de entregar.

---

## 7. Banner / llamadas destacadas dentro del cuerpo

Para elementos tipo "banner de cofinanciación UE" o llamadas finales, **ubicarlos dentro de `<main>`** (o del wrapper `.ryc-page`), como `<section>`, **nunca** como `<footer>` (ver punto 6). Esto garantiza:

- Que el CMS no los trate como parte del footer institucional.
- Que siguen visibles aunque se oculten los footers del CMS.

---

## 8. Pipeline de generación — responsabilidades del script

El script de generación (p. ej. `scripts/gen_<proyecto>.py`) debe, para cada fragmento de entrada:

1. **Redimensionar y embeber imágenes** en base64 (PNG / JPEG según regla 3).
2. **Eliminar referencias a footer**: bloques CSS `.footer/.footer-grid/.footer-bottom` y comentarios `<!-- FOOTER -->`.
3. **Inyectar CSS adicional** que haga falta (banner cofinanciación, overrides puntuales).
4. **Scopar reglas globales** a `.<prefijo>-page` según tabla del punto 4 (`body`/`html`/`main` directo, `img`/`a`/`*` con `:where()`).
5. **Envolver** el HTML visible en `<div class="<prefijo>-page">…</div>` tras el **primer** `</style>`.
6. **Cerrar `<script>` abiertos** si el fragmento fuente deja alguno sin cerrar: recuento `<script>` vs `</script>` y añadir los `</script>` que falten. (Ejemplo real: `convocatorias.txt` del dev team lo deja abierto; sin cerrar, todo lo que viene detrás queda atrapado dentro del script y no se renderiza).
7. **Resolver traducciones** (tabla `EN_TRANS` o similar) del español al idioma destino.
8. **Verificar** que no queden cadenas en el idioma origen en los ficheros destino.

Ejemplo de verificador:

```
- "OK — todo traducido" → sin problemas, listo para commit
- "AVISO fichero.html: falta traducir «…»" → añadir el patrón a EN_TRANS y regenerar
```

---

## 9. Ruta del proyecto — autodetectar, nunca hardcodear

Las rutas absolutas al proyecto (p. ej. `C:/Users/.../OneDrive - MINISTERIO DE CIENCIA…`) **no deben quedar escritas a fuego** en el script: si la carpeta OneDrive cambia de nombre (paso de "MCI" a "MICIU", por ejemplo), el script deja de funcionar. Autodetectar siempre:

```python
PROYECTO = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
)
```

---

## 10. Integración en Drupal

### Procedimiento para cada página

1. Abrir el fichero HTML con un editor de texto.
2. En Drupal: crear / editar la Página básica correspondiente.
3. Formato de texto: **Full HTML** (sin filtros de etiquetas).
4. Pegar el contenido completo del fichero (incluido el `<!DOCTYPE html>` — Drupal lo ignora).
5. Guardar y previsualizar.

### Problemas frecuentes y solución

| Síntoma | Causa | Solución |
|---|---|---|
| CSS o JS desaparecen al guardar | El formato filtra `<style>` / `<script>` | Usar **"Full HTML"** sin filtros |
| CKEditor "limpia" el código | CKEditor reescribe HTML | Pegar en modo **"Código fuente"** o desactivar CKEditor para ese formato |
| Error al guardar (fichero grande) | `post_max_size` PHP < 32 MB | Subir `post_max_size` a ≥ 32 MB |
| Estilos no se aplican | CSS estaba en `<head>` (Drupal lo descarta) | Mover CSS al body en el generador |
| El footer institucional desaparece | Regla nuestra `display:none` sobre `footer` | Eliminar; ver punto 6 |
| Tarjetas / botones con layout colapsado | Reglas de Drupal pisan selectores de elemento (`h3 span`, etc.) | Usar BEM con prefijo (punto 5) en lugar de elementos semánticos con span decorativos |

---

## 11. Entrega y previsualización con GitHub

### El directorio de salida **es el repositorio git**

El repo (`.git/`) vive **dentro** del directorio de salida, no en la raíz del proyecto. Así la raíz queda limpia para material de entrada y documentación, y lo que se versiona y publica es exactamente lo que se entrega.

### GitHub Pages como previsualización + enlace compartible

Publicar el directorio de salida en GitHub Pages permite:

- **Previsualizar la maqueta** en el navegador exactamente como se verá (sin tener que montar un servidor local).
- **Compartir por enlace** con cualquier persona (dirección, equipo de contenido, dev team) sin enviar ficheros HTML por correo (que suelen rebotar por seguridad).
- Cada push a `main` actualiza la preview en 1–2 minutos, de modo que las iteraciones son inmediatas.

> No hay carpeta `dist/` separada: los mismos ficheros sirven para GitHub Pages y para entregar a Drupal. Un único juego de ficheros, cero sincronización manual.

### Flujo recomendado

```
1. Colocar fuentes en !ENTRADA/ (brief, imágenes, fragmentos .txt…)
2. IA aplica los cambios y regenera los HTML en el directorio de salida
3. El script imprime "OK — todo traducido" o avisos
4. Si hay avisos, corregir y regenerar hasta pase limpio
5. Commit + push a main
6. GitHub Pages actualiza la preview en 1-2 min
7. Compartir URL con los interesados
8. Nueva ronda de revisión → repetir
```

### `.gitignore` mínimo

```
.claude/
```

`!ENTRADA/` queda automáticamente fuera del repo por estar **fuera** del directorio que contiene `.git/`.

---

## 12. Lecciones aprendidas — evitar siempre

- Imágenes base64 sin redimensionar previo (ficheros de decenas de MB).
- Editar los HTML manualmente (se sobrescriben al regenerar).
- Usar Node.js / sharp cuando Python + PIL es suficiente (más sencillo, sin dependencias de npm).
- Regex con `[^>]*` para reemplazar atributos de `<img>` (elimina `alt` y `loading`).
- Carpetas `dist/` o `pages/` intermedias: los ficheros definitivos van directamente al directorio de salida.
- **Elementos `<svg>` o recursos `.svg`** (ver punto 3).
- **`<footer>` propio ni reglas `footer/.footer`** (ver punto 6).
- **Scopar reglas globales sin `:where()`**: sube la especificidad y pisa reglas con una sola clase (ver punto 4).
- **Selectores de elemento (`h3`, `span`, `button`…) en el HTML entregable**: los filtros del CMS pueden reescribir sus atributos. Preferir `<div>` con clase BEM prefijada (ver punto 5).
- **Hardcodear rutas absolutas** al proyecto en los scripts (ver punto 9).
- **Dos reglas con prefijo ambiguo** en la tabla de traducciones (p. ej. "Estabilización obligatoria con incentivo" vs "…con incentivo económico"): la corta puede "cortar" parte de la larga. Usar siempre el delimitador completo (`<h3>…</h3>`) en los patrones para evitarlo.
- **Asumir que `<script>` del fragmento origen está cerrado**: a veces el dev team lo deja abierto (porque al pegar en Drupal lo cierra el CMS). Para HTML estático hay que cerrarlo explícitamente; si no, atrapa todo el HTML posterior (banner, `</body>`…) como JavaScript no ejecutado.
- **`rfind` vs `find` para localizar el `</style>` del cierre**: si el fragmento trae varios bloques `<style>` separados por HTML, `rfind` deja el primer bloque HTML (normalmente el `<nav>`) **fuera** del wrapper de aislamiento → el nav no hereda la tipografía y se ve con la del user-agent. Usar `find` (el primer cierre).
