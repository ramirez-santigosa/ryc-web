# Web Convocatoria Ramón y Cajal (RYC) — Memoria del proyecto

## Descripción
Web estática para la convocatoria Ramón y Cajal dentro del sitio de la AEI (Agencia Estatal de Investigación), con foco en las novedades de la convocatoria 2026.

## Estructura
```
index.html                  → Landing principal RYC
pages/novedades-2026.html   → Detalle de cambios convocatoria 2026
pages/convocatorias.html    → Histórico de convocatorias por año
pages/programa.html         → Información general del programa
css/styles.css              → Estilos globales (variables, layout, componentes)
css/ryc.css                 → Estilos específicos RYC
js/main.js                  → Interactividad (menú móvil, acordeones, tabs)
assets/                     → Imágenes
```

## Decisiones de diseño
- **Paleta de colores:** Basada en la web AEI 25 aniversario
  - Azul institucional AEI: `#264c80`
  - Rojo/granate RYC (del pin): `#8B1A1A`
  - Dorado (acentos): `#C8A951`
  - Fondo claro: `#FAF7F2`
  - Texto principal: `#333333`
- **Tipografía:** Sistema (sin dependencias externas), similar a la AEI
- **Layout:** Bootstrap 5 CDN para grid responsive
- **Imagen hero:** Pin RYC recortado vía CSS para ocultar la leyenda "25 Aniversario"
- **Navegación:** Menú con enlace a web 25 años como pestaña destacada
- **Breadcrumb:** Inicio > Convocatorias > Ramón y Cajal

## Novedades RYC 2026 (datos extraídos de documentación)
1. **Financiación de un proyecto de I+D+i** (5 años) incluida en la ayuda — incompatible con PID
2. **Entrevista en la evaluación** — nuevo proceso con foco en la propuesta científica
3. **Incentivos para participar en el ERC:**
   - ERC financiada → +30% cofinanciación salario
   - ERC máxima calificación sin financiación → Europa Excelencia A + 10% salario
   - ERC segunda fase → Europa Excelencia B + 10% salario
4. **Incentivo a estabilización** — ayuda de 75.000€ por plaza permanente creada (obligatorio)
5. **Desaparece** la convocatoria de Consolidación Investigadora (se integra en RYC)
6. **Desaparece** la ayuda específica de atracción de talento (ya cubierta por proyecto)

## URLs de referencia
- Web AEI: https://www.aei.gob.es/
- 25 años RYC: https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal
- Programa RYC: https://www.aei.gob.es/25-anos-convocatoria-ramon-cajal/programa-ramon-cajal
- Ficha RYC: https://www.aei.gob.es/noticias/ryc-ramon-cajal
- Vídeo novedades: https://www.youtube.com/watch?v=Jsm3iyT10r0

## Mantenimiento
- Para añadir una nueva convocatoria: editar el array `convocatorias` en `pages/convocatorias.html`
- Los estilos usan variables CSS en `:root` para fácil personalización
