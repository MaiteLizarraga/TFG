---
type: moc
area: odoo
project: TFG Odoo Agentic AI
tags:
  - odoo
  - obsidian/moc
---

# MOC — Odoo API y modelos

## Conceptos fundamentales

- [[Separación entre API, ORM y PostgreSQL]]
- [[ORM de Odoo]]
- [[API JSON-2 de Odoo]]
- [[Autenticación mediante API Key]]
- [[Relación entre pedido de compra y líneas]]
- [[Dependencias de módulos Odoo y datos de negocio]]

## Modelos de interés

- `purchase.order`
- `purchase.order.line`
- `res.partner`
- `product.product`
- `stock.quant`
- `stock.picking`
- `stock.move`
- `mrp.production`
- `sale.order`

## Pruebas realizadas

- [[Primera consulta a la API JSON-2]]
- [[Carga de datos de demostración]]
- [[Exploración de purchase.order]]

## Regla de diseño

Los agentes acceden a Odoo mediante herramientas semánticas MCP y la API; no consultan ni modifican directamente PostgreSQL.
