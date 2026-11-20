---
type: procedimiento
area: infraestructura
status: current-as-documented
project: TFG Odoo Agentic AI
tags:
  - infraestructura/docker
  - infraestructura/postgresql
---

# Docker y despliegue de Odoo

## Versiones documentadas

- Docker Engine: `29.8.1`
- Docker CLI: `29.8.1`
- containerd.io: `2.3.6`
- Docker Buildx: `0.37.1`
- Docker Compose plugin: `5.5.1`
- Git: `2.53.0`

La prueba inicial `docker run hello-world` funcionó correctamente.

## Servicios y versiones

El despliegue utiliza Docker Compose con dos servicios:

- Odoo: imagen `odoo:19.0`, contenedor `odoo-tfg`.
- PostgreSQL: imagen `postgres:17`, contenedor `odoo-tfg-db`.

El servicio `db` utiliza las variables `POSTGRES_DB`, `POSTGRES_USER` y `POSTGRES_PASSWORD`. El servicio `odoo` recibe `HOST`, `USER` y `PASSWORD`, y depende del servicio `db`.

## Volúmenes y puertos

Volúmenes principales:

```yaml
- ./data/postgres:/var/lib/postgresql/data
- ./data/odoo:/var/lib/odoo
- ./config:/etc/odoo
```

Puertos publicados:

```yaml
# Odoo
- "8069:8069"

# PostgreSQL
- "5432:5432"
```

La persistencia se mantiene en los directorios locales `./data/postgres` y `./data/odoo`; la configuración de Odoo se monta desde `./config`.

## Configuración de Odoo dentro del contenedor

El montaje `./config:/etc/odoo` oculta los archivos que ya existan en ese directorio dentro de la imagen. En este entorno, el servidor no arrancaba correctamente porque no encontraba la configuración esperada.

Para resolverlo, se creó el archivo `~/odoo-tfg/config/odoo.conf`:

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
```

Con esta configuración, Odoo pudo localizar los addons y su directorio de datos.

**Consideración:** un bind mount de Docker sobre un directorio del contenedor oculta el contenido preexistente de ese directorio, aunque no lo borra de la imagen.

## Consideraciones de seguridad

- La configuración de origen documenta credenciales de demostración sencillas. Antes de utilizar este despliegue fuera de un entorno local aislado, deben sustituirse por secretos adecuados y evitar almacenarlos en el repositorio.
- PostgreSQL aparece publicado en todas las interfaces (`0.0.0.0` y `[::]`). Para el uso local, conviene comprobar si basta con publicar el puerto en `127.0.0.1`, especialmente si DBeaver se ejecuta en la misma máquina virtual. No se debe cambiar la configuración sin comprobar antes el estado real del entorno.

## Enlaces

- [[Entorno Ubuntu-TFG]]
- [[PostgreSQL y DBeaver]]
- [[Instalación de los módulos funcionales]]
- [[Estado actual del entorno]]
- [[Registro de problemas técnicos]]
