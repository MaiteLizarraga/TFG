---
type: concepto
area: odoo
project: TFG Odoo Agentic AI
status: understood
tags:
  - odoo/api
  - odoo/orm
  - infraestructura/postgresql
---

# ORM de Odoo y PostgreSQL

## ORM de Odoo

**ORM** significa *Object-Relational Mapping*, o mapeo objeto-relacional.

Odoo trabaja con modelos de negocio, por ejemplo:

- `purchase.order`
- `purchase.order.line`
- `res.partner`
- `product.product`
- `stock.quant`
- `stock.picking`
- `stock.move`
- `mrp.production`
- `sale.order`

El ORM gestiona, entre otras funciones:

- Persistencia y relaciones entre modelos.
- Validaciones y lógica de negocio.
- Permisos, ACL y record rules.
- Campos calculados y herencia de modelos.
- Operaciones como `create`, `write` y `unlink`.

## Separación entre API, ORM y PostgreSQL

**La API no devuelve el ORM.** La API es la interfaz externa para solicitar operaciones a Odoo; el ORM permanece dentro de Odoo.

### Flujo de lectura

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

### Responsabilidades

- **API:** interfaz de acceso externo.
- **ORM:** gestiona modelos, relaciones, persistencia, validaciones, permisos, reglas de acceso y lógica de negocio.
- **PostgreSQL:** almacena los datos persistentes.

## Implicación para el TFG

Los agentes no deben acceder directamente a PostgreSQL. El acceso a través de Odoo conserva las validaciones, los permisos y los comportamientos de negocio definidos por el ERP.

La inspección directa de PostgreSQL puede utilizarse para analizar el entorno, pero no constituye el mecanismo de acceso de los agentes. En la arquitectura del TFG, los agentes acceden a Odoo mediante herramientas semánticas MCP y la API, sin consultar ni modificar directamente la base de datos.

## Enlaces

- [[API JSON-2 de Odoo]]
- [[Modelos de compras - purchase.order]]
- [[MCP como capa semántica y controlada]]
- [[Decisiones arquitectónicas del sistema]]
