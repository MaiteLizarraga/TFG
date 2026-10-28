---
type: dashboard
area: proyecto
project: TFG Odoo Agentic AI
status: active
tags:
  - tfg
  - obsidian/dashboard
---

# TFG — Odoo + Agentic AI

> [!abstract] Objetivo
> Desarrollar un sistema de **Agentic AI para la gestión de incidencias de Supply Chain** que complemente Odoo, sin sustituirlo ni acceder directamente a PostgreSQL.

## Mapas de contenido

- [[MOC - Proyecto y arquitectura]]
- [[MOC - Entorno e infraestructura]]
- [[MOC - Odoo API y modelos]]
- [[MOC - Integración agentic]]
- [[MOC - Registro técnico]]
- [[MOC - Journaling y control de versiones]]

## Estado actual

- [x] Entorno base de Odoo 19 Community desplegado con Docker Compose.
- [x] PostgreSQL 17 operativo.
- [x] Módulos funcionales `sale_management`, `purchase`, `stock` y `mrp` instalados.
- [x] Primera consulta a la API JSON-2 ejecutada correctamente.
- [x] DBeaver conectado a la base de datos para inspección.
- [ ] Explorar tablas y relacionarlas con los modelos ORM.
- [ ] Diseñar la carga masiva de datos mediante API/ORM.
- [ ] Probar operaciones de escritura mediante JSON-2.
- [ ] Diseñar herramientas MCP semánticas.
- [ ] Integrar herramientas con LangGraph.
- [ ] Implementar el flujo de incidencias y los disparadores.
- [ ] Añadir persistencia de `IncidentAnalysis` en `agentic_db`.
- [ ] Incorporar observabilidad con Langfuse.

## Decisiones que no se deben perder de vista

- Los agentes no acceden directamente a PostgreSQL.
- Odoo conserva la responsabilidad sobre ORM, permisos y lógica de negocio.
- MCP ofrece herramientas semánticas controladas.
- El FDE es un rol humano, no un agente.
- No se implementan un Software Engineer Agent ni un QA Agent.
- La documentación del TFG se mantiene separada del entorno de ejecución.

## Cómo usar esta vault

1. Añade conceptos nuevos como notas atómicas y enlázalos con `[[enlaces internos]]`.
2. Registra problemas y soluciones en [[Plantilla - Incidencia técnica]].
3. Registra procedimientos reproducibles en [[Plantilla - Procedimiento técnico]].
4. Usa [[Plantilla - Concepto]] para conceptos técnicos.
5. Registra decisiones en [[Plantilla - Decisión técnica]].
6. Consulta [[Taxonomía de propiedades y etiquetas]] para mantener consistencia.
7. Revisa periódicamente [[MOC - Registro técnico]] para evitar que las notas queden aisladas.
