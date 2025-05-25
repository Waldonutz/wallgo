# WallGo Build Instructions

## Mac Application

The Mac application has been built and is available in the project root directory as `WallGo.app`. You can run it by double-clicking on it in Finder.

### Rebuilding the Mac Application

If you need to rebuild the Mac application:

1. Activate the virtual environment:
   ```
   source wallgo_env/bin/activate
   ```

2. Run PyInstaller with the cross-platform spec file:
   ```
   pyinstaller --clean --noconfirm --distpath ./WallGo_Build/dist/mac cross_platform_build.spec
   ```

3. The application will be created in `./WallGo_Build/dist/mac/WallGo.app`

## Windows Application

To build the Windows application, you need to run PyInstaller on a Windows machine:

### Option 1: Using the batch file

1. Copy all project files to a Windows machine
2. Install Python 3.6 or higher
3. Run the `build_windows.bat` batch file by double-clicking it
4. The executable will be created in the `dist\WallGo` directory

### Option 2: Manual build

1. Copy all project files to a Windows machine
2. Install Python 3.6 or higher
3. Create a virtual environment:
   ```
   python -m venv wallgo_env
   ```

4. Activate the virtual environment:
   ```
   wallgo_env\Scripts\activate
   ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   pip install pyinstaller
   ```

6. Build the Windows executable:
   ```
   pyinstaller --clean --noconfirm windows_build.spec
   ```

7. The executable will be created in the `dist\WallGo` directory

## Notes

- The Mac application is built for macOS and will only run on Mac systems
- The Windows executable will only run on Windows systems
- Both builds include all necessary dependencies and should run without requiring Python to be installed
