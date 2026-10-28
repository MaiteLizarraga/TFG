---
type: concept
area: journaling-version-control
project: TFG Odoo Agentic AI
status: implemented
tags:
  - tfg
  - git
  - github
---

# GitHub como repositorio de seguimiento del TFG

## Objetivo

El vault de Obsidian utilizado para el journaling del TFG está conectado a un repositorio privado de GitHub. Además de servir como copia remota, permite revisar la evolución del trabajo y consultar el historial de versiones.

## Entorno

- Vault local: `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`
- Repositorio remoto: `MaiteLizarraga/TFG` (privado)
- Remoto Git: `origin` → `git@github.com:MaiteLizarraga/TFG.git`
- Sistema: Ubuntu (`ubuntu-tfg`)
- Git: `2.53.0`
- Rama principal: `main`
- Autenticación: SSH, verificada con `ssh -T git@github.com`

## Qué se sincroniza

- `Journaling/`: notas consolidadas y estructuradas, incluida la sección `06 Journaling y control de versiones`.
- `__WIP_to_journal/`: notas provisionales y material de origen que también se mantienen en el repositorio.
- `Admin/`: excluido del repositorio mediante la regla `/Admin/` de `.gitignore`.
- `.obsidian/` y `Welcome.md`: excluidos según `.gitignore`.

El repositorio es privado, pero eso no convierte los archivos sincronizados en contenido exclusivamente local. No deben incluirse secretos, claves privadas, credenciales ni información que no se quiera compartir con las personas que tengan acceso al repositorio.

## Flujo de versionado

```text
Editar o crear notas en Obsidian
              ↓
          git status
              ↓
     git add -A (preparar)
              ↓
  revisar git diff --cached
              ↓
           git commit
              ↓
       git push origin main
              ↓
        GitHub actualizado
```

Antes de preparar los cambios, comprobar las exclusiones y el contenido pendiente. Tras el `commit` y el `push` realizados el 28 de octubre de 2026, la nueva estructura quedó publicada. Las actualizaciones posteriores de estas notas requerirán su propio commit y push.

## Automatización

El flujo actual se realiza manualmente. La automatización mediante el complemento [[Automatización con Obsidian Git]] sigue siendo una tarea pendiente; no debe considerarse activa hasta instalarla, configurarla y probarla.

## Notas relacionadas

- [[Configuración local de Git para el journaling]]
- [[Autenticación SSH con GitHub]]
- [[Estructura del repositorio de journaling]]
