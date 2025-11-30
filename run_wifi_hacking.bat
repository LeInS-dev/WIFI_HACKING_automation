@echo off
chcp 65001 >nul
title WiFi Hacking Automation - NetworkChuck Tutorial
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔥 WiFi Hacking Automation 🔥                ║
echo ║            Basado en "3 Levels of WiFi Hacking"             ║
echo ║                  Tutorial de NetworkChuck                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ADVERTENCIA IMPORTANTE ⚠️
echo    Este software es para fines EDUCATIVOS y de entrenamiento ético únicamente.
echo    Solo debe ser utilizado en redes que le pertenecen o con permiso explícito.
echo    El acceso no autorizado a redes WiFi es ilegal y tiene consecuencias legales.
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

:MENU
echo Por favor seleccione una opción:
echo.
echo 1️⃣  Iniciar Interfaz Gráfica (Recomendado)
echo 2️⃣  Ejecutar Nivel 1 - Descubrimiento de Redes (Línea de comandos)
echo 3️⃣  Ejecutar Nivel 2 - Análisis de Contraseñas (Línea de comandos)
echo 4️⃣  Ejecutar Nivel 3 - Evil Twin Simulation (Línea de comandos)
echo 5️⃣  Ver Reportes Generados
echo 6️⃣  Instalar Dependencias (Python requerido)
echo 7️⃣  Información y Ayuda
echo 8️⃣  Salir
echo.
set /p choice="Seleccione una opción (1-8): "

if "%choice%"=="1" goto GUI
if "%choice%"=="2" goto LEVEL1
if "%choice%"=="3" goto LEVEL2
if "%choice%"=="4" goto LEVEL3
if "%choice%"=="5" goto REPORTS
if "%choice%"=="6" goto INSTALL
if "%choice%"=="7" goto HELP
if "%choice%"=="8" goto EXIT
echo.
echo ❌ Opción no válida. Por favor seleccione 1-8.
echo.
goto MENU

:GUI
echo.
echo 🖥️  Iniciando Interfaz Gráfica...
echo.
python wifi_hacking_menu.py
if errorlevel 1 (
    echo.
    echo ❌ Error al ejecutar la interfaz gráfica.
    echo    Asegúrese de tener Python instalado correctamente.
    echo.
    pause
)
goto MENU

:LEVEL1
echo.
echo 📡 Iniciando Nivel 1: Descubrimiento de Redes...
echo.
cd Level1_Discovery
python wifi_discovery.py
cd ..
echo.
pause
goto MENU

:LEVEL2
echo.
echo 🔓 Iniciando Nivel 2: Análisis de Contraseñas...
echo.
cd Level2_Password
python password_analysis.py
cd ..
echo.
pause
goto MENU

:LEVEL3
echo.
echo 👻 Iniciando Nivel 3: Evil Twin Simulation...
echo.
echo ⚠️  ADVERTENCIA: Este nivel simula ataques avanzados.
echo    Es puramente educativo y no debe ser usado maliciosamente.
echo.
pause
cd Level3_Advanced
python evil_twin_sim.py
cd ..
echo.
pause
goto MENU

:REPORTS
echo.
echo 📊 Buscando reportes generados...
echo.
if exist "Reports" (
    echo Se encontraron los siguientes reportes:
    echo.
    dir Reports /s /b *.txt *.json
    echo.
    echo Los reportes están en formato JSON y texto plano.
    echo Puede abrirlos con cualquier editor de texto.
) else (
    echo ❌ No se encontró la carpeta de reportes.
    echo    Ejecute primero alguno de los niveles para generar reportes.
)
echo.
pause
goto MENU

:INSTALL
echo.
echo 🔧 Verificando e instalando dependencias...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH.
    echo.
    echo Por favor:
    echo 1. Descargue Python desde https://python.org/downloads/
    echo 2. Instale Python asegurándose de marcar "Add Python to PATH"
    echo 3. Reinicie esta aplicación
    echo.
    pause
    goto MENU
)

echo ✅ Python detectado.
echo.
echo Verificando módulos requeridos...
python -c "import tkinter, subprocess, json, os, sys, threading, datetime, socket" 2>nul
if errorlevel 1 (
    echo ⚠️  Algunos módulos Python podrían faltar.
    echo    Intentando instalar módulos estándar...
    echo.
    echo NOTA: La mayoría de los módulos requeridos vienen con Python.
    echo Si experimenta problemas, reinstale Python completamente.
) else (
    echo ✅ Todos los módulos requeridos están disponibles.
)
echo.
pause
goto MENU

:HELP
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                       📚 INFORMACIÓN                        ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║                                                              ║
echo ║ AUTOMATIZACIÓN WIFI - TUTORIAL NETWORKCHUCK                 ║
echo ║                                                              ║
echo ║ NIVELES DISPONIBLES:                                        ║
echo ║                                                              ║
echo ║ 📡 NIVEL 1 - Descubrimiento de Redes:                       ║
echo ║    • Escaneo de redes WiFi disponibles                      ║
echo ║    • Análisis de señales y canales                          ║
echo ║    • Identificación de tipos de seguridad                   ║
echo ║    • Generación de reportes detallados                      ║
echo ║                                                              ║
echo ║ 🔓 NIVEL 2 - Análisis de Contraseñas:                       ║
echo ║    • Estructura de handshakes WPA/WPA2                      ║
echo ║    • Simulación de captura de paquetes                      ║
echo ║    • Análisis de vectores de ataque                         ║
echo ║    • Evaluación de fortaleza de contraseñas                 ║
echo ║                                                              ║
echo ║ 👻 NIVEL 3 - Evil Twin Attacks:                             ║
echo ║    • Simulación de puntos de acceso falsos                  ║
echo ║    • Implementación de portales cautivos                     ║
echo ║    • Captura simulada de credenciales                       ║
echo ║    • Análisis de riesgos de seguridad                       ║
echo ║                                                              ║
echo ║ CARACTERÍSTICAS:                                            ║
echo ║ • Generación automática de reportes en JSON y TXT           ║
echo ║ • Interfaz gráfica intuitiva                                ║
echo ║ • Registro completo de actividades                          ║
echo ║ • Simulaciones educativas seguras                           ║
echo ║                                                              ║
echo ║ REQUISITOS:                                                 ║
echo ║ • Python 3.6+ instalado                                     ║
echo ║ • Windows 10/11 (recomendado)                              ║
echo ║ • Permisos de administrador para algunas funciones          ║
echo ║                                                              ║
echo ║ USO ÉTICO:                                                  ║
echo ║ Este software es diseñado exclusivamente para:              ║
echo ║ • Entrenamiento educativo                                   ║
echo ║ • Pruebas en redes propias                                  ║
echo ║ • Demostraciones con permiso explícito                       ║
echo ║                                                              ║
echo ║ NO DEBE SER UTILIZADO PARA:                                 ║
echo ║ • Acceder a redes ajenas sin permiso                        ║
echo ║ • Actividades maliciosas ilegales                          ║
echo ║ • Cualquier fin no ético                                   ║
echo ║                                                              ║
echo ║ Para más información, consulte el tutorial original:        ║
echo ║ https://www.youtube.com/watch?v=dZwbb42pdtg                 ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
goto MENU

:EXIT
echo.
echo 👋 Gracias por usar WiFi Hacking Automation.
echo    Recuerde usar estos conocimientos de manera ética y responsable.
echo.
timeout /t 2 >nul
exit /b 0