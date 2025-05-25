@echo off
echo Building WallGo for Windows...

REM Create virtual environment if it doesn't exist
if not exist wallgo_env (
    python -m venv wallgo_env
)

REM Activate virtual environment
call wallgo_env\Scripts\activate

REM Install required packages
pip install -r requirements.txt
pip install pyinstaller

REM Build the executable
pyinstaller --clean --noconfirm windows_build.spec

echo Build complete! The executable is in the dist\WallGo directory.
pause
