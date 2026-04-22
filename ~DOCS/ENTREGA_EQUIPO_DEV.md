# Despliegue en Drupal — Web Programa Ramón y Cajal 2026

Se adjuntan 8 ficheros HTML listos para pegar en Drupal (4 en español, 4 en inglés). **No hay assets que subir** — CSS, JS e imágenes van embebidos en cada fichero.

## Ficheros

| Fichero | Página Drupal |
|---------|--------------|
| `index.html` | Inicio RYC (español) |
| `novedades-2026.html` | Novedades 2026 (español) |
| `programa-ryc.html` | Programa RYC (español) |
| `convocatorias.html` | Convocatorias (español) |
| `ing/index.html` | RYC Home (inglés) |
| `ing/updates-2026.html` | 2026 Updates (inglés) |
| `ing/programme.html` | RYC Programme (inglés) |
| `ing/calls.html` | Calls (inglés) |

## Procedimiento para cada página

1. Abrir el fichero HTML con un editor de texto
2. En Drupal: crear o editar la Página básica correspondiente
3. Formato de texto: **Full HTML** (sin filtros de etiquetas)
4. Pegar el contenido completo del fichero
5. Guardar

El header y footer institucional de Drupal funcionan con normalidad — el CSS de cada página oculta automáticamente el footer duplicado.

> **Banner de cofinanciación UE**: aparece embebido en el cuerpo de `index`, `programa-ryc`, `convocatorias` (ES) y sus equivalentes en `ing/`. **No** aparece en `novedades-2026.html` ni `ing/updates-2026.html` — esto es intencional (decisión de la 4ª revisión).

## Si hay problemas al guardar

| Síntoma | Solución |
|---------|----------|
| CKEditor reescribe el HTML | Pegar en modo **Código fuente** |
| Error al guardar por tamaño | Subir `post_max_size` en php.ini a **32 MB** o más |
| CSS o JS desaparecen al guardar | Verificar que el formato es **Full HTML** (sin filtros) |

## Previsualización

https://ramirez-santigosa.github.io/ryc-web/
