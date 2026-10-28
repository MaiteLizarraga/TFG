---
type: decision-tecnica
area: arquitectura
status: planned
project: TFG Odoo Agentic AI
tags:
  - datos/modelo-relacional
  - arquitectura/multiagente
---

# Persistencia de `IncidentAnalysis`

El roadmap contempla una base de datos independiente llamada `agentic_db` para persistir `IncidentAnalysis`.

## Estructura conceptual mencionada

El resultado de análisis de una incidencia se plantea como un objeto estructurado con:

- hechos (`facts`)
- evidencias (`evidence`)
- propuestas (`proposals`)
- aprobación (`approval`)
- resultado de ejecución (`execution result`)

## Pendiente de diseño

El esquema definitivo, el ciclo de vida, las políticas de retención y la relación con los registros de Odoo aún deben especificarse.

## Enlaces

- [[Arquitectura objetivo del sistema agentic]]
- [[Roadmap de integración]]
- [[Observabilidad del sistema agentic]]
