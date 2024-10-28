import requests
from bs4 import BeautifulSoup
import json

# Servicios a consultar
servicios = ["python+3.11","apache+2.2.3","rdp+8.0","java+8.0"]
base_url_mitre = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="
base_url_cve_api = "https://cveawg.mitre.org/api/cve/"

# Función para obtener los primeros 15 CVEs de cada servicio
def obtener_cves(servicio):
    url = base_url_mitre + servicio
    response = requests.get(url)
    
    # Verificamos si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al obtener CVEs para {servicio}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Parseamos la tabla de resultados de CVEs en la página web
    cves = []
    
    # Buscamos en la tabla de CVEs los enlaces que contienen los CVEs
    for row in soup.find_all("a", href=True):
        # Detectar las URLs que contienen "CVERecord?id="
        if "CVERecord?id=" in row['href']:  
            cves.append(row.text)  # Extraemos el texto del enlace (el CVE)
            if len(cves) == 15:  # Limitar a los primeros 15 CVEs
                break

    if not cves:
        print(f"No se encontraron CVEs para {servicio}.")
    return cves

# Función para obtener los detalles de cada CVE usando la API
def obtener_detalles_cve(cve_id):
    url = base_url_cve_api + cve_id
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener detalles para {cve_id}")
        return None

# Estructura donde guardaremos todos los CVEs y sus detalles por servicio
cve_data = {}

# Iteramos sobre cada servicio
for servicio in servicios:
    print(f"Consultando CVEs para {servicio}...")
    
    # Obtenemos los primeros 15 CVEs para el servicio
    cves = obtener_cves(servicio)
    print(f"CVEs obtenidos para {servicio}: {cves}")
    
    # Si encontramos CVEs, buscamos sus detalles
    if cves:
        cve_details = {}
        for cve in cves:
            print(f"Consultando detalles de {cve}...")
            details = obtener_detalles_cve(cve)
            if details:
                cve_details[cve] = details
        
        # Guardamos los detalles de los CVEs por servicio
        cve_data[servicio] = cve_details

# Guardamos los datos en un archivo JSON
with open("cves_por_servicio.json", "w") as f:
    json.dump(cve_data, f, indent=4)

print("Proceso completado. Datos almacenados en cves_por_servicio.json.")
