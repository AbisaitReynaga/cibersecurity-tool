import xml.etree.ElementTree as ET
import json

file_xml="/home/cibersecurity-tool/web_application/data/scanning_data/data_raw/scanning.xml"
output_file="/home/cibersecurity-tool/web_application/data/scanning_data/json_data/scanning.json"

tree = ET.parse(file_xml)
root = tree.getroot()
hosts_info = []

# Obtener dirección IP, MAC, y detalles de puertos
for host in root.findall("./host"):
    host_info = {"ip": None, "mac": None, "vendor": None, "ports": []}

    # Extraer IP, MAC y Vendor
    for address in host.findall("./address"):
        if address.attrib.get("addrtype") == "ipv4":
            host_info["ip"] = address.attrib.get("addr")
        elif address.get("addrtype") == "mac":
            host_info["mac"] = address.get("addr")
            host_info["vendor"] = address.get("vendor")
    
    # Extraer información de cada puerto
    for port in host.findall("./ports/port"):
        port_info = {
            "portid": port.attrib.get("portid"),
            "protocol": port.attrib.get("protocol"),
            "state": None,
            "service": None,
            "name": None,
            "ssl": None,
            "product": None,
            "version": None,
            "ostype": None,
            "extrainfo": None
        }
        
        # Estado del puerto
        state = port.find("state")
        if state is not None:
            port_info["state"] = state.attrib.get("state")
        
        # Información del servicio
        service = port.find("service")
        if service is not None:
            port_info["service"] = service.attrib.get("name")
            port_info["name"] = service.attrib.get("product")
            port_info["version"] = service.attrib.get("version")
            port_info["ostype"] = service.attrib.get("ostype")
            port_info["extrainfo"] = service.attrib.get("extrainfo")
            port_info["ssl"] = service.attrib.get("tunnel") == "ssl"
        
        # Agregar información del puerto al host
        host_info["ports"].append(port_info)
    
    # Agregar información del host a la lista principal
    hosts_info.append(host_info)

# Guardar en archivo JSON
with open(output_file, 'w') as file:
    json.dump(hosts_info, file, indent=4)
