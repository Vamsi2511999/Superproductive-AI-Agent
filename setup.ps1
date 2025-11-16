# Superproductive AI Agent - Installation Script

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Superproductive AI Agent - Setup" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = py --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 16 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Setting up Backend" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Setup Backend
Set-Location backend

Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
py -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Setting up environment file..." -ForegroundColor Yellow
if (-Not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file. Please add your OpenAI API key!" -ForegroundColor Green
    Write-Host "  Edit backend\.env and set OPENAI_API_KEY=your-key-here" -ForegroundColor Yellow
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

Set-Location ..

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Setting up Frontend" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Setup Frontend
Set-Location frontend

Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Set-Location ..

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Green
Write-Host "1. Add your OpenAI API key to backend\.env" -ForegroundColor White
Write-Host "2. Open TWO PowerShell terminals:" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 1 (Backend):" -ForegroundColor Yellow
Write-Host "   cd backend" -ForegroundColor White
Write-Host "   .\start.ps1" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 2 (Frontend):" -ForegroundColor Yellow
Write-Host "   cd frontend" -ForegroundColor White
Write-Host "   .\start.ps1" -ForegroundColor White
Write-Host ""
Write-Host "3. Open http://localhost:5173 in your browser" -ForegroundColor White
Write-Host ""
