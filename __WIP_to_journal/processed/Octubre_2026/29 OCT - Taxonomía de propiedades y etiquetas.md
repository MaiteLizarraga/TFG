---
type: journal
area: journaling
project: TFG Odoo Agentic AI
date: 2026-10-29
status: processed
tags:
  - obsidian
  - git/github
  - documentacion/convenciones
---

# 29 OCT — Taxonomía de propiedades, etiquetas y organización del vault

## Trabajo realizado

- Se definió la nota [[Taxonomía de propiedades y etiquetas]] para unificar las convenciones de clasificación de las notas.
- Se estableció la separación entre `type` (tipo de nota), `area` (ámbito principal) y `tags` (conceptos técnicos).
- Se definieron familias de etiquetas jerárquicas breves: `odoo/*`, `arquitectura/*`, `infraestructura/*`, `integracion/*`, `observabilidad/*`, `datos/*` y `documentacion/*`.
- Se actualizaron las plantillas de concepto, decisión técnica, incidencia, procedimiento y sesión de trabajo, además del dashboard inicial y los MOC pertinentes.
- Se revisó la organización de la documentación: el conocimiento permanente y las convenciones deben estar en notas enlazadas de `Journaling/`; los README/LEEME que solo explican cómo importar paquetes ZIP no aportan conocimiento duradero y se retiraron.
- Se aclaró el flujo de trabajo diario: registrar cada jornada en una nota propia, trasladar las notas ya procesadas a `__WIP_to_journal/processed/Octubre_2026/` y no añadir trabajo de una fecha nueva a la nota de un día anterior.
- Se acordó utilizar el término **vault** en la documentación en español, en lugar de «bóveda».

## Decisiones y criterios

- Las propiedades clasifican la nota y las etiquetas describen su contenido técnico; no se duplicará automáticamente el tipo de nota en las etiquetas.
- La normalización de las notas existentes será progresiva, al editarlas, sin hacer una migración masiva innecesaria.
- La documentación operativa duradera se mantiene en `Journaling/`; los detalles de una sesión se registran en la nota diaria correspondiente.

## Notas relacionadas

- [[Taxonomía de propiedades y etiquetas]]
- [[Estructura del repositorio de journaling]]
- [[Colaboración con ChatGPT mediante GitHub]]
