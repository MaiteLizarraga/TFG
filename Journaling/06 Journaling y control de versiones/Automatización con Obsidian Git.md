---
type: procedimiento
area: journaling
project: TFG Odoo Agentic AI
status: planned
tags:
  - obsidian/workflow
  - documentacion/procedimiento
---

# Automatización con Obsidian Git

## Objetivo

Configurar el complemento **Obsidian Git** para reducir la necesidad de ejecutar manualmente `git commit` y `git push` cada vez que se modifica el journaling.

## Flujo objetivo

```text
Editar una nota en Obsidian
              ↓
   Obsidian Git detecta cambios
              ↓
       commit automático
              ↓
        push a GitHub
```

## Estado

- [x] Repositorio Git local inicializado.
- [x] Rama principal `main` configurada.
- [x] Remoto SSH `origin` configurado.
- [x] Autenticación SSH verificada.
- [x] Primer `push` completado.
- [ ] Instalar y configurar el complemento Obsidian Git.
- [ ] Definir la frecuencia de `commit` y `push` automáticos.
- [ ] Probar el comportamiento y verificar el historial en GitHub.

## Precauciones

Antes de activar la automatización, revisar la configuración del complemento y confirmar qué archivos se publicarán. Mantener fuera del repositorio las claves privadas, tokens y otros secretos.

Relacionado: [[GitHub como repositorio de seguimiento del TFG]].
