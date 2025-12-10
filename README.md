# Herramienta para Redmi A2 Lite

Esta es una utilidad CLI mínima en Python que agrupa comandos comunes para trabajar con un dispositivo Android (ej. Redmi A2 Lite).

Requisitos
- Tener instaladas las Android `platform-tools` (adb, fastboot) y que estén en `PATH`.
- Activar `Opciones de desarrollador` y `Depuración USB` en el dispositivo.
- Python 3.8+ (Windows PowerShell: usar `python` en PATH).

Instalación rápida (Windows PowerShell):

```powershell
cd "c:\Users\Santiago\OneDrive\Desktop\tool"
python -m pip install -r requirements.txt
# Asegúrate que adb/fastboot estén instalados y en PATH
.\\run-tool.ps1 check-tools
```

Uso
- `python tool.py check_tools` : Verifica `adb` y `fastboot`.
- `python tool.py devices` : Lista dispositivos en ADB y Fastboot.
- `python tool.py info` : Muestra propiedades básicas del dispositivo.
- `python tool.py reboot device|bootloader|recovery` : Reinicios.
- `python tool.py pull <src> <dst>` : Descarga archivos desde el dispositivo.
- `python tool.py push <src> <dst>` : Sube archivos al dispositivo.
- `python tool.py sideload <file>` : Sideload via ADB (modo recovery).
- `python tool.py flash <partition> <image>` : Flashea una imagen con fastboot.
- `python tool.py logcat --out archivo.txt` : Guarda `adb logcat -d` en un archivo.
- `python tool.py unlock_bootloader --confirm` : Desbloquea bootloader (peligroso).
 - `python tool.py flash <partition> <image> --confirm [--dry-run]` : Flashea una imagen con fastboot. Añade `--dry-run` para simular.
 - `python tool.py sideload <file> --confirm [--dry-run]` : Sideload via ADB (modo recovery). Añade `--dry-run` para simular.
 - `python tool.py backup [dst] [--compress] [--dry-run]` : Backup de `/sdcard` a carpeta local; `--compress` comprime el backup.
 - `python tool.py flash-package <manifest.json> --confirm [--dry-run]` : Flashea varias imágenes descritas en un manifiesto JSON.

Advertencias y notas
- Muchas operaciones (flasheo, desbloqueo) borran datos y pueden invalidar garantía.
- No uses esta herramienta para intentar bypass de bloqueos (FRP, bloqueo de pantalla) ni actividades ilegales.
- Antes de usar `unlock_bootloader` o `fastboot flash` asegúrate de entender los riesgos.

Siguientes mejoras posibles
- Añadir confirmaciones interactivas y backups automáticos.
- Integración con imágenes específicas para `Redmi A2 Lite` (TWRP, firmware stock).
- Implementar streaming de `adb logcat` en tiempo real y filtro por tags.

Seguridad y nuevas opciones añadidas
- `--confirm`: muchas operaciones peligrosas requieren confirmación interactiva o pasar `--confirm` para omitir la pregunta.
- `--dry-run`: simula las acciones peligrosas (muestra los comandos que se ejecutarían).
- `backup --compress`: comprime el backup en un archivo `.zip`.

Ejemplo de manifiesto para `flash-package`:

```
{
	"actions": [
		{"partition": "recovery", "image": "twrp.img"},
		{"partition": "boot", "image": "boot.img"}
	]
}
```

Ejemplo de uso (simular flasheo de paquete):

```powershell
python .\tool.py flash-package manifest.json --confirm --dry-run
```

Si quieres, puedo:
- Añadir soporte para flasheo de paquetes concretos del Redmi A2 Lite.
- Añadir un modo gráfico (Electron/PySimpleGUI) para Windows.
- Implementar más comandos seguros (backup completo, ver particiones).

