---
type: reference
area: odoo
project: TFG Odoo Agentic AI
status: active
tags:
  - odoo
  - dependencias
  - datos-sinteticos
  - postgresql
---

# Dependencias de módulos Odoo y datos de negocio

## Objetivo

Para diseñar un generador de datos sintéticos coherentes para el escenario del TFG, hay que conocer tanto las dependencias entre módulos de Odoo como las relaciones entre las entidades de negocio. Son dos grafos distintos y complementarios.

## Dependencias directas comprobadas

En la instalación consultada, las dependencias directas de los cuatro módulos funcionales son:

| Módulo funcional | Módulo Odoo | Dependencias directas | Número |
|---|---|---|---:|
| Ventas | `sale_management` | `digest`, `sale` | 2 |
| Compras | `purchase` | `account` | 1 |
| Inventario | `stock` | `barcodes_gs1_nomenclature`, `digest`, `product` | 3 |
| Fabricación | `mrp` | `product`, `resource`, `stock` | 3 |

**Total: 9 relaciones de dependencia directa.** Este recuento corresponde a las dependencias directas identificadas en la instalación consultada; no representa el total de dependencias transitivas.

## Dos grafos diferentes

### 1. Grafo de dependencias de módulos

Representa las dependencias de software declaradas por los módulos. Por ejemplo:

```text
mrp → stock → product
```

La consulta recursiva permite recorrer las dependencias transitivas de los cuatro módulos raíz (`sale_management`, `purchase`, `stock` y `mrp`) y registrar la ruta seguida.

### 2. Grafo de dependencias de datos de negocio

Representa las entidades y relaciones que deben existir para que los registros sean coherentes. Por ejemplo, en fabricación hay que estudiar la relación entre órdenes de fabricación, productos, listas de materiales y sus líneas:

```text
mrp.production
    ├── product
    └── mrp.bom
          └── mrp.bom.line
```

Modelos relevantes que se deben estudiar para el escenario:

- `res.partner`
- `product.template`
- `product.product`
- `purchase.order`
- `purchase.order.line`
- `stock.picking`
- `stock.move`
- `stock.quant`
- `mrp.bom`
- `mrp.bom.line`
- `mrp.production`
- `sale.order`
- `sale.order.line`

Para generar datos sintéticos, conocer las dependencias de negocio y el orden de creación de los registros es tan importante como conocer las dependencias de módulos.

## Consulta exploratoria de PostgreSQL

Se comprobó la estructura de las tablas `ir_module_module` e `ir_module_module_dependency` mediante `information_schema.columns`. La consulta devolvió 35 filas de columnas en total para ambas tablas.

Comando empleado:

```bash
docker exec -it odoo-tfg-db psql -U odoo -d Odoo-tfg -c "
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('ir_module_module', 'ir_module_module_dependency')
ORDER BY table_name, ordinal_position;
"
```

Para obtener el grafo completo se utilizó una CTE recursiva que parte de los cuatro módulos raíz, sigue las dependencias transitivas y evita ciclos comprobando si el siguiente módulo ya aparece en la ruta:

```sql
WITH RECURSIVE deps AS (
    SELECT
        m.name AS root,
        d.name AS dependency,
        1 AS level,
        ARRAY[m.name, d.name]::text[] AS path
    FROM ir_module_module m
    JOIN ir_module_module_dependency d
        ON d.module_id = m.id
    WHERE m.name IN ('sale_management', 'purchase', 'stock', 'mrp')

    UNION ALL

    SELECT
        deps.root,
        d2.name AS dependency,
        deps.level + 1 AS level,
        deps.path || d2.name AS path
    FROM deps
    JOIN ir_module_module m2
        ON m2.name = deps.dependency
    JOIN ir_module_module_dependency d2
        ON d2.module_id = m2.id
    WHERE NOT d2.name = ANY(deps.path)
)
SELECT
    root,
    dependency,
    level,
    array_to_string(path, ' -> ') AS path
FROM deps
ORDER BY root, level, dependency;
```

En la sesión original, la salida se redirigió a `~/odoo-tfg/grafo-modulos-completo.csv` usando `psql --csv`.

## Implicaciones para el TFG

1. Identificar primero las dependencias de módulos para entender qué componentes intervienen en la instalación.
2. Estudiar después los modelos y relaciones de negocio que necesita el escenario.
3. Diseñar el generador de datos sintéticos teniendo en cuenta las relaciones y el orden de creación de los registros.
4. Tratar la consulta directa a PostgreSQL como una técnica de inspección del entorno, **no como el mecanismo de acceso de los agentes**. En la arquitectura del TFG, los agentes acceden a Odoo mediante herramientas semánticas y la API; no consultan ni modifican directamente la base de datos.

## Estado

Las dependencias directas y el esquema de consulta recursiva están documentados. La extracción completa del grafo y el análisis detallado de las relaciones entre modelos son pasos diferenciados; los ejemplos de modelos de esta nota constituyen el ámbito inicial de estudio, no una especificación exhaustiva de todas sus relaciones.
