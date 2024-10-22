# web_application/app.py
from flask import Flask
from web_application.mail import mail  # Import the mail object

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)  # Initialize the mail object with the app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)