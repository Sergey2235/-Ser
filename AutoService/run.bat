@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   АвтоТранс - Система учёта заявок
echo ========================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Ошибка при запуске!
    echo Проверьте установку Python и зависимостей.
    echo.
    pause
)