---
type: decision
status: accepted
project: TFG Odoo Agentic AI
tags:
  - tfg
  - architecture/decision
---

# Decisiones arquitectónicas del sistema

## Decisiones registradas

1. Utilizar Odoo 19 Community como ERP.
2. Limitar el alcance funcional a Ventas, Compras, Inventario y Fabricación.
3. No sustituir el ERP ni acceder directamente a PostgreSQL desde los agentes.
4. Utilizar la API JSON-2 de Odoo.
5. Incorporar MCP como capa semántica/controlada entre agentes y API.
6. Mantener el ORM, los permisos y la lógica de negocio bajo responsabilidad de Odoo.
7. No crear módulos Python ad hoc dentro de Odoo para resolver la integración.
8. No incluir un Software Engineer Agent ni un QA Agent.
9. Considerar el FDE un rol humano.
10. Tratar la observabilidad como un elemento de primera clase.

## Justificación técnica registrada

La separación de responsabilidades favorece la mantenibilidad y evita que los agentes eludan las validaciones, permisos, reglas de acceso y lógica de negocio del ERP.

## Enlaces relacionados

- [[Separación entre API, ORM y PostgreSQL]]
- [[MCP como capa semántica y controlada]]
- [[Human-in-the-loop y rol del FDE]]
- [[Observabilidad del sistema agentic]]

> [!warning] Para la memoria del TFG
> Estas son decisiones de diseño del proyecto. Si se redacta una justificación académica, habrá que fundamentarlas posteriormente con fuentes técnicas y bibliográficas.
