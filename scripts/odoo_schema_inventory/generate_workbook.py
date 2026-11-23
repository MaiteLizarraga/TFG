import csv
import json
from pathlib import Path
from collections import defaultdict

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter


# =========================================================
# RUTAS
# =========================================================

BASE = Path.home() / "odoo-tfg/data/odoo_schema_inventory"
RAW = BASE / "raw"
SQL = BASE / "sql_exports"
OUTPUT = BASE / "odoo_schema_inventory.xlsx"


def load_json(filename):
    with (RAW / filename).open(encoding="utf-8") as f:
        return json.load(f)


def load_csv(filename):
    path = SQL / filename
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def value(v):
    """Convierte valores de Odoo en valores legibles para Excel."""
    if v is False or v is None:
        return ""
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v


def module_list(v):
    if not v:
        return set()
    return {
        item.strip()
        for item in str(v).split(",")
        if item.strip()
    }


# =========================================================
# CARGA DE FUENTES
# =========================================================

models = load_json("ir_models.json")
fields = load_json("ir_model_fields.json")
installed_modules = load_json("installed_modules.json")
dependencies = load_json("module_dependencies.json")

connection = load_csv("1-id_conexion.csv")
all_tables = load_csv("2-inventario_tablas.csv")
selected_tables = load_csv("3-id_27_tablas_principales.csv")
sql_columns = load_csv("4-diccionario_columnas_sql.csv")
primary_keys = load_csv("5-claves_primarias_pk.csv")
foreign_keys = load_csv("6-claves_foraneas_fk.csv")
constraints = load_csv("7-restricciones_sql_check_unique_exclusion.csv")
unique_indexes = load_csv("8-indices_unicos.csv")


# =========================================================
# ALCANCE DE MÓDULOS
# =========================================================

functional_modules = {
    "product", "uom",
    "purchase", "purchase_stock", "purchase_mrp",
    "stock", "stock_account",
    "mrp", "mrp_account",
    "sale", "sale_management", "sale_stock", "sale_mrp",
    "product_expiry", "mrp_product_expiry",
    "sale_stock_product_expiry",
}

installed_by_id = {
    module["id"]: module["name"]
    for module in installed_modules
}

installed_names = set(installed_by_id.values())

dependency_graph = {
    name: set() for name in installed_names
}

dependencies_by_module = defaultdict(set)

for dep in dependencies:
    module_ref = dep.get("module_id")

    if not module_ref:
        continue

    parent = installed_by_id.get(module_ref[0])
    child = dep.get("name")

    if parent in installed_names and child in installed_names:
        dependency_graph[parent].add(child)
        dependencies_by_module[parent].add(child)

module_scope = set(functional_modules)
pending = list(functional_modules)

while pending:
    current = pending.pop()

    for dependency in dependency_graph.get(current, set()):
        if dependency not in module_scope:
            module_scope.add(dependency)
            pending.append(dependency)

technical_modules = module_scope - functional_modules


# =========================================================
# SELECCIÓN DE MODELOS
# =========================================================

core_models = {
    # Maestros
    "product.template",
    "product.product",
    "product.category",
    "product.supplierinfo",
    "product.pricelist",
    "product.pricelist.item",
    "uom.uom",
    "res.partner",
    "res.company",
    "res.users",

    # Compras
    "purchase.order",
    "purchase.order.line",

    # Inventario
    "stock.warehouse",
    "stock.location",
    "stock.picking.type",
    "stock.picking",
    "stock.move",
    "stock.move.line",
    "stock.quant",
    "stock.lot",
    "stock.route",
    "stock.rule",
    "stock.warehouse.orderpoint",
    "stock.scrap",
    "stock.return.picking",

    # Fabricación
    "mrp.bom",
    "mrp.bom.line",
    "mrp.bom.byproduct",
    "mrp.production",
    "mrp.workcenter",
    "mrp.routing.workcenter",
    "mrp.workorder",

    # Ventas
    "sale.order",
    "sale.order.line",
}

models_by_name = {
    model["model"]: model
    for model in models
}

missing = core_models - set(models_by_name)

if missing:
    raise ValueError(
        f"Faltan modelos principales en Odoo: {sorted(missing)}"
    )

core_models &= set(models_by_name)

core_fields = [
    f for f in fields
    if f.get("model") in core_models
]

related_models = set()

for field in core_fields:
    relation = field.get("relation")

    if relation and relation in models_by_name:
        if relation not in core_models:
            related_models.add(relation)

selected_models = core_models | related_models

related_fields = [
    f for f in fields
    if f.get("model") in related_models
]

selected_fields = core_fields + related_fields


# =========================================================
# PREPARACIÓN DEL LIBRO
# =========================================================

wb = Workbook()
wb.remove(wb.active)

wb.properties.title = "Inventario del esquema de Odoo"
wb.properties.subject = "Modelos ORM y esquema físico PostgreSQL"
wb.properties.creator = "TFG - Odoo Agentic AI"

if connection:
    wb.properties.description = (
        f"Base de datos: {connection[0].get('database', '')}. "
        f"Usuario: {connection[0].get('username', '')}. "
        f"Versión: {connection[0].get('postgres_version', '')}."
    )

header_fill = PatternFill(
    fill_type="solid",
    fgColor="263B5E"
)

header_font = Font(
    color="FFFFFF",
    bold=True
)


def add_sheet(name, headers, rows):
    ws = wb.create_sheet(name)

    ws.append(headers)

    for row in rows:
        ws.append([value(v) for v in row])

    ws.freeze_panes = "A2"
    ws.sheet_view.showGridLines = False

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True
        )

    ws.row_dimensions[1].height = 32

    if ws.max_row > 1:
        ws.auto_filter.ref = ws.dimensions

        # Tabla Excel con filtros y formato alterno.
        table_name = "T_" + name.replace("_", "")
        table = Table(
            displayName=table_name,
            ref=ws.dimensions
        )
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )
        ws.add_table(table)

    # Ajuste de anchos, limitado para evitar columnas enormes.
    for col_idx in range(1, ws.max_column + 1):
        letter = get_column_letter(col_idx)
        max_length = len(str(ws.cell(1, col_idx).value or ""))

        for row_idx in range(2, min(ws.max_row, 300) + 1):
            cell_value = ws.cell(row_idx, col_idx).value
            if cell_value is not None:
                max_length = max(
                    max_length,
                    min(len(str(cell_value)), 55)
                )

        ws.column_dimensions[letter].width = min(
            max(max_length + 2, 12),
            45
        )

    return ws


# =========================================================
# 01. MODELOS
# =========================================================

model_rows = []

for name in sorted(selected_models):
    model = models_by_name[name]
    modules = module_list(model.get("modules"))

    model_rows.append([
        model.get("id"),
        name,
        model.get("name"),
        model.get("modules"),
        "Principal" if name in core_models else "Relacionado directo",
        model.get("abstract"),
        model.get("transient"),
        bool(modules & functional_modules),
    ])

add_sheet(
    "01_Modelos",
    [
        "ID", "Modelo", "Descripción", "Módulos",
        "Nivel de selección", "Abstracto", "Transitorio",
        "Relacionado con módulos funcionales"
    ],
    model_rows
)


# =========================================================
# 02. CAMPOS
# =========================================================

field_rows = []

field_headers = [
    "ID", "Modelo", "Campo", "Etiqueta", "Tipo",
    "Obligatorio", "Solo lectura", "Almacenado",
    "Calculado", "Dependencias", "Relacionado",
    "Modelo relacionado", "Campo inverso",
    "Selección", "On delete", "Índice",
    "Módulos", "Tabla relación", "Columna 1",
    "Columna 2", "Ayuda", "Estado"
]

for f in sorted(
    selected_fields,
    key=lambda x: (x.get("model", ""), x.get("name", ""))
):
    field_rows.append([
        f.get("id"),
        f.get("model"),
        f.get("name"),
        f.get("field_description"),
        f.get("ttype"),
        f.get("required"),
        f.get("readonly"),
        f.get("store"),
        f.get("compute"),
        f.get("depends"),
        f.get("related"),
        f.get("relation"),
        f.get("relation_field"),
        f.get("selection"),
        f.get("on_delete"),
        f.get("index"),
        f.get("modules"),
        f.get("relation_table"),
        f.get("column1"),
        f.get("column2"),
        f.get("help"),
        f.get("state"),
    ])

add_sheet("02_Campos", field_headers, field_rows)


# =========================================================
# 03. RELACIONES ORM
# =========================================================

relational_types = {
    "many2one",
    "one2many",
    "many2many",
}

relation_rows = []

for f in sorted(
    selected_fields,
    key=lambda x: (x.get("model", ""), x.get("name", ""))
):
    if f.get("ttype") not in relational_types:
        continue

    relation_rows.append([
        f.get("model"),
        f.get("name"),
        f.get("field_description"),
        f.get("ttype"),
        f.get("relation"),
        f.get("relation_field"),
        f.get("relation_table"),
        f.get("column1"),
        f.get("column2"),
        f.get("required"),
        f.get("on_delete"),
        f.get("modules"),
    ])

add_sheet(
    "03_Relaciones",
    [
        "Modelo origen", "Campo", "Etiqueta", "Tipo relación",
        "Modelo destino", "Campo inverso", "Tabla intermedia",
        "Columna 1", "Columna 2", "Obligatorio",
        "On delete", "Módulos"
    ],
    relation_rows
)


# =========================================================
# 04. TABLAS Y COLUMNAS SQL
# =========================================================

pk_by_table = {
    (pk["table_name"], pk["column_name"])
    for pk in primary_keys
}

columns_by_table = defaultdict(list)

for col in sql_columns:
    columns_by_table[col["table_name"]].append(col)

selected_table_names = {
    row["table_name"]
    for row in selected_tables
}

sql_rows = []

for table in sorted(all_tables, key=lambda x: x["table_name"]):
    table_name = table["table_name"]
    is_selected = table_name in selected_table_names

    table_columns = columns_by_table.get(table_name, [])

    if not table_columns:
        sql_rows.append([
            table_name,
            table.get("table_type"),
            is_selected,
            "",
            "",
            "",
            "",
            "",
            ""
        ])
        continue

    for col in table_columns:
        sql_rows.append([
            table_name,
            table.get("table_type"),
            is_selected,
            col.get("ordinal_position"),
            col.get("column_name"),
            col.get("data_type"),
            col.get("udt_name"),
            col.get("is_nullable"),
            col.get("column_default"),
            (table_name, col.get("column_name")) in pk_by_table,
        ])

add_sheet(
    "04_Tablas_SQL",
    [
        "Tabla", "Tipo de tabla", "Incluida en selección SQL",
        "Posición", "Columna", "Tipo SQL", "Tipo interno",
        "Admite NULL", "Valor por defecto", "Es PK"
    ],
    sql_rows
)


# =========================================================
# 05. CLAVES FORÁNEAS
# =========================================================

fk_rows = []

for fk in sorted(
    foreign_keys,
    key=lambda x: (
        x["table_name"],
        x["constraint_name"],
        x["ordinal_position"]
    )
):
    fk_rows.append([
        fk.get("table_name"),
        fk.get("constraint_name"),
        fk.get("column_name"),
        fk.get("foreign_table_name"),
        fk.get("foreign_column_name"),
        fk.get("ordinal_position"),
        fk.get("update_rule"),
        fk.get("delete_rule"),
    ])

add_sheet(
    "05_Claves_Foraneas",
    [
        "Tabla origen", "Restricción", "Columna origen",
        "Tabla referenciada", "Columna referenciada",
        "Posición", "Regla UPDATE", "Regla DELETE"
    ],
    fk_rows
)


# =========================================================
# 06. RESTRICCIONES E ÍNDICES ÚNICOS
# =========================================================

constraint_rows = []

for c in sorted(
    constraints,
    key=lambda x: (
        x["table_name"],
        x["constraint_type"],
        x["constraint_name"]
    )
):
    constraint_rows.append([
        "Restricción",
        c.get("table_name"),
        c.get("constraint_name"),
        c.get("constraint_type"),
        c.get("definition"),
        "",
        ""
    ])

constraint_names = {
    c["constraint_name"]
    for c in constraints
}

for idx in sorted(
    unique_indexes,
    key=lambda x: (x["table_name"], x["index_name"])
):
    is_primary = idx.get("is_primary", "").lower() == "true"

    if is_primary:
        category = "Índice de clave primaria"
    elif idx["index_name"] in constraint_names:
        category = "Índice asociado a restricción"
    else:
        category = "Índice único independiente"

    constraint_rows.append([
        "Índice",
        idx.get("table_name"),
        idx.get("index_name"),
        category,
        idx.get("index_definition"),
        idx.get("is_primary"),
        idx.get("is_unique"),
    ])

add_sheet(
    "06_Restricciones",
    [
        "Tipo de objeto", "Tabla", "Nombre",
        "Tipo / categoría", "Definición",
        "Es PK", "Es único"
    ],
    constraint_rows
)


# =========================================================
# 07. MÓDULOS
# =========================================================

module_rows = []

for module in sorted(
    installed_modules,
    key=lambda x: x["name"]
):
    name = module["name"]

    if name in functional_modules:
        level = "Funcional"
    elif name in technical_modules:
        level = "Dependencia técnica"
    else:
        level = "Otro módulo instalado"

    module_rows.append([
        module.get("id"),
        name,
        module.get("shortdesc"),
        module.get("state"),
        module.get("demo"),
        level,
        ", ".join(sorted(dependencies_by_module.get(name, set()))),
    ])

add_sheet(
    "07_Modulos",
    [
        "ID", "Módulo técnico", "Descripción",
        "Estado", "Demo", "Clasificación",
        "Dependencias directas"
    ],
    module_rows
)


# =========================================================
# 08. MODELOS PRINCIPALES DEL TFG
# =========================================================

functional_rows = []

for name in sorted(core_models):
    model = models_by_name[name]

    functional_rows.append([
        model.get("id"),
        name,
        model.get("name"),
        model.get("modules"),
        model.get("abstract"),
        model.get("transient"),
    ])

add_sheet(
    "08_Modelos_TFG",
    [
        "ID", "Modelo", "Descripción", "Módulos",
        "Abstracto", "Transitorio"
    ],
    functional_rows
)


# =========================================================
# GUARDAR Y RESUMIR
# =========================================================

wb.save(OUTPUT)

print("\n========== LIBRO GENERADO ==========")
print(f"Archivo: {OUTPUT}")
print(f"Tamaño: {OUTPUT.stat().st_size:,} bytes")
print("\n========== RESUMEN ==========")

for ws in wb.worksheets:
    print(f"{ws.title:25} {ws.max_row - 1:6} registros")

print("\nGeneración completada.")
