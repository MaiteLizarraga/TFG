---
type: experiment
status: successful
project: TFG Odoo Agentic AI
tags:
  - odoo
  - api
  - experiment
---

# Primera consulta a la API JSON-2

## Objetivo

Comprobar de extremo a extremo la conexión entre `curl`, la API JSON-2, el ORM y PostgreSQL.

## Petición realizada

```bash
curl -X POST \
  http://localhost:8069/json/2/purchase.order/search_read \
  -H "Authorization: bearer $ODOO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Odoo-Database: Odoo-tfg" \
  -d '{
    "domain": [],
    "fields": ["id", "name", "partner_id", "amount_total"],
    "limit": 5
  }'
```

## Resultado

La petición respondió correctamente con cinco registros. Ejemplos del resultado documentado:

| ID | Pedido | Proveedor | Total |
|---:|---|---|---:|
| 11 | P00011 | Ready Mat | 6936.0 |
| 10 | P00010 | Azure Interior | 2505.0 |
| 9 | P00009 | Gemini Furniture | 12500.0 |
| 8 | P00008 | Wood Corner | 6465.5 |
| 7 | P00007 | Ready Mat | 1222.5 |

## Qué demuestra

```text
curl → Odoo JSON-2 API → método del modelo → ORM → PostgreSQL → JSON
```

La API de Odoo estaba operativa en el entorno del TFG en el momento de la prueba.

## Enlaces

- [[API JSON-2 de Odoo]]
- [[Autenticación mediante API Key]]
- [[Exploración de purchase.order]]
