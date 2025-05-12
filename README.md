# 🛡️ PhishScope

**PhishScope** es una herramienta OSINT defensiva diseñada para Blue Teams y analistas SOC. Permite analizar grandes volúmenes de correos `.eml` en busca de phishing, incluso sin enlaces maliciosos visibles.

---

## 🧠 Características destacadas

✅ Análisis contextual del contenido (NLP + embeddings semánticos)  
✅ Verificación de autenticidad del remitente (SPF, DKIM, DMARC)  
✅ Análisis de adjuntos por extensión y SHA256  
✅ Extracción y resolución de URLs (incl. redirecciones encadenadas)  
✅ PhishScore multivariable configurable  
✅ Exportación visual a Excel con colores por nivel de riesgo  
✅ Procesamiento por lotes de correos `.eml`

---

## 📦 Requisitos

- Python 3.9 o superior
- Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

## 📁 Estructura

```
phiscope_core/
├── email/                   # Carpeta para los archivos .eml
├── phiscope_batch.py        # Script principal de análisis
├── resultados_phishscope.xlsx # Excel generado con resultados
├── requirements.txt         # Dependencias necesarias
```

---

## ▶️ Cómo usar

1. Coloca tus correos `.eml` en la carpeta `email/`
2. Activa tu entorno virtual:
```bash
.venv\Scripts\activate
```
3. Ejecuta el análisis:
```bash
python phiscope_batch.py
```
4. Abre `resultados_phishscope.xlsx` para ver el análisis con formato condicional.

---

## 🧪 PhishScore

Sistema de puntuación basado en múltiples factores:

| Factor                         | Peso aproximado |
|-------------------------------|------------------|
| Patrones NLP (urgencia, etc.) | 30%              |
| Enlaces acortados/redirigidos | 20%              |
| Adjuntos sospechosos          | 15%              |
| Headers técnicos              | 15%              |
| SPF/DKIM/DMARC inválidos      | 20%              |

---

## 📊 Niveles de riesgo

| Score       | Riesgo                | Color   |
|-------------|------------------------|---------|
| 0 - 29      | Limpio                 | 🟩 Verde |
| 30 - 49     | Sospechoso             | 🟨 Amarillo |
| 50 - 69     | Posible phishing       | 🟧 Naranja |
| 70 - 100    | Phishing muy probable  | 🟥 Rojo |

---

## 🔒 Privacidad

No se requiere conexión a servicios externos salvo para resolver redirecciones o verificar autenticidad DNS.

---

## 📅 Última actualización
2025-05-12

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 🙋 ¿Preguntas o sugerencias?

Abre un issue o escríbeme si quieres colaborar.
