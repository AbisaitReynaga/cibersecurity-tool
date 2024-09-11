import sys
import os

# Add the parent directory to sys.path so Python can find 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_application import app

if __name__ == '__main__':
    pip install -r requirements.txt
    app.run(host='0.0.0.0', port=5000, debug=True)