---
type: diseño
area: arquitectura
status: proposed
project: TFG Odoo Agentic AI
tags:
  - arquitectura/multiagente
  - arquitectura/orquestacion
  - arquitectura/mcp
  - arquitectura/observabilidad
  - jev/choice
  - jev/score
  - evaluacion/kpis
---

# Diseño de orquestación, Jev, agentes y evaluación

## Estado y alcance de esta decisión

Este documento consolida el diseño conceptual acordado para la prueba de concepto. Es una propuesta de arquitectura que deberá concretarse durante la implementación y validarse con la documentación y las APIs reales de las tecnologías seleccionadas.

Se mantiene el alcance inicial: Odoo Community Edition como ERP de referencia, datos sintéticos, investigación y análisis de incidencias de cadena de suministro, generación de propuestas y supervisión humana. Los agentes no ejecutarán modificaciones en Odoo.

## 1. Arquitectura general

La arquitectura sigue un patrón en estrella: LangGraph Orchestrator es el componente central y coordina cuatro agentes especializados. Los agentes no se comunican directamente entre sí; envían sus resultados al orquestador.

Flujo conceptual:

1. Odoo activa el proceso mediante una Automation Rule y un webhook.
2. El orquestador inicializa el estado de la incidencia y registra su identificador.
3. Jev Choice realiza una clasificación preliminar de la incidencia en uno de los cinco niveles definidos.
4. LangGraph decide qué agentes deben intervenir, asigna tareas y controla el flujo.
5. Los agentes LLM consultan Odoo mediante herramientas MCP de solo lectura.
6. El orquestador consolida resultados, evidencias, hipótesis e información pendiente. Puede solicitar nuevas investigaciones.
7. Cuando dispone de información suficiente, prepara preguntas para Jev Score sobre las probabilidades de consecuencias concretas.
8. El sistema presenta el diagnóstico, las evidencias, las estimaciones y las propuestas en Streamlit para revisión humana.

La clasificación inicial de Choice es preliminar y no sustituye la evaluación posterior basada en evidencias. Los cinco niveles deben conservar sus criterios y denominaciones ya definidos en [[Escenarios de evaluación - cinco niveles de complejidad]]. Se debe mantener diferenciada la complejidad de investigación de la gravedad o impacto operativo: no son necesariamente la misma dimensión.

## 2. LangGraph Orchestrator

### Responsabilidades

- Recibir el trigger de Odoo mediante webhook.
- Inicializar y mantener el estado global de la incidencia, incluido un identificador de correlación.
- Solicitar a Jev Choice la clasificación inicial.
- Determinar qué agentes deben intervenir mediante la lógica de routing de LangGraph y reglas de coordinación.
- Asignar tareas delimitadas a los agentes con el contexto y los datos pertinentes.
- Recibir y consolidar resultados, evidencias, hipótesis y propuestas.
- Controlar iteraciones y decidir si se necesita información adicional de uno o varios agentes.
- Preparar las preguntas de evaluación que se enviarán a Jev Score al finalizar la investigación.
- Consolidar el resultado para su presentación en Streamlit.

### Qué no hace

- No realiza las investigaciones funcionales que corresponden a los agentes.
- No sustituye a los LLM en la interpretación y análisis de información.
- No delega en Jev la coordinación del flujo ni el routing principal.
- No permite comunicación directa entre agentes.
- No ofrece acceso indiscriminado a todos los modelos y registros de Odoo.
- No ejecuta modificaciones en Odoo en el alcance inicial.
- No aprueba automáticamente propuestas ni convierte una estimación probabilística en una autorización de ejecución.

### Routing y Choice

La selección de agentes corresponde al orquestador y a la lógica de LangGraph, no a Jev Choice. El orquestador puede activar uno o varios agentes según el trigger, la clasificación preliminar, los hallazgos y las reglas de coordinación. Choice puede utilizarse opcionalmente para clasificar cuestiones cerradas, pero no es el mecanismo principal de routing.

## 3. Jev

Jev es una capa de evaluación y decisión estructurada. No es un agente de investigación, no consulta Odoo y no coordina agentes.

### Choice: clasificación inicial

- Interviene al principio, después de recibir el trigger.
- Clasifica la incidencia en uno de los cinco niveles definidos.
- Permite mostrar una primera valoración en Streamlit y aporta contexto al orquestador.
- Es una clasificación preliminar que puede revisarse con la información obtenida durante la investigación.

### Score: estimaciones probabilísticas al final

Después de que los agentes hayan recopilado y estructurado la información, el orquestador prepara preguntas concretas sobre las consecuencias de la incidencia. Jev Score devuelve estimaciones probabilísticas que se incorporan al análisis final.

Ejemplos de preguntas:
- ¿Qué probabilidad hay de que el pedido de compra X no pueda entregarse a tiempo?
- ¿Qué probabilidad hay de que la falta de este componente provoque una interrupción de la orden de fabricación?
- ¿Qué probabilidad hay de que el pedido de venta Y incumpla su fecha comprometida?
- ¿Qué probabilidad hay de que las existencias disponibles sean insuficientes para cubrir las necesidades previstas?

Estas estimaciones no son certezas ni decisiones de ejecución. La semántica exacta, el formato de salida y la interpretación de Score deberán contrastarse con la documentación y la implementación de Jev antes de desarrollar la integración.

### Noul: fuera del flujo principal inicial

No se incorpora como funcionalidad obligatoria en la primera versión. Su posible uso queda pendiente de identificar un caso de uso concreto que aporte valor adicional frente a Choice y Score. No se asignará automáticamente a todos los agentes.

## 4. Agentes especializados

Los cuatro agentes se implementarán como agentes basados en LLM. Su responsabilidad es investigar su ámbito funcional, consultar datos, relacionar registros, identificar evidencias e hipótesis y devolver resultados estructurados al orquestador.

### PurchaseAgent

Investiga pedidos de compra, proveedores, fechas previstas, cantidades y retrasos o incumplimientos.

Tools funcionales iniciales:
- `read_purchase_orders`: pedidos de compra, estados, fechas y cantidades.
- `read_suppliers`: información de proveedores.
- `read_purchase_order_lines`: detalle de líneas de compra y productos asociados.

### InventoryAgent

Investiga existencias, movimientos, reservas y disponibilidad de materiales.

Tools funcionales iniciales:
- `read_stock_quants`: cantidades disponibles y reservadas por producto y ubicación.
- `read_stock_moves`: movimientos de inventario y su estado.
- `read_stock_move_lines`: detalle de movimientos.

### ManufacturingAgent

Investiga órdenes de fabricación, necesidades de materiales y posibles interrupciones de producción.

Tools funcionales iniciales:
- `read_manufacturing_orders`: órdenes de fabricación, estados y fechas.
- `read_bills_of_materials`: listas de materiales (BoM).
- `read_production_components`: componentes y cantidades requeridas para fabricar un producto.

### SalesAgent

Identifica pedidos de venta afectados, compromisos de entrega e impacto en clientes.

Tools funcionales iniciales:
- `read_sales_orders`: pedidos de venta, estados y fechas de entrega.
- `read_sales_order_lines`: productos, cantidades y líneas de pedido.
- `read_customers`: información de clientes asociada a los pedidos afectados.

### Catálogo evolutivo

Este catálogo es una primera propuesta funcional, no una lista cerrada. A medida que avance el desarrollo y se identifiquen necesidades de investigación adicionales, podrán incorporarse, combinarse, dividirse o retirarse herramientas. Los nombres indicados son nombres funcionales, no necesariamente nombres de modelos o métodos nativos de Odoo. Habrá que validar los modelos, campos, relaciones, filtros y permisos concretos en Odoo 19 Community.

## 5. MCP y reutilización de herramientas

La integración de herramientas se realizará mediante MCP. Por tanto, las tools no tienen por qué pertenecer en exclusiva a un único agente. Un servidor MCP puede exponer herramientas comunes que distintos agentes reutilicen, siempre que el contexto de ejecución y los permisos permitan ese acceso.

Se propone distinguir:

- **Herramientas compartidas:** consultas de productos, proveedores, existencias, movimientos y otros datos transversales que pueden ser necesarios para más de un agente.
- **Herramientas de dominio:** operaciones de consulta más específicas de Compras, Fabricación o Ventas.
- **Permisos y contexto:** aunque una herramienta sea compartida, el acceso debe estar restringido por el usuario técnico, ACL, reglas de registro y validación de parámetros. La disponibilidad de una tool para varios agentes no implica acceso ilimitado a todos los datos.

Candidatas a reutilización compartida:
- Consulta de productos y variantes.
- Consulta de proveedores.
- Consulta de existencias por producto y ubicación.
- Consulta de movimientos de inventario.
- Consulta de pedidos de compra y sus líneas cuando la investigación de fabricación necesite conocer el aprovisionamiento.

La distribución final de las tools entre agentes se definirá según los recorridos de investigación y las necesidades observadas durante el desarrollo. Se evitará duplicar implementaciones cuando varios agentes necesiten la misma operación. La reutilización MCP no elimina la necesidad de delimitar qué agentes pueden invocar cada herramienta.

## 6. OdooAPIClient

Se implementará un cliente común, `OdooAPIClient`, que encapsule la comunicación con Odoo mediante la API externa JSON-2. No es un agente ni una tool de Jev; es una capa de integración utilizada internamente por las herramientas MCP.

Responsabilidades:
- Gestionar la autenticación y las credenciales de integración.
- Construir y enviar peticiones JSON-2.
- Ejecutar operaciones de lectura sobre modelos autorizados.
- Validar parámetros de entrada y respuestas.
- Gestionar errores de comunicación y respuestas de la API.
- Controlar límites de consulta y evitar peticiones innecesariamente grandes.
- Devolver resultados estructurados a las herramientas MCP.

La seguridad se aplicará también en Odoo mediante un usuario técnico con permisos limitados, ACL y reglas de registro. No habrá acceso directo a PostgreSQL: las consultas se realizarán mediante JSON-2 y el ORM de Odoo.

Las tools de dominio pueden encapsular varias consultas JSON-2 y devolver resultados consolidados; no es necesario que exista una correspondencia uno a uno entre cada tool y cada método de Odoo.

## 7. Observabilidad: OpenTelemetry

OpenTelemetry es una capa de instrumentación y observabilidad, independiente de Jev y de los KPI. Permite recopilar trazas, métricas y logs de la ejecución del sistema.

Se utilizará para instrumentar, entre otros elementos, el webhook, el orquestador, las invocaciones de agentes, las llamadas a herramientas MCP, las consultas a Odoo y las llamadas a modelos o servicios de IA, en la medida en que las integraciones lo permitan.

Relación con los KPI:
- KPI de eficiencia y coste: las trazas y métricas pueden aportar duración, número de invocaciones y pasos. El coste de inferencia requerirá además registrar el uso de tokens y las tarifas aplicables a cada modelo o servicio.
- KPI de fiabilidad y trazabilidad: los spans, eventos y logs permiten detectar errores y reconstruir operaciones. La vinculación con la incidencia exige propagar explícitamente un identificador de correlación en las trazas y en los registros de resultados/evidencias.

OpenTelemetry no calcula ni evalúa por sí mismo los KPI: proporciona datos instrumentados que después se procesan para obtener las métricas de evaluación. Los KPI 5 y 6 se calculan a partir de esos datos y de registros complementarios.

## 8. KPI y evaluación del sistema

Se conservan seis KPI principales. Los valores se calcularán a partir de ejecuciones instrumentadas y referencias de evaluación (*ground truth*). Jev no debe utilizarse para calcular métricas deterministas.

| KPI | Medición | Jev |
|---|---|---|
| Identificación de áreas afectadas | Precisión, recall y F1 respecto a los módulos esperados en el escenario. | No interviene; cálculo automático frente al ground truth. |
| Correspondencia con el recorrido ideal | Porcentaje de pasos esperados ejecutados y número de pasos innecesarios. | No interviene; comparación de trazas con el recorrido de referencia. |
| Calidad de las evidencias | Rúbrica de corrección, relevancia y cobertura respecto al escenario. | No interviene directamente; Score podría complementar preguntas probabilísticas específicas, no sustituir la evaluación de referencia. |
| Calidad de las propuestas | Puntuación manual de 0 a 10 mediante rúbrica: pertinencia, viabilidad, fundamentación, consideración de riesgos y adecuación de alternativas. | No interviene directamente en la puntuación de referencia. |
| Eficiencia y coste | Tiempo de ejecución, número de llamadas a tools, pasos ejecutados y coste de inferencia por escenario. | No interviene; cálculo con trazas, métricas y datos de uso/coste. |
| Fiabilidad y trazabilidad | Porcentaje de ejecuciones completadas sin errores y porcentaje de operaciones/evidencias vinculadas al identificador de incidencia. | No interviene; cálculo con logs, trazas y registros de correlación. |

### Interpretación de los KPI

- **Identificación de áreas afectadas:** compara los módulos identificados por el sistema con los definidos como afectados en el escenario de referencia.
- **Correspondencia con el recorrido ideal:** mide tanto la recuperación de los pasos esperados como la realización de consultas o pasos innecesarios.
- **Calidad de las evidencias:** evalúa si las evidencias son correctas, pertinentes y suficientes para justificar el diagnóstico.
- **Calidad de las propuestas:** la evaluación de referencia será manual mediante una rúbrica de cinco criterios, cada uno valorado de 0 a 2 puntos. La suma produce una puntuación de 0 a 10.
- **Eficiencia y coste:** combina recursos temporales y computacionales; se informarán sus medidas por separado aunque pertenezcan al mismo KPI.
- **Fiabilidad y trazabilidad:** se informarán por separado el porcentaje de ejecuciones sin errores y la proporción de operaciones/evidencias correctamente correlacionadas.

Las estimaciones de Jev Score sobre consecuencias de la incidencia se mostrarán como resultados del análisis de riesgo, no como KPI de rendimiento del sistema. Las probabilidades no sustituyen la comparación con el ground truth ni la evaluación humana de propuestas y evidencias.

## 9. Supervisión humana y límites de autonomía

El sistema investiga, analiza y propone. En el alcance inicial:
- Los agentes disponen de herramientas de solo lectura.
- No se crean ni modifican pedidos, movimientos, órdenes de fabricación ni otros registros de Odoo.
- Las probabilidades de Jev no autorizan automáticamente acciones.
- Las propuestas se presentan para que una persona valore y decida si procede llevarlas a cabo.
- Las incertidumbres y la información insuficiente deben quedar explícitas en el resultado.

## 10. Decisiones pendientes

1. Confirmar las denominaciones y criterios exactos de los cinco niveles y mantener separadas complejidad y gravedad cuando corresponda.
2. Definir preguntas estándar de Jev Score y el procedimiento para contrastar sus estimaciones con resultados de referencia.
3. Verificar la semántica, los tipos de salida y la integración real de Choice, Score y Noul en Jev.
4. Contrastar el catálogo funcional de tools con los modelos, campos y relaciones de Odoo 19 Community.
5. Definir qué herramientas MCP serán compartidas, cuáles serán específicas y cómo se aplicarán los permisos por agente.
6. Concretar la propagación del identificador de incidencia y la instrumentación OpenTelemetry.
7. Precisar el método de cálculo del coste de inferencia según el proveedor y los modelos utilizados.

## Enlaces relacionados

- [[Arquitectura objetivo del sistema agentic]]
- [[Decisiones arquitectónicas del sistema]]
- [[MCP como capa semántica y controlada]]
- [[Herramientas MCP previstas]]
- [[Observabilidad del sistema agentic]]
- [[Escenarios de evaluación - cinco niveles de complejidad]]
- [[Persistencia de IncidentAnalysis]]
