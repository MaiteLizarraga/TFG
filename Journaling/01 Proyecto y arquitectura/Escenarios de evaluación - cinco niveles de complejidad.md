---
type: referencia
area: evaluacion
status: proposed
project: TFG Odoo Agentic AI
tags:
  - evaluacion/escenarios
  - evaluacion/ground-truth
  - supply-chain/incidencias
  - odoo/modulos
---

# Escenarios de evaluación: cinco niveles de complejidad

## Objetivo

Definir un único tipo de incidencia de Supply Chain con cinco niveles de complejidad creciente. Cada nivel establece qué información debe recuperar el sistema, qué módulos y procesos debe investigar, qué relaciones debe identificar, qué evidencias debe obtener y qué conclusión o propuesta sería aceptable.

Esta definición constituye una primera propuesta funcional del escenario de evaluación. Los escenarios deberán concretarse posteriormente mediante registros, identificadores, cantidades, fechas y relaciones verificables en los datos sintéticos de Odoo.

## Incidencia de referencia

**Retraso o incumplimiento en el suministro de una materia prima por parte de un proveedor**, que puede provocar una ruptura de stock y afectar a la planificación de fabricación y al cumplimiento de los pedidos de venta.

El escenario permite recorrer progresivamente los cuatro módulos funcionales seleccionados para el TFG:

- Compras (`purchase`).
- Inventario (`stock`).
- Fabricación (`mrp`).
- Ventas (`sale_management`).

Se mantiene el mismo tipo de incidencia en los cinco niveles, aumentando gradualmente la cantidad de información que debe relacionarse, las dependencias entre procesos y la complejidad de las decisiones.

## Nivel 1. Incidencia localizada en Compras e Inventario

**Situación:** un proveedor comunica que no va a entregar en la fecha prevista una materia prima incluida en un pedido de compra confirmado.

- **Información que debería recuperar:** pedido de compra, proveedor, producto, cantidad solicitada, cantidad pendiente de recepción y fecha de entrega prevista.
- **Módulos y procesos que debería investigar:** Compras, para consultar el pedido y sus líneas; e Inventario, para comprobar las recepciones previstas y las existencias actuales del producto.
- **Relaciones que debería identificar:** correspondencia entre el pedido de compra, el producto afectado y el movimiento de entrada pendiente.
- **Evidencias que debería obtener:** pedido de compra confirmado, línea pendiente de recepción, fecha prevista de llegada y disponibilidad actual del producto.
- **Conclusión o propuesta aceptable:** identificar el retraso y cuantificar la cantidad potencialmente no disponible. Proponer solicitar al proveedor una nueva fecha de entrega o confirmar una fecha alternativa.

**Objetivo del nivel:** comprobar que el sistema identifica correctamente una incidencia sencilla y relaciona información de dos módulos.

## Nivel 2. Incidencia con impacto en la disponibilidad de inventario

**Situación:** el retraso del proveedor provoca que las existencias disponibles de la materia prima sean insuficientes para cubrir las necesidades previstas. Existen, además, reservas o movimientos de inventario que condicionan la disponibilidad real.

- **Información que debería recuperar:** toda la información del nivel 1, además de existencias disponibles, cantidades reservadas, movimientos de stock pendientes y necesidades previstas del producto.
- **Módulos y procesos que debería investigar:** Compras e Inventario, incluyendo recepciones, ubicaciones, reservas y movimientos de existencias.
- **Relaciones que debería identificar:** relación entre la recepción retrasada, el stock físico, las cantidades reservadas y la disponibilidad efectiva para otros procesos.
- **Evidencias que debería obtener:** cantidades físicas y disponibles, reservas existentes, movimientos pendientes y diferencia entre la demanda prevista y el stock utilizable.
- **Conclusión o propuesta aceptable:** determinar si existe una ruptura de stock real o potencial, cuantificar el déficit y proponer medidas como priorizar determinadas reservas, buscar existencias alternativas o solicitar un suministro parcial.

**Objetivo del nivel:** comprobar que el sistema distingue entre existencias físicas y disponibilidad efectiva, y que relaciona correctamente los movimientos de inventario.

## Nivel 3. Incidencia con impacto en Fabricación

**Situación:** la falta de materia prima afecta a una o varias órdenes de fabricación que necesitan ese producto como componente. El retraso puede impedir iniciar o completar la producción prevista.

- **Información que debería recuperar:** toda la información anterior, además de listas de materiales (BoM), órdenes de fabricación, cantidades de componentes requeridas, cantidades consumidas y pendientes, fechas planificadas y estado de las órdenes.
- **Módulos y procesos que debería investigar:** Compras, Inventario y Fabricación, incluyendo aprovisionamiento de componentes, disponibilidad para producción y planificación de órdenes de fabricación.
- **Relaciones que debería identificar:** relación entre el pedido de compra retrasado, el déficit de inventario, los componentes requeridos por las listas de materiales y las órdenes de fabricación afectadas.
- **Evidencias que debería obtener:** órdenes de fabricación afectadas, necesidades de componentes, disponibilidad insuficiente y fechas de producción que podrían verse comprometidas.
- **Conclusión o propuesta aceptable:** identificar qué órdenes de fabricación están en riesgo, cuantificar el impacto y proponer alternativas como reprogramar la producción, priorizar órdenes o buscar un suministro alternativo.

**Objetivo del nivel:** comprobar que el sistema reconstruye dependencias entre aprovisionamiento, inventario y fabricación.

## Nivel 4. Incidencia con impacto en los compromisos comerciales

**Situación:** la falta de materia prima afecta a la producción de productos terminados necesarios para satisfacer varios pedidos de clientes. Algunas entregas comerciales pueden incumplirse si no se modifica la planificación.

- **Información que debería recuperar:** toda la información anterior, además de pedidos de venta, productos solicitados, cantidades pendientes de entrega, fechas comprometidas y movimientos de salida asociados.
- **Módulos y procesos que debería investigar:** los cuatro módulos: Compras, Inventario, Fabricación y Ventas. Deberá analizar tanto el aprovisionamiento como la producción y los compromisos de entrega a clientes.
- **Relaciones que debería identificar:** relación entre el retraso del proveedor, la disponibilidad de componentes, las órdenes de fabricación afectadas, los productos terminados y los pedidos de venta que dependen de ellos.
- **Evidencias que debería obtener:** pedidos de venta afectados, cantidades pendientes, fechas comprometidas, órdenes de fabricación vinculadas y estimación del retraso potencial de las entregas.
- **Conclusión o propuesta aceptable:** reconstruir el impacto de la incidencia sobre los compromisos comerciales y proponer alternativas como modificar la planificación de producción, priorizar determinados pedidos o negociar nuevas fechas de entrega con los clientes.

**Objetivo del nivel:** comprobar que el sistema es capaz de reconstruir el impacto transversal de una incidencia desde el proveedor hasta el cliente.

## Nivel 5. Incidencia transversal con alternativas y dependencias múltiples

**Situación:** el proveedor confirma que no podrá suministrar la materia prima durante un periodo prolongado. Existen varias órdenes de fabricación y pedidos de venta afectados, pero también posibles alternativas: otro proveedor, existencias en otras ubicaciones o una materia prima sustitutiva técnicamente válida.

- **Información que debería recuperar:** toda la información anterior, además de otros pedidos de compra del mismo producto, proveedores alternativos disponibles en el ERP, existencias en otras ubicaciones, listas de materiales alternativas si están definidas y posibles fechas de aprovisionamiento.
- **Módulos y procesos que debería investigar:** los cuatro módulos, ampliando la investigación a las relaciones entre proveedores, aprovisionamiento, disponibilidad global, fabricación, planificación y compromisos comerciales.
- **Relaciones que debería identificar:** dependencias entre distintos pedidos de compra, proveedores, productos y ubicaciones; impacto de las alternativas de aprovisionamiento sobre las órdenes de fabricación; y consecuencias sobre los pedidos de venta y sus fechas comprometidas.
- **Evidencias que debería obtener:** confirmación del incumplimiento del proveedor, déficit de materia prima, órdenes de fabricación y pedidos de venta afectados, disponibilidad de alternativas y diferencias entre los escenarios posibles.
- **Conclusión o propuesta aceptable:** presentar varias alternativas de resolución fundamentadas en los datos disponibles, explicando sus consecuencias sobre producción, inventario y compromisos comerciales. Por ejemplo, priorizar un proveedor alternativo, redistribuir existencias o reprogramar determinadas órdenes. La propuesta deberá identificar las limitaciones y la información que todavía sea necesario confirmar.

**Objetivo del nivel:** comprobar que el sistema puede investigar un escenario con múltiples dependencias, comparar alternativas y presentar una propuesta razonada sin tomar la decisión final.

## Progresión de complejidad

| Nivel | Módulos implicados | Complejidad que se introduce |
|---|---|---|
| 1 | Compras + Inventario | Identificación y correlación de una incidencia localizada. |
| 2 | Compras + Inventario | Disponibilidad real, reservas y déficit de stock. |
| 3 | Compras + Inventario + Fabricación | Dependencias entre componentes y órdenes de fabricación. |
| 4 | Los cuatro módulos | Impacto de la incidencia sobre los compromisos comerciales. |
| 5 | Los cuatro módulos | Investigación de alternativas y comparación de escenarios de resolución. |

## Condiciones para construir el ground truth

Cada nivel debe disponer de un conjunto de datos de referencia conocido que especifique:

- Los módulos y procesos afectados.
- Los registros relevantes que el sistema debería consultar.
- Las relaciones entre entidades y procesos que debería identificar.
- Las evidencias necesarias para justificar el diagnóstico.
- Las conclusiones y propuestas consideradas aceptables.

Las alternativas del nivel 5 deben estar representadas en los datos de Odoo. Por ejemplo, si se espera que el sistema considere una materia prima sustitutiva, esa posibilidad y sus condiciones de uso deberán estar modeladas previamente. La evaluación debe medir si el sistema recupera y utiliza correctamente la información disponible, no si inventa alternativas.

La definición actual es funcional. En una fase posterior habrá que traducir cada nivel a registros concretos de Odoo, con identificadores, cantidades, fechas, estados y relaciones verificables, para obtener un ground truth reproducible.

## Relación con la evaluación del sistema

Los recorridos de investigación realizados por los agentes se compararán con recorridos ideales definidos previamente para cada nivel. La evaluación considerará la identificación de módulos, la recuperación de evidencias, la reconstrucción de relaciones y la calidad de las propuestas.

Esta comparación permite evaluar el comportamiento del sistema frente a una referencia controlada. Por sí sola, no demuestra una mejora frente al procedimiento manual basado en Excel; para medir una reducción del tiempo o del esfuerzo humano sería necesaria una línea base manual comparable.

## Enlaces relacionados

- [[Contexto y alcance del TFG]]
- [[Arquitectura objetivo del sistema agentic]]
- [[Dependencias de módulos Odoo y datos de negocio]]
