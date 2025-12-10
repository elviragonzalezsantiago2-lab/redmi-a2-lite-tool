# Redmi A2 Lite Tool

Herramienta completa multi-plataforma para gestionar dispositivos **Redmi A2 Lite** usando ADB, Fastboot y Python.

## Características

✅ **CLI avanzada** (`tool.py`) con comandos completos para ADB/Fastboot
✅ **Interfaz gráfica** (`gui.py`) con PySimpleGUI — amigable para usuarios
✅ **Ejecutables compilados** (`redmi-a2-lite-tool.exe`, `redmi-a2-lite-gui.exe`)
✅ **Validaciones de dispositivo** — verifica que sea un Redmi A2 Lite
✅ **Modo `--dry-run`** — simula operaciones peligrosas sin ejecutar
✅ **Confirmaciones interactivas** — seguridad en operaciones críticas
✅ **Backup inteligente** — con compresión ZIP y exclusiones configurables
✅ **Flasheo automatizado** — via manifiesto JSON
✅ **Suite de pruebas** (`pytest`) — validación de funciones

## Instalación rápida

### Opción 1: Usar ejecutables precompilados (Recomendado para usuarios)

```powershell
# CLI (terminal)
.\dist\redmi-a2-lite-tool.exe --help

# GUI (interfaz gráfica)
.\dist\redmi-a2-lite-gui.exe
```

### Opción 2: Desde código fuente (Desarrollo)

```powershell
# 1. Instalar Python 3.8+ si no lo tienes
# 2. Clonar/descargar el repositorio

cd "c:\Users\Santiago\OneDrive\Desktop\tool"

# 3. Instalar dependencias
python -m pip install -r requirements.txt

# 4. Ejecutar CLI
python tool.py --help

# 5. O lanzar GUI
python gui.py
```

## Uso

### CLI - Comandos principales

```powershell
# Verificar herramientas y dispositivos
python tool.py check-tools
python tool.py devices
python tool.py info

# Reiniciar dispositivo
python tool.py reboot device      # Sistema normal
python tool.py reboot bootloader  # Modo fastboot
python tool.py reboot recovery    # Modo recovery

# Transferencia de archivos
python tool.py pull /sdcard/DCIM ./backup      # Descargar
python tool.py push archivo.zip /sdcard/       # Subir

# Backup con compresión y exclusiones
python tool.py backup ./mi_backup --compress --exclude DCIM --exclude Videos

# Sideload (OTA en recovery)
python tool.py sideload update.zip --confirm --dry-run

# Flasheo de imágenes
python tool.py flash recovery twrp.img --confirm --dry-run --validate-device

# Flasheo de paquete (múltiples imágenes)
python tool.py flash-package manifest.json --confirm --validate-device

# Desbloqueo de bootloader (peligroso)
python tool.py unlock-bootloader --confirm --dry-run

# Capturar logcat
python tool.py logcat --out debug.txt
```

### GUI

```powershell
python gui.py
```

Interfaz intuitiva con botones para:
- Información del dispositivo
- Reiniciar (Sistema / Bootloader / Recovery)
- Transferencia de archivos (Pull/Push)
- Backup y Logcat
- Flasheo avanzado (imagen, paquete)

## Ejemplos prácticos

### Backup completo de /sdcard con compresión

```powershell
python tool.py backup ./sdcard_backup --compress
```

Resultado: `./sdcard_backup/` y `./sdcard_backup.zip`

### Flashear TWRP en Redmi A2 Lite (con validación)

```powershell
# 1. Descargar TWRP compatible para Redmi A2 Lite
# 2. Copiar a carpeta del proyecto como "twrp.img"
# 3. Ejecutar:
python tool.py flash recovery twrp.img --confirm --validate-device
```

### Flashear ROM completa via manifiesto

Crear `rom-manifest.json`:

```json
{
  "actions": [
    {"partition": "recovery", "image": "twrp.img"},
    {"partition": "boot", "image": "boot.img"},
    {"partition": "system", "image": "system.img"}
  ]
}
```

Ejecutar:

```powershell
python tool.py flash-package rom-manifest.json --confirm --validate-device
```

### Modo simulación (--dry-run)

Prueba todas las operaciones sin ejecutarlas realmente:

```powershell
python tool.py flash recovery twrp.img --confirm --dry-run
# Salida: DRY-RUN: fastboot flash recovery twrp.img
```

## Opciones avanzadas

| Opción | Uso | Ejemplo |
|--------|-----|---------|
| `--confirm` | Omitir confirmación interactiva | `flash ... --confirm` |
| `--dry-run` | Simular sin ejecutar (seguro) | `flash ... --dry-run` |
| `--validate-device` | Verificar que sea Redmi A2 Lite | `flash ... --validate-device` |
| `--compress` | Comprimir backup en ZIP | `backup ... --compress` |
| `--exclude` | Excluir carpetas del backup | `backup ... --exclude DCIM --exclude Videos` |

## Seguridad

⚠️ **Advertencias importantes:**

1. **Desbloqueo de bootloader** → Perderás datos y puede invalidar garantía
2. **Flasheo de ROM** → Riesgo de "brick" (dispositivo inutilizable)
3. **Sideload** → Modifica el sistema operativo
4. **Todos requieren ADB/Fastboot** → El dispositivo debe estar conectado y en modo correcto

✅ **Medidas de seguridad integradas:**

- Confirmaciones interactivas obligatorias (salvo `--confirm` explícito)
- Validación de dispositivo con `--validate-device`
- Modo `--dry-run` para simular antes de ejecutar
- Archivos `.img` deben existir antes de flashear
- Reversión de cambios no siempre es posible

## Desarrollo

### Ejecutar pruebas

```powershell
python -m pytest -q
# Salida esperada: 3 passed
```

### Recompilar ejecutables

```powershell
# CLI
python -m PyInstaller --onefile --name redmi-a2-lite-tool tool.py

# GUI
python -m PyInstaller --onefile --name redmi-a2-lite-gui gui.py -w
```

### Estructura del proyecto

```
tool/
├── tool.py                  # CLI principal (Click)
├── gui.py                   # Interfaz gráfica (PySimpleGUI)
├── requirements.txt         # Dependencias Python
├── README.md                # Este archivo
├── .gitignore               # Configuración Git
├── tests/
│   ├── test_tool.py         # Tests básicos
│   └── test_tool_extra.py   # Tests avanzados (dry-run, flash-package)
├── dist/
│   ├── redmi-a2-lite-tool.exe   # Ejecutable CLI compilado
│   └── redmi-a2-lite-gui.exe    # Ejecutable GUI compilado
├── build/                   # Directorios de compilación (PyInstaller)
└── redmi-a2-lite-tool.spec  # Especificación PyInstaller
```

## Roadmap futuro

- [ ] Soporte para más dispositivos Redmi (A2, Note series, etc.)
- [ ] Autodetección de imágenes y firmware oficiales
- [ ] Modo batch/script para automatización
- [ ] Integración con gestor de paquetes (Chocolatey, scoop)
- [ ] Documentación de particiones específicas del Redmi A2 Lite
- [ ] Notificaciones del sistema (progreso en background)

## Requisitos previos

1. **Android platform-tools** (ADB + Fastboot)
   - Windows: Descargar desde [Google](https://developer.android.com/tools/releases/platform-tools)
   - Añadir a PATH

2. **Python 3.8+** (si usas código fuente)
   - Descargar desde [python.org](https://www.python.org/downloads/)

3. **Dispositivo Redmi A2 Lite**
   - Activar "Opciones de desarrollador" (pulsar 7 veces "Versión de compilación" en Ajustes)
   - Habilitar "Depuración USB"
   - Conectar por USB al PC

## Troubleshooting

### "adb no encontrado"
```
Solución: Instala platform-tools e añade a PATH
```

### "Device offline" en adb
```
Solución: Desconectar/reconectar USB, confiar en la computadora (popup en teléfono)
```

### "fastboot no encontrado"
```
Solución: Reiniciar PC en bootloader: `adb reboot bootloader`
```

### Duda sobre imagen oficial del Redmi A2 Lite
```
Buscar en: https://xiaomifirm.com/ o comunidades Redmi
```

## Licencia

Código educativo. Úsalo bajo tu responsabilidad.

## Contribuciones

PRs bienvenidos. Por favor:
1. Prueba localmente (`pytest`)
2. Añade tests para nuevas funciones
3. Documenta cambios en `README.md`

---

**Creado con ❤️ para usuarios de Redmi A2 Lite**

¿Preguntas? Revisa `tool.py --help` o `python tool.py <comando> --help` para detalles específicos.
