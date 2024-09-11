from flask import Flask
from flask_bootstrap import Bootstrap4  # Import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap4(app)

# Import routes after initializing the app to avoid circular imports
from . import routes
