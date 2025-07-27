@echo off
echo Starting Huawei LTE Router AI Automation Agent...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    echo Virtual environment created successfully.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist ".venv\Lib\site-packages\requests" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed successfully.
    echo.
)

REM Check if .env file exists
if not exist ".env" (
    echo Environment file not found. Creating from template...
    copy env_example.txt .env
    echo Please edit .env file with your router credentials.
    echo.
)

echo Starting application...
echo.
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
) 