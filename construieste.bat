@echo off
rem Dublu-clic pe acest fisier: construieste dist\CriptoLab\CriptoLab.exe
cd /d "%~dp0"
py -3 construieste.py || python construieste.py
pause
