---
type: moc
area: odoo
project: TFG Odoo Agentic AI
status: active
tags:
  - documentacion/moc
  - obsidian/moc
  - odoo/api
  - odoo/modelos
---

# MOC — Odoo API y modelos

## Conceptos fundamentales

- [[API JSON-2 de Odoo]]
- [[ORM de Odoo y PostgreSQL]]
- [[Modelos de compras - purchase.order]]
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
- [[Carga de datos dummy]]
- [[Instalación de los módulos funcionales]]

## Regla de diseño

Los agentes acceden a Odoo mediante herramientas semánticas MCP y la API; no consultan ni modifican directamente PostgreSQL.
