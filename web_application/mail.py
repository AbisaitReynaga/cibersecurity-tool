from flask_mail import Mail
from mail_config import MAIL_CONFIG

mail = Mail()  # Create Mail instance without initializing with app yet

def init_mail(app):
    app.config.update(MAIL_CONFIG)
    mail.init_app(app)  # Initialize mail with app config
