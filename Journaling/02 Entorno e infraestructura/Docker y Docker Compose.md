---
type: concepto
area: infraestructura
status: active
project: TFG Odoo Agentic AI
tags:
  - infraestructura/docker
---

# Docker y Docker Compose

## Versiones documentadas

- Docker Engine: 29.8.1
- Docker CLI: 29.8.1
- containerd.io: 2.3.6
- Docker Buildx: 0.37.1
- Docker Compose plugin: 5.5.1
- Git: 2.53.0

La prueba inicial `docker run hello-world` funcionó correctamente.

## Contenedores principales

- `odoo-tfg`
- `odoo-tfg-db`

## Persistencia

- `./data/odoo` → `/var/lib/odoo`
- `./data/postgres` → `/var/lib/postgresql/data`
- `./config` → `/etc/odoo`

## Puertos publicados documentados

- Odoo: `8069:8069`
- PostgreSQL: `5432:5432`

> [!warning] Seguridad
> El texto de origen indica que PostgreSQL está publicado en todas las interfaces (`0.0.0.0` y `[::]`). Para un entorno local, revisa si es necesario exponerlo así. Si DBeaver se ejecuta en la misma VM, normalmente puede bastar con publicar el puerto en `127.0.0.1`. No cambies la configuración sin comprobar antes el estado real del entorno.

## Enlaces

- [[Configuración Docker Compose de Odoo]]
- [[PostgreSQL y DBeaver]]
- [[Registro de problemas técnicos]]
