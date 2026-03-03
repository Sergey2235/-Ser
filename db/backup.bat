@echo off
chcp 65001 >nul
setlocal

:: Настройки
set DB_NAME=AutoService.db
set BACKUP_DIR=backup
set DATE=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%
set DATE=%DATE: =0%

:: Создание папки backup
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Копирование базы
copy "%DB_NAME%" "%BACKUP_DIR%\%DB_NAME%_%DATE%.bak" >nul

if %errorlevel% == 0 (
    echo [OK] Резервная копия создана: %BACKUP_DIR%\%DB_NAME%_%DATE%.bak
) else (
    echo [ERROR] Не удалось создать резервную копию
)

pause