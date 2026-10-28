---
type: procedimiento
area: infraestructura
status: current-as-documented
project: TFG Odoo Agentic AI
tags:
  - infraestructura/docker
  - infraestructura/postgresql
---

# Configuración Docker Compose de Odoo

## Servicios y versiones

- Odoo: `odoo:19.0`
- Base de datos: `postgres:17`

## Configuración inicial documentada

El servicio `db` usa las variables `POSTGRES_DB`, `POSTGRES_USER` y `POSTGRES_PASSWORD`. El servicio `odoo` recibe `HOST`, `USER` y `PASSWORD`, y depende del servicio `db`.

Volúmenes principales:

```yaml
- ./data/postgres:/var/lib/postgresql/data
- ./data/odoo:/var/lib/odoo
- ./config:/etc/odoo
```

Puertos documentados:

```yaml
# Odoo
- "8069:8069"

# PostgreSQL
- "5432:5432"
```

## Consideraciones

- Montar `./config:/etc/odoo` oculta los archivos que ya existan en ese directorio dentro de la imagen.
- Para evitar el problema, se creó `config/odoo.conf`.
- El texto de origen documenta credenciales de demostración sencillas. Antes de usar este despliegue fuera de un entorno local aislado, hay que sustituirlas por secretos adecuados y evitar almacenarlas en el repositorio.

## Enlaces

- [[Configuración de Odoo dentro del contenedor]]
- [[Incidencia - permisos del directorio de datos de Odoo]]
- [[PostgreSQL y DBeaver]]
