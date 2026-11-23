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

- `res.partner`
- `product.template`
- `product.product`
- `uom.uom`
- `purchase.order` y `purchase.order.line`
- `sale.order` y `sale.order.line`
- `mrp.bom` y `mrp.bom.line`
- `mrp.production`
- `stock.picking`
- `stock.move`
- `stock.quant`
- `stock.lot`

## Datos de prueba y generación

- [[Estrategia de datos de prueba]] — escenario sintético de fabricante y distribuidora de sushi, productos, BoM, trazabilidad por lotes, caducidades y cinco experimentos.
- [[Carga de datos dummy]]

## Pruebas realizadas

- [[Primera consulta a la API JSON-2]]
- [[Carga de datos dummy]]
- [[Instalación de los módulos funcionales]]

## Reglas de diseño

- Los agentes acceden a Odoo mediante herramientas semánticas MCP y la API; no consultan ni modifican directamente PostgreSQL.
- Los datos sintéticos se crean mediante la API JSON-2/ORM y los flujos estándar de Odoo.
- Los lotes y las caducidades forman parte del escenario de inventario y fabricación.
- No se presume una vinculación automática entre pedidos de venta y órdenes de fabricación: se verifican rutas y reglas; si no existe, la correspondencia se conserva en el manifiesto.
