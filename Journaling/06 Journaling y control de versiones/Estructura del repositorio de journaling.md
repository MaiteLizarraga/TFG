---
type: reference
area: journaling-version-control
project: TFG Odoo Agentic AI
status: implemented
tags:
  - tfg
  - git
  - github
---

# Estructura del repositorio de journaling

## Estructura actual del vault

El vault de Obsidian está en `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`. La organización actual separa el contenido consolidado, el material provisional y la administración:

```text
TFG-Odoo-Agentic-AI/
├── Admin/                         # Excluido de Git mediante /Admin/
├── Journaling/                    # Contenido consolidado y estructurado
│   ├── 00 Inicio/
│   ├── 01 Proyecto y arquitectura/
│   ├── 02 Entorno e infraestructura/
│   ├── 03 Odoo API y modelos/
│   ├── 04 Integración agentic/
│   ├── 05 Registro técnico/
│   ├── 06 Journaling y control de versiones/
│   └── 90 Plantillas/
└── __WIP_to_journal/              # Notas provisionales; también se versionan
    ├── Octubre_2026/
    └── processed/
        └── Septiembre_2026/
```

La estructura es orientativa: las carpetas mensuales y los contenidos pueden evolucionar a medida que se procese el diario.

## Función de cada zona

- **`Journaling/`**: conocimiento consolidado, organizado por áreas y enlazado mediante notas de Obsidian.
- **`__WIP_to_journal/`**: notas diarias o material provisional pendiente de revisar y transformar en contenido estructurado. Se conserva en el repositorio remoto como parte del historial del proyecto.
- **`__WIP_to_journal/processed/`**: material original ya procesado, que se mantiene como archivo de consulta.
- **`Admin/`**: contenido administrativo que debe permanecer fuera de GitHub; se excluye con la regla `/Admin/` de `.gitignore`.

## Flujo de mantenimiento

1. Registrar el trabajo diario en `__WIP_to_journal/Octubre_2026/` (o en la carpeta mensual correspondiente).
2. Cuando convenga, revisar las notas provisionales y extraer decisiones, procedimientos y conocimiento duradero.
3. Incorporar ese conocimiento a las notas adecuadas de `Journaling/`, evitando duplicar sin necesidad el diario original.
4. Mantener en `processed/` el material de origen que ya se haya procesado.
5. Revisar `git status` y el contenido preparado; confirmar los cambios con `git commit` y publicarlos con `git push origin main`.

## Historial de reorganización

Tras el primer `push`, las notas del diario se agruparon bajo `Journaling/` en lugar de aparecer directamente en la raíz del repositorio. La estructura anterior describe el vault actual y no debe confundirse con el entorno de ejecución de Odoo ni con una segunda bóveda.

Relacionado: [[GitHub como repositorio de seguimiento del TFG]] y [[Configuración local de Git para el journaling]].
