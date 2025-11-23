#!/bin/bash

echo "========================================"
echo " Video Streaming RTSP/RTP - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python found!"
echo ""

# Check if dependencies are installed
echo "Checking dependencies..."
if ! pip3 show opencv-python &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
else
    echo "Dependencies already installed."
fi

echo ""

# Check if video file exists
if [ ! -f movie.Mjpeg ]; then
    echo "No video file found. Creating test video..."
    python3 VideoConverter.py --test
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create test video"
        exit 1
    fi
    echo "Test video created successfully!"
    echo ""
fi

echo "========================================"
echo " Starting RTSP Server..."
echo "========================================"
echo ""
echo "The server will start on 127.0.0.1:8554"
echo "Press Ctrl+C to stop the server"
echo ""
echo "After the server starts, run ./start_client.sh"
echo "in another terminal to launch the client."
echo ""
read -p "Press Enter to continue..."

python3 Server.py
