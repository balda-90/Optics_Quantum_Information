@echo off
cd /d "%~dp0"
echo [MASTER OQI] Avvio chat VOCALE con i materiali...

if not exist ".venv\Scripts\activate.bat" (
    echo Creazione virtualenv...
    python -m venv .venv
)

call ".venv\Scripts\activate.bat"
pip install -r requirements.txt

python -m agents.voice_cli

echo.
echo Sessione vocale terminata. Premi un tasto per chiudere.
pause >nul

