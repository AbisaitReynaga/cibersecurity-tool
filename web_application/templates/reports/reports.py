# web_application/reports.py

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from weasyprint import HTML
from werkzeug.utils import secure_filename

reports_blueprint = Blueprint('reports', __name__)
mail = Mail()

@reports_blueprint.route('/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        # Get data from the form
        title = request.form.get('title')
        description = request.form.get('description')
        additional_data = request.form.get('data')
        
        # Load and prepare JSON data
        try:
            json_data = json.loads(additional_data)
        except json.JSONDecodeError:
            flash("Invalid JSON data.", "error")
            return redirect(url_for('reports.reports'))

        # Fill the template with JSON data and other details
        rendered_template = render_template(
            'report/report_template.html',
            title=title,
            description=description,
            data=json_data
        )

        # Generate PDF
        pdf_file_path = 'generated_report.pdf'
        HTML(string=rendered_template).write_pdf(pdf_file_path)

        # Send email with PDF attachment
        send_email_with_attachment(pdf_file_path)

        flash("Report generated and emailed successfully.", "success")
        return redirect(url_for('reports.reports'))

    return render_template('reports/reports.html')

def send_email_with_attachment(pdf_file_path):
    msg = Message("Your Report", recipients=["recipient@example.com"])  # Replace with recipient's email
    msg.body = "Please find the attached report."
    with open(pdf_file_path, 'rb') as pdf:
        msg.attach(secure_filename(pdf_file_path), 'application/pdf', pdf.read())
    mail.send(msg)


