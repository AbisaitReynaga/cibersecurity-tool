import json

def analyze_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    alive_hosts = len(data)  # Total number of hosts
    total_services = sum(len(host['Services']) for host in data)  # Total number of services
    infrastructure = len(set(host['MAC'] for host in data if 'MAC' in host))  # Unique MAC addresses
    risks = sum(1 for host in data if 'OS' in host)  # Hosts with OS identified

    return {
        'alive_hosts': alive_hosts,
        'total_services': total_services,
        'infrastructure': infrastructure,
        'risks': risks
    }

if __name__ == "__main__":
    json_file = '../output.json'  # Adjust the path as needed
    overview_data = analyze_data(json_file)
    print(overview_data)  # For debugging
