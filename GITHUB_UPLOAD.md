# Instrucciones para subir a GitHub

## Paso 1: Crear repositorio en GitHub

1. Ve a [github.com](https://github.com) e inicia sesión
2. Click en **"+"** → **"New repository"**
3. Nombre: `redmi-a2-lite-tool`
4. Descripción: `Herramienta completa para Redmi A2 Lite (ADB/Fastboot/GUI)`
5. **NO** inicialices con README (ya lo tienes)
6. Click **"Create repository"**

## Paso 2: Conectar repo local a GitHub

Copia y ejecuta en PowerShell:

```powershell
cd "c:\Users\Santiago\OneDrive\Desktop\tool"

# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/redmi-a2-lite-tool.git

# Si ya existe remote, actualiza:
# git remote set-url origin https://github.com/TU_USUARIO/redmi-a2-lite-tool.git

git branch -M main
git push -u origin main
```

## Paso 3: Subir tag (versión)

```powershell
git push origin v1.0.0
```

## Paso 4: Crear Release en GitHub

1. Ve a tu repo en GitHub
2. Click en **"Releases"** en la barra derecha
3. Click **"Create a new release"**
4. Tag version: `v1.0.0`
5. Release title: `Redmi A2 Lite Tool v1.0.0`
6. Descripción (copiar de CHANGELOG.md):
   ```
   🎉 Primera versión estable!
   
   ### Features:
   - CLI completa con 11+ comandos ADB/Fastboot
   - GUI gráfica con Tkinter (gratis, sin dependencias)
   - Ejecutables compilados (.exe)
   - Suite de tests
   - Documentación completa en español
   - Seguridad: confirmaciones, dry-run, validaciones
   
   ### Downloads:
   - `redmi-a2-lite-tool.exe` - CLI para terminal
   - `redmi-a2-lite-gui.exe` - Interfaz gráfica
   
   Ver CHANGELOG.md para detalles completos.
   ```
7. Drag & drop (o "Upload files"):
   - `dist/redmi-a2-lite-tool.exe`
   - `dist/redmi-a2-lite-gui.exe`
8. Click **"Publish release"**

## Alternativa: Usar GitHub CLI (más rápido)

Si tienes GitHub CLI instalado:

```powershell
# Login
gh auth login

# Crear release con archivos
gh release create v1.0.0 dist/redmi-a2-lite-tool.exe dist/redmi-a2-lite-gui.exe `
  --title "Redmi A2 Lite Tool v1.0.0" `
  --notes "Primera versión estable con CLI, GUI y tests. Ver CHANGELOG.md"
```

## Paso 5: Compartir

Una vez publicado, puedes compartir:
- Repo: `https://github.com/TU_USUARIO/redmi-a2-lite-tool`
- Release: `https://github.com/TU_USUARIO/redmi-a2-lite-tool/releases/tag/v1.0.0`
- Raw .exe: `https://github.com/TU_USUARIO/redmi-a2-lite-tool/releases/download/v1.0.0/redmi-a2-lite-tool.exe`

## Opcionales: Mejorar visibilidad

1. **Badge en README** (añadir a `README_COMPLETE.md`):
   ```markdown
   [![GitHub release](https://img.shields.io/github/v/release/TU_USUARIO/redmi-a2-lite-tool?style=flat-square)](https://github.com/TU_USUARIO/redmi-a2-lite-tool/releases)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   [![Tests](https://github.com/TU_USUARIO/redmi-a2-lite-tool/workflows/Tests%20&%20Build/badge.svg)](https://github.com/TU_USUARIO/redmi-a2-lite-tool/actions)
   ```

2. **Añadir topics** en settings del repo:
   - `redmi`, `adb`, `fastboot`, `android`, `tool`, `gui`, `python`

3. **Star en README** si quieres que otros den like:
   ```markdown
   ⭐ Si te resulta útil, dale una estrella en GitHub
   ```

---

**¿Necesitas ayuda con algo específico?** Pregunta en Discord, Reddit o GitHub Issues.
