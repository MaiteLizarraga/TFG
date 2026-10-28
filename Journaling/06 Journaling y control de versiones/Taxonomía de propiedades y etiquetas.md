---
type: reference
area: journaling
project: TFG Odoo Agentic AI
status: active
tags:
  - obsidian/taxonomia
  - documentacion/convenciones
---

# Taxonomía de propiedades y etiquetas

## Objetivo

Mantener una clasificación coherente de las notas del TFG sin duplicar información en las propiedades y las etiquetas.

## Propiedades

| Propiedad | Uso | Valores orientativos |
|---|---|---|
| `type` | Tipo de nota | `moc`, `concepto`, `procedimiento`, `decision-tecnica`, `incidencia`, `referencia`, `sesion`, `dashboard` |
| `area` | Ámbito principal | `proyecto`, `odoo`, `arquitectura`, `infraestructura`, `integracion`, `observabilidad`, `datos`, `journaling` |
| `project` | Proyecto al que pertenece | `TFG Odoo Agentic AI` |
| `status` | Estado, cuando sea útil | `active`, `draft`, `proposed`, `open`, `resolved`, `deprecated` |
| `tags` | Temas técnicos y relaciones transversales | Etiquetas jerárquicas descritas abajo |

No es necesario incluir todas las propiedades en todas las notas. Mantén los valores específicos que ya sean útiles para un flujo concreto, como `severity` en una incidencia.

## Etiquetas técnicas

Usa etiquetas jerárquicas con nombres breves y en minúsculas. La etiqueta completa incluye el prefijo de su familia.

| Familia | Etiquetas iniciales |
|---|---|
| Odoo | `odoo/api`, `odoo/orm`, `odoo/modelos`, `odoo/modulos` |
| Arquitectura | `arquitectura/multiagente`, `arquitectura/orquestacion`, `arquitectura/human-in-the-loop` |
| Infraestructura | `infraestructura/docker`, `infraestructura/postgresql`, `infraestructura/ubuntu` |
| Integración | `integracion/mcp`, `integracion/autenticacion`, `integracion/permisos` |
| Observabilidad | `observabilidad/trazas`, `observabilidad/langfuse` |
| Datos | `datos/sinteticos`, `datos/modelo-relacional` |
| Documentación | `documentacion/moc`, `documentacion/procedimiento`, `documentacion/decision-tecnica`, `documentacion/concepto`, `documentacion/incidencia` |

Esta lista es una base, no un catálogo cerrado. Añade etiquetas cuando aporten una forma útil de recuperar o relacionar notas; evita crear sinónimos para el mismo concepto.

## Reglas de uso

1. **`type` clasifica la nota**: por ejemplo, `type: moc`, `type: procedimiento` o `type: decision-tecnica`.
2. **`area` identifica su ámbito principal**: por ejemplo, `area: odoo` o `area: arquitectura`.
3. **`tags` describen el contenido técnico**: una nota sobre autenticación de la API puede llevar `odoo/api` e `integracion/autenticacion`.
4. No repitas automáticamente el tipo de nota como etiqueta si ya está representado por `type`. Usa `documentacion/*` solo cuando esa clasificación transversal sea útil.
5. Usa enlaces `[[...]]` y los MOC para representar relaciones entre notas; las etiquetas no sustituyen a los enlaces.
6. En notas existentes, normaliza las propiedades y etiquetas cuando las edites. No hace falta revisar todas las notas de golpe ni añadir etiquetas por obligación.

## Ejemplo

```yaml
---
type: procedimiento
area: odoo
project: TFG Odoo Agentic AI
status: active
tags:
  - odoo/api
  - integracion/autenticacion
  - integracion/permisos
---
```

## Relación con la bóveda

- [[MOC - Journaling y control de versiones]]
- [[Inicio - TFG Odoo Agentic AI]]
