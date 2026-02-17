@echo off
cd /d "%~dp0"
echo Starting TalkMate AI...
echo.

if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python talkmate.py

pause
