# 📄 README.md — PhishScope

## 🛡️ ¿Qué es PhishScope?
PhishScope es una herramienta OSINT defensiva diseñada para Blue Teams y analistas SOC que permite analizar grandes volúmenes de correos `.eml` y `.msg` para detectar amenazas de phishing, incluso si no contienen enlaces maliciosos visibles.

---

## ⚙️ Características principales
- ✅ Análisis contextual con NLP (embeddings semánticos)
- ✅ Verificación SPF, DKIM y DMARC
- ✅ Análisis de adjuntos sospechosos por extensión y SHA256
- ✅ Resolución y extracción de URLs, incluyendo redirecciones
- ✅ Sistema de puntuación multivariable (PhishScore)
- ✅ Exportación a Excel con colores de riesgo automático
- ✅ Procesamiento masivo por lotes
- ✅ Configuración completamente editable vía archivo `config.json`
- ✅ Soporte para correos `.msg` (Outlook)

---

## 📁 Estructura del Proyecto
```
PhishScope/
├── email/                      # Carpeta con correos .eml y .msg a analizar
├── config.json                 # Configuración editable
├── config_loader.py            # Lector del JSON
├── phiscope_batch.py           # Script principal
├── resultados_phishscope.xlsx # Resultados en Excel
├── requirements_windows.txt    # Dependencias Windows
├── requirements_linux.txt      # Dependencias Linux/macOS
└── README.md
```

---

## 📦 Requisitos
### 🪟 Windows
- Python 3.9+
- PowerShell

### 🐧 Linux/macOS
- Python 3.9+
- Bash / Terminal

---

## ▶️ Instalación paso a paso
```bash
# Clona el repositorio
git clone https://github.com/U7Dani/PhishScope.git
cd PhishScope

# Crear entorno virtual
# Windows:
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements_windows.txt  # o requirements_linux.txt
```

---

## ⚙️ Configuración por JSON
Toda la configuración está en `config.json`. Ejemplo:
```json
{
  "EMAIL_DIR": "email",
  "SALIDA_XLSX": "resultados_phishscope.xlsx",
  "ACORTADORES": ["bit.ly", "tinyurl.com", "t.co", "goo.gl"],
  "EXT_PELIGROSAS": [".exe", ".vbs", ".js", ".scr", ".bat", ".com", ".pif", ".jar", ".wsf", ".hta", ".iso", ".xlsm"],
  "PATRONES": {
    "urgencia": ["responda urgentemente", "acción requerida", "urgente", "inicie sesión ahora"],
    "autoridad": ["equipo de seguridad", "soporte técnico", "cuenta oficial"],
    "recompensa": ["ha ganado", "reembolso disponible", "oferta limitada"],
    "castigo": ["suspenderemos su cuenta", "será bloqueado", "último aviso"]
  }
}
```
Puedes adaptarlo sin tocar el código Python.

---

## 📂 Formatos soportados
| Formato | Soporte | Descripción                           |
|---------|---------|---------------------------------------|
| `.eml`  | ✅       | Estándar MIME                         |
| `.msg`  | ✅       | Correos individuales de Outlook       |
| `.pst`  | 🔜       | (planeado) Buzones exportados Outlook |

---

## 🚀 Ejecución del análisis
```bash
python phiscope_batch.py
```
El resultado estará en `resultados_phishscope.xlsx` con colores según el riesgo.

---

## 📊 ¿Cómo funciona PhishScore?
| Factor                           | Peso estimado |
|----------------------------------|---------------|
| Patrones NLP (urgencia, etc.)   | 30%           |
| Enlaces redirigidos/acortados   | 20%           |
| Adjuntos peligrosos             | 15%           |
| Headers anómalos (Reply-To)     | 15%           |
| SPF/DKIM/DMARC inválidos        | 20%           |

---

## 🧪 Niveles de riesgo en Excel
| Score         | Riesgo                  | Color     |
|---------------|--------------------------|-----------|
| 0–29          | Limpio                  | 🟩 Verde   |
| 30–49         | Sospechoso              | 🟨 Amarillo|
| 50–69         | Posible phishing        | 🟧 Naranja |
| 70–100        | Phishing muy probable   | 🟥 Rojo    |

---

## 🔒 Privacidad
No se envían datos a servicios externos. Solo:
- Consultas DNS para autenticación de dominio
- Resolución de redirecciones HTTP

---

## 📄 Licencia
MIT — libre para uso profesional, defensivo o educativo.

---

## 🙋 Contacto
¿Ideas, feedback o colaboración? Crea un issue en GitHub o contáctame en [LinkedIn](https://www.linkedin.com/in/danielsanchezgarcia).