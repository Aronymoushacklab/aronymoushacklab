# ░█████╗░██████╗░░█████╗░███╗░░██╗░█████╗░██╗░░░██╗
# ██╔══██╗██╔══██╗██╔══██╗████╗░██║██╔══██╗██║░░░██║
# ███████║██████╔╝██║░░██║██╔██╗██║██║░░██║██║░░░██║
# ██╔══██║██╔═══╝░██║░░██║██║╚████║██║░░██║██║░░░██║
# ██║░░██║██║░░░░░╚█████╔╝██║░╚███║╚█████╔╝╚██████╔╝
# ╚═╝░░╚═╝╚═╝░░░░░░╚════╝░╚═╝░░╚══╝░╚════╝░░╚═════╝░
#          🔍 Google Dorks Scanner by Aronymous Hack Lab

from googlesearch import search
import time
import datetime
import os
# Hijos de Perras recuerden instalar las librerias y modulos. Para que funcione el script. .l.
# 🎯 Configuración genera
# No me hago responsable por el mal uso del script 
# Uso de forma etica
DORKS = [
 

    # 🔐 Archivos confidenciales
    'filetype:env "DB_PASSWORD"',
    'filetype:sql "insert into" (contraseñas)',
    'filetype:log inurl:"password"',
    'filetype:txt inurl:"credentials"',
    'filetype:xml inurl:backup',
    'filetype:json inurl:credentials',
    'filetype:xls site:.gov "password"',

    # 📁 Backups, .env y código fuente
    'intitle:"index of" ".env"',
    'intitle:"index of" "config.php"',
    'intitle:"index of" "db_backup"',
    'filetype:bak inurl:"www"',
    'filetype:inc inurl:"config"',
    'intitle:"index of" site:.git',

    # 🛡 Paneles de administración y acceso
    'inurl:admin intitle:"login"',
    'intitle:"Dashboard" inurl:admin',
    'inurl:login.asp',
    'intitle:"webmin" inurl:10000',
    'intitle:"phpMyAdmin" inurl:"main.php"',
    'site:.edu intitle:"admin login"',

    # 🛰 Cámaras IP públicas
    'intitle:"Live View / - AXIS"',
    'inurl:/view.shtml',
    'intitle:"IPCam" inurl:"/video.cgi"',
    'intitle:"Live View" inurl:viewerframe?mode=',
    'inurl:"/axis-cgi/mjpg"',
    'intitle:"webcamXP 5"',

    # 🌍 Geolocalizado por país
    'site:.cr filetype:xls "contraseña"',
    'site:.mx intitle:"index of" "password"',
    'site:.mil filetype:pdf "ufo"',
    'site:.gov.br filetype:pdf "acceso"',

]
NUM_RESULTS = 5         # Resultados por dork
DELAY = 10              # Tiempo entre dorks (segundos)
RESULT_FILE = f"resultados_dorks_{datetime.date.today()}.txt"

# 🧰 Función para guardar resultados
def guardar_resultados(dork, urls):
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n🔎 Dork: {dork}\n")
        for url in urls:
            f.write(f" - {url}\n")

# 🔎 Función principal de búsqueda
def buscar_dork(dork):
    print(f"\n[+] Analizando: {dork}")
    resultados = []
    try:
        for url in search(dork, num_results=NUM_RESULTS, lang="es"):
            print(f"    • {url}")
            resultados.append(url)
    except Exception as e:
        print(f"[!] Error: {e}")
    return resultados

# 🚀 Función principal
def main():
    os.system("clear")  # Usa 'cls' si estás en Windows
    print("══════════════════════════════════════════════")
    print("   🧠 Aronymous Hack Lab - Google Dorks Tool")
    print("══════════════════════════════════════════════\n")
    
    for dork in DORKS:
        urls = buscar_dork(dork)
        if urls:
            guardar_resultados(dork, urls)
        else:
            print("[!] Sin resultados para este dork.")
        time.sleep(DELAY)

    print(f"\n✅ Escaneo completado. Resultados guardados en: {RESULT_FILE}\n")

if __name__ == "__main__":
    main()
