---
type: procedimiento
area: odoo
status: completed
project: TFG Odoo Agentic AI
tags:
  - odoo/modulos
  - infraestructura/docker
---

# Instalación de los módulos funcionales

## Estrategia

Los módulos se instalaron mediante el CLI de Odoo utilizando `--stop-after-init`, para evitar problemas con operaciones de módulos mientras el servidor web estaba ejecutándose.

## Comandos ejecutados

```bash
docker compose run --rm odoo odoo -d Odoo-tfg -i sale_management --stop-after-init
docker compose run --rm odoo odoo -d Odoo-tfg -i purchase --stop-after-init
docker compose run --rm odoo odoo -d Odoo-tfg -i stock --stop-after-init
docker compose run --rm odoo odoo -d Odoo-tfg -i mrp --stop-after-init
```

## Verificación

Se consultó `ir_module_module` y se confirmó el estado `installed` para:

- `sale_management`
- `purchase`
- `stock`
- `mrp`

La instalación de dependencias adicionales es normal y no amplía por sí sola el alcance funcional del TFG.

## Relacionado

- [[Odoo 19 Community como ERP del proyecto]]
- [[Registro de problemas técnicos]]
