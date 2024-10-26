import os
from dotenv import load_dotenv

load_dotenv()

MAIL_CONFIG = {
    'MAIL_SERVER': os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    'MAIL_PORT': int(os.getenv('MAIL_PORT', 465)),
    'MAIL_USE_TLS': os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't'],
    'MAIL_USE_SSL': os.getenv('MAIL_USE_SSL', 'false').lower() in ['true', '1', 't'],
    'MAIL_DEBUG': os.getenv('MAIL_DEBUG', 'false').lower() in ['true', '1', 't'],
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
    'MAIL_DEFAULT_SENDER': os.getenv('MAIL_DEFAULT_SENDER'),
    'MAIL_SUPPRESS_SEND': os.getenv('MAIL_SUPPRESS_SEND', 'false').lower() in ['true', '1', 't'],
    'MAIL_ASCII_ATTACHMENTS': False
}