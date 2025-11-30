#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Hacking Automation - Menú Principal
Basado en el tutorial "3 Levels of WiFi Hacking" de NetworkChuck
Author: Claude AI Assistant
"""

# Configurar consola para UTF-8 en Windows
import sys
import os
import io

if sys.platform == 'win32':
    # Configurar codificación UTF-8 para salida estándar
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.system('chcp 65001 >nul 2>&1')

import subprocess
import json
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class WiFiHackingMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WiFi Hacking Automation - NetworkChuck Tutorial")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')

        # Variables
        self.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_log = []

        # Crear estilo
        self.setup_styles()

        # Crear interfaz
        self.create_interface()

    def setup_styles(self):
        """Configurar estilos visuales"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar colores
        style.configure('Title.TLabel',
                       background='#1a1a1a',
                       foreground='#00ff00',
                       font=('Consolas', 16, 'bold'))

        style.configure('Subtitle.TLabel',
                       background='#1a1a1a',
                       foreground='#00cccc',
                       font=('Consolas', 12))

        style.configure('Info.TLabel',
                       background='#1a1a1a',
                       foreground='#ffffff',
                       font=('Consolas', 10))

        style.configure('Action.TButton',
                       font=('Consolas', 12, 'bold'),
                       padding=10)

        style.map('Action.TButton',
                 background=[('active', '#00ff00'),
                           ('!active', '#00cc00')])

        style.configure('Danger.TButton',
                       font=('Consolas', 12, 'bold'),
                       padding=10)

        style.map('Danger.TButton',
                 background=[('active', '#ff4444'),
                           ('!active', '#cc0000')])

    def create_interface(self):
        """Crear interfaz gráfica"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        title_label = ttk.Label(main_frame,
                               text="🔥 WiFi Hacking Automation",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))

        subtitle_label = ttk.Label(main_frame,
                                 text="Basado en el tutorial de NetworkChuck - 3 Levels of WiFi Hacking",
                                 style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))

        # Advertencia ética
        warning_frame = tk.Frame(main_frame, bg='#2a1a1a', relief=tk.RIDGE, bd=2)
        warning_frame.pack(fill=tk.X, pady=(0, 20))

        warning_text = """⚠️  ADVERTENCIA IMPORTANTE ⚠️
Este software es para fines educativos y de entrenamiento ético únicamente.
Solo debe ser utilizado en redes que le pertenecen o con permiso explícito.
El acceso no autorizado a redes WiFi es ilegal y puede tener consecuencias legales graves."""

        warning_label = ttk.Label(warning_frame, text=warning_text, style='Info.TLabel')
        warning_label.pack(padx=10, pady=10)

        # Frame de niveles
        levels_frame = tk.Frame(main_frame, bg='#1a1a1a')
        levels_frame.pack(fill=tk.BOTH, expand=True)

        # Nivel 1
        self.create_level_card(levels_frame, 1,
                              "📡 Nivel 1: Descubrimiento de Redes",
                              ["Escaneo de redes WiFi", "Análisis de señales", "Identificación de seguridad"],
                              "#00ff00", self.run_level1)

        # Nivel 2
        self.create_level_card(levels_frame, 2,
                              "🔓 Nivel 2: Análisis de Contraseñas",
                              ["Captura de handshakes", "Análisis WPA/WPA2", "Técnicas de recuperación"],
                              "#ffaa00", self.run_level2)

        # Nivel 3
        self.create_level_card(levels_frame, 3,
                              "👻 Nivel 3: Evil Twin Attacks",
                              ["Simulación de ataques", "Portales cautivos", "Análisis avanzado"],
                              "#ff4444", self.run_level3)

        # Frame de control
        control_frame = tk.Frame(main_frame, bg='#1a1a1a')
        control_frame.pack(fill=tk.X, pady=(20, 0))

        # Botones de control
        ttk.Button(control_frame, text="📊 Ver Reportes",
                  command=self.view_reports,
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(control_frame, text="📋 Ver Logs",
                  command=self.view_logs,
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(control_frame, text="❌ Salir",
                  command=self.exit_app,
                  style='Danger.TButton').pack(side=tk.RIGHT)

        # Barra de estado
        self.status_label = ttk.Label(control_frame,
                                     text="Listo para comenzar análisis WiFi",
                                     style='Info.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=20)

    def create_level_card(self, parent, level, title, features, color, command):
        """Crear tarjeta para cada nivel"""
        card_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        card_frame.grid(row=(level-1)//2, column=(level-1)%2, padx=10, pady=10, sticky='nsew')

        # Configurar pesos de grid
        parent.grid_rowconfigure((level-1)//2, weight=1)
        parent.grid_columnconfigure((level-1)%2, weight=1)

        # Nivel
        level_label = tk.Label(card_frame, text=f"NIVEL {level}",
                              font=('Consolas', 14, 'bold'),
                              bg='#2a2a2a', fg=color)
        level_label.pack(pady=(15, 5))

        # Título
        title_label = tk.Label(card_frame, text=title,
                             font=('Consolas', 11, 'bold'),
                             bg='#2a2a2a', fg='white',
                             wraplength=350)
        title_label.pack(padx=15, pady=(0, 10))

        # Características
        features_frame = tk.Frame(card_frame, bg='#2a2a2a')
        features_frame.pack(padx=15, pady=(0, 15))

        for feature in features:
            feature_label = tk.Label(features_frame, text=f"• {feature}",
                                   font=('Consolas', 9),
                                   bg='#2a2a2a', fg='#cccccc',
                                   anchor='w')
            feature_label.pack(fill=tk.X, pady=2)

        # Botón de acción
        if level == 3:
            button_style = 'Danger.TButton'
        else:
            button_style = 'Action.TButton'

        action_button = ttk.Button(card_frame,
                                 text=f"Iniciar Nivel {level}",
                                 command=command,
                                 style=button_style)
        action_button.pack(padx=15, pady=(0, 15))

    def run_level1(self):
        """Ejecutar Nivel 1 - Descubrimiento de Redes"""
        self.log_action("Iniciando Nivel 1: Descubrimiento de Redes")
        self.status_label.config(text="Ejecutando Nivel 1...")

        try:
            script_path = os.path.join("Level1_Discovery", "wifi_discovery.py")
            if os.path.exists(script_path):
                self.run_script(script_path, "Nivel 1 - Descubrimiento")
            else:
                messagebox.showerror("Error", f"No se encontró el script: {script_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando Nivel 1: {str(e)}")
            self.log_action(f"Error en Nivel 1: {str(e)}")

    def run_level2(self):
        """Ejecutar Nivel 2 - Análisis de Contraseñas"""
        self.log_action("Iniciando Nivel 2: Análisis de Contraseñas")
        self.status_label.config(text="Ejecutando Nivel 2...")

        try:
            script_path = os.path.join("Level2_Password", "password_analysis.py")
            if os.path.exists(script_path):
                self.run_script(script_path, "Nivel 2 - Análisis de Contraseñas")
            else:
                messagebox.showerror("Error", f"No se encontró el script: {script_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando Nivel 2: {str(e)}")
            self.log_action(f"Error en Nivel 2: {str(e)}")

    def run_level3(self):
        """Ejecutar Nivel 3 - Evil Twin Attacks"""
        self.log_action("Iniciando Nivel 3: Evil Twin Attacks")
        self.status_label.config(text="Ejecutando Nivel 3...")

        # Advertencia adicional para Nivel 3
        warning = "⚠️ El Nivel 3 simula ataques avanzados.\n\nEste contenido es puramente educativo y no debe ser utilizado para actividades maliciosas.\n\n¿Desea continuar con la simulación educativa?"

        if not messagebox.askyesno("Confirmación", warning):
            self.log_action("Nivel 3 cancelado por usuario")
            self.status_label.config(text="Listo para comenzar análisis WiFi")
            return

        try:
            script_path = os.path.join("Level3_Advanced", "evil_twin_sim.py")
            if os.path.exists(script_path):
                self.run_script(script_path, "Nivel 3 - Evil Twin Simulation")
            else:
                messagebox.showerror("Error", f"No se encontró el script: {script_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando Nivel 3: {str(e)}")
            self.log_action(f"Error en Nivel 3: {str(e)}")

    def run_script(self, script_path, level_name):
        """Ejecutar script en proceso separado"""
        try:
            # Crear ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title(f"Ejecutando {level_name}")
            progress_window.geometry("500x300")
            progress_window.configure(bg='#1a1a1a')

            # Texto de estado
            status_label = tk.Label(progress_window,
                                  text=f"Ejecutando {level_name}...\n\nPor favor espere.",
                                  font=('Consolas', 12),
                                  bg='#1a1a1a', fg='white')
            status_label.pack(pady=20)

            # Área de salida
            output_text = scrolledtext.ScrolledText(progress_window,
                                                  width=60, height=15,
                                                  font=('Consolas', 9),
                                                  bg='#000000', fg='#00ff00')
            output_text.pack(padx=20, pady=(0, 20))

            # Ejecutar script
            def execute_script():
                try:
                    # Usar subprocess para ejecutar el script
                    process = subprocess.Popen([sys.executable, script_path],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT,
                                             text=True,
                                             cwd=os.path.dirname(os.path.abspath(__file__)))

                    # Leer salida en tiempo real
                    for line in process.stdout:
                        output_text.insert(tk.END, line)
                        output_text.see(tk.END)
                        progress_window.update()

                    process.wait()

                    if process.returncode == 0:
                        self.log_action(f"{level_name} completado exitosamente")
                        messagebox.showinfo("Éxito", f"{level_name} completado exitosamente")
                    else:
                        self.log_action(f"{level_name} finalizado con errores")
                        messagebox.showwarning("Advertencia", f"{level_name} finalizado con posibles errores")

                except Exception as e:
                    error_msg = f"Error ejecutando script: {str(e)}"
                    output_text.insert(tk.END, f"\nERROR: {error_msg}\n")
                    self.log_action(error_msg)
                    messagebox.showerror("Error", error_msg)

                finally:
                    progress_window.destroy()
                    self.status_label.config(text="Listo para comenzar análisis WiFi")

            # Ejecutar en hilo separado para no bloquear la GUI
            import threading
            thread = threading.Thread(target=execute_script)
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar {level_name}: {str(e)}")

    def view_reports(self):
        """Ver reportes generados"""
        reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Reports")

        if not os.path.exists(reports_dir):
            messagebox.showinfo("Reportes", "No hay reportes disponibles aún")
            return

        # Crear ventana de reportes
        report_window = tk.Toplevel(self.root)
        report_window.title("Reportes Generados")
        report_window.geometry("800x600")
        report_window.configure(bg='#1a1a1a')

        # Lista de reportes
        reports_frame = tk.Frame(report_window, bg='#1a1a1a')
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Buscar reportes
        report_files = []
        for root, dirs, files in os.walk(reports_dir):
            for file in files:
                if file.endswith(('.json', '.txt')):
                    report_files.append(os.path.join(root, file))

        if not report_files:
            tk.Label(reports_frame, text="No se encontraron reportes",
                    font=('Consolas', 12),
                    bg='#1a1a1a', fg='white').pack(pady=50)
        else:
            # Lista de reportes
            listbox = tk.Listbox(reports_frame,
                               font=('Consolas', 10),
                               bg='#2a2a2a', fg='white',
                               selectbackground='#00ff00')
            listbox.pack(fill=tk.BOTH, expand=True)

            for report_file in sorted(report_files):
                relative_path = os.path.relpath(report_file, reports_dir)
                listbox.insert(tk.END, relative_path)

            # Botón para abrir reporte
            def open_report():
                selection = listbox.curselection()
                if selection:
                    report_file = report_files[selection[0]]
                    os.startfile(report_file)  # Abrir con aplicación predeterminada

            ttk.Button(reports_frame, text="Abrir Reporte Seleccionado",
                      command=open_report).pack(pady=10)

    def view_logs(self):
        """Ver logs de la sesión"""
        log_window = tk.Toplevel(self.root)
        log_window.title("Logs de Sesión")
        log_window.geometry("700x500")
        log_window.configure(bg='#1a1a1a')

        # Área de logs
        log_text = scrolledtext.ScrolledText(log_window,
                                           width=80, height=25,
                                           font=('Consolas', 9),
                                           bg='#000000', fg='#00ff00')
        log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Mostrar logs
        for log_entry in self.session_log:
            log_text.insert(tk.END, f"{log_entry}\n")

    def log_action(self, action):
        """Registrar acción en logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        self.session_log.append(log_entry)
        print(log_entry)  # También imprimir en consola

    def exit_app(self):
        """Salir de la aplicación"""
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir?"):
            self.log_action("Aplicación cerrada por usuario")
            self.root.quit()
            self.root.destroy()

    def run(self):
        """Iniciar aplicación"""
        self.log_action("Aplicación WiFi Hacking Automation iniciada")
        self.root.mainloop()

def main():
    """Función principal"""
    print("🔥 WiFi Hacking Automation - Menu Principal")
    print("   Basado en NetworkChuck Tutorial")
    print("   ⚠️  Uso ético y educativo solamente")
    print()

    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    try:
        app = WiFiHackingMenu()
        app.run()
    except KeyboardInterrupt:
        print("\n⚠️ Aplicación cancelada por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()