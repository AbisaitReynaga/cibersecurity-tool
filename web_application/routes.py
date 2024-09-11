from flask import render_template
from . import app  # Import the app instance from the `__init__.py` file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

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

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')
