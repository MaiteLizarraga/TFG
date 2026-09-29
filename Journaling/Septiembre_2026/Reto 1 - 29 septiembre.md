# Configuración de Git y GitHub para el Journaling del TFG

## Objetivo

Configurar el Vault de Obsidian utilizado para el journaling del TFG como un repositorio Git conectado a GitHub, de forma que el tutor pueda consultar la evolución del trabajo, revisar los cambios y acceder al historial de versiones.

El objetivo no es únicamente disponer de una copia de seguridad, sino utilizar GitHub como **repositorio de seguimiento y versionado del desarrollo del TFG**.

## Entorno

- **Vault de Obsidian:** `/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI`
    
- **Repositorio GitHub:** `MaiteLizarraga/TFG`
    
- **Repositorio GitHub:** privado
    
- **Sistema:** Ubuntu (`ubuntu-tfg`)
    
- **Git:** 2.53.0
    
- **Rama principal:** `main`
    

## 1. Comprobación de Git

Se comprobó que Git ya estaba instalado:

```bash
git --version
```

Resultado:

```text
git version 2.53.0
```

También se comprobó la identidad configurada globalmente para los commits:

```text
Name:  Maite Lizarraga
Email: maite.lizarraga@gmail.com
```

## 2. Revisión inicial del Vault

El contenido inicial del Vault era:

```text
TFG-Odoo-Agentic-AI/
├── .obsidian/
├── Septiembre_2026/
└── Welcome.md
```

Se decidió no incluir en Git:

- `.obsidian/` → configuración interna de Obsidian.
    
- `Welcome.md` → nota de bienvenida generada por Obsidian, no relevante para el journaling del TFG.
    

## 3. Creación del `.gitignore`

Se creó el archivo `.gitignore` con:

```text
.obsidian/
Welcome.md
```

De esta forma, estos archivos no se incorporan al repositorio.

Se comprobó posteriormente mediante `git status` que Git únicamente detectaba:

```text
.gitignore
Septiembre_2026/
```

por lo que el `.gitignore` estaba funcionando correctamente.

## 4. Inicialización del repositorio local

Se inicializó Git dentro del Vault:

```bash
git init
```

Git creó correctamente el repositorio local:

```text
/home/maite/odoo-tfg/docs/journal/TFG-Odoo-Agentic-AI/.git/
```

La rama inicial se cambió de `master` a `main`.

## 5. Primer commit

Se añadieron los archivos:

```bash
git add .
```

y se creó el primer commit:

```bash
git commit -m "added Obsidian Journaling"
```

Commit inicial:

```text
0ae1d81 added Obsidian Journaling
```

Git confirmó que se habían incluido únicamente:

```text
.gitignore
Septiembre_2026/Reto 1 - 27, 28 y 29 septiembre 2026.md
```

No se incluyeron `.obsidian/` ni `Welcome.md`.

## 6. Conexión con GitHub

Se configuró como repositorio remoto:

```bash
git remote add origin git@github.com:MaiteLizarraga/TFG.git
```

Inicialmente, GitHub rechazó la conexión mediante SSH porque Ubuntu no disponía todavía de una clave SSH asociada a la cuenta.

## 7. Configuración de autenticación SSH

Se comprobó que no existía una clave SSH en `~/.ssh`.

Se generó una nueva clave ED25519:

```bash
ssh-keygen -t ed25519 -C "maite.lizarraga@gmail.com"
```

La clave se creó en:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

La clave pública se añadió a la cuenta de GitHub como **Authentication Key**.

Se verificó posteriormente la autenticación:

```bash
ssh -T git@github.com
```

Resultado:

```text
Hi MaiteLizarraga! You've successfully authenticated, but GitHub does not provide shell access.
```

Por tanto, la autenticación SSH quedó correctamente configurada.

> La clave privada `~/.ssh/id_ed25519` no se comparte ni se sube nunca al repositorio.

## 8. Primer push a GitHub

Una vez configurada la autenticación SSH, se ejecutó:

```bash
git push -u origin main
```

El primer commit quedó publicado en el repositorio privado:

```text
MaiteLizarraga/TFG
```

## 9. Organización de la estructura del repositorio

Después del primer push se decidió mejorar la estructura del repositorio para evitar que las carpetas correspondientes a cada mes aparezcan directamente en la raíz.

Estructura inicial:

```text
TFG/
└── Septiembre_2026/
```

Se reorganizó a:

```text
TFG/
└── Journaling/
    └── Septiembre_2026/
        └── Reto 1 - 27, 28 y 29 septiembre 2026.md
```

Para ello se creó `Journaling` y se movió la carpeta:

```bash
mkdir Journaling
mv Septiembre_2026 Journaling/
```

Como el primer commit ya había sido publicado en GitHub, esta reorganización se registró mediante un nuevo commit, en lugar de modificar el commit anterior.

## Estado actual

El Vault de Obsidian está conectado con el repositorio privado de GitHub:

```text
Obsidian Vault
      │
      ▼
     Git
      │
      ▼
GitHub: MaiteLizarraga/TFG
```

La estructura relevante es:

```text
TFG-Odoo-Agentic-AI/
├── .git/
├── .gitignore
└── Journaling/
    └── Septiembre_2026/
        └── Reto 1 - 27, 28 y 29 septiembre 2026.md
```

La configuración permite que el historial del journaling quede versionado mediante Git y sea consultable en GitHub.

## Siguiente paso

El siguiente paso será configurar **Obsidian Git** para automatizar el proceso de `commit` y `push`, evitando tener que ejecutar manualmente los comandos Git cada vez que se modifica el journaling.

El objetivo final será:

```text
Modificar el journaling en Obsidian
              ↓
        Git detecta cambios
              ↓
            commit
              ↓
             push
              ↓
        GitHub actualizado
              ↓
      Tutor puede revisar
       la evolución del TFG
```