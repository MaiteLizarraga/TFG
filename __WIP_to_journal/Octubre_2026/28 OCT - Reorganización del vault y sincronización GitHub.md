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
- Se verificó la conexión de ChatGPT con el repositorio privado `MaiteLizarraga/TFG` y sus permisos de escritura en la rama `main`.
- Se acordó que ChatGPT podrá crear y modificar archivos directamente en GitHub como parte de las tareas encargadas, consultando antes las notas existentes.
- Se estableció que los cambios importantes —como borrar archivos, reorganizar el vault o alterar decisiones documentadas— requieren confirmación previa.
- Se creó la nota [[Colaboración con ChatGPT mediante GitHub]] en `Journaling/06 Journaling y control de versiones/` para documentar este flujo de trabajo.
- Se acordó registrar cada jornada de trabajo en dos niveles: documentar el conocimiento o procedimiento duradero en `Journaling/` y añadir el registro de actividad a la nota del día en `__WIP_to_journal/`. Todos los cambios de una misma fecha se acumulan bajo esa fecha, sin crear una nota diaria nueva por cada tarea.

## Flujo de trabajo acordado

1. La usuaria define la tarea y su alcance.
2. ChatGPT consulta el contenido existente antes de modificar archivos y realiza los cambios autorizados directamente en GitHub.
3. El conocimiento estable o los procedimientos se documentan en la sección temática correspondiente de `Journaling/`.
4. La actividad realizada se añade a la nota del día correspondiente en `__WIP_to_journal/`; se reutiliza la nota de la fecha actual para agrupar las tareas del día.
5. ChatGPT comunica qué archivos ha creado o modificado y el commit generado.
6. Para sincronizar los cambios con el vault local, ejecutar desde la raíz del repositorio:

```bash
git pull origin main
```

Antes de hacer el `pull`, conviene comprobar que no haya cambios locales sin guardar o conflictos pendientes. Si existen cambios locales, deben revisarse antes de sincronizar para evitar perder trabajo.

## Procedimiento de publicación manual

Si se trabaja desde el entorno local, desde la raíz del repositorio:

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

- Continuar registrando el trabajo diario en `__WIP_to_journal/`, agrupando todas las tareas del día bajo la fecha correspondiente.
- Documentar en `Journaling/` el conocimiento duradero, los procedimientos y los acuerdos de trabajo.
- Procesar periódicamente las notas provisionales y trasladar el conocimiento duradero a las notas temáticas de `Journaling/`.
- Mantener `Admin/` excluido y no guardar secretos, credenciales ni claves privadas en el repositorio.

## Nota de estado

El commit y el push mencionados al inicio de esta nota ya se habían completado antes de redactarla. Los cambios posteriores descritos aquí se han registrado directamente en GitHub mediante commits. La sincronización del vault local se realiza aparte mediante `git pull origin main`.
