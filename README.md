
![image](https://github.com/user-attachments/assets/a5297153-e9c3-425d-84c5-95bdf72aac8e)



# 🛡️ **PhishScope**

**PhishScope** es una herramienta **OSINT defensiva** desarrollada para Blue Teams y analistas SOC. Permite analizar grandes volúmenes de correos `.eml` y detectar phishing, incluso sin enlaces maliciosos visibles.

---

## ⚙️ Características principales

- ✅ Análisis contextual con NLP (embeddings semánticos)
- ✅ Extracción y resolución de URLs (incluye redirecciones)
- ✅ Verificación de autenticidad del remitente (SPF, DKIM, DMARC)
- ✅ Detección de adjuntos sospechosos y generación de hash SHA256
- ✅ PhishScore configurable por múltiples señales
- ✅ Exportación a Excel con colores por nivel de riesgo
- ✅ Procesamiento por lotes de archivos `.eml`

---

## 💻 Instalación por sistema operativo

### 🪟 Windows

#### 🧱 Requisitos

- Python 3.9+ → [Descargar desde aquí](https://www.python.org/downloads/windows/)
- PowerShell o CMD
- Git (opcional)

#### 📦 Instalación paso a paso

powershell
# Clona el repositorio
git clone https://github.com/U7Dani/PhishScope.git
cd PhishScope

# Crea y activa un entorno virtual
py -3 -m venv .venv
.venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt
🐧 Linux / macOS
🧱 Requisitos
Python 3.9+ (sudo apt install python3.9 python3.9-venv)

Git

pip (python3 -m ensurepip)

curl (opcional)

📦 Instalación paso a paso
bash
Copiar
Editar
git clone https://github.com/U7Dani/PhishScope.git
cd PhishScope

# Crea y activa el entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt

### 📁 Estructura del proyecto
```bash
PhishScope/
├── email/                        # Carpeta donde se colocan los archivos .eml
├── phiscope_batch.py            # Script principal de análisis
├── resultados_phishscope.xlsx   # Resultado en Excel con colores
├── requirements.txt             # Lista de dependencias
├── README.md                    # Documentación
```

---

### ▶️ ¿Cómo usar?
1. Coloca tus correos `.eml` en la carpeta `email/`.

2. Activa el entorno virtual:

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

3. Ejecuta el análisis:
```bash
python phiscope_batch.py
```

4. Abre `resultados_phishscope.xlsx` para visualizar el análisis con colores según el nivel de riesgo.

---

### 🧪 ¿Cómo funciona el PhishScore?

| Factor                         | Peso estimado |
|-------------------------------|---------------|
| Patrones NLP (urgencia, etc.) | 30%           |
| Enlaces redirigidos/acortados | 20%           |
| Adjuntos peligrosos           | 15%           |
| Headers anómalos (Reply-To)   | 15%           |
| SPF/DKIM/DMARC inválidos      | 20%           |

---

### 📊 Niveles de riesgo (colores en Excel)

| Score     | Riesgo                | Color   |
|-----------|------------------------|---------|
| 0 – 29    | Limpio                 | 🟩 Verde     |
| 30 – 49   | Sospechoso             | 🟨 Amarillo  |
| 50 – 69   | Posible phishing       | 🟧 Naranja   |
| 70 – 100  | Phishing muy probable  | 🟥 Rojo      |


![image](https://github.com/user-attachments/assets/88d71699-013c-4737-97eb-ccac10ea19af)


🔒 Privacidad y seguridad
La herramienta no envía contenido sensible a servicios externos.

Solo realiza:

Consultas DNS (SPF/DKIM/DMARC)

Peticiones HTTP HEAD para resolver redirecciones

📅 Última actualización
📆 12 de mayo de 2025

📄 Licencia
Este proyecto está bajo la Licencia MIT.
Libre para modificar, estudiar y usar en entornos defensivos o educativos.

🙋 Contacto y colaboración
¿Ideas? ¿Sugerencias? ¿Colaboraciones?

👉 Abre un issue en el repositorio o contacta por LinkedIn.
   https://www.linkedin.com/in/danielsánchezgarcía/
