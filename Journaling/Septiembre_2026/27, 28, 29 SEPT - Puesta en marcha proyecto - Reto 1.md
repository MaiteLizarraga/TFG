## Puesta en marcha de Odoo 19 + Agentic AI

> **Periodo documentado:** septiembre de 2026  
> **Objetivo de esta fase:** preparar el entorno técnico del TFG, desplegar Odoo 19 Community con datos de demostración, comprender su arquitectura interna y comenzar el acceso mediante su API JSON-2.

---

# 1. Contexto y decisiones arquitectónicas previas

## Objetivo del TFG

El proyecto consiste en desarrollar un sistema de **Agentic AI para la gestión de incidencias de Supply Chain**, utilizando un ERP realista como sistema de información empresarial.

La decisión tomada es utilizar:

**Odoo 19 Community**

como ERP del proyecto.

El sistema agentic no sustituirá al ERP ni accederá directamente a su base de datos. Odoo seguirá siendo el sistema que mantiene los datos y aplica su lógica de negocio.

### Áreas funcionales deliberadamente seleccionadas

Se han definido únicamente cuatro módulos funcionales de Odoo:

1. **Sales / Ventas** — `sale_management`
    
2. **Purchase / Compras** — `purchase`
    
3. **Inventory / Inventario** — `stock`
    
4. **Manufacturing / Fabricación** — `mrp`
    

Durante la instalación Odoo incorpora automáticamente otros módulos como dependencias técnicas. Estos no se consideran módulos funcionales adicionales del proyecto.

---

# 2. Arquitectura conceptual definida

La arquitectura del sistema se ha ido concretando como:

```text
                    ┌─────────────────────┐
                    │      ODOO 19        │
                    │      Community      │
                    └──────────┬──────────┘
                               │
                         JSON-2 API
                               │
                               ▼
                             ORM
                               │
                               ▼
                         PostgreSQL
```

Y, posteriormente, la arquitectura agentic será:

```text
                         HUMAN
                           │
                           ▼
                         ODOO
                           │
                    Automation Rule
                           │
                         Webhook
                           │
                           ▼
                  FastAPI / LangGraph
                           │
                    Orchestrator
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    Purchase Agent   Inventory Agent   Manufacturing Agent
          │                │                │
          └────────────────┼────────────────┘
                           │
                         MCP
                           │
                     Odoo JSON-2 API
                           │
                          ORM
                           │
                      PostgreSQL
```

También existirá un **Sales Agent**.

### Decisiones importantes

- No habrá un **Software Engineer Agent**.
    
- No habrá un **QA Agent**.
    
- El **FDE es un rol humano**, no un agente.
    
- Los agentes no accederán directamente a PostgreSQL.
    
- Los agentes utilizarán herramientas semánticas mediante MCP.
    
- MCP actuará como una capa controlada entre los agentes y la API de Odoo.
    
- Odoo continuará siendo responsable del ORM, permisos y lógica de negocio.
    
- No se crearán módulos Python ad-hoc dentro de Odoo para resolver la integración.
    
- Se prioriza la mantenibilidad y la separación de responsabilidades.
    
- La observabilidad será un elemento de primera clase.
    

---

# 3. Preparación del entorno — Ubuntu-TFG

## Máquina virtual

Se creó/utilizó una máquina virtual independiente:

```text
Ubuntu-TFG
```

con:

```text
Ubuntu 26.04 LTS
VirtualBox 7.2.20
usuario: maite
hostname: ubuntu-tfg
```

### Restricción importante

Existe otra VM:

```text
Ubuntu-Kathara
```

que pertenece a otro trabajo/laboratorio.

Se decidió expresamente **no tocar Ubuntu-Kathara**.

Todo el entorno del TFG se está montando en:

```text
Ubuntu-TFG
```

---

# 4. Docker

## Instalación

Se configuró el repositorio oficial de Docker para Ubuntu 26.04 (`resolute`).

Versiones comprobadas:

```text
Docker Engine 29.8.1
Docker CLI 29.8.1
containerd.io 2.3.6
Docker Buildx 0.37.1
Docker Compose plugin 5.5.1
```

También se instaló Git:

```text
Git 2.53.0
```

Configuración de nombre Git:

```text
Maite Lizarraga
```

## Prueba inicial

Se ejecutó:

```bash
docker run hello-world
```

y funcionó correctamente.

Esto confirmó que Docker estaba operativo antes de comenzar con Odoo.

---

# 5. Estructura inicial del proyecto

Se creó:

```text
~/odoo-tfg/
```

con:

```text
odoo-tfg/
├── compose.yaml
├── config/
└── data/
    ├── odoo/
    └── postgres/
```

La estructura tiene una separación clara:

- `compose.yaml` → infraestructura Docker.
    
- `config/` → configuración de Odoo.
    
- `data/odoo/` → datos persistentes de Odoo.
    
- `data/postgres/` → datos persistentes de PostgreSQL.
    

Más adelante se ha decidido mantener la documentación del proyecto separada mediante Obsidian.

---

# 6. Docker Compose para Odoo

Se creó inicialmente el siguiente entorno:

```yaml
services:

  db:
    image: postgres:17
    container_name: odoo-tfg-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - ./data/postgres:/var/lib/postgresql/data

  odoo:
    image: odoo:19.0
    container_name: odoo-tfg
    restart: unless-stopped
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - ./data/odoo:/var/lib/odoo
      - ./config:/etc/odoo
```

Se utilizaron:

```text
odoo:19.0
postgres:17
```

La elección fue mantener versiones actuales y compatibles con Odoo 19.

---

# 7. Primer problema: configuración de Odoo

## Problema

Al montar:

```text
./config:/etc/odoo
```

se estaba ocultando la configuración que venía originalmente en la imagen de Odoo.

Odoo no arrancaba correctamente porque el directorio de configuración del contenedor había quedado enmascarado por el volumen.

## Solución

Se creó:

```text
~/odoo-tfg/config/odoo.conf
```

con:

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons
data_dir = /var/lib/odoo
```

Esto permitió a Odoo encontrar correctamente sus addons y su directorio de datos.

---

# 8. Segundo problema: permisos de `/var/lib/odoo`

## Problema

Después de resolver la configuración, Odoo falló al intentar acceder a:

```text
/var/lib/odoo/sessions
```

El problema era de permisos sobre el volumen:

```text
~/odoo-tfg/data/odoo
```

## Diagnóstico

Se comprobó que el usuario dentro del contenedor utilizaba:

```text
uid=100
gid=101
```

correspondientes al usuario/grupo de Odoo.

## Solución

Se ejecutó:

```bash
sudo chown -R 100:101 ~/odoo-tfg/data/odoo
```

y después:

```bash
docker compose restart odoo
```

Odoo arrancó correctamente.

---

# 9. Creación de la base de datos Odoo

Una vez funcionando Odoo se accedió mediante:

```text
http://localhost:8069
```

y se creó la base de datos:

```text
Odoo-tfg
```

Esta es actualmente la base de datos principal utilizada por el proyecto.

---

# 10. Instalación de los módulos funcionales

La instalación de módulos se realizó deliberadamente mediante el CLI de Odoo utilizando:

```text
--stop-after-init
```

Esto permitió evitar problemas relacionados con operaciones de módulos mientras el servidor web estaba ejecutándose.

---

# 11. Instalación de Sales

Se ejecutó:

```bash
docker compose run --rm odoo odoo -d Odoo-tfg -i sale_management --stop-after-init
```

## Resultado

Se instalaron correctamente:

```text
sale
sale_edi_ubl
sale_management
sale_sms
spreadsheet_dashboard_sale
sale_pdf_quote_builder
```

Los módulos adicionales son dependencias/integraciones de Odoo.

El módulo funcional relevante para el proyecto es:

```text
sale_management
```

---

# 12. Instalación de Purchase

Se ejecutó:

```bash
docker compose run --rm odoo odoo -d Odoo-tfg -i purchase --stop-after-init
```

## Resultado

Se instaló correctamente:

```text
purchase
purchase_edi_ubl_bis3
sale_purchase
```

El módulo funcional relevante es:

```text
purchase
```

---

# 13. Instalación de Inventory

Se ejecutó:

```bash
docker compose run --rm odoo odoo -d Odoo-tfg -i stock --stop-after-init
```

## Resultado

Se instalaron correctamente:

```text
stock
barcodes
barcodes_gs1_nomenclature
stock_account
stock_sms
purchase_stock
spreadsheet_dashboard_stock_account
sale_stock
sale_purchase_stock
```

El módulo funcional relevante es:

```text
stock
```

Los demás son dependencias o integraciones.

---

# 14. Instalación de Manufacturing

Se ejecutó:

```bash
docker compose run --rm odoo odoo -d Odoo-tfg -i mrp --stop-after-init
```

## Resultado

La instalación terminó correctamente.

Entre los módulos cargados estaban:

```text
mrp
mrp_account
purchase_mrp
sale_mrp
```

Odoo informó:

```text
Odoo version: 19.0-20260926
74 modules loaded
```

No hubo errores durante esta instalación.

El módulo funcional relevante es:

```text
mrp
```

---

# 15. Verificación de los cuatro módulos

Para verificar que los cuatro módulos principales estaban realmente instalados se consultó directamente PostgreSQL mediante `psql`:

```bash
docker exec -it odoo-tfg-db psql -U odoo -d Odoo-tfg -c "
SELECT name, state
FROM ir_module_module
WHERE name IN ('sale_management', 'purchase', 'stock', 'mrp')
ORDER BY name;
"
```

Resultado:

```text
      name       |   state
-----------------+-----------
 mrp             | installed
 purchase        | installed
 sale_management | installed
 stock           | installed
(4 rows)
```

Esto confirmó definitivamente que los cuatro módulos funcionales estaban instalados.

---

# 16. Problema con la interfaz inicial de Odoo

Al acceder a Odoo inicialmente se mostraba:

```text
Discuss
```

Esto produjo cierta confusión porque parecía que no estaban disponibles los módulos instalados.

## Resolución

Se comprobó que simplemente se estaba mostrando la aplicación Discuss.

Los cuatro módulos sí estaban instalados y posteriormente fueron visibles desde la interfaz:

- Sales
    
- Purchase
    
- Inventory
    
- Manufacturing
    

No fue necesario reinstalar nada.

---

# 17. Datos de demostración

Durante la configuración se activó la opción para cargar datos de demostración.

Esto permitió disponer de pedidos, proveedores, productos y otros registros de ejemplo.

En Purchase aparecieron pedidos como:

```text
P00001
P00002
...
P00011
```

con proveedores como:

```text
Wood Corner
Gemini Furniture
Azure Interior
Ready Mat
My Company (San Francisco)
```

Estos datos son especialmente útiles para las primeras pruebas de la API y posteriormente para construir escenarios de incidencias.

---

# 18. Developer Mode

Se activó el modo desarrollador normal de Odoo:

```text
Settings
→ Developer Tools
→ Activate developer mode
```

Se eligió:

```text
Activate developer mode
```

y no las variantes con assets/tests.

Esto permitió inspeccionar internamente:

- modelos
    
- campos
    
- tipos
    
- relaciones
    
- propiedades
    
- metadatos de Odoo
    

---

# 19. Exploración del modelo `purchase.order`

Se accedió al modelo:

```text
purchase.order
```

desde el modo desarrollador.

Odoo lo identifica como:

```text
Model Description: Purchase Order
Model: purchase.order
Type: Base Object
```

Aparecía asociado a aplicaciones como:

```text
purchase
purchase_edi_ubl_bis3
purchase_mrp
purchase_stock
sale_purchase
sale_purchase_stock
```

Se inspeccionaron numerosos campos, entre ellos:

```text
access_token
access_url
access_warning
acknowledged
activity_ids
activity_type_id
activity_user_id
amount_tax
amount_total
amount_total_cc
amount_untaxed
company_currency_id
company_id
currency_id
date_approve
date_order
date_planned
dest_address_id
duplicated_order_ids
effective_date
fiscal_position_id
has_sale_order
id
incoming_picking_count
incoterm_id
```

También se abrió el detalle de un campo y se observaron propiedades como:

```text
Field Name
Field Label
Field Type
Field Help

Required?
Readonly?
Stored?
Indexed?
Copied?
Enable Ordered Tracking?

Related Model?
On Delete?
Domain?
```

---

# 20. Comprensión del ORM

A partir de esta exploración se estudió el concepto:

```text
ORM = Object-Relational Mapping
```

En español:

```text
Mapeo Objeto-Relacional
```

La conclusión importante para el proyecto es que Odoo no es simplemente una interfaz sobre tablas PostgreSQL.

Odoo trabaja con modelos como:

```text
purchase.order
purchase.order.line
res.partner
product.product
stock.quant
stock.picking
mrp.production
sale.order
```

El ORM se encarga, entre otras cosas, de:

- persistencia
    
- relaciones entre modelos
    
- validaciones
    
- permisos
    
- ACLs
    
- record rules
    
- lógica de negocio
    
- campos calculados
    
- herencia de modelos
    
- operaciones `create`, `write`, `unlink`, etc.
    

La arquitectura se conceptualizó como:

```text
Aplicación / Agente
        ↓
Odoo API
        ↓
Odoo ORM
        ↓
PostgreSQL
```

---

# 21. Distinción entre API y ORM

Se aclaró una cuestión fundamental:

**La API no devuelve el ORM.**

La API es la interfaz externa mediante la cual una aplicación puede solicitar operaciones a Odoo.

El ORM permanece dentro de Odoo.

La secuencia es:

```text
Agente
  ↓
Odoo API
  ↓
Método del modelo Odoo
  ↓
ORM
  ↓
PostgreSQL
  ↓
ORM
  ↓
API
  ↓
JSON
  ↓
Agente
```

Por tanto, la API está alineada con los modelos del ORM, pero **no expone objetos ORM directamente**.

Lo que devuelve son datos serializados, normalmente JSON.

---

# 22. API JSON-2 de Odoo 19

Se decidió utilizar la API moderna de Odoo 19:

```text
JSON-2
```

con endpoints conceptualmente del tipo:

```text
/json/2/<modelo>/<método>
```

Esto encaja especialmente bien con el proyecto porque permite acceder a modelos y métodos de Odoo sin acceder directamente a PostgreSQL.

---

# 23. Creación de API Key

Se creó una API Key en el usuario de Odoo.

La API Key se mantiene como secreto y no se ha compartido.

En Ubuntu se guardó temporalmente mediante una variable de entorno:

```bash
export ODOO_API_KEY='...'
```

La decisión de utilizar una variable de entorno evita escribir la credencial directamente en el código o en comandos posteriores.

---

# 24. Primera llamada real a la API

Se realizó la primera llamada real a Odoo JSON-2 mediante `curl`.

Comando utilizado:

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

La API respondió correctamente:

```json
[
  {
    "id": 11,
    "name": "P00011",
    "partner_id": [11, "Ready Mat"],
    "amount_total": 6936.0
  },
  {
    "id": 10,
    "name": "P00010",
    "partner_id": [15, "Azure Interior"],
    "amount_total": 2505.0
  },
  {
    "id": 9,
    "name": "P00009",
    "partner_id": [10, "Gemini Furniture"],
    "amount_total": 12500.0
  },
  {
    "id": 8,
    "name": "P00008",
    "partner_id": [8, "Wood Corner"],
    "amount_total": 6465.5
  },
  {
    "id": 7,
    "name": "P00007",
    "partner_id": [11, "Ready Mat"],
    "amount_total": 1222.5
  }
]
```

## Importancia de esta prueba

Fue la primera confirmación de extremo a extremo de:

```text
curl
 ↓
Odoo JSON-2 API
 ↓
purchase.order.search_read()
 ↓
Odoo ORM
 ↓
PostgreSQL
 ↓
JSON
 ↓
curl
```

Por tanto, **la API de Odoo ya está funcionando correctamente en el entorno del TFG**.

---

# 25. Consulta de las líneas de un pedido

Se identificó que las líneas de un pedido de compra no forman parte directamente del modelo:

```text
purchase.order
```

sino que están en:

```text
purchase.order.line
```

La relación conceptual es:

```text
purchase.order
       │
       │ order_id
       ▼
purchase.order.line
       │
       │ product_id
       ▼
product.product
```

Para consultar las líneas de `P00011`, cuyo ID es `11`, se preparó una consulta mediante:

```text
purchase.order.line/search_read
```

con el dominio:

```json
[
  ["order_id", "=", 11]
]
```

y campos como:

```text
id
order_id
product_id
name
product_qty
price_unit
price_subtotal
price_total
```

Esto permite obtener:

- producto
    
- descripción
    
- cantidad
    
- precio unitario
    
- subtotal
    
- total
    

Esta prueba sirve además para estudiar cómo la API representa las relaciones entre modelos del ORM.

---

# 26. Discusión sobre cargas masivas de datos

Se planteó la necesidad de realizar un **volcado/carga masiva de datos** para crear escenarios realistas para el TFG.

Inicialmente se aclaró la diferencia entre:

### A. Insertar directamente en PostgreSQL

Por ejemplo:

```sql
INSERT INTO purchase_order ...
```

### B. Crear registros mediante el ORM/API

Por ejemplo:

```text
script
 ↓
Odoo API
 ↓
ORM
 ↓
PostgreSQL
```

Se decidió que, para la aplicación, **no se deben hacer inserciones directas en PostgreSQL**.

La razón es que eso saltaría:

- ORM
    
- validaciones
    
- permisos
    
- record rules
    
- lógica de negocio
    
- relaciones y comportamientos de Odoo
    

La estrategia prevista es utilizar la API/ORM para crear datos.

Esto permitirá posteriormente construir escenarios coherentes de Supply Chain, por ejemplo:

```text
Proveedor
   ↓
Pedido de compra
   ↓
Recepción
   ↓
Stock
   ↓
Orden de fabricación
   ↓
Producto terminado
   ↓
Pedido de venta
```

Esto será especialmente importante para generar incidencias realistas para los agentes.

---

# 27. PostgreSQL y acceso mediante DBeaver

Aunque el agente no accederá directamente a PostgreSQL, se decidió instalar una herramienta gráfica para **inspeccionar y comprender la estructura interna de Odoo**.

Se eligió:

```text
DBeaver Community
```

No para sustituir al ORM, sino para poder observar qué hay detrás de él.

---

# 28. Publicación del puerto PostgreSQL

Inicialmente el `compose.yaml` solo publicaba:

```yaml
ports:
  - "8069:8069"
```

en Odoo.

PostgreSQL no tenía ningún puerto publicado.

Para permitir que DBeaver accediera a PostgreSQL se añadió al servicio `db`:

```yaml
ports:
  - "5432:5432"
```

Por tanto, el estado actual es:

```text
Odoo:
0.0.0.0:8069 → 8069

PostgreSQL:
0.0.0.0:5432 → 5432
```

---

# 29. Verificación del contenedor PostgreSQL

Se ejecutó:

```bash
docker ps
```

y se obtuvo:

```text
odoo-tfg-db
0.0.0.0:5432->5432/tcp
[::]:5432->5432/tcp
```

Esto confirmó que PostgreSQL estaba correctamente publicado.

El contenedor Odoo seguía funcionando con:

```text
0.0.0.0:8069->8069/tcp
```

---

# 30. Instalación de DBeaver

Se decidió instalar DBeaver **dentro de Ubuntu-TFG**, en lugar de Windows.

Razones:

- PostgreSQL está dentro de la misma VM.
    
- Se evita configurar inicialmente la red entre Windows y VirtualBox.
    
- DBeaver puede acceder directamente a `localhost:5432`.
    
- Todo el entorno de desarrollo queda concentrado en Ubuntu-TFG.
    
- No afecta a Ubuntu-Kathara.
    

Se comprobó primero:

```bash
snap --version
```

Resultado:

```text
snap 2.76.3
snapd 2.76.3
ubuntu 26.04
architecture amd64
```

---

# 31. Instalación de DBeaver — primer intento

Se ejecutó:

```bash
sudo snap install dbeaver-ce
```

Snap devolvió un aviso indicando que el paquete utilizaba:

```text
classic confinement
```

y requería confirmación explícita.

## Solución

Se ejecutó:

```bash
sudo snap install dbeaver-ce --classic
```

Resultado:

```text
dbeaver-ce 26.2.1.202609210342 from DBeaver (dbeaver-corp) installed
```

DBeaver quedó instalado correctamente.

---

# 32. Conexión de DBeaver a PostgreSQL

DBeaver se abrió correctamente.

Se creó una conexión PostgreSQL con:

```text
Host: localhost
Port: 5432
Database: Odoo-tfg
Username: odoo
Password: odoo
```

La conexión fue satisfactoria.

Por tanto, actualmente podemos inspeccionar PostgreSQL gráficamente mediante DBeaver.

---

# 33. Situación técnica actual

A fecha de esta sesión, el entorno básico del TFG está operativo.

## Odoo

```text
Odoo 19 Community
```

Funcionando en:

```text
http://localhost:8069
```

## PostgreSQL

```text
PostgreSQL 17
```

en:

```text
odoo-tfg-db
```

y publicado en:

```text
localhost:5432
```

## Docker

Contenedores principales:

```text
odoo-tfg
odoo-tfg-db
```

## Proyecto

Ruta:

```text
/home/maite/odoo-tfg
```

con:

```text
compose.yaml
config/
data/
```

## Base de datos

```text
Odoo-tfg
```

## Módulos funcionales

```text
sale_management
purchase
stock
mrp
```

Todos:

```text
state = installed
```

## API

JSON-2 funcionando correctamente.

Primera consulta real ejecutada con éxito sobre:

```text
purchase.order
```

## DBeaver

Instalado en Ubuntu-TFG:

```text
DBeaver Community 26.2.1
```

conectado correctamente a:

```text
PostgreSQL → Odoo-tfg
```

---

# 34. Decisiones tomadas hasta ahora

## ERP

Se utilizará:

```text
Odoo 19 Community
```

como ERP realista del proyecto.

## Base de datos

Se utilizará:

```text
PostgreSQL 17
```

como base de datos de Odoo.

## Despliegue

Odoo y PostgreSQL se ejecutan mediante:

```text
Docker Compose
```

dentro de Ubuntu-TFG.

## Acceso de agentes

Los agentes no accederán directamente a PostgreSQL.

El flujo será:

```text
Agent
 ↓
MCP
 ↓
Odoo JSON-2 API
 ↓
Odoo ORM
 ↓
PostgreSQL
```

## Carga de datos

Los datos de negocio deberán crearse preferentemente mediante API/ORM y no mediante `INSERT` directo en PostgreSQL.

## Inspección de BD

DBeaver se utilizará para:

- explorar tablas
    
- entender el esquema
    
- comprobar relaciones
    
- inspeccionar datos
    
- comprender cómo el ORM se materializa en PostgreSQL
    

No será la vía de acceso de los agentes.

## MCP

MCP será una capa semántica/controlada.

La intención es que el agente pueda utilizar herramientas como:

```text
get_purchase_order()
get_purchase_order_lines()
get_supplier()
get_stock()
get_incoming_shipments()
get_manufacturing_orders()
get_sales_commitments()
```

en lugar de permitir al LLM realizar consultas arbitrarias sobre el modelo de Odoo.

---

# 35. Problemas encontrados y soluciones

|Problema|Solución|
|---|---|
|El volumen `./config:/etc/odoo` ocultaba la configuración de Odoo|Crear `config/odoo.conf`|
|Odoo no podía escribir en `/var/lib/odoo/sessions`|`sudo chown -R 100:101 ~/odoo-tfg/data/odoo`|
|La instalación de módulos desde la UI se quedó en estado inconsistente|Instalar mediante CLI con `--stop-after-init`|
|Inicialmente parecía que solo estaba disponible Discuss|Se comprobó que era solo la aplicación visible; los módulos estaban instalados|
|Necesidad de verificar módulos realmente instalados|Consulta directa a `ir_module_module`|
|Necesidad de acceso API|Crear API Key y utilizar JSON-2|
|Necesidad de consultar relaciones de pedidos|Utilizar `purchase.order.line` y `order_id`|
|Necesidad de inspeccionar PostgreSQL gráficamente|Instalar DBeaver|
|PostgreSQL no estaba publicado|Añadir `5432:5432` al servicio `db`|
|Snap rechazó inicialmente DBeaver por classic confinement|Ejecutar `sudo snap install dbeaver-ce --classic`|

---

# 36. Próxima fase

El entorno ya está preparado para pasar de la **instalación y exploración** a la **construcción de la integración**.

El orden lógico a partir de aquí es:

1. Explorar con DBeaver las tablas generadas por Odoo.
    
2. Relacionar físicamente las tablas con los modelos ORM que hemos visto.
    
3. Comprender mejor las relaciones:
    
    - `purchase.order`
        
    - `purchase.order.line`
        
    - `product.product`
        
    - `res.partner`
        
    - `stock.picking`
        
    - `stock.move`
        
    - `stock.quant`
        
    - `mrp.production`
        
    - `sale.order`
        
4. Diseñar una estrategia para generar datos de prueba masivos y coherentes.
    
5. Probar operaciones de escritura mediante la API de Odoo.
    
6. Diseñar los primeros MCP tools semánticos.
    
7. Integrar esos tools con el agente.
    
8. Construir posteriormente el flujo de incidencias mediante LangGraph.
    
9. Incorporar webhook/event-driven triggers desde Odoo.
    
10. Añadir persistencia de `IncidentAnalysis` en una base de datos independiente (`agentic_db`).
    
11. Incorporar observabilidad con Langfuse.
    

---

# 37. Estado conceptual alcanzado

La principal comprensión técnica alcanzada en esta fase es:

```text
                     ┌─────────────────────┐
                     │       AGENTE        │
                     └──────────┬──────────┘
                                │
                              MCP
                                │
                                ▼
                     ┌─────────────────────┐
                     │    ODOO JSON-2      │
                     │        API          │
                     └──────────┬──────────┘
                                │
                         métodos/modelos
                                │
                                ▼
                     ┌─────────────────────┐
                     │     ODOO ORM        │
                     │                     │
                     │ purchase.order      │
                     │ purchase.order.line │
                     │ product.product     │
                     │ stock.picking       │
                     │ mrp.production      │
                     │ sale.order          │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │    PostgreSQL 17    │
                     └─────────────────────┘
```

La API **no contiene ni devuelve el ORM**.

La API es la puerta de entrada.

El ORM permanece dentro de Odoo y es quien interactúa con PostgreSQL.

Esta separación será fundamental para justificar posteriormente la arquitectura del sistema agentic y la decisión de que los agentes **no accedan directamente a la base de datos**.