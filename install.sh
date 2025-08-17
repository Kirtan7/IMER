#!/bin/bash

# Installer for IMER

echo "📦 Installing IMER (Image Metadata Extractor & Remover)..."

# Install dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Install Python libraries
pip3 install --upgrade pip
pip3 install pillow exifread piexif folium colorama

# Copy script to /usr/local/bin
sudo cp imer.py /usr/local/bin/imer
sudo chmod +x /usr/local/bin/imer

echo "✅ Installation complete!"
echo "Now you can run the tool by typing: imer"

