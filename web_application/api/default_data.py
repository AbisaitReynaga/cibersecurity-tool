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
        {"icon": "icon/ftp.png", "title": "FTP", "number": 12},
        {"icon": "icon/http.png", "title": "HTTP", "number": 25},
        {"icon": "icon/ssh.png", "title": "SSH", "number": 7},
        {"icon": "icon/smtp.png", "title": "SMTP", "number": 5},
    ]

