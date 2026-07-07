@echo off
cd /d "%~dp0"
echo [MASTER OQI] Avvio pipeline completa (ingestion + knowledge graph)...

if not exist ".venv\Scripts\activate.bat" (
    echo Creazione virtualenv...
    python -m venv .venv
)

call ".venv\Scripts\activate.bat"
pip install -r requirements.txt

python -m agents.pipeline

echo.
echo Pipeline completata. Premi un tasto per chiudere.
pause >nul

