---
type: referencia-tecnica
area: odoo
project: TFG Odoo Agentic AI
status: completed
tags:
  - odoo/modelos
  - odoo/api
  - infraestructura/postgresql
  - datos/modelo-relacional
  - datos/sinteticos
---

# Inventario del esquema de Odoo

## 1. Objetivo

Se ha realizado un inventario del esquema de la instalación de Odoo 19 Community para identificar los modelos, campos, relaciones y estructuras SQL relevantes para el TFG.

El objetivo es disponer de una referencia técnica para diseñar y generar los datos sintéticos del escenario de evaluación, así como para conocer las relaciones entre los modelos funcionales de Compras, Inventario, Fabricación y Ventas.

El inventario permite contrastar los metadatos del ORM con la estructura física de PostgreSQL. No modifica los datos de negocio ni cambia el mecanismo de acceso previsto para los agentes.

## 2. Fuentes de información

Se han utilizado dos fuentes complementarias:

### 2.1. Metadatos del ORM de Odoo

La API JSON-2 ha permitido consultar los modelos y campos registrados en Odoo mediante los modelos técnicos:

- `ir.model`
- `ir.model.fields`
- `ir.module.module`
- `ir.module.module.dependency`

Se han obtenido los modelos registrados, sus campos, tipos, etiquetas, propiedades, relaciones y módulos que participan en sus definiciones.

Los datos se han exportado a JSON para analizarlos posteriormente con Python.

### 2.2. Esquema físico de PostgreSQL

Desde DBeaver se han realizado consultas de solo lectura sobre el catálogo de PostgreSQL para inspeccionar:

- Inventario de tablas.
- Columnas y tipos de datos.
- Claves primarias (PK).
- Claves foráneas (FK).
- Restricciones CHECK, UNIQUE y EXCLUSION.
- Índices únicos.

Se han inspeccionado específicamente 27 tablas principales relacionadas con los modelos funcionales del TFG.

La inspección de PostgreSQL se utiliza exclusivamente como análisis técnico del esquema. Los agentes no accederán directamente a la base de datos: utilizarán la API de Odoo y el ORM.

## 3. Alcance funcional

Se han tomado como punto de partida 16 módulos funcionales:

- `product`, `uom`
- `purchase`, `purchase_stock`, `purchase_mrp`
- `stock`, `stock_account`
- `mrp`, `mrp_account`
- `sale`, `sale_management`, `sale_stock`, `sale_mrp`
- `product_expiry`, `mrp_product_expiry`
- `sale_stock_product_expiry`

El cierre transitivo de dependencias comprende 37 módulos: los 16 funcionales y 21 dependencias técnicas adicionales.

La instalación tiene 77 módulos instalados en total.

Se han definido 34 modelos principales para el alcance del TFG. A partir de ellos se han incorporado los modelos relacionados directamente, sin realizar una expansión recursiva de todas las relaciones.

## 4. Resultados del inventario del ORM

Los datos extraídos de Odoo contienen:

| Elemento | Registros |
|---|---:|
| Modelos registrados | 469 |
| Campos registrados | 9.205 |
| Módulos instalados | 77 |
| Dependencias de módulos | 1.482 |

Tras aplicar el alcance funcional:

| Elemento | Resultado |
|---|---:|
| Modelos principales | 34 |
| Modelos relacionados directamente | 83 |
| Modelos seleccionados | 117 |
| Campos de los modelos principales | 2.456 |
| Campos de los modelos seleccionados | 4.539 |
| Campos relacionales seleccionados | 1.572 |

Los 1.572 campos relacionales corresponden a campos `many2one`, `one2many` y `many2many` de los modelos seleccionados.

La selección de modelos relacionados es deliberadamente directa. No se pretende incluir de forma indiscriminada todo el grafo de modelos de Odoo.

## 5. Resultados de la inspección SQL

Se han inspeccionado 27 tablas principales:

- Compras: `purchase_order`, `purchase_order_line`.
- Ventas: `sale_order`, `sale_order_line`.
- Productos: `product_template`, `product_product`, `product_category`, `product_supplierinfo`.
- Unidades de medida: `uom_uom`.
- Inventario: `stock_warehouse`, `stock_location`, `stock_picking_type`, `stock_picking`, `stock_move`, `stock_move_line`, `stock_quant`, `stock_lot`, `stock_route`, `stock_rule`, `stock_warehouse_orderpoint`, `stock_scrap`.
- Fabricación: `mrp_bom`, `mrp_bom_line`, `mrp_production`, `mrp_workcenter`, `mrp_workorder`.

La inspección ha permitido identificar las columnas físicas, las claves primarias, las claves foráneas y las restricciones e índices asociados a estas tablas.

Todas las tablas principales inspeccionadas disponen de una clave primaria simple basada en la columna `id`.

Las relaciones físicas de PostgreSQL complementan la información del ORM, pero no sustituyen la interpretación de las relaciones y comportamientos de negocio definidos por Odoo.

## 6. Libro Excel de referencia

Se ha generado el libro:

`odoo_schema_inventory.xlsx`

Contiene ocho hojas:

| Hoja | Contenido | Registros |
|---|---|---:|
| `01_Modelos` | Modelos seleccionados y clasificación | 117 |
| `02_Campos` | Diccionario de campos del ORM | 4.539 |
| `03_Relaciones` | Campos relacionales | 1.572 |
| `04_Tablas_SQL` | Inventario de tablas y columnas inspeccionadas | 1.375 |
| `05_Claves_Foraneas` | Claves foráneas | 291 |
| `06_Restricciones` | Restricciones e índices únicos | 51 |
| `07_Modulos` | Módulos instalados y clasificación | 77 |
| `08_Modelos_TFG` | Modelos principales del TFG | 34 |

Los recuentos corresponden a los registros de las hojas del libro, sin incluir las cabeceras.

La hoja `04_Tablas_SQL` contiene el inventario general de tablas y el detalle de columnas de las tablas seleccionadas. La clasificación de restricciones e índices queda pendiente de una auditoría final para comprobar que no se contabilizan dos veces las restricciones UNIQUE y sus índices de respaldo.

## 7. Scripts desarrollados

Se han creado tres scripts Python en `scripts/odoo_schema_inventory/`:

### `analyze_scope.py`

Analiza los metadatos extraídos de Odoo y permite explorar el alcance de modelos, campos y módulos.

### `reduce_scope.py`

Aplica la selección de módulos funcionales, calcula sus dependencias y obtiene los modelos principales y sus relaciones directas.

No genera archivos: presenta el resumen del alcance por consola.

### `generate_workbook.py`

Combina los metadatos JSON y las exportaciones SQL CSV para generar el libro Excel con las ocho hojas descritas.

Utiliza `openpyxl`.

## 8. Organización de los datos generados

Los datos de trabajo se conservan fuera del repositorio:

`~/odoo-tfg/data/odoo_schema_inventory/`

Estructura:

- `raw/`: metadatos originales extraídos de Odoo en JSON.
- `sql_exports/`: exportaciones CSV realizadas desde DBeaver.
- `odoo_schema_inventory.xlsx`: libro Excel consolidado.

Los scripts de análisis y generación sí forman parte del repositorio. Los datos extraídos y el Excel no se versionan para evitar incorporar exportaciones voluminosas y copias de información del entorno.

## 9. Implicaciones para el TFG

El inventario proporciona una base para:

- Identificar los campos reales disponibles en Odoo 19.
- Diseñar las entidades sintéticas y sus relaciones.
- Preparar las operaciones de creación y consulta mediante JSON-2.
- Comprobar las relaciones entre Compras, Inventario, Fabricación y Ventas.
- Identificar los campos de trazabilidad por lotes y caducidad.
- Evitar asumir nombres de campos o relaciones que no estén presentes en la instalación.
- Validar los datos creados mediante el ORM y contrastarlos con la estructura SQL.

La generación de datos de negocio seguirá realizándose mediante la API JSON-2 y los flujos estándar de Odoo. No se utilizarán escrituras directas en PostgreSQL.

## 10. Estado y tareas pendientes

El inventario y el libro Excel se han generado correctamente y se ha comprobado que el archivo puede abrirse mediante `openpyxl`.

Queda pendiente:

1. Ejecutar la auditoría de los CSV y del libro para confirmar los recuentos y la clasificación de restricciones e índices.
2. Revisar el contenido del Excel con LibreOffice Calc.
3. Utilizar el diccionario de modelos y campos para preparar la generación de los datos sintéticos.
4. Contrastar las relaciones del escenario con los modelos y campos reales de Odoo.

## Enlaces

- [[Estrategia de datos de prueba]]
- [[ORM de Odoo y PostgreSQL]]
- [[API JSON-2 de Odoo]]
- [[Dependencias de módulos Odoo y datos de negocio]]
