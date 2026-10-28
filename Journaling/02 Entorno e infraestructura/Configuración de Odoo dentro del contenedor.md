---
type: procedimiento
area: infraestructura
status: resolved
project: TFG Odoo Agentic AI
tags:
  - infraestructura/docker
  - documentacion/procedimiento
---

# Configuración de Odoo dentro del contenedor

## Problema

El montaje `./config:/etc/odoo` ocultaba la configuración original de la imagen de Odoo y el servidor no arrancaba correctamente.

## Solución aplicada

Se creó el archivo `~/odoo-tfg/config/odoo.conf`:

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
```

Con esta configuración, Odoo pudo localizar los addons y su directorio de datos.

## Lección técnica

Un bind mount de Docker sobre un directorio del contenedor oculta el contenido preexistente de ese directorio, aunque no lo borra de la imagen.

## Relacionado

- [[Configuración Docker Compose de Odoo]]
- [[Registro de problemas técnicos]]
