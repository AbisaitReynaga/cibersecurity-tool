#from flask import Blueprint, render_template, request
#import sh, json, os, subprocess,csv
#from collections import Counter, defaultdict
#from web_application import app

from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from web_application import app, mail
from flask_mail import Message
from weasyprint import HTML
from web_application.api.default_data import get_default_data_overview_label, get_default_data_pie_chart_overview, get_default_report_data, get_findings_list_services
from web_application.utils.data.analyze_data import analyze_data
import sh, json, os, subprocess,csv
from collections import Counter, defaultdict

overview = Blueprint('overview', __name__)

@app.route('/')
@app.route('/overview')
def index():
    json_file = '/home/cibersecurity-tool/web_application/data/scanning_data.json'
    # overview_data = analyze_data(json_file)
    overview_data = get_default_data_overview_label()
    findings_services = get_findings_list_services()

    return render_template(
        'overview/overview.html',
        alive_hosts=overview_data['alive_hosts'],
        services=overview_data['services'],
        infrastructure=overview_data['infrastructure'],
        risks=overview_data['risks'],
        findings_services=findings_services
    )

@app.route('/overview/findings')
def get_findings_data():
    findings_data = get_default_data_pie_chart_overview()
    return jsonify(findings_data)

@app.route('/reported')
def get_reported():
    return render_template('/reports/create_report.html')


@app.route('/hidden')  # or any other appropriate route name
def hidden():
    return render_template('index.html')
@app.route('/gattering_information')
def gattering_information():
    return render_template('/scanning/gattering_information.html')
@app.route('/view_cves', methods=['POST'])
def view_cve():
    config_file_path = '/home/cibersecurity-tool/web_application/data/cve_vulnerabilities.json'
    if not os.path.exists(config_file_path):
        return render_template('gattering_information.html',
                               data={},
                               alert_message="CVE file is missing. Please perform a scanning.")
    with open(config_file_path, 'r') as f:
        data = json.load(f)
    return render_template('/scanning/view_cve.html', data=data)

@app.route('/view_scanning', methods=['POST'])
def view_scanning():
    config_file_path = '/home/cibersecurity-tool/web_application/data/scanning_data.json'
    if not os.path.exists(config_file_path):
        return render_template('gattering_information.html',
                               data={},
                               alert_message="Host data file is missing. Please perform a scanning.")
    with open(config_file_path, 'r') as f:
        data = json.load(f)
    return render_template('/scanning/view_scanning.html', data=data)


@app.route('/traffic_analyze')
def traffic_analyze():
    return render_template('traffic_analyze.html')

@app.route('/domain_analyze')
def domain_analyze():
    return render_template('domain_analyze.html')

@app.route('/risk_information')
def risk_information():
    return render_template('risk_information.html')

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    # Load default report data from the default_data.py
    placeholder_data = get_default_report_data()

    return render_template('reports/reports.html', data=placeholder_data)

@app.route('/save_report', methods=['POST'])
def save_report():
    title       = request.form.get('title')
    description = request.form.get('description')
    email       = request.form.get('email')

    # Add the risk_scale key to the data dictionary
    data = {
        'title': title,
        'description': description,
        'risk_scale': {
            'Low': 'Minimal risk identified',
            'Medium': 'Moderate risk identified',
            'High': 'Significant risk identified'
        }
    }

    # Render the report template with the data
    rendered_html = render_template('reports/report_template.html', data=data)

    # Define the path for the PDF output
    output_folder = os.path.join(os.getcwd(), 'web_application', 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_path = os.path.join(output_folder, f"{title}_report.pdf")
    HTML(string=rendered_html).write_pdf(pdf_path)

    msg = Message(
        subject="Report",
        sender='a20310068@ceti.mx',
        recipients=[request.form.get('email')],
        body='Hello, this is a test email.'
    )
    msg.body = "This is the email body"

    with app.open_resource(pdf_path) as pdf:
        msg.attach(f'{title}_report.pdf', 'application/pdf', pdf.read())

    # Return success message
    try:
        mail.send(msg)
        return jsonify({'success': True, 'message': f'Report saved as {pdf_path} and emailed to {email}!'})
    except Exception as e:
        print(f"Failed to send email: {e}")
        return jsonify({'success': False, 'message': 'Error sending email'}), 500

@app.route('/settings')
def settings():
    return render_template('settings.html')

# Custom routes
@app.route('/load_data', methods=['POST'])
def load_data():
    config_file_path = '/home/cibersecurity-tool/web_application/data/config.json'
    if not os.path.exists(config_file_path):
        return render_template(
            'gattering_information.html',
            data={},
            alert_message="Organization configuration is missing. Please configure the organization."
        )

    scanning_path = '/home/cibersecurity-tool/web_application/scripts/host_discover_scripts/host_discovery.sh'
    search_cve_path = '/home/cibersecurity-tool/web_application/scripts/search_cve.sh'

    try:
        subprocess.run(['/bin/bash', scanning_path], check=True)
        subprocess.run(['/bin/bash', search_cve_path], check=True)
    except subprocess.CalledProcessError as e:
        return render_template(
            'gattering_information.html',
            data={},
            alert_message=f"Error while executing the script: {e}"
        )

    with open('/home/cibersecurity-tool/web_application/data/scanning_data.json', 'r') as f:
        data = json.load(f)

    return render_template('gattering_information.html', data=data)



@app.route('/save_organization_data', methods=['POST'])
def save_data():

    netmask = request.form.get("netmask")

    # Convertir la máscara de red a CIDR
    cidr = netmask_to_cidr(netmask)

    data = {
        "organization_name": request.form.get("organization_name"),
        "network": request.form.get("network"),
        "netmask": cidr,
        "gateway": request.form.get("gateway"),
        "domain": request.form.get("domain")
    }

    json_file_path = os.path.join("/home/cibersecurity-tool/web_application/data", "config.json")

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return render_template('settings.html',data=data)

def netmask_to_cidr(netmask):
    # Convierte la máscara de red en una lista de octetos
    octets = netmask.split('.')

    # Convierte cada octeto a binario, cuenta los bits '1'
    cidr = sum([bin(int(octet)).count('1') for octet in octets])

    return cidr

@app.route('/view_report', methods=['POST'])
def view_report():
    # Leer archivo JSON
    with open('/home/cibersecurity-tool/web_application/data/scanning_data.json', 'r') as json_file:
        data_json = json.load(json_file)

    # Leer archivo CSV
    puertos_info = {}
    with open('/home/cibersecurity-tool/web_application/data/ports.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            puerto_protocolo = row['Puerto'].strip()  # Asegurarse de que no haya espacios
            puertos_info[puerto_protocolo] = {
                'Descripcion': row['Descripcion'],
                'Recomendacion': row['Recomendacion']
            }

    # Procesar datos de servicios por host
    hosts_info = defaultdict(list)
    os_counter = Counter()
    for record in data_json:
        host = record['Host']
        os_name = record.get('OS', 'Desconocido')  # Obtener el sistema operativo, o 'Desconocido' si no existe
        os_counter[os_name] += 1  # Contar la ocurrencia del sistema operativo
        for service in record['Services']:
            puerto_protocolo = service['Port']
            protocolo = service['Protocol']
            hosts_info[host].append((puerto_protocolo, protocolo))

    # Contar ocurrencias de cada servicio
    servicios_contador = Counter((puerto_protocolo, protocolo) for host, servicios in hosts_info.items() for puerto_protocolo, protocolo in servicios)

    # Generar el informe en HTML
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Infraestructura</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: 'Arial', sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }
            h1, h2 { color: #2c3e50; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; background: white; }
            th, td { border: 1px solid #bdc3c7; padding: 8px; text-align: left; }
            th { background-color: #2c3e50; color: white; }
            tr:nth-child(even) { background: #ecf0f1; }
            tr:hover { background: #dfe6e9; }
            .chart-container { width: 100%; height: 400px; margin-bottom: 30px; }
            footer { margin-top: 20px; font-size: 12px; color: #7f8c8d; }
        </style>
    </head>
    <body>
	<a href="/reported">
        <h1>Reporte de Infraestructura</h1>
	</a>
        <h2>Resumen General</h2>
        <p>Este informe proporciona un analisis detallado de los servicios detectados en la infraestructura de la red. Incluye informacion sobre los puertos abiertos, servicios asociados y recomendaciones para mejorar la seguridad de la red.</p>
        
        <h2>Servicios Utilizados</h2>
        <table>
            <tr>
                <th>Servicio</th>
                <th>Puerto</th>
                <th># Ocurrencia</th>
                <th>Descripcion</th>
            </tr>
    """

    # Agregar datos a la seccion de Servicios utilizados
    for (puerto_protocolo, servicio), cantidad in servicios_contador.items():
        descripcion = puertos_info.get(puerto_protocolo, {}).get('Descripcion', 'Utilizado por posible dispositivo IoT')
        html_content += f"""
            <tr>
                <td>{servicio}</td>
                <td>{puerto_protocolo}</td>
                <td>{cantidad}</td>
                <td>{descripcion}</td>
            </tr>
        """

    html_content += """
        </table>
        
        <h2>Servicios por Host</h2>
        <table>
            <tr>
                <th>Host</th>
                <th>Cantidad de Servicios</th>
                <th>Puertos</th>
            </tr>
    """

    # Agregar datos a la seccion de Servicios por Host
    for host, servicios in hosts_info.items():
        cantidad_servicios = len(servicios)
        puertos = ", ".join(f"{p}/{s}" for p, s in servicios)
        html_content += f"""
            <tr>
                <td>{host}</td>
                <td>{cantidad_servicios}</td>
                <td>{puertos}</td>
            </tr>
        """

    html_content += """
        </table>
        
        <h2>Recomendacion de Servicios</h2>
        <table>
            <tr>
                <th>Puerto</th>
                <th>Servicio</th>
                <th>Descripcion</th>
                <th>Recomendacion</th>
            </tr>
    """

    # Agregar datos a la seccion de Recomendacion de Servicios
    for (puerto_protocolo, servicio), _ in servicios_contador.items():
        descripcion = puertos_info.get(puerto_protocolo, {}).get('Descripcion', 'Utilizado por posible dispositivo IoT')
        recomendacion = puertos_info.get(puerto_protocolo, {}).get('Recomendacion', 'Revisar fisicamente el dispositivo')
        html_content += f"""
            <tr>
                <td>{puerto_protocolo}</td>
                <td>{servicio}</td>
                <td>{descripcion}</td>
                <td>{recomendacion}</td>
            </tr>
        """

    html_content += """
        </table>
        
        <h2>Graficos de Servicios</h2>
        <div class="chart-container">
            <canvas id="servicesChart"></canvas>
        </div>
        
        <h2>Grafico de Sistemas Operativos</h2>
        <div class="chart-container">
            <canvas id="osChart"></canvas>
        </div>

        <h2>Recomendaciones de Seguridad</h2>
        <p>A continuacion se presentan algunas recomendaciones para mejorar la seguridad de la infraestructura de la red:</p>
        <ol>
            <li><strong>Monitoreo de Servicios:</strong> Implementar soluciones de deteccion de intrusos (IDS) para identificar actividades sospechosas.</li>
            <li><strong>Actualizacion de Software:</strong> Mantener todos los servicios y aplicaciones actualizados con los ultimos parches de seguridad.</li>
            <li><strong>Control de Acceso:</strong> Limitar el acceso a los servicios criticos solo a usuarios y dispositivos autorizados.</li>
            <li><strong>Desactivacion de Servicios Innecesarios:</strong> Revisar la lista de servicios activos y desactivar aquellos que no sean necesarios.</li>
            <li><strong>Configuracion de Firewalls:</strong> Restringir el trafico solo a los puertos y protocolos necesarios.</li>
            <li><strong>Cifrado de Datos:</strong> Implementar cifrado para la transmision de datos sensibles utilizando protocolos seguros.</li>
            <li><strong>Pruebas de Seguridad:</strong> Programar pruebas de penetracion y auditorias de seguridad regularmente.</li>
            <li><strong>Documentacion y Procedimientos:</strong> Mantener una documentacion clara y actualizada sobre la configuracion de la red.</li>
        </ol>

        <script>
            const ctx = document.getElementById('servicesChart').getContext('2d');
            const labels = {labels};
            const data = {
                labels: labels,
                datasets: [{
                    label: 'Ocurrencias de Servicios',
                    data: {data},
                    backgroundColor: 'rgba(44, 62, 80, 0.5)',
                    borderColor: 'rgba(44, 62, 80, 1)',
                    borderWidth: 1
                }]
            };
            const config = {
                type: 'bar',
                data: data,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            };
            const servicesChart = new Chart(ctx, config);

            // Grafico de sistemas operativos
            const osCtx = document.getElementById('osChart').getContext('2d');
            const osLabels = {osLabels};
            const osData = {
                labels: osLabels,
                datasets: [{
                    label: 'Cantidad de Hosts por Sistema Operativo',
                    data: {osData},
                    backgroundColor: 'rgba(231, 76, 60, 0.5)',
                    borderColor: 'rgba(231, 76, 60, 1)',
                    borderWidth: 1
                }]
            };
            const osConfig = {
                type: 'bar',
                data: osData,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            };
            const osChart = new Chart(osCtx, osConfig);
        </script>

        <footer>
        </footer>
    </body>
    </html>
    """

    # Preparar los datos para la grafica de servicios
    labels = []
    data = []
    for (puerto_protocolo, servicio), cantidad in servicios_contador.items():
        labels.append(f"{servicio} ({puerto_protocolo})")
        data.append(cantidad)

    # Preparar los datos para la grafica de sistemas operativos
    os_labels = list(os_counter.keys())
    os_data = list(os_counter.values())

    # Convertir listas a cadenas para insertar en HTML
    labels_str = json.dumps(labels)  # Convertir a JSON para que sea un array en JavaScript
    data_str = json.dumps(data)  # Convertir a JSON para que sea un array en JavaScript
    os_labels_str = json.dumps(os_labels)  # Convertir a JSON para que sea un array en JavaScript
    os_data_str = json.dumps(os_data)  # Convertir a JSON para que sea un array en JavaScript

    # Guardar el contenido en un archivo HTML
    with open('/home/cibersecurity-tool/web_application/templates/reports/report.html', 'w') as html_file:
        html_file.write(html_content.replace('{labels}', labels_str).replace('{data}', data_str)
                        .replace('{osLabels}', os_labels_str).replace('{osData}', os_data_str))

    return render_template("reports/report.html")
