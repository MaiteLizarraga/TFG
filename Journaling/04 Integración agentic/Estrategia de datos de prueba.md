---
type: design
status: planned
project: TFG Odoo Agentic AI
tags:
  - test-data
  - odoo
  - supply-chain
---

# Estrategia de datos de prueba

## Necesidad

Se ha planteado crear una carga masiva de datos para construir escenarios realistas de Supply Chain.

## Decisión de acceso

Los registros de negocio deben crearse preferentemente mediante API/ORM, no con `INSERT` directo en PostgreSQL.

## Motivo

Las inserciones directas podrían saltarse:

- Validaciones del ORM.
- Permisos y record rules.
- Lógica de negocio.
- Relaciones y comportamientos definidos por Odoo.

## Flujo de negocio de ejemplo

```text
Proveedor
  ↓
Pedido de compra
  ↓
Recepción
  ↓
Stock
  ↓
Orden de fabricación
  ↓
Producto terminado
  ↓
Pedido de venta
```

## Pendiente

Definir generador, volumen, consistencia referencial, casos nominales y escenarios de incidencia.

## Enlaces

- [[Carga de datos de demostración]]
- [[API JSON-2 de Odoo]]
- [[Roadmap de integración]]
