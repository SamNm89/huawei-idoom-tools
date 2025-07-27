Write-Host "Starting Huawei LTE Router AI Automation Agent..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Virtual environment created successfully." -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# Check if requirements are installed
if (-not (Test-Path ".venv\Lib\site-packages\requests")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Dependencies installed successfully." -ForegroundColor Green
    Write-Host ""
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Environment file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item env_example.txt .env
    Write-Host "Please edit .env file with your router credentials." -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "Starting application..." -ForegroundColor Green
Write-Host ""
python main.py

# Keep window open if there's an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Application exited with an error." -ForegroundColor Red
    Read-Host "Press Enter to continue"
} 