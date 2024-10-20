# web_application/default_data.py

def get_default_data_overview_label():
    return {
        "findings_labels": ["Critical", "High", "Medium", "Low"],
        "findings_data": [10, 20, 30, 40],
        "alive_hosts": 5,
        "services": 10,
        "infrastructure": 3,
        "risks": 2,
        
    }

def get_default_data_pie_chart_overview():
    return {
        
    }
    # Dummy data for top findings
    findings_labels = ['Vulnerabilities', 'Open Ports', 'Misconfigurations', 'Weak Passwords', 'Others']
    findings_data = [10, 20, 30, 25, 15]  # Corresponding data for each finding

    findings_list = [
        {"description": "New record, over 90 views.", "time": "10 mins"},
        {"description": "Database error.", "time": "15 mins"},
        {"description": "New record, over 40 users.", "time": "17 mins"},
        {"description": "New comments.", "time": "25 mins"},
        {"description": "Check transactions.", "time": "28 mins"},
        {"description": "CPU overload.", "time": "35 mins"},
        {"description": "New shares.", "time": "39 mins"}
    ]
