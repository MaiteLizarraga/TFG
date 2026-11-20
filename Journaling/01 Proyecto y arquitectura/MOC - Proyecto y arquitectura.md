---
type: moc
area: arquitectura
project: TFG Odoo Agentic AI
tags:
  - documentacion/moc
  - obsidian/moc
---

# MOC — Proyecto y arquitectura

Este índice reúne la documentación principal del contexto, las decisiones de diseño, la arquitectura, la implementación conceptual y la evaluación del TFG.

## Contexto y alcance

- [[Contexto y alcance del TFG]] — objetivo, Odoo 19 Community, módulos funcionales y límites del proyecto.

## Decisiones y arquitectura

- [[Decisiones arquitectónicas del sistema]] — decisiones registradas, arquitectura objetivo, componentes y flujo general.
- [[Diseño de orquestación, Jev, agentes y evaluación]] — orquestador, Jev, agentes, MCP, OdooAPIClient, OpenTelemetry, KPI y supervisión humana.

## Evaluación

- [[Escenarios de evaluación - cinco niveles de complejidad]] — incidencia de referencia, cinco niveles, progresión y condiciones para construir el ground truth.

## Principios y documentación técnica relacionada

- [[ORM de Odoo y PostgreSQL]]
- [[MCP como capa semántica y controlada]]
- [[Human-in-the-loop y rol del FDE]]
- [[Observabilidad del sistema agentic]]
- [[Herramientas MCP previstas]]
- [[Persistencia de IncidentAnalysis]]
- [[Dependencias de módulos Odoo y datos de negocio]]
- [[API JSON-2 de Odoo]]
- [[Roadmap de integración]]

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
        ↓
Consolidación de evidencias y propuestas
        ↓
Streamlit → revisión humana
```

## Agentes previstos

- [[Purchase Agent]]
- [[Inventory Agent]]
- [[Manufacturing Agent]]
- [[Sales Agent]]

> [!note] Estado
> La arquitectura anterior es el diseño objetivo documentado. No implica que todos sus componentes estén implementados.
