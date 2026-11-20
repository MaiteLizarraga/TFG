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

Los agentes no accederán directamente a PostgreSQL. Las herramientas MCP encapsularán las operaciones permitidas y expondrán una interfaz orientada al dominio de negocio.

## Herramientas previstas

Las siguientes herramientas forman parte del diseño inicial. Su documentación no implica que estén implementadas:

| Herramienta | Propósito previsto |
|---|---|
| `get_purchase_order()` | Recuperar información de un pedido de compra |
| `get_purchase_order_lines()` | Consultar las líneas de un pedido |
| `get_supplier()` | Consultar información de proveedor |
| `get_stock()` | Consultar disponibilidad o datos de stock |
| `get_incoming_shipments()` | Consultar recepciones entrantes |
| `get_manufacturing_orders()` | Consultar órdenes de fabricación |
| `get_sales_commitments()` | Consultar compromisos de venta |

## Criterios de diseño pendientes

- Esquema de entrada y salida.
- Validación de parámetros.
- Autorización y permisos.
- Manejo de errores.
- Límites de resultados.
- Trazabilidad y correlación con la incidencia.
- Diferenciación entre herramientas de lectura y de escritura.

## Enlaces

- [[Decisiones arquitectónicas del sistema]]
- [[API JSON-2 de Odoo]]
- [[ORM de Odoo y PostgreSQL]]
- [[Agentes especializados]]
- [[Roadmap de integración]]
