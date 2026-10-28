---
type: referencia
area: infraestructura
status: active
project: TFG Odoo Agentic AI
tags:
  - infraestructura/ubuntu
  - infraestructura/virtualbox
---

# Entorno Ubuntu-TFG

## Máquina virtual

| Propiedad | Valor documentado |
|---|---|
| Nombre | `Ubuntu-TFG` |
| Sistema operativo | Ubuntu 26.04 LTS |
| Virtualización | VirtualBox 7.2.20 |
| Usuario | `maite` |
| Hostname | `ubuntu-tfg` |

## Separación respecto a otros trabajos

Existe otra máquina virtual, `Ubuntu-Kathara`, dedicada a otro laboratorio. Se decidió expresamente no modificarla.

## Ruta del proyecto

`/home/maite/odoo-tfg`

Estructura inicial:

```text
odoo-tfg/
├── compose.yaml
├── config/
└── data/
    ├── odoo/
    └── postgres/
```

La documentación del proyecto se mantiene separada del entorno de ejecución mediante Obsidian.

## Enlaces

- [[Docker y Docker Compose]]
- [[Estado actual del entorno]]
