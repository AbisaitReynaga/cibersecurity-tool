# Import the Flask class from the flask module
from flask import Flask, render_template

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and a function to handle requests to that route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gattering_information')
def gattering_information():
    return render_template('gattering_information.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/test')
def test():
    return render_template('template.html')

@app.route('/scan')
def scan():
    # Ejecutar el comando nmap
    result = subprocess.run(['nmap', '-sn', '192.168.10.0/24'], capture_output=True, text=True)
    output = result.stdout

    # Parsear el resultado de nmap
    hosts = []
    current_host = {}
    for line in output.split('\n'):
        ip_match = re.search(r'Nmap scan report for (.+)', line)
        mac_match = re.search(r'MAC Address: (.+) \((.+)\)', line)
        if ip_match:
            if current_host:
                hosts.append(current_host)
                current_host = {}
            current_host['ip'] = ip_match.group(1)
        if mac_match:
            current_host['mac'] = mac_match.group(1)
            current_host['vendor'] = mac_match.group(2)

    if current_host:
        hosts.append(current_host)

    return jsonify(hosts)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)