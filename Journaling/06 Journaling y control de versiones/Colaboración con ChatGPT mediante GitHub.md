---
type: process
area: journaling-version-control
project: TFG Odoo Agentic AI
status: active
created: 2026-10-28
tags:
  - tfg
  - github
  - obsidian/workflow
---

# Colaboración con ChatGPT mediante GitHub

## Acceso al repositorio

El repositorio privado [`MaiteLizarraga/TFG`](https://github.com/MaiteLizarraga/TFG) está conectado a ChatGPT y se ha comprobado que la conexión dispone de permisos de escritura en la rama `main`.

Esto permite trabajar directamente sobre los archivos del repositorio, sin tener que intercambiar ZIP para cada cambio.

## Forma de trabajo acordada

- **Crear notas:** ChatGPT puede crear notas nuevas directamente en GitHub cuando formen parte de una tarea solicitada.
- **Modificar notas:** antes de editar un archivo existente, debe consultar su contenido y respetar la estructura y las decisiones documentadas.
- **Commits:** puede guardar los cambios autorizados mediante commits en GitHub, agrupando los cambios relacionados cuando tenga sentido.
- **Cambios delicados:** debe pedir confirmación antes de borrar archivos, reorganizar el vault o cambiar decisiones importantes ya documentadas.
- **Límites de autorización:** el acceso al repositorio no autoriza a realizar cambios por iniciativa propia fuera de las tareas encargadas por la usuaria.

## Sincronización con Obsidian

Los cambios realizados directamente en GitHub **no se reflejan automáticamente en el vault local**.

Para traerlos a Ubuntu, ejecutar desde la carpeta del vault:

```bash
git pull origin main
```

Antes de hacer el `pull`, conviene comprobar que no haya cambios locales sin guardar o conflictos pendientes. Si existen cambios locales, deben revisarse antes de sincronizar para evitar perder trabajo.

## Principio de trabajo

La usuaria define las tareas y el alcance. ChatGPT se encarga de ejecutar los cambios autorizados con cuidado, comprobar el contexto de los archivos afectados y comunicar qué ha creado o modificado y qué commit se ha generado.
