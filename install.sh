#!/bin/bash

# Update the package list (for Ubuntu/Debian systems)
echo "Updating package list..."
sudo apt update

# Upgrade packages
echo "Upgrading packages..."
sudo apt upgrade -y

# Activate the virtual environment in the main directory
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Change to the web_application directory
cd web_application || { echo "Directory 'web_application' not found!"; exit 1; }

# Install required packages from requirements.txt
echo "Installing required packages..."

#Uncomment when adding dependencies
pip freeze > requirements.txt

pip install -r requirements.txt

# Additional setup commands can be added here
echo "Installation complete!"

# Run the Flask application
echo "Starting the Flask application..."
python run.py
