@echo off

:: Check if Python 3.10 is installed
python --version | findstr /r "3\.10"
if %errorlevel% neq 0 (
    echo Python 3.10 is not installed.
    echo Downloading and installing Python 3.10...
    :: Replace the URL with the actual download URL for Python 3.10
    curl -o python-3.10.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    start /wait python-3.10.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-3.10.exe
)

:: Check if pip is installed
python -m pip --version
if %errorlevel% neq 0 (
    echo pip is not installed.
    echo Installing pip...
    python -m ensurepip --upgrade
)

:: Check if aiohttp is installed
python -m pip show aiohttp >nul 2>&1
if %errorlevel% neq 0 (
    echo aiohttp is not installed.
    echo Installing aiohttp...
    python -m pip install aiohttp
)

:: Check if pygelbooru is installed
python -m pip show pygelbooru >nul 2>&1
if %errorlevel% neq 0 (
    echo pygelbooru is not installed.
    echo Installing pygelbooru...
    python -m pip install pygelbooru
)

:: Launch the app
echo Launching gelbooru_image_downloader_1.0.py...
python gelbooru_image_downloader_1.0.py

pause
