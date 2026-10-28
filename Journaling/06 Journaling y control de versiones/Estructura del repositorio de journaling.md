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

## Reorganización

Tras el primer `push`, se decidió agrupar las carpetas mensuales bajo `Journaling`, evitando que aparecieran directamente en la raíz del repositorio.

Estructura inicial:

```text
TFG/
└── Septiembre_2026/
```

Estructura reorganizada:

```text
TFG/
└── Journaling/
    └── Septiembre_2026/
        └── Reto 1 - 27, 28 y 29 septiembre 2026.md
```

La reorganización se realizó con:

```bash
mkdir Journaling
mv Septiembre_2026 Journaling/
```

Como el primer commit ya estaba publicado, el cambio se registró en un nuevo commit, sin reescribir el commit anterior.

## Estado documentado

El Vault local de Obsidian es `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`. El repositorio remoto es `MaiteLizarraga/TFG`, privado, y la rama principal es `main`.

La estructura anterior describe la organización del repositorio GitHub después de la reorganización. No debe confundirse automáticamente con la estructura de la bóveda de conocimiento Obsidian generada para documentar la arquitectura del TFG.

Relacionado: [[GitHub como repositorio de seguimiento del TFG]].
