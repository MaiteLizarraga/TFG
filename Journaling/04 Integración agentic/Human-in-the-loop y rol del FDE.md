---
type: concepto
area: arquitectura
project: TFG Odoo Agentic AI
tags:
  - arquitectura/human-in-the-loop
  - arquitectura/multiagente
---

# Human-in-the-loop y rol del FDE

## Decisión registrada

El FDE (*Forward Deployed Engineer*) se considera un rol humano, no un agente del sistema.

## Implicación

La arquitectura debe distinguir claramente las responsabilidades de las personas y las de los agentes. La intervención humana y las reglas de aprobación concretas deberán definirse en fases posteriores si forman parte del flujo final.

El diseño contempla mantener la supervisión humana sobre las propuestas y las acciones que puedan afectar a los registros de negocio. El alcance inicial del TFG se centra en el análisis de incidencias y no presupone la ejecución autónoma de cambios en Odoo.

## Enlaces

- [[Decisiones arquitectónicas del sistema]]
- [[Agentes especializados]]
- [[Roadmap de integración]]
