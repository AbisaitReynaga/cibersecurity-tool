#!/bin/bash

# Update the package list (for Ubuntu/Debian systems)
echo "Updating package list..."
sudo apt update

# Upgrade packages
echo "Upgrading packages..."
sudo apt upgrade -y

# Create and activate a virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv

# Activate the virtual environment
# It's good to use the full path to ensure it works in non-interactive shells
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Navigate to the web_application directory (if not already in it)
cd web_application || { echo "Directory 'web_application' not found!"; exit 1; }

# Install required packages from requirements.txt
echo "Installing required packages..."
pip install -r requirements.txt

# Additional setup commands can be added here
echo "Installation complete!"

# Run the Flask application
echo "Starting the Flask application..."
python run.py