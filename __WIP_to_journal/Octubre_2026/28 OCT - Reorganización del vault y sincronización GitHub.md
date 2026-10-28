---
type: journal
project: TFG Odoo Agentic AI
date: 2026-10-28
status: provisional
tags:
  - tfg
  - journaling
  - obsidian
  - git
  - github
---

# 28 OCT — Reorganización del vault y sincronización con GitHub

## Trabajo realizado

- Se consolidó la organización del vault en una única estructura, con el contenido de conocimiento bajo `Journaling/`.
- Se mantuvo `__WIP_to_journal/` como zona de trabajo provisional para las notas diarias y el material pendiente de procesar.
- Se decidió que `__WIP_to_journal/` también se sincroniza con el repositorio privado de GitHub; por tanto, no es una carpeta exclusivamente local.
- Se añadió a `.gitignore` la regla `/Admin/` para excluir el contenido administrativo situado en la raíz del vault. Se mantienen también las exclusiones de `.obsidian/` y `Welcome.md`.
- Se revisó el flujo manual de control de versiones y se completó un `commit` y un `push` a la rama `main`.
- Se identificó la necesidad de reflejar la estructura actual y el procedimiento de publicación en `Journaling/06 Journaling y control de versiones/`.

## Procedimiento de publicación

Desde la raíz del repositorio:

```bash
git status
git add -A
git status
git diff --cached --stat
git diff --cached
```

Revisar que `Admin/` no aparezca entre los archivos preparados y que el resto de los cambios sea el esperado. Después:

```bash
git commit -m "Describe the change"
git push origin main
git status
```

`git add` prepara los cambios, `git commit` los registra en el historial local y `git push` los publica en GitHub.

## Próximos pasos

- Incorporar esta nota y las actualizaciones de la sección 06 al siguiente commit y push.
- Continuar registrando el trabajo diario en `__WIP_to_journal/`.
- Procesar periódicamente las notas provisionales y trasladar el conocimiento duradero a las notas temáticas de `Journaling/`.
- Mantener `Admin/` excluido y no guardar secretos, credenciales ni claves privadas en el repositorio.

## Nota de estado

El commit y el push mencionados arriba ya se habían completado antes de redactar esta nota. La incorporación de este nuevo registro y de las notas actualizadas constituye un cambio posterior y debe publicarse en un nuevo commit.