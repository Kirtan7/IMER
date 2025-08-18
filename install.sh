#!/bin/bash

# Exit immediately if a command fails
set -e

SCRIPT_NAME="imer"
INSTALL_PATH="/usr/local/bin"
SOURCE_FILE="$(pwd)/imer.py"

echo "[+] Starting installation..."

# -------- Install dependencies --------
echo "[+] Installing Python dependencies..."
if command -v pipx >/dev/null 2>&1; then
    echo "[*] pipx found -> using pipx for isolated installation"
    pipx install --force -r requirements.txt
else
    echo "[*] pipx not found -> using python venv"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# -------- Make main script executable --------
chmod +x "$SOURCE_FILE"

# -------- Install global command --------
echo "[+] Creating global command..."
sudo rm -f "$INSTALL_PATH/$SCRIPT_NAME"
sudo ln -s "$SOURCE_FILE" "$INSTALL_PATH/$SCRIPT_NAME"

echo "[✔] Installation complete!"
echo "You can now run the tool globally using: $SCRIPT_NAME"
