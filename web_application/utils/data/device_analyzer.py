import json
from collections import Counter, defaultdict

class DeviceAnalyzer:
    def __init__(self, json_data):
        self.data = json_data
        self.port_counts = defaultdict(lambda: {"count": 0, "ssl_count": 0, "names": set(), "ports": set(), "risk": None})

    def process_ports(self):
        # Extraer datos de puertos y contar combinaciones
        for device in self.data:
            ip = device.get("ip")
            mac = device.get("mac")
            ports = device.get("ports", [])

            for port in ports:
                portid = port.get("portid")
                protocol = port.get("protocol")
                name = port.get("name", "None")  # Usa "None" si el nombre es nulo
                ssl = port.get("ssl", False)
                
                # Contar el puerto y las combinaciones (portid, protocol, name)
                key = (ip, mac)  # Agrupar por IP y MAC
                self.port_counts[key]["count"] += 1
                self.port_counts[key]["ports"].add(portid)
                self.port_counts[key]["names"].add(name)
                
                # Contar los puertos con SSL
                if ssl or protocol == 'tcp' and portid == "22":
                    self.port_counts[key]["ssl_count"] += 1

    def calculate_risk(self):
        # Calcular el riesgo basado en los puertos con SSL
        for key, info in self.port_counts.items():
            total_ports = info["count"]
            ssl_ports = info["ssl_count"]
            risk = "Bajo"  # Por defecto, si todos los puertos son con SSL o seguro

            if ssl_ports == total_ports:
                risk = "Bajo"
            elif ssl_ports > total_ports / 2:
                risk = "Medio"
            elif ssl_ports < total_ports / 2:
                risk = "Alto"
            
            # Puerto 22 siempre se considera seguro
            if 'ssh' in info["names"]:
                risk = "Bajo"
            
            info["risk"] = risk

    def get_summary(self):
        # Generar el resumen agrupado
        summary = []
        for key, info in self.port_counts.items():
            ip, mac = key
            ports = ', '.join(str(port) for port in info["ports"])  # Convertir puertos a cadenas
            names = ', '.join(str(name) for name in info["names"]) or "None"
            risk = info["risk"]

            summary.append({
                "ip": ip,
                "mac": mac,
                "qty_port": info["count"],
                "ports": ports,
                "names": names,
                "risk": risk
            })
        return summary
