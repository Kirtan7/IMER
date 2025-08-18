#!/bin/bash

# Exit on error
set -e

# Define install path
INSTALL_PATH="/usr/local/bin"
SCRIPT_NAME="imer"
SOURCE_FILE="$(pwd)/imer.py"

# Make sure script is executable
chmod +x "$SOURCE_FILE"

# Remove old command if exists
sudo rm -f "$INSTALL_PATH/$SCRIPT_NAME"

# Create new symlink
sudo ln -s "$SOURCE_FILE" "$INSTALL_PATH/$SCRIPT_NAME"

echo "[+] Installed '$SCRIPT_NAME' globally. Run with: $SCRIPT_NAME"
