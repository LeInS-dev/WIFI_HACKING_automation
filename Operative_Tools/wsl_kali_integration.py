#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Professional Toolkit - Kali Linux WSL Integration
Professional security tools integration via Windows Subsystem for Linux
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

import subprocess
import json
import time
import re
from datetime import datetime
import tempfile
import shutil

class KaliWSLIntegration:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = f"../Reports/kali_integration_{self.session_id}"
        os.makedirs(self.report_dir, exist_ok=True)
        self.wsl_available = False
        self.kali_available = False
        self.tools_available = {}

    def check_wsl_availability(self):
        """Verificar disponibilidad de WSL"""
        print("🔍 Checking WSL availability...")

        try:
            # Verificar si WSL está instalado
            result = subprocess.run(['wsl', '-l'], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                self.wsl_available = True
                print("✅ WSL is available")

                # Verificar distribuciones disponibles
                distros = self.parse_wsl_list(result.stdout)
                print(f"📦 Found {len(distros)} WSL distributions:")
                for distro in distros:
                    status = "✅" if distro['running'] else "⭕"
                    print(f"   {status} {distro['name']}")

                return distros
            else:
                print("❌ WSL is not available")
                return []

        except FileNotFoundError:
            print("❌ WSL is not installed")
            return []
        except Exception as e:
            print(f"❌ Error checking WSL: {e}")
            return []

    def parse_wsl_list(self, output):
        """Parsear salida de wsl -l"""
        distros = []
        lines = output.split('\n')

        for line in lines:
            line = line.strip()
            # Limpiar caracteres Unicode extraños
            line = ''.join(char for char in line if ord(char) < 256 or char in 'áéíóúñüÁÉÍÓÚÑÜ')

            if line and not line.startswith('Distribuciones') and not line.startswith('Windows'):
                # Extraer nombres de distribuciones
                if 'docker' in line.lower():
                    distros.append({
                        'name': 'docker-desktop',
                        'state': 'Stopped',
                        'running': False,
                        'version': '2'
                    })
                elif 'ubuntu' in line.lower():
                    distros.append({
                        'name': 'Ubuntu',
                        'state': 'Stopped',
                        'running': False,
                        'version': '2'
                    })
                elif 'kali' in line.lower():
                    distros.append({
                        'name': 'kali-linux',
                        'state': 'Stopped',
                        'running': False,
                        'version': '2'
                    })

        return distros

    def check_kali_availability(self):
        """Verificar disponibilidad de Kali Linux"""
        print("\n🐧 Checking Kali Linux availability...")

        try:
            # Verificar si Kali está instalado
            result = subprocess.run(['wsl', '-l'], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                # Limpiar caracteres Unicode
                cleaned_output = ''.join(char for char in result.stdout if ord(char) < 256 or char in 'áéíóúñüÁÉÍÓÚÑÜ')

                if 'kali' in cleaned_output.lower():
                    self.kali_available = True
                    print("✅ Kali Linux is available")
                    return True
                else:
                    print("❌ Kali Linux is not installed")
                    return False
            else:
                print("❌ Cannot check WSL distributions")
                return False

        except Exception as e:
            print(f"❌ Error checking Kali: {e}")
            return False

    def start_kali_wsl(self):
        """Iniciar Kali Linux en WSL"""
        if not self.kali_available:
            print("❌ Kali Linux is not available")
            return False

        print("🚀 Starting Kali Linux WSL...")

        try:
            # Intentar iniciar Kali
            result = subprocess.run(['wsl', '-d', 'kali-linux', '--', 'echo', 'Kali ready'],
                                  capture_output=True, text=True, timeout=30)

            if result.returncode == 0 and 'Kali ready' in result.stdout:
                print("✅ Kali Linux started successfully")
                return True
            else:
                print("⚠️  Kali Linux needs configuration")
                # Intentar iniciar sin distribución específica
                result2 = subprocess.run(['wsl', '--', 'lsb_release', '-i'],
                                       capture_output=True, text=True, timeout=20)
                if result2.returncode == 0:
                    print("✅ WSL environment available (may not be Kali)")
                    return True
                else:
                    print("❌ Cannot start WSL environment")
                    return False

        except Exception as e:
            print(f"❌ Error starting Kali: {e}")
            return False

    def check_security_tools(self):
        """Verificar herramientas de seguridad en Kali"""
        print("\n🛠️  Checking security tools in Kali...")

        security_tools = {
            'aircrack-ng': ['aircrack-ng', '--help'],
            'airodump-ng': ['airodump-ng', '--help'],
            'aireplay-ng': ['aireplay-ng', '--help'],
            'airmon-ng': ['airmon-ng', '--help'],
            'wash': ['wash', '--help'],
            'reaver': ['reaver', '--help'],
            'bully': ['bully', '--help'],
            'nmap': ['nmap', '--version'],
            'wireshark': ['tshark', '--version'],
            'hashcat': ['hashcat', '--version'],
            'john': ['john', '--version'],
            'hydra': ['hydra', '--version'],
            'netcat': ['nc', '--help'],
            'tcpdump': ['tcpdump', '--version'],
            'masscan': ['masscan', '--version'],
        }

        available_tools = {}

        for tool_name, command in security_tools.items():
            try:
                print(f"   🔍 Checking {tool_name}...", end=" ")

                # Ejecutar comando en WSL
                wsl_command = ['wsl'] + command
                result = subprocess.run(wsl_command, capture_output=True, text=True, timeout=10)

                if result.returncode == 0:
                    available_tools[tool_name] = {
                        'available': True,
                        'output': result.stdout[:100] + "..." if len(result.stdout) > 100 else result.stdout
                    }
                    print("✅")
                else:
                    available_tools[tool_name] = {
                        'available': False,
                        'error': result.stderr[:100] + "..." if len(result.stderr) > 100 else result.stderr
                    }
                    print("❌")

            except subprocess.TimeoutExpired:
                available_tools[tool_name] = {
                    'available': False,
                    'error': 'Command timeout'
                }
                print("⏰")
            except Exception as e:
                available_tools[tool_name] = {
                    'available': False,
                    'error': str(e)
                }
                print("❌")

        self.tools_available = available_tools
        return available_tools

    def run_kali_scan(self, interface='wlan0', scan_duration=30):
        """Ejecutar escaneo WiFi con herramientas de Kali"""
        print(f"\n📡 Running Kali WiFi scan on {interface}...")

        if not self.kali_available:
            print("❌ Kali Linux is not available")
            return None

        try:
            # Crear script temporal para el escaneo
            scan_script = f'''#!/bin/bash
# WiFi Security Scan Script
echo "Starting WiFi security scan..."
echo "Interface: {interface}"
echo "Duration: {scan_duration}s"

# Verificar interfaz
if ! ip link show {interface} > /dev/null 2>&1; then
    echo "Interface {interface} not found"
    exit 1
fi

# Poner interfaz en modo monitor (si es posible)
echo "Setting up monitor mode..."
sudo ip link set {interface} down
sudo iw dev {interface} set type monitor
sudo ip link set {interface} up

# Escanear redes con iwlist
echo "Scanning networks..."
timeout {scan_duration} sudo iwlist {interface} scan 2>/dev/null > /tmp/wifi_scan.txt

# Analizar con airodump-ng si está disponible
if command -v airodump-ng > /dev/null 2>&1; then
    echo "Running airodump-ng..."
    timeout {scan_duration} sudo airodump-ng {interface} -w /tmp/airodump --output-format csv 2>/dev/null
fi

# Obtener información de canales
echo "Analyzing channels..."
iwlist {interface} channel 2>/dev/null > /tmp/channels.txt

echo "Scan completed"
'''

            # Escribir script temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write(scan_script)
                script_path = f.name

            try:
                # Copiar script a WSL y ejecutar
                wsl_script_path = f"/tmp/wifi_scan_{self.session_id}.sh"

                # Copiar script
                copy_cmd = ['wsl', '--', 'cp', script_path, wsl_script_path]
                subprocess.run(copy_cmd, timeout=10)

                # Hacer ejecutable
                chmod_cmd = ['wsl', '--', 'chmod', '+x', wsl_script_path]
                subprocess.run(chmod_cmd, timeout=10)

                # Ejecutar script
                print(f"   🔹 Executing scan script ({scan_duration}s)...")
                run_cmd = ['wsl', '--', 'bash', wsl_script_path]
                result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=scan_duration + 30)

                if result.returncode == 0:
                    print("✅ Scan completed successfully")

                    # Recuperar resultados
                    scan_results = self.retrieve_scan_results()
                    return scan_results
                else:
                    print(f"⚠️  Scan completed with warnings")
                    print(f"   Output: {result.stdout[-200:]}")
                    return self.retrieve_scan_results()

            finally:
                # Limpiar script temporal
                try:
                    os.unlink(script_path)
                    subprocess.run(['wsl', '--', 'rm', '-f', wsl_script_path], timeout=10)
                except:
                    pass

        except Exception as e:
            print(f"❌ Error running Kali scan: {e}")
            return None

    def retrieve_scan_results(self):
        """Recuperar resultados del escaneo desde WSL"""
        results = {}

        try:
            # Recuperar archivo de escaneo
            scan_result = subprocess.run(['wsl', '--', 'cat', '/tmp/wifi_scan.txt'],
                                       capture_output=True, text=True, timeout=10)
            if scan_result.returncode == 0:
                results['wifi_scan'] = self.parse_iwlist_output(scan_result.stdout)

            # Recuperar análisis de canales
            channel_result = subprocess.run(['wsl', '--', 'cat', '/tmp/channels.txt'],
                                          capture_output=True, text=True, timeout=10)
            if channel_result.returncode == 0:
                results['channel_analysis'] = self.parse_channel_output(channel_result.stdout)

            # Recuperar resultados de airodump-ng si existen
            airodump_files = subprocess.run(['wsl', '--', 'ls', '/tmp/airodump*.csv 2>/dev/null'],
                                           capture_output=True, text=True, timeout=10)
            if airodump_files.returncode == 0 and airodump_files.stdout.strip():
                results['airodump'] = self.parse_airodump_output(airodump_files.stdout)

            return results

        except Exception as e:
            print(f"⚠️  Error retrieving scan results: {e}")
            return {'error': str(e)}

    def parse_iwlist_output(self, output):
        """Parsear salida de iwlist scan"""
        networks = []
        current_network = {}
        lines = output.split('\n')

        for line in lines:
            line = line.strip()

            if line.startswith('Cell'):
                if current_network:
                    networks.append(current_network)
                current_network = {'cell': line}

            elif 'ESSID:' in line:
                essid = line.split('ESSID:"')[1].split('"')[0] if '"' in line else 'Hidden'
                current_network['ssid'] = essid

            elif 'Address:' in line:
                mac = line.split('Address:')[1].strip()
                current_network['bssid'] = mac

            elif 'Channel:' in line:
                channel = line.split('Channel:')[1].strip()
                current_network['channel'] = channel

            elif 'Frequency:' in line:
                freq = line.split('Frequency:')[1].split(' ')[0]
                current_network['frequency'] = freq

            elif 'Quality=' in line:
                quality = line.split('Quality=')[1].split('/')[0]
                current_network['quality'] = quality

            elif 'Signal level=' in line:
                signal = line.split('Signal level=')[1].split(' ')[0]
                current_network['signal'] = signal

            elif 'Encryption key:' in line:
                encrypted = 'on' in line.lower()
                current_network['encrypted'] = encrypted

        if current_network:
            networks.append(current_network)

        return {'networks': networks, 'total_found': len(networks)}

    def parse_channel_output(self, output):
        """Parsear análisis de canales"""
        channels = []
        lines = output.split('\n')

        for line in lines:
            if 'Channel' in line and any(char.isdigit() for char in line):
                channels.append(line.strip())

        return {'supported_channels': channels}

    def parse_airodump_output(self, file_list):
        """Parsear salida de airodump-ng"""
        # Simplificado - en implementación real procesaría archivos CSV
        return {'airodump_files': file_list.strip().split('\n')}

    def generate_integration_report(self):
        """Generar reporte de integración con Kali"""
        report_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'wsl_available': self.wsl_available,
            'kali_available': self.kali_available,
            'tools_available': self.tools_available,
            'summary': self.generate_tool_summary()
        }

        # Guardar reporte JSON
        json_file = os.path.join(self.report_dir, f"kali_integration_{self.session_id}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Reporte de texto
        text_file = os.path.join(self.report_dir, f"kali_integration_{self.session_id}.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("KALI LINUX WSL INTEGRATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Session: {self.session_id}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("ENVIRONMENT STATUS:\n")
            f.write("-" * 30 + "\n")
            f.write(f"WSL Available: {'✅ Yes' if self.wsl_available else '❌ No'}\n")
            f.write(f"Kali Linux Available: {'✅ Yes' if self.kali_available else '❌ No'}\n\n")

            if self.tools_available:
                f.write("SECURITY TOOLS STATUS:\n")
                f.write("-" * 30 + "\n")

                available_count = sum(1 for tool in self.tools_available.values() if tool['available'])
                total_count = len(self.tools_available)

                for tool, status in self.tools_available.items():
                    symbol = "✅" if status['available'] else "❌"
                    f.write(f"{symbol} {tool}\n")

                f.write(f"\nSummary: {available_count}/{total_count} tools available\n")

            summary = self.generate_tool_summary()
            f.write(f"\nOVERALL AVAILABILITY: {summary['availability_percentage']:.1f}%\n")

        print(f"📊 Integration report saved:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📝 Text: {text_file}")

        return report_data

    def generate_tool_summary(self):
        """Generar resumen de disponibilidad de herramientas"""
        if not self.tools_available:
            return {'total_tools': 0, 'available_tools': 0, 'availability_percentage': 0}

        total_tools = len(self.tools_available)
        available_tools = sum(1 for tool in self.tools_available.values() if tool['available'])

        return {
            'total_tools': total_tools,
            'available_tools': available_tools,
            'availability_percentage': (available_tools / total_tools * 100) if total_tools > 0 else 0
        }

    def run_complete_integration_check(self):
        """Ejecutar verificación completa de integración"""
        print("🛡️ Kali Linux WSL Integration Check")
        print("=" * 50)
        print(f"Session ID: {self.session_id}")
        print("For professional security use only\n")

        try:
            # 1. Verificar WSL
            distros = self.check_wsl_availability()

            # 2. Verificar Kali
            if self.wsl_available:
                self.check_kali_availability()

                # 3. Iniciar Kali si está disponible
                if self.kali_available:
                    if self.start_kali_wsl():
                        # 4. Verificar herramientas
                        self.check_security_tools()

                        # 5. Generar reporte
                        report = self.generate_integration_report()

                        # 6. Mostrar resumen
                        self.display_integration_summary(report)

                        return report
                    else:
                        print("❌ Cannot start Kali Linux")
                        return None
                else:
                    print("❌ Kali Linux is not available")
                    return None
            else:
                print("❌ WSL is not available")
                return None

        except KeyboardInterrupt:
            print("\n⚠️ Integration check cancelled")
            return None
        except Exception as e:
            print(f"\n❌ Integration check failed: {e}")
            return None

    def display_integration_summary(self, report):
        """Mostrar resumen de integración"""
        print(f"\n🎯 INTEGRATION SUMMARY")
        print("=" * 40)

        print(f"🖥️  WSL: {'✅ Available' if report['wsl_available'] else '❌ Not Available'}")
        print(f"🐧 Kali Linux: {'✅ Available' if report['kali_available'] else '❌ Not Available'}")

        if report['tools_available']:
            summary = report['summary']
            print(f"🛠️  Security Tools: {summary['available_tools']}/{summary['total_tools']} available")
            print(f"📊 Availability: {summary['availability_percentage']:.1f}%")

            if summary['availability_percentage'] >= 80:
                print("✅ EXCELLENT: Ready for professional operations")
            elif summary['availability_percentage'] >= 50:
                print("💡 GOOD: Partial capabilities available")
            else:
                print("⚠️  LIMITED: Install more security tools")

def main():
    """Función principal"""
    integration = KaliWSLIntegration()

    try:
        results = integration.run_complete_integration_check()
        return bool(results)
    except Exception as e:
        print(f"\n❌ Integration check failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)