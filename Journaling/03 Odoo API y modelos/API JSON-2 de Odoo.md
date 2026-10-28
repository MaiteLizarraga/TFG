---
type: technology
status: tested
project: TFG Odoo Agentic AI
tags:
  - odoo
  - api
  - json
---

# API JSON-2 de Odoo

## Decisión

Se decidió utilizar la API JSON-2 de Odoo 19 para que la integración acceda a modelos y métodos sin conectarse directamente a PostgreSQL.

## Endpoint observado

```text
/json/2/<modelo>/<método>
```

Ejemplo utilizado:

```text
/json/2/purchase.order/search_read
```

## Cabeceras de la prueba

- `Authorization: bearer $ODOO_API_KEY`
- `Content-Type: application/json`
- `X-Odoo-Database: Odoo-tfg`

## Resultado verificado

La primera llamada real a `purchase.order/search_read` devolvió cinco pedidos con campos `id`, `name`, `partner_id` y `amount_total`.

## Límites y responsabilidad

La API es la puerta de entrada. El ORM permanece dentro de Odoo y es quien interactúa con PostgreSQL.

## Enlaces

- [[Autenticación mediante API Key]]
- [[Primera consulta a la API JSON-2]]
- [[Separación entre API, ORM y PostgreSQL]]
