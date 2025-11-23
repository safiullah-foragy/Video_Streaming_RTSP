@echo off
echo ========================================
echo  Video Streaming Client - YouTube Style
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting video streaming client...
echo.
echo Make sure the server is running in another terminal!
echo (Run start_server.bat if you haven't already)
echo.
pause

python Client.py
