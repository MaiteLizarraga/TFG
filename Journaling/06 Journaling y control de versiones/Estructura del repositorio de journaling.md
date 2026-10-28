---
type: referencia
area: journaling
project: TFG Odoo Agentic AI
status: active
tags:
  - git/estructura
  - obsidian/workflow
---

# Estructura del repositorio de journaling

## Estructura actual del vault

El vault de Obsidian está en `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`. La organización separa el conocimiento consolidado, el material provisional y la administración:

```text
TFG-Odoo-Agentic-AI/
├── Admin/                         # Excluido de Git mediante /Admin/
├── Journaling/                    # Conocimiento consolidado y estructurado
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
        ├── Octubre_2026/
        └── Septiembre_2026/
```

Las carpetas mensuales y sus contenidos evolucionan a medida que se procesa el diario.

## Función de cada zona

- **`Journaling/`**: conocimiento consolidado, organizado por áreas y enlazado mediante notas de Obsidian. Aquí se documentan conceptos, decisiones, procedimientos, incidencias y acuerdos duraderos.
- **`__WIP_to_journal/`**: notas diarias o material provisional pendiente de revisar y transformar en contenido estructurado. Se conserva en el repositorio remoto como parte del historial del proyecto.
- **`__WIP_to_journal/processed/`**: notas originales ya procesadas, que se mantienen como archivo de consulta y trazabilidad.
- **`Admin/`**: contenido administrativo que debe permanecer fuera de GitHub; se excluye con la regla `/Admin/` de `.gitignore`.

## Flujo de mantenimiento

1. Registrar la actividad diaria en `__WIP_to_journal/Octubre_2026/` (o en la carpeta del mes correspondiente), agrupando el trabajo por fecha.
2. Extraer del diario el conocimiento duradero y actualizar las notas temáticas adecuadas de `Journaling/`.
3. Cuando una nota diaria ya esté procesada, guardarla en `__WIP_to_journal/processed/<mes>/`.
4. Mantener los detalles de trabajo diario en la nota de esa fecha y evitar añadirlos a notas de fechas anteriores.
5. Revisar `git status` y el contenido preparado; confirmar los cambios con `git commit` y publicarlos con `git push origin main`.

## Documentación del vault

La información permanente sobre la estructura, el flujo de trabajo, las convenciones y las decisiones debe vivir en notas enlazadas dentro de `Journaling/`, no en README o LEEME creados para distribuir paquetes ZIP. Las instrucciones puntuales para importar un ZIP no forman parte del conocimiento duradero del proyecto.

- [[Taxonomía de propiedades y etiquetas]]
- [[Colaboración con ChatGPT mediante GitHub]]
- [[Configuración local de Git para el journaling]]
- [[GitHub como repositorio de seguimiento del TFG]]

## Historial de reorganización

Tras el primer `push`, las notas del diario se agruparon bajo `Journaling/` en lugar de aparecer directamente en la raíz del repositorio. Esta estructura describe el vault de conocimiento y seguimiento del proyecto; no debe confundirse con el entorno de ejecución de Odoo ni con un segundo vault.
