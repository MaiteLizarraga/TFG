import json
from collections import Counter
from pathlib import Path

RAW = Path.home() / "odoo-tfg/data/odoo_schema_inventory/raw"


def load_json(filename):
    with (RAW / filename).open(encoding="utf-8") as f:
        return json.load(f)


modules_data = load_json("installed_modules.json")
dependencies = load_json("module_dependencies.json")
models = load_json("ir_models.json")
fields = load_json("ir_model_fields.json")

# Módulos instalados: ID -> nombre técnico
installed = {
    module["id"]: module["name"]
    for module in modules_data
}

installed_names = set(installed.values())

# Módulos funcionales que delimitan el alcance del TFG
roots = {
    "product",
    "uom",
    "purchase",
    "purchase_stock",
    "purchase_mrp",
    "stock",
    "stock_account",
    "mrp",
    "mrp_account",
    "sale",
    "sale_management",
    "sale_stock",
    "sale_mrp",
    "product_expiry",
    "mrp_product_expiry",
    "sale_stock_product_expiry",
}

missing = roots - installed_names

if missing:
    raise ValueError(
        f"Estos módulos funcionales no están instalados: {sorted(missing)}"
    )

# Grafo de dependencias: módulo -> dependencias
graph = {name: set() for name in installed_names}

for dependency in dependencies:
    module_ref = dependency.get("module_id")

    if not module_ref:
        continue

    parent = installed.get(module_ref[0])
    child = dependency.get("name")

    if parent in installed_names and child in installed_names:
        graph[parent].add(child)

# Cierre transitivo de dependencias
scope = set(roots)
pending = list(roots)

while pending:
    current = pending.pop()

    for dependency in graph.get(current, set()):
        if dependency not in scope:
            scope.add(dependency)
            pending.append(dependency)


def module_list(value):
    if not isinstance(value, str) or not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


# Modelos que pertenecen a alguno de los módulos del alcance
selected_models = [
    model for model in models
    if module_list(model.get("modules")) & scope
]

selected_model_names = {
    model["model"] for model in selected_models
}

# Campos aportados por módulos del alcance y pertenecientes
# a los modelos seleccionados
selected_fields = [
    field for field in fields
    if field.get("model") in selected_model_names
    and module_list(field.get("modules")) & scope
]

print("\n========== MÓDULOS ==========")
print(f"Módulos funcionales iniciales: {len(roots)}")
print(f"Módulos instalados incluidos en el alcance: {len(scope)}")

for name in sorted(scope):
    marker = " [INICIAL]" if name in roots else ""
    print(f"  {name}{marker}")

print("\n========== MODELOS ==========")
print(f"Modelos registrados en Odoo: {len(models)}")
print(f"Modelos dentro del alcance: {len(selected_models)}")
print(f"Modelos abstractos: {sum(m.get('abstract', False) for m in selected_models)}")
print(f"Modelos transitorios: {sum(m.get('transient', False) for m in selected_models)}")

print("\n========== CAMPOS ==========")
print(f"Campos registrados en Odoo: {len(fields)}")
print(f"Campos dentro del alcance: {len(selected_fields)}")

print("\n========== MODELOS POR MÓDULO ==========")
counter = Counter()

for model in selected_models:
    for module in module_list(model.get("modules")) & scope:
        counter[module] += 1

for module, count in sorted(counter.items()):
    print(f"{module:30} {count:4}")

print("\n========== MUESTRA DE MODELOS FUNCIONALES ==========")

keywords = (
    "product", "purchase", "stock", "mrp", "sale",
    "uom", "lot", "warehouse", "location", "picking",
    "move", "bom", "production"
)

for model in sorted(selected_models, key=lambda x: x["model"]):
    name = model["model"]

    if any(keyword in name for keyword in keywords):
        print(
            f"{name:45} "
            f"{model.get('modules', '')}"
        )
