import json
from pathlib import Path
from collections import Counter

RAW = Path.home() / "odoo-tfg/data/odoo_schema_inventory/raw"


def load_json(filename):
    with (RAW / filename).open(encoding="utf-8") as f:
        return json.load(f)


models = load_json("ir_models.json")
fields = load_json("ir_model_fields.json")
installed_modules = load_json("installed_modules.json")
dependencies = load_json("module_dependencies.json")

# ---------------------------------------------------------
# NIVEL 1. Módulos funcionales
# ---------------------------------------------------------

functional_modules = {
    "product", "uom",
    "purchase", "purchase_stock", "purchase_mrp",
    "stock", "stock_account",
    "mrp", "mrp_account",
    "sale", "sale_management", "sale_stock", "sale_mrp",
    "product_expiry", "mrp_product_expiry",
    "sale_stock_product_expiry",
}

# ---------------------------------------------------------
# NIVEL 2. Dependencias técnicas
# ---------------------------------------------------------

installed_by_id = {
    module["id"]: module["name"]
    for module in installed_modules
}

installed_names = set(installed_by_id.values())

dependency_graph = {
    name: set() for name in installed_names
}

for dependency in dependencies:
    module_ref = dependency.get("module_id")

    if not module_ref:
        continue

    parent = installed_by_id.get(module_ref[0])
    child = dependency.get("name")

    if parent in installed_names and child in installed_names:
        dependency_graph[parent].add(child)

module_scope = set(functional_modules)
pending = list(functional_modules)

while pending:
    current = pending.pop()

    for dependency in dependency_graph.get(current, set()):
        if dependency not in module_scope:
            module_scope.add(dependency)
            pending.append(dependency)

technical_dependencies = module_scope - functional_modules

# ---------------------------------------------------------
# NIVEL 3. Modelos operativos principales
# ---------------------------------------------------------

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

missing_core = core_models - set(models_by_name)

if missing_core:
    print("ADVERTENCIA: modelos principales no encontrados:")
    for name in sorted(missing_core):
        print(f"  {name}")

core_models &= set(models_by_name)

# ---------------------------------------------------------
# Campos completos de los modelos principales
# ---------------------------------------------------------

core_fields = [
    field for field in fields
    if field.get("model") in core_models
]

# ---------------------------------------------------------
# Modelos relacionados directamente con los principales
# ---------------------------------------------------------

related_models = set()

for field in core_fields:
    relation = field.get("relation")

    if relation and relation in models_by_name:
        if relation not in core_models:
            related_models.add(relation)

# No incluimos automáticamente relaciones de segundo nivel:
# así evitamos que el inventario vuelva a crecer sin control.

related_fields = [
    field for field in fields
    if field.get("model") in related_models
]

selected_models = core_models | related_models

# ---------------------------------------------------------
# Resumen
# ---------------------------------------------------------

print("\n========== NIVEL 1: MÓDULOS FUNCIONALES ==========")
print(f"Total: {len(functional_modules)}")

for name in sorted(functional_modules):
    print(f"  {name}")

print("\n========== NIVEL 2: DEPENDENCIAS TÉCNICAS ==========")
print(f"Total: {len(technical_dependencies)}")

for name in sorted(technical_dependencies):
    print(f"  {name}")

print("\n========== NIVEL 3: MODELOS ==========")
print(f"Modelos principales: {len(core_models)}")
print(f"Modelos relacionados directos: {len(related_models)}")
print(f"Total de modelos: {len(selected_models)}")

print("\n========== CAMPOS ==========")
print(f"Campos de modelos principales: {len(core_fields)}")
print(f"Campos de modelos relacionados: {len(related_fields)}")
print(f"Total de campos: {len(core_fields) + len(related_fields)}")

print("\n========== MODELOS PRINCIPALES ==========")

for name in sorted(core_models):
    model = models_by_name[name]
    print(
        f"{name:42} "
        f"abstract={model.get('abstract')} "
        f"transient={model.get('transient')}"
    )

print("\n========== MODELOS RELACIONADOS ==========")

for name in sorted(related_models):
    model = models_by_name[name]
    print(
        f"{name:42} "
        f"abstract={model.get('abstract')} "
        f"transient={model.get('transient')}"
    )

print("\n========== CAMPOS POR TIPO DE RELACIÓN ==========")

counter = Counter(
    field.get("ttype")
    for field in core_fields + related_fields
)

for field_type, count in sorted(counter.items()):
    print(f"{field_type:20} {count:5}")
