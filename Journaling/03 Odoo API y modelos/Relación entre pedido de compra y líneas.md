---
type: concept
project: TFG Odoo Agentic AI
tags:
  - odoo
  - data-model
  - purchase
---

# Relación entre pedido de compra y líneas

Las líneas de un pedido de compra se representan en el modelo `purchase.order.line`, no como registros independientes dentro de `purchase.order`.

## Relación conceptual

```text
purchase.order
      │
      │ order_id
      ▼
purchase.order.line
      │
      │ product_id
      ▼
product.product
```

Para consultar las líneas del pedido `P00011` (ID `11`) se preparó una consulta a:

```text
purchase.order.line/search_read
```

con el dominio:

```json
[
  ["order_id", "=", 11]
]
```

Campos previstos en la consulta:

- `id`
- `order_id`
- `product_id`
- `name`
- `product_qty`
- `price_unit`
- `price_subtotal`
- `price_total`

Esto permite obtener el producto, la descripción, la cantidad, el precio unitario, el subtotal y el total.

> [!note] Estado
> El texto de origen documenta que se preparó la consulta; no confirma aquí el resultado de su ejecución.

## Enlaces

- [[ORM de Odoo]]
- [[API JSON-2 de Odoo]]
- [[Exploración de purchase.order]]
