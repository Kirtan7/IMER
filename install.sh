#!/bin/bash

echo "🔍 Detecting system type..."

# === Step 1: Install dependencies ===
if [ -f /etc/debian_version ]; then
    echo "✅ Debian/Kali/Ubuntu detected. Installing via apt where possible..."
    sudo apt update
    sudo apt install -y python3-pil python3-piexif python3-exifread python3-folium python3-colorama python3-pip

    # Pillow is not always available via apt, ensure via pip
    pip3 install --break-system-packages Pillow || pip3 install Pillow
else
    echo "⚠️ Non-Debian system detected. Installing via pip..."
    pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt
fi

# === Step 2: Create global 'imer' command ===
echo "⚙️ Setting up global command 'imer'..."

# Remove old command if exists
if [ -f /usr/local/bin/imer ]; then
    echo "🗑️ Removing old 'imer' command..."
    sudo rm -f /usr/local/bin/imer
fi

# Create new launcher
sudo bash -c "cat > /usr/local/bin/imer" <<EOF
#!/bin/bash
python3 "$(pwd)/imer.py" "\$@"
EOF

sudo chmod +x /usr/local/bin/imer

echo "🎉 Installation complete! You can now run the tool using: imer"
