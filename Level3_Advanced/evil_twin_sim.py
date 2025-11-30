#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Hacking Automation - Nivel 3: Evil Twin Attacks
NetworkChuck Tutorial Implementation - Versión Educativa
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
import datetime
import re
import threading
import socket
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

class EvilTwinSimulator:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = f"../Reports/evil_twin_{self.session_id}"
        os.makedirs(self.report_dir, exist_ok=True)
        self.captured_data = []
        self.is_running = False

    def check_requirements(self):
        """Verificar requisitos para simulación"""
        print("🔧 Verificando requisitos para simulación...")

        requirements = {
            'python_version': 'OK' if hasattr(socket, 'create_connection') else 'Needs upgrade',
            'http_server': 'OK' if hasattr(socket, 'socket') else 'Missing',
            'threading': 'OK' if hasattr(threading, 'Thread') else 'Missing',
            'network_access': 'Checking...'
        }

        # Verificar acceso de red básico
        try:
            socket.create_connection(('8.8.8.8', 53), timeout=3)
            requirements['network_access'] = 'OK'
        except:
            requirements['network_access'] = 'Limited'

        print("Estado de requisitos:")
        for req, status in requirements.items():
            print(f"  {req}: {status}")

        return all(status == 'OK' for status in requirements.values())

    def simulate_access_point_scan(self):
        """Simular escaneo de puntos de acceso objetivo"""
        print("📡 Simulando escaneo de puntos de acceso...")

        # Datos simulados de redes
        simulated_networks = [
            {
                'ssid': 'HomeNetwork_5G',
                'bssid': '00:11:22:33:44:55',
                'channel': 6,
                'signal': -45,
                'security': 'WPA2-PSK',
                'clients': 3
            },
            {
                'ssid': 'CoffeeShop_WiFi',
                'bssid': 'AA:BB:CC:DD:EE:FF',
                'channel': 11,
                'signal': -62,
                'security': 'WPA2-PSK',
                'clients': 8
            },
            {
                'ssid': 'Office_Guest',
                'bssid': '11:22:33:44:55:66',
                'channel': 1,
                'signal': -38,
                'security': 'WPA2-PSK',
                'clients': 15
            }
        ]

        # Guardar datos de escaneo
        scan_file = os.path.join(self.report_dir, f"network_scan_{self.session_id}.json")
        with open(scan_file, 'w', encoding='utf-8') as f:
            json.dump(simulated_networks, f, indent=2, ensure_ascii=False)

        print(f"✅ Escaneo completado. Encontradas {len(simulated_networks)} redes")
        return simulated_networks

    def create_evil_twin_config(self, target_network):
        """Crear configuración para Evil Twin simulado"""
        print("👻 Creando configuración de Evil Twin...")

        evil_twin_config = {
            'target_network': target_network,
            'evil_twin_ssid': target_network['ssid'],
            'evil_twin_bssid': 'DE:AD:BE:EF:00:00',  # BSSID simulado
            'channel': target_network['channel'],
            'interface': 'wlan0mon',  # Interface simulada
            'auth_method': 'open',  # Para facilitar conexión
            'captive_portal': True,
            'landing_page': {
                'title': 'WiFi Authentication Required',
                'subtitle': f'Please enter credentials for {target_network["ssid"]}',
                'fields': ['username', 'password', 'email']
            },
            'monitoring': {
                'capture_requests': True,
                'log_connections': True,
                'track_clients': True
            }
        }

        # Guardar configuración
        config_file = os.path.join(self.report_dir, f"evil_twin_config_{self.session_id}.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(evil_twin_config, f, indent=2, ensure_ascii=False)

        print(f"✅ Configuración de Evil Twin creada")
        print(f"   SSID: {evil_twin_config['evil_twin_ssid']}")
        print(f"   BSSID: {evil_twin_config['evil_twin_bssid']}")
        print(f"   Canal: {evil_twin_config['channel']}")

        return evil_twin_config

    class CaptivePortalHandler(BaseHTTPRequestHandler):
        """Handler simulado para portal cautivo"""

        def __init__(self, captured_data, *args, **kwargs):
            self.captured_data = captured_data
            super().__init__(*args, **kwargs)

        def do_GET(self):
            """Manejar solicitudes GET"""
            if self.path == '/' or self.path == '/login.html':
                self.serve_login_page()
            elif self.path == '/style.css':
                self.serve_css()
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            """Manejar solicitudes POST (capturar credenciales)"""
            if self.path == '/login':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                # Parsear datos del formulario
                credentials = self.parse_form_data(post_data.decode('utf-8'))

                # Capturar credenciales
                credentials['timestamp'] = datetime.now().isoformat()
                credentials['client_ip'] = self.client_address[0]
                credentials['user_agent'] = self.headers.get('User-Agent', 'Unknown')

                self.captured_data.append(credentials)

                # Redirigir a página de "éxito"
                self.send_response(302)
                self.send_header('Location', '/success.html')
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

        def serve_login_page(self):
            """Servir página de login simulada"""
            html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Authentication</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 50px; }
        .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h2 { color: #333; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #555; }
        input[type="text"], input[type="password"], input[type="email"] {
            width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box;
        }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>WiFi Authentication Required</h2>
        <div class="warning">
            ⚠️ Please enter your network credentials to continue.
        </div>
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="username">Username or Email:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <div class="form-group">
                <label for="email">Email Address:</label>
                <input type="email" id="email" name="email">
            </div>
            <button type="submit">Connect to WiFi</button>
        </form>
    </div>
</body>
</html>
            """

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        def serve_css(self):
            """Servir CSS"""
            css_content = """
            body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 50px; }
            .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h2 { color: #333; text-align: center; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #555; }
            input[type="text"], input[type="password"], input[type="email"] {
                width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box;
            }
            button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            """

            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(css_content.encode('utf-8'))

        def parse_form_data(self, raw_data):
            """Parsear datos del formulario"""
            data = {}
            for pair in raw_data.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    import urllib.parse
                    data[key] = urllib.parse.unquote_plus(value)
            return data

        def log_message(self, format, *args):
            """Sobreescribir para evitar logs en consola"""
            pass

    def simulate_captive_portal(self, config):
        """Simular portal cautivo"""
        print("🌐 Iniciando portal cautivo simulado...")
        print("⚠️  NOTA: Esto es una simulación educativa")

        # Crear handler personalizado con acceso a captured_data
        def handler_factory(*args, **kwargs):
            return self.CaptivePortalHandler(self.captured_data, *args, **kwargs)

        # Iniciar servidor HTTP en puerto 8080
        try:
            server = HTTPServer(('localhost', 8080), handler_factory)

            print(f"✅ Portal cautivo iniciado en http://localhost:8080")
            print("   (Simulación para demostración educativa)")

            # Simular algunas conexiones
            self.simulate_client_connections(config)

            return True
        except Exception as e:
            print(f"❌ Error iniciando portal cautivo: {e}")
            return False

    def simulate_client_connections(self, config):
        """Simular conexiones de clientes"""
        print("👥 Simulando conexiones de clientes...")

        # Datos simulados de clientes
        simulated_clients = [
            {
                'username': 'john.doe',
                'password': 'password123',
                'email': 'john.doe@email.com',
                'client_ip': '192.168.1.100',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            },
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@company.com',
                'client_ip': '192.168.1.101',
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
            },
            {
                'username': 'guest_user',
                'password': 'guest2023',
                'email': 'guest@email.com',
                'client_ip': '192.168.1.102',
                'user_agent': 'Mozilla/5.0 (Android 11; Mobile; rv:68.0)'
            }
        ]

        for client in simulated_clients:
            client['timestamp'] = datetime.now().isoformat()
            client['ssid_connected'] = config['evil_twin_ssid']
            client['bssid_connected'] = config['evil_twin_bssid']

            self.captured_data.append(client)
            print(f"   📱 Cliente conectado: {client['username']} ({client['client_ip']})")
            time.sleep(1)  # Simular tiempo entre conexiones

        print(f"✅ {len(simulated_clients)} conexiones simuladas y capturadas")

    def analyze_captured_data(self):
        """Analizar datos capturados"""
        print("🔬 Analizando datos capturados...")

        if not self.captured_data:
            print("❌ No hay datos para analizar")
            return None

        analysis = {
            'total_connections': len(self.captured_data),
            'unique_usernames': len(set(client.get('username', '') for client in self.captured_data)),
            'unique_ips': len(set(client.get('client_ip', '') for client in self.captured_data)),
            'password_patterns': {},
            'risk_assessment': {
                'weak_passwords': 0,
                'reused_passwords': 0,
                'personal_info_in_password': 0
            },
            'recommendations': []
        }

        # Analizar patrones de contraseñas
        for client in self.captured_data:
            password = client.get('password', '')
            if password:
                # Detectar contraseñas débiles
                if len(password) < 8 or password.lower() in ['password', '123456', 'admin', 'qwerty']:
                    analysis['risk_assessment']['weak_passwords'] += 1

                # Detectar información personal en contraseñas
                username = client.get('username', '').lower()
                if username and username in password.lower():
                    analysis['risk_assessment']['personal_info_in_password'] += 1

        # Generar recomendaciones
        analysis['recommendations'] = [
            "✅ Implementar certificados SSL/TLS para todo el tráfico",
            "✅ Usar 802.1X/EAP-TLS para autenticación enterprise",
            "✅ Implementar detección de Evil Twins",
            "✅ Educar usuarios sobre riesgos de redes desconocidas",
            "✅ Usar VPN en redes públicas",
            "✅ Implementar listas negras de BSSIDs sospechosos"
        ]

        return analysis

    def generate_report(self, networks, config, analysis):
        """Generar reporte completo del Evil Twin"""
        print("📄 Generando reporte de Evil Twin...")

        report_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'simulation_type': 'Evil Twin Attack',
            'networks_scanned': networks,
            'evil_twin_config': config,
            'captured_data': self.captured_data,
            'analysis': analysis,
            'educational_summary': {
                'purpose': 'Demostrar riesgos de Evil Twins',
                'attack_description': 'Un Evil Twin crea un punto de acceso WiFi falso con el mismo nombre que uno legítimo',
                'vulnerability': 'Los dispositivos se conectan automáticamente a la red con señal más fuerte',
                'impact': 'Captura de credenciales, tráfico de red, ataques man-in-the-middle',
                'protection_methods': [
                    'Verificar siempre la red legítima',
                    'Usar HTTPS siempre que sea posible',
                    'Evitar redes WiFi abiertas o desconocidas',
                    'Utilizar VPN',
                    'Configurar perfiles WiFi específicos'
                ]
            }
        }

        # Guardar JSON
        json_file = os.path.join(self.report_dir, f"evil_twin_report_{self.session_id}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Generar reporte en texto plano
        text_file = os.path.join(self.report_dir, f"evil_twin_report_{self.session_id}.txt")
        self.generate_text_report(report_data, text_file)

        print(f"✅ Reportes guardados en:")
        print(f"   📊 JSON: {json_file}")
        print(f"   📝 Texto: {text_file}")

        return report_data

    def generate_text_report(self, data, filename):
        """Generar reporte en formato texto plano"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("WiFi HACKING AUTOMATION - NIVEL 3: EVIL TWIN ATTACKS\n")
            f.write("="*60 + "\n\n")

            f.write(f"SESIÓN: {data['session_id']}\n")
            f.write(f"FECHA Y HORA: {data['timestamp']}\n\n")

            f.write("REDES ESCANEADAS:\n")
            f.write("-" * 30 + "\n")
            for i, network in enumerate(data['networks_scanned'], 1):
                f.write(f"{i}. {network['ssid']}\n")
                f.write(f"   BSSID: {network['bssid']}\n")
                f.write(f"   Canal: {network['channel']}\n")
                f.write(f"   Seguridad: {network['security']}\n")
                f.write(f"   Clientes: {network['clients']}\n\n")

            f.write("CONFIGURACIÓN DE EVIL TWIN:\n")
            f.write("-" * 30 + "\n")
            config = data['evil_twin_config']
            f.write(f"SSID Clonado: {config['evil_twin_ssid']}\n")
            f.write(f"BSSID Falso: {config['evil_twin_bssid']}\n")
            f.write(f"Canal: {config['channel']}\n")
            f.write(f"Método de Autenticación: {config['auth_method']}\n")
            f.write(f"Portal Cautivo: {'Sí' if config['captive_portal'] else 'No'}\n")

            if data['captured_data']:
                f.write("\nDATOS CAPTURADOS:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total de conexiones: {len(data['captured_data'])}\n\n")

                for i, client in enumerate(data['captured_data'], 1):
                    f.write(f"Cliente {i}:\n")
                    f.write(f"  Usuario: {client.get('username', 'N/A')}\n")
                    f.write(f"  Email: {client.get('email', 'N/A')}\n")
                    f.write(f"  IP: {client.get('client_ip', 'N/A')}\n")
                    f.write(f"  Timestamp: {client.get('timestamp', 'N/A')}\n")

            if data['analysis']:
                f.write("\n\nANÁLISIS DE SEGURIDAD:\n")
                f.write("-" * 30 + "\n")
                analysis = data['analysis']
                f.write(f"Total de conexiones: {analysis['total_connections']}\n")
                f.write(f"Usuarios únicos: {analysis['unique_usernames']}\n")
                f.write(f"IPs únicas: {analysis['unique_ips']}\n")

                risk = analysis['risk_assessment']
                f.write(f"\nEvaluación de Riesgos:\n")
                f.write(f"  Contraseñas débiles: {risk['weak_passwords']}\n")
                f.write(f"  Info personal en passwords: {risk['personal_info_in_password']}\n")

            f.write("\n\nRESUMEN EDUCATIVO:\n")
            f.write("-" * 30 + "\n")
            edu = data['educational_summary']
            f.write(f"Ataque: {edu['attack_description']}\n")
            f.write(f"Vulnerabilidad: {edu['vulnerability']}\n")
            f.write(f"Impacto: {edu['impact']}\n")

            f.write("\n\nMÉTODOS DE PROTECCIÓN:\n")
            f.write("-" * 30 + "\n")
            for i, method in enumerate(edu['protection_methods'], 1):
                f.write(f"{i}. {method}\n")

    def run_simulation(self, target_network_index=0):
        """Ejecutar simulación completa de Evil Twin"""
        print("🚀 INICIANDO SIMULACIÓN DE EVIL TWIN - NIVEL 3")
        print("="*60)
        print("⚠️  SIMULACIÓN EDUCATIVA - USO ÉTICO SOLAMENTE")
        print("="*60)

        # Verificar requisitos
        if not self.check_requirements():
            print("❌ Requisitos mínimos no cumplidos")
            return None

        # Escanear redes
        networks = self.simulate_access_point_scan()

        if not networks:
            print("❌ No se encontraron redes para simular")
            return None

        # Seleccionar red objetivo (simulación)
        target_network = networks[target_network_index]
        print(f"🎯 Red seleccionada para Evil Twin: {target_network['ssid']}")

        # Crear configuración de Evil Twin
        config = self.create_evil_twin_config(target_network)

        # Simular portal cautivo
        portal_success = self.simulate_captive_portal(config)

        if not portal_success:
            print("❌ Error en simulación de portal cautivo")
            return None

        # Analizar datos capturados
        analysis = self.analyze_captured_data()

        # Generar reporte
        report = self.generate_report(networks, config, analysis)

        print("\n🎉 SIMULACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print("📚 Se ha demostrado educativamente:")
        print("   • Creación de puntos de acceso falsos")
        print("   • Implementación de portales cautivos")
        print("   • Captura de credenciales")
        print("   • Análisis de riesgos de seguridad")

        return report

def main():
    """Función principal para ejecutar simulación de Evil Twin"""
    print("🔥 WiFi Hacking Automation - Nivel 3: Evil Twin Attacks")
    print("   Tutorial basado en NetworkChuck")
    print("   ⚠️  SIMULACIÓN EDUCATIVA - USO ÉTICO SOLAMENTE")
    print()

    simulator = EvilTwinSimulator()

    try:
        report = simulator.run_simulation()
        if report:
            print(f"\n✅ Simulación completada. Reporte guardado en: {simulator.report_dir}")
            return True
        else:
            print("\n❌ No se pudo completar la simulación")
            return False
    except KeyboardInterrupt:
        print("\n⚠️  Simulación cancelada por usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)