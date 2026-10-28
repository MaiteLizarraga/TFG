# Paquete incremental: Git, GitHub y journaling

Este ZIP contiene únicamente archivos que se deben incorporar o actualizar dentro del vault existente. No es una sustitución completa del vault.

## Rutas incluidas

- `Journaling/06 Journaling y control de versiones/`: notas actualizadas sobre Git, GitHub, `.gitignore`, la estructura del repositorio y el flujo de publicación.
- `__WIP_to_journal/Octubre_2026/28 OCT - Reorganización del vault y sincronización GitHub.md`: registro provisional de la sesión del 28 de octubre de 2026.

## Cómo incorporarlo

1. Haz una copia de seguridad o comprueba que el repositorio está limpio antes de extraer el ZIP.
2. Extrae el contenido en la **raíz del vault** (`TFG-Odoo-Agentic-AI`), conservando las rutas de carpetas.
3. Las notas existentes de la sección 06 se actualizan con la versión incluida en el paquete. Si has editado alguna por tu cuenta desde la última versión, compara los cambios antes de reemplazarla.
4. Abre Obsidian y comprueba las notas y los enlaces internos.
5. Desde la raíz del repositorio, revisa y publica los cambios:

   ```bash
   git status
   git add -A
   git status
   git diff --cached --stat
   git diff --cached
   git commit -m "Document vault organization and Git workflow"
   git push origin main
   git status
   ```

   Antes del commit, verifica que `Admin/` no esté preparado para publicación. `__WIP_to_journal/` sí debe aparecer en Git, según la decisión actual.

## Importante

- `Admin/` se excluye mediante `/Admin/` en `.gitignore`.
- `__WIP_to_journal/` se sincroniza con GitHub y, por tanto, forma parte del contenido del repositorio privado.
- No incluyas claves privadas, tokens, credenciales ni otros secretos.
- Este paquete actualiza un vault existente; no crea un segundo vault ni inicializa otro repositorio.