import os
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

reports_blueprint = Blueprint('reports', __name__)
mail = Mail()

JSON_FILE_PATH = 'data/report_data.json'

@reports_blueprint.route('/reports', methods=['GET', 'POST'])
def reports():
    # Load existing report data from the JSON file
    report_data = load_json_data(JSON_FILE_PATH)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        additional_data = request.form.get('data')
        
        try:
            json_data = json.loads(additional_data)
            report_data['title'] = title
            report_data['description'] = description
            report_data['json_data'] = json_data
            
            save_json_data(report_data, JSON_FILE_PATH)
            flash("Report updated successfully!", "success")
        except json.JSONDecodeError:
            flash("Invalid JSON data.", "error")
            return redirect(url_for('reports.reports'))

    # Render the template with existing report data
    return render_template('reports/reports.html', report_data=report_data)

def load_json_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    return {}

def save_json_data(data, filepath):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def send_email_with_attachment(pdf_file_path):
    msg = Message("Your Report", recipients=["recipient@example.com"])  # Replace with recipient's email
    msg.body = "Please find the attached report."
    with open(pdf_file_path, 'rb') as pdf:
        msg.attach(secure_filename(pdf_file_path), 'application/pdf', pdf.read())
    mail.send(msg)
