---
type: concepto
area: integracion
status: planned
project: TFG Odoo Agentic AI
tags:
  - integracion/mcp
  - integracion/permisos
  - arquitectura/human-in-the-loop
---

# MCP como capa semántica y controlada

## Decisión de diseño

MCP actuará como una capa controlada entre los agentes y la API JSON-2 de Odoo.

La intención es ofrecer herramientas de negocio semánticas, en lugar de permitir que el LLM construya consultas arbitrarias sobre los modelos de Odoo.

## Ejemplos de herramientas previstas

- `get_purchase_order()`
- `get_purchase_order_lines()`
- `get_supplier()`
- `get_stock()`
- `get_incoming_shipments()`
- `get_manufacturing_orders()`
- `get_sales_commitments()`

## Flujo de acceso

```text
Agente
  ↓
Herramienta MCP
  ↓
Odoo JSON-2 API
  ↓
Odoo ORM
  ↓
PostgreSQL
```

## Enlaces

- [[Decisiones arquitectónicas del sistema]]
- [[Separación entre API, ORM y PostgreSQL]]
- [[Herramientas MCP previstas]]
