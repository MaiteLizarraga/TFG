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

El Vault de Obsidian utilizado para el journaling del TFG está conectado a un repositorio privado de GitHub. El objetivo no es únicamente disponer de una copia de seguridad: GitHub permite al tutor consultar la evolución del trabajo, revisar cambios y acceder al historial de versiones.

## Entorno

- Vault de Obsidian: `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`
- Repositorio remoto: `MaiteLizarraga/TFG`
- Visibilidad: privado
- Sistema: Ubuntu (`ubuntu-tfg`)
- Git: `2.53.0`
- Rama principal: `main`

## Flujo de versionado

```text
Modificar el journaling en Obsidian
              ↓
        Git detecta cambios
              ↓
            commit
              ↓
             push
              ↓
        GitHub actualizado
              ↓
      Tutor puede revisar
       la evolución del TFG
```

El flujo de `commit` y `push` está configurado manualmente. La automatización con el complemento [[Automatización con Obsidian Git]] queda como siguiente paso.

## Notas relacionadas

- [[Configuración local de Git para el journaling]]
- [[Autenticación SSH con GitHub]]
- [[Estructura del repositorio de journaling]]
