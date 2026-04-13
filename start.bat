@echo off
title SleepGuard - Starting...
color 0A

echo.
echo  ================================================
echo   SLEEPGUARD - Drowsiness Detection System
echo  ================================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo  [ERROR] Python not found!
    echo  Please install Python from https://python.org
    echo.
    pause
    exit /b
)

echo  [1/3] Python found!

:: Install dependencies silently
echo  [2/3] Installing dependencies...
pip install flask opencv-python mediapipe numpy --quiet --disable-pip-version-check

echo  [3/3] Starting server...
echo.
echo  ================================================
echo   Website: http://localhost:5000
echo   Press Ctrl+C to stop
echo  ================================================
echo.

:: Open browser after 3 seconds
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Start Flask
python app.py

pause