---
type: incidencia
area: infraestructura
status: resolved
project: TFG Odoo Agentic AI
tags:
  - infraestructura/docker
  - documentacion/incidencia
---

# Incidencia — permisos del directorio de datos de Odoo

## Síntoma

Odoo fallaba al intentar acceder a `/var/lib/odoo/sessions`.

## Diagnóstico

El contenedor utilizaba:

- UID: `100`
- GID: `101`

El volumen afectado era `~/odoo-tfg/data/odoo`.

## Solución aplicada

```bash
sudo chown -R 100:101 ~/odoo-tfg/data/odoo
docker compose restart odoo
```

Tras el cambio, Odoo arrancó correctamente.

## Relacionado

- [[Configuración Docker Compose de Odoo]]
- [[Registro de problemas técnicos]]
