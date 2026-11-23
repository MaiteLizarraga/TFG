---
type: concepto
area: odoo
project: TFG Odoo Agentic AI
status: understood
tags:
  - odoo/api
  - odoo/orm
  - infraestructura/postgresql
---

# ORM de Odoo y PostgreSQL

## ORM de Odoo

**ORM** significa *Object-Relational Mapping*, o mapeo objeto-relacional.

Odoo trabaja con modelos de negocio, por ejemplo:

- `purchase.order`
- `purchase.order.line`
- `res.partner`
- `product.product`
- `stock.quant`
- `stock.picking`
- `stock.move`
- `mrp.production`
- `sale.order`

El ORM gestiona, entre otras funciones:

- Persistencia y relaciones entre modelos.
- Validaciones y lógica de negocio.
- Permisos, ACL y record rules.
- Campos calculados y herencia de modelos.
- Operaciones como `create`, `write` y `unlink`.

## Modelo, campos y registros

En Odoo, un **modelo** es la definición de un tipo de objeto de negocio o de sistema con el que trabaja el ERP. Define qué datos tiene ese objeto, qué relaciones mantiene con otros objetos y qué operaciones se pueden realizar sobre él.

En términos de programación, un modelo es una clase del ORM de Odoo. En muchos casos, sus registros se almacenan en una tabla de PostgreSQL.

Por ejemplo:

| Modelo Odoo | Qué representa | Tabla SQL habitual |
|---|---|---|
| `product.template` | Plantilla o ficha general de un producto | `product_template` |
| `product.product` | Variante concreta de un producto | `product_product` |
| `purchase.order` | Pedido de compra | `purchase_order` |
| `purchase.order.line` | Línea de un pedido de compra | `purchase_order_line` |
| `stock.quant` | Cantidad de producto en una ubicación | `stock_quant` |
| `mrp.production` | Orden de fabricación | `mrp_production` |

Cuando se crea un pedido de compra en Odoo:

- El modelo `purchase.order` define los datos generales del pedido: proveedor, fecha, estado, etc.
- El modelo `purchase.order.line` define sus líneas: producto, cantidad, precio, etc.
- Cada pedido es un **registro** del modelo `purchase.order`.
- Cada línea es un registro del modelo `purchase.order.line`.
- Los **campos** son los atributos de esos registros: `partner_id`, `date_order`, `state`, `product_id`, `product_qty`, etc.

La relación entre estos conceptos puede representarse así:

```text
Modelo: purchase.order
        ↓
Campos: partner_id, date_order, state, order_line...
        ↓
Registros: PO00001, PO00002, PO00003...
        ↓
Persistencia habitual: tabla purchase_order
```

Por tanto:

- **Modelo:** define la estructura y el comportamiento de un tipo de objeto.
- **Campo:** define un dato o una relación del modelo.
- **Registro:** es una instancia concreta del modelo, con sus propios valores.
- **Tabla SQL:** es una estructura de almacenamiento de PostgreSQL que puede persistir los datos del modelo.

## Correspondencia entre modelos de Odoo y tablas PostgreSQL

Un modelo de Odoo no siempre equivale a una tabla SQL. Hay modelos abstractos, modelos transitorios (asistentes temporales), modelos que comparten tablas y relaciones Many2many que utilizan tablas intermedias.

Por este motivo, no debemos deducir la estructura física de PostgreSQL únicamente a partir del nombre técnico del modelo. Para elaborar el inventario de datos del TFG, consultaremos el esquema real de PostgreSQL y contrastaremos sus tablas, columnas, claves y restricciones con los metadatos del ORM de Odoo.

## Separación entre API, ORM y PostgreSQL

**La API no devuelve el ORM.** La API es la interfaz externa para solicitar operaciones a Odoo; el ORM permanece dentro de Odoo.

### Flujo de lectura

```text
Agente
  ↓
Odoo JSON-2 API
  ↓
Método del modelo Odoo
  ↓
ORM
  ↓
PostgreSQL
  ↓
ORM
  ↓
API
  ↓
JSON
  ↓
Agente
```

La API devuelve datos serializados —normalmente JSON—, no objetos ORM directamente.

### Responsabilidades

- **API:** interfaz de acceso externo.
- **ORM:** gestiona modelos, relaciones, persistencia, validaciones, permisos, reglas de acceso y lógica de negocio.
- **PostgreSQL:** almacena los datos persistentes.

## Implicación para el TFG

Los agentes no deben acceder directamente a PostgreSQL. El acceso a través de Odoo conserva las validaciones, los permisos y los comportamientos de negocio definidos por el ERP.

La inspección directa de PostgreSQL puede utilizarse para analizar el entorno, pero no constituye el mecanismo de acceso de los agentes. En la arquitectura del TFG, los agentes acceden a Odoo mediante herramientas semánticas MCP y la API, sin consultar ni modificar directamente la base de datos.

## Enlaces

- [[API JSON-2 de Odoo]]
- [[Modelos de compras - purchase.order]]
- [[MCP como capa semántica y controlada]]
- [[Decisiones arquitectónicas del sistema]]
