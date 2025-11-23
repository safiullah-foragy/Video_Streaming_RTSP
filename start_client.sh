#!/bin/bash

echo "========================================"
echo " Video Streaming Client - YouTube Style"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "Starting video streaming client..."
echo ""
echo "Make sure the server is running in another terminal!"
echo "(Run ./start_server.sh if you haven't already)"
echo ""
read -p "Press Enter to continue..."

python3 Client.py
