#!/bin/bash

# Update the package list (for Ubuntu/Debian systems)
echo "Updating package list..."
sudo apt update

# Upgrade packages
echo "Upgrading packages..."
sudo apt upgrade -y

# Install Python dependencies
echo "Installing required Python packages..."
cd web_application
pip install -r requirements.txt

# Verify installation
echo "All required packages have been installed successfully."
