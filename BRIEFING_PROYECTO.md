# BRIEFING COMPLETO — Web Programa Ramón y Cajal 2026

## 1. Contexto del proyecto

### Organismo promotor
- **Agencia Estatal de Investigación (AEI)**, dependiente del Ministerio de Ciencia, Innovación y Universidades del Gobierno de España.

### Objetivo
Crear una web informativa sobre las **novedades de la convocatoria 2026 del Programa Ramón y Cajal (RYC)**, que introduce cambios sustanciales respecto a convocatorias anteriores. La web debe comunicar de forma clara y atractiva las 5 grandes novedades de la convocatoria al público objetivo (personal investigador posdoctoral, universidades y centros de investigación).

### Destino final
La web se desplegará en producción dentro del portal de la AEI, que funciona sobre **Drupal 9.5.11**. En ese entorno:
- Se usarán el header y footer institucionales de la AEI (hasta la miga de pan).
- Probablemente se elimine la banda lateral de accesos directos y la página ocupe todo el ancho bajo la miga de pan.
- El contenido HTML/CSS/JS desarrollado aquí se integrará como bloque o plantilla dentro de Drupal.

### Entorno de desarrollo y previsualización
- **Repositorio GitHub:** https://github.com/ramirez-santigosa/ryc-web
- **Producción (GitHub Pages):**
  - Versión actual (v2): https://ramirez-santigosa.github.io/ryc-web/
  - Versión anterior (v1): https://ramirez-santigosa.github.io/ryc-web/v1/
- **Rama principal:** `main` (versión v2, la actual)
- **Rama/tag de respaldo:** `ryc-web_v1` (versión anterior, pre-rediseño)

---

## 2. Estructura de ficheros

```
ryc-web/
├── index.html                  # Página principal (Inicio RYC)
├── pages/
│   ├── novedades-2026.html     # Novedades de la convocatoria 2026
│   ├── programa.html           # Programa RYC (historia, cifras, dashboard)
│   └── convocatorias.html      # Histórico de convocatorias
├── css/
│   ├── styles.css              # Estilos globales (variables, layout, footer, nav)
│   └── ryc.css                 # Estilos específicos RYC (hero, novedades, carrusel)
├── js/
│   ├── main.js                 # Interactividad: menú móvil, acordeones, scroll suave
│   └── datos-ryc.json          # Datos del dashboard (no usado directamente, embebidos en programa.html)
├── assets/                     # Imágenes
│   ├── fondo-banner-azul-aei.png       # Banner página principal (azul claro + siluetas)
│   ├── fondo-banner-azul-degradado.png # Banner novedades (degradado azul oscuro + siluetas)
│   ├── silueta-azul.png               # Silueta de Ramón y Cajal (PNG con alpha)
│   ├── fondo-azul-solo.png            # Fondo sólido azul claro
│   ├── ej-azul-aei-2.png             # Imagen de referencia del diseño del banner index
│   ├── ejemplo-azul-degradado.png     # Imagen de referencia del diseño del banner novedades
│   ├── edificio-aei-bandera.jpg       # Foto sede AEI
│   ├── conferencia-lateral.jpg        # Foto sección impacto (programa.html)
│   ├── aei-dron.png                   # Vista aérea AEI (novedad 5)
│   ├── pin-ramon-y-cajal-2026-azul.jpg    # Pin/medalla azul (no usado en v2, sí en v1)
│   ├── pin-ramon-y-cajal-2026-granate.jpg # Pin/medalla granate (no usado en v2)
│   └── [otras fotos de eventos AEI]
├── v1/                         # Copia estática de la versión anterior (solo lectura)
├── version-fecyt/              # Versión alternativa FECYT (no modificada en este proyecto)
├── 00-Documentación inicial/   # Documentos originales del proyecto (no en git)
├── 00-Logs iniciales/          # Indicaciones de la primera versión (no en git)
├── 01-Documentación revisión/  # Documentos de revisión y nuevos diseños (no en git)
│   └── NUEVOS DISEÑOS/         # Imágenes de referencia para el rediseño
├── 01-Logs revisión/           # Indicaciones de la revisión v2 (no en git)
└── css/ryc-fecyt.css           # CSS versión FECYT (no usado en versión principal)
```

---

## 3. Arquitectura técnica

### Stack
- **HTML5 estático** — sin frameworks ni preprocesadores
- **CSS3** con variables CSS (custom properties) para paleta de colores
- **JavaScript vanilla** — sin dependencias excepto Chart.js para gráficos
- **Chart.js 4.4.7** (CDN) — solo en `programa.html` para el dashboard interactivo

### Dependencias externas
| Recurso | Uso | Carga |
|---------|-----|-------|
| Chart.js 4.4.7 | Dashboard de datos RYC en programa.html | CDN (jsdelivr) |
| Logos AEI/Ministerio | Header institucional | Cargados desde aei.gob.es |
| Fotos Unsplash/Wikimedia | Imágenes ilustrativas en novedades | URLs externas directas |

### Sin servidor
La web funciona abriendo los HTML directamente en un navegador (doble clic) o sirviéndola con cualquier servidor estático. No requiere backend, base de datos ni compilación.

---

## 4. Paleta de colores (v2)

Definida en `:root` de `css/styles.css`:

| Variable | Valor | Uso |
|----------|-------|-----|
| `--aei-azul` | `#1b4c96` | Color principal (títulos, nav, botones, números) |
| `--aei-azul-oscuro` | `#143a73` | Hover de botones y enlaces |
| `--aei-azul-claro` | `#dae3f3` | Fondo del banner principal, fondos suaves |
| `--ryc-granate` | `#1b4c96` | Alias de azul (heredado de v1 donde era granate) |
| `--ryc-granate-oscuro` | `#143a73` | Alias de azul oscuro |
| `--ryc-dorado` | `#c8a951` | Acentos: líneas decorativas, "Ramón y Cajal" en títulos, bordes de botones hero |
| `--ryc-dorado-claro` | `#d4bd7a` | Hover dorado |
| `--fondo-claro` | `#f0f4fa` | Fondo general del body |
| `--fondo-blanco` | `#ffffff` | Fondo de tarjetas y secciones |

**Nota importante:** Las variables `--ryc-granate` y `--ryc-granate-oscuro` ahora contienen valores azules (no granates). Se mantienen los nombres por compatibilidad con selectores existentes. En `programa.html`, no se usa dorado (solo azules).

---

## 5. Páginas y contenido

### 5.1. index.html — Página principal

**Banner:** Fondo azul claro con siluetas de Ramón y Cajal en los laterales (`fondo-banner-azul-aei.png`). Título centrado "Programa Ramón y Cajal" (azul + dorado). Sin medalla/pin. Botones: "Novedades 2026" (azul con borde dorado) y "Ver convocatorias" (outline azul).

**Secciones (en este orden):**
1. **¿Qué es el Programa Ramón y Cajal?** — Descripción + foto edificio AEI + datos clave (25 años, 5 años de ayuda) + botón "Conocer el programa"
2. **Novedades de la Convocatoria 2026** — 5 ítems numerados (círculos blancos sobre azul) con iconos SVG laterales
3. **Convocatorias recientes** — Cards de 2026 (próxima), 2025 (en tramitación), 2024 y 2023 (resueltas)
4. **Enlaces de interés** — Carrusel con flechas (máx. 7, sin loop): 25 Años RYC, Vídeo, Web AEI, Convocatorias AEI, Europa Excelencia

### 5.2. novedades-2026.html — Novedades 2026

**Banner:** Fondo degradado azul oscuro (`fondo-banner-azul-degradado.png`). Texto centrado. Sin medalla. Padding más estrecho que index.

**Secciones:**
1. **¿Para qué cambia la convocatoria?** — Grid 2 columnas (sin carrusel): "Fortalecer la carrera..." y "Mejorar el posicionamiento internacional...". Tarjetas con borde izquierdo dorado.
2. **Las 5 grandes novedades** — Cada una con imagen + banda azul con número y título en mayúsculas:
   - **1. Financiación proyecto propio I+D+i** — Proyecto de 5 años evaluable, no compatible con PID hasta año 4
   - **2. Entrevista en evaluación** — Criterios tabulados: independencia, viabilidad, aportaciones, calidad, impacto
   - **3. Incentivos ERC** — 30%/10% incremento salario + Europa Excelencia + condiciones informe intermedio
   - **4. Estabilización obligatoria** — Ayuda a entidad beneficiaria (sin cifra de 75.000€)
   - **5. Integración convocatorias** — Supresión Consolidación, desaparición atracción talento, incremento Europa Excelencia (sin mención a transferencia PID→RYC)
3. **Presentación en vídeo** — Embed YouTube
4. **¿Qué implica para las personas candidatas?** — 4 tarjetas: Propuesta sólida, Liderazgo, Visión europea, Estabilidad
5. **CTA** — "¿Todo listo para la convocatoria 2026?" (lenguaje inclusivo)

### 5.3. programa.html — Programa RYC

**Banner:** Fondo azul claro (`fondo-banner-azul-aei.png`). Texto en azul oscuro y dorado. Mismo padding estrecho que novedades. **Solo azules, sin dorado en el cuerpo de la página.**

**Secciones (en este orden):**
1. **Historia y objetivos** — Origen (2001), objetivo principal, foto Ramón y Cajal (Wikimedia)
2. **El programa en cifras** — 4 datos (2001, +25, 5, 6,3%) + Dashboard interactivo con Chart.js (3 vistas: género/año, área temática, CCAA). Colores de gráficos: azul claro (#5b9bd5) para mujeres, azul oscuro (#1b4c96) para hombres
3. **Evolución del programa** — Acordeones: 2001, 2012, 2021, 2022, 2023, 2026
4. **Impacto del programa** — Foto conferencia + 4 tarjetas
5. **25 años de excelencia** — CTA hacia web conmemorativa

### 5.4. convocatorias.html — Histórico

Listado de todas las convocatorias RYC desde 2001 hasta 2026 con enlaces a fichas en aei.gob.es.

---

## 6. Navegación

Menú principal (barra azul, presente en todas las páginas):

```
Inicio RYC | Novedades 2026 | Programa RYC | Convocatorias | 25 Años RYC
```

- "25 Años RYC" es un enlace externo a aei.gob.es (sin flecha, con estilo destacado dorado)
- Breadcrumb: Inicio > Convocatorias > Ramón y Cajal > [página actual]
- Menú responsive con hamburguesa en móvil (gestionado por `js/main.js`)

---

## 7. Componentes reutilizables

| Componente | Clase CSS | Descripción |
|------------|-----------|-------------|
| Tarjeta | `.tarjeta` | Caja blanca con sombra y borde izquierdo azul |
| Botón principal | `.btn-ryc` | Fondo azul, texto claro |
| Botón outline | `.btn-ryc-outline` | Borde azul, fondo transparente |
| Botón AEI | `.btn-aei` | Fondo azul institucional |
| Dato clave | `.dato-item` + `.dato-numero` | Número grande + etiqueta |
| Novedad (index) | `.novedad-item` | Número + texto + icono SVG |
| Novedad detalle | `.novedad-detalle` + `.novedad-banda` | Imagen con banda título azul |
| Reto/implicación | `.reto-card` | Tarjeta con borde superior azul |
| Acordeón | `.acordeon` | Expandible con +/− |
| Carrusel | `.carrusel-wrapper` | Wrapper con flechas prev/next, no hay loop |
| Convocatoria | `.convocatoria-card` | Card con año, estado y botón |

---

## 8. Textos sensibles — Decisiones editoriales

Estos textos fueron revisados y aprobados por la dirección. Cambios futuros deben consultarse:

| Punto | Texto actual | Razón |
|-------|-------------|-------|
| Descripción RYC | "de todas las nacionalidades y áreas de conocimiento" | Sustituye "tanto de nacionalidad española como extranjera" por indicación explícita |
| Entrevista | "grado de independencia y la capacidad de liderazgo y la viabilidad" | Redacción específica aprobada |
| Estabilización | "incentivación para la entidad beneficiaria" | Se eliminó la cifra de 75.000€ por indicación |
| Novedad 1 | "que será objeto de la evaluación" | Añadido que el proyecto se evalúa |
| Novedad 1 | "No será compatible con PID hasta el año 4" | "Incompatible" se cambió a "No será compatible" |
| Novedad 3 | Condiciones del informe intermedio | Texto largo sobre mantenimiento de ayudas y trasvase |
| Novedad 5 | Sin "Se transfiere presupuesto de PID a RYC" | Eliminado por indicación |
| CTA final | "¿Todo listo para la convocatoria 2026?" | Lenguaje inclusivo, sustituye "¿Preparada?" |
| Criterios evaluación | Orden: independencia, viabilidad, aportaciones, calidad, impacto | Reordenado dos veces por indicación |
| Banner novedades | "impulsar la excelencia de las universidades y los centros de investigación" | Sin "mejorar la posición de España en Europa" |

---

## 9. Historial de versiones

| Versión | Rama/Tag | Descripción |
|---------|----------|-------------|
| v1 | `ryc-web_v1` + `/v1/` | Versión original: paleta granate/dorado, medalla en banner, carruseles, textos originales |
| v2 | `main` (actual) | Rediseño completo: paleta azul AEI, banners con siluetas, textos actualizados, sin medalla |

### Cambios clave de v1 a v2
- Paleta: granate (#8B1A1A) → azul oscuro (#1b4c96)
- Banners: degradado granate con medalla → fondo azul claro/degradado con siluetas Ramón y Cajal
- Menú: reordenado, "El Programa" → "Programa RYC", sin flechas en "25 Años RYC"
- Textos: múltiples revisiones editoriales (ver tabla arriba)
- Sección "¿Qué es el Programa?" movida a primera posición en index
- Sección "Historia y objetivos" movida a primera posición en programa.html
- Sección "¿Por qué cambia?" → "¿Para qué cambia?" (sin carrusel, grid 2 columnas, sin apartados ERC/dificultades)
- Gráficos del dashboard: colores azul claro/oscuro en vez de granate/azul
- Foto de impacto cambiada (sin vaso tipo cóctel)
- Foto novedad 4 cambiada (sin marcas comerciales)

---

## 10. Notas para futuras modificaciones

### Para cambiar textos
Los textos están directamente en los ficheros HTML. No hay CMS ni base de datos. Buscar el texto a modificar con Ctrl+F en el fichero correspondiente.

### Para cambiar colores
Modificar las variables en `:root` de `css/styles.css`. El cambio se propaga automáticamente. **Excepción:** los colores de los gráficos Chart.js están hardcodeados en el `<script>` de `programa.html` (variables `colMujer` y `colHombre`).

### Para cambiar imágenes de los banners
- Reemplazar `assets/fondo-banner-azul-aei.png` (banner index, azul claro)
- Reemplazar `assets/fondo-banner-azul-degradado.png` (banner novedades, azul degradado)
- La referencia CSS está en `ryc.css` (`.hero` y `.hero-novedades`)

### Para integrar en Drupal
1. Extraer el contenido de `<main>` de cada HTML
2. Incluir los CSS (`styles.css` + `ryc.css`) como assets del tema o módulo
3. Incluir `main.js` para la interactividad
4. En `programa.html`, incluir también Chart.js y el `<script>` del dashboard
5. El header/footer institucional se sustituye por el de Drupal
6. Ajustar las rutas de assets según la estructura de Drupal

### Para añadir una nueva tarjeta al carrusel de enlaces (index.html)
Añadir un nuevo `<div class="tarjeta">` dentro de `#carrusel-enlaces-track`. El carrusel acepta hasta 7 items. El JS se adapta automáticamente.

### Precauciones
- Las imágenes de Unsplash y Wikimedia se cargan desde URLs externas. Si se caen, las fotos de las novedades desaparecen. Considerar descargarlas a `/assets/` antes de producción.
- La variable `--ryc-granate` contiene un azul (#1b4c96), no un granate. Si se necesita volver al granate, cambiar ambas variables y revisar los SVG inline de index.html que tienen colores hardcodeados.
- Los datos del dashboard (2001-2024) están embebidos en el HTML de programa.html, no en un fichero externo. Para actualizarlos, editar los arrays `datosAnio`, `datosArea` y `datosCCAA` en el `<script>`.
