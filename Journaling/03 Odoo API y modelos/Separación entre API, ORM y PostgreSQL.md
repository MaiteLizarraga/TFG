---
type: concepto
area: odoo
status: understood
project: TFG Odoo Agentic AI
tags:
  - odoo/api
  - odoo/orm
  - infraestructura/postgresql
---

# Separación entre API, ORM y PostgreSQL

## Idea clave

**La API no devuelve el ORM.** La API es la interfaz externa para solicitar operaciones a Odoo; el ORM permanece dentro de Odoo.

## Flujo de lectura

```text
Agente
  ↓
Odoo JSON-2 API
  ↓
Método del modelo Odoo
  ↓
ORM
  ↓
PostgreSQL
  ↓
ORM
  ↓
API
  ↓
JSON
  ↓
Agente
```

La API devuelve datos serializados —normalmente JSON—, no objetos ORM directamente.

## Responsabilidades

- **API:** interfaz de acceso externo.
- **ORM:** gestiona modelos, relaciones, persistencia, validaciones, permisos, reglas de acceso y lógica de negocio.
- **PostgreSQL:** almacena los datos persistentes.

## Implicación para el TFG

Los agentes no deben acceder directamente a PostgreSQL. El acceso a través de Odoo conserva las validaciones, los permisos y los comportamientos de negocio definidos por el ERP.

## Enlaces

- [[ORM de Odoo]]
- [[API JSON-2 de Odoo]]
- [[MCP como capa semántica y controlada]]
- [[Decisiones arquitectónicas del sistema]]
