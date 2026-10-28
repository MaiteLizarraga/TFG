---
type: architecture
status: planned
project: TFG Odoo Agentic AI
tags:
  - tfg
  - agentic-ai
  - architecture
---

# Arquitectura objetivo del sistema agentic

## Flujo propuesto

```text
HUMAN
  ↓
ODOO
  ↓
Automation Rule
  ↓
Webhook
  ↓
FastAPI / LangGraph
  ↓
Orchestrator
  ├── Purchase Agent
  ├── Inventory Agent
  ├── Manufacturing Agent
  └── Sales Agent
  ↓
MCP
  ↓
Odoo JSON-2 API
  ↓
Odoo ORM
  ↓
PostgreSQL
```

## Componentes

- **Odoo:** sistema de información empresarial y responsable de la lógica de negocio.
- **Automation Rule / Webhook:** mecanismo previsto para iniciar el flujo ante determinados eventos.
- **FastAPI / LangGraph:** capa de integración y orquestación prevista.
- **Orchestrator:** coordina el trabajo de los agentes.
- **Agentes especializados:** analizan información de las áreas funcionales correspondientes.
- **MCP:** expone herramientas semánticas controladas.
- **JSON-2 API:** interfaz externa de acceso a Odoo.
- **ORM:** capa interna de Odoo que interactúa con la base de datos.
- **PostgreSQL:** persistencia de Odoo.

## Estado

Esta es la arquitectura objetivo. El entorno Odoo/API está probado; la orquestación y los agentes forman parte de fases posteriores.

## Enlaces

- [[Decisiones arquitectónicas del sistema]]
- [[Separación entre API, ORM y PostgreSQL]]
- [[MCP como capa semántica y controlada]]
- [[Roadmap de integración]]
