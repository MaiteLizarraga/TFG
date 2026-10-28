---
type: moc
area: architecture
project: TFG Odoo Agentic AI
tags:
  - tfg
  - obsidian/moc
---

# MOC — Proyecto y arquitectura

## Alcance y decisiones

- [[Contexto y alcance del TFG]]
- [[Decisiones arquitectónicas del sistema]]
- [[Arquitectura objetivo del sistema agentic]]
- [[Odoo 19 Community como ERP del proyecto]]

## Principios de diseño

- [[Separación entre API, ORM y PostgreSQL]]
- [[MCP como capa semántica y controlada]]
- [[Human-in-the-loop y rol del FDE]]
- [[Observabilidad del sistema agentic]]

## Flujo general

```text
Usuario / evento en Odoo
        ↓
Regla de automatización / webhook
        ↓
FastAPI / LangGraph
        ↓
Orchestrator
        ↓
Agentes especializados
        ↓
Herramientas semánticas MCP
        ↓
Odoo JSON-2 API → ORM → PostgreSQL
```

## Agentes previstos

- [[Purchase Agent]]
- [[Inventory Agent]]
- [[Manufacturing Agent]]
- [[Sales Agent]]

> [!note] Estado
> La arquitectura anterior es el diseño objetivo documentado. No implica que todos sus componentes estén implementados.
