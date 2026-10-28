---
type: exploration
status: in-progress
project: TFG Odoo Agentic AI
tags:
  - odoo
  - purchase
  - data-model
---

# Exploración de `purchase.order`

## Identificación del modelo

- Descripción: `Purchase Order`
- Modelo: `purchase.order`
- Tipo: `Base Object`

Se inspeccionó el modelo mediante el modo desarrollador de Odoo.

## Campos observados

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

## Relación con el proyecto

La exploración ayuda a comprender los modelos del ORM y a diseñar posteriormente herramientas semánticas de lectura para compras.

## Enlaces

- [[ORM de Odoo]]
- [[Relación entre pedido de compra y líneas]]
- [[API JSON-2 de Odoo]]
