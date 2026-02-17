@echo off
echo ================================================
echo   TalkMate AI - Setup Script
echo ================================================
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Create a .env file with your OpenAI API key:
echo      OPENAI_API_KEY=your_key_here
echo.
echo   2. Run the application:
echo      venv\Scripts\activate
echo      python talkmate.py
echo.
echo ================================================

pause
