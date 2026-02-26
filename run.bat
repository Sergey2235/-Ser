@echo off
chcp 65001 >nul
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Ошибка при запуске. Проверьте, что Python установлен и все файлы на месте.
    pause
)
