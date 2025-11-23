@echo off
echo ========================================
echo  Video Streaming RTSP/RTP - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
pip show opencv-python >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)

echo.

REM Check if video file exists
if not exist movie.Mjpeg (
    echo No video file found. Creating test video...
    python VideoConverter.py --test
    if errorlevel 1 (
        echo ERROR: Failed to create test video
        pause
        exit /b 1
    )
    echo Test video created successfully!
    echo.
)

echo ========================================
echo  Starting RTSP Server...
echo ========================================
echo.
echo The server will start on 127.0.0.1:8554
echo Press Ctrl+C to stop the server
echo.
echo After the server starts, run start_client.bat
echo in another terminal to launch the client.
echo.
pause

python Server.py
