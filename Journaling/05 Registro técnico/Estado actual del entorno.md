---
type: referencia
area: infraestructura
project: TFG Odoo Agentic AI
status: operational-as-documented
last_reviewed: 2026-09
tags:
  - infraestructura/ubuntu
  - infraestructura/docker
  - infraestructura/postgresql
---

# Estado actual del entorno

> [!info] Fecha de referencia
> El documento de origen registra el estado en septiembre de 2026. Verifica el estado real si ha habido cambios desde entonces.

## Componentes

| Componente | Estado documentado |
|---|---|
| Odoo | Odoo 19 Community operativo |
| PostgreSQL | PostgreSQL 17 operativo |
| Docker Compose | Operativo |
| Base de datos | `Odoo-tfg` |
| Módulos funcionales | `sale_management`, `purchase`, `stock`, `mrp` instalados |
| API JSON-2 | Primera consulta ejecutada correctamente |
| DBeaver | Instalado y conectado a PostgreSQL |

## Rutas y endpoints

- Proyecto: `/home/maite/odoo-tfg`
- Odoo: `http://localhost:8069`
- PostgreSQL: `localhost:5432`

## Próximo hito

Pasar de la instalación y exploración a la construcción de la integración.

## Enlaces

- [[Entorno Ubuntu-TFG]]
- [[Docker y Docker Compose]]
- [[API JSON-2 de Odoo]]
- [[Roadmap de integración]]
