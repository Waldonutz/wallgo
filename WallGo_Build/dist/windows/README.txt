WallGo - Windows Build Instructions

To build the Windows executable, you need to run PyInstaller on a Windows machine:

1. Copy all the project files to a Windows machine
2. Install Python 3.6 or higher
3. Create a virtual environment:
   python -m venv wallgo_env

4. Activate the virtual environment:
   wallgo_env\Scripts\activate

5. Install the required dependencies:
   pip install -r requirements.txt
   pip install pyinstaller

6. Build the Windows executable:
   pyinstaller --clean --noconfirm windows_build.spec

7. The executable will be created in the dist\WallGo directory

Note: The windows_build.spec file is already configured to create a standalone Windows executable.
