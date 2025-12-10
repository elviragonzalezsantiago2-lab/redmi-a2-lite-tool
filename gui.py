#!/usr/bin/env python3
"""
GUI para Redmi A2 Lite Tool
Interfaz gráfica usando Tkinter (incluido con Python, sin costo).
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.simpledialog as simpledialog
import subprocess
import sys
from pathlib import Path
import json
import threading


class RedmiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Redmi A2 Lite Tool - GUI")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="Redmi A2 Lite Tool", font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        subtitle = ttk.Label(main_frame, text="Utilidad para dispositivos Android (ADB/Fastboot)")
        subtitle.pack(pady=5)
        
        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab 1: Información
        self.create_info_tab(notebook)
        
        # Tab 2: Control
        self.create_control_tab(notebook)
        
        # Tab 3: Archivos
        self.create_files_tab(notebook)
        
        # Tab 4: Backup
        self.create_backup_tab(notebook)
        
        # Tab 5: Flasheo
        self.create_flash_tab(notebook)
        
        # Output log
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        ttk.Label(main_frame, text="Salida de comandos:").pack(anchor=tk.W)
        self.output = scrolledtext.ScrolledText(main_frame, height=10, width=100, state=tk.DISABLED, wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Limpiar log", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Salir", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def create_info_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Información")
        
        ttk.Button(frame, text="📋 Ver Información", command=lambda: self.run_cmd(['info'], "Información del Dispositivo")).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="📱 Listar Dispositivos", command=lambda: self.run_cmd(['devices'], "Dispositivos Conectados")).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="🔧 Verificar Herramientas", command=lambda: self.run_cmd(['check-tools'], "Verificación de Herramientas")).pack(pady=5, fill=tk.X)
    
    def create_control_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Control")
        
        ttk.Button(frame, text="🔄 Reiniciar (Sistema)", command=lambda: self.run_cmd(['reboot', 'device'], "Reinicio")).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="🔄 Reiniciar (Bootloader)", command=lambda: self.run_cmd(['reboot', 'bootloader'], "Reinicio Bootloader")).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="🔄 Reiniciar (Recovery)", command=lambda: self.run_cmd(['reboot', 'recovery'], "Reinicio Recovery")).pack(pady=5, fill=tk.X)
    
    def create_files_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Archivos")
        
        ttk.Button(frame, text="📥 Pull (Descargar archivo)", command=self.pull_file).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="📤 Push (Subir archivo)", command=self.push_file).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="📝 Ver Logcat", command=self.logcat).pack(pady=5, fill=tk.X)
    
    def create_backup_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Backup")
        
        ttk.Button(frame, text="💾 Backup /sdcard (sin comprimir)", command=lambda: self.backup(compress=False)).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="💾 Backup /sdcard (con ZIP)", command=lambda: self.backup(compress=True)).pack(pady=5, fill=tk.X)
    
    def create_flash_tab(self, notebook):
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="Flasheo")
        
        ttk.Label(frame, text="⚠️ OPERACIONES PELIGROSAS - Pueden borrar datos", foreground='red').pack(pady=10)
        
        ttk.Button(frame, text="⚡ Flash Imagen", command=self.flash_image).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="📦 Flash Paquete (JSON)", command=self.flash_package).pack(pady=5, fill=tk.X)
        ttk.Button(frame, text="🔓 Desbloquear Bootloader", command=self.unlock_bootloader).pack(pady=5, fill=tk.X)
    
    def run_cmd(self, args, title="Salida"):
        """Ejecuta comando en thread separado para no bloquear UI."""
        def execute():
            try:
                result = subprocess.run(
                    [sys.executable, 'tool.py'] + args,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=Path(__file__).parent
                )
                output = result.stdout + (result.stderr if result.stderr else "")
                self.log_output(f"\n[{title}]\n{'='*60}\n{output}\n{'='*60}\n")
            except Exception as e:
                self.log_output(f"\n❌ ERROR: {e}\n")
        
        thread = threading.Thread(target=execute, daemon=True)
        thread.start()
    
    def log_output(self, text):
        """Añade texto al output log."""
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)
    
    def clear_output(self):
        """Limpia el output log."""
        self.output.config(state=tk.NORMAL)
        self.output.delete('1.0', tk.END)
        self.output.config(state=tk.DISABLED)
    
    def pull_file(self):
        src = simpledialog.askstring("Pull", "Ruta en dispositivo (ej: /sdcard/archivo.txt):")
        if src:
            dst = filedialog.askdirectory(title="Carpeta de destino")
            if dst:
                self.run_cmd(['pull', src, dst], "Pull - Descarga")
    
    def push_file(self):
        src = filedialog.askopenfilename(title="Archivo a subir")
        if src:
            dst = simpledialog.askstring("Push", "Ruta destino (ej: /sdcard/):")
            if dst:
                self.run_cmd(['push', src, dst], "Push - Subida")
    
    def logcat(self):
        out = simpledialog.askstring("Logcat", "Archivo de salida:", initialvalue="logcat.txt")
        if out:
            self.run_cmd(['logcat', '--out', out], "Logcat")
    
    def backup(self, compress=False):
        dst = filedialog.askdirectory(title="Carpeta para backup")
        if dst:
            cmd = ['backup', dst]
            if compress:
                cmd.append('--compress')
            self.run_cmd(cmd, f"Backup /sdcard {'(comprimido)' if compress else ''}")
    
    def flash_image(self):
        image = filedialog.askopenfilename(title="Seleccionar imagen (.img)", filetypes=[("IMG files", "*.img"), ("All", "*.*")])
        if image:
            part = simpledialog.askstring("Flash", "Partición (ej: recovery, boot):", initialvalue="recovery")
            if part:
                if messagebox.askyesno("Confirmación", "¿Flashear imagen? Esto puede dañar el dispositivo."):
                    self.run_cmd(['flash', part, image, '--confirm', '--validate-device'], "Flash Imagen")
    
    def flash_package(self):
        manifest = filedialog.askopenfilename(title="Seleccionar manifiesto JSON", filetypes=[("JSON files", "*.json"), ("All", "*.*")])
        if manifest:
            if messagebox.askyesno("Confirmación", "¿Flashear paquete? Esto puede dañar el dispositivo."):
                self.run_cmd(['flash-package', manifest, '--confirm', '--validate-device'], "Flash Paquete")
    
    def unlock_bootloader(self):
        if messagebox.askyesno("⚠️ ADVERTENCIA CRÍTICA", 
            "Desbloquear bootloader:\n\n"
            "❌ Perderá TODOS los datos\n"
            "❌ Invalidará la garantía\n"
            "❌ No se puede revertir fácilmente\n\n"
            "¿Estás SEGURO de que deseas continuar?"):
            self.run_cmd(['unlock-bootloader', '--confirm'], "Desbloqueo Bootloader")


if __name__ == '__main__':
    root = tk.Tk()
    app = RedmiGUI(root)
    root.mainloop()
