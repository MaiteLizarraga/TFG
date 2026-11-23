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
  - supply-chain/alimentacion
---

# Estrategia de datos de prueba

## 1. Datos demo existentes y criterios de separación

Durante la configuración de Odoo 19 Community se activaron los datos de demostración. En el entorno se observaron pedidos de compra `P00001` a `P00011` y proveedores como Wood Corner, Gemini Furniture, Azure Interior, Ready Mat y My Company (San Francisco).

La primera consulta a la API JSON-2 recuperó correctamente cinco pedidos de compra, entre ellos `P00011` (Ready Mat), `P00010` (Azure Interior), `P00009` (Gemini Furniture) y `P00008` (Wood Corner). Estos registros han servido para comprobar la conexión, explorar modelos y familiarizarse con los datos de Odoo.

Los datos demo no representan la incidencia del TFG ni constituyen un conjunto de evaluación controlado. Por tanto:

- Se conservan para exploración y pruebas técnicas generales.
- No se modifican para construir el escenario principal.
- Las entidades sintéticas se identifican mediante referencias externas con el prefijo `TFG-`.
- Se reutilizan la compañía, el almacén y las ubicaciones existentes siempre que sea adecuado, sin duplicarlos innecesariamente.

Referencia: [[Carga de datos dummy]].

## 2. Escenario de referencia `TFG-INC-001`

### 2.1. Empresa y contexto operativo

El escenario representa una empresa ficticia **fabricante y distribuidora de sushi**. Compra ingredientes frescos, fabrica bandejas de sushi en dos formatos y distribuye los productos terminados a varios clientes.

La incidencia que se evaluará es una **reducción inesperada de la disponibilidad de salmón fresco**, materia prima crítica para la fabricación. El escenario base parte de una situación estable: todos los ingredientes están disponibles en cantidad suficiente para atender el plan de fabricación. La reducción de existencias de salmón se introducirá posteriormente mediante el trigger del experimento, no como una condición inicial.

El escenario recorre los cuatro módulos funcionales del TFG:

1. Compras (`purchase`): proveedores y pedidos de aprovisionamiento.
2. Inventario (`stock`): existencias, lotes, caducidades, movimientos y disponibilidad.
3. Fabricación (`mrp`): listas de materiales y órdenes de fabricación.
4. Ventas (`sale_management`): pedidos de clientes y compromisos de entrega.

No se fija por ahora una cronología de retraso de proveedor ni una fecha D0. Las fechas operativas que Odoo necesite se definirán al preparar cada ejecución, manteniendo el escenario reproducible mediante el manifiesto.

### 2.2. Magnitud de la operación

La empresa fabrica **10.000 bandejas diarias en total**, repartidas inicialmente de forma equilibrada entre los dos formatos:

- 5.000 bandejas de sushi de 10 piezas.
- 5.000 bandejas de sushi de 15 piezas.

La distribución 50/50 es una hipótesis de diseño para concretar el conjunto de datos. Se podrá cambiar en una versión posterior del escenario, pero cualquier cambio deberá reflejarse en las cantidades de fabricación, ventas, consumo y stock.

Se mantiene una única receta de referencia para ambos formatos, con las cantidades por bandeja acordadas. Por tanto, a efectos de este conjunto sintético, una bandeja de 10 piezas y una de 15 piezas consumen la misma cantidad de cada ingrediente. Es una simplificación deliberada para aislar la lógica de aprovisionamiento e impacto transversal, no una afirmación sobre una receta gastronómica real.

### 2.3. Productos y unidades de medida

**Materias primas (cinco):**

| Referencia | Producto | Unidad de medida | Consumo por bandeja |
|---|---|---:|---:|
| `TFG-MP-001` | Salmón fresco | kg | 0,30 |
| `TFG-MP-002` | Arroz para sushi | kg | 0,25 |
| `TFG-MP-003` | Alga nori | unidad | 2 |
| `TFG-MP-004` | Aguacate | kg | 0,20 |
| `TFG-MP-005` | Queso crema | kg | 0,10 |

**Productos terminados (dos):**

| Referencia | Producto | Unidad | Producción diaria de referencia |
|---|---|---|---:|
| `TFG-PT-001` | Bandeja de sushi variado de 10 piezas | unidad | 5.000 |
| `TFG-PT-002` | Bandeja de sushi variado de 15 piezas | unidad | 5.000 |

Las referencias son identificadores externos estables; no deben confundirse con los IDs numéricos internos que Odoo asigna a los registros. Las referencias se introducirán en los campos estándar disponibles, por ejemplo `res.partner.ref` para contactos y `default_code` para productos. La creación de `product.template` puede generar una variante `product.product`; el generador deberá recuperar y guardar el ID real de la variante.

### 2.4. Lista de materiales (BoM)

**BoM** significa *Bill of Materials*, traducido habitualmente como **lista de materiales** o **estructura de fabricación**. En Odoo define qué componentes se necesitan y en qué cantidades para fabricar una unidad de un producto terminado. Se representa mediante `mrp.bom` y sus líneas `mrp.bom.line`.

Se mantendrá una única receta de referencia, con las siguientes cantidades por bandeja:

| Ingrediente | Cantidad por bandeja |
|---|---:|
| Salmón fresco | 0,30 kg |
| Arroz para sushi | 0,25 kg |
| Alga nori | 2 unidades |
| Aguacate | 0,20 kg |
| Queso crema | 0,10 kg |

La decisión de utilizar una sola receta para los dos formatos debe verificarse en Odoo 19: se comprobará cómo asociar una misma BoM a ambos productos terminados y si la configuración permite seleccionar una BoM común sin duplicar la receta. Si Odoo exige una BoM por producto, se crearán dos registros de BoM equivalentes, manteniendo una única definición lógica de receta en el manifiesto. No se alterarán las cantidades por el mero hecho de que haya dos tamaños.

Referencia lógica: `TFG-BOM-001` (receta común; o dos registros técnicos equivalentes si Odoo lo requiere).

### 2.5. Consumo diario calculado

Para una producción total de 10.000 bandejas diarias:

| Ingrediente | Consumo por bandeja | Necesidad diaria |
|---|---:|---:|
| Salmón fresco | 0,30 kg | 3.000 kg |
| Arroz para sushi | 0,25 kg | 2.500 kg |
| Alga nori | 2 unidades | 20.000 unidades |
| Aguacate | 0,20 kg | 2.000 kg |
| Queso crema | 0,10 kg | 1.000 kg |

El cálculo se basa en la receta sintética única y en el volumen de fabricación diario. Las cantidades son datos de diseño del experimento, no una receta comercial validada.

## 3. Contactos y documentos operativos

### 3.1. Proveedores y clientes

Se crearán dos proveedores y un mínimo de cinco clientes sintéticos. Los nombres son ficticios y se utilizarán exclusivamente para el entorno de pruebas.

**Proveedores**

| Referencia | Nombre propuesto | Función |
|---|---|---|
| `TFG-PROV-001` | Atlántico Fresh Foods, S.L. | Proveedor principal de salmón fresco y proveedor de referencia para el escenario. |
| `TFG-PROV-002` | Nippon Food Supply, S.L. | Proveedor alternativo de salmón; se incorpora al nivel 5 para comparar una alternativa de aprovisionamiento. |

**Clientes**

| Referencia | Nombre propuesto | Demanda diaria de referencia | Función |
|---|---|---:|---|
| `TFG-CLI-001` | Sushi Market, S.L. | 2.000 bandejas | Cliente mayorista. |
| `TFG-CLI-002` | Tokyo Catering, S.L. | 2.000 bandejas | Cliente de catering. |
| `TFG-CLI-003` | Nippon Express Foods, S.L. | 2.000 bandejas | Distribuidor regional. |
| `TFG-CLI-004` | Kyoto Retail, S.L. | 2.000 bandejas | Cadena de tiendas. |
| `TFG-CLI-005` | Wasabi Gourmet, S.L. | 2.000 bandejas | Cliente de restauración y distribución. |

Para la primera versión se asignarán 1.000 bandejas de cada formato a cada cliente, de modo que cada uno reciba 2.000 bandejas y el total diario de ventas sea 10.000 bandejas. La distribución es sintética y equilibrada; se conservará en el manifiesto.

### 3.2. Documentos de referencia

| Referencia lógica | Documento Odoo | Contenido de referencia |
|---|---|---|
| `TFG-PO-001` | Pedido de compra principal | Compra de 3.000 kg de salmón fresco al proveedor principal, equivalente a un día de consumo de referencia. No se considera retrasado en el escenario base. |
| `TFG-SO-001` a `TFG-SO-005` | Pedidos de venta | Un pedido por cliente, con 1.000 bandejas de 10 piezas y 1.000 bandejas de 15 piezas por pedido. |
| `TFG-MO-001` | Orden de fabricación | 5.000 bandejas de 10 piezas. |
| `TFG-MO-002` | Orden de fabricación | 5.000 bandejas de 15 piezas. |
| `TFG-BOM-001` | BoM lógica | Receta común de cinco ingredientes; técnicamente podrá materializarse en una o dos BoM según las restricciones verificadas en Odoo. |
| `TFG-PO-002` | Oferta/pedido alternativo | Solo en el nivel 5: propuesta de suministro de salmón por el proveedor alternativo, todavía no aprobada ni confirmada. |

Las cantidades de los documentos se corresponden con el volumen diario de referencia. La compra principal de 3.000 kg representa un día de consumo de salmón; no se presupone que su recepción esté retrasada. La propuesta alternativa se reservará para el experimento de nivel 5.

Las referencias `TFG-PO-...`, `TFG-SO-...`, `TFG-MO-...` y `TFG-BOM-...` son IDs lógicos del conjunto de prueba. No implican que Odoo permita asignar esos valores directamente a los nombres secuenciales de los documentos. El manifiesto guardará la correspondencia entre cada referencia lógica y los IDs internos reales.

## 4. Inventario, lotes y caducidades

### 4.1. Situación inicial estable

El conjunto de datos parte de una situación estable: todo el stock necesario para cubrir dos ciclos diarios de fabricación está disponible en las ubicaciones internas seleccionadas. Esto incluye el salmón. No existe déficit inicial ni recepción retrasada que condicione la producción.

Se propone mantener un stock inicial equivalente a dos días de consumo:

| Producto | Consumo diario | Stock inicial propuesto (2 días) |
|---|---:|---:|
| Salmón fresco | 3.000 kg | 6.000 kg |
| Arroz para sushi | 2.500 kg | 5.000 kg |
| Alga nori | 20.000 unidades | 40.000 unidades |
| Aguacate | 2.000 kg | 4.000 kg |
| Queso crema | 1.000 kg | 2.000 kg |

Los productos terminados pueden partir de cero o de una cantidad explícita que se defina para cada experimento. Para la primera versión se recomienda partir de cero para que la producción diaria y los pedidos de venta sean trazables.

El trigger del escenario modificará posteriormente la disponibilidad de salmón mediante una operación de inventario coherente con Odoo. El volumen y el mecanismo exactos de la reducción se definirán en el diseño del trigger y quedarán registrados como parte de la variante experimental. El estado inicial del resto de ingredientes permanecerá estable, salvo que un experimento indique expresamente lo contrario.

### 4.2. Trazabilidad por lotes y caducidad

Se cambia la decisión inicial de trazabilidad básica: al tratarse de alimentos frescos, **se utilizarán lotes y fechas de caducidad**.

- Los cinco ingredientes tendrán seguimiento por lote (`tracking = 'lot'`).
- Los dos productos terminados también tendrán seguimiento por lote para conservar la trazabilidad del producto fabricado.
- Cada lote tendrá una cantidad, ubicación y fecha de caducidad coherentes con el producto.
- Las recepciones de proveedores deberán permitir registrar el lote recibido y su caducidad.
- Las órdenes de fabricación consumirán componentes identificados por lote y producirán lotes de producto terminado.
- Las entregas deberán conservar la relación con los lotes expedidos, según el flujo estándar de Odoo.

La configuración concreta de fechas de caducidad depende de los campos disponibles en la versión instalada y de la activación de la funcionalidad de fechas de caducidad. Antes de generar datos se inspeccionarán los campos de producto y lote, las opciones de seguimiento y los métodos de negocio correspondientes. No se inventarán nombres de campos ni se escribirán estados internos sin verificar.

La caducidad permitirá introducir posteriormente escenarios adicionales: lote de salmón próximo a caducar, lote bloqueado/no utilizable, consumo FEFO (First Expired, First Out) o redistribución entre ubicaciones. No se incorporarán estas complejidades al escenario base salvo que formen parte del nivel evaluado.

## 5. Modelos y relaciones de negocio

Los modelos iniciales que intervienen en la construcción son:

| Modelo Odoo | Uso | Relaciones principales |
|---|---|---|
| `res.partner` | Proveedores y clientes | `partner_id` en pedidos de compra y venta. |
| `product.template` | Definición de productos | Puede generar variantes de producto. |
| `product.product` | Variantes utilizadas en líneas y movimientos | Productos de compras, ventas, stock, BoM y fabricación. |
| `uom.uom` | Unidades de medida | Unidades y conversiones de cantidades. |
| `mrp.bom` | Lista de materiales | Producto terminado y componentes. |
| `mrp.bom.line` | Líneas de la BoM | Producto componente y cantidad requerida. |
| `purchase.order` / `purchase.order.line` | Pedidos y líneas de compra | Proveedor, producto, cantidad y recepción prevista. |
| `sale.order` / `sale.order.line` | Pedidos y líneas de venta | Cliente, producto y cantidad solicitada. |
| `stock.picking` | Recepciones, entregas y transferencias | Agrupa movimientos de inventario. |
| `stock.move` | Movimientos de productos | Cantidades, ubicaciones, estado y operaciones logísticas. |
| `stock.quant` | Existencias por producto y ubicación | Cantidad física y reservada; no se utilizará para insertar stock directamente. |
| `stock.lot` | Lotes de ingredientes y productos terminados | Producto, referencia de lote y fechas de caducidad según configuración. |
| `mrp.production` | Órdenes de fabricación | Producto terminado, BoM y movimientos de componentes. |

### Grafo funcional simplificado

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
                   stock.picking / stock.move
                         │
                         ▼
                  stock.lot / stock.quant
                         │
                         ▼
                    mrp.production
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
          mrp.bom              producto terminado
             │                       │
        mrp.bom.line                 ▼
             │                  sale.order.line
             ▼                       │
        ingredientes                 ▼
                                sale.order
                                     │
                                     ▼
                              res.partner (cliente)
```

El esquema representa dependencias funcionales, no todas las relaciones técnicas de Odoo. Las relaciones efectivas se verificarán en los registros y movimientos creados por el ERP.

## 6. Balance de cantidades y construcción del conjunto de datos

### 6.1. Balance diario

| Concepto | Salmón | Arroz | Nori | Aguacate | Queso crema |
|---|---:|---:|---:|---:|---:|
| Necesidad diaria | 3.000 kg | 2.500 kg | 20.000 ud. | 2.000 kg | 1.000 kg |
| Stock inicial (2 días) | 6.000 kg | 5.000 kg | 40.000 ud. | 4.000 kg | 2.000 kg |
| Déficit inicial | 0 | 0 | 0 | 0 | 0 |

La tabla describe cantidades físicas iniciales de referencia. Odoo puede distinguir cantidades físicas, reservadas, previstas y disponibles; estas magnitudes se comprobarán mediante los modelos y ubicaciones reales, no se inferirán únicamente de la tabla.

### 6.2. Orden de creación propuesto

1. **Comprobar infraestructura existente:** compañía, almacén, ubicaciones internas, unidades de medida, categorías, rutas y reglas de aprovisionamiento. Reutilizar los registros existentes.
2. **Inspeccionar configuración de trazabilidad:** verificar seguimiento por lotes y fechas de caducidad en Odoo 19, incluidos los campos de producto y lote.
3. **Crear contactos:** dos proveedores y cinco clientes en `res.partner`, con referencias `TFG-PROV-...` y `TFG-CLI-...`.
4. **Crear productos:** cinco materias primas y dos productos terminados. Configurar tipo, unidad, referencia, opciones de compra/venta/fabricación, seguimiento por lote y opciones de caducidad que existan en la instancia.
5. **Crear la BoM:** asociar los cinco ingredientes a los productos terminados. Verificar si una BoM puede compartirse o si se necesitan dos registros técnicos equivalentes.
6. **Crear lotes iniciales:** registrar lotes de ingredientes con cantidades y caducidades coherentes, y asignarlos a las ubicaciones internas mediante el flujo de inventario de Odoo.
7. **Establecer existencias iniciales:** cargar las cantidades de la tabla mediante ajustes de inventario estándar, no mediante escrituras directas en `stock.quant`.
8. **Crear y confirmar el pedido de compra principal:** 3.000 kg de salmón al proveedor principal. No marcarlo como retrasado en el escenario base.
9. **Generar la recepción entrante:** mantenerla en el estado operativo correspondiente al escenario, registrando lotes y caducidades cuando proceda. La recepción no debe duplicar las existencias iniciales si estas ya se han cargado.
10. **Crear los cinco pedidos de venta:** cada uno con 1.000 bandejas de 10 piezas y 1.000 bandejas de 15 piezas.
11. **Crear las órdenes de fabricación:** una orden de 5.000 bandejas de 10 piezas y otra de 5.000 de 15 piezas; comprobar las necesidades de componentes generadas.
12. **Comprobar relaciones y movimientos:** verificar qué vínculos crea Odoo automáticamente y cuáles requieren rutas, reglas de aprovisionamiento o referencias lógicas en el manifiesto.
13. **Preparar la alternativa de suministro:** incorporar al proveedor alternativo y la propuesta de 3.000 kg de salmón solo en la variante de nivel 5. No confirmarla ni ejecutarla en el caso base.

Las confirmaciones, reservas, recepciones, fabricación y entregas se realizarán mediante flujos de negocio de Odoo. No se simularán estados finales modificando campos internos sin ejecutar las operaciones correspondientes.

### 6.3. Relación entre pedidos de venta y órdenes de fabricación

No se asumirá que crear un pedido de venta y una orden de fabricación genera automáticamente una relación entre ambos. Se comprobarán las rutas y reglas de aprovisionamiento disponibles (por ejemplo, MTO/MTS y reglas asociadas) y los módulos de integración instalados.

Si la configuración de Odoo no genera una vinculación automática y verificable, se conservará la correspondencia lógica entre pedidos de venta y órdenes de fabricación en el manifiesto del escenario. No se presentará una relación inferida como si fuera una relación nativa del ERP.

## 7. Experimentos: cinco niveles de complejidad

Los cinco experimentos parten del mismo conjunto de datos estable. Cada nivel añade información y relaciones que el sistema debe investigar. El trigger que reduce la disponibilidad de salmón se aplicará de forma controlada en cada ejecución; no forma parte del estado inicial.

| Experimento | Datos adicionales respecto al anterior | Pregunta/objetivo de evaluación | Resultado esperado |
|---|---|---|---|
| **E1 — Compras e Inventario** | Proveedor principal, pedido de compra, recepción prevista, existencias y lotes de salmón. | Identificar qué suministro y qué lotes condicionan la disponibilidad de salmón tras activarse el trigger. | Localizar proveedor, pedido, cantidad afectada, lotes y stock disponible. |
| **E2 — Disponibilidad y caducidad** | Movimientos pendientes, reservas, ubicaciones y fechas de caducidad de los cinco ingredientes. | Determinar la disponibilidad efectiva, teniendo en cuenta lotes, caducidades y cantidades reservadas. | Cuantificar déficit o riesgo y justificar qué stock es utilizable. |
| **E3 — Fabricación** | Dos productos terminados, BoM/BoM equivalentes, dos órdenes de fabricación y lotes de componentes. | Calcular cómo afecta la reducción de salmón a las necesidades de fabricación de ambos formatos. | Identificar órdenes afectadas, necesidades de ingredientes y cantidades potencialmente fabricables. |
| **E4 — Compromisos comerciales** | Cinco clientes, cinco pedidos de venta, cantidades por formato, fechas y relaciones verificadas con fabricación/entregas. | Reconstruir el impacto sobre los compromisos comerciales. | Identificar clientes y pedidos afectados, cantidades y prioridades posibles, con evidencias. |
| **E5 — Alternativas de aprovisionamiento** | Segundo proveedor y oferta/propuesta alternativa de salmón, con cantidad, precio, plazo y condiciones. | Comparar la alternativa con el suministro principal y formular una propuesta supervisada. | Presentar opciones, consecuencias y datos pendientes; solicitar aprobación humana antes de ejecutar. |

### Reglas de comparabilidad

- Cada experimento conserva los datos y relaciones de los niveles anteriores.
- Las ampliaciones se registran como cambios explícitos de la variante.
- El escenario base comienza con stock suficiente de todos los ingredientes, incluido el salmón.
- El trigger de reducción de salmón debe ser reproducible y quedar documentado (cantidad, lote, ubicación, operación y resultado).
- El proveedor alternativo solo se incorpora en E5.
- Una oferta alternativa no se considera suministro confirmado hasta que exista el documento correspondiente y su estado se haya verificado en Odoo.
- No se propondrán ingredientes sustitutivos si no están modelados y validados en la BoM o en el proceso productivo.
- Los agentes pueden analizar y proponer; las compras, reservas, cambios de planificación y demás acciones con impacto operativo quedan sujetas a Human-in-the-Loop.

## 8. Generación mediante API JSON-2 / ORM

### Decisión de acceso

Los registros de negocio se crearán y modificarán mediante la API JSON-2 de Odoo 19, que invoca métodos de los modelos a través del ORM. No se utilizarán sentencias `INSERT`, `UPDATE` o `DELETE` directas en PostgreSQL para construir el escenario.

El ORM gestiona validaciones, restricciones, permisos, ACL, record rules, relaciones, campos calculados y lógica de negocio. Una inserción directa en PostgreSQL podría omitir comportamientos y movimientos que Odoo genera al confirmar documentos.

### Operaciones previstas

- `search_read`: comprobar si una entidad con referencia `TFG-` existe y recuperar sus datos.
- `fields_get`: inspeccionar los campos reales y sus tipos en la versión instalada antes de crear registros.
- `create`: crear contactos, productos, BoM, lotes y documentos.
- `write`: actualizar campos permitidos cuando sea necesario.
- Métodos de negocio: confirmar, reservar, producir o validar documentos solo después de verificar su comportamiento en Odoo 19 y los permisos del usuario técnico.

Las relaciones One2many y Many2many se enviarán mediante los comandos relacionales admitidos por el ORM. El generador recuperará los IDs internos devueltos por Odoo y los utilizará en las operaciones posteriores. Cada llamada JSON-2 debe tratarse como una operación transaccional independiente; el generador debe comprobar el resultado de cada paso y no asumir que una secuencia de llamadas constituye una única transacción.

### Observaciones verificadas en la instancia Odoo 19

La consulta `fields_get` de `product.template` ha confirmado, entre otros, los campos `name`, `default_code`, `type`, `is_storable`, `purchase_ok`, `sale_ok`, `uom_id`, `categ_id`, `tracking`, `company_id`, `active` y `route_ids`. En esa consulta no aparecieron `detailed_type` ni `uom_po_id`; no deben darse por disponibles.

En `product.product` se han confirmado `product_tmpl_id`, `default_code`, `barcode`, `uom_id`, `active` y `company_id`.

Una consulta de `uom.uom/search_read` falló al solicitar `category_id`, con el error `Invalid field 'category_id' on 'uom.uom'`. Antes de consultar unidades de medida se debe ejecutar `fields_get` sobre `uom.uom` y seleccionar los nombres reales de los campos. El error no demuestra que falten unidades de medida.

### Precauciones específicas de Inventario, lotes y Fabricación

- No crear ni modificar directamente registros de `stock.quant` para simular existencias.
- Inicializar stock mediante ajustes de inventario realizados por el flujo de Odoo.
- Crear y asignar lotes mediante los modelos y operaciones estándar, comprobando la configuración de caducidad.
- Crear recepciones a partir de pedidos de compra y mantenerlas en el estado requerido por cada experimento.
- Confirmar órdenes de fabricación y comprobar los movimientos de componentes y lotes que genera Odoo.
- Validar recepciones y entregas únicamente cuando el experimento lo indique.
- No cambiar manualmente estados de documentos para simular operaciones que no se han ejecutado.

### Separación de credenciales

La API Key de Odoo se suministrará mediante una variable de entorno o mecanismo local seguro. No se escribirá en Markdown, manifiestos ni repositorio. Las credenciales se mantendrán separadas de los datos sintéticos.

Referencias: [[API JSON-2 de Odoo]] y [[ORM de Odoo y PostgreSQL]].

## 9. Validación de consistencia y ground truth

La carga no se considerará correcta únicamente porque las llamadas a la API devuelvan una respuesta satisfactoria. Después de crear los registros se ejecutarán comprobaciones funcionales y relacionales.

### Validaciones de entidades y relaciones

- Cada referencia `TFG-` identifica un único contacto o producto dentro de su ámbito.
- Cada línea de compra apunta al pedido, proveedor y producto correctos.
- La BoM corresponde a los productos terminados y contiene los cinco componentes y cantidades previstos.
- Las órdenes de fabricación utilizan el producto y la BoM esperados.
- Los pedidos de venta contienen las cantidades y formatos asignados a cada cliente.
- Los lotes y fechas de caducidad están asociados a los productos y movimientos correctos.
- Las recepciones y movimientos pertenecen a los documentos y productos correspondientes.
- Las relaciones entre pedidos de venta, fabricación y movimientos se verifican en Odoo; no se deducen solo por coincidencia de nombres.

### Validaciones cuantitativas

Para 10.000 bandejas diarias, la necesidad esperada es 3.000 kg de salmón, 2.500 kg de arroz, 20.000 unidades de nori, 2.000 kg de aguacate y 1.000 kg de queso crema. El stock inicial propuesto equivale a dos días de consumo y, por tanto, no presenta déficit inicial.

Los cálculos se contrastarán con las cantidades físicas, reservadas, previstas y disponibles que Odoo devuelve. Se comprobará también el balance por lote y ubicación y la coherencia de las fechas de caducidad.

### Ground truth por experimento

Cada experimento tendrá una referencia que especifique:

1. Identificador del escenario y experimento.
2. Versión del conjunto de datos y configuración del trigger.
3. IDs internos y referencias `TFG-` de los registros relevantes.
4. Módulos y procesos que deben investigarse.
5. Relaciones que el agente debería reconstruir.
6. Evidencias necesarias para justificar el diagnóstico.
7. Cantidades, lotes, caducidades y fechas esperadas.
8. Conclusiones y propuestas aceptables.
9. Alternativas que deben descartarse y el motivo, cuando proceda.

El ground truth se construirá a partir de los datos realmente existentes en Odoo, no solo de las tablas de diseño. Si una relación o movimiento no se ha generado, no se incluirá como evidencia disponible.

### Criterios de evaluación

Se comprobará si el sistema identifica los registros relevantes, recupera campos y cantidades, distingue stock físico de disponibilidad efectiva, interpreta lotes y caducidades, reconstruye relaciones entre los cuatro módulos, fundamenta sus conclusiones en evidencias, compara alternativas sin inventar datos y solicita intervención humana cuando corresponda.

## 10. Reproducibilidad, manifiesto e idempotencia

### Manifiesto del escenario

Cada ejecución mantendrá un manifiesto con, al menos:

- Identificador: `TFG-INC-001`.
- Versión del conjunto de datos.
- Experimento/nivel de complejidad.
- Configuración del trigger (incluyendo producto, lote, ubicación, cantidad y operación).
- Referencia lógica `TFG-` de cada entidad.
- Modelo Odoo e ID interno devuelto por la API.
- Relaciones relevantes entre registros.
- Cantidades, lotes, fechas de caducidad y estados esperados.
- Resultado de las validaciones.

El manifiesto no almacenará contraseñas, API Keys ni otros secretos.

### Idempotencia

El generador deberá poder ejecutarse más de una vez sin duplicar entidades:

1. Buscar contactos y productos por sus referencias `TFG-`.
2. Si no existen, crearlos.
3. Si existen, comprobar que coinciden con la definición esperada antes de actualizarlos.
4. Guardar los IDs internos devueltos por Odoo.
5. Antes de crear lotes y documentos operativos, comprobar si ya existe el registro lógico correspondiente.
6. No eliminar automáticamente registros si tienen movimientos, relaciones o dependencias que puedan verse afectados.

No basta con repetir llamadas `create`, porque producirían duplicados. La idempotencia debe diseñarse por modelo y operación.

### Aislamiento y limpieza

- Los registros sintéticos se identificarán mediante el prefijo `TFG-` en los campos de referencia disponibles.
- Se reutilizarán compañía, almacén y ubicaciones existentes, salvo que una prueba requiera explícitamente otros.
- Los registros sintéticos se mantendrán separados de los datos demo.
- La limpieza se realizará mediante operaciones del ORM y solo después de comprobar dependencias y efectos asociados.
- Para pruebas destructivas o reinicios completos se valorará utilizar una base de datos clonada o restaurable.

### Estado de implementación

Este documento define el diseño funcional y las entidades sintéticas de referencia. **Las entidades y documentos descritos todavía no se consideran creados en la base de datos Odoo.** Quedan pendientes la inspección completa de campos, la configuración de rutas y caducidades, la creación efectiva de registros, la validación de movimientos y la construcción del ground truth.

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
