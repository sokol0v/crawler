@echo off
chcp 1251 >nul
cd /d "%~dp0"

:menu
cls
echo ==========================
echo   КРАУЛЕР
echo ==========================
echo.
echo  1 - Запуск (по умолчанию)
echo  2 - Свои пути
echo  3 - README
echo  4 - Выход
echo.
set /p ch="Выберите (1-4): "

if "%ch%"=="1" goto :run1
if "%ch%"=="2" goto :run2
if "%ch%"=="3" goto :read
if "%ch%"=="4" exit /b

echo Неверно.
pause
goto :menu

:run1
set IN=urls.txt
set OUT=href_urls
goto :start

:run2
echo.
echo Введите путь к файлу с URL:
set /p IN="[urls.txt]: "
if "%IN%"=="" set IN=urls.txt
echo Введите папку для результатов:
set /p OUT="[href_urls]: "
if "%OUT%"=="" set OUT=href_urls
goto :start

:read
if exist README.md (notepad README.md) else echo README.md не найден.
pause
goto :menu

:start
echo.
echo Запуск: python crawler.py -i "%IN%" -o "%OUT%"
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
python crawler.py -i "%IN%" -o "%OUT%"
if defined VIRTUAL_ENV deactivate
echo.
pause
goto :menu