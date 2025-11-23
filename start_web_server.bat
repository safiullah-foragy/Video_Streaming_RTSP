@echo off
echo ========================================
echo  Web-Based Video Streaming Server
echo ========================================
echo.

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if Flask is installed
py -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    py -m pip install Flask opencv-python Pillow numpy
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
) else (
    echo Dependencies already installed.
    echo.
)

REM Check if videos folder exists
if not exist "assets\videos" (
    echo Creating assets\videos folder...
    mkdir assets\videos
    echo.
)

echo ========================================
echo  Starting Web Server...
echo ========================================
echo.
echo Server will start on: http://localhost:5000
echo.
echo To access from other devices on your network:
echo 1. Find your IP address: ipconfig
echo 2. Open browser on other device
echo 3. Go to: http://YOUR_IP:5000
echo.
echo Add videos to: assets\videos\ folder
echo Supported formats: MP4, AVI, MOV, MKV, WebM
echo.
echo Press Ctrl+C to stop the server
echo.
pause

py web_server.py
