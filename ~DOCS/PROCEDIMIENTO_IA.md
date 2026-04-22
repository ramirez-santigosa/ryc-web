# PROCEDIMIENTO — Cómo alimentar a una IA (Claude Code o similar) para generar la maqueta

Esta guía describe **el flujo de trabajo con una IA asistente** (Claude Code, Cursor, Copilot Chat, etc.) encargada de proponer la maqueta web a partir del material que aporta el equipo de contenido.

Se asume que ya se han leído:
- `DIRECTRICES_TECNICAS.md` — qué debe cumplir la maqueta.
- `DIRECTRICES_CONTENIDO.md` — qué material aporta el equipo de contenido.

---

## 1. Modelo mental

La IA no "inventa" la web. **Propone** una maqueta a partir de tres insumos:

1. **Brief inicial** (1 documento) — qué se quiere conseguir y para quién.
2. **Material de contenido e imagen** — fuentes, paleta, fotos, datos (ver `DIRECTRICES_CONTENIDO.md`).
3. **Restricciones técnicas** — CMS destino y reglas de entrega (ver `DIRECTRICES_TECNICAS.md`).

Tú tomas decisiones; la IA propone e implementa. Nunca al revés. Si algo no está claro, **pide que pregunte antes de actuar** — no que asuma.

---

## 2. Estructura de la carpeta del proyecto

```
<nombre-proyecto>/
│
├── .claude/                       # Datos de la IA (no va a git)
│
├── !ENTRADA/                      # Material de entrada (no va a git)
│   ├── 01-inicial/                # Brief + material inicial (ver DIRECTRICES_CONTENIDO)
│   ├── 02-primera-revision/       # Feedback de la primera ronda + nuevos materiales
│   ├── 03-segunda-revision/
│   └── 0N-revision-N/
│
└── !SALIDA/                       # ES el repositorio git — .git/ vive aquí dentro
    ├── .gitignore                 #   contiene únicamente: .claude/
    ├── CLAUDE.md                  # Contexto persistente cargado automáticamente
    ├── *.html                     # Páginas generadas (ES)
    ├── ing/*.html                 # Páginas generadas (EN), si aplica
    ├── assets/                    # Recursos que se referencian por URL absoluta
    ├── scripts/
    │   └── gen_*.py               # Script generador
    └── ~DOCS/                     # Documentación (este directorio)
```

**Regla de oro:** todo lo que está en `!ENTRADA/` es tuyo; todo lo que está en `!SALIDA/` (salvo `.claude/`) lo rastrea git. **Los HTML nunca se editan a mano** — se regeneran con el script.

---

## 3. Arranque del proyecto — Fase 0

### 3.1. Preparar el directorio

1. Crear la carpeta del proyecto.
2. Crear `!ENTRADA/01-inicial/`.
3. Colocar el material inicial siguiendo `DIRECTRICES_CONTENIDO.md`.
4. Crear `!SALIDA/` vacío con un `.gitignore` que contenga `.claude/`.
5. Inicializar git dentro de `!SALIDA/` (`git init`), crear repositorio remoto en GitHub, activar GitHub Pages sobre `main`.

### 3.2. Brief inicial — plantilla

Crear `!ENTRADA/01-inicial/00-BRIEF.md`:

```markdown
# Brief — <Nombre del proyecto>

## Qué es
<Una frase: qué es la iniciativa/programa/servicio cuyo microsite se va a maquetar.>

## Objetivo de la web
<Qué debe comunicar, a quién, para qué. Evitar adjetivos vacíos ("moderna", "atractiva") — ser concreto: "informar a personal investigador posdoctoral de los cambios de la convocatoria 2026 del RYC".>

## Público objetivo
<Perfil(es) principal(es). Máximo 3. Qué saben de antemano, qué vienen a buscar, qué deciden después.>

## Idiomas
<Solo ES, ES+EN, etc.>

## CMS de destino
<Drupal 9.x, WordPress, SharePoint, HTML estático…>

## Restricciones conocidas del CMS
<Filtros HTML, límite de tamaño, si acepta <script>, si acepta base64…>

## URL prevista en producción
<Slug de cada página en el CMS, para que los enlaces internos se generen con esas URLs definitivas.>

## Referencias
<3-5 URLs de webs con estética parecida. Una referencia concreta vale más que mil descripciones.>

## Lo que NO se quiere
<Cosas que se quiere evitar explícitamente. P. ej. "sin medallas decorativas", "sin fondos de imagen en los h2", "sin tipografía serif".>
```

### 3.3. Sentencia de lanzamiento a la IA

Tras colocar el brief y el material, lanzar a la IA con algo así:

```
Lee !ENTRADA/01-inicial/00-BRIEF.md y el resto de material de esa carpeta.
Propón la estructura de la web (páginas, secciones de cada página) en un
documento breve dentro de ~DOCS/ antes de generar nada.
Cuando dé el OK, genera los ficheros HTML en !SALIDA/ (y !SALIDA/ing/ si hay inglés),
siguiendo ~DOCS/DIRECTRICES_TECNICAS.md.
```

Importante: **pedir propuesta antes de generar**. Si la IA genera directamente y no coincide con lo esperado, se pierde tiempo rehaciendo.

---

## 4. Iteraciones — Fases 1…N

Cada ronda de revisión **se deja por escrito** en `!ENTRADA/0N-revision-N/REVISION_N.md`. La IA no retiene memoria fiable entre sesiones: lo que no está escrito, desaparece.

### 4.1. Plantilla de revisión

```markdown
# Revisión N — <fecha>

## Cambios de texto
- Página X, sección Y: sustituir «<texto actual exacto>» por «<texto nuevo>».
- Página X: añadir párrafo tras el punto Z: «<texto>».

## Cambios de imagen
- Página X, sección Y: usar <imagen.png> (fichero adjunto en esta misma carpeta).

## Cambios de diseño / layout
- <Descripción precisa del cambio visual, idealmente con un antes/después o un screenshot.>

## Correcciones
- <Lo que no funciona o está mal.>

## Textos aprobados — NO reescribir
- Sección X: el texto actual ya ha sido validado por <órgano/persona> — no tocarlo.
```

### 4.2. Sentencia de lanzamiento de la revisión

```
Lee el documento <documento-de-la-revision>.docx (o .pdf, o .md) ubicado en
la carpeta !ENTRADA/0N-revision-N/. Aplica todos los cambios indicados.
Sigue las reglas de ~DOCS/DIRECTRICES_TECNICAS.md.
Al terminar, regenera los HTML y pásame un resumen de qué has hecho
antes de subir nada a GitHub.
```

Lo último es crítico: **la IA no debe subir nada a GitHub sin que tú lo autorices**. Por eso hay que pedir "resumen antes de subir".

### 4.3. Validar antes de subir

Antes de dar el OK para commit + push, comprobar:

- Las páginas se ven bien abriendo los HTML **directamente en el navegador** (sin Drupal). Esta comprobación detecta problemas estructurales (scripts sin cerrar, reglas que pisan, etc.) que en Drupal pueden quedar camuflados.
- Los HTML se ven bien pegados en el **CMS de destino** (al menos una página de muestra): layout, tipografías, botones, imágenes.
- El verificador automático del script no deja avisos (por ejemplo, cadenas sin traducir en la versión EN).

### 4.4. Publicación

Con el OK, pedir a la IA:

```
Haz commit con un mensaje descriptivo que explique la revisión aplicada,
sube a main y actualiza ~DOCS/BRIEFING_PROYECTO.md con:
 - nueva versión en el historial
 - cualquier pendiente que haya surgido en esta ronda
```

GitHub Pages recompila en 1–2 minutos. La URL de la preview se puede compartir sin reenviar HTML por correo.

---

## 5. Reglas de oro al trabajar con la IA

### 5.1. Ser concreto

Mal: *"quiero que se vea más limpio"*.
Bien: *"en la tarjeta de la convocatoria 2026, el fondo es demasiado oscuro comparado con las otras; usa el mismo tono que el resto del listado"*.

### 5.2. Indicar la página y la sección

Mal: *"el botón no se lee bien"*.
Bien: *"en `index.html`, en la sección 'Convocatorias recientes', el botón 'Ver histórico completo' sale con fondo transparente; debería tener fondo azul oscuro y texto blanco como los botones de las tarjetas"*.

### 5.3. Pegar el texto actual exacto

Si se quiere cambiar un texto, **pegar literalmente el texto que hay ahora** y **el texto nuevo**. Evitar "donde dice algo parecido a…": la IA puede acertar pero también puede modificar otro sitio.

### 5.4. Revisar la IA — no delegar el juicio

Antes de que la IA suba nada:

- Pedir que **liste qué va a cambiar** (resumen de cambios, no del código).
- Confirmar que coincide con lo pedido.
- Solo entonces autorizar commit + push.

### 5.5. Cuando la IA dice "no encuentro el fichero"

Si la IA no localiza una carpeta o fichero, **darle la ruta exacta** — no aceptar que "no existe" si sabemos que sí. OneDrive, Teams y SharePoint a veces tienen problemas de sincronización o de juntion links que confunden a los buscadores.

### 5.6. Cuando la IA "gasta tokens" dando vueltas

Si la IA hace varios intentos sin resolver:

- Parar y dar un ejemplo concreto de lo que debería hacer.
- O pedir que **lea una referencia concreta** que ya funciona (p. ej.: *"mira cómo lo hace `!ENTRADA/05-cuarta revision/convocatorias.txt` y aprende la diferencia con lo tuyo"*).
- O cambiar de enfoque: si el camino actual es frágil, mejor rediseñarlo que parchearlo más veces.

### 5.7. Cosas que la IA **no** debe hacer sin confirmación explícita

- Hacer `git push` a `main`.
- Modificar carpetas fuera del proyecto.
- Instalar paquetes globales en la máquina.
- Cambiar configuración del repositorio remoto (colaboradores, permisos, branches protegidas).
- Borrar ficheros de `!ENTRADA/` (aunque parezcan obsoletos — pueden ser histórico valioso).

---

## 6. Qué guardar al cerrar cada ronda

Al terminar una ronda de revisión:

- `!ENTRADA/0N-revision-N/` queda como histórico intocable.
- `~DOCS/BRIEFING_PROYECTO.md` refleja el estado actual y lo que queda pendiente.
- El commit de git documenta qué cambió y por qué.
- La URL de GitHub Pages está actualizada para compartir.

Con eso, cualquier persona (incluida tú en una semana) puede retomar el proyecto sin reconstruir contexto.

---

## 7. Checklist rápida antes de empezar

Antes de pedirle a la IA que genere nada, verifica:

- [ ] Carpeta `!ENTRADA/01-inicial/` con el brief y el material de contenido.
- [ ] Repositorio git creado dentro de `!SALIDA/` y remoto en GitHub.
- [ ] GitHub Pages activado sobre `main`.
- [ ] `~DOCS/` con los 4 documentos base: BRIEFING, DIRECTRICES_TECNICAS, DIRECTRICES_CONTENIDO, PROCEDIMIENTO_IA.
- [ ] Brief revisado por alguien que no seas tú (una mirada externa detecta vaguedades).
- [ ] Material gráfico con licencias/atribuciones aclaradas.
- [ ] Slugs de producción del CMS definidos (o al menos, acuerdo con el equipo de desarrollo de cuándo lo estarán).

Cuando los 7 puntos están, se puede lanzar la Fase 0 con confianza.
