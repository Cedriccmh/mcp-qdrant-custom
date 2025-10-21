@echo off
echo ========================================
echo Killing Process on Port 8765
echo ========================================
echo.

set PORT=8765

echo Checking for processes using port %PORT%...
netstat -ano | findstr :%PORT% | findstr LISTENING >nul 2>&1

if %errorlevel% equ 0 (
    echo Found process(es) using port %PORT%:
    netstat -ano | findstr :%PORT% | findstr LISTENING
    echo.
    echo Attempting to kill...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%PORT% ^| findstr LISTENING') do (
        echo Killing PID: %%a
        taskkill /F /T /PID %%a
    )
    echo.
    timeout /t 2 /nobreak >nul
    
    REM Check again
    netstat -ano | findstr :%PORT% | findstr LISTENING >nul 2>&1
    if %errorlevel% equ 0 (
        echo WARNING: Port %PORT% is still in use!
        netstat -ano | findstr :%PORT% | findstr LISTENING
    ) else (
        echo SUCCESS: Port %PORT% is now free!
    )
) else (
    echo Port %PORT% is already free.
)

echo.
pause