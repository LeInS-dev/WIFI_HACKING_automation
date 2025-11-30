# 🔥 WiFi Hacking Automation

Basado en el tutorial **"3 Levels of WiFi Hacking"** de NetworkChuck

## ⚠️ ADVERTENCIA IMPORTANTE

Este software es para fines **EDUCATIVOS** y de entrenamiento ético únicamente. Solo debe ser utilizado en redes que le pertenecen o con permiso explícito. El acceso no autorizado a redes WiFi es ilegal y puede tener consecuencias legales graves.

## 📋 Descripción

Esta automatización implementa los tres niveles de hacking WiFi enseñados por NetworkChuck:

1. **Nivel 1**: Descubrimiento y análisis de redes
2. **Nivel 2**: Análisis de handshakes y contraseñas
3. **Nivel 3**: Evil Twin attacks y técnicas avanzadas

## 🚀 Inicio Rápido

### Requisitos
- Python 3.6 o superior
- Windows 10/11 (recomendado)
- Permisos de administrador para algunas funciones

### Ejecución

#### Método 1: Interfaz Gráfica (Recomendado)
```bash
# Doble clic en el archivo o ejecutar:
run_wifi_hacking.bat
```

#### Método 2: Línea de Comandos
```bash
# Nivel 1 - Descubrimiento
python Level1_Discovery/wifi_discovery.py

# Nivel 2 - Análisis de Contraseñas
python Level2_Password/password_analysis.py

# Nivel 3 - Evil Twin Simulation
python Level3_Advanced/evil_twin_sim.py
```

## 📁 Estructura de Directorios

```
WiFi_Hacking_Automation/
├── run_wifi_hacking.bat          # Ejecutable principal
├── wifi_hacking_menu.py          # Interfaz gráfica
├── README.md                     # Este archivo
├── Level1_Discovery/             # Nivel 1: Descubrimiento
│   └── wifi_discovery.py         # Script principal
├── Level2_Password/              # Nivel 2: Contraseñas
│   └── password_analysis.py      # Script principal
├── Level3_Advanced/              # Nivel 3: Evil Twin
│   └── evil_twin_sim.py          # Script principal
└── Reports/                      # Reportes generados
    ├── discovery_*/              # Reportes Nivel 1
    ├── password_analysis_*/      # Reportes Nivel 2
    └── evil_twin_*/              # Reportes Nivel 3
```

## 🔍 Niveles Detallados

### 📡 Nivel 1: Descubrimiento de Redes

**Funcionalidades:**
- Escaneo completo de redes WiFi disponibles
- Análisis de señales y canales
- Identificación de tipos de seguridad (WEP, WPA, WPA2, WPA3)
- Clasificación de redes (abiertas, seguras, ocultas)
- Generación de reportes detallados

**Herramientas simuladas:**
- Wireshark equivalente
- NetSurveyor funcionalidad
- Análisis espectro

**Salida:**
- Reporte JSON con datos completos
- Reporte TXT legible
- Recomendaciones de seguridad

### 🔓 Nivel 2: Análisis de Contraseñas

**Funcionalidades:**
- Análisis estructural de handshakes WPA/WPA2
- Simulación de captura de paquetes
- Creación de wordlists personalizadas
- Análisis de vectores de ataque
- Evaluación de fortaleza de contraseñas

**Conceptos cubiertos:**
- 4-way handshake WPA/WPA2
- Ataques de diccionario
- Técnicas de brute force
- Rainbow tables
- Contramedidas

**Salida:**
- Análisis completo de handshakes
- Simulación de cracking educativa
- Recomendaciones de seguridad

### 👻 Nivel 3: Evil Twin Attacks

**Funcionalidades:**
- Simulación de puntos de acceso falsos
- Implementación de portales cautivos
- Captura simulada de credenciales
- Análisis de riesgos de seguridad

**Técnicas demostradas:**
- Evil Twin creation
- Captive portal attacks
- Man-in-the-middle concepts
- Credential harvesting

**Salida:**
- Reporte detallado de simulación
- Análisis de vulnerabilidades
- Guías de protección

## 📊 Reportes

Cada nivel genera dos tipos de reportes:

### JSON Report
- Datos estructurados completos
- Información técnica detallada
- Metadatos de sesión
- Fácil para procesamiento posterior

### Text Report
- Formato legible para humanos
- Resúmenes ejecutivos
- Recomendaciones claras
- Formato para documentación

## 🛡️ Características de Seguridad

- **Modo Educación**: Todas las operaciones son simuladas
- **Ethical Only**: Advertencias claras y confirmaciones
- **Audit Trail**: Registro completo de todas las actividades
- **No Malicious**: No incluye herramientas de ataque reales
- **Learning Focus**: Enfoque en comprensión y defensa

## 🔧 Configuración

### Variables Modificables
Cada script permite personalizar:

- **Target Networks**: Configurar objetivos específicos
- **Wordlists**: Añadir diccionarios personalizados
- **Output Formats**: Personalizar formatos de reporte
- **Simulation Parameters**: Ajustar parámetros de simulación

### Personalización Avanzada
```python
# Ejemplo de configuración personalizada
config = {
    'target_ssid': 'MyNetwork',
    'scan_timeout': 30,
    'wordlist_custom': ['password1', 'password2'],
    'report_format': ['json', 'txt', 'html']
}
```

## 📚 Referencias Educativas

### Tutorial Original
- **Video**: [3 Levels of WiFi Hacking - NetworkChuck](https://www.youtube.com/watch?v=dZwbb42pdtg)
- **Canal**: NetworkChuck

### Conceptos Fundamentales
- **WiFi Security**: WEP, WPA, WPA2, WPA3
- **Handshake**: 4-way handshake process
- **Attacks**: Dictionary, Brute force, Evil Twin
- **Defense**: Network hardening, monitoring

## 🤝 Contribuciones

Este proyecto es educativo. Para contribuir:

1. Mantener el enfoque educativo
2. No agregar funcionalidades maliciosas
3. Documentar claramente los conceptos
4. Incluir advertencias éticas

## 📄 Licencia

Proyecto educativo de código abierto. Uso responsable únicamente.

## ⚖️ Consideraciones Legales

- **Uso Ético**: Solo en redes propias o con permiso
- **Legalidad**: Cumplir con leyes locales
- **Responsabilidad**: El usuario es responsable del uso
- **Educación**: Propósito exclusivamente educativo

## 🔗 Recursos Adicionales

### Herramientas Reales (para uso ético)
- **Aircrack-ng**: Suite de pruebas WiFi
- **Wireshark**: Analizador de protocolos
- **Kali Linux**: Distribución de pentesting
- **Hashcat**: Recuperación de contraseñas

### Seguridad WiFi
- **WPA3**: Latest security standard
- **Enterprise Solutions**: 802.1X, EAP-TLS
- **Network Segmentation**: VLANs, firewalls
- **Monitoring**: IDS/IPS systems

## 🆘 Ayuda y Soporte

### Problemas Comunes
1. **Python no encontrado**: Instalar Python desde python.org
2. **Permisos**: Ejecutar como administrador
3. **Antivirus**: Puede bloquear scripts educativos
4. **Firewall**: Puede interferir con escaneos

### Comandos Útiles
```bash
# Verificar instalación de Python
python --version

# Verificar módulos requeridos
python -c "import tkinter, subprocess, json, os"

# Ejecutar con permisos (Windows)
# Right-click -> "Run as administrator"
```

## 📈 Próximos Pasos

Después de completar este tutorial:

1. **Estudiar seguridad WiFi**: Aprender conceptos avanzados
2. **Certificaciones**: Considerar certificaciones éticas
3. **Herramientas reales**: Explorar suites profesionales
4. **Seguridad empresarial**: Implementar en entornos reales

---

**Recuerde**: Con grandes conocimientos vienen grandes responsabilidades. Use estos conocimientos para proteger, no para atacar. 🛡️