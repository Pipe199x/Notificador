import os
import json
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración (desde secretos)
REMITENTE_EMAIL = os.getenv("REMITENTE_EMAIL")
CONTRASENA_EMAIL = os.getenv("CONTRASENA_EMAIL")
DESTINATARIO_EMAIL = os.getenv("DESTINATARIO_EMAIL")
LOGIN_URL = "https://fe.libellum.co/"
USUARIO = os.getenv("LOGIN_USUARIO")
CLAVE = os.getenv("LOGIN_CLAVE")
REGISTRO_DATOS = "datos_enviados.json"

def enviar_email(asunto, mensaje):
    try:
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = REMITENTE_EMAIL
        msg['To'] = DESTINATARIO_EMAIL

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(REMITENTE_EMAIL, CONTRASENA_EMAIL)
            server.sendmail(REMITENTE_EMAIL, DESTINATARIO_EMAIL, msg.as_string())

        print("📧 Correo enviado correctamente.")
    except Exception as e:
        print("❌ Error enviando el correo:", e)

def cargar_datos_enviados():
    if os.path.exists(REGISTRO_DATOS):
        with open(REGISTRO_DATOS, "r") as f:
            return json.load(f)
    return []

def guardar_datos_enviados(datos):
    with open(REGISTRO_DATOS, "w") as f:
        json.dump(datos, f, indent=2)

def iniciar_sesion():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Documento']"))
    )
    driver.find_element(By.XPATH, "//input[@placeholder='Documento']").send_keys(USUARIO)
    driver.find_element(By.XPATH, "//input[@placeholder='Clave de Acceso']").send_keys(CLAVE)
    driver.find_element(By.XPATH, "//button[text()='Ingresar']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "page-content"))
    )
    return driver

def navegar_y_extraer(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Documentos')]"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )

    filas = driver.find_elements(By.XPATH, "//table/tbody/tr")
    datos = []
    for fila in filas:
        columnas = fila.find_elements(By.XPATH, "./th | ./td")
        if len(columnas) >= 8:
            datos.append({
                "documento": columnas[1].text.strip(),
                "razon_social": columnas[2].text.strip(),
                "fecha": columnas[3].text.strip(),
                "estado": columnas[4].text.strip(),
                "total_factura": columnas[7].text.strip()
            })
    return datos

if __name__ == "__main__":
    try:
        driver = iniciar_sesion()
        datos_extraidos = navegar_y_extraer(driver)
        driver.quit()

        anteriores = cargar_datos_enviados()
        nuevos = [d for d in datos_extraidos if d not in anteriores]

        if nuevos:
            mensaje = "🆕 Nuevos documentos:\n\n"
            for d in nuevos:
                mensaje += (
                    f"Documento: {d['documento']}\n"
                    f"Razón Social: {d['razon_social']}\n"
                    f"Fecha: {d['fecha']}\n"
                    f"Estado: {d['estado']}\n"
                    f"Total Factura: {d['total_factura']}\n\n"
                )
            enviar_email("Notificación de Nuevos Documentos", mensaje)
            guardar_datos_enviados(datos_extraidos)
        else:
            print("📭 No hay nuevos documentos.")
    except Exception as e:
        print("🚨 Error general:", e)
