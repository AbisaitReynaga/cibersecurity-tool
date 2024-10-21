from flask import render_template, request, Blueprint, jsonify, redirect, url_for
from web_application import app
import sh, json, os, subprocess
from web_application.api.default_data import get_default_data_overview_label, get_default_data_pie_chart_overview, get_findings_list_services
from web_application.utils.data.analyze_data import analyze_data

overview = Blueprint('overview', __name__)

@app.route('/')
@app.route('/overview')
def index():
    json_file = '/home/cybersecurity-tool/web_application/data/scanning_data.json'  
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

@app.route('/hidden')  # or any other appropriate route name
def hidden():
    return render_template('index.html')

@app.route('/gattering_information')
def gattering_information():
    return render_template('gattering_information.html')

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
    # Placeholder data
    placeholder_data = {
        'title': 'Sample Report Title',
        'description': 'This is a sample report description.',
        'json_data': {"key": "value"},
        'date': '2024-10-20',
        'client_name': 'Client Inc.',
        'executive_summary': 'This is a summary of the executive findings.',
        'scope': ['Scope Item 1', 'Scope Item 2'],
        'methodology': {'Tool 1': 'Description of Tool 1', 'Tool 2': 'Description of Tool 2'},
        'high_risk_vulnerabilities': [
            {'title': 'Vulnerability 1', 'description': 'Description 1', 'impact': 'High', 'recommendation': 'Fix 1'},
        ],
        'medium_risk_vulnerabilities': [
            {'title': 'Vulnerability 2', 'description': 'Description 2', 'impact': 'Medium', 'recommendation': 'Fix 2'},
        ],
        'low_risk_vulnerabilities': [
            {'title': 'Vulnerability 3', 'description': 'Description 3', 'impact': 'Low', 'recommendation': 'Fix 3'},
        ],
        'immediate_actions': ['Immediate action 1'],
        'medium_term_actions': ['Medium-term action 1'],
        'long_term_actions': ['Long-term action 1'],
        'incident_response': 'Incident response details.',
        'conclusion': 'Conclusion of the report.',
        'risk_scale': {'High': 'Severe impact', 'Medium': 'Moderate impact', 'Low': 'Minor impact'},
        'tools_used': ['Tool A', 'Tool B'],
        'contact_name': 'John Doe',
        'contact_position': 'Security Consultant',
        'contact_organization': 'CyberSec Inc.',
        'contact_email': 'john.doe@example.com',
        'contact_phone': '123-456-7890'
    }
    
    return render_template('reports/reports.html', data=placeholder_data)

@app.route('/save_report', methods=['POST'])
def save_report():
    title = request.form.get('title')
    description = request.form.get('description')
    json_data = request.form.get('data')
    
    # Process and save the report data...
    
    return jsonify({'success': True, 'message': 'Report saved successfully!', 'data': json_data})


@app.route('/settings')
def settings():
    return render_template('settings.html')

# Custom routes 
@app.route('/load_data', methods=['POST'])
def load_data():
    config_file_path = '/home/cybersecurity-tool/data/config.json'
    if not os.path.exists(config_file_path):
        return render_template('gattering_information.html', 
                                data={}, 
                                alert_message="Organization configuration is missing. Please configure the organization.")

    script_path = '/home/cybersecurity-tool/host_discover_scripts/host_discovery.sh'
    try:
        subprocess.run(['/bin/bash', script_path], check=True)
    except subprocess.CalledProcessError as e:
        return render_template('gattering_information.html',
                                data={},
                                alert_message=f"Error while executing the script: {e}")

    with open('/home/cybersecurity-tool/data/scanning_data.json', 'r') as f:
        data = json.load(f)
    return render_template('gattering_information.html',data=data)

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

    json_file_path = os.path.join("data", "config.json")

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return render_template('settings.html',data=data)

def netmask_to_cidr(netmask):
    # Convierte la máscara de red en una lista de octetos
    octets = netmask.split('.')
    
    # Convierte cada octeto a binario, cuenta los bits '1'
    cidr = sum([bin(int(octet)).count('1') for octet in octets])
    
    return cidr