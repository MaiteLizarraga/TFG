---
type: procedure
area: journaling-version-control
project: TFG Odoo Agentic AI
status: implemented
tags:
  - tfg
  - git
  - ssh
  - github
---

# Autenticación SSH con GitHub

## Problema inicial

El primer intento de conexión con GitHub por SSH fue rechazado porque Ubuntu todavía no tenía una clave SSH asociada a la cuenta.

## Generación de la clave

Se comprobó que no existía una clave SSH en `~/.ssh` y se generó una clave ED25519:

```bash
ssh-keygen -t ed25519 -C "maite.lizarraga@gmail.com"
```

Rutas generadas:

- Clave privada: `~/.ssh/id_ed25519`
- Clave pública: `~/.ssh/id_ed25519.pub`

La clave pública se añadió a GitHub como **Authentication Key**.

## Verificación

```bash
ssh -T git@github.com
```

Respuesta obtenida:

```text
Hi MaiteLizarraga! You've successfully authenticated, but GitHub does not provide shell access.
```

La respuesta confirma que la autenticación SSH funciona. El mensaje sobre el acceso shell es normal: GitHub no proporciona una shell interactiva mediante esa conexión.

## Seguridad

**No compartir ni subir la clave privada `~/.ssh/id_ed25519` al repositorio.** Solo la clave pública (`.pub`) se registra en GitHub.

Relacionado: [[Configuración local de Git para el journaling]].
