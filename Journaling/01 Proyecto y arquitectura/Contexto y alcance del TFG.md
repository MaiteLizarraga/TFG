---
type: concepto
area: proyecto
status: active
project: TFG Odoo Agentic AI
tags:
  - arquitectura/multiagente
  - odoo/modulos
---

# Contexto, alcance y ERP del TFG

## 1. Objetivo del proyecto

Desarrollar un sistema de **Agentic AI para la gestión de incidencias de Supply Chain**, utilizando un ERP realista como sistema de información empresarial.

El sistema agentic complementará al ERP: no lo sustituirá ni accederá directamente a su base de datos. Su función será investigar incidencias, correlacionar información de distintas áreas funcionales, reunir evidencias y generar propuestas para su revisión humana.

## 2. ERP seleccionado: Odoo 19 Community

Se ha seleccionado **Odoo 19 Community** como ERP de referencia para representar un sistema de información empresarial realista.

Odoo mantiene los datos y ejecuta su lógica de negocio. La capa agentic se integra con el ERP mediante su API externa JSON-2 y el ORM, respetando los permisos y las reglas de acceso de Odoo. No se contempla el acceso directo de los agentes a PostgreSQL.

### Módulos funcionales incluidos

| Área funcional | Módulo técnico |
|---|---|
| Ventas | `sale_management` |
| Compras | `purchase` |
| Inventario | `stock` |
| Fabricación | `mrp` |

Odoo puede instalar dependencias técnicas de estos módulos. Estas dependencias no se consideran áreas funcionales adicionales del proyecto.

### Entorno de referencia

- **Versión:** Odoo 19 Community.
- **Base de datos de trabajo:** `Odoo-tfg`.
- **Acceso web local:** `http://localhost:8069`.
- **API utilizada:** JSON-2.

La configuración del entorno, la instalación de módulos y las pruebas de acceso a la API se documentan en los apartados técnicos específicos del vault.

## 3. Alcance funcional y límites

El proyecto se centra en la gestión de incidencias de cadena de suministro que requieren relacionar información de Compras, Inventario, Fabricación y Ventas.

El sistema deberá investigar la información relevante, identificar relaciones entre registros, reunir evidencias y formular propuestas fundamentadas. En el alcance inicial, los agentes dispondrán de herramientas de consulta y **no ejecutarán modificaciones en Odoo**.

### Fuera de alcance según las decisiones actuales

- Software Engineer Agent.
- QA Agent.
- Acceso directo de los agentes a PostgreSQL.
- Desarrollo de módulos Python ad hoc dentro de Odoo para resolver la integración.
- Sustitución del ERP o de su lógica de negocio por el sistema agentic.
- Ejecución autónoma de cambios o transacciones en Odoo.

## 4. Documentación relacionada

- [[Decisiones arquitectónicas del sistema]] — decisiones de diseño y arquitectura general.
- [[Diseño de orquestación, Jev, agentes y evaluación]] — responsabilidades, herramientas, integración, observabilidad y KPI.
- [[Escenarios de evaluación - cinco niveles de complejidad]] — incidencia de referencia y niveles de complejidad.
- [[Instalación de los módulos funcionales]] — instalación y configuración de los módulos.
- [[Dependencias de módulos Odoo y datos de negocio]] — dependencias técnicas y relaciones de negocio.
- [[API JSON-2 de Odoo]] — interfaz externa utilizada para la integración.
- [[Separación entre API, ORM y PostgreSQL]] — separación de responsabilidades y acceso a datos.
- [[Roadmap de integración]] — fases previstas de implementación.
