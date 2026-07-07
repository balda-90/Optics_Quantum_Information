@echo off
cd /d "%~dp0"
echo [MASTER OQI] Avvio chat testuale con i materiali...

if not exist ".venv\Scripts\activate.bat" (
    echo Creazione virtualenv...
    python -m venv .venv
)

call ".venv\Scripts\activate.bat"
pip install -r requirements.txt

python -m agents.cli

echo.
echo Chat terminata. Premi un tasto per chiudere.
pause >nul

