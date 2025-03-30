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

# 🔐 Variables de entorno (cargadas desde GitHub Secrets)
REMITENTE_EMAIL = os.getenv("REMITENTE_EMAIL")
CONTRASENA_EMAIL = os.getenv("CONTRASENA_EMAIL")
DESTINATARIO_EMAIL = os.getenv("DESTINATARIO_EMAIL")
LOGIN_USUARIO = os.getenv("LOGIN_USUARIO")
LOGIN_CLAVE = os.getenv("LOGIN_CLAVE")
LOGIN_URL = "https://fe.libellum.co/"
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
        print("❌ Error al enviar correo:", e)


def cargar_datos_enviados():
    if os.path.exists(REGISTRO_DATOS):
        with open(REGISTRO_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def guardar_datos_enviados(datos):
    with open(REGISTRO_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


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
    driver.find_element(By.XPATH, "//input[@placeholder='Documento']").send_keys(LOGIN_USUARIO)
    driver.find_element(By.XPATH, "//input[@placeholder='Clave de Acceso']").send_keys(LOGIN_CLAVE)
    driver.find_element(By.XPATH, "//button[text()='Ingresar']").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "page-content"))
    )
    print("✅ Inicio de sesión exitoso.")
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
        # 1. Iniciar sesión y extraer datos
        driver = iniciar_sesion()
        datos_extraidos = navegar_y_extraer(driver)
        driver.quit()

        # 2. Cargar el registro de documentos ya enviados
        datos_enviados = cargar_datos_enviados()

        # 3. Detectar nuevos documentos
        nuevos_datos = [d for d in datos_extraidos if d not in datos_enviados]

        if nuevos_datos:
            # 4. Construir mensaje
            mensaje = "🆕 Nuevos documentos encontrados:\n\n"
            for d in nuevos_datos:
                mensaje += (
                    f"📄 Documento: {d['documento']}\n"
                    f"🏢 Razón Social: {d['razon_social']}\n"
                    f"📅 Fecha: {d['fecha']}\n"
                    f"✅ Estado DIAN: {d['estado']}\n"
                    f"💰 Total Factura: {d['total_factura']}\n\n"
                )

            # 5. Enviar correo
            enviar_email("Notificación de Nuevos Documentos", mensaje)

            # 6. Actualizar el JSON con todos los documentos conocidos
            guardar_datos_enviados(datos_enviados + nuevos_datos)
        else:
            print("📭 No hay documentos nuevos para enviar.")
    except Exception as e:
        print("🚨 Error general:", e)
