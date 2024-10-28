from flask import Flask
from web_application import routes
from web_application.mail import mail  # Import the mail object

app = Flask(__name__)

# Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'a20310068@ceti.mx'
app.config['MAIL_PASSWORD'] = 'Mydear100'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)  # Initialize the mail object with the app

if "mail" in app.extensions:
    print("Mail extension is initialized.")
else:
    print("Mail extension is NOT initialized.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
