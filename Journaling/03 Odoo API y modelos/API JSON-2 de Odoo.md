---
type: referencia
area: odoo
status: tested
project: TFG Odoo Agentic AI
tags:
  - odoo/api
  - integracion/autenticacion
---

# API JSON-2 de Odoo

## Decisión

Se decidió utilizar la API JSON-2 de Odoo 19 para que la integración acceda a modelos y métodos sin conectarse directamente a PostgreSQL.

## Endpoint

```text
/json/2/<modelo>/<método>
```

Ejemplo utilizado: `/json/2/purchase.order/search_read`.

## Autenticación mediante API Key

Se creó una API Key para el usuario de Odoo. La clave se mantuvo como secreto y no se incluyó en la documentación.

Durante la prueba se almacenó temporalmente en una variable de entorno:

```bash
export ODOO_API_KEY='...'
```

La petición utiliza la cabecera `Authorization: bearer $ODOO_API_KEY`.

Buenas prácticas:
- No pegar el valor real de la API Key en notas.
- No versionar secretos en Git.
- Evitar capturas de pantalla que muestren credenciales.
- Considerar un mecanismo persistente y seguro para la configuración local.

## Cabeceras de la prueba

- `Authorization: bearer $ODOO_API_KEY`
- `Content-Type: application/json`
- `X-Odoo-Database: Odoo-tfg`

## Responsabilidades y límites

La API es la puerta de entrada externa a Odoo. El ORM permanece dentro de Odoo y es quien interactúa con PostgreSQL. La API devuelve datos serializados, no objetos ORM directamente.

## Enlaces

- [[Primera consulta a la API JSON-2]]
- [[ORM de Odoo y PostgreSQL]]
- [[Modelos de compras - purchase.order]]
