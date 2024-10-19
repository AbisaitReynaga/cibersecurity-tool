import sys
import os
import subprocess

# Add the parent directory to sys.path so Python can find 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define the path to the installation script
install_script = os.path.join(os.path.dirname(__file__), '..', 'install.sh')

# Run the install.sh script
try:
    print("Running installation script...")
    result = subprocess.run(['bash', install_script], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred while running the installation script: {e}")
    sys.exit(1)

from web_application import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)