from flask import Flask
from flask_bootstrap import Bootstrap4  
from flask_mail import Mail

app = Flask(__name__)
bootstrap = Bootstrap4(app)
mail = Mail(app) 

app.config.from_mapping({
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USERNAME': 'a20310068@ceti.mx',
    'MAIL_PASSWORD': 'jcun ndmj sxfn vxiz',
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False
})

mail.init_app(app)

# Import routes after initializing the app to avoid circular imports
from web_application import routes
