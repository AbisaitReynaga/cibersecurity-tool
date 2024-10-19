# web_application/default_data.py

def get_default_data_overview_label():
    return {
        "findings_labels": ["Critical", "High", "Medium", "Low"],
        "findings_data": [10, 20, 30, 40],
        "alive_hosts": 5,
        "services": 10,
        "infrastructure": 3,
        "risks": 2
    }
