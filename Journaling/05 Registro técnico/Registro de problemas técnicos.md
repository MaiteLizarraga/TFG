---
type: referencia
area: infraestructura
project: TFG Odoo Agentic AI
tags:
  - documentacion/incidencia
  - infraestructura/docker
  - odoo/api
---

# Registro de problemas técnicos

| Problema | Solución o estado | Nota |
|---|---|---|
| El volumen `./config:/etc/odoo` ocultaba la configuración original | Resuelto creando `config/odoo.conf` | [[Configuración de Odoo dentro del contenedor]] |
| Odoo no podía escribir en `/var/lib/odoo/sessions` | Resuelto ajustando propietario UID:GID | [[Incidencia - permisos del directorio de datos de Odoo]] |
| La instalación de módulos desde la UI quedó en estado inconsistente | Se optó por CLI con `--stop-after-init` | [[Instalación de los módulos funcionales]] |
| Solo se mostraba Discuss al entrar en Odoo | Se comprobó que los módulos sí estaban instalados | [[Instalación de los módulos funcionales]] |
| Había que verificar el estado de los módulos | Consulta a `ir_module_module` | [[Instalación de los módulos funcionales]] |
| Necesidad de probar el acceso API | API Key y JSON-2 | [[Primera consulta a la API JSON-2]] |
| Consultar líneas de un pedido | Modelo `purchase.order.line` y campo `order_id` | [[Relación entre pedido de compra y líneas]] |
| Inspeccionar PostgreSQL gráficamente | DBeaver instalado y conectado | [[PostgreSQL y DBeaver]] |
| DBeaver necesitaba acceder al puerto PostgreSQL | Se publicó `5432:5432` | Revisar exposición de red en [[Docker y Docker Compose]] |
| Snap exigió confirmar classic confinement | Instalación con `--classic` | Registrar detalles adicionales si vuelve a ser relevante |
