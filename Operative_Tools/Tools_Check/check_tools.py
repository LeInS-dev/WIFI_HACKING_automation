#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Professional Toolkit - Tool Verification
Checks availability of security tools for operational use
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
import platform
import json
from datetime import datetime

class ToolVerifier:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = "../Reports/tool_verification"
        os.makedirs(self.report_dir, exist_ok=True)

        # Herramientas profesionales por categoría
        self.tools_categories = {
            "Windows_Nativo": {
                "netsh": ["netsh", "wlan", "show", "networks"],
                "ping": ["ping", "-n", "1", "127.0.0.1"],
                "tracert": ["tracert", "-h", "1", "127.0.0.1"],
                "arp": ["arp", "-a"],
                "ipconfig": ["ipconfig", "/all"],
                "nslookup": ["nslookup", "google.com"],
            },
            "Python_Security": {
                "scapy": ["python", "-c", "import scapy; print('Scapy available')"],
                "requests": ["python", "-c", "import requests; print('Requests available')"],
                "nmap": ["python", "-c", "import nmap; print('Python-nmap available')"],
                "pywifi": ["python", "-c", "import pywifi; print('PyWifi available')"],
            },
            "Wireless_Security": {
                # Estas herramientas estarían disponibles en Kali Linux
                "aircrack-ng": ["aircrack-ng", "--help"],
                "airodump-ng": ["airodump-ng", "--help"],
                "aireplay-ng": ["aireplay-ng", "--help"],
                "airmon-ng": ["airmon-ng", "--help"],
                "wash": ["wash", "--help"],
                "reaver": ["reaver", "--help"],
                "bully": ["bully", "--help"],
                "pixiewps": ["pixiewps", "--help"],
            },
            "Network_Analysis": {
                "nmap": ["nmap", "--version"],
                "wireshark": ["wireshark", "--version"],
                "tshark": ["tshark", "--version"],
                "tcpdump": ["tcpdump", "--version"],
                "netcat": ["nc", "--help"],
                "masscan": ["masscan", "--version"],
            },
            "Password_Recovery": {
                "john": ["john", "--version"],
                "hashcat": ["hashcat", "--version"],
                "hydra": ["hydra", "--version"],
                "medusa": ["medusa", "--help"],
            }
        }

    def check_tool(self, category, tool_name, command):
        """Verificar si una herramienta está disponible"""
        try:
            if platform.system() == "Windows" and category in ["Wireless_Security", "Network_Analysis", "Password_Recovery"]:
                # Estas herramientas no suelen estar disponibles nativamente en Windows
                return {
                    "available": False,
                    "note": "Tool requires Kali Linux or manual installation",
                    "platform": "Linux/WSL"
                }

            result = subprocess.run(command, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                return {
                    "available": True,
                    "output": result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout,
                    "platform": platform.system()
                }
            else:
                return {
                    "available": False,
                    "error": result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr,
                    "returncode": result.returncode,
                    "platform": platform.system()
                }

        except subprocess.TimeoutExpired:
            return {
                "available": False,
                "error": "Command timeout",
                "platform": platform.system()
            }
        except FileNotFoundError:
            return {
                "available": False,
                "error": "Tool not found in PATH",
                "platform": platform.system()
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "platform": platform.system()
            }

    def run_verification(self):
        """Ejecutar verificación completa de herramientas"""
        print("🔍 WiFi Security Professional Toolkit - Tool Verification")
        print("=" * 60)
        print(f"🖥️  Platform: {platform.system()} {platform.release()}")
        print(f"🕐 Session: {self.session_id}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        results = {}

        for category, tools in self.tools_categories.items():
            print(f"🔧 Checking {category.replace('_', ' ')} tools...")
            category_results = {}

            for tool_name, command in tools.items():
                print(f"   📱 {tool_name}...", end=" ")
                result = self.check_tool(category, tool_name, command)
                category_results[tool_name] = result

                if result["available"]:
                    print("✅ Available")
                else:
                    print("❌ Not Available")

            results[category] = category_results
            print()

        # Generar reporte
        self.generate_report(results)

        return results

    def generate_report(self, results):
        """Generar reporte de verificación de herramientas"""
        # Reporte JSON
        json_file = os.path.join(self.report_dir, f"tool_verification_{self.session_id}.json")

        report_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "platform": f"{platform.system()} {platform.release()}",
            "results": results,
            "summary": self.generate_summary(results)
        }

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        # Reporte de texto
        text_file = os.path.join(self.report_dir, f"tool_verification_{self.session_id}.txt")

        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("WIFI SECURITY PROFESSIONAL TOOLKIT - TOOL VERIFICATION REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Platform: {platform.system()} {platform.release()}\n\n")

            for category, tools in results.items():
                f.write(f"\n{category.replace('_', ' ').upper()} TOOLS:\n")
                f.write("-" * 50 + "\n")

                for tool_name, result in tools.items():
                    status = "✅ AVAILABLE" if result["available"] else "❌ NOT AVAILABLE"
                    f.write(f"{tool_name:20} : {status}\n")

                    if not result["available"] and "note" in result:
                        f.write(f"{'':22}   📝 {result['note']}\n")
                    elif not result["available"] and "error" in result:
                        f.write(f"{'':22}   ⚠️  {result['error']}\n")

            f.write("\n" + "=" * 70 + "\n")
            f.write("SUMMARY:\n")
            f.write("-" * 50 + "\n")
            summary = self.generate_summary(results)
            f.write(f"Total tools checked: {summary['total_tools']}\n")
            f.write(f"Available tools: {summary['available_tools']}\n")
            f.write(f"Available percentage: {summary['availability_percentage']:.1f}%\n")

        print(f"📊 Tool verification report saved:")
        print(f"   📄 JSON: {json_file}")
        print(f"   📝 Text: {text_file}")

        # Mostrar resumen
        summary = self.generate_summary(results)
        print(f"\n📋 SUMMARY:")
        print(f"   Total tools checked: {summary['total_tools']}")
        print(f"   Available tools: {summary['available_tools']}")
        print(f"   Availability: {summary['availability_percentage']:.1f}%")

        if summary['availability_percentage'] < 50:
            print(f"\n⚠️  RECOMMENDATION: Use Kali Linux WSL for full operational capabilities")
        elif summary['availability_percentage'] < 80:
            print(f"\n💡 RECOMMENDATION: Install missing security tools for full functionality")
        else:
            print(f"\n✅ EXCELLENT: Your system is well-equipped for WiFi security operations")

    def generate_summary(self, results):
        """Generar resumen de disponibilidad de herramientas"""
        total_tools = 0
        available_tools = 0

        for category, tools in results.items():
            for tool_name, result in tools.items():
                total_tools += 1
                if result["available"]:
                    available_tools += 1

        return {
            "total_tools": total_tools,
            "available_tools": available_tools,
            "availability_percentage": (available_tools / total_tools * 100) if total_tools > 0 else 0
        }

def main():
    """Función principal"""
    print("🛡️  WiFi Security Professional Toolkit - Tool Verification")
    print("⚠️  For professional security company use only")
    print("   Requires proper authorization for operational use\n")

    verifier = ToolVerifier()

    try:
        results = verifier.run_verification()
        return True
    except KeyboardInterrupt:
        print("\n⚠️  Tool verification cancelled by user")
        return False
    except Exception as e:
        print(f"\n❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)