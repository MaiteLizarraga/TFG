---
type: procedure
area: journaling-version-control
project: TFG Odoo Agentic AI
status: implemented
tags:
  - tfg
  - git
---

# Configuración local de Git para el journaling

## Entorno e identidad

Se comprobó que Git estaba instalado (`git version 2.53.0`) y que la identidad global configurada para los commits era:

- Nombre: `Maite Lizarraga`
- Email: `maite.lizarraga@gmail.com`

El repositorio local se encuentra en `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`, dentro de Ubuntu (`ubuntu-tfg`). La rama principal es `main` y el remoto `origin` apunta a `git@github.com:MaiteLizarraga/TFG.git`.

## `.gitignore` en la raíz del vault

Configuración documentada:

```gitignore
.obsidian/
Welcome.md

# Contenido administrativo privado
/Admin/
```

- `.obsidian/`: excluye la configuración interna de Obsidian.
- `Welcome.md`: excluye la nota de bienvenida generada por Obsidian.
- `/Admin/`: excluye la carpeta administrativa situada en la raíz del vault. La barra inicial limita la regla a esa ubicación.

La exclusión de `Admin/` evita que su contenido se añada al repositorio en futuras operaciones normales de `git add -A`. Si un archivo ya estuviera versionado, añadirlo a `.gitignore` no lo eliminaría automáticamente del seguimiento; habría que comprobarlo con `git ls-files Admin/`.

## Inicialización y primer commit

Desde la raíz del vault se ejecutaron inicialmente:

```bash
git init
git branch -M main
git add .
git commit -m "added Obsidian Journaling"
```

El commit inicial registrado fue `0ae1d81` (`added Obsidian Journaling`). La autenticación SSH y la publicación en GitHub se documentan en [[Autenticación SSH con GitHub]] y [[GitHub como repositorio de seguimiento del TFG]].

## Flujo de trabajo para registrar cambios

Desde la raíz del repositorio:

```bash
git status
git check-ignore -v Admin/archivo.md
git add -A
git status
git diff --cached --stat
git diff --cached
```

Revisar el estado y el contenido preparado antes de confirmar el commit. La comprobación de `git check-ignore` debe apuntar a un archivo real dentro de `Admin/`; no debe añadirse contenido administrativo al área de preparación.

Si el área preparada es correcta:

```bash
git commit -m "Describe the change"
git push origin main
git status
```

- `git add`: prepara cambios para el próximo commit.
- `git commit`: guarda una versión en el historial local.
- `git push`: publica los commits locales en GitHub.
- `git status`: permite comprobar si quedan cambios pendientes.

## Seguridad

No añadir credenciales, tokens ni claves privadas al repositorio. Como `__WIP_to_journal/` también se sincroniza con GitHub, debe tratarse como contenido remoto compartido con quienes tengan acceso al repositorio privado, no como un espacio exclusivamente local.

Relacionado: [[Estructura del repositorio de journaling]] y [[GitHub como repositorio de seguimiento del TFG]].
