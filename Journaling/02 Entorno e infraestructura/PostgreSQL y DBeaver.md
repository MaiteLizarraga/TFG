---
type: referencia
area: infraestructura
status: active
project: TFG Odoo Agentic AI
tags:
  - infraestructura/postgresql
  - datos/modelo-relacional
---

# PostgreSQL y DBeaver

## PostgreSQL

- Versión: PostgreSQL 17.
- Contenedor: `odoo-tfg-db`.
- Base de datos de trabajo: `Odoo-tfg`.
- Puerto publicado: `5432`.

## DBeaver

- Edición: DBeaver Community.
- Versión documentada: 26.2.1.
- Instalación: Snap con confinamiento clásico.
- Conexión comprobada a `localhost:5432`, base de datos `Odoo-tfg`.

## Propósito de DBeaver

Se utiliza para inspeccionar la estructura física de la base de datos, explorar tablas, observar relaciones y entender cómo se materializan los modelos del ORM.

**No es la vía de acceso de los agentes.** Los agentes utilizarán MCP y la API JSON-2 de Odoo.

## Consideración de seguridad

El origen documenta que PostgreSQL está publicado en todas las interfaces. Revisa si basta con `127.0.0.1:5432` para el uso local de DBeaver.

## Enlaces

- [[Separación entre API, ORM y PostgreSQL]]
- [[Configuración Docker Compose de Odoo]]
- [[Roadmap de integración]]
