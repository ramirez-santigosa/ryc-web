# BRIEFING PARA CLAUDE CODE — WEB CONVOCATORIA RAMÓN Y CAJAL (RYC)

## Objetivo

Desarrollar una web para la convocatoria Ramón y Cajal (RYC) dentro del sitio de la Agencia Estatal de Investigación (AEI), lista para trasladar a producción con el mínimo trabajo adicional. El resultado final será un conjunto de archivos HTML/CSS estáticos, bien estructurados, entregables al equipo técnico de la AEI.

---

## Contexto del proyecto

### Sitio principal de referencia
- Web AEI: https://www.aei.gob.es/
- Sección convocatorias: https://www.aei.gob.es/convocatorias
- Ficha actual RYC: https://www.aei.gob.es/noticias/ryc-ramon-cajal
- Web 25 aniversario (referencia de diseño principal): https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal
- Información general del programa: https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal/programa-ramon-cajal

### Vídeo de novedades 2026
https://www.youtube.com/watch?v=Jsm3iyT10r0

### Archivos locales del proyecto
Todos los documentos de contexto y assets están en la carpeta `00-Documentación inicial/`:
- `250602-FECYT-Pin-ramon-y-cajal-AAFF.jpg` → imagen principal de la convocatoria (usar SIN la leyenda de 25 aniversario)
- Documentos con los cambios sustanciales de la convocatoria 2026
- Presentación de las novedades del programa

**Antes de escribir código, lee todos los documentos de `00-Documentación inicial/` para extraer los datos concretos de los cambios de la convocatoria 2026.**

---

## Estructura de páginas a generar

```
index.html                  → Página principal RYC (nueva landing en sección Convocatorias)
pages/novedades-2026.html   → Detalle de cambios y novedades de la convocatoria 2026
pages/convocatorias.html    → Histórico de convocatorias por año (mantenible)
pages/programa.html         → Información general del programa RYC
```

### Archivos de soporte
```
css/styles.css              → Estilos globales
css/ryc.css                 → Estilos específicos RYC
js/main.js                  → Interactividad básica (tabs, acordeones, etc.)
assets/                     → Imágenes y recursos
CLAUDE.md                   → Memoria del proyecto para Claude Code
```

---

## Requisitos de diseño

### Estilo visual
- **Referencia principal:** web 25 aniversario (https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal)
- Visitar y analizar esa web para extraer: paleta de colores, tipografía, estructura de cabecera/pie, componentes usados
- Reutilizar la imagen `250602-FECYT-Pin-ramon-y-cajal-AAFF.jpg` como imagen hero principal, eliminando o tapando visualmente la leyenda del 25 aniversario (recorte CSS o posicionamiento)
- Estética institucional: sobria, clara, accesible

### Navegación
- Menú principal con enlace a cada página
- **Pestaña o enlace destacado** que apunte a la web de los 25 años: https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal
- Breadcrumb: Inicio > Convocatorias > Ramón y Cajal

---

## Requisitos funcionales por página

### index.html — Landing principal RYC
- Hero con imagen de la convocatoria (sin leyenda 25 años)
- Descripción breve del programa
- **Sección destacada "Novedades 2026"** con los cambios principales y CTA a `novedades-2026.html`
- Acceso rápido a la convocatoria vigente
- Enlace/pestaña a la web de los 25 años
- Bloque de convocatorias recientes (últimos 2-3 años) con enlace a `convocatorias.html`

### pages/novedades-2026.html — Cambios convocatoria 2026
- Sección hero con titular impactante sobre los cambios
- **Listado visual de las novedades principales** extraídas de los documentos de `00-Documentación inicial/`
- Embed del vídeo de presentación: https://www.youtube.com/watch?v=Jsm3iyT10r0
- Enlace/botón de descarga a la presentación de novedades (si hay PDF en la carpeta)
- Sección "¿Qué implica para los candidatos?" con los retos que plantean los cambios
- CTA a la convocatoria oficial

### pages/convocatorias.html — Histórico por año
- Tabla o tarjetas por año (más reciente primero)
- Cada fila/tarjeta: año, título oficial, fecha resolución, enlace a ficha en AEI
- **Diseño pensado para mantenimiento fácil:** estructura de datos en un array JS o comentario HTML claro para que sea trivial añadir un nuevo año
- Incluir datos de convocatorias pasadas visibles en https://www.aei.gob.es/noticias/ryc-ramon-cajal

### pages/programa.html — Información general
- Historia y objetivos del programa RYC
- Datos clave (número de investigadores, instituciones, impacto)
- Basado en el contenido de https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal/programa-ramon-cajal

---

## Requisitos técnicos

- **HTML5 semántico** — uso correcto de `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`
- **CSS sin frameworks externos** — o con Bootstrap CDN si facilita el responsive (consultar preferencia)
- **Responsive** — mobile first, funciona en móvil, tablet y escritorio
- **Sin dependencias de servidor** — todo estático, funciona con doble clic en index.html
- **Accesibilidad básica** — atributos `alt` en imágenes, contraste suficiente, navegable por teclado
- **Comentarios en el código** — especialmente en las secciones pensadas para mantenimiento anual
- **Código limpio y entregable** — preparado para que el equipo técnico de la AEI lo integre en su CMS con el mínimo trabajo

---

## Control de versiones

- Repositorio Git local desde el inicio (`git init`)
- Commits frecuentes con mensajes descriptivos
- Preparado para publicar en GitHub Pages para revisión del cliente (rama `main`, carpeta raíz o `/docs`)

---

## Flujo de trabajo sugerido para Claude Code

1. Leer todos los documentos de `00-Documentación inicial/` y extraer datos de novedades 2026
2. Visitar las URLs de referencia de la AEI para analizar estilos y estructura
3. Crear `CLAUDE.md` con el resumen del proyecto y decisiones tomadas
4. Generar `css/styles.css` con las variables de color y tipografía extraídas de la web de referencia
5. Construir `index.html` completo
6. Construir `pages/novedades-2026.html` con los datos reales extraídos
7. Construir `pages/convocatorias.html` con estructura mantenible
8. Construir `pages/programa.html`
9. Revisión de coherencia visual entre páginas
10. Commit final y preparación para GitHub Pages

---

## Entregables finales

- Carpeta completa del proyecto lista para `git push`
- URL de GitHub Pages para revisión del cliente
- Código comentado listo para entrega al equipo técnico de la AEI

---

*Briefing generado el 01/04/2026. Basado en el briefing original del cliente y la sesión de definición del alcance.*
