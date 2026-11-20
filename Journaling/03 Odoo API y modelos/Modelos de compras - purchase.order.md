---
type: referencia
area: odoo
status: in-progress
project: TFG Odoo Agentic AI
tags:
  - odoo/modelos
  - odoo/modulos
  - datos/modelo-relacional
---

# Modelos de compras - purchase.order

## Identificación del modelo

- Descripción: `Purchase Order`
- Modelo: `purchase.order`
- Tipo: `Base Object`

Se inspeccionó el modelo mediante el modo desarrollador de Odoo.

## Campos observados en purchase.order

Entre los campos revisados se encuentran:

- `amount_tax`
- `amount_total`
- `amount_untaxed`
- `company_id`
- `currency_id`
- `date_approve`
- `date_order`
- `date_planned`
- `dest_address_id`
- `effective_date`
- `incoming_picking_count`
- `incoterm_id`
- `partner_id`

También se inspeccionaron propiedades de campos como nombre, etiqueta, tipo, ayuda, requerido, solo lectura, almacenado, indexado, copiado, modelo relacionado, comportamiento al borrar y dominio.

## Relación entre pedido de compra y líneas

Las líneas de un pedido de compra se representan en el modelo `purchase.order.line`, no como registros independientes dentro de `purchase.order`.

### Relación conceptual

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

Para consultar las líneas del pedido `P00011` (ID `11`) se preparó una consulta a `purchase.order.line/search_read`, con el dominio:

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

## Relación con el proyecto

La exploración ayuda a comprender los modelos del ORM y a diseñar posteriormente herramientas semánticas de lectura para compras. La relación entre el pedido, sus líneas y los productos es también relevante para preparar datos de prueba coherentes.

## Enlaces

- [[ORM de Odoo y PostgreSQL]]
- [[API JSON-2 de Odoo]]
- [[Primera consulta a la API JSON-2]]
- [[Dependencias de módulos Odoo y datos de negocio]]
