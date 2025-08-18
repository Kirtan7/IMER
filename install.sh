#!/bin/bash

echo "🔍 Detecting system type..."
if [ -f /etc/debian_version ]; then
    echo "✅ Debian/Kali/Ubuntu detected. Installing via apt..."
    sudo apt update
    sudo apt install -y python3-piexif python3-exifread python3-folium python3-colorama
else
    echo "⚠️ Non-Debian system detected. Installing via pip..."
    pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt
fi

echo "🎉 Installation complete! You can now run the tool using: ./imer"
