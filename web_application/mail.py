from flask_mail import Mail
from mail_config import MAIL_CONFIG

mail = Mail()  # Create the Mail instance without initializing it yet

def init_mail(app):
    """Initialize Flask-Mail with the provided app."""
    app.config.update(MAIL_CONFIG)
    mail.init_app(app)
