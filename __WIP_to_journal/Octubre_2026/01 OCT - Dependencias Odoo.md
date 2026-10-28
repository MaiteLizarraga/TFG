### Lo que sabemos con certeza de nuestra instalación

### Dependencias directas comprobadas

| Módulo funcional               | Dependencias directas                            | Nº    |
| ------------------------------ | ------------------------------------------------ | ----- |
| **Ventas — `sale_management`** | `digest`, `sale`                                 | **2** |
| **Compras — `purchase`**       | `account`                                        | **1** |
| **Inventario — `stock`**       | `barcodes_gs1_nomenclature`, `digest`, `product` | **3** |
| **Fabricación — `mrp`**        | `product`, `resource`, `stock`                   | **3** |
Total de dependencias directas: 9 relaciones.

**Si el objetivo es generar datos sintéticos coherentes para Odoo, necesitamos las dependencias transitivas**, pero con una precisión importante: no necesitamos "insertar" manualmente esas dependencias. Necesitamos conocerlas para entender **qué entidades y relaciones existen y en qué orden debemos generar los datos**.

### Pero hay otra distinción importante

No debemos confundir:

**A. Dependencias de módulos Odoo**

```
mrp → stock → product
```

con:

**B. Dependencias de datos de negocio**

```
manufacturing.order
        ↓
        product
        ↓
        bom
        ↓
        bom.line
```

Para **generar los datos sintéticos**, las B son incluso más importantes que las A.

### Fase 1 — Grafo de módulos

Extraemos recursivamente:

```
sale_management
 └── sale
      ├── ...
      └── ...

purchase
 └── account
      ├── ...
      └── ...

stock
 ├── product
 ├── digest
 └── barcodes_gs1_nomenclature
      └── ...

mrp
 ├── product
 ├── resource
 └── stock
      ├── ...
      └── ...
```

Así sabemos **todo el software instalado que interviene**.

### Fase 2 — Grafo de datos

Después estudiamos los modelos que realmente necesitamos para nuestro escenario:

```
res.partner
product.template
product.product
purchase.order
purchase.order.line
stock.picking
stock.move
stock.quant
mrp.bom
mrp.bom.line
mrp.production
sale.order
sale.order.line
...
```

y sus relaciones.

**Esto es lo que finalmente nos permitirá diseñar el generador de datos sintéticos.**

Sí. Vamos a obtener **primero el grafo de dependencias de módulos**, de forma completa y verificable desde PostgreSQL. No necesitamos todavía mirar los modelos de datos.

### 1. Verificar la estructura de las tablas

Ejecuta:

```
docker exec -it odoo-tfg-db psql -U odoo -d Odoo-tfg -c "
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('ir_module_module', 'ir_module_module_dependency')
ORDER BY table_name, ordinal_position;
"
```

Esto nos confirma las columnas reales que vamos a utilizar.

maite@ubuntu-tfg:~/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI$ docker exec -it odoo-tfg-db psql -U odoo -d Odoo-tfg -c "
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('ir_module_module', 'ir_module_module_dependency')
ORDER BY table_name, ordinal_position;
"
      column_name      |          data_type          
-----------------------+-----------------------------
 id                    | integer
 create_uid            | integer
 create_date           | timestamp without time zone
 write_date            | timestamp without time zone
 write_uid             | integer
 website               | character varying
 summary               | jsonb
 name                  | character varying
 author                | character varying
 icon                  | character varying
 state                 | character varying
 latest_version        | character varying
 shortdesc             | jsonb
 category_id           | integer
 description           | jsonb
 application           | boolean
 demo                  | boolean
 web                   | boolean
 license               | character varying
 sequence              | integer
 auto_install          | boolean
 to_buy                | boolean
 maintainer            | character varying
 published_version     | character varying
 url                   | character varying
 contributors          | text
 menus_by_module       | text
 reports_by_module     | text
 views_by_module       | text
 module_type           | character varying
 imported              | boolean
 id                    | integer
 name                  | character varying
 module_id             | integer
 auto_install_required | boolean
(35 rows)

### 2. Obtener el grafo completo de dependencias — recursivamente

Después ejecuta:

docker exec odoo-tfg-db psql -U odoo -d Odoo-tfg --csv -c "
WITH RECURSIVE deps AS (

    -- Dependencias directas de los 4 m�dulos ra�z
    SELECT
        m.name AS root,
        d.name AS dependency,
        1 AS level,
        ARRAY[m.name, d.name]::text[] AS path

    FROM ir_module_module m
    JOIN ir_module_module_dependency d
        ON d.module_id = m.id

    WHERE m.name IN (
        'sale_management',
        'purchase',
        'stock',
        'mrp'
    )

    UNION ALL

    -- Dependencias transitivas
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

    -- Evitar ciclos
    WHERE NOT d2.name = ANY(deps.path)
)

SELECT
    root,
    dependency,
    level,
    array_to_string(path, ' -> ') AS path

FROM deps

ORDER BY
    root,
    level,
    dependency;
" > ~/odoo-tfg/grafo-modulos-completo.csv