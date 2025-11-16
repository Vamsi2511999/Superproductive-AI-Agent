# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend server
Write-Host "Starting Superproductive AI Agent Backend..." -ForegroundColor Green
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
