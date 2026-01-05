@echo off
REM Setup script for Buchführung application (Windows)

echo ============================================
echo Buchführung - Setup Script
echo ============================================
echo.

REM Check Python version
echo Checking Python version...
python --version

if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies.
    exit /b 1
)

echo.
echo ============================================
echo Setup completed successfully!
echo ============================================
echo.
echo To run the application:
echo   python src/main.py
echo.
echo To create sample data:
echo   python create_sample_data.py
echo.
echo To run tests:
echo   python test_functionality.py
echo.
pause
