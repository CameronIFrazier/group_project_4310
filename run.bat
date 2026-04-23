@echo off
cd /d "%~dp0"
"C:\Users\tater\AppData\Local\Microsoft\WindowsApps\python3.12.exe" deadlock_detector.py
if errorlevel 1 (
    echo.
    echo Error occurred. Check the console above for details.
    pause
)
