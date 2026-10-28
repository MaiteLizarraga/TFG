---
type: project
status: active
project: TFG Odoo Agentic AI
tags:
  - tfg
  - supply-chain
  - agentic-ai
---

# Contexto y alcance del TFG

## Objetivo

Desarrollar un sistema de **Agentic AI para la gestión de incidencias de Supply Chain**, utilizando un ERP realista como sistema de información empresarial.

## ERP seleccionado

Se ha elegido [[Odoo 19 Community como ERP del proyecto]].

El sistema agentic complementará al ERP: no lo sustituirá ni accederá directamente a su base de datos.

## Módulos funcionales incluidos

| Área | Módulo técnico |
|---|---|
| Ventas | `sale_management` |
| Compras | `purchase` |
| Inventario | `stock` |
| Fabricación | `mrp` |

Otros módulos pueden instalarse como dependencias técnicas, pero no se consideran áreas funcionales adicionales del proyecto.

## Fuera de alcance según las decisiones actuales

- Software Engineer Agent.
- QA Agent.
- Acceso directo de los agentes a PostgreSQL.
- Módulos Python ad hoc dentro de Odoo para resolver la integración.

## Enlaces relacionados

- [[Decisiones arquitectónicas del sistema]]
- [[Arquitectura objetivo del sistema agentic]]
- [[Roadmap de integración]]
