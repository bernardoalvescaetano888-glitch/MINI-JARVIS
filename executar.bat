@echo off
title MINI-JARVIS 2.0
cd /d "%~dp0"
python jarvis_gui.py
if errorlevel 1 (
  echo.
  echo A interface grafica falhou — abrindo a versao de terminal...
  python jarvis.py
)
pause
