@echo off
cd /d "%~dp0"
pip install -r requirements.txt
set FLASK_APP=main.py
set FLASK_ENV=development
tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
if "%ERRORLEVEL%"=="0" (
    start chrome http://127.0.0.1:5000
) else (
    where /q firefox
    if "%ERRORLEVEL%"=="0" (
        start firefox http://127.0.0.1:5000
    ) else (
        start http://127.0.0.1:5000
    )
)
flask run
pause
