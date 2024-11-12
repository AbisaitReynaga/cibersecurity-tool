import json
from collections import Counter, defaultdict

class PortAnalyzer:
    def __init__(self, json_data):
        self.data = json_data
        self.port_counts = defaultdict(lambda: {"count": 0, "names": set()})

    def process_ports(self):
        # Extraer datos de puertos y contar combinaciones
        port_data = []
        for device in self.data:
            for port in device.get("ports", []):
                portid = port.get("portid")
                protocol = port.get("protocol")
                name = port.get("name", "None")  # Usa "None" si el nombre es nulo
                port_data.append((portid, protocol, name))

        # Contar las combinaciones de (portid, protocol, name)
        port_count = Counter(port_data)

        # Agrupar por PortID y Protocol
        for (portid, protocol, name), count in port_count.items():
            key = (portid, protocol)
            self.port_counts[key]["count"] += count
            self.port_counts[key]["names"].add(name if name else "None")

    def get_summary(self):
        # Generar el resumen agrupado
        summary = []
        for (portid, protocol), info in self.port_counts.items():
            names = ', '.join(info["names"]) if info["names"] else "None"
            summary.append({
                "PortID": portid,
                "Protocol": protocol,
                "Names": names,
                "Count": info["count"]
            })
        return summary
