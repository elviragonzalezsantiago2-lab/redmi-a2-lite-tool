# Contributing to Redmi A2 Lite Tool

¡Gracias por tu interés en contribuir!

## Cómo reportar bugs

1. Verifica que el bug no existe ya en [Issues](https://github.com/tu-repo/issues)
2. Crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Salida esperada vs real
   - Versión de Python y SO

Ejemplo:
```
Título: Flash falla con "adb: command not found"
Descripción:
Intento flashear recovery pero recibo error.
Pasos:
1. Ejecuto: python tool.py flash recovery twrp.img --confirm
2. Recibo: adb: command not found
Entorno: Python 3.9, Windows 10
```

## Cómo sugerir features

1. Abre un [Discussion](https://github.com/tu-repo/discussions) o issue con etiqueta `enhancement`
2. Describe el caso de uso
3. Sugiere la implementación

Ejemplo:
```
Feature: Soporte para Redmi Note 10
Caso de uso: Reutilizar CLI para otros modelos Redmi
Propuesta: Añadir opción --device para seleccionar modelo
```

## Pull Requests

1. Fork el repositorio
2. Crea rama: `git checkout -b feature/tu-feature`
3. Haz cambios:
   - Sigue [PEP 8](https://pep8.org/)
   - Añade docstrings en funciones nuevas
   - Actualiza `CHANGELOG.md`
4. Prueba: `pytest -q`
5. Commit: `git commit -m "Add: Descripción clara"`
6. Push: `git push origin feature/tu-feature`
7. Abre PR en GitHub

### Reglas de commits

- Usa presente: "Add feature" (no "Added feature")
- Prefijos: `Add:`, `Fix:`, `Docs:`, `Test:`, `Refactor:`
- Sé específico: "Add --dry-run to flash" (no "Update tool")

### Checklist antes de PR

- [ ] Tests pasan: `pytest -q`
- [ ] Sin conflictos de merge
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado
- [ ] Commit messages claros

## Desarrollo local

```powershell
# 1. Clonar
git clone https://github.com/tu-repo/redmi-a2-lite-tool.git
cd redmi-a2-lite-tool

# 2. Instalar
python -m pip install -r requirements.txt

# 3. Hacer cambios
# Editar archivos...

# 4. Probar
python -m pytest -q
python tool.py --help
python gui.py

# 5. Compilar ejecutables (opcional)
python -m PyInstaller --onefile --name redmi-a2-lite-tool tool.py
python -m PyInstaller --onefile --name redmi-a2-lite-gui gui.py -w
```

## Estructura del proyecto

```
tool/
├── tool.py                  # CLI principal (~340 líneas)
├── gui.py                   # GUI Tkinter (~200 líneas)
├── requirements.txt         # Dependencias
├── tests/
│   ├── test_tool.py
│   └── test_tool_extra.py
├── README.md                # Docs básico
├── README_COMPLETE.md       # Docs completo
├── CHANGELOG.md             # Este archivo
├── LICENSE                  # MIT
└── .github/
    └── workflows/           # CI/CD (opcional)
```

## Preguntas?

- Abre un [Discussion](https://github.com/tu-repo/discussions)
- Lee `README_COMPLETE.md` para detalles
- Revisa `tool.py --help` para comandos disponibles

¡Gracias por contribuir! 🎉
