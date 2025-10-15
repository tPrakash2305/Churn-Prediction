# Quick Installation Script for Customer Churn Prediction System
# Run this in PowerShell from the project directory

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Customer Churn Prediction System" -ForegroundColor Cyan
Write-Host "  Quick Installation Script" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/4] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "      $pythonVersion" -ForegroundColor Green

# Install required packages
Write-Host ""
Write-Host "[2/4] Installing required packages..." -ForegroundColor Yellow
Write-Host "      This may take 5-10 minutes..." -ForegroundColor Gray

# Install packages one by one to show progress
$packages = @(
    "pandas==2.0.3",
    "numpy==1.24.3",
    "matplotlib==3.7.2",
    "seaborn==0.12.2",
    "scikit-learn==1.3.0",
    "xgboost==1.7.6",
    "imbalanced-learn==0.11.0",
    "shap==0.42.1",
    "streamlit==1.25.0",
    "joblib==1.3.2",
    "plotly==5.15.0"
)

foreach ($package in $packages) {
    Write-Host "      Installing $package..." -ForegroundColor Gray
    pip install $package --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Failed to install $package" -ForegroundColor Red
    }
}

# Verify installation
Write-Host ""
Write-Host "[3/4] Verifying installation..." -ForegroundColor Yellow
python verify_setup.py

# Final instructions
Write-Host ""
Write-Host "[4/4] Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "      1. Download dataset:" -ForegroundColor White
Write-Host "         https://www.kaggle.com/datasets/blastchar/telco-customer-churn" -ForegroundColor Cyan
Write-Host "         Place as: data/raw/telco_churn.csv" -ForegroundColor Gray
Write-Host ""
Write-Host "      2. Train models:" -ForegroundColor White
Write-Host "         python src/train.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "      3. Launch dashboard:" -ForegroundColor White
Write-Host "         streamlit run app/app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
