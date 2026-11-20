---
type: referencia
area: journaling
project: TFG Odoo Agentic AI
status: active
tags:
  - git/estructura
  - obsidian/workflow
---

# Estructura y sincronización del repositorio

## Objetivo

El vault de Obsidian utilizado para el journaling del TFG está conectado a un repositorio privado de GitHub. El repositorio funciona como copia remota y permite revisar la evolución del trabajo y consultar el historial de versiones.

## Entorno

- Vault local: `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`
- Repositorio remoto: `MaiteLizarraga/TFG` (privado)
- Remoto Git: `origin` → `git@github.com:MaiteLizarraga/TFG.git`
- Sistema: Ubuntu (`ubuntu-tfg`)
- Git: `2.53.0`
- Rama principal: `main`
- Autenticación: SSH, verificada con `ssh -T git@github.com`

## Estructura del vault

La organización separa el conocimiento consolidado, el material provisional y la administración:

```text
TFG-Odoo-Agentic-AI/
├── Admin/                         # Excluido de Git mediante /Admin/
├── Journaling/                    # Conocimiento consolidado y estructurado
│   ├── 00 Inicio/
│   ├── 01 Proyecto y arquitectura/
│   ├── 02 Entorno e infraestructura/
│   ├── 03 Odoo API y modelos/
│   ├── 04 Integración agentic/
│   ├── 05 Registro técnico/
│   ├── 06 Journaling y control de versiones/
│   └── 90 Plantillas/
└── __WIP_to_journal/              # Notas provisionales; también se versionan
    ├── Octubre_2026/
    └── processed/
        ├── Octubre_2026/
        └── Septiembre_2026/
```

Las carpetas mensuales y sus contenidos evolucionan a medida que se procesa el diario.

## Función de cada zona

- **`Journaling/`**: conocimiento consolidado, organizado por áreas y enlazado mediante notas de Obsidian. Aquí se documentan conceptos, decisiones, procedimientos, incidencias y acuerdos duraderos.
- **`__WIP_to_journal/`**: notas diarias o material provisional pendiente de revisar y transformar en contenido estructurado. También se mantiene en el repositorio remoto.
- **`__WIP_to_journal/processed/`**: notas originales ya procesadas, que se conservan como archivo de consulta y trazabilidad.
- **`Admin/`**: contenido administrativo que debe permanecer fuera de GitHub; se excluye con la regla `/Admin/` de `.gitignore`.

## Qué se sincroniza

- `Journaling/` y `__WIP_to_journal/` se versionan en el repositorio.
- `Admin/` queda excluido mediante `/Admin/`.
- `.obsidian/` y `Welcome.md` también se excluyen según el `.gitignore` documentado.

El repositorio es privado, pero eso no convierte los archivos sincronizados en contenido exclusivamente local. No deben incluirse secretos, claves privadas, credenciales ni información que no se quiera compartir con las personas que tengan acceso al repositorio.

## Flujo de mantenimiento del vault

1. Registrar la actividad diaria en `__WIP_to_journal/<mes>/`, agrupando el trabajo por fecha.
2. Extraer del diario el conocimiento duradero y actualizar las notas temáticas adecuadas de `Journaling/`.
3. Cuando una nota diaria ya esté procesada, guardarla en `__WIP_to_journal/processed/<mes>/`.
4. Mantener los detalles de trabajo diario en la nota de esa fecha y evitar añadirlos a notas de fechas anteriores.
5. Mantener la información permanente sobre estructura, convenciones y decisiones en notas enlazadas dentro de `Journaling/`.

## Flujo de versionado y sincronización

El flujo de versionado documentado es manual:

```text
Editar o crear notas en Obsidian
              ↓
          git status
              ↓
     git add -A (preparar)
              ↓
  revisar git diff --cached
              ↓
           git commit
              ↓
       git push origin main
              ↓
        GitHub actualizado
```

Antes de preparar los cambios, comprobar las exclusiones y el contenido pendiente. Revisar el área preparada antes de confirmar el commit.

Los cambios realizados directamente en GitHub no se reflejan automáticamente en el vault local. Para traerlos a Ubuntu, ejecutar desde la raíz del vault:

```bash
git pull origin main
```

Antes del `pull`, comprobar que no haya cambios locales sin guardar o conflictos pendientes. Si existen cambios locales, deben revisarse antes de sincronizar para evitar perder trabajo.

Tras el `commit` y el `push` iniciales realizados el 28 de octubre de 2026, la estructura quedó publicada. Las actualizaciones posteriores requieren sus propios commits y pushes.

## Automatización

El flujo actual se realiza manualmente. La automatización mediante el complemento [[Automatización con Obsidian Git]] sigue siendo una tarea pendiente; no debe considerarse activa hasta instalarla, configurarla y probarla.

## Documentación relacionada

- [[Configuración local de Git para el journaling]]
- [[Autenticación SSH con GitHub]]
- [[Colaboración con ChatGPT mediante GitHub]]
- [[Taxonomía de propiedades y etiquetas]]

## Historial de organización

Tras el primer `push`, las notas del diario se agruparon bajo `Journaling/` en lugar de aparecer directamente en la raíz del repositorio. Esta estructura describe el vault de conocimiento y seguimiento del proyecto; no debe confundirse con el entorno de ejecución de Odoo ni con un segundo vault.

Las instrucciones puntuales para importar un ZIP no forman parte del conocimiento duradero del proyecto.
