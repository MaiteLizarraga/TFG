---
type: referencia
area: odoo
project: TFG Odoo Agentic AI
status: active
tags:
  - odoo/modulos
  - datos/sinteticos
  - infraestructura/postgresql
---

# Dependencias de módulos Odoo y datos de negocio

## Objetivo

Para diseñar un generador de datos sintéticos coherentes para el escenario del TFG, hay que conocer tanto las dependencias entre módulos de Odoo como las relaciones entre las entidades de negocio. Son dos grafos distintos y complementarios.

## Dependencias directas comprobadas

En la instalación consultada, las dependencias directas de los cuatro módulos funcionales son:

| Módulo funcional | Módulo Odoo | Dependencias directas | Número |
|---|---|---|---:|
| Ventas | `sale_management` | `digest`, `sale` | 2 |
| Compras | `purchase` | `account` | 1 |
| Inventario | `stock` | `barcodes_gs1_nomenclature`, `digest`, `product` | 3 |
| Fabricación | `mrp` | `product`, `resource`, `stock` | 3 |

**Total: 9 relaciones de dependencia directa.** Este recuento corresponde a las dependencias directas identificadas en la instalación consultada; no representa el total de dependencias transitivas.

## Dos grafos diferentes

### 1. Grafo de dependencias de módulos

Representa las dependencias de software declaradas por los módulos. Por ejemplo:

```text
mrp → stock → product
```

La consulta recursiva permite recorrer las dependencias transitivas de los cuatro módulos raíz (`sale_management`, `purchase`, `stock` y `mrp`) y registrar la ruta seguida.

### 2. Grafo de dependencias de datos de negocio

Representa las entidades y relaciones que deben existir para que los registros sean coherentes. Por ejemplo, en fabricación hay que estudiar la relación entre órdenes de fabricación, productos, listas de materiales y sus líneas:

```text
mrp.production
    ├── product
    └── mrp.bom
          └── mrp.bom.line
```

Modelos relevantes que se deben estudiar para el escenario:

- `res.partner`
- `product.template`
- `product.product`
- `purchase.order`
- `purchase.order.line`
- `stock.picking`
- `stock.move`
- `stock.quant`
- `mrp.bom`
- `mrp.bom.line`
- `mrp.production`
- `sale.order`
- `sale.order.line`

Para generar datos sintéticos, conocer las dependencias de negocio y el orden de creación de los registros es tan importante como conocer las dependencias de módulos.

## Consulta exploratoria de PostgreSQL

Se comprobó la estructura de las tablas `ir_module_module` e `ir_module_module_dependency` mediante `information_schema.columns`. La consulta devolvió 35 filas de columnas en total para ambas tablas.

Comando empleado:

```bash
docker exec -it odoo-tfg-db psql -U odoo -d Odoo-tfg -c "
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name IN ('ir_module_module', 'ir_module_module_dependency')
ORDER BY table_name, ordinal_position;
"
```

Para obtener el grafo completo se utilizó una CTE recursiva que parte de los cuatro módulos raíz, sigue las dependencias transitivas y evita ciclos comprobando si el siguiente módulo ya aparece en la ruta:

```sql
WITH RECURSIVE deps AS (
    SELECT
        m.name AS root,
        d.name AS dependency,
        1 AS level,
        ARRAY[m.name, d.name]::text[] AS path
    FROM ir_module_module m
    JOIN ir_module_module_dependency d
        ON d.module_id = m.id
    WHERE m.name IN ('sale_management', 'purchase', 'stock', 'mrp')

    UNION ALL

    SELECT
        deps.root,
        d2.name AS dependency,
        deps.level + 1 AS level,
        deps.path || d2.name AS path
    FROM deps
    JOIN ir_module_module m2
        ON m2.name = deps.dependency
    JOIN ir_module_module_dependency d2
        ON d2.module_id = m2.id
    WHERE NOT d2.name = ANY(deps.path)
)
SELECT
    root,
    dependency,
    level,
    array_to_string(path, ' -> ') AS path
FROM deps
ORDER BY root, level, dependency;
```

En la sesión original, la salida se redirigió a `~/odoo-tfg/grafo-modulos-completo.csv` usando `psql --csv`.

## Implicaciones para el TFG

1. Identificar primero las dependencias de módulos para entender qué componentes intervienen en la instalación.
2. Estudiar después los modelos y relaciones de negocio que necesita el escenario.
3. Diseñar el generador de datos sintéticos teniendo en cuenta las relaciones y el orden de creación de los registros.
4. Tratar la consulta directa a PostgreSQL como una técnica de inspección del entorno, **no como el mecanismo de acceso de los agentes**. En la arquitectura del TFG, los agentes acceden a Odoo mediante herramientas semánticas y la API; no consultan ni modifican directamente la base de datos.

## Estado

Las dependencias directas y el esquema de consulta recursiva están documentados. La extracción completa del grafo y el análisis detallado de las relaciones entre modelos son pasos diferenciados; los ejemplos de modelos de esta nota constituyen el ámbito inicial de estudio, no una especificación exhaustiva de todas sus relaciones.


## Inventario y clasificación de módulos instalados (Odoo 19.0)

### Contexto de la comprobación

El 30 de octubre de 2026 se consultó el registro de módulos de la base de datos `Odoo-tfg` mediante el ORM de Odoo:

```python
modules = env['ir.module.module'].search([('state', '=', 'installed')])
for module in modules:
    print(f"{module.name}: {module.shortdesc}")
```

La consulta devolvió los módulos que se enumeran a continuación. La clasificación que sigue es **funcional y orientativa**: describe el papel de cada módulo en la instalación, pero no demuestra por sí sola si fue instalado manualmente, como dependencia directa o como dependencia transitiva. Para determinar esas relaciones hay que consultar `dependencies_id` o los manifiestos de los módulos.

### 1. Módulos funcionales principales del TFG

Son los cuatro módulos seleccionados para representar los procesos de negocio dentro del alcance del proyecto:

| Módulo técnico | Nombre | Función |
|---|---|---|
| `sale_management` | Sales | Gestión comercial: presupuestos, pedidos de venta, clientes y seguimiento comercial. |
| `purchase` | Purchase | Gestión de compras: pedidos a proveedores, confirmaciones y seguimiento de aprovisionamientos. |
| `stock` | Inventory | Gestión de almacenes, ubicaciones, existencias, movimientos, transferencias, recepciones y entregas. |
| `mrp` | Manufacturing | Gestión de fabricación: listas de materiales (BoM), órdenes de fabricación, componentes y operaciones productivas. |

### 2. Integración entre procesos

Conectan procesos de negocio y permiten que las operaciones de un área desencadenen o acompañen operaciones en otras áreas:

| Módulo técnico | Nombre | Función |
|---|---|---|
| `purchase_stock` | Purchase Stock | Integra Compras e Inventario, vinculando pedidos de compra con recepciones y movimientos de stock. |
| `sale_stock` | Sales and Warehouse Management | Integra Ventas e Inventario, vinculando pedidos de venta con necesidades de entrega y movimientos de stock. |
| `purchase_mrp` | Purchase and MRP Management | Relaciona aprovisionamiento y fabricación. |
| `sale_mrp` | Sales and MRP Management | Relaciona pedidos de venta y necesidades de fabricación. |
| `sale_purchase` | Sale Purchase | Conecta operaciones comerciales con procesos de compra. |
| `sale_purchase_stock` | MTO Sale ↔ Purchase | Integra flujos Make To Order (MTO) entre Ventas, Compras e Inventario. |
| `stock_account` | WMS Accounting | Integra Inventario y Contabilidad, incluyendo la valoración de existencias y sus efectos contables. |
| `mrp_account` | Accounting - MRP | Integra Fabricación y Contabilidad. |

### 3. Contabilidad y gestión financiera

| Módulo técnico | Nombre | Función |
|---|---|---|
| `account` | Invoicing | Contabilidad y facturación: facturas, asientos, diarios, cuentas y conciliación. |
| `account_payment` | Payment - Account | Gestión de pagos integrada con documentos contables. |
| `account_edi_ubl_cii` | Import/Export electronic invoices with UBL/CII | Intercambio de facturas electrónicas mediante UBL y CII. |
| `account_add_gln` | Add Partner GLN | Añade identificadores GLN a contactos para identificar empresas o ubicaciones en intercambios comerciales. |
| `analytic` | Analytic Accounting | Imputación analítica de costes e ingresos a proyectos, departamentos u otras dimensiones. |
| `l10n_us` | United States - Localizations | Componentes de localización para Estados Unidos. |
| `l10n_us_account` | United States - Accounting | Configuración contable específica de Estados Unidos. |

**Punto pendiente:** la presencia de `l10n_us` y `l10n_us_account` indica que hay componentes de localización estadounidense instalados. Si el escenario del TFG representa una empresa española, conviene comprobar la localización de la compañía y el motivo de esta instalación antes de modificarla.

### 4. Productos, unidades de medida y recursos

| Módulo técnico | Nombre | Función |
|---|---|---|
| `product` | Products & Pricelists | Productos, variantes, categorías, referencias, precios y listas de precios. |
| `uom` | Units of measure | Unidades de medida y conversiones, por ejemplo entre cajas y unidades. |
| `resource` | Resource | Recursos y calendarios de disponibilidad utilizados por distintas aplicaciones, incluida la planificación. |
| `resource_mail` | Resource Mail | Integración de recursos con funcionalidades de comunicación y seguimiento. |
| `sales_team` | Sales Teams | Organización de equipos y actividad comercial. |

### 5. Comunicación y colaboración

| Módulo técnico | Nombre | Función |
|---|---|---|
| `mail` | Discuss | Mensajería, conversaciones, notificaciones, actividades y seguimiento de registros mediante el chatter. |
| `mail_bot` | OdooBot | Bot integrado de Odoo para asistencia y notificaciones. |
| `sms` | SMS gateway | Infraestructura para envío y gestión de SMS. |
| `sale_sms` | Sale - SMS | Integración de SMS con procesos comerciales. |
| `stock_sms` | Stock - SMS | Integración de notificaciones SMS con operaciones de inventario. |
| `digest` | KPI Digests | Resúmenes periódicos de indicadores y actividad. |
| `google_gmail` | Google Gmail | Integración con Gmail. |
| `microsoft_outlook` | Microsoft Outlook | Integración con Microsoft Outlook. |
| `snailmail` | Snail Mail | Servicio de envío de correspondencia postal física desde Odoo. |
| `snailmail_account` | Snail Mail - Account | Integración del servicio postal con facturación y contabilidad. |

### 6. Seguridad, autenticación y usuarios

| Módulo técnico | Nombre | Función |
|---|---|---|
| `auth_signup` | Signup | Registro de usuarios e invitaciones para crear cuentas. |
| `auth_totp` | Two-Factor Authentication (TOTP) | Autenticación multifactor mediante códigos temporales. |
| `auth_totp_mail` | 2FA Invite mail | Integración de invitaciones por correo con la autenticación TOTP. |
| `auth_totp_portal` | TOTPortal | Extiende TOTP al portal de usuarios. |
| `auth_passkey` | Passkeys | Autenticación mediante passkeys y mecanismos como WebAuthn. |
| `auth_passkey_portal` | Passkeys Portal | Soporte de passkeys en el portal. |
| `portal` | Customer Portal | Acceso limitado de clientes y usuarios externos a documentos e información. |
| `privacy_lookup` | Privacy | Funcionalidades de búsqueda y gestión de información personal relacionadas con privacidad. |

### 7. Núcleo, interfaz, comunicación remota y servicios técnicos

| Módulo técnico | Nombre | Función |
|---|---|---|
| `base` | Base | Núcleo del ERP: ORM, modelos fundamentales, usuarios, permisos y configuración básica. |
| `web` | Web | Cliente e interfaz web de Odoo, vistas y navegación. |
| `http_routing` | Web Routing | Enrutamiento de peticiones HTTP. |
| `rpc` | RPC endpoints | Infraestructura para llamadas remotas (Remote Procedure Call). |
| `api_doc` | API Documentation | Módulo de documentación de API presente en esta instalación; su procedencia y alcance concreto quedan pendientes de verificar. |
| `bus` | IM Bus | Comunicación en tiempo real entre servidor y clientes, utilizada para notificaciones y actualizaciones. |
| `html_editor` | HTML Editor | Edición de contenido HTML utilizada por componentes de Odoo. |
| `web_tour` | Tours | Recorridos guiados e instrucciones interactivas en la interfaz. |
| `web_unsplash` | Unsplash Image Library | Integración con la biblioteca de imágenes Unsplash. |
| `base_setup` | Initial Setup Tools | Herramientas de configuración inicial. |
| `onboarding` | Onboarding Toolbox | Herramientas de incorporación y orientación inicial. |
| `base_import` | Base import | Importación de datos desde archivos, por ejemplo CSV o Excel. |
| `base_import_module` | Base import module | Importación de módulos de Odoo mediante archivos ZIP. |
| `base_install_request` | Base - Module Install Request | Gestión de solicitudes de instalación de módulos desde determinados flujos de Odoo. |

### 8. Códigos de barras y logística

| Módulo técnico | Nombre | Función |
|---|---|---|
| `barcodes` | Barcode | Identificación de productos y operaciones de almacén mediante códigos de barras. |
| `barcodes_gs1_nomenclature` | Barcode - GS1 Nomenclature | Interpretación de nomenclaturas y formatos GS1. |

### 9. Intercambio electrónico de documentos comerciales

| Módulo técnico | Nombre | Función |
|---|---|---|
| `purchase_edi_ubl_bis3` | Import/Export electronic orders with UBL | Intercambio de pedidos de compra mediante UBL y especificaciones Peppol BIS. |
| `sale_edi_ubl` | Import electronic orders with UBL | Gestión de pedidos electrónicos de venta mediante UBL. |

### 10. Servicios externos y funcionalidades adicionales

| Módulo técnico | Nombre | Función |
|---|---|---|
| `iap` | In-App Purchases | Infraestructura para servicios externos de Odoo que pueden requerir créditos o consumo. |
| `iap_mail` | IAP / Mail | Integración de servicios IAP con funcionalidades de correo. |
| `partner_autocomplete` | Partner Autocomplete | Facilita la creación de contactos mediante búsqueda y recuperación de información empresarial. |
| `payment` | Payment Engine | Infraestructura para proveedores y transacciones de pago electrónico. |
| `spreadsheet` | Spreadsheet | Hojas de cálculo integradas en Odoo. |
| `spreadsheet_account` | Spreadsheet Accounting Formulas | Fórmulas de hojas de cálculo relacionadas con contabilidad. |
| `spreadsheet_dashboard` | Spreadsheet dashboard | Infraestructura para dashboards basados en hojas de cálculo. |
| `spreadsheet_dashboard_account` | Spreadsheet dashboard for accounting | Dashboards de información contable. |
| `spreadsheet_dashboard_sale` | Spreadsheet dashboard for sales | Dashboards de información comercial. |
| `spreadsheet_dashboard_stock_account` | Spreadsheet dashboard for stock | Dashboards de inventario y valoración de existencias. |
| `utm` | UTM Trackers | Seguimiento de campañas y canales de captación mediante parámetros UTM. |

### Lectura de la instalación para el TFG

La clasificación permite separar:

1. **Procesos funcionales principales:** Compras, Inventario, Fabricación y Ventas.
2. **Integración funcional:** módulos que conectan esos procesos y permiten flujos transversales.
3. **Soporte funcional:** contabilidad, productos, unidades de medida, recursos y comunicación.
4. **Infraestructura técnica:** núcleo, ORM, interfaz, enrutamiento, RPC, autenticación y servicios internos.
5. **Funcionalidades adicionales:** códigos de barras, EDI, hojas de cálculo, integraciones externas y otros servicios.

La presencia de numerosos módulos instalados no significa que todos formen parte del alcance funcional del TFG ni que se hayan instalado manualmente. Los cuatro módulos funcionales principales siguen siendo `sale_management`, `purchase`, `stock` y `mrp`.

### Relevancia para la arquitectura agentic

- Los agentes operan sobre los procesos de negocio de Compras, Inventario, Fabricación y Ventas.
- Las integraciones entre módulos explican por qué una operación puede producir efectos en varias áreas del ERP.
- `base` proporciona el núcleo y el ORM sobre el que se apoyan los modelos de negocio.
- `rpc` y `api_doc` no deben confundirse con la API JSON-2 concreta que se utilizará para la integración. La presencia de estos módulos no demuestra por sí sola qué endpoints están habilitados ni los permisos del usuario de integración.
- La inspección directa de PostgreSQL puede servir para analizar el entorno, pero no constituye el mecanismo de acceso de los agentes. En la arquitectura del TFG, los agentes acceden a Odoo mediante herramientas semánticas y la API, sin consultar ni modificar directamente la base de datos.

### Verificaciones pendientes

- Consultar `dependencies_id` para obtener las dependencias declaradas de todos los módulos instalados y distinguir dependencias directas y transitivas.
- Verificar el origen y alcance del módulo `api_doc`.
- Revisar la localización estadounidense (`l10n_us`, `l10n_us_account`) y la configuración de país de la compañía.
