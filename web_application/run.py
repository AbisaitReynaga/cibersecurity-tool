import os
import sys
from flask import Flask
from mail import init_mail  # Import `mail` and initialization function

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

init_mail(app)

from web_application import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
