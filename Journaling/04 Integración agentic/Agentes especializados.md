---
type: referencia
area: integracion
status: planned
project: TFG Odoo Agentic AI
tags:
  - arquitectura/multiagente
  - odoo/modulos
---

# Agentes especializados

La arquitectura contempla cuatro agentes especializados, coordinados por el orquestador. Sus fichas describen responsabilidades previstas y no implican que los agentes estén implementados.

## Purchase Agent

Agente especializado en Compras.

- Consultará información de pedidos de compra, líneas y proveedores.
- Utilizará herramientas semánticas MCP para acceder a Odoo.
- Su alcance funcional se corresponde con el módulo de Compras.

## Inventory Agent

Agente especializado en Inventario.

- Consultará información de existencias y disponibilidad.
- Podrá consultar recepciones y movimientos de inventario mediante herramientas MCP.
- Su alcance funcional se corresponde con el módulo de Inventario.

## Manufacturing Agent

Agente especializado en Fabricación.

- Consultará órdenes de fabricación y la información relacionada.
- Utilizará herramientas MCP controladas para acceder a los datos de Odoo.
- Su alcance funcional se corresponde con el módulo de Fabricación (MRP).

## Sales Agent

Agente especializado en Ventas.

- Consultará pedidos de venta y compromisos comerciales.
- Utilizará herramientas MCP controladas para acceder a los datos de Odoo.
- Su alcance funcional se corresponde con el módulo de Ventas.

## Criterios comunes

- Los agentes no acceden directamente a PostgreSQL.
- El acceso a Odoo se realiza a través de herramientas MCP y la API JSON-2.
- Cada agente se limita a su dominio funcional y devuelve información al orquestador.
- Las herramientas disponibles, sus contratos y permisos se definen en [[MCP como capa semántica y controlada]].

## Estado

Los cuatro agentes están previstos en el diseño de la arquitectura. La implementación y validación de cada uno quedan pendientes y deberán reflejarse aquí cuando se realicen.

## Enlaces

- [[Decisiones arquitectónicas del sistema]]
- [[MCP como capa semántica y controlada]]
- [[Human-in-the-loop y rol del FDE]]
- [[Roadmap de integración]]
