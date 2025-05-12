import os
import email
import hashlib
import pandas as pd
import tldextract
import dns.resolver
import requests
from bs4 import BeautifulSoup
from email import policy
from email.parser import BytesParser
from sentence_transformers import SentenceTransformer, util
from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import FormulaRule

# Rutas y configuración
EMAIL_DIR = "email"
SALIDA_XLSX = "resultados_phishscope.xlsx"
ACORTADORES = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl']
EXT_PELIGROSAS = ['.exe', '.vbs', '.js', '.scr', '.bat', '.com', '.pif', '.jar', '.wsf', '.hta', '.iso', '.xlsm']

# Carga modelo de embeddings
modelo_nlp = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
PATRONES = {
    "urgencia": ["responda urgentemente", "acción requerida", "urgente", "inicie sesión ahora"],
    "autoridad": ["equipo de seguridad", "soporte técnico", "cuenta oficial"],
    "recompensa": ["ha ganado", "reembolso disponible", "oferta limitada"],
    "castigo": ["suspenderemos su cuenta", "será bloqueado", "último aviso"]
}

def calcular_similitud(texto):
    resultados = {"urgencia": 0, "autoridad": 0, "recompensa": 0, "castigo": 0}
    emb_texto = modelo_nlp.encode(texto, convert_to_tensor=True)
    for categoria, frases in PATRONES.items():
        for frase in frases:
            emb_patron = modelo_nlp.encode(frase, convert_to_tensor=True)
            sim = util.cos_sim(emb_texto, emb_patron).item()
            if sim > 0.7:
                resultados[categoria] += 1
    return resultados

def extraer_urls(html):
    soup = BeautifulSoup(html, "html.parser")
    urls = [a['href'] for a in soup.find_all('a', href=True)]
    return urls

def resolver_redireccion(url):
    try:
        return requests.head(url, allow_redirects=True, timeout=5).url
    except Exception:
        return url

def verificar_auth(domain):
    resultados = {"spf": "❌", "dkim": "❌", "dmarc": "❌"}
    try:
        if any("v=spf1" in r.to_text() for r in dns.resolver.resolve(domain, "TXT")):
            resultados["spf"] = "✔️"
    except: pass
    try:
        if dns.resolver.resolve(f"_dmarc.{domain}", "TXT"):
            resultados["dmarc"] = "✔️"
    except: pass
    try:
        if dns.resolver.resolve(f"selector1._domainkey.{domain}", "TXT"):
            resultados["dkim"] = "✔️"
    except: pass
    return resultados

def analizar_adjuntos(msg):
    adjuntos = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = part.get_filename()
            ext = os.path.splitext(filename)[-1].lower()
            if ext in EXT_PELIGROSAS:
                contenido = part.get_payload(decode=True)
                sha256 = hashlib.sha256(contenido).hexdigest()
                adjuntos.append((filename, sha256))
    return adjuntos

def calcular_phishscore(sim_nlp, urls_info, adjuntos, auth):
    score = 0
    score += sum(sim_nlp.values()) * 10
    score += sum(20 for a in urls_info if a[3] or tldextract.extract(a[1]).registered_domain in ACORTADORES)
    score += 15 * len(adjuntos)
    score += 15 if auth["reply_diff"] else 0
    score += -10 if auth["spf"] == auth["dkim"] == auth["dmarc"] == "✔️" else 10
    return min(score, 100)

# Procesar correos
resultados = []
for archivo in os.listdir(EMAIL_DIR):
    if not archivo.endswith(".eml"):
        continue
    ruta = os.path.join(EMAIL_DIR, archivo)
    with open(ruta, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    remitente = msg.get("From", "")
    reply_to = msg.get("Reply-To", "")
    subject = msg.get("Subject", "")
    cuerpo = msg.get_body(preferencelist=("html", "plain")).get_content()
    urls = extraer_urls(cuerpo)
    urls_info = [(u, resolver_redireccion(u), u, tldextract.extract(u).registered_domain != tldextract.extract(resolver_redireccion(u)).registered_domain) for u in urls]
    sim_nlp = calcular_similitud(subject + " " + cuerpo)
    adjuntos = analizar_adjuntos(msg)
    domain = tldextract.extract(remitente).registered_domain
    auth = verificar_auth(domain)
    auth["reply_diff"] = reply_to and reply_to not in remitente
    score = calcular_phishscore(sim_nlp, urls_info, adjuntos, auth)
    if score >= 70:
        riesgo = "🟥 Phishing muy probable"
    elif score >= 50:
        riesgo = "🟧 Posible phishing"
    elif score >= 30:
        riesgo = "🟨 Sospechoso"
    else:
        riesgo = "🟩 Limpio"
    resultados.append({
        "archivo": archivo,
        "remitente_nombre": remitente.split("<")[0].strip(),
        "remitente_email": remitente.split("<")[-1].strip(">").strip(),
        "subject": subject,
        "score": score,
        "riesgo": riesgo,
        "enlaces": ", ".join(u[1] for u in urls_info),
        "adjuntos": ", ".join(f"{a[0]} ({a[1][:6]}...)" for a in adjuntos),
        "nlp_urgencia": sim_nlp["urgencia"],
        "nlp_autoridad": sim_nlp["autoridad"],
        "nlp_recompensa": sim_nlp["recompensa"],
        "nlp_castigo": sim_nlp["castigo"],
        "spf": auth["spf"],
        "dkim": auth["dkim"],
        "dmarc": auth["dmarc"]
    })

# Exportar a Excel con formato
df = pd.DataFrame(resultados)
df.to_excel(SALIDA_XLSX, index=False)

# Formato condicional
wb = load_workbook(SALIDA_XLSX)
ws = wb.active
col_riesgo = "F"
col_range = f"{col_riesgo}2:{col_riesgo}{ws.max_row}"
colores = [
    ("\"🟥 Phishing muy probable\"", "FF0000"),
    ("\"🟧 Posible phishing\"", "FFA500"),
    ("\"🟨 Sospechoso\"", "FFFF00"),
    ("\"🟩 Limpio\"", "C6EFCE"),
]
for val, color in colores:
    regla = FormulaRule(formula=[f"${col_riesgo}2={val}"], fill=PatternFill(start_color=color, end_color=color, fill_type="solid"))
    ws.conditional_formatting.add(col_range, regla)

# Congelar fila de encabezado y autoajuste de ancho
ws.freeze_panes = "A2"
for col in ws.columns:
    max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
    ws.column_dimensions[col[0].column_letter].width = max(10, max_length + 2)

wb.save(SALIDA_XLSX)
wb.close()
