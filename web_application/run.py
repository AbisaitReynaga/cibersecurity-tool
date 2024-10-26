import sys
import os
from flask_mail import Mail, Message
from flask import Flask
import subprocess
from dotenv import load_dotenv 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()
app = Flask(__name__)

# Load email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')  # Default to Gmail
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))  # Default to port 587
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']  # Default to True
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't']  # Default to False
app.config['MAIL_DEBUG'] = os.getenv('MAIL_DEBUG', 'false').lower() in ['true', '1', 't']  # Default to False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Load from .env
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Load from .env
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])  # Use MAIL_USERNAME as default
app.config['MAIL_MAX_EMAILS'] = None  # Optional: Set if needed
app.config['MAIL_SUPPRESS_SEND'] = os.getenv('MAIL_SUPPRESS_SEND', 'false').lower() in ['true', '1', 't']  # Default to False
app.config['MAIL_ASCII_ATTACHMENTS'] = False  # Default to False

mail = Mail(app)  # Initialize the mail object with the app

from web_application import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)