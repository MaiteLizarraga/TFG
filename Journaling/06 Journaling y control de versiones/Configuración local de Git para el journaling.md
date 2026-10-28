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

## Comprobación de Git e identidad

Se comprobó que Git estaba instalado:

```bash
git --version
```

Resultado registrado: `git version 2.53.0`.

La identidad global configurada para los commits era:

- Nombre: `Maite Lizarraga`
- Email: `maite.lizarraga@gmail.com`

## Archivos excluidos

En la raíz del Vault se creó `.gitignore` con:

```gitignore
.obsidian/
Welcome.md
```

- `.obsidian/`: configuración interna de Obsidian, excluida del repositorio.
- `Welcome.md`: nota de bienvenida generada por Obsidian, excluida por no ser relevante para el journaling.

La comprobación mediante `git status` mostró únicamente `.gitignore` y `Septiembre_2026/` como contenido pendiente, lo que confirmó que las exclusiones funcionaban.

## Inicialización y primer commit

Desde la raíz del Vault:

```bash
git init
git branch -M main
git add .
git commit -m "added Obsidian Journaling"
```

El commit inicial registrado fue `0ae1d81` (`added Obsidian Journaling`). Incluyó `.gitignore` y `Septiembre_2026/Reto 1 - 27, 28 y 29 septiembre 2026.md`.

## Repositorio remoto y publicación

El remoto se configuró con:

```bash
git remote add origin git@github.com:MaiteLizarraga/TFG.git
git push -u origin main
```

La autenticación SSH necesaria para completar el `push` se documenta en [[Autenticación SSH con GitHub]].

## Nota de seguridad

No añadir credenciales, tokens ni claves privadas al repositorio. Revisar el contenido de `git status` antes de hacer `git add` y publicar cambios.
