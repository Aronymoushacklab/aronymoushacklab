import requests
from bs4 import BeautifulSoup
import csv
import time

# Configuración - CAMBIA ESTO
aronymous_hack_lab_iplogger_stats_url = "https://iplogger.com/aronymous"
aronymous_hack_lab_phpsessid_cookie = "tu_php_sess_id_aqui"
aronymous_hack_lab_ipinfo_token = "tu_token_ipinfo_aqui"  # opcional, pero recomendado para evitar límites

aronymous_hack_lab_session = requests.Session()

# Inyectamos la cookie PHPSESSID para autenticarnos
aronymous_hack_lab_session.cookies.set("PHPSESSID", aronymous_hack_lab_phpsessid_cookie, domain="iplogger.org")

def aronymous_hack_lab_obtener_datos_iplogger(url):
    print(f"Accediendo a: {url}")
    r = aronymous_hack_lab_session.get(url)
    if r.status_code != 200:
        print(f"Error al acceder: Status {r.status_code}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    # Buscamos la tabla de IPs
    tabla = soup.find("table")
    if not tabla:
        print("No se encontró tabla con datos.")
        return []

    filas = tabla.find_all("tr")
    datos = []

    # Se asume que la primer fila es encabezado
    for fila in filas[1:]:
        columnas = fila.find_all("td")
        if len(columnas) < 4:
            continue

        ip = columnas[1].text.strip()
        fecha = columnas[0].text.strip()
        user_agent = columnas[3].text.strip()

        datos.append({
            "ip": ip,
            "fecha": fecha,
            "user_agent": user_agent
        })
    return datos

def aronymous_hack_lab_geolocalizar_ip(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        if aronymous_hack_lab_ipinfo_token:
            url += f"?token={aronymous_hack_lab_ipinfo_token}"

        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()

        return {
            "ip": ip,
            "ciudad": data.get("city", "N/A"),
            "region": data.get("region", "N/A"),
            "pais": data.get("country", "N/A"),
            "loc": data.get("loc", "N/A"),
            "org": data.get("org", "N/A")
        }
    except Exception as e:
        return {"ip": ip, "error": str(e)}

def aronymous_hack_lab_guardar_csv(datos, nombre_archivo="iplogger_geolocalizacion.csv"):
    keys = datos[0].keys()
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(datos)
    print(f"Datos guardados en {nombre_archivo}")

def aronymous_hack_lab_main():
    datos_iplogger = aronymous_hack_lab_obtener_datos_iplogger(aronymous_hack_lab_iplogger_stats_url)
    if not datos_iplogger:
        print("No se obtuvieron datos de IPLogger.")
        return

    print(f"Se obtuvieron {len(datos_iplogger)} registros de IPLogger.")
    resultados = []

    for i, entrada in enumerate(datos_iplogger, start=1):
        print(f"Geolocalizando IP {i}/{len(datos_iplogger)}: {entrada['ip']}")
        geo = aronymous_hack_lab_geolocalizar_ip(entrada["ip"])
        combinado = {**entrada, **geo}
        resultados.append(combinado)
        time.sleep(1)  # Para no saturar la API de ipinfo.io

    aronymous_hack_lab_guardar_csv(resultados)

if __name__ == "__main__":
    aronymous_hack_lab_main()
