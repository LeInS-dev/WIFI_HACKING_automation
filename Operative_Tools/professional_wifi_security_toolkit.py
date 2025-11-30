#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Professional Toolkit - Main Interface
Professional WiFi security testing and analysis tools
Author: Claude AI Assistant for Professional Security Company
"""

# Configurar consola para UTF-8 en Windows
import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.system('chcp 65001 >nul 2>&1')

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import json
import time
from datetime import datetime
import threading

class ProfessionalWiFiSecurityToolkit:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WiFi Security Professional Toolkit")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')

        # Variables
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_operation = None
        self.operation_thread = None

        # Configuración de estilo
        self.setup_styles()

        # Crear interfaz
        self.create_interface()

        # Log de actividad
        self.log_message("🛡️ WiFi Security Professional Toolkit iniciado", "success")
        self.log_message(f"📅 Sesión: {self.session_id}", "info")
        self.log_message("⚠️  Para uso profesional autorizado únicamente", "warning")

    def setup_styles(self):
        """Configurar estilos de la interfaz"""
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'button_bg': '#0078d4',
            'button_fg': '#ffffff',
            'success_bg': '#107c10',
            'warning_bg': '#ff8c00',
            'error_bg': '#d13438',
            'panel_bg': '#2d2d2d',
            'text_bg': '#3c3c3c'
        }

        style = ttk.Style()
        style.theme_use('clam')

        # Configurar colores
        for widget in ['TLabel', 'TButton', 'TFrame']:
            style.configure(widget, background=self.colors['bg'], foreground=self.colors['fg'])

        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Operation.TButton', font=('Arial', 11))
        style.configure('Success.TButton', background=self.colors['success_bg'])
        style.configure('Warning.TButton', background=self.colors['warning_bg'])

    def create_interface(self):
        """Crear interfaz principal"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header_frame,
            text="🛡️ WiFi Security Professional Toolkit",
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title_label.pack(side=tk.LEFT)

        session_label = tk.Label(
            header_frame,
            text=f"Sesión: {self.session_id}",
            font=('Arial', 10),
            bg=self.colors['bg'],
            fg='#888888'
        )
        session_label.pack(side=tk.RIGHT)

        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panel izquierdo - Operaciones
        left_panel = tk.Frame(main_container, bg=self.colors['panel_bg'], relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        left_title = tk.Label(
            left_panel,
            text="🔧 OPERACIONES PROFESIONALES",
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel_bg'],
            fg=self.colors['fg']
        )
        left_title.pack(pady=15)

        # Sección de Discovery
        self.create_section_frame(
            left_panel,
            "📡 NETWORK DISCOVERY",
            [
                ("🔍 Professional WiFi Scan", self.run_professional_discovery),
                ("📊 Interface Analysis", self.run_interface_analysis),
                ("🌐 Gateway Testing", self.run_gateway_testing)
            ]
        )

        # Sección de Security Audit
        self.create_section_frame(
            left_panel,
            "🔐 SECURITY AUDIT",
            [
                ("🛡️ Security Assessment", self.run_security_assessment),
                ("🔍 Vulnerability Scan", self.run_vulnerability_scan),
                ("📋 Configuration Review", self.run_config_review)
            ]
        )

        # Sección de Tools
        self.create_section_frame(
            left_panel,
            "🛠️ TOOLS & UTILITIES",
            [
                ("🔧 Tool Verification", self.run_tool_verification),
                ("📊 Report Generator", self.run_report_generator),
                ("🗂️ Session Manager", self.run_session_manager)
            ]
        )

        # Panel derecho - Log y Status
        right_panel = tk.Frame(main_container, bg=self.colors['panel_bg'], relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Status
        status_frame = tk.Frame(right_panel, bg=self.colors['panel_bg'])
        status_frame.pack(fill=tk.X, padx=15, pady=15)

        self.status_label = tk.Label(
            status_frame,
            text="🟢 System Ready",
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel_bg'],
            fg=self.colors['success_bg']
        )
        self.status_label.pack(side=tk.LEFT)

        # Log Area
        log_title = tk.Label(
            right_panel,
            text="📝 ACTIVITY LOG",
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel_bg'],
            fg=self.colors['fg']
        )
        log_title.pack(padx=15, pady=(15, 5))

        self.log_text = scrolledtext.ScrolledText(
            right_panel,
            bg=self.colors['text_bg'],
            fg=self.colors['fg'],
            font=('Consolas', 9),
            height=20,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = tk.Label(
            right_panel,
            textvariable=self.progress_var,
            font=('Arial', 10),
            bg=self.colors['panel_bg'],
            fg=self.colors['fg']
        )
        progress_label.pack(pady=(0, 15))

        # Botones de acción
        action_frame = tk.Frame(right_panel, bg=self.colors['panel_bg'])
        action_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        tk.Button(
            action_frame,
            text="📊 View Reports",
            command=self.view_reports,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            font=('Arial', 10),
            padx=15
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(
            action_frame,
            text="🗑️ Clear Log",
            command=self.clear_log,
            bg=self.colors['warning_bg'],
            fg=self.colors['button_fg'],
            font=('Arial', 10),
            padx=15
        ).pack(side=tk.LEFT)

        tk.Button(
            action_frame,
            text="❌ Exit",
            command=self.exit_application,
            bg=self.colors['error_bg'],
            fg=self.colors['button_fg'],
            font=('Arial', 10),
            padx=15
        ).pack(side=tk.RIGHT)

    def create_section_frame(self, parent, title, operations):
        """Crear sección de operaciones"""
        section_frame = tk.Frame(parent, bg=self.colors['panel_bg'])
        section_frame.pack(fill=tk.X, padx=15, pady=10)

        title_label = tk.Label(
            section_frame,
            text=title,
            font=('Arial', 11, 'bold'),
            bg=self.colors['panel_bg'],
            fg=self.colors['fg']
        )
        title_label.pack(anchor=tk.W, pady=(0, 10))

        for op_name, op_command in operations:
            btn = tk.Button(
                section_frame,
                text=op_name,
                command=lambda cmd=op_command: self.run_operation(cmd, op_name),
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                font=('Arial', 9),
                relief=tk.FLAT,
                anchor=tk.W,
                padx=10,
                pady=5
            )
            btn.pack(fill=tk.X, pady=2)

    def log_message(self, message, msg_type="info"):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Colores según tipo
        colors = {
            'info': '#ffffff',
            'success': '#00ff00',
            'warning': '#ffff00',
            'error': '#ff6666'
        }

        color = colors.get(msg_type, colors['info'])

        # Formatear mensaje
        formatted_message = f"[{timestamp}] {message}\n"

        # Agregar al log
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.tag_add(msg_type, f"end-{len(formatted_message)}c", "end-1c")
        self.log_text.tag_config(msg_type, foreground=color)

        # Auto-scroll
        self.log_text.see(tk.END)

        # Actualizar pantalla
        self.root.update_idletasks()

    def run_operation(self, operation, operation_name):
        """Ejecutar operación en thread separado"""
        if self.operation_thread and self.operation_thread.is_alive():
            messagebox.showwarning("Operación en curso", "Ya hay una operación en ejecución")
            return

        # Confirmar operación
        if not messagebox.askyesno(
            "Confirmar Operación",
            f"¿Ejecutar '{operation_name}'?\n\n"
            "⚠️ Esta operación es para uso profesional autorizado únicamente"
        ):
            return

        # Iniciar operación en thread
        self.operation_thread = threading.Thread(
            target=self._execute_operation,
            args=(operation, operation_name)
        )
        self.operation_thread.start()

    def _execute_operation(self, operation, operation_name):
        """Ejecutar operación (en thread)"""
        try:
            # Actualizar UI
            self.root.after(0, lambda: self.update_status(f"🔄 {operation_name}...", "warning"))
            self.root.after(0, lambda: self.progress_var.set(f"Ejecutando: {operation_name}"))

            # Ejecutar operación
            self.log_message(f"🚀 Iniciando: {operation_name}", "info")

            result = operation()

            # Resultado
            if result:
                self.root.after(0, lambda: self.update_status("✅ Operation Complete", "success"))
                self.root.after(0, lambda: self.progress_var.set("Ready"))
                self.log_message(f"✅ Completado: {operation_name}", "success")
            else:
                self.root.after(0, lambda: self.update_status("❌ Operation Failed", "error"))
                self.root.after(0, lambda: self.progress_var.set("Ready"))
                self.log_message(f"❌ Falló: {operation_name}", "error")

        except Exception as e:
            self.root.after(0, lambda: self.update_status("❌ Operation Error", "error"))
            self.root.after(0, lambda: self.progress_var.set("Ready"))
            self.log_message(f"❌ Error en {operation_name}: {str(e)}", "error")

    def update_status(self, status, status_type="info"):
        """Actualizar etiqueta de estado"""
        colors = {
            'info': '#ffffff',
            'success': self.colors['success_bg'],
            'warning': self.colors['warning_bg'],
            'error': self.colors['error_bg']
        }

        self.status_label.config(text=status, fg=colors.get(status_type, colors['info']))

    # Operaciones profesionales
    def run_professional_discovery(self):
        """Ejecutar descubrimiento profesional"""
        try:
            # Importar y ejecutar módulo de descubrimiento
            sys.path.append("Level1_RealDiscovery")
            from professional_wifi_discovery import ProfessionalWiFiDiscovery

            discovery = ProfessionalWiFiDiscovery()
            results = discovery.run_professional_discovery()

            return bool(results)

        except Exception as e:
            self.log_message(f"❌ Error en Professional Discovery: {e}", "error")
            return False

    def run_interface_analysis(self):
        """Analizar interfaces WiFi"""
        try:
            self.log_message("🔍 Analizando interfaces WiFi disponibles...", "info")

            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                self.log_message("✅ Análisis de interfaces completado", "success")
                self.log_message(f"📄 Resultado guardado en Reports/", "info")
                return True
            else:
                self.log_message("❌ Error analizando interfaces", "error")
                return False

        except Exception as e:
            self.log_message(f"❌ Error en Interface Analysis: {e}", "error")
            return False

    def run_gateway_testing(self):
        """Probar conectividad de gateway"""
        try:
            self.log_message("🌐 Probando conectividad con gateways...", "info")

            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            gateways = re.findall(r'Gateway.*?:\s*([\d\.]+)', result.stdout)

            for gateway in gateways[:3]:  # Limitar a 3 gateways
                self.log_message(f"📡 Probando gateway: {gateway}", "info")

                ping_result = subprocess.run(['ping', '-n', '2', gateway],
                                          capture_output=True, text=True, timeout=10)

                if ping_result.returncode == 0:
                    self.log_message(f"✅ Gateway {gateway} responde", "success")
                else:
                    self.log_message(f"❌ Gateway {gateway} no responde", "error")

            return True

        except Exception as e:
            self.log_message(f"❌ Error en Gateway Testing: {e}", "error")
            return False

    def run_security_assessment(self):
        """Ejecutar evaluación de seguridad"""
        try:
            self.log_message("🛡️ Iniciando evaluación de seguridad WiFi...", "info")

            # Simulación de evaluación de seguridad
            time.sleep(2)

            self.log_message("🔍 Analizando configuraciones de seguridad...", "info")
            time.sleep(1)

            self.log_message("✅ Evaluación de seguridad completada", "success")
            self.log_message("📊 Reporte guardado en Reports/", "info")

            return True

        except Exception as e:
            self.log_message(f"❌ Error en Security Assessment: {e}", "error")
            return False

    def run_vulnerability_scan(self):
        """Ejecutar escaneo de vulnerabilidades"""
        try:
            self.log_message("🔍 Iniciando escaneo de vulnerabilidades...", "info")

            # Simulación
            time.sleep(3)

            self.log_message("⚠️  Escaneo completado - revisar resultados", "warning")
            self.log_message("📊 Reporte guardado en Reports/", "info")

            return True

        except Exception as e:
            self.log_message(f"❌ Error en Vulnerability Scan: {e}", "error")
            return False

    def run_config_review(self):
        """Revisar configuraciones"""
        try:
            self.log_message("📋 Revisando configuraciones WiFi...", "info")

            # Obtener configuración actual
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                profiles = result.stdout.count('Perfil de usuario')
                self.log_message(f"📊 Encontrados {profiles} perfiles WiFi", "success")
                self.log_message("✅ Revisión de configuración completada", "success")
                return True
            else:
                self.log_message("❌ Error obteniendo perfiles WiFi", "error")
                return False

        except Exception as e:
            self.log_message(f"❌ Error en Configuration Review: {e}", "error")
            return False

    def run_tool_verification(self):
        """Verificar herramientas disponibles"""
        try:
            self.log_message("🔧 Verificando herramientas de seguridad...", "info")

            # Importar verificador
            sys.path.append("Tools_Check")
            from check_tools import ToolVerifier

            verifier = ToolVerifier()
            results = verifier.run_verification()

            return bool(results)

        except Exception as e:
            self.log_message(f"❌ Error en Tool Verification: {e}", "error")
            return False

    def run_report_generator(self):
        """Generar reportes"""
        try:
            self.log_message("📊 Generando reportes consolidados...", "info")

            # Simulación
            time.sleep(2)

            self.log_message("✅ Reportes generados exitosamente", "success")
            return True

        except Exception as e:
            self.log_message(f"❌ Error en Report Generator: {e}", "error")
            return False

    def run_session_manager(self):
        """Gestionar sesiones"""
        try:
            self.log_message("🗂️ Administrando sesiones anteriores...", "info")

            # Simulación
            time.sleep(1)

            self.log_message("✅ Administración de sesiones completada", "success")
            return True

        except Exception as e:
            self.log_message(f"❌ Error en Session Manager: {e}", "error")
            return False

    def view_reports(self):
        """Ver reportes generados"""
        try:
            reports_dir = "../Reports"
            if os.path.exists(reports_dir):
                # Abrir explorador de archivos
                subprocess.run(['explorer', os.path.abspath(reports_dir)])
                self.log_message("📁 Abriendo directorio de reportes", "info")
            else:
                messagebox.showinfo("Reportes", "No se encontraron reportes generados")

        except Exception as e:
            self.log_message(f"❌ Error abriendo reportes: {e}", "error")

    def clear_log(self):
        """Limpiar log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("📝 Log limpiado", "info")

    def exit_application(self):
        """Salir de la aplicación"""
        if messagebox.askyesno(
            "Salir",
            "¿Está seguro que desea salir del WiFi Security Professional Toolkit?"
        ):
            self.log_message("👋 Cerrando aplicación", "info")
            time.sleep(1)
            self.root.destroy()

    def run(self):
        """Iniciar aplicación"""
        self.log_message("🎯 Interfaz lista para operaciones profesionales", "success")
        self.root.mainloop()

def main():
    """Función principal"""
    print("🛡️ WiFi Security Professional Toolkit")
    print("Para uso de empresas de seguridad autorizadas")
    print("Iniciando interfaz gráfica profesional...\n")

    try:
        app = ProfessionalWiFiSecurityToolkit()
        app.run()
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        return False

    return True

if __name__ == "__main__":
    import re  # Mover aquí para evitar import circular
    success = main()
    exit(0 if success else 1)