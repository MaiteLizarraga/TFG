---
type: decision-tecnica
area: datos
status: planned
project: TFG Odoo Agentic AI
tags:
  - datos/sinteticos
  - odoo/api
  - datos/modelo-relacional
  - evaluacion/ground-truth
---

# Estrategia de datos de prueba

## 1. Datos demo existentes y sus limitaciones

Durante la configuración de Odoo 19 Community se activaron los datos de demostración. En el entorno se observaron pedidos de compra `P00001` a `P00011` y proveedores como:

- Wood Corner.
- Gemini Furniture.
- Azure Interior.
- Ready Mat.
- My Company (San Francisco).

La primera consulta a la API JSON-2 recuperó correctamente cinco pedidos de compra, entre ellos `P00011` (Ready Mat), `P00010` (Azure Interior), `P00009` (Gemini Furniture) y `P00008` (Wood Corner). Estos registros han servido para comprobar la conexión, explorar modelos y familiarizarse con los datos que devuelve Odoo.

Sin embargo, los datos demo no se han diseñado para representar la incidencia concreta del TFG. No se ha comprobado que exista en ellos una cadena completa y controlada que conecte un retraso de suministro con un déficit de inventario, órdenes de fabricación afectadas y compromisos comerciales. Tampoco constituyen por sí solos un conjunto de evaluación reproducible con un resultado esperado conocido.

Por tanto:

- Se conservan para exploración y pruebas técnicas generales.
- No se modifican para construir el escenario principal.
- Se crean entidades sintéticas independientes, identificadas mediante referencias con el prefijo `TFG-`.
- Se reutiliza la compañía y la infraestructura básica existentes en Odoo siempre que sea adecuado, sin duplicarlas innecesariamente.

Referencia: [[Carga de datos dummy]].

## 2. Escenario de referencia `TFG-INC-001`

### Descripción

**`TFG-INC-001`: retraso de un proveedor en la entrega de una materia prima.**

Un proveedor confirma que no podrá entregar en la fecha prevista una partida de tableros de madera necesaria para fabricar armarios modulares. Las existencias disponibles no cubren las necesidades de producción. Como consecuencia, dos órdenes de fabricación pueden retrasarse y afectar a dos pedidos de clientes.

El escenario recorre los cuatro módulos funcionales del TFG:

1. Compras (`purchase`): pedido confirmado y suministro retrasado.
2. Inventario (`stock`): recepción pendiente y disponibilidad insuficiente.
3. Fabricación (`mrp`): órdenes que necesitan el componente afectado.
4. Ventas (`sale_management`): pedidos de clientes que dependen de los productos terminados.

### Línea temporal de referencia

Se utiliza una fecha de corte fija para que las pruebas sean reproducibles. Las fechas son datos del escenario, no fechas dinámicas calculadas durante cada ejecución.

| Hito | Fecha de referencia |
|---|---|
| Confirmación del pedido de compra | 17/11/2026 |
| Fecha inicialmente prevista de recepción | 03/12/2026 |
| Fecha de corte y comunicación del retraso (`D0`) | 01/12/2026 |
| Nueva fecha comunicada por el proveedor principal | 11/12/2026 |
| Fecha posible de suministro alternativo | 04/12/2026 |
| Entrega comprometida al cliente 1 | 08/12/2026 |
| Entrega comprometida al cliente 2 | 10/12/2026 |

La fecha alternativa es una posibilidad que el agente debe identificar y comparar, no una solución que deba ejecutar automáticamente.

### Situación de partida

- Hay 8 tableros disponibles en el almacén.
- Hay 10 kits de herrajes disponibles.
- No hay armarios terminados disponibles.
- La fabricación de 10 armarios requiere 20 tableros y 10 kits.
- El pedido de compra principal aporta 20 tableros, pero su recepción se retrasa.
- El proveedor alternativo puede suministrar 12 tableros el 04/12/2026, sujeto a confirmación.

Con estos datos, el déficit inicial de tableros para completar las 10 unidades es de 12. Los kits de herrajes no son inicialmente el factor limitante.

### Entidades sintéticas propuestas

Las siguientes entidades constituyen el conjunto de datos de referencia que se debe crear en Odoo. Los códigos son referencias externas estables para reconocerlas; no se deben confundir con los identificadores numéricos internos que Odoo asignará al crear los registros.

**Proveedores y clientes**

| Referencia `TFG-` | Nombre propuesto | Tipo | Función en el escenario |
|---|---|---|---|
| `TFG-PROV-001` | Maderas del Norte, S.L. | Proveedor | Proveedor principal que comunica el retraso. |
| `TFG-PROV-002` | Suministros Forestales Cantábricos, S.L. | Proveedor | Alternativa capaz de suministrar 12 tableros antes. |
| `TFG-CLI-001` | Mobiliario Artea, S.L. | Cliente | Cliente del pedido de 6 armarios. |
| `TFG-CLI-002` | Equipamientos Lur, S.L. | Cliente | Cliente del pedido de 4 armarios. |

**Productos**

| Referencia `TFG-` | Producto | Tipo | Unidad de medida | Función |
|---|---|---|---|---|
| `TFG-MP-001` | Tablero contrachapado de abedul de 18 mm | Materia prima | Unidad | Componente afectado por el retraso. |
| `TFG-MP-002` | Kit de herrajes para armario | Componente | Unidad | Segundo componente de la lista de materiales. |
| `TFG-PT-001` | Armario modular de dos puertas | Producto terminado | Unidad | Producto fabricado y vendido a los clientes. |

Las referencias se introducirán en los campos estándar adecuados, por ejemplo `res.partner.ref` para contactos y `product.product.default_code` (o el campo de referencia disponible en la variante) para productos. La creación de una plantilla de producto puede generar automáticamente su variante; el generador deberá recuperar y registrar el identificador de esta última.

**Relaciones de negocio del escenario**

| Referencia lógica | Registro | Datos principales |
|---|---|---|
| `TFG-BOM-001` | Lista de materiales de `TFG-PT-001` | 2 unidades de `TFG-MP-001` y 1 unidad de `TFG-MP-002` por armario. |
| `TFG-PO-001` | Pedido de compra al proveedor principal | 20 unidades de `TFG-MP-001`, confirmadas y pendientes de recepción. |
| `TFG-MO-001` | Orden de fabricación | 6 unidades de `TFG-PT-001`; requiere 12 tableros y 6 kits. |
| `TFG-MO-002` | Orden de fabricación | 4 unidades de `TFG-PT-001`; requiere 8 tableros y 4 kits. |
| `TFG-SO-001` | Pedido de venta del cliente 1 | 6 unidades de `TFG-PT-001`, entrega comprometida el 08/12/2026. |
| `TFG-SO-002` | Pedido de venta del cliente 2 | 4 unidades de `TFG-PT-001`, entrega comprometida el 10/12/2026. |
| `TFG-PO-002` | Pedido alternativo propuesto | 12 unidades de `TFG-MP-001` al proveedor alternativo, con posible entrega el 04/12/2026. |

Las referencias `TFG-BOM-001`, `TFG-MO-001`, etc. son identificadores lógicos del conjunto de prueba. No implican que Odoo permita asignar esos valores directamente al nombre secuencial de cada documento. Se guardará su correspondencia con los IDs internos reales en el manifiesto del escenario.

## 3. Modelos y relaciones necesarios

Los modelos iniciales que intervienen en la construcción del escenario son:

| Modelo Odoo | Uso en el escenario | Relaciones principales |
|---|---|---|
| `res.partner` | Proveedores y clientes sintéticos | Se relaciona con pedidos de compra y venta mediante `partner_id`. |
| `product.template` | Definición de productos | Puede generar una o varias variantes. |
| `product.product` | Variantes concretas utilizadas en líneas y movimientos | Se referencia desde líneas de compra, venta, movimientos y listas de materiales. |
| `uom.uom` | Unidades de medida | Determina las unidades utilizadas para cantidades y conversiones. |
| `mrp.bom` | Lista de materiales del armario | Relacionada con el producto terminado y sus componentes. |
| `mrp.bom.line` | Componentes de la lista de materiales | Relaciona la BoM con `product.product` y sus cantidades. |
| `purchase.order` | Pedidos a proveedores | Relacionado con proveedor y líneas de compra. |
| `purchase.order.line` | Productos y cantidades solicitadas | Relacionado con el pedido y el producto. |
| `stock.picking` | Recepciones y entregas | Agrupa movimientos de inventario. |
| `stock.move` | Movimientos de productos | Representa cantidades, ubicaciones, estado y operaciones logísticas. |
| `stock.quant` | Existencias por producto y ubicación | Refleja las cantidades físicas y reservadas; no se utilizará como mecanismo de inserción directa. |
| `mrp.production` | Órdenes de fabricación | Relacionada con producto terminado, BoM y movimientos de componentes. |
| `sale.order` | Pedidos de clientes | Relacionado con cliente y líneas de venta. |
| `sale.order.line` | Productos y cantidades vendidas | Relacionado con pedido y producto. |

### Grafo simplificado de datos

```text
res.partner (proveedor)
        │
        ▼
purchase.order ── purchase.order.line
                         │
                         ▼
                    product.product
                         │
                         ▼
                   stock.move / picking
                         │
                         ▼
                    stock.quant
                         │
                         ▼
                    mrp.production
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        mrp.bom                 product terminado
             │                       │
        mrp.bom.line                 ▼
             │                  sale.order.line
             ▼                       │
        componentes                  ▼
                               sale.order
                                    │
                                    ▼
                              res.partner
                                (cliente)
```

Este esquema representa las dependencias funcionales relevantes, no todas las relaciones técnicas ni todos los campos relacionales de Odoo. Las relaciones efectivas deberán verificarse en los registros creados y en los movimientos generados por el propio ERP.

## 4. Diseño del conjunto de datos y orden de creación

### Principios de diseño

- **Coherencia referencial:** cada línea y movimiento debe apuntar a registros existentes.
- **Coherencia cuantitativa:** las cantidades de compra, stock, componentes, fabricación y venta deben cuadrar.
- **Coherencia temporal:** las fechas previstas, el retraso, la fabricación y las entregas deben permitir reconstruir la incidencia.
- **Trazabilidad:** todos los registros sintéticos deben poder identificarse mediante referencias `TFG-` o mediante el manifiesto.
- **Separación:** los registros del escenario no deben confundirse con los datos demo.
- **Reproducibilidad:** las cantidades, fechas y relaciones se fijan explícitamente; no se generan aleatoriamente para la evaluación principal.

### Balance de cantidades del escenario base

| Concepto | Tableros (`TFG-MP-001`) | Kits (`TFG-MP-002`) | Armarios (`TFG-PT-001`) |
|---|---:|---:|---:|
| Existencias iniciales | 8 | 10 | 0 |
| Necesidad para 10 armarios | 20 | 10 | 10 |
| Déficit inicial | 12 | 0 | — |
| Pedido principal pendiente | 20 | — | — |
| Posible suministro alternativo | 12 | — | — |

La tabla describe el balance funcional previsto. Las cantidades físicas, reservadas, previstas y disponibles que devuelve Odoo pueden diferir según las ubicaciones, rutas, movimientos y reservas configurados. El generador y las pruebas deberán comprobarlas mediante los modelos de inventario, no asumirlas a partir de esta tabla.

### Orden de creación propuesto

1. **Comprobar infraestructura existente:** compañía, almacén, ubicaciones internas, unidad de medida y configuración de rutas. Reutilizar los registros existentes.
2. **Crear contactos:** proveedores y clientes sintéticos en `res.partner`, con sus referencias `TFG-PROV-...` y `TFG-CLI-...`.
3. **Crear productos:** materias primas, componente y producto terminado. Configurar tipo de producto, unidad de medida, referencias internas y opciones de compra/venta/fabricación que correspondan.
4. **Crear la lista de materiales:** asociar el armario con dos tableros y un kit de herrajes.
5. **Establecer existencias iniciales:** 8 tableros y 10 kits en la ubicación interna seleccionada, mediante el procedimiento de ajuste de inventario de Odoo.
6. **Crear y confirmar el pedido de compra principal:** 20 tableros al proveedor principal, con recepción inicialmente prevista para el 03/12/2026.
7. **Generar la recepción entrante:** dejarla en el estado operativo que represente una recepción pendiente, sin validarla ni incrementar el stock antes de tiempo.
8. **Crear los pedidos de venta:** 6 y 4 armarios para los dos clientes, con sus fechas comprometidas.
9. **Crear las órdenes de fabricación:** 6 y 4 armarios, con sus necesidades de componentes y fechas planificadas.
10. **Comprobar las relaciones y los movimientos:** verificar qué vínculos crea Odoo automáticamente y cuáles requieren configurar rutas, reglas de aprovisionamiento o referencias de origen.
11. **Preparar la alternativa de suministro:** registrar la oferta o pedido alternativo solo en la variante del escenario que evalúe esa alternativa; no introducirla como solución confirmada en el caso base.

La confirmación de pedidos y la generación de recepciones, reservas y órdenes deben realizarse mediante los flujos de negocio de Odoo. No se deben fabricar artificialmente estados finales modificando campos internos sin ejecutar las operaciones correspondientes.

### Configuración funcional que debe verificarse

Antes de generar los registros se comprobará:

- Que los productos utilizan unidades de medida compatibles.
- Que el producto terminado tiene una BoM activa y válida.
- Que el almacén y las ubicaciones permiten recepciones, fabricación y entregas.
- Qué rutas de aprovisionamiento están disponibles y si se utilizará MTO, MTS u otra configuración.
- Cómo se vincularán los pedidos de venta con las órdenes de fabricación y sus movimientos.
- Qué estados y fechas se generan al confirmar cada documento.

No se presupone que la relación entre una venta y una orden de fabricación aparezca automáticamente por crear ambos documentos. Depende de las rutas y reglas de aprovisionamiento configuradas. Si no se utiliza una ruta que establezca ese vínculo, la correspondencia lógica se conservará en el manifiesto y se documentará como tal.

## 5. Construcción progresiva de los cinco niveles

Los cinco niveles mantienen el mismo tipo de incidencia y amplían progresivamente la información que debe investigar el sistema. Se construirán como variantes controladas del conjunto de datos, no como cinco bases de datos inconexas.

| Nivel | Información y registros necesarios | Capacidad que se evalúa |
|---|---|---|
| **1. Compras e Inventario** | `TFG-PROV-001`, `TFG-MP-001`, `TFG-PO-001`, línea de compra y recepción pendiente. Existencias iniciales del producto. | Detectar el retraso, identificar el pedido y cuantificar la cantidad pendiente. |
| **2. Disponibilidad de Inventario** | Todo lo anterior, con existencias por ubicación, movimientos pendientes y reservas relevantes. Se puede añadir una demanda competidora controlada para distinguir stock físico de disponibilidad efectiva. | Calcular el déficit real y explicar cómo afectan las reservas y los movimientos a la disponibilidad. |
| **3. Fabricación** | Todo lo anterior, más `TFG-MP-002`, `TFG-PT-001`, `TFG-BOM-001`, `TFG-MO-001` y `TFG-MO-002`. | Identificar las órdenes afectadas y calcular las necesidades de componentes. |
| **4. Compromisos comerciales** | Todo lo anterior, más `TFG-CLI-001`, `TFG-CLI-002`, `TFG-SO-001` y `TFG-SO-002`, junto con sus líneas y entregas. | Reconstruir el impacto desde el proveedor hasta los pedidos de clientes. |
| **5. Alternativas** | Todo lo anterior, más `TFG-PROV-002` y la oferta o pedido alternativo de 12 tableros, con precio y fecha de disponibilidad diferenciados. Pueden añadirse variantes controladas de stock en otras ubicaciones si se modelan realmente en Odoo. | Comparar alternativas, explicar sus consecuencias y señalar qué información requiere confirmación humana. |

### Reglas para mantener comparabilidad

- Los niveles superiores conservan los datos y relaciones de los niveles anteriores, salvo que una variante esté expresamente identificada.
- Las ampliaciones se documentan como cambios concretos del conjunto de datos.
- Una alternativa de suministro no se considera confirmada hasta que exista el registro y el estado correspondiente en Odoo.
- No se introducirán sustitutos de materias primas sin modelar y validar previamente su compatibilidad en la BoM o en el proceso productivo.
- El nivel 5 debe permitir comparar alternativas, pero no autoriza a los agentes a ejecutar compras, reservas o cambios de planificación.

## 6. Generación mediante API JSON-2 / ORM

### Decisión de acceso

Los registros de negocio se crearán y modificarán mediante la API JSON-2 de Odoo 19, que invoca métodos de los modelos a través del ORM. No se utilizarán sentencias `INSERT`, `UPDATE` o `DELETE` directas en PostgreSQL para construir el escenario.

### Motivo

El ORM gestiona:

- Validaciones y restricciones de los modelos.
- Permisos, ACL y record rules.
- Relaciones entre registros.
- Campos calculados y lógica de negocio.
- Operaciones y efectos asociados a los flujos de Odoo.

Una inserción directa en PostgreSQL podría crear registros incompletos o inconsistentes y omitir los movimientos y comportamientos que Odoo genera al confirmar documentos.

### Operaciones previstas

El generador utilizará operaciones de lectura y creación sobre los modelos necesarios, además de los métodos de negocio que se validen durante la implementación:

- `search_read` para comprobar si una entidad con referencia `TFG-` ya existe y recuperar sus datos.
- `create` para crear contactos, productos, listas de materiales y documentos.
- `write` cuando sea necesario actualizar campos permitidos.
- Métodos de confirmación, asignación o validación propios de los documentos, únicamente después de comprobar su comportamiento en Odoo 19 y los permisos del usuario técnico.

Las relaciones One2many y Many2many deberán enviarse utilizando los comandos relacionales admitidos por el ORM. El generador recuperará los IDs internos devueltos por Odoo y los utilizará en las operaciones posteriores.

### Precauciones específicas de Inventario y Fabricación

- No crear ni modificar directamente registros de `stock.quant` para simular existencias.
- Inicializar el stock mediante un ajuste de inventario realizado por el flujo de Odoo.
- Crear recepciones a partir de los pedidos de compra y mantenerlas pendientes cuando el escenario lo requiera.
- Confirmar órdenes de fabricación y comprobar los movimientos de componentes que genera Odoo.
- Validar una recepción o una entrega únicamente cuando el caso de prueba lo indique.
- No cambiar manualmente estados de documentos para simular operaciones que no se han ejecutado.

### Separación de credenciales

La API Key de Odoo se suministrará mediante una variable de entorno o un mecanismo local seguro. No se escribirá en el Markdown, en el manifiesto de datos ni en el repositorio. La configuración de secretos se mantendrá separada de los datos sintéticos.

Referencia: [[API JSON-2 de Odoo]] y [[ORM de Odoo y PostgreSQL]].

## 7. Validación de consistencia y ground truth

La carga no se considerará correcta únicamente porque las llamadas a la API devuelvan una respuesta satisfactoria. Después de crear los registros se ejecutarán comprobaciones funcionales y relacionales.

### Validaciones de entidades y relaciones

- Cada referencia `TFG-` identifica un único contacto o producto dentro de su ámbito.
- Cada línea de compra apunta al pedido y producto correctos.
- La BoM activa corresponde al producto terminado y contiene los componentes y cantidades previstos.
- Las órdenes de fabricación utilizan el producto y la BoM esperados.
- Los pedidos de venta contienen las cantidades y fechas comprometidas.
- Las recepciones y movimientos pertenecen a los documentos y productos correspondientes.
- Las relaciones entre pedidos de venta, fabricación y movimientos se verifican en Odoo; no se deducen solo por coincidencia de nombres.

### Validaciones cuantitativas

Para el conjunto base:

- Necesidad de tableros: (10 \\times 2 = 20) unidades.
- Necesidad de kits: (10 \\times 1 = 10) unidades.
- Tableros iniciales: 8 unidades.
- Déficit inicial de tableros: (20 - 8 = 12) unidades.
- Kits iniciales: 10 unidades; no existe déficit inicial de este componente.
- Pedido principal: 20 tableros pendientes.
- Alternativa potencial: 12 tableros.

Los cálculos se contrastarán con las cantidades que Odoo devuelve para existencias, reservas, movimientos y necesidades de fabricación. Debe distinguirse entre cantidad física, reservada, prevista y disponible.

### Ground truth por nivel

Cada nivel tendrá una referencia de evaluación con:

1. Identificador del escenario y nivel.
2. IDs internos y referencias `TFG-` de los registros relevantes.
3. Módulos y procesos que deben investigarse.
4. Relaciones que el agente debería reconstruir.
5. Evidencias necesarias para justificar el diagnóstico.
6. Cantidades y fechas esperadas.
7. Conclusiones y propuestas aceptables.
8. Alternativas que deben descartarse y el motivo, cuando proceda.

El ground truth se construirá a partir de los datos realmente existentes en Odoo, no solo de las tablas de diseño de este documento. Si una relación o un movimiento no se ha generado, no se incluirá como evidencia disponible.

### Criterios de evaluación

Se comprobará si el sistema:

- Identifica los registros relevantes.
- Recupera correctamente los campos y cantidades.
- Distingue stock físico de disponibilidad efectiva.
- Reconstruye las relaciones entre Compras, Inventario, Fabricación y Ventas.
- Fundamenta las conclusiones en evidencias recuperadas.
- Compara alternativas sin inventar datos.
- Explicita incertidumbres y solicita intervención humana cuando sea necesaria.

## 8. Reproducibilidad y control de los datos

### Identificación y manifiesto

Cada ejecución del generador deberá mantener un manifiesto del escenario con, al menos:

- Identificador: `TFG-INC-001`.
- Versión del conjunto de datos.
- Nivel de complejidad.
- Fecha de corte del escenario.
- Referencia lógica `TFG-` de cada entidad.
- Modelo Odoo e ID interno devuelto por la API.
- Relaciones relevantes entre registros.
- Cantidades, fechas y estados esperados.
- Resultado de las validaciones.

El manifiesto no almacenará contraseñas, API Keys ni otros secretos. Puede mantenerse como artefacto de datos del proyecto, separado de las credenciales.

### Idempotencia

El generador deberá poder ejecutarse más de una vez sin duplicar entidades:

1. Buscar cada contacto y producto por su referencia `TFG-`.
2. Si no existe, crearlo.
3. Si existe, comprobar si coincide con la definición esperada antes de actualizarlo.
4. Guardar los IDs internos devueltos por Odoo.
5. Antes de crear documentos operativos, comprobar si ya existe el documento lógico correspondiente.
6. No eliminar automáticamente registros si hay movimientos, relaciones o dependencias que puedan verse afectados.

La idempotencia debe diseñarse por modelo y operación. No basta con repetir llamadas `create`, ya que producirían duplicados.

### Aislamiento y limpieza

- Los registros sintéticos se identificarán mediante el prefijo `TFG-` en las referencias disponibles.
- Se reutilizarán compañía, almacén y ubicaciones existentes, salvo que una prueba requiera explícitamente otros.
- Se mantendrán separados los registros demo y los del escenario.
- La limpieza de datos se realizará mediante operaciones del ORM y solo después de comprobar dependencias y efectos asociados.
- Para pruebas destructivas o reinicios completos se valorará utilizar una base de datos clonada o restaurable, en lugar de borrar selectivamente documentos con movimientos relacionados.

### Estado de implementación

Este documento define el diseño funcional y las entidades sintéticas de referencia. **Las entidades y documentos descritos todavía no se consideran creados en la base de datos Odoo**: su creación efectiva, la configuración de rutas, la generación de movimientos y la validación del ground truth son tareas de implementación posteriores.

## Enlaces

- [[Carga de datos dummy]]
- [[API JSON-2 de Odoo]]
- [[Primera consulta a la API JSON-2]]
- [[Modelos de compras - purchase.order]]
- [[Dependencias de módulos Odoo y datos de negocio]]
- [[ORM de Odoo y PostgreSQL]]
- [[Escenarios de evaluación - cinco niveles de complejidad]]
- [[MCP como capa semántica y controlada]]
- [[Roadmap de integración]]
