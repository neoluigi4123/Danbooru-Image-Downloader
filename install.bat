@echo off

:: Check if Python 3.10 is installed
python --version | findstr /r "3\.10"
if %errorlevel% neq 0 (
    echo Python 3.10 is not installed.
    echo Downloading and installing Python 3.10...
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

:: Download the "latest" file to determine the latest version of the script
echo Downloading the latest version information...
curl -L -o latest_version.txt https://raw.githubusercontent.com/neoluigi4123/Gelbooru-Image-Downloader/main/latest

:: Read the latest version number from the file
set /p VERSION=<latest_version.txt
echo Latest version is %VERSION%

:: Construct the download URL based on the version number
set DOWNLOAD_URL=https://raw.githubusercontent.com/neoluigi4123/Gelbooru-Image-Downloader/main/gelbooru_image_downloader_%VERSION%.py
echo Downloading %DOWNLOAD_URL%...
curl -L -o gelbooru_image_downloader.py %DOWNLOAD_URL%

:: Launch the app
echo Launching gelbooru_image_downloader.py...
python gelbooru_image_downloader.py

pause