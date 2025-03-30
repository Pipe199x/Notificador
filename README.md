
# **Automatización de Notificación de Nuevos Documentos**

Este proyecto automatiza la extracción de datos desde un sitio web protegido mediante autenticación, verifica si hay nuevos documentos y, en caso de haberlos, envía un correo electrónico con la información correspondiente.

---

## **Requerimientos**

### **1. Software necesario**
- **Python**: Descargar e instalar la versión más reciente desde [python.org](https://www.python.org/downloads/). Asegúrate de seleccionar la opción **"Add Python to PATH"** durante la instalación.
- **Google Chrome**: Descargar e instalar el navegador Google Chrome desde [google.com/chrome](https://www.google.com/chrome/).
- **ChromeDriver**: Descargar la versión de ChromeDriver que corresponda a tu versión de Google Chrome desde [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads). 
  - Para comprobar tu versión de Google Chrome, abre Chrome y escribe `chrome://settings/help`.

---

### **2. Librerías de Python**
Instala las siguientes librerías usando `pip`:

```bash
pip install selenium
```

---

### **3. Gmail (Contraseña de aplicación)**
- Ve a tu cuenta de Gmail y habilita la autenticación en dos pasos desde la sección de **Seguridad** en [mi cuenta de Google](https://myaccount.google.com/security).
- Una vez activada la autenticación en dos pasos, crea una **contraseña de aplicación**:
  - Ve a la sección **Contraseñas de aplicación**.
  - Selecciona una aplicación personalizada (por ejemplo, "Script Python").
  - Google generará una contraseña especial de 16 caracteres que se usará exclusivamente en este script.

---

### **4. Configuración del archivo de trabajo**
1. **Clonar este proyecto o crear un archivo llamado `notificaciones.py`** y copia el código proporcionado en este README.
2. **Ubicación de ChromeDriver**:
   - Descarga el archivo ChromeDriver y descomprímelo.
   - Coloca el archivo ejecutable en una ubicación conocida (por ejemplo, `C:\ProgramData\chromedriver\`).
   - Actualiza la variable `CHROMEDRIVER_PATH` en el script con la ruta al archivo.

---

### **5. Configuración del script**

Actualiza las siguientes variables en el script con tus credenciales:

```python
REMITENTE_EMAIL = "duqueandres880@gmail.com"  # Tu dirección de correo electrónico
CONTRASENA_EMAIL = "hpze wkob vqtr wsvi"  # Contraseña de aplicación generada
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
DESTINATARIO_EMAIL = "duqueandres880@gmail.com"  # Dirección donde se enviarán los correos
CHROMEDRIVER_PATH = r"C:\ProgramData\chromedriver\chromedriver.exe"  # Ruta al ChromeDriver descargado
LOGIN_URL = "https://fe.libellum.co/"  # URL del sitio web a automatizar
USUARIO = "admin@agenciadeseguros.com.co"  # Usuario para iniciar sesión en el sitio web
CLAVE = "L1b3ll5m*"  # Contraseña para iniciar sesión en el sitio web
```

---

## **Estructura del proyecto**
El proyecto contiene los siguientes elementos:

```
notificaciones/
├── notificaciones.py        # Código principal
├── datos_enviados.json      # Registro de los documentos enviados (se genera automáticamente)
```

---

## **Ejecución del script manual**
Para ejecutar el script manualmente:
1. Abre la consola o terminal y navega al directorio donde está el archivo `notificaciones.py`.
2. Ejecuta el comando:
   ```bash
   python notificaciones.py
   ```

Si todo está configurado correctamente, el script se conectará al sitio web, extraerá los datos de los documentos y enviará un correo con los nuevos documentos si los hay.

---

## **Automatización (Ejecución automática cada 24 horas)**

### **Crear un archivo `.bat`**
1. Crea un archivo con la extensión `.bat` (por ejemplo, `ejecutar_notificaciones.bat`) en el mismo directorio que `notificaciones.py`.
2. Escribe lo siguiente en el archivo `.bat`:
   ```bat
   @echo off
   cd C:\ruta\a\tu\proyecto
   python notificaciones.py
   ```

### **Configurar el Programador de Tareas de Windows**
1. Abre el **Programador de Tareas** de Windows.
2. Haz clic en **Crear Tarea** en el panel de la derecha.
3. Configura los siguientes parámetros:
   - **General**:
     - Nombre de la tarea: "Ejecutar Notificaciones".
     - Selecciona "Ejecutar con los privilegios más altos".
   - **Desencadenadores**:
     - Crea un desencadenador para que la tarea se ejecute "Diariamente" y especifica la hora de inicio.
     - Marca "Repetir cada 1 día".
   - **Acciones**:
     - Crea una acción y selecciona "Iniciar un programa".
     - En el campo de programa, selecciona el archivo `.bat` que creaste.
   - **Condiciones y configuración**:
     - Desmarca "Iniciar la tarea solo si el equipo está con alimentación eléctrica" si es necesario.
4. Guarda la tarea.

---

## **Cómo funciona el código**
1. **Inicio de sesión en el sitio web**:
   - Utiliza Selenium para abrir el navegador Chrome, navegar al sitio web y autenticarse usando las credenciales proporcionadas.

2. **Extracción de datos**:
   - Una vez dentro del sitio, se navega a la sección de documentos y se extraen los datos relevantes de la tabla HTML.

3. **Comparación de datos**:
   - Compara los datos extraídos con un registro local (`datos_enviados.json`).
   - Si hay nuevos datos, genera un mensaje con solo los nuevos documentos.

4. **Envío de correo**:
   - Envía el mensaje con los nuevos documentos al correo especificado utilizando la librería `smtplib`.

5. **Actualización del registro**:
   - Los datos enviados se almacenan en el archivo `datos_enviados.json` para evitar que se vuelvan a enviar en ejecuciones futuras.

---

## **Errores comunes y solución**
1. **El ChromeDriver no coincide con la versión de Chrome**:
   - Verifica que la versión de ChromeDriver sea la misma que la de tu navegador Google Chrome.
2. **No se encuentra el archivo `.bat` en el Programador de Tareas**:
   - Asegúrate de que la ruta del archivo `.bat` sea correcta y accesible.
3. **El correo no se envía**:
   - Revisa que el servidor SMTP y la contraseña de la aplicación estén configurados correctamente.
4. **Errores en la extracción de datos**:
   - Si el sitio web cambia su estructura, actualiza los selectores XPath en el script.

---

¡Con este README, cualquier persona puede implementar y ejecutar el proyecto desde cero de manera sencilla!

## Posibles problemas y soluciones

### 1. Error de compatibilidad entre ChromeDriver y Google Chrome
**Problema:** 
Al ejecutar el script, puedes encontrar un error relacionado con la compatibilidad entre ChromeDriver y la versión de Google Chrome instalada.

**Solución:**
1. Verifica tu versión de Google Chrome:
   - Abre Google Chrome.
   - Ve a `chrome://settings/help`.
   - Anota el número de versión (por ejemplo, 115.0.0.0).

2. Descarga la versión compatible de ChromeDriver:
   - Ve al sitio oficial de ChromeDriver: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads).
   - Descarga la versión que coincide con tu versión de Google Chrome.

3. Reemplaza el archivo `chromedriver.exe` en tu carpeta de proyecto.

---

### 2. Error al instalar Chocolatey
**Problema:** 
Durante la instalación de Chocolatey, el sistema muestra un error indicando que los permisos son insuficientes.

**Solución:**
1. Ejecuta PowerShell como Administrador:
   - Busca `PowerShell` en el menú Inicio, haz clic derecho y selecciona `Ejecutar como Administrador`.

2. Usa el siguiente comando para instalar Chocolatey:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

3. Reinicia PowerShell después de la instalación.

---

### 3. Problemas con la contraseña del correo de Gmail
**Problema:** 
El script muestra un error de autenticación (535: Username and Password not accepted).

**Solución:**
1. Verifica que estés usando una contraseña de aplicación y no tu contraseña de Gmail:
   - Ve a tu cuenta de Google: [https://myaccount.google.com/security](https://myaccount.google.com/security).
   - En la sección "Inicio de sesión y seguridad", activa la verificación en dos pasos.
   - Genera una contraseña de aplicación para este script.

2. Usa esta contraseña de aplicación en lugar de tu contraseña habitual.

---

### 4. Error al programar la tarea en el Programador de Tareas de Windows
**Problema:** 
La tarea programada no se ejecuta correctamente o muestra un error al intentar iniciarla.

**Solución:**
1. Verifica que el archivo `.bat` tenga permisos de ejecución.
2. Asegúrate de que la ruta al archivo `.bat` sea válida.
3. Si la tarea requiere privilegios elevados:
   - Edita la tarea en el Programador de Tareas.
   - Marca la opción `Ejecutar con los privilegios más altos`.

4. Si el problema persiste, prueba ejecutar el archivo `.bat` manualmente para verificar que funcione correctamente.

---

### 5. Error durante la extracción de datos con Selenium
**Problema:** 
El script no encuentra los elementos esperados en la página web.

**Solución:**
1. Verifica que la URL del sitio web sea correcta y accesible.
2. Asegúrate de que la estructura del DOM de la página no haya cambiado.
3. Usa herramientas como `driver.get_screenshot_as_file("debug.png")` para capturar el estado de la página al momento del error.

---

### 6. Error al guardar o enviar correos
**Problema:** 
El script no guarda correctamente los datos o no envía correos.

**Solución:**
1. Asegúrate de que la dirección de destino del correo (`DESTINATARIO_EMAIL`) sea válida.
2. Verifica la conexión a Internet.
3. Revisa los logs del script para obtener más detalles sobre el error.
