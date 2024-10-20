import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from weasyprint import HTML
from werkzeug.utils import secure_filename

reports_blueprint = Blueprint('reports', __name__)
mail = Mail()

# File path for storing the JSON report data
JSON_FILE_PATH = 'data/report_data.json'

@reports_blueprint.route('/reports', methods=['GET', 'POST'])
def reports():
    # Load existing report data from the JSON file
    report_data = load_json_data(JSON_FILE_PATH)

    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        description = request.form.get('description')
        additional_data = request.form.get('data')
        
        # Validate and update the JSON data
        try:
            json_data = json.loads(additional_data)
            report_data['title'] = title
            report_data['description'] = description
            report_data['json_data'] = json_data
            
            # Save updated report data to the file
            save_json_data(report_data, JSON_FILE_PATH)

            flash("Report updated successfully!", "success")
        except json.JSONDecodeError:
            flash("Invalid JSON data.", "error")
            return redirect(url_for('reports.reports'))

    # Pass the JavaScript as a string to the template
    preview_script = '''
    function updatePreview() {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const data = document.getElementById('data').value;

        document.getElementById('previewTitle').innerText = title || 'Your report title will appear here';
        document.getElementById('previewDescription').innerText = description || 'Your report description will appear here';
        document.getElementById('previewData').innerText = data || 'Your additional data will appear here in JSON format';
    }
    '''
    
    return render_template('reports/reports.html', report_data=report_data, preview_script=preview_script)

def load_json_data(filepath):
    """ Load JSON data from a file """
    if os.path.exists(filepath):
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    return {}

def save_json_data(data, filepath):
    """ Save JSON data to a file """
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def send_email_with_attachment(pdf_file_path):
    msg = Message("Your Report", recipients=["recipient@example.com"])  # Replace with recipient's email
    msg.body = "Please find the attached report."
    with open(pdf_file_path, 'rb') as pdf:
        msg.attach(secure_filename(pdf_file_path), 'application/pdf', pdf.read())
    mail.send(msg)
