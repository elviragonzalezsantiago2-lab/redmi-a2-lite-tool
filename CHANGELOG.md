# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-10

### Added
- **CLI completa** (`tool.py`) con 11+ comandos ADB/Fastboot
  - `check-tools`: Verificar adb/fastboot en PATH
  - `devices`: Listar dispositivos conectados
  - `info`: Información del dispositivo
  - `reboot`: Reiniciar (device/bootloader/recovery)
  - `pull`: Descargar archivos
  - `push`: Subir archivos
  - `backup`: Backup de /sdcard con compresión y exclusiones
  - `logcat`: Capturar logs del sistema
  - `flash`: Flashear imágenes individuales
  - `flash-package`: Flashear paquetes vía manifiesto JSON
  - `sideload`: Instalar OTA en recovery
  - `unlock-bootloader`: Desbloquear bootloader (peligroso)

- **GUI gráfica** (`gui.py`) con Tkinter
  - 5 tabs: Información, Control, Archivos, Backup, Flasheo
  - Diálogos para entrada de datos
  - Output log en tiempo real
  - Threads para no bloquear UI

- **Seguridad**
  - Confirmaciones interactivas en operaciones críticas
  - Opción `--confirm` para bypass de prompts
  - Opción `--dry-run` para simular operaciones
  - Opción `--validate-device` para verificar que sea Redmi A2 Lite
  - Validación de archivos antes de flasheo

- **Features avanzadas**
  - Backup con compresión ZIP
  - Exclusiones configurables en backup (DCIM, Videos, etc.)
  - Flasheo automatizado vía manifiesto JSON
  - Soporte para múltiples particiones

- **Packaging & Distribution**
  - Ejecutables compilados con PyInstaller
    - `redmi-a2-lite-tool.exe` (7.8 MB)
    - `redmi-a2-lite-gui.exe` (9.4 MB)
  - Sin dependencias externas (Tkinter incluido con Python)

- **Testing**
  - Suite de pruebas con pytest
  - Tests para CLI básica y operaciones avanzadas
  - Validación de dry-run y flash-package

- **Documentation**
  - `README.md`: Guía básica en español
  - `README_COMPLETE.md`: Documentación completa (400+ líneas)
  - `CHANGELOG.md`: Historial de cambios
  - `LICENSE`: MIT + disclaimer

- **Version Control**
  - Repositorio Git inicializado
  - `.gitignore` completo
  - Commits organizados y descriptivos

### Changed
- GUI migrada de PySimpleGUI (pago) a Tkinter (gratis)

### Fixed
- Compatibilidad con Python 3.8+
- Manejo de rutas en Windows (OneDrive)

### Verified
- ✅ 3/3 pruebas unitarias pasan
- ✅ CLI funciona sin adb/fastboot (modo simulación)
- ✅ GUI lanza sin errores
- ✅ Ejecutables compilados y probados

---

## Notas para futuras versiones

### v1.1.0 (Planned)
- [ ] Soporte para más modelos Redmi (A2, Note series)
- [ ] Auto-detección de firmware oficial
- [ ] Progreso visual en operaciones largas
- [ ] Exportar logs en HTML/PDF

### v2.0.0 (Future)
- [ ] API REST para control remoto
- [ ] Dashboard web (Flask/FastAPI)
- [ ] Integración con CI/CD (GitHub Actions)
- [ ] Plugin system para extensiones

---

## Instalación & Uso

Ver `README_COMPLETE.md` para instrucciones detalladas.

### Rápido
```powershell
# Ejecutable directo
.\dist\redmi-a2-lite-tool.exe --help
.\dist\redmi-a2-lite-gui.exe
```

### Desde código
```powershell
python -m pip install -r requirements.txt
python tool.py --help
python gui.py
```

---

## Contribuciones

PRs bienvenidos. Asegúrate de:
1. Pasar todas las pruebas: `pytest`
2. Documentar nuevas features
3. Seguir el estilo del código (PEP 8)
