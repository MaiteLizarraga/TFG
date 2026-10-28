---
type: concepto
area: odoo
status: configured
project: TFG Odoo Agentic AI
tags:
  - odoo/api
  - integracion/autenticacion
---

# Autenticación mediante API Key

Se creó una API Key para el usuario de Odoo. La clave se mantuvo como secreto y no se incluyó en la documentación.

Durante la prueba se almacenó temporalmente en una variable de entorno:

```bash
export ODOO_API_KEY='...'
```

## Buenas prácticas para la documentación

- No pegar el valor real de la API Key en notas.
- No versionar secretos en Git.
- Evitar capturas de pantalla que muestren credenciales.
- Considerar un mecanismo persistente y seguro para la configuración local.

## Enlace relacionado

- [[Primera consulta a la API JSON-2]]
