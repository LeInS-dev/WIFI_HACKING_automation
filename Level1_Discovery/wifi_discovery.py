#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Hacking Automation - Nivel 1: Descubrimiento de Redes
NetworkChuck Tutorial Implementation
Author: Claude AI Assistant
"""

import subprocess
import json
import time
import datetime
import os
import re
from datetime import datetime

class WiFiDiscovery:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = f"../Reports/discovery_{self.session_id}"
        os.makedirs(self.report_dir, exist_ok=True)

    def check_interface(self):
        """Verificar interfaces WiFi disponibles"""
        print("🔍 Verificando interfaces WiFi...")
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'],
                                  capture_output=True, text=True)
            interfaces = []
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Nombre' in line or 'Name' in line:
                    interfaces.append(line.split(':')[1].strip())
            return interfaces
        except Exception as e:
            print(f"❌ Error verificando interfaces: {e}")
            return []

    def scan_networks(self):
        """Escaneo de redes WiFi disponibles"""
        print("📡 Escaneando redes WiFi disponibles...")
        networks = []

        try:
            # Usar netsh para escanear redes en Windows
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                                  capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                networks = self.parse_networks(result.stdout)
                print(f"✅ Encontradas {len(networks)} redes")
            else:
                print("❌ Error al escanear redes")

        except subprocess.TimeoutExpired:
            print("⏰ Tiempo de escaneo expirado")
        except Exception as e:
            print(f"❌ Error durante el escaneo: {e}")

        return networks

    def parse_networks(self, output):
        """Parsear salida del escaneo de redes"""
        networks = []
        current_network = {}
        lines = output.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('SSID'):
                if current_network:
                    networks.append(current_network)
                current_network = {
                    'ssid': line.split(':')[1].strip() if ':' in line else 'Hidden Network',
                    'bssids': [],
                    'signal_strengths': [],
                    'channels': [],
                    'security_types': []
                }
            elif line.startswith('Tipo de autenticación') or line.startswith('Authentication'):
                if ':' in line:
                    auth_type = line.split(':')[1].strip()
                    if current_network:
                        current_network['security_types'].append(auth_type)
            elif line.startswith('Señal') or line.startswith('Signal'):
                if ':' in line:
                    signal = line.split(':')[1].strip()
                    if current_network:
                        current_network['signal_strengths'].append(signal)
            elif line.startswith('Canal') or line.startswith('Channel'):
                if ':' in line:
                    channel = line.split(':')[1].strip()
                    if current_network:
                        current_network['channels'].append(channel)
            elif line.startswith('BSSID'):
                if ':' in line:
                    bssid = line.split(':')[1].strip()
                    if current_network:
                        current_network['bssids'].append(bssid)

        if current_network:
            networks.append(current_network)

        return networks

    def analyze_networks(self, networks):
        """Análisis de redes encontradas"""
        print("🔬 Analizando redes encontradas...")

        analysis = {
            'total_networks': len(networks),
            'open_networks': 0,
            'secured_networks': 0,
            'hidden_networks': 0,
            'unique_channels': set(),
            'security_distribution': {},
            'high_signal_networks': []
        }

        for network in networks:
            # Clasificar por seguridad
            if network['ssid'] == 'Hidden Network':
                analysis['hidden_networks'] += 1
            elif any('Open' in sec or 'Abierta' in sec for sec in network['security_types']):
                analysis['open_networks'] += 1
            else:
                analysis['secured_networks'] += 1

            # Analizar canales
            for channel in network['channels']:
                if channel.isdigit():
                    analysis['unique_channels'].add(int(channel))

            # Contar tipos de seguridad
            for sec_type in network['security_types']:
                if sec_type in analysis['security_distribution']:
                    analysis['security_distribution'][sec_type] += 1
                else:
                    analysis['security_distribution'][sec_type] = 1

            # Redes con señal fuerte
            for signal in network['signal_strengths']:
                if '%' in signal:
                    try:
                        signal_value = int(signal.replace('%', '').strip())
                        if signal_value > 70:
                            analysis['high_signal_networks'].append({
                                'ssid': network['ssid'],
                                'signal': signal_value
                            })
                    except ValueError:
                        pass

        analysis['unique_channels'] = list(analysis['unique_channels'])
        return analysis

    def generate_report(self, networks, analysis):
        """Generar reporte en formato JSON y texto"""
        print("📄 Generando reporte...")

        # Datos completos del reporte
        report_data = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'scan_summary': {
                'total_networks_found': analysis['total_networks'],
                'open_networks': analysis['open_networks'],
                'secured_networks': analysis['secured_networks'],
                'hidden_networks': analysis['hidden_networks']
            },
            'networks': networks,
            'analysis': analysis,
            'recommendations': self.generate_recommendations(analysis)
        }

        # Guardar JSON
        json_file = os.path.join(self.report_dir, f"discovery_report_{self.session_id}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Generar reporte en texto plano
        text_file = os.path.join(self.report_dir, f"discovery_report_{self.session_id}.txt")
        self.generate_text_report(report_data, text_file)

        print(f"✅ Reportes guardados en:")
        print(f"   📊 JSON: {json_file}")
        print(f"   📝 Texto: {text_file}")

        return report_data

    def generate_text_report(self, data, filename):
        """Generar reporte en formato texto plano"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("WiFi HACKING AUTOMATION - NIVEL 1: DESCUBRIMIENTO\n")
            f.write("="*60 + "\n\n")

            f.write(f"SESIÓN: {data['session_id']}\n")
            f.write(f"FECHA Y HORA: {data['timestamp']}\n\n")

            f.write("RESUMEN DEL ESCANEO:\n")
            f.write("-" * 30 + "\n")
            summary = data['scan_summary']
            f.write(f"Total de redes encontradas: {summary['total_networks_found']}\n")
            f.write(f"Redes abiertas: {summary['open_networks']}\n")
            f.write(f"Redes seguras: {summary['secured_networks']}\n")
            f.write(f"Redes ocultas: {summary['hidden_networks']}\n\n")

            f.write("ANÁLISIS DETALLADO:\n")
            f.write("-" * 30 + "\n")
            analysis = data['analysis']
            f.write(f"Canales únicos utilizados: {', '.join(map(str, analysis['unique_channels']))}\n")
            f.write(f"Redes con señal fuerte (>70%): {len(analysis['high_signal_networks'])}\n\n")

            if analysis['security_distribution']:
                f.write("DISTRIBUCIÓN DE TIPOS DE SEGURIDAD:\n")
                for sec_type, count in analysis['security_distribution'].items():
                    f.write(f"  {sec_type}: {count} redes\n")
                f.write("\n")

            f.write("REDES ENCONTRADAS:\n")
            f.write("-" * 30 + "\n")
            for i, network in enumerate(data['networks'], 1):
                f.write(f"\n{i}. SSID: {network['ssid']}\n")
                f.write(f"   BSSIDs: {', '.join(network['bssids'])}\n")
                f.write(f"   Seguridad: {', '.join(network['security_types'])}\n")
                f.write(f"   Señales: {', '.join(network['signal_strengths'])}\n")
                f.write(f"   Canales: {', '.join(network['channels'])}\n")

            f.write("\nRECOMENDACIONES:\n")
            f.write("-" * 30 + "\n")
            for i, rec in enumerate(data['recommendations'], 1):
                f.write(f"{i}. {rec}\n")

    def generate_recommendations(self, analysis):
        """Generar recomendaciones basadas en el análisis"""
        recommendations = []

        if analysis['open_networks'] > 0:
            recommendations.append(f"⚠️  Se encontraron {analysis['open_networks']} redes abiertas. Estas redes representan riesgos de seguridad.")

        if len(analysis['unique_channels']) < 4:
            recommendations.append("📡 Hay poca diversidad de canales. Considera configurar tu red en canales menos congestionados.")

        if analysis['secured_networks'] < analysis['open_networks']:
            recommendations.append("🔒 Menos del 50% de las redes están seguras. Esto indica un entorno de baja seguridad general.")

        if len(analysis['high_signal_networks']) > 5:
            recommendations.append("📶 Muchas redes con señal fuerte. Considera el posible solapamiento e interferencia.")

        recommendations.append("✅ Para redes propias: implementa WPA3 o WPA2-Enterprise para máxima seguridad.")
        recommendations.append("🔐 Cambia contraseñas por defecto y actualiza firmware de routers regularmente.")

        return recommendations

    def run_scan(self):
        """Ejecutar escaneo completo"""
        print("🚀 INICIANDO ESCANEO WIFI - NIVEL 1")
        print("="*50)

        # Verificar interfaces
        interfaces = self.check_interface()
        if not interfaces:
            print("❌ No se encontraron interfaces WiFi")
            return None

        print(f"✅ Interfaces detectadas: {', '.join(interfaces)}")

        # Escanear redes
        networks = self.scan_networks()

        if not networks:
            print("❌ No se encontraron redes")
            return None

        # Analizar redes
        analysis = self.analyze_networks(networks)

        # Generar reporte
        report = self.generate_report(networks, analysis)

        print("\n🎉 ESCANEO COMPLETADO EXITOSAMENTE")
        print("="*50)
        print(f"📊 Total redes: {analysis['total_networks']}")
        print(f"🔓 Redes abiertas: {analysis['open_networks']}")
        print(f"🔒 Redes seguras: {analysis['secured_networks']}")
        print(f"👻 Redes ocultas: {analysis['hidden_networks']}")

        return report

def main():
    """Función principal para ejecutar el descubrimiento"""
    print("🔥 WiFi Hacking Automation - Nivel 1: Descubrimiento de Redes")
    print("   Tutorial basado en NetworkChuck")
    print("   ⚠️  USO ÉTICO: Solo para redes propias o con permiso explícito")
    print()

    discovery = WiFiDiscovery()

    try:
        report = discovery.run_scan()
        if report:
            print(f"\n✅ Reporte guardado con éxito en: {discovery.report_dir}")
            return True
        else:
            print("\n❌ No se pudo completar el escaneo")
            return False
    except KeyboardInterrupt:
        print("\n⚠️  Escaneo cancelado por usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)