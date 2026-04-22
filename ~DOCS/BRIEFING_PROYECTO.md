# BRIEFING — Web Programa Ramón y Cajal 2026

Documento de contexto **específico** de este proyecto. Para las directrices técnicas reusables consultar `DIRECTRICES_TECNICAS.md`; para el flujo con la IA, `PROCEDIMIENTO_IA.md`.

---

## 1. Contexto

### Organismo promotor
Agencia Estatal de Investigación (AEI), Ministerio de Ciencia, Innovación y Universidades.

### Objetivo
Web informativa sobre las **novedades de la convocatoria 2026 del Programa Ramón y Cajal** (RYC), dirigida a personal investigador posdoctoral, universidades y centros de investigación.

### Destino final
Portal de la AEI sobre **Drupal 9.5.11**. El HTML/CSS/JS se integra como bloque o plantilla dentro de Drupal, usando el header y footer institucionales del portal.

### Entornos

| Entorno | URL / Ubicación |
|---------|-----|
| Repositorio GitHub | Remoto `origin/main` (ver `.git/config` del propio `!SALIDA/`) |
| Previsualización (GitHub Pages) — español | Raíz del repo |
| Previsualización (GitHub Pages) — inglés | Subcarpeta `ing/` |
| Drupal — ficheros para pegar | `!SALIDA/*.html` (ES) y `!SALIDA/ing/*.html` (EN) |

---

## 2. Estructura de ficheros

```
09-WEB NUEVO RYC 2026/          (carpeta del proyecto)
│
├── .claude/                     # Datos Claude Code (no va a git)
│
├── !ENTRADA/                    # Material de entrada (no va a git)
│   ├── 01-inicial/
│   ├── 02-primera-revision/
│   ├── 03-segunda-revision/
│   ├── 04-tercera-revision/     # pagina*.txt del equipo dev + imágenes
│   ├── 05-cuarta-revision/      # revisión actual (incluye convocatorias.txt dev)
│   └── datos/                   # Datos originales (xlsx…)
│
└── !SALIDA/                     # ES el repositorio git — .git/ vive aquí dentro
    ├── .gitignore
    ├── CLAUDE.md                # Cargado automáticamente por Claude Code
    ├── index.html               # Español (ver "pendiente 5") 
    ├── novedades-2026.html
    ├── programa-ryc.html
    ├── convocatorias.html
    ├── ing/                     # Inglés
    │   ├── index.html
    │   ├── updates-2026.html
    │   ├── programme.html
    │   └── calls.html
    ├── assets/                  # Fondos de banner referenciados por URL absoluta
    ├── scripts/
    │   └── gen_ryc3.py          # Generador Python (ver PROCEDIMIENTO_IA.md)
    └── ~DOCS/                   # Documentación del proyecto (este directorio)
        ├── BRIEFING_PROYECTO.md        (este documento)
        ├── DIRECTRICES_TECNICAS.md
        ├── DIRECTRICES_CONTENIDO.md
        └── PROCEDIMIENTO_IA.md
```

---

## 3. Páginas

### `index.html` — Inicio RYC
1. Hero (fondo azul con siluetas, título, botones)
2. ¿Qué es el Programa RYC? (descripción + foto edificio AEI + datos clave)
3. Novedades 2026 (5 ítems numerados con iconos)
4. Convocatorias recientes (cards 2026, 2025, 2024, 2023)
5. Banner cofinanciación UE
6. Enlaces de interés (carrusel)

### `novedades-2026.html` — Novedades 2026
1. ¿Para qué cambia la convocatoria?
2. Las 5 grandes novedades (imagen banda + número + contenido)
3. Presentación en vídeo (YouTube embed)
4. ¿Qué implica para las personas candidatas? (4 tarjetas)

> Esta página **no** lleva banner de cofinanciación UE (decisión 4ª revisión).

### `programa-ryc.html` — Programa RYC
1. Historia y objetivos
2. El programa en cifras + dashboard Chart.js
3. Evolución del programa (acordeones 2001–2026)
4. Impacto del programa (foto excavación + 4 tarjetas)
5. 25 años de excelencia (CTA)

### `convocatorias.html` — Convocatorias
Listado de convocatorias RYC 2001–2026, cards estáticas pre-renderizadas con clases BEM `.ryc-card`, enlaces a fichas en aei.gob.es.

---

## 4. Navegación

```
Inicio RYC | Novedades 2026 | Programa RYC | Convocatorias | 25 Años RYC ↗
```
- "25 Años RYC" enlaza directamente a `aei.gob.es` (no tiene página propia).
- Menú responsive con hamburguesa en móvil.

---

## 5. Paleta de colores (resumen)

| Variable | Valor | Uso |
|----------|-------|-----|
| `--aei-azul` | `#1b4c96` | Color principal (títulos, nav, botones, números) |
| `--aei-azul-oscuro` | `#143a73` | Hover |
| `--aei-azul-claro` | `#dae3f3` | Fondos suaves |
| `--ryc-dorado` | `#c8a951` | Acentos: líneas decorativas, nombre "Ramón y Cajal" en títulos |
| `--fondo-claro` | `#f0f4fa` | Fondo general |
| `--fondo-blanco` | `#ffffff` | Tarjetas y secciones |

---

## 6. Textos sensibles — Decisiones editoriales

| Punto | Decisión | Razón |
|-------|----------|-------|
| Novedad 1 | "No será compatible con la convocatoria PID hasta el cuarto año de ejecución" | Redacción definitiva (2ª revisión) |
| Novedad 3 — ERC | Condiciones informe intermedio (texto largo) | Redacción completa sobre mantenimiento de ayudas y trasvase |
| Novedad 4 | Sin cifra de 75.000 € | Retirada por indicación |
| Novedad 5 — Europa Excelencia | "Se incrementa la dotación…" | Sin cifras (2ª revisión) |
| Novedad 5 — R3 | Certificado R3 como investigador/a establecido/a | Nueva viñeta añadida (2ª revisión) |
| CTA final | Retirado el apartado "¿Todo listo?" | A la espera de ficha oficial convocatoria 2026 |
| Criterios evaluación | Orden: aportaciones, calidad, impacto, independencia, viabilidad | Reordenado en 2ª revisión |
| Banner cofinanciación UE | Solo en `index`, `programa-ryc` y `convocatorias` (ES+EN) | 4ª revisión |
| Europa Excelencia / R3 en EN | Se mantienen **sin traducir** | Nombres propios oficiales |

---

## 7. Historial de versiones

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| v1 | mar 2026 | Versión original: paleta granate/dorado, medalla en banner |
| v2 | abr 2026 | Rediseño completo: paleta azul AEI, banners con siluetas |
| v2.1 | 16-04-2026 | 2ª revisión editorial: texto Novedad 1 (PID), reorden criterios, viñeta R3 |
| v2.2 | 21-04-2026 | 3ª revisión: nuevas imágenes base64, banner EU, fix convocatorias CSS |
| v2.3 | 21-04-2026 | Unificación: un solo juego de ficheros para GitHub Pages y Drupal |
| v2.4 | 21-04-2026 | `!SALIDA/` ES el repo (`.git/` dentro); `gen_ryc3.py` sin paso sync |
| v2.5 | 22-04-2026 | 4ª revisión — traducciones faltantes al EN; banner UE retirado de Novedades; rediseño tarjetas convocatorias; ruta PROYECTO autodetectada |
| v2.6 | 22-04-2026 | 4ª revisión — banner UE dentro de `<main>` como `<section>`; eliminadas TODAS las referencias a footer; logo cofinanciación a PNG; regla "sin SVG, sin `<footer>`" documentada |
| v2.7 | 22-04-2026 | 4ª revisión — aislamiento CSS en `<div class="ryc-page">`; scoping con `:where()` para no pisar reglas con clase; adoptado `convocatorias.txt` del dev team (cards estáticas BEM `.ryc-card`) |
| v2.8 | 22-04-2026 | 4ª revisión — fix `<script>` sin cerrar en `convocatorias.txt` (atrapaba el banner UE); wrapper con `find('</style>')` para que el `<nav>` de convocatorias quede dentro y herede la tipografía; `.btn-ryc-outline` igualado a `.btn-ryc` (relleno azul + texto blanco) |

---

## 8. Pendiente para la próxima revisión (🔜)

**Renombrar ficheros y URLs para integración directa en Drupal** — el dev team no debería tener que renombrar enlaces al pegar en Drupal.

### 8.1. Renombrado de ficheros propuesto

| Actual (ES) | Nuevo (ES) | URL Drupal |
|---|---|---|
| `index.html` | `inicio-ryc.html` | `https://www.aei.gob.es/inicio-ryc` |
| `novedades-2026.html` | `novedades-ryc-2026.html` | `https://www.aei.gob.es/novedades-ryc-2026` |
| `programa-ryc.html` | `programa-ryc-2026.html` | `https://www.aei.gob.es/programa-ryc-2026` |
| `convocatorias.html` | `convocatorias-ryc.html` | `https://www.aei.gob.es/convocatorias-ryc` |

### 8.2. Inglés — tres opciones (a confirmar con el dev team)

- **A** — Drupal i18n con mismos slugs y prefijo `/en/`:
  `ing/{inicio-ryc,novedades-ryc-2026,programa-ryc-2026,convocatorias-ryc}.html` → `aei.gob.es/en/…`
- **B** — Slugs traducidos:
  `ing/{ryc-home,ryc-updates-2026,ryc-programme-2026,ryc-calls}.html`
- **C** — URLs exactas que defina el dev team.

### 8.3. Cambios en `gen_ryc3.py`

- Quitar `apply_nav(NAV_ES)` y `apply_nav(NAV_EN)`: en vez de convertir URLs absolutas AEI a relativas, **dejarlas absolutas** para que Drupal las acepte sin tocarlas.
- Añadir `RENAME_MAP` para escribir los ficheros con los nombres nuevos.
- Opcional: generar un `index.html` en la raíz que sea una landing con enlaces a las 4 páginas nuevas (útil para GitHub Pages como índice).

### 8.4. Impacto en GitHub Pages

Los enlaces del nav apuntarán a URLs de producción AEI (que aún no existen hasta que Drupal las dé de alta). Cada página se sigue pudiendo previsualizar individualmente por su URL de GitHub Pages; la "landing" opcional de 8.3 facilita navegar entre las 8 páginas de preview sin salir del repo.
