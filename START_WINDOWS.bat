@echo off
title Momna Birthday App - Keep this window open
cd /d "%~dp0"
echo.
echo MOMNA KHAN - BIRTHDAY APP
echo Keep this window open while viewing the website.
echo When ready, your browser should open automatically.
echo You can also open http://localhost:8501 yourself.
echo.

if not exist "app.py" goto missing_files
if not exist "assets\momna.jpeg" goto missing_files

if exist ".venv\Scripts\python.exe" goto check_environment
set "BIRTHDAY_PYTHON="
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if not errorlevel 1 set "BIRTHDAY_PYTHON=py -3"
if defined BIRTHDAY_PYTHON goto create_environment
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >nul 2>&1
if not errorlevel 1 set "BIRTHDAY_PYTHON=python"
if not defined BIRTHDAY_PYTHON goto missing_python

:create_environment
echo Setting up Python for the first launch...
%BIRTHDAY_PYTHON% -m venv .venv
if errorlevel 1 goto environment_error

:check_environment
".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"
if errorlevel 1 goto old_environment
".venv\Scripts\python.exe" -c "import streamlit, importlib, sys; assert streamlit.__version__ == '1.50.0'; importlib.import_module('tomllib' if sys.version_info >= (3, 11) else 'tomli')" >nul 2>&1
if not errorlevel 1 goto launch
echo Installing Streamlit. Please wait; the first launch needs internet.
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto installation_error

:launch
echo.
echo Starting your birthday website...
echo Address: http://localhost:8501
echo If the browser does not open, copy that address into Chrome or Edge.
echo To stop the app, press Ctrl+C in this window.
echo.
".venv\Scripts\python.exe" launch.py
echo.
echo The app has stopped. If an error appears above, copy that text.
pause
exit /b

:missing_files
echo ERROR: The app files are missing from this folder.
echo Right-click the downloaded ZIP, select Extract All, and open momna_birthday.
goto failed

:missing_python
echo ERROR: Python 3.9 or newer was not found. Python 3.12 is recommended.
echo Install it from https://www.python.org/downloads/ and enable Add Python to PATH.
goto failed

:environment_error
echo ERROR: Could not create the Python environment. See the details above.
goto failed

:old_environment
echo ERROR: This folder's .venv uses an older or unavailable Python version.
echo Install Python 3.12, rename the .venv folder, and run this launcher again.
goto failed

:installation_error
echo ERROR: Streamlit installation failed. Check the error above and your internet.
goto failed

:failed
pause
exit /b 1
