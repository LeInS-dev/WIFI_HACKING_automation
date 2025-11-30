#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Professional Toolkit - Level 1: Professional WiFi Discovery
Real operational WiFi network discovery and analysis
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
import datetime
import re
import threading
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProfessionalWiFiDiscovery:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = f"../Reports/professional_discovery_{self.session_id}"
        os.makedirs(self.report_dir, exist_ok=True)
        self.discovered_networks = []
        self.interface_info = {}

    def check_wifi_interface(self):
        """Verificar y obtener información de interfaces WiFi"""
        print("🔍 Analyzing WiFi interfaces...")

        try:
            # Windows: netsh wlan show interfaces
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                interfaces = self.parse_interfaces(result.stdout)
                self.interface_info = interfaces
                print(f"✅ Found {len(interfaces)} WiFi interface(s)")
                return interfaces
            else:
                print("❌ Error getting WiFi interface information")
                return []

        except Exception as e:
            print(f"❌ Error checking interfaces: {e}")
            return []

    def parse_interfaces(self, output):
        """Parsear salida de netsh interfaces"""
        interfaces = []
        current_interface = {}
        lines = output.split('\n')

        for line in lines:
            line = line.strip()
            if 'Nombre' in line or 'Name' in line:
                if ':' in line:
                    current_interface['name'] = line.split(':', 1)[1].strip()
            elif 'Estado' in line or 'State' in line:
                if ':' in line:
                    current_interface['state'] = line.split(':', 1)[1].strip()
            elif 'Descripción' in line or 'Description' in line:
                if ':' in line:
                    current_interface['description'] = line.split(':', 1)[1].strip()
            elif 'GUID' in line:
                if ':' in line:
                    current_interface['guid'] = line.split(':', 1)[1].strip()
                    interfaces.append(current_interface.copy())
                    current_interface = {}

        return interfaces

    def scan_networks_comprehensive(self):
        """Escaneo comprehensivo de redes WiFi"""
        print("📡 Performing comprehensive WiFi network scan...")
        networks = []

        try:
            # Método 1: Escaneo básico con netsh
            print("   🔹 Basic network discovery...")
            basic_networks = self.scan_with_netsh()
            networks.extend(basic_networks)

            # Método 2: Escaneo de BSSIDs extendido
            print("   🔹 Extended BSSID discovery...")
            extended_networks = self.scan_bssid_details()
            self.merge_network_data(networks, extended_networks)

            # Método 3: Análisis de canales
            print("   🔹 Channel analysis...")
            self.analyze_channels(networks)

            # Método 4: Verificación de seguridad
            print("   🔹 Security analysis...")
            self.analyze_security(networks)

            print(f"✅ Comprehensive scan completed. Found {len(networks)} networks")
            return networks

        except Exception as e:
            print(f"❌ Error during comprehensive scan: {e}")
            return []

    def scan_with_netsh(self):
        """Escaneo básico usando netsh"""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                                  capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return self.parse_netsh_networks(result.stdout)
            else:
                print("⚠️  Basic scan failed, trying alternative method...")
                return self.scan_networks_alternative()

        except Exception as e:
            print(f"⚠️  Netsh scan error: {e}")
            return self.scan_networks_alternative()

    def scan_networks_alternative(self):
        """Método alternativo de escaneo"""
        networks = []
        try:
            # Intentar con netsh sin BSSID
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks'],
                                  capture_output=True, text=True, timeout=20)

            if result.returncode == 0:
                networks = self.parse_simple_networks(result.stdout)

        except Exception as e:
            print(f"⚠️  Alternative scan also failed: {e}")

        return networks

    def parse_netsh_networks(self, output):
        """Parsear salida completa de netsh con BSSIDs"""
        networks = []
        current_network = {}
        lines = output.split('\n')

        for line in lines:
            line = line.strip()

            if line.startswith('SSID'):
                if current_network:
                    networks.append(current_network)

                ssid_part = line.split(':', 1) if ':' in line else [line, '']
                ssid = ssid_part[1].strip() if len(ssid_part) > 1 else 'Hidden Network'
                if not ssid:
                    ssid = 'Hidden Network'

                current_network = {
                    'ssid': ssid,
                    'bssids': [],
                    'signals': [],
                    'channels': [],
                    'security_types': [],
                    'authentication': [],
                    'encryption': [],
                    'network_types': [],
                    'bands': [],
                    'first_seen': datetime.now().isoformat()
                }

            elif current_network:
                if line.startswith('Autenticación') or line.startswith('Authentication'):
                    if ':' in line:
                        auth_type = line.split(':', 1)[1].strip()
                        current_network['authentication'].append(auth_type)

                elif line.startswith('Cifrado') or line.startswith('Encryption'):
                    if ':' in line:
                        enc_type = line.split(':', 1)[1].strip()
                        current_network['encryption'].append(enc_type)

                elif line.startswith('Tipo de red') or line.startswith('Network type'):
                    if ':' in line:
                        net_type = line.split(':', 1)[1].strip()
                        current_network['network_types'].append(net_type)

                elif line.startswith('BSSID'):
                    if ':' in line:
                        bssid = line.split(':', 1)[1].strip()
                        if bssid and len(bssid) >= 17:  # Validar formato MAC
                            current_network['bssids'].append(bssid)

                elif line.startswith('Señal') or line.startswith('Signal'):
                    if ':' in line:
                        signal = line.split(':', 1)[1].strip().replace('%', '')
                        try:
                            signal_dbm = self.convert_percentage_to_dbm(int(signal))
                            current_network['signals'].append({
                                'percentage': int(signal),
                                'dbm': signal_dbm
                            })
                        except:
                            current_network['signals'].append({'percentage': signal, 'dbm': 'N/A'})

                elif line.startswith('Canal') or line.startswith('Channel'):
                    if ':' in line:
                        channel = line.split(':', 1)[1].strip()
                        current_network['channels'].append(channel)

                elif line.startswith('Banda') or line.startswith('Band'):
                    if ':' in line:
                        band = line.split(':', 1)[1].strip()
                        current_network['bands'].append(band)

        if current_network:
            networks.append(current_network)

        return networks

    def parse_simple_networks(self, output):
        """Parsear salida simple de netsh (sin BSSID)"""
        networks = []
        lines = output.split('\n')

        for line in lines:
            if 'SSID' in line and ':' in line:
                ssid = line.split(':', 1)[1].strip()
                if ssid:
                    networks.append({
                        'ssid': ssid,
                        'bssids': [],
                        'signals': [],
                        'channels': [],
                        'security_types': [],
                        'authentication': [],
                        'encryption': [],
                        'network_types': [],
                        'bands': [],
                        'first_seen': datetime.now().isoformat(),
                        'note': 'Limited data - BSSID scan required'
                    })

        return networks

    def scan_bssid_details(self):
        """Obtener detalles adicionales de BSSIDs"""
        # Esta función podría usar WSL/Kali para obtener más detalles
        # Por ahora, devuelve estructura para futura implementación
        return []

    def merge_network_data(self, networks, additional_data):
        """Combinar datos de diferentes métodos de escaneo"""
        for additional in additional_data:
            found = False
            for network in networks:
                if network['ssid'] == additional.get('ssid'):
                    # Combinar datos sin duplicar
                    for key in ['bssids', 'channels', 'signals']:
                        if key in additional:
                            for item in additional[key]:
                                if item not in network[key]:
                                    network[key].append(item)
                    found = True
                    break

            if not found:
                networks.append(additional)

    def analyze_channels(self, networks):
        """Analizar distribución y superposición de canales"""
        channel_analysis = {}

        for network in networks:
            for channel in network.get('channels', []):
                try:
                    ch_num = int(re.findall(r'\d+', str(channel))[0])
                    if ch_num not in channel_analysis:
                        channel_analysis[ch_num] = []
                    channel_analysis[ch_num].append(network['ssid'])
                except:
                    pass

        # Agregar análisis de interferencias
        for network in networks:
            network['channel_interference'] = self.calculate_interference(
                network.get('channels', []), channel_analysis
            )

    def calculate_interference(self, channels, channel_analysis):
        """Calcular nivel de interferencia de canal"""
        max_interference = 0

        for channel in channels:
            try:
                ch_num = int(re.findall(r'\d+', str(channel))[0])
                if ch_num in channel_analysis:
                    interference = len(channel_analysis[ch_num]) - 1  # Menos sí mismo
                    max_interference = max(max_interference, interference)
            except:
                pass

        return {
            'max_networks_same_channel': max_interference,
            'interference_level': 'High' if max_interference > 3 else 'Medium' if max_interference > 1 else 'Low'
        }

    def analyze_security(self, networks):
        """Analizar configuraciones de seguridad"""
        for network in networks:
            auth_types = network.get('authentication', [])
            enc_types = network.get('encryption', [])

            # Determinar nivel de seguridad
            if 'WPA3' in str(auth_types):
                security_level = 'Excellent'
            elif 'WPA2' in str(auth_types):
                security_level = 'Good'
            elif 'WPA' in str(auth_types):
                security_level = 'Fair'
            elif 'Open' in str(auth_types) or not auth_types:
                security_level = 'Poor'
            else:
                security_level = 'Unknown'

            # Detectar vulnerabilidades comunes
            vulnerabilities = []

            if 'WEP' in str(enc_types):
                vulnerabilities.append('WEP encryption deprecated')

            if 'WPA' in str(auth_types) and 'WPA2' not in str(auth_types):
                vulnerabilities.append('WPA only vulnerable to KRACK attacks')

            if not auth_types:
                vulnerabilities.append('Open network - no encryption')

            network['security_analysis'] = {
                'level': security_level,
                'vulnerabilities': vulnerabilities,
                'recommendations': self.generate_security_recommendations(security_level, vulnerabilities)
            }

    def generate_security_recommendations(self, security_level, vulnerabilities):
        """Generar recomendaciones de seguridad"""
        recommendations = []

        if security_level in ['Poor', 'Fair']:
            recommendations.append('Upgrade to WPA2 or WPA3')

        if 'WEP' in str(vulnerabilities):
            recommendations.append('Disable WEP encryption immediately')

        if 'Open network' in str(vulnerabilities):
            recommendations.append('Implement encryption and authentication')

        if not recommendations:
            recommendations.append('Security configuration is adequate')

        return recommendations

    def convert_percentage_to_dbm(self, percentage):
        """Convertir porcentaje de señal a dBm"""
        # Fórmula aproximada: dBm = -100 + (percentage * 0.6)
        return round(-100 + (percentage * 0.6), 1)

    def ping_gateways(self):
        """Verificar conectividad con gateways detectados"""
        print("🌐 Checking gateway connectivity...")

        try:
            # Obtener gateway default
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            gateways = re.findall(r'Gateway.*?:\s*([\d\.]+)', result.stdout)

            connectivity_results = {}
            for gateway in gateways:
                try:
                    ping_result = subprocess.run(['ping', '-n', '1', gateway],
                                              capture_output=True, text=True, timeout=5)
                    connectivity_results[gateway] = {
                        'responsive': ping_result.returncode == 0,
                        'response_time': self.extract_ping_time(ping_result.stdout)
                    }
                except:
                    connectivity_results[gateway] = {'responsive': False, 'response_time': 'N/A'}

            return connectivity_results

        except Exception as e:
            print(f"⚠️  Gateway connectivity check failed: {e}")
            return {}

    def extract_ping_time(self, ping_output):
        """Extraer tiempo de respuesta de ping"""
        try:
            time_match = re.search(r'tiempo[=<](\d+)ms', ping_output, re.IGNORECASE)
            if time_match:
                return f"{time_match.group(1)}ms"
            return 'N/A'
        except:
            return 'N/A'

    def run_professional_discovery(self):
        """Ejecutar descubrimiento WiFi profesional completo"""
        print("🛡️ WiFi Security Professional Toolkit - Professional Discovery")
        print("=" * 70)
        print(f"🔬 Session ID: {self.session_id}")
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("⚠️  For authorized security testing only")
        print()

        discovery_results = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'scan_parameters': {
                'scan_type': 'comprehensive_professional',
                'methods_used': ['netsh_bssid', 'channel_analysis', 'security_audit'],
                'platform': f"{sys.platform}"
            }
        }

        try:
            # 1. Verificar interfaces
            interfaces = self.check_wifi_interface()
            discovery_results['interfaces'] = interfaces

            # 2. Escaneo comprehensivo
            networks = self.scan_networks_comprehensive()
            discovery_results['networks'] = networks

            # 3. Verificar conectividad
            gateway_connectivity = self.ping_gateways()
            discovery_results['gateway_connectivity'] = gateway_connectivity

            # 4. Análisis adicional
            analysis = self.generate_professional_analysis(networks)
            discovery_results['analysis'] = analysis

            # 5. Generar reportes
            self.generate_professional_reports(discovery_results)

            # 6. Mostrar resumen
            self.display_summary(discovery_results)

            print(f"\n✅ Professional discovery completed successfully")
            print(f"📊 Reports saved to: {self.report_dir}")

            return discovery_results

        except KeyboardInterrupt:
            print(f"\n⚠️ Discovery cancelled by user")
            return None
        except Exception as e:
            print(f"\n❌ Discovery failed: {e}")
            return None

    def generate_professional_analysis(self, networks):
        """Generar análisis profesional de las redes descubiertas"""
        analysis = {
            'network_summary': {
                'total_networks': len(networks),
                'unique_ssids': len(set(net['ssid'] for net in networks if net['ssid'] != 'Hidden Network')),
                'hidden_networks': len([net for net in networks if net['ssid'] == 'Hidden Network']),
                'networks_with_bssids': len([net for net in networks if net.get('bssids')]),
                'total_bssids': sum(len(net.get('bssids', [])) for net in networks)
            },
            'security_analysis': {
                'excellent_security': len([net for net in networks
                                         if net.get('security_analysis', {}).get('level') == 'Excellent']),
                'good_security': len([net for net in networks
                                    if net.get('security_analysis', {}).get('level') == 'Good']),
                'fair_security': len([net for net in networks
                                    if net.get('security_analysis', {}).get('level') == 'Fair']),
                'poor_security': len([net for net in networks
                                    if net.get('security_analysis', {}).get('level') == 'Poor']),
            },
            'channel_analysis': {
                'channels_used': sorted(set(
                    ch for net in networks for ch in net.get('channels', [])
                    if ch.isdigit()
                )),
                'channel_distribution': {},
                'high_interference_networks': len([net for net in networks
                                                  if net.get('channel_interference', {}).get('interference_level') == 'High'])
            }
        }

        # Analizar distribución de canales
        for net in networks:
            for ch in net.get('channels', []):
                if ch.isdigit():
                    if ch not in analysis['channel_analysis']['channel_distribution']:
                        analysis['channel_analysis']['channel_distribution'][ch] = 0
                    analysis['channel_analysis']['channel_distribution'][ch] += 1

        return analysis

    def generate_professional_reports(self, discovery_results):
        """Generar reportes profesionales en JSON y texto"""
        # Reporte JSON
        json_file = os.path.join(self.report_dir, f"professional_discovery_{self.session_id}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(discovery_results, f, indent=2, ensure_ascii=False)

        # Reporte de texto profesional
        text_file = os.path.join(self.report_dir, f"professional_discovery_{self.session_id}.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("WIFI SECURITY PROFESSIONAL TOOLKIT - NETWORK DISCOVERY REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"SESSION INFORMATION:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Session ID: {discovery_results['session_id']}\n")
            f.write(f"Date: {discovery_results['timestamp']}\n")
            f.write(f"Platform: {discovery_results['scan_parameters']['platform']}\n")
            f.write(f"Scan Type: {discovery_results['scan_parameters']['scan_type']}\n\n")

            # Análisis de redes
            analysis = discovery_results['analysis']
            f.write("NETWORK ANALYSIS SUMMARY:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total Networks Discovered: {analysis['network_summary']['total_networks']}\n")
            f.write(f"Unique SSIDs: {analysis['network_summary']['unique_ssids']}\n")
            f.write(f"Hidden Networks: {analysis['network_summary']['hidden_networks']}\n")
            f.write(f"Networks with BSSID Data: {analysis['network_summary']['networks_with_bssids']}\n")
            f.write(f"Total BSSIDs Detected: {analysis['network_summary']['total_bssids']}\n\n")

            # Análisis de seguridad
            f.write("SECURITY ANALYSIS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Excellent Security (WPA3): {analysis['security_analysis']['excellent_security']}\n")
            f.write(f"Good Security (WPA2): {analysis['security_analysis']['good_security']}\n")
            f.write(f"Fair Security (WPA): {analysis['security_analysis']['fair_security']}\n")
            f.write(f"Poor Security (Open/WEP): {analysis['security_analysis']['poor_security']}\n\n")

            # Análisis de canales
            f.write("CHANNEL ANALYSIS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Channels Used: {', '.join(analysis['channel_analysis']['channels_used'])}\n")
            f.write(f"Networks with High Interference: {analysis['channel_analysis']['high_interference_networks']}\n")

            f.write("\nChannel Distribution:\n")
            for channel, count in sorted(analysis['channel_analysis']['channel_distribution'].items()):
                f.write(f"  Channel {channel}: {count} networks\n")
            f.write("\n")

            # Detalles de redes
            f.write("DETAILED NETWORK INFORMATION:\n")
            f.write("-" * 40 + "\n")

            for i, network in enumerate(discovery_results['networks'], 1):
                f.write(f"\n{i}. SSID: {network['ssid']}\n")
                if network.get('bssids'):
                    f.write(f"   BSSIDs: {', '.join(network['bssids'])}\n")
                if network.get('authentication'):
                    f.write(f"   Authentication: {', '.join(network['authentication'])}\n")
                if network.get('encryption'):
                    f.write(f"   Encryption: {', '.join(network['encryption'])}\n")
                if network.get('channels'):
                    f.write(f"   Channels: {', '.join(network['channels'])}\n")
                if network.get('signals'):
                    avg_signal = sum(s.get('percentage', 0) for s in network['signals']) / len(network['signals'])
                    f.write(f"   Average Signal: {avg_signal:.1f}%\n")

                sec_analysis = network.get('security_analysis', {})
                if sec_analysis:
                    f.write(f"   Security Level: {sec_analysis.get('level', 'Unknown')}\n")
                    if sec_analysis.get('vulnerabilities'):
                        f.write(f"   Vulnerabilities: {', '.join(sec_analysis['vulnerabilities'])}\n")
                    if sec_analysis.get('recommendations'):
                        f.write(f"   Recommendations: {', '.join(sec_analysis['recommendations'])}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("REPORT GENERATED: WiFi Security Professional Toolkit\n")
            f.write("For authorized security testing purposes only\n")

        print(f"📊 Professional reports generated:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📝 Text: {text_file}")

    def display_summary(self, discovery_results):
        """Mostrar resumen en consola"""
        analysis = discovery_results['analysis']
        networks = discovery_results['networks']

        print(f"\n🎯 PROFESSIONAL DISCOVERY SUMMARY")
        print("=" * 50)
        print(f"📊 Total Networks: {analysis['network_summary']['total_networks']}")
        print(f"🔐 Security Distribution:")
        print(f"   🟢 Excellent (WPA3): {analysis['security_analysis']['excellent_security']}")
        print(f"   🔵 Good (WPA2): {analysis['security_analysis']['good_security']}")
        print(f"   🟡 Fair (WPA): {analysis['security_analysis']['fair_security']}")
        print(f"   🔴 Poor (Open/WEP): {analysis['security_analysis']['poor_security']}")
        print(f"📡 Channel Analysis:")
        print(f"   Channels Used: {len(analysis['channel_analysis']['channels_used'])}")
        print(f"   High Interference: {analysis['channel_analysis']['high_interference_networks']} networks")

def main():
    """Función principal"""
    print("🛡️ WiFi Security Professional Toolkit - Level 1: Professional Discovery")
    print("⚠️  AUTHORIZED SECURITY TESTING ONLY")
    print("   Requires explicit permission for operational use")
    print()

    discovery = ProfessionalWiFiDiscovery()

    try:
        results = discovery.run_professional_discovery()
        return bool(results)
    except Exception as e:
        print(f"\n❌ Professional discovery failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)