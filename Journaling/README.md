# Bóveda Obsidian — TFG Odoo Agentic AI

Este paquete contiene notas Markdown enlazadas, mapas de contenido (MOC), un dashboard inicial y plantillas para documentar el TFG.

## Cómo incorporarlo

1. Descomprime la carpeta `Obsidian_TFG_Odoo_Agentic_AI`.
2. Copia sus carpetas dentro de la bóveda que ya utilizas en Obsidian.
3. Abre Obsidian y comprueba que aparecen las notas.
4. En **Settings → Core plugins**, activa **Templates**.
5. En **Settings → Templates**, configura `90 Plantillas` como `Template folder location`.
6. Abre `00 Inicio/Inicio - TFG Odoo Agentic AI.md` como página inicial.
7. En **Graph view**, abre el grafo global. Para explorar un área, abre su MOC y utiliza **Local graph**.

## Qué incluye

- Dashboard de inicio con tareas.
- MOC de proyecto/arquitectura, infraestructura, API/modelos, integración agentic y registro técnico.
- Notas atómicas con propiedades YAML y enlaces internos `[[...]]`.
- Registro de decisiones, conceptos, procedimientos, pruebas y problemas.
- Plantillas para conceptos, procedimientos, incidencias, decisiones y sesiones de trabajo.
- Convención de propiedades y etiquetas en [[Taxonomía de propiedades y etiquetas]].

## Convenciones de documentación

- `type` clasifica la nota; `area` indica su ámbito principal.
- `tags` describe conceptos técnicos con etiquetas jerárquicas breves, por ejemplo `odoo/api` o `integracion/mcp`.
- Los enlaces internos y los MOC representan las relaciones entre notas.
- La taxonomía se mantiene en [[Taxonomía de propiedades y etiquetas]].

## Importante

- Las notas reflejan el contenido del documento fuente y diferencian los componentes implementados de los planificados.
- La fecha de estado procede del documento original (septiembre de 2026); verifica los datos si el entorno ha cambiado.
- No se incluyen valores reales de API Keys.
- El documento fuente incluía credenciales de demostración para PostgreSQL/Odoo. No se reproducen como una contraseña operativa en estas notas; revisa `compose.yaml` local y no subas secretos a Git.
- Se ha señalado como recomendación de seguridad revisar la publicación de PostgreSQL en `0.0.0.0` y `[::]`.
- Los enlaces a notas que no forman parte de este paquete se han evitado, salvo marcadores de posición en las plantillas.
