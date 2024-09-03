# Import the Flask class from the flask module
from flask import Flask, render_template,request
import sh,json,os
from utils.analyze_data import analyze_data
# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and a function to handle requests to that route
@app.route('/')
def index():
    json_file = 'output.json'  # Adjust the path as needed
    overview_data = analyze_data(json_file)

    return render_template('index.html', 
                           alive_hosts=overview_data['alive_hosts'], 
                           services=overview_data['total_services'], 
                           infrastructure=overview_data['infrastructure'], 
                           risks=overview_data['risks'])

@app.route('/gattering_information')
def gattering_information():
    return render_template('gattering_information.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/test')
def test():
    return render_template('template.html')

@app.route('/report')
def report():
    return render_template('report/report.html')

@app.route('/load_data', methods=['POST'])
def load_data():
    # Reemplaza 'tu_script.sh' con la ruta a tu script bash
    #script_path = '/home/cybersecurity-tool/host_discover_scripts/host_discovery.sh'
    #sh.bash('/home/cybersecurity-tool/host_discover_scripts/host_discovery.sh')
    with open('/home/cybersecurity-tool/results.json', 'r') as f:
        data = json.load(f)
    return render_template('gattering_information.html',data=data)

@app.route('/save_organization_data', methods=['POST'])
def save_data():

    data = {
        "organization_name": request.form.get("organization_name"),
        "network": request.form.get("network"),
        "netmask": request.form.get("netmask"),
        "gateway": request.form.get("gateway"),
        "domain": request.form.get("domain")
    }

    json_file_path = os.path.join("data", "config.json")

    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return render_template('settings.html',data=data)


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
