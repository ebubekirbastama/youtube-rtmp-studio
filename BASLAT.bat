@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt
if errorlevel 1 (echo Paketler kurulamadi. Python 3.10+ kontrol edin. & pause & exit /b 1)
py youtube_rtmp_studio.py
pause
