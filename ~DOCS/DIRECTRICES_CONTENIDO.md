# DIRECTRICES PARA EL EQUIPO DE CONTENIDO

Qué material aporta el equipo responsable del contenido y de la imagen corporativa al inicio de un proyecto de maqueta web. Esta guía **no pide número de páginas ni texto concreto** — esas propuestas las hace la IA a partir del material que se le entrega.

El objetivo es proporcionar **fuentes de información** y **decisiones de marca** claras, no redactar la web.

---

## 1. Qué tipo de documentos aportar (no qué contenido)

En general, **mejor entregar el documento original íntegro** (informe, presentación, BOE, memoria) que un resumen. La IA sabe extraer y reformular; lo que necesita es acceso a la fuente primaria.

### 1.1. Documentos sobre el programa o iniciativa

- **Normativa oficial**: convocatoria publicada en boletín oficial, bases, resolución, decreto…
- **Ficha descriptiva** del programa/servicio en formato PDF o Word: objetivos, requisitos, quién puede participar, plazos típicos.
- **Documentos de planificación**: plan estratégico, plan anual de actuación, memoria anual, contrato de gestión, indicadores.
- **Histórico**: si existe una página previa del mismo servicio, aportar su URL o un volcado del contenido.
- **Informes de evaluación o impacto** si los hay (AIReF, tribunal de cuentas, internos…).

### 1.2. Documentos sobre las novedades / motivo del proyecto

- **Memoria justificativa** de los cambios respecto a versiones anteriores.
- **Notas de prensa** o comunicados oficiales ya publicados.
- **Presentaciones internas** usadas en comités, patronatos o consejos rectores.
- Cualquier cuadro comparativo "versión anterior vs versión nueva" si existe.

### 1.3. Datos para gráficos y dashboards

Si la página incluye cifras, evolución histórica o visualizaciones:

- **Tablas en formato abierto** (CSV, Excel con datos limpios en una hoja). Indicar claramente columnas, unidades, rango temporal, fuente.
- **Última fecha de actualización** de cada dataset.
- Persona de contacto del órgano que custodia los datos (por si hay dudas de interpretación).

### 1.4. Glosario y tono

- **Lista de términos técnicos** del dominio con su definición corta preferida.
- **Decisiones de estilo**: tuteo / usted, lenguaje inclusivo (forma preferida), siglas que deben desarrollarse siempre la primera vez, siglas que nunca se desarrollan, etc.
- **Textos ya aprobados por dirección** que **no deben reescribirse** (señalados explícitamente como intocables).

---

## 2. Identidad visual — qué decisiones aportar

### 2.1. Paleta de colores

Entregar los colores corporativos en **formato reutilizable**, no capturas de pantalla:

- Valores hex (`#1b4c96`) o RGB.
- Rol de cada color: principal, secundario, acento, fondos, texto, líneas, hover, estados (éxito, aviso, error) si aplican.
- Si hay pareja "claro / oscuro" para modo accesible, indicarla.

### 2.2. Tipografía

Indicar:

- Tipografía preferida para títulos y para texto corrido (o si se acepta una stack de sistema tipo `-apple-system, Segoe UI, Roboto, Arial, sans-serif`, que es lo más robusto para Drupal).
- Pesos disponibles (400, 500, 600, 700).
- Si hay un archivo de fuente propio, aportarlo (aunque por norma general los proyectos integrados en Drupal usan la tipografía del tema del portal).

### 2.3. Tono visual — referencias

En lugar de describir con palabras, es más útil entregar **ejemplos concretos**:

- 3–5 URLs de páginas web existentes con una estética parecida a la que se busca.
- Capturas de memoria anual, cartel promocional, diapositiva de presentación institucional que representen el estilo objetivo.
- Si hay una web previa de la misma marca/programa que sirva de referencia (aunque esté obsoleta), aportar su URL.

---

## 3. Material gráfico

### 3.1. Fotografías

- Entregar en **resolución alta original** (la IA reducirá). Mínimo 1200 px en el lado largo.
- Formato: JPG o PNG. **No** SVG (se rasterizan antes de embeberse).
- **Atribución y licencia** de cada foto: autor, fuente, si es dominio público / Creative Commons / propia del organismo / banco de imágenes con licencia.
- Si la foto va a ir como fondo de banda ancha (hero), entregar el encuadre con espacio sobrante para recortar.

### 3.2. Logos

- Logo institucional en alta resolución, fondo transparente (PNG) o vectorial (SVG, solo como fuente — la IA lo rasteriza).
- Versiones que existan: color, blanco, negro, monocromo.
- **Zona de respeto** del logo si hay manual de identidad corporativa.

### 3.3. Iconos

- Si hay un set de iconos propio (corporativo), entregarlo. Si no, indicar un set público de referencia (Heroicons, Feather, Material…).
- Estilo preferido: outline, filled, duotone…

### 3.4. Vídeos embebidos

- URL de YouTube / Vimeo (solo embeds, no hay que subir el vídeo a la web).
- Título y descripción breve del vídeo tal como se quiere mostrar.
- Si el vídeo aún no está publicado, indicar cuándo estará disponible.

---

## 4. Enlaces externos

Lista de todos los enlaces externos que deben aparecer en la web:

- URL completa (no descripción tipo "buscador de AEI" sin la URL).
- A qué apartado de la web enlaza (hero, sidebar, CTA final, carrusel de enlaces de interés…).
- Si el enlace debe abrir en pestaña nueva (`target="_blank"`).

---

## 5. Entorno técnico de destino

Información que el equipo de contenido conoce pero que el maquetador necesita saber:

- **CMS de destino**: Drupal (versión), WordPress, SharePoint, HTML estático…
- **URL prevista** de cada página ya en producción (slugs de Drupal), para que los enlaces internos se generen con esas URLs definitivas y al pegar en el CMS no haya que renombrar nada.
- **Idiomas**: solo castellano, castellano + inglés, multilingüe completo.
- **Restricciones conocidas** del CMS (filtros HTML, límite de tamaño de página, si acepta `<script>` embebido, si acepta imágenes base64…).

---

## 6. Formato de entrega al maquetador

Estructura recomendada de la carpeta de entrada:

```
!ENTRADA/
├── 01-inicial/
│   ├── 00-BRIEF.md               (objetivo, público, tono — ver PROCEDIMIENTO_IA.md)
│   ├── 10-paleta-colores.md      (hex + rol de cada color)
│   ├── 20-tipografia.md
│   ├── 30-material-grafico/       (fotos, logos, iconos sin tocar)
│   ├── 40-documentos-fuente/      (normativa, memoria, presentaciones…)
│   ├── 50-datos/                  (xlsx, csv para gráficos)
│   ├── 60-enlaces-externos.md     (lista de URLs)
│   └── 70-referencias-visuales/   (capturas, URLs de webs parecidas)
│
└── 0N-revision-N/                 (una carpeta por ronda de feedback)
    ├── REVISION_N.md              (cambios solicitados, ver PROCEDIMIENTO_IA.md)
    └── imágenes-nuevas/           (solo las que cambian)
```

- **Nombres de fichero descriptivos y numerados** para que el orden alfabético refleje el orden de lectura.
- **Un documento = un propósito**. Evitar `DOCUMENTO_GENERAL_V5_final_definitivo.docx` con de todo mezclado.
- Si un documento es confidencial o interno, marcarlo en el nombre y avisar al responsable técnico.

---

## 7. Qué **no** hace falta aportar

El equipo de contenido **no** tiene que:

- Proponer el número de páginas ni la estructura del site — lo propone la IA y se ajusta en iteraciones.
- Escribir los textos ya "maquetados" (títulos, subtítulos, pies, CTAs): la IA propone a partir del material fuente.
- Decidir qué imagen va en qué sección: la IA propone un layout y se revisa.
- Generar capturas, wireframes o mockups previos (salvo que existan por otra vía y se quieran entregar como referencia).

El valor del equipo de contenido está en **las fuentes, las decisiones de marca y las intocables** — no en pre-maquetar la web.
