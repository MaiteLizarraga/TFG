---
type: decision-tecnica
area: arquitectura
status: accepted
project: TFG Odoo Agentic AI
tags:
  - arquitectura/multiagente
  - arquitectura/orquestacion
  - arquitectura/human-in-the-loop
---

# Decisiones arquitectónicas y arquitectura objetivo

## 1. Decisiones arquitectónicas registradas

1. Utilizar Odoo 19 Community como ERP de referencia.
2. Limitar el alcance funcional a Ventas, Compras, Inventario y Fabricación.
3. No sustituir el ERP ni acceder directamente a PostgreSQL desde los agentes.
4. Utilizar la API externa JSON-2 de Odoo.
5. Incorporar MCP como capa semántica y controlada entre los agentes y la API.
6. Mantener el ORM, los permisos, las reglas de acceso y la lógica de negocio bajo responsabilidad de Odoo.
7. No crear módulos Python ad hoc dentro de Odoo para resolver la integración.
8. No incluir un Software Engineer Agent ni un QA Agent.
9. Considerar el FDE un rol humano.
10. Tratar la observabilidad como un elemento de primera clase.
11. Mantener supervisión humana: el sistema investiga, analiza y propone; no ejecuta modificaciones en Odoo en el alcance inicial.

## 2. Justificación técnica registrada

La separación de responsabilidades favorece la mantenibilidad y evita que los agentes eludan las validaciones, permisos, reglas de acceso y lógica de negocio del ERP. Odoo conserva la responsabilidad sobre sus datos y operaciones; la capa agentic accede a la información mediante interfaces controladas.

Estas son decisiones de diseño del proyecto. Si se incorporan a la memoria académica, su justificación deberá fundamentarse con fuentes técnicas y bibliográficas.

## 3. Arquitectura objetivo

La arquitectura prevista conecta Odoo con una capa de integración y orquestación, que coordina agentes especializados. Estos acceden a las capacidades del ERP mediante herramientas MCP y la API JSON-2, que utiliza el ORM de Odoo para operar sobre la base de datos.

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

### Componentes y responsabilidades

- **Odoo:** sistema de información empresarial y responsable de los datos y la lógica de negocio.
- **Automation Rule / Webhook:** mecanismo previsto para iniciar el flujo ante determinados eventos.
- **FastAPI / LangGraph:** capa de integración y orquestación prevista.
- **Orchestrator:** coordina el trabajo de los agentes y controla el flujo de investigación.
- **Agentes especializados:** analizan información de las áreas funcionales correspondientes.
- **MCP:** expone herramientas semánticas y controladas para las consultas de los agentes.
- **JSON-2 API:** interfaz externa de acceso a Odoo.
- **ORM:** capa interna de Odoo que aplica la lógica de negocio y accede a los datos.
- **PostgreSQL:** persistencia de Odoo.

### Flujo de la prueba de concepto

Odoo activa la investigación mediante una Automation Rule y un webhook. LangGraph coordina los agentes especializados; estos consultan la información del ERP mediante herramientas MCP y la API JSON-2/ORM. El sistema consolida evidencias, análisis y propuestas, que se presentan en Streamlit para su revisión humana.

![[img/Esquema-arquitectura-prueba-concepto.svg]]

### Estado de la arquitectura

Esta es la arquitectura objetivo, no una afirmación de que todos sus componentes estén implementados. El entorno Odoo/API está probado; la orquestación y los agentes forman parte de fases posteriores del desarrollo.

El diseño detallado de las responsabilidades del orquestador, Jev, los agentes LLM, las herramientas MCP, OdooAPIClient, OpenTelemetry y los KPI se desarrolla en [[Diseño de orquestación, Jev, agentes y evaluación]].

![[img/Arquitectura-orquestador-Jev-MCP-OpenTelemetry.svg]]

## 4. Documentación relacionada

- [[Contexto y alcance del TFG]] — objetivo, ERP, módulos y límites funcionales.
- [[Diseño de orquestación, Jev, agentes y evaluación]] — diseño detallado de la solución.
- [[Escenarios de evaluación - cinco niveles de complejidad]] — escenarios de referencia.
- [[Separación entre API, ORM y PostgreSQL]] — separación de responsabilidades en el acceso a datos.
- [[MCP como capa semántica y controlada]] — integración de herramientas.
- [[Human-in-the-loop y rol del FDE]] — supervisión humana y responsabilidades.
- [[Observabilidad del sistema agentic]] — instrumentación y observabilidad.
- [[Roadmap de integración]] — planificación de implementación.

> [!warning] Para la memoria del TFG
> Las decisiones anteriores describen el diseño del proyecto. Las afirmaciones técnicas que se incluyan en la memoria deberán justificarse posteriormente con fuentes técnicas y bibliográficas.
