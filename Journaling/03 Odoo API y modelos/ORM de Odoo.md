---
type: concepto
area: odoo
project: TFG Odoo Agentic AI
tags:
  - odoo/orm
---

# ORM de Odoo

**ORM** significa *Object-Relational Mapping*, o mapeo objeto-relacional.

Odoo trabaja con modelos de negocio, por ejemplo:

- `purchase.order`
- `purchase.order.line`
- `res.partner`
- `product.product`
- `stock.quant`
- `stock.picking`
- `mrp.production`
- `sale.order`

El ORM gestiona, entre otras funciones:

- Persistencia y relaciones entre modelos.
- Validaciones y lógica de negocio.
- Permisos, ACL y record rules.
- Campos calculados y herencia de modelos.
- Operaciones como `create`, `write` y `unlink`.

## Distinción importante

La API está alineada con los modelos y métodos de Odoo, pero no expone objetos ORM directamente. Véase [[Separación entre API, ORM y PostgreSQL]].

## Enlaces

- [[API JSON-2 de Odoo]]
- [[Exploración de purchase.order]]
