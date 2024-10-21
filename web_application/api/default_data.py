# web_application/default_data.py

def get_default_data_overview_label():
    return {
        "alive_hosts": 5,
        "services": 10,
        "infrastructure": 3,
        "risks": 2,
    }

def get_default_data_pie_chart_overview():
    return {
        "findings_labels": ['Vulnerabilities', 'Open Ports', 'Misconfigurations', 'Weak Passwords', 'Others'],
        "findings_data": [10, 20, 30, 25, 15]
    }

def get_findings_list_services():
    return [
        {"icon": "images/icons/ftp.png", "title": "FTP", "number": 12},
        {"icon": "images/icons/http.png", "title": "HTTP", "number": 25},
        {"icon": "images/icons/ssh.png", "title": "SSH", "number": 7},
        {"icon": "images/icons/smtp.png", "title": "SMTP", "number": 5},
    ]

def get_default_report_data():
    return {
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
        'contact_phone': '123-456-7899'
    }