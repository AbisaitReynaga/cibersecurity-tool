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
from web_application.utils.data.port_analyzer import PortAnalyzer
from web_application.utils.data.device_analyzer import DeviceAnalyzer
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

    with open('/home/cibersecurity-tool/web_application/data/scanning_data/json_data/scanning.json', 'r') as f:
        data = json.load(f)
    analyzer = PortAnalyzer(data)
    analyzer.process_ports()

    device = DeviceAnalyzer(data)
    device.process_ports()
    device.calculate_risk()

    # Obtener y mostrar el resumen de puertos
    summary_d = device.get_summary()

    # Obtener y mostrar el resumen de puertos
    summary = analyzer.get_summary()
    #print(summary)


    return render_template('reports/report.html', data=data,ports=summary, devices=summary_d)
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
