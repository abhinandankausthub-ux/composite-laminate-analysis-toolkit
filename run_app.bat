@echo off
title Composite Laminate Toolkit Launcher

echo ==========================================
echo     Composite Laminate Toolkit
echo ==========================================
echo.

REM ------------------------------------------------
REM Check if Python is installed
REM ------------------------------------------------
python --version >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not added to PATH.
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit
)

echo Python detected.
python --version
echo.

REM ------------------------------------------------
REM Upgrade pip
REM ------------------------------------------------
echo Upgrading pip...
python -m pip install --upgrade pip

echo.

REM ------------------------------------------------
REM Install requirements
REM ------------------------------------------------
echo Installing required packages from requirements.txt
echo.

pip install -r requirements.txt

echo.

REM ------------------------------------------------
REM Verify Streamlit installation
REM ------------------------------------------------
python -c "import streamlit" >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Streamlit failed to install.
    echo Please check your internet connection.
    pause
    exit
)

echo All dependencies installed successfully.
echo.

REM ------------------------------------------------
REM Launch the Streamlit application
REM ------------------------------------------------
echo Starting Composite Laminate Toolkit...
echo.

streamlit run app.py

echo.
echo Application closed.

pause
