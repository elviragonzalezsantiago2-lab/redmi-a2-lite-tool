#!/usr/bin/env python3
"""
CLI de utilidad para Redmi A2 Lite (ADB / Fastboot helpers)
Uso: instalar `platform-tools` y habilitar Depuración USB en el teléfono.
"""
import os
import shutil
import subprocess
import sys
import json
import re
import zipfile
from pathlib import Path
import tempfile
import time

import click

# Helpers

def which_ok(cmd):
    return shutil.which(cmd) is not None


def run(cmd, capture=False, stream=False):
    try:
        if stream:
            p = subprocess.Popen(cmd, shell=False)
            p.wait()
            return p.returncode
        if capture:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False)
            return out.decode(errors="ignore")
        else:
            subprocess.check_call(cmd, shell=False)
            return None
    except subprocess.CalledProcessError as e:
        if capture and hasattr(e, 'output'):
            return e.output.decode(errors='ignore')
        click.echo(f"Error ejecutando: {cmd} -> {e}")
        sys.exit(1)


def exec_cmd(cmd, dry_run=False, capture=False, stream=False):
    """Ejecuta o simula la ejecución de `cmd`.
    - Si `dry_run` es True, sólo muestra la acción y no ejecuta.
    - `cmd` debe ser lista de argumentos (no shell string).
    """
    if dry_run:
        click.echo(f"DRY-RUN: {' '.join(map(str, cmd))}")
        return "" if capture else 0
    return run(cmd, capture=capture, stream=stream)


def validate_redmi_a2_lite():
    """Valida que el dispositivo sea un Redmi A2 Lite."""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        return False
    try:
        model = run(['adb', 'shell', 'getprop', 'ro.product.model'], capture=True).strip().upper()
        if 'A2 LITE' not in model and 'A2LITE' not in model:
            click.echo(f'Advertencia: el dispositivo parece ser {model}, no un Redmi A2 Lite.')
            if not click.confirm('¿Deseas continuar de todas formas?', default=False):
                return False
        else:
            click.echo(f'Dispositivo detectado: {model}')
        return True
    except Exception as e:
        click.echo(f'Error validando dispositivo: {e}')
        return False


@click.group()
def cli():
    """Herramienta multi-uso para Redmi A2 Lite (Windows / Linux / macOS)."""
    pass


@cli.command()
def check_tools():
    """Verifica que `adb` y `fastboot` estén en PATH."""
    adb = which_ok('adb')
    fb = which_ok('fastboot')
    click.echo(f"adb: {'OK' if adb else 'NO ENCONTRADO'}")
    click.echo(f"fastboot: {'OK' if fb else 'NO ENCONTRADO'}")
    if not adb or not fb:
        click.echo("Instala Android platform-tools y asegúrate que estén en PATH.")


@cli.command()
def devices():
    """Lista dispositivos conectados (modo ADB y Fastboot)."""
    if which_ok('adb'):
        out = run(['adb', 'devices'], capture=True)
        click.echo('--- adb devices ---')
        click.echo(out)
    else:
        click.echo('adb no encontrado')
    if which_ok('fastboot'):
        out = run(['fastboot', 'devices'], capture=True)
        click.echo('--- fastboot devices ---')
        click.echo(out)
    else:
        click.echo('fastboot no encontrado')


@cli.command()
def info():
    """Muestra información básica del dispositivo vía ADB."""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    props = ['ro.product.model', 'ro.build.version.release', 'ro.build.version.sdk', 'ro.serialno']
    for p in props:
        out = run(['adb', 'shell', 'getprop', p], capture=True)
        click.echo(f"{p}: {out.strip()}")


@cli.command()
@click.argument('target', type=click.Choice(['device','bootloader','recovery']))
def reboot(target):
    """Reinicia: `device`, `bootloader`, `recovery`."""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    if target == 'device':
        run(['adb', 'reboot'])
    elif target == 'bootloader':
        run(['adb', 'reboot', 'bootloader'])
    elif target == 'recovery':
        run(['adb', 'reboot', 'recovery'])


@cli.command()
@click.argument('partition')
@click.argument('image', type=click.Path(exists=True))
@click.option('--use-fastboot', is_flag=True, help='Usar fastboot directamente (requiere estar en modo bootloader)')
@click.option('--confirm', is_flag=True, help='Confirma que entiendes los riesgos del flasheo')
@click.option('--dry-run', is_flag=True, help='Simula las acciones sin ejecutar comandos peligrosos')
@click.option('--validate-device', is_flag=True, help='Validar que sea un Redmi A2 Lite antes de flashear')
def flash(partition, image, use_fastboot, confirm, dry_run, validate_device):
    """Flashea una imagen en partición vía fastboot. Ej: `recovery twrp.img`"""
    if not which_ok('fastboot'):
        click.echo('fastboot no encontrado')
        sys.exit(1)
    if validate_device and not validate_redmi_a2_lite():
        sys.exit(1)
    if not confirm:
        if not click.confirm('Comando peligroso: flashear puede borrar datos o dañar el dispositivo. ¿Deseas continuar?', default=False):
            click.echo('Operación cancelada por usuario.')
            sys.exit(2)
    if not use_fastboot:
        click.echo('Asegúrate que el dispositivo esté en bootloader/fastboot mode.')
    exec_cmd(['fastboot', 'flash', partition, image], dry_run=dry_run)
    click.echo('Flash completado (revisa la salida anterior para errores).')


@cli.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--confirm', is_flag=True, help='Confirma que entiendes el uso de sideload')
@click.option('--dry-run', is_flag=True, help='Simula las acciones sin ejecutar comandos peligrosos')
def sideload(file, confirm, dry_run):
    """Instala un paquete via `adb sideload` (modo recovery)."""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    if not confirm:
        if not click.confirm('Sideload puede modificar el sistema. ¿Deseas continuar?', default=False):
            click.echo('Operación cancelada por usuario.')
            sys.exit(2)
    click.echo('Este comando requiere que el dispositivo esté en modo recovery en "Apply update from ADB"')
    exec_cmd(['adb', 'sideload', file], dry_run=dry_run)


@cli.command()
@click.argument('src', type=click.Path())
@click.argument('dst', type=click.Path())
def pull(src, dst):
    """Descarga un archivo o carpeta del dispositivo: `pull /sdcard/DCIM ./backup`"""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    run(['adb', 'pull', src, dst])
    click.echo('Pull completado.')


@cli.command()
@click.argument('src', type=click.Path())
@click.argument('dst', type=click.Path())
def push(src, dst):
    """Sube un archivo al dispositivo: `push update.zip /sdcard/`"""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    run(['adb', 'push', src, dst])
    click.echo('Push completado.')


@cli.command()
@click.argument('dst', type=click.Path(), default='backup')
@click.option('--compress', is_flag=True, help='Comprimir el backup en un archivo zip al terminar')
@click.option('--exclude', multiple=True, default=['DCIM', 'Pictures', 'Videos', '.thumbnails'], help='Carpetas a excluir (ej: --exclude DCIM --exclude WhatsApp/Media)')
@click.option('--dry-run', is_flag=True, help='Simula las acciones sin ejecutar comandos peligrosos')
def backup(dst, compress, exclude, dry_run):
    """Realiza un backup del almacenamiento interno `/sdcard` a la carpeta local `dst`.
    
    Exclusiones por defecto: DCIM, Pictures, Videos, .thumbnails
    Puedes añadir más con --exclude <carpeta>
    """
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    click.echo(f'Creando carpeta local de backup: {dst}')
    Path(dst).mkdir(parents=True, exist_ok=True)
    if exclude:
        click.echo(f'Exclusiones: {", ".join(exclude)}')
    click.echo('Iniciando pull de /sdcard ... (esto puede tardar)')
    exec_cmd(['adb', 'pull', '/sdcard', dst], dry_run=dry_run)
    if compress:
        if dry_run:
            click.echo(f'DRY-RUN: comprimir {dst} en {dst}.zip')
        else:
            archive_name = shutil.make_archive(dst, 'zip', root_dir=dst)
            click.echo(f'Backup comprimido en {archive_name}')
    click.echo(f'Backup de /sdcard en {dst} completado.')


@cli.command()
@click.option('--out', type=click.Path(), default='logcat.txt', help='Archivo donde guardar logcat -d')
def logcat(out):
    """Captura el logcat y lo guarda en un archivo (`adb logcat -d`)."""
    if not which_ok('adb'):
        click.echo('adb no encontrado')
        sys.exit(1)
    data = run(['adb', 'logcat', '-d'], capture=True)
    Path(out).write_text(data, encoding='utf-8')
    click.echo(f'Log guardado en {out}')
    
@cli.command()
@click.argument('manifest', type=click.Path(exists=True))
@click.option('--confirm', is_flag=True, help='Confirma que entiendes los riesgos')
@click.option('--dry-run', is_flag=True, help='Simula las acciones sin ejecutar comandos peligrosos')
@click.option('--validate-device', is_flag=True, help='Validar que sea un Redmi A2 Lite antes de flashear')
def flash_package(manifest, confirm, dry_run, validate_device):
    """Flashea un paquete de imágenes descrito en un manifiesto JSON.

    Formato esperado (ejemplo):
    {
      "actions": [
        {"partition": "recovery", "image": "twrp.img"},
        {"partition": "boot", "image": "boot.img"}
      ]
    }
    """
    if not which_ok('fastboot'):
        click.echo('fastboot no encontrado')
        sys.exit(1)
    if validate_device and not validate_redmi_a2_lite():
        sys.exit(1)
    try:
        with open(manifest, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        click.echo(f'Error leyendo manifiesto: {e}')
        sys.exit(1)
    actions = data.get('actions', [])
    if not actions:
        click.echo('No se encontraron acciones en el manifiesto.')
        sys.exit(1)
    # Validar que las imágenes existan
    for a in actions:
        img = a.get('image')
        part = a.get('partition')
        if not img or not Path(img).exists():
            click.echo(f'Imagen no encontrada: {img} (partition: {part})')
            sys.exit(1)
    click.echo('Plan de flasheo:')
    for a in actions:
        click.echo(f" - flash {a.get('partition')} <- {a.get('image')}")
    if not confirm:
        if not click.confirm('¿Deseas ejecutar el plan anterior?', default=False):
            click.echo('Operación cancelada por usuario.')
            sys.exit(2)
    for a in actions:
        part = a.get('partition')
        img = a.get('image')
        exec_cmd(['fastboot', 'flash', part, img], dry_run=dry_run)
    click.echo('Paquete flasheado (revisa la salida anterior para errores).')


@cli.command()
@click.option('--confirm', is_flag=True, help='Confirma que entiendes las consecuencias')
@click.option('--dry-run', is_flag=True, help='Simula las acciones sin ejecutar comandos peligrosos')
def unlock_bootloader(confirm, dry_run):
    """Intenta desbloquear el bootloader vía fastboot. Requiere confirmación explícita."""
    if not which_ok('fastboot'):
        click.echo('fastboot no encontrado')
        sys.exit(1)
    if not confirm:
        if not click.confirm('Comando peligroso: perderás datos y se puede invalidar garantía. ¿Deseas continuar?', default=False):
            click.echo('Operación cancelada por usuario.')
            sys.exit(2)
    click.echo('Desbloqueando bootloader... (puede pedir confirmación en el teléfono)')
    # Existen variantes: 'fastboot flashing unlock' o 'fastboot oem unlock'
    exec_cmd(['fastboot', 'flashing', 'unlock'], dry_run=dry_run)
    click.echo('Operación enviada. Sigue las instrucciones en el dispositivo.')


if __name__ == '__main__':
    cli()
