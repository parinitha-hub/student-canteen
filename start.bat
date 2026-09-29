@echo off
title Savitha Canteen - Food Order & AI Demand Predictor
color 0E

cd /d "%~dp0"

echo ======================================================================
echo           SAVITHA CANTEEN - CAMPUS DINING & KITCHEN AI
echo ======================================================================
echo.
echo [1/3] Checking Python Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found in PATH.
    echo [*] Opening Savitha Canteen in Instant Client AI Mode...
    start "" index.html
    goto done
)

echo [2/3] Checking Backend Server Status...
netstat -ano | findstr :5000 | findstr LISTENING >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Savitha Canteen Backend Server is already active on Port 5000.
) else (
    echo [*] Launching Python Flask ML Backend on Port 5000...
    start "Savitha Canteen Backend Server" /min python run.py
    
    :: Wait up to 5 seconds for backend to start listening
    for /l %%i in (1,1,5) do (
        timeout /t 1 /nobreak >nul
        netstat -ano | findstr :5000 | findstr LISTENING >nul 2>&1
        if not errorlevel 1 goto server_ready
    )
)

:server_ready
echo [3/3] Opening Website in Browser...
start http://127.0.0.1:5000

echo.
echo ======================================================================
echo  Server is active on: http://127.0.0.1:5000
echo.
echo  PORTALS:
echo   - Student / Customer: Fast 1-Click Login (No Password!)
echo   - Kitchen Staff:      Secure PIN / Password Protected Portal
echo ======================================================================
:done
pause
