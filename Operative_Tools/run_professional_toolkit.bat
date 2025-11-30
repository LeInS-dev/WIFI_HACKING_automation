@echo off
chcp 65001 >nul
title WiFi Security Professional Toolkit
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                🛡️ WiFi Security Professional Toolkit 🛡️                ║
echo ║                    Herramienta Operativa para Empresas                     ║
echo ║                          de Seguridad WiFi                                ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ADVERTENCIA IMPORTANTE ⚠️
echo    Esta herramienta está diseñada EXCLUSIVAMENTE para:
echo    • Empresas de seguridad cibernética profesionales
echo    • Pruebas de penetración con autorización explícita
echo    • Auditorías de seguridad en redes propias o contratadas
echo    • Cumplimiento normativo y evaluaciones de riesgo
echo.
echo    El uso no autorizado está prohibido y puede tener consecuencias legales.
echo.
echo ═════════════════════════════════════════════════════════════════════════
echo.

:MENU
echo Por favor seleccione una opción:
echo.
echo 1️⃣  Iniciar Interfaz Gráfica Profesional (Recomendado)
echo 2️⃣  Ejecutar Network Discovery (Línea de comandos)
echo 3️⃣  Verificar Herramientas Disponibles
echo 4️⃣  Ver Reportes Generados
echo 5️⃣  Documentación y Ayuda
echo 6️⃣  Configurar Entorno WSL/Kali
echo 7️⃣  Información Legal y Ética
echo 8️⃣  Salir
echo.
set /p choice="Seleccione una opción (1-8): "

if "%choice%"=="1" goto GUI
if "%choice%"=="2" goto DISCOVERY
if "%choice%"=="3" goto TOOLS
if "%choice%"=="4" goto REPORTS
if "%choice%"=="5" goto HELP
if "%choice%"=="6" goto WSL
if "%choice%"=="7" goto LEGAL
if "%choice%"=="8" goto EXIT
echo.
echo ❌ Opción no válida. Por favor seleccione 1-8.
echo.
goto MENU

:GUI
echo.
echo 🖥️  Iniciando Interfaz Gráfica Profesional...
echo.
python professional_wifi_security_toolkit.py
if errorlevel 1 (
    echo.
    echo ❌ Error al ejecutar la interfaz profesional.
    echo    Asegúrese de tener Python instalado correctamente.
    echo.
    pause
)
goto MENU

:DISCOVERY
echo.
echo 📡 Ejecutando Network Discovery Profesional...
echo.
cd Level1_RealDiscovery
python professional_wifi_discovery.py
if errorlevel 1 (
    echo.
    echo ❌ Error en el descubrimiento de redes.
    echo.
) else (
    echo ✅ Descubrimiento completado exitosamente.
)
cd ..
echo.
pause
goto MENU

:TOOLS
echo.
echo 🔧 Verificando herramientas de seguridad disponibles...
echo.
cd Tools_Check
python check_tools.py
cd ..
echo.
pause
goto MENU

:REPORTS
echo.
echo 📊 Buscando reportes profesionales generados...
echo.
if exist "..\Reports" (
    echo Se encontraron los siguientes reportes profesionales:
    echo.
    dir ..\Reports /s /b *.txt *.json
    echo.
    echo Los reportes están en formato JSON y texto profesional.
    echo Puede abrirlos con cualquier editor de texto.
) else (
    echo ❌ No se encontró la carpeta de reportes.
    echo    Ejecute primero alguna operación para generar reportes.
)
echo.
pause
goto MENU

:HELP
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                       📚 DOCUMENTACIÓN PROFESIONAL                        ║
echo ╠════════════════════════════════════════════════════════════════════════╣
echo ║                                                                              ║
echo ║ WIFI SECURITY PROFESSIONAL TOOLKIT                                         ║
echo ║ Versión Operativa para Empresas de Seguridad                               ║
echo ║                                                                              ║
echo ║ CAPACIDADES OPERATIVAS:                                                     ║
echo ║                                                                              ║
echo ║ 📡 NETWORK DISCOVERY:                                                       ║
echo ║    • Escaneo profesional de redes WiFi                                     ║
echo ║    • Análisis de interfaces y configuración                                ║
echo ║    • Detección de BSSIDs y análisis de canales                              ║
echo ║    • Evaluación de señales y cobertura                                     ║
echo ║                                                                              ║
echo ║ 🔐 SECURITY AUDIT:                                                          ║
echo ║    • Análisis de configuraciones de seguridad                              ║
echo ║    • Identificación de vulnerabilidades comunes                            ║
echo ║    • Evaluación de cifrado y autenticación                                 ║
echo ║    • Recomendaciones de hardening                                          ║
echo ║                                                                              ║
echo ║ 🛠️ HERRAMIENTAS PROFESIONALES:                                              ║
echo ║    • Integración con herramientas nativas de Windows                       ║
echo ║    • Soporte para WSL/Kali Linux                                           ║
echo ║    • Verificación de capacidades operativas                                ║
echo ║    • Generación de reportes profesionales                                 ║
echo ║                                                                              ║
echo ║ REQUISITOS OPERATIVOS:                                                      ║
echo ║ • Windows 10/11 con WSL2                                                  ║
echo ║ • Python 3.6+ instalado                                                  ║
echo ║ • Kali Linux WSL (opcional, para capacidades completas)                   ║
echo ║ • Permisos de administrador para algunas funciones                        ║
echo ║                                                                              ║
echo ║ USO PROFESIONAL AUTORIZADO:                                                ║
echo ║ Esta herramienta está diseñada exclusivamente para:                        ║
echo ║ • Empresas de seguridad cibernética                                        ║
echo ║ • Consultores de seguridad autorizados                                     ║
echo ║ • Auditorías con consentimiento explícito                                 ║
echo ║ • Pruebas en infraestructura propia                                       ║
echo ║                                                                              ║
echo ║ CARACTERÍSTICAS TÉCNICAS:                                                   ║
echo ║ • Reportes en formato JSON y texto profesional                            ║
echo ║ • Interfaz gráfica intuitiva para operaciones                             ║
echo ║ • Registro completo de actividades                                         ║
echo ║ • Cumplimiento con estándares de seguridad                                ║
echo ║                                                                              ║
echo ║ INTEGRACIÓN CON HERRAMIENTAS:                                               ║
echo ║ • Windows nativo: netsh, ipconfig, ping, etc.                            ║
echo ║ • Python Security: scapy, requests, nmap                                 ║
echo ║ • WSL/Kali: aircrack-ng, hashcat, wireshark, etc.                       ║
echo ║                                                                              ║
echo ║ Para más información sobre capacidades operativas:                         ║
echo ║ Consulte la documentación completa en cada módulo                         ║
echo ║                                                                              ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
pause
goto MENU

:WSL
echo.
echo 🔧 Configuración de Entorno WSL/Kali Linux
echo ===========================================
echo.
echo Esta opción configurará la integración con Kali Linux para capacidades
echo completas de seguridad WiFi. Se requiere WSL2 instalado.
echo.
echo ⚠️  NOTA: Esta configuración requiere conocimientos avanzados de Linux.
echo.
set /p wsl_confirm="¿Desea proceder con la configuración WSL? (S/N): "
if /i "%wsl_confirm%"=="S" (
    echo.
    echo 🐧 Iniciando configuración WSL/Kali...
    python wsl_kali_integration.py
) else (
    echo Configuración cancelada.
)
echo.
pause
goto MENU

:LEGAL
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                       ⚖️ INFORMACIÓN LEGAL Y ÉTICA                       ║
echo ╠════════════════════════════════════════════════════════════════════════╣
echo ║                                                                              ║
echo ║ TÉRMINOS DE USO PROFESIONAL                                                 ║
echo ║                                                                              ║
echo ║ Esta herramienta está diseñada exclusivamente para uso profesional         ║
echo ║ autorizado en el campo de la seguridad cibernética.                         ║
echo ║                                                                              ║
echo ║ REQUISITOS LEGALES:                                                         ║
echo ║ • Autorización explícita por escrito del propietario de la red             ║
echo ║ • Contrato de servicios de seguridad cibernética                           ║
echo ║ • Cumplimiento de leyes locales y regulaciones aplicables                  ║
echo ║ • Certificaciones profesionales en seguridad (recomendado)                ║
echo ║                                                                              ║
echo ║ USO AUTORIZADO:                                                             ║
echo ║ • Auditorías de seguridad en redes cliente                                 ║
echo ║ • Pruebas de penetración éticas                                            ║
echo ║ • Evaluaciones de vulnerabilidades autorizadas                             ║
echo ║ • Cumplimiento normativo (PCI DSS, ISO 27001, etc.)                       ║
echo ║                                                                              ║
echo ║ USO PROHIBIDO:                                                              ║
echo ║ • Acceso no autorizado a redes ajenas                                     ║
echo ║ • Actividades maliciosas o ilegales                                       ║
echo ║ • Violación de privacidad o confidencialidad                               ║
echo ║ • Cualquier fin que no sea seguridad profesional autorizada                 ║
echo ║                                                                              ║
echo ║ RESPONSABILIDAD:                                                            ║
echo ║ El usuario es responsable del cumplimiento de todas las leyes              ║
echo ║ y regulaciones aplicables. El desarrollador no se responsibilityiza        ║
echo ║ del mal uso de esta herramienta.                                            ║
echo ║                                                                              ║
echo ║ CERTIFICACIONES RECOMENDADAS:                                               ║
echo ║ • Certified Ethical Hacker (CEH)                                           ║
echo ║ • Offensive Security Certified Professional (OSCP)                         ║
echo ║ • CompTIA Security+                                                        ║
echo ║ • GIAC Certified Penetration Tester (GPEN)                                ║
echo ║                                                                              ║
echo ║ ESTÁNDARES DE CUMPLIMIENTO:                                                 ║
echo ║ • NIST Cybersecurity Framework                                            ║
echo ║ • ISO/IEC 27001                                                           ║
echo ║ • PCI DSS (para redes que procesan tarjetas)                             ║
echo ║ • GDPR (para datos en la UE)                                               ║
echo ║                                                                              ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo Al utilizar esta herramienta, usted confirma que:
echo 1. Tiene autorización explícita para las pruebas
echo 2. Es un profesional de seguridad cibernética calificado
echo 3. Cumple con todas las leyes y regulaciones aplicables
echo 4. Acepta toda la responsabilidad por el uso de la herramienta
echo.
pause
goto MENU

:EXIT
echo.
echo 👍 Gracias por usar WiFi Security Professional Toolkit.
echo    Recuerde utilizar estas herramientas de manera ética y profesional.
echo.
timeout /t 2 >nul
exit /b 0